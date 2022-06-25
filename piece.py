import pygame
import os

# load images for black pieces
b_bishop = pygame.image.load(os.path.join("img","black_bishop.png"))
b_king = pygame.image.load(os.path.join("img", "black_king.png"))
b_knight = pygame.image.load(os.path.join("img", "black_knight.png"))
b_pawn = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_queen = pygame.image.load(os.path.join("img", "black_queen.png"))
b_rook = pygame.image.load(os.path.join("img", "black_rook.png"))

# load images for white pieces
w_bishop = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_king = pygame.image.load(os.path.join("img", "white_king.png"))
w_knight = pygame.image.load(os.path.join("img", "white_knight.png"))
w_pawn = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_queen = pygame.image.load(os.path.join("img", "white_queen.png"))
w_rook = pygame.image.load(os.path.join("img", "white_rook.png"))

b = [b_bishop, b_king, b_knight, b_pawn, b_queen, b_rook]
w = [w_bishop, w_king, w_knight, w_pawn, w_queen, w_rook]
n = len(b)
B, W = [], []
for i in range(n):
    B.append(pygame.transform.scale(b[i],(55,55)))
    W.append(pygame.transform.scale(w[i],(55,55)))

# create classes for each piece
class Piece:

    img = -1
    rect = (113,113,525,525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        """
        :param row: int
        :param col: int
        :param color: str
        """
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False
        self.rook = False

    def isSelected(self):
        """
        to return if piece is selected
        :return: bool
        """
        return self.selected

    def update_valid_moves(self,board):
        """
        possible position where piece can be placed on the board
        :param board: matrix
        :return: None
        """
        self.move_list = self.valid_moves(board)

    def change_pos(self,pos):
        """
        New position that piece moves to
        :param pos: list (new position)
        :return: None
        """
        self.row = pos[0]
        self.col = pos[1]

    def draw(self,win,color):
        """
        draw piece on the board
        :param win: surface
        :param color: str
        :return: None
        """
        # draw piece on the board based on the row and col
        if self.color == 'w':
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]
        x = 4 + self.startX + self.col*self.rect[2]/8
        y = 3 + self.startY + self.row*self.rect[3]/8
        if self.selected and self.color == color:
            pygame.draw.rect(win,(255,0,0),(x,y,62,62),4)
        win.blit(drawThis,(x,y))

class Bishop(Piece):

    img = 0

    def __init__(self,row,col,color):
        super().__init__(row,col,color)

    def valid_moves(self,board):
        """
        to get all valid move position for Bishop
        :param board: matrix
        :return: list
        """
        i,j=self.row,self.col
        moves=[]
        djR=j-1
        djL=j+1
        # check for going top right
        for di in range(i+1,8):
            if djR>-1:
                p=board[di][djR]
                # if no piece on the pos
                if p == 0:
                    moves.append((djR,di))
                # if another color of piece on the pos
                elif p.color != self.color:
                    moves.append((djR,di))
                    break
                else:
                    break
            else:
                break
            djR -= 1
        # check for going bottom left
        for di in range(i-1,-1,-1):
            if djL<8:
                p=board[di][djL]
                if p==0:
                    moves.append((djL,di))
                elif p.color != self.color:
                    moves.append((djL,di))
                    break
                else:
                    break
            else:
                break
            djL += 1
        djR=j+1
        djL=j-1
        # check for going to top left
        for di in range(i-1,-1,-1):
            if djL>-1:
                p=board[di][djL]
                if p == 0:
                    moves.append((djL,di))
                elif p.color != self.color:
                    moves.append((djL,di))
                    break
                else:
                    break
            else:
                break
            djL -= 1
        # check for going to bottom right
        for di in range(i+1,8):
            if djR < 8:
                p = board[di][djR]
                if p == 0:
                    moves.append((djR,di))
                elif p.color != self.color:
                    moves.append((djR,di))
                    break
                else:
                    break
            else:
                break
            djR += 1
        return moves

class King(Piece):

    img=1

    def __init__(self, row, col, color):
        super().__init__(row,col,color)
        self.king=True
        self.moved=False

    def valid_moves(self,board):
        """
        to get the valid moves for King
        :param board: matrix
        :return: list
        """
        i,j = self.row,self.col
        # moves to store the pos in (col,row)
        moves=[]
        if i>0:
            # check top left
            if j>0:
                p=board[i-1][j-1]
                if p == 0:
                    moves.append((j-1,i-1))
                elif p.color != self.color:
                    moves.append((j-1,i-1))
            # check top
            p=board[i-1][j]
            if p==0:
                moves.append((j,i-1))
            elif p.color != self.color:
                moves.append((j,i-1))
            # check top right
            if j<7:
                p=board[i-1][j+1]
                if p==0:
                    moves.append((j+1,i-1))
                elif p.color != self.color:
                    moves.append((j+1,i-1))
        if i<7:
            # check bottom left
            if j>0:
                p=board[i+1][j-1]
                if p == 0:
                    moves.append((j-1,i+1))
                elif p.color != self.color:
                    moves.append((j-1,i+1))
            # check bottom
            p=board[i+1][j]
            if p == 0:
                moves.append((j, i + 1))
            elif p.color != self.color:
                moves.append((j, i + 1))
            # check bottom right
            if j<7:
                p=board[i+1][j+1]
                if p == 0:
                    moves.append((j+1,i+1))
                elif p.color != self.color:
                    moves.append((j+1,i+1))
        # check right
        if j<7:
            p=board[i][j+1]
            if p == 0:
                moves.append((j + 1,i))
            elif p.color != self.color:
                moves.append((j + 1, i))
        # check left
        if j>0:
            p=board[i][j-1]
            if p == 0:
                moves.append((j - 1,i))
            elif p.color != self.color:
                moves.append((j - 1, i))
        return moves

class Knight(Piece):

    img=2

    def __init__(self,row,col,color):
        super().__init__(row,col,color)

    def valid_moves(self,board):
        """
        to get valid moves for knight
        :param board: matrix
        :return: list
        """
        i,j=self.row,self.col
        moves=[]
        # check down left
        if i<6 and j>0:
            p=board[i+2][j-1]
            if p == 0:
                moves.append((j - 1,i+2))
            elif p.color != self.color:
                moves.append((j - 1, i+2))
        if i<7 and j>1:
            p=board[i+1][j-2]
            if p == 0:
                moves.append((j - 2,i+1))
            elif p.color != self.color:
                moves.append((j - 2, i+1))
        # check up left
        if i>1 and j>0:
            p=board[i-2][j-1]
            if p == 0:
                moves.append((j - 1,i-2))
            elif p.color != self.color:
                moves.append((j - 1, i-2))
        if i>0 and j>1:
            p=board[i-1][j-2]
            if p == 0:
                moves.append((j - 2,i-1))
            elif p.color != self.color:
                moves.append((j - 2, i-1))
        # check down right
        if i<6 and j<7:
            p=board[i+2][j+1]
            if p == 0:
                moves.append((j + 1,i+2))
            elif p.color != self.color:
                moves.append((j + 1, i+2))
        if i<7 and j<6:
            p=board[i+1][j+2]
            if p == 0:
                moves.append((j+2,i+1))
            elif p.color != self.color:
                moves.append((j+2,i+1))
        # check up right
        if i>1 and j<7:
            p=board[i-2][j+1]
            if p == 0:
                moves.append((j + 1,i-2))
            elif p.color != self.color:
                moves.append((j + 1, i-2))
        if i>0 and j<6:
            p=board[i-1][j+2]
            if p == 0:
                moves.append((j + 2,i-1))
            elif p.color != self.color:
                moves.append((j + 2, i-1))
        return moves

class Pawn(Piece):

    img=3

    def __init__(self,row,col,color):
        super().__init__(row,col,color)
        self.first=True
        self.pawn=True

    def promotion(self,row):
        """
        to check if pawn will be promoted
        :param row: int
        :return: bool
        """
        if row == 0 or row == 7:
            return True
        return False

    def valid_moves(self,board):
        """
        to check valid move for pawn
        :param board: matrix
        :return: list
        """
        i,j=self.row,self.col
        moves=[]
        try:
            # black pawn
            if self.color == 'b':
                # check down
                if i<7:
                    p=board[i+1][j]
                    if p==0:
                        moves.append((j,i+1))
                    # check diagonal to right and left
                    if j<7:
                        p=board[i+1][j+1]
                        if p != 0 and p.color != self.color:
                            moves.append((j+1,i+1))
                    if j>0:
                        p=board[i+1][j-1]
                        if p != 0 and p.color != self.color:
                            moves.append((j-1,i+1))
                if self.first:
                    p=board[i+2][j]
                    if p==0 and board[i+1][j]==0:
                        moves.append((j,i+2))
            # white pawn
            else:
                # check up
                if i > 0:
                    p = board[i - 1][j]
                    if p == 0:
                        moves.append((j, i - 1))
                    # check diagonal to right and left
                    if j < 7:
                        p = board[i - 1][j + 1]
                        if p != 0 and p.color != self.color:
                            moves.append((j + 1, i - 1))
                    if j > 0:
                        p = board[i - 1][j - 1]
                        if p != 0 and p.color != self.color:
                            moves.append((j - 1, i - 1))
                if self.first:
                    p = board[i - 2][j]
                    if p == 0 and board[i - 1][j] == 0:
                        moves.append((j, i - 2))
        except:
            pass
        return moves

class Queen(Piece):

    img=4

    def __init__(self,row,col,color):
        super().__init__(row,col,color)

    def valid_moves(self,board):
        """
        to check valid moves for Queen
        :param board: matrix
        :return: list
        """
        i,j = self.row,self.col
        moves=[]
        djR,djL=j+1,j-1
        # top right
        for di in range(i-1,-1,-1):
            if djR<8:
                p=board[di][djR]
                if p==0:
                    moves.append((djR,di))
                elif p.color != self.color:
                    moves.append((djR,di))
                    break
                else:
                    break
            else:
                break
            djR +=1
        # bottom left
        for di in range(i+1,8):
            if djL>-1:
                p=board[di][djL]
                if p==0:
                    moves.append((djL,di))
                elif p.color != self.color:
                    moves.append((djL,di))
                    break
                else:
                    break
            else:
                break
            djL-=1
        djR,djL=j+1,j-1
        # top left
        for di in range(i-1,-1,-1):
            if djL>-1:
                p=board[di][djL]
                if p==0:
                    moves.append((djL,di))
                elif p.color != self.color:
                    moves.append((djL,di))
                    break
                else:
                    break
            else:
                break
            djL -=1
        # bottom right
        for di in range(i+1,8):
            if djR<8:
                p=board[di][djR]
                if p==0:
                    moves.append((djR,di))
                elif p.color != self.color:
                    moves.append((djR,di))
                    break
                else:
                    break
            else:
                break
            djR+=1
        # check up
        for x in range(i-1,-1,-1):
            p=board[x][j]
            if p==0:
                moves.append((j,x))
            elif p.color != self.color:
                moves.append((j,x))
                break
            else:
                break
        # check down
        for x in range(i+1,8):
            p=board[x][j]
            if p==0:
                moves.append((j,x))
            elif p.color != self.color:
                moves.append((j,x))
                break
            else:
                break
        # check left
        for y in range(j-1,-1,-1):
            p = board[i][y]
            if p==0:
                moves.append((y,i))
            elif p.color != self.color:
                moves.append((y,i))
                break
            else:
                break
        # check right
        for y in range(j+1,8):
            p=board[i][y]
            if p==0:
                moves.append((y,i))
            elif p.color != self.color:
                moves.append((y,i))
                break
            else:
                break
        return moves

class Rook(Piece):

    img=5

    def __init__(self,row,col,color):
        super().__init__(row,col,color)
        self.moved=False
        self.rook=True

    def valid_moves(self,board):
        """
        to check valid moves for Rook
        :param board: matrix
        :return: list
        """
        i,j = self.row,self.col
        moves=[]
        # check up
        for x in range(i-1,-1,-1):
            p=board[x][j]
            if p==0:
                moves.append((j,x))
            elif p.color != self.color:
                moves.append((j,x))
                break
            else:
                break
        # check down
        for x in range(i+1,8):
            p=board[x][j]
            if p==0:
                moves.append((j,x))
            elif p.color != self.color:
                moves.append((j,x))
                break
            else:
                break
        # check left
        for y in range(j-1,-1,-1):
            p = board[i][y]
            if p==0:
                moves.append((y,i))
            elif p.color != self.color:
                moves.append((y,i))
                break
            else:
                break
        # check right
        for y in range(j+1,8):
            p=board[i][y]
            if p==0:
                moves.append((y,i))
            elif p.color != self.color:
                moves.append((y,i))
                break
            else:
                break
        return moves
