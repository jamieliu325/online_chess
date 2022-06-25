from piece import Bishop, King, Rook, Pawn, Queen, Knight
import time
import pygame
pygame.font.init()
class Board:
    rect=(113,113,525,525)
    startX,startY=rect[0],rect[1]
    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.ready=False
        self.last=None
        self.copy=True
        self.board=[[0 for y in range(cols)] for x in range(rows)]
        self.p1Name="Player 1"
        self.p2Name="Player 2"
        self.time1 = 900
        self.time2 = 900
        self.storedTime1=0
        self.storedTime2=0
        self.winner=None
        self.startTime=time.time()
        self.turn='w'

        # set up black and white pieces on the board
        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")

    def update_moves(self):
        """
        update valid moves for all the pieces on the board
        :return: None
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    def draw(self,win,color):
        """
        draw board and highlight the last move
        :param win: surface
        :param color: str
        :return: None
        """
        if self.last and color == self.turn:
            y,x = self.last[0]
            y1,x1 = self.last[1]
            xx = 4+self.startX+x*self.rect[2]/8
            yy = 3+self.startY+y*self.rect[3]/8
            pygame.draw.circle(win,(0,0,225),(xx+32,yy+30),34,4)
            xx1 = 4+self.startX+x1*self.rect[2]/8
            yy1 = 3+self.startY+y1*self.rect[3]/8
            pygame.draw.circle(win,(0,0,225),(xx1+32,yy1+30),34,4)
        s=None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win,color)
                    if self.board[i][j].isSelected:
                        s=(i,j)

    def get_danger_moves(self,color):
        """
        to get all valid moves for opponent on the board
        :param color: str
        :return: list
        """
        danger_moves=[]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j].color != color:
                    for move in self.board[i][j].move_list:
                        danger_moves.append(move)
        return danger_moves

    def is_checked(self,color):
        """
        return if is checked
        :param color: str
        :return: bool
        """
        global win
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        king_pos = (-1,-1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j].king and self.board[i][j].color == color:
                    king_pos = (j,i)
        if king_pos in danger_moves:
            return True
        return False

    def select(self,col,row,color):
        """
        to select a piece or pos
        :param col: str
        :param row: int
        :param color: int
        :return: None
        """
        changed = False
        prev=(-1,-1)
        # to get the selected piece
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0 and self.board[i][j].selected:
                    prev=(i,j)
        # to move piece to an empty pos
        if self.board[row][col] == 0 and prev != (-1,-1):
            moves = self.board[prev[0]][prev[1]].move_list
            if (col,row) in moves:
                changed = self.move(prev,(row,col),color)
        else:
            # if select an empty pos
            if prev == (-1,-1):
                self.reset_selected()
                if self.board[row][col] != 0:
                    self.board[row][col].selected = True
            else:
                # to capture a piece
                if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                    moves = self.board[prev[0]][prev[1]].move_list
                    if (col,row) in moves:
                        changed = self.move(prev,(row,col),color)

                else:
                    #  if clicked on the piece in the same color
                    if self.board[row][col].color == color:
                        self.reset_selected()
                        # castling, rook is selected and not moved, rook is going to the pos of king
                        if self.board[prev[0]][prev[1]].rook and self.board[row][col].king:
                                if self.board[prev[0]][prev[1]].moved == False and self.board[row][col].moved == False:
                                    castle = True
                                    # rook is at the left side of king
                                    dangerMoves = self.get_danger_moves(color)
                                    if prev[1]<col:
                                        # to check if any piece between rook and king
                                        for j in range(prev[1]+1,col):
                                            if self.board[row][j] != 0 or (j,row) in dangerMoves:
                                                castle = False
                                                break
                                        if castle:
                                            changed = self.move(prev,(row,3),color)
                                            changed = self.move((row,col),(row,2),color)
                                        if not changed:
                                            self.board[row][col].selected=True
                                    # rook is at the right side of king
                                    else:
                                        for j in range(col+1,prev[1]):
                                            if self.board[row][j] != 0 or (j,row) in dangerMoves:
                                                castle = False
                                                break
                                        if castle:
                                            changed = self.move(prev,(row,6),color)
                                            changed = self.move((row,col),(row,5),color)
                                        if not changed:
                                            self.board[row][col].selected = True
                                # select king if castle is not initiated
                                else:
                                    self.board[row][col].selected = True

        # to change the turn
        if changed:
            if self.turn == 'w':
                self.turn = 'b'
                self.reset_selected()
            else:
                self.turn = 'w'
                self.reset_selected()


    def reset_selected(self):
        """
        to clear selection
        :return: None
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def move(self,start,end,color):
        """
        to move piece from start to end
        :param start: tuple
        :param end: tuple
        :param color: str
        :return: bool
        """
        changed=True
        nBoard = self.board[:]
        if nBoard[start[0]][start[1]].pawn:
            nBoard[start[0]][start[1]].first = False
        elif nBoard[start[0]][start[1]].rook:
            nBoard[start[0]][start[1]].moved = True
        elif nBoard[start[0]][start[1]].king:
            nBoard[start[0]][start[1]].moved = True
        # change position
        nBoard[start[0]][start[1]].change_pos((end[0],end[1]))
        # change piece
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board =nBoard
        # if checked, reverse the move
        if self.is_checked(color):
            changed = False
            nBoard=self.board[:]
            if nBoard[end[0]][end[1]].pawn:
                nBoard[end[0]][end[1]].first = True
            elif nBoard[end[0]][end[1]].rook:
                nBoard[end[0]][end[1]].moved = False
            elif nBoard[end[0]][end[1]].king:
                nBoard[end[0]][end[1]].moved = False
            # change position
            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            # change piece
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.board = nBoard
        else:
            self.reset_selected()
        # update move list and time for player after a move
        if changed:
            if nBoard[end[0]][end[1]].pawn:
                if nBoard[end[0]][end[1]].promotion(end[0]):
                    nBoard[end[0]][end[1]] = Queen(end[0],end[1],color)
        self.update_moves()
        if changed:
            self.last = [start,end]
            if self.turn == 'w':
                self.storedTime1 += (time.time()-self.startTime)
            else:
                self.storedTime2 += (time.time()-self.startTime)
            self.startTime=time.time()

        return changed