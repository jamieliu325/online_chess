import pygame
import os
from client import Network

pygame.font.init()
# load bg images
board = pygame.transform.scale(pygame.image.load(os.path.join("img", "board_alt.png")), (750, 750))
chessbg = pygame.image.load(os.path.join("img", "chessbg.png"))
rect = (113, 113, 525, 525)

turn = "w"


def menu_screen(win):
    """
    display menu screen and run the main loop
    :param win: surface
    :return: None
    """
    global bo, chessbg
    run = True
    offline = False

    while run:
        win.blit(chessbg, (0, 0))
        font = pygame.font.SysFont("comicsans", 45)
        # to check if it's connected to the server
        if offline:
            off = font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))
            win.blit(off, (width / 2 - off.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    # connect to the server and run the main loop
                    bo = connect()
                    run = False
                    main()
                    break
                except:
                    print("Server Offline")
                    offline = True


def redraw_gameWindow(win, bo, p1, p2, color, ready):
    """
    draw the game window
    :param win: surface
    :param bo: matrix
    :param p1: int
    :param p2: int
    :param color: str
    :param ready: bool
    :return: None
    """
    # draw the window
    win.blit(board, (0, 0))
    bo.draw(win, color)

    font = pygame.font.SysFont("comicsans", 20)
    txt = font.render("Press q to Quit or Resign", 1, (255, 255, 255))
    win.blit(txt, (10, 10))

    # display the timers for both player
    formatTime1 = str(int(p1 // 60)) + ":" + str(int(p1 % 60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1 % 60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2 % 60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]
    try:
        txt2 = font.render(bo.p1Name + "\'s Time: " + str(formatTime2), 1, (255, 255, 255))
        txt1 = font.render(bo.p2Name + "\'s Time: " + str(formatTime1), 1, (255, 255, 255))
    except Exception as e:
        print(e)
    win.blit(txt2, (530, 10))
    win.blit(txt1, (530, 700))

    if not ready:
        show = "Waiting for Player"
        if color == "s":
            show = "Waiting for Players"
        font = pygame.font.SysFont("comicsans", 60)
        txt3 = font.render(show, 1, (255, 0, 0))
        win.blit(txt3, (width / 2 - txt3.get_width() / 2, 300))

    # show player color
    font = pygame.font.SysFont("comicsans", 25)
    if color == "w":
        txt4 = font.render("YOU ARE WHITE", 1, (255, 0, 0))
        win.blit(txt4, (width / 2 - txt4.get_width() / 2, 10))
    else:
        txt5 = font.render("YOU ARE BLACK", 1, (255, 0, 0))
        win.blit(txt5, (width / 2 - txt5.get_width() / 2, 10))

    # show turn
    if bo.turn == color:
        txt6 = font.render("YOUR TURN", 1, (255, 0, 0))
        win.blit(txt6, (width / 2 - txt6.get_width() / 2, 700))
    else:
        txt7 = font.render("THEIR TURN", 1, (255, 0, 0))
        win.blit(txt7, (width / 2 - txt7.get_width() / 2, 700))

    # show check
    if bo.is_checked(color):
        font = pygame.font.SysFont("comicsans", 80)
        txt8 = font.render("CHECK!", 1, (255, 0, 0))
        win.blit(txt8, (width/2-txt8.get_width()/2,200))

    pygame.display.update()

def end_screen(win, text):
    """
    display end screen
    :param win: surface
    :param text: str
    :return: None
    """

    font = pygame.font.SysFont("comicsans", 60)
    txt = font.render(text, 1, (255, 0, 0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False



def click(pos):
    """
    :return: pos (x, y) in col and row
    """
    x = pos[0]
    y = pos[1]
    if rect[0] < x < rect[0] + rect[2]:
        if rect[1] < y < rect[1] + rect[3]:
            divX = x - rect[0]
            divY = y - rect[1]
            i = int(divX / (rect[2] / 8))
            j = int(divY / (rect[3] / 8))
            return i, j
    return -1, -1

def connect():
    """
    :return: Network class
    """
    global n
    n = Network()
    return n.board


def main():
    global turn, bo, name

    color = bo.start_user
    count = 0

    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    run = True

    while run:
        if not color == "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
        except Exception as e:
            print(e)
            end_screen(win, "Other player left")
            run = False
            break

        # to check if it's over time
        if p1Time <= 0:
            bo = n.send("winner b")
        elif p2Time <= 0:
            bo = n.send("winner w")

        # if there is a winner
        if bo.winner == "w":
            end_screen(win, "White is the Winner!")
            run = False
        elif bo.winner == "b":
            end_screen(win, "Black is the winner")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # who quit lose game
                    if color == "w":
                        bo = n.send("winner b")
                    else:
                        bo = n.send("winner w")

            if event.type == pygame.MOUSEBUTTONUP:
                if color == bo.turn and bo.ready:
                    pos = pygame.mouse.get_pos()
                    # to send update moves request to the server and receive data
                    bo = n.send("update moves")
                    # to send data for click pos to the server and receive board data
                    i, j = click(pos)
                    bo = n.send("select " + str(i) + " " + str(j) + " " + color)
            redraw_gameWindow(win, bo, p1Time, p2Time, color, bo.ready)
    # disconnected
    n.disconnect()
    bo = 0
    menu_screen(win)


name = input("Please type your name: ")
# set up window
width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")
menu_screen(win)


