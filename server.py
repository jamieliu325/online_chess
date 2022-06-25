import socket
from _thread import *
from board import Board
import pickle
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server = '192.168.0.126'
port = 5555
# translate the host name to IPv4 address format
server_ip = socket.gethostbyname(server)

# assigns IP address and port number to a socket instance
try:
    s.bind((server,port))
except socket.error as e:
    print(e)

# socket is ready for accepting connections
s.listen()
print('Waiting for a connection')

# variables
connections = 0
games = {0:Board(8,8)}

def threaded_client(conn,game):
    """
    connect client to the game
    :param conn: socket connection
    :param game: int
    :return: None
    """
    global games,connections

    bo = games[game]

    # assign a color to player
    if connections % 2 ==0:
        currentID = 'w'
    else:
        currentID = 'b'

    bo.start_user = currentID
    # pickle the object
    data_string = pickle.dumps(bo)

    # start the game and timer
    if currentID == 'b':
        bo.ready = True
        bo.startTime = time.time()
    # send data to the server
    conn.send(data_string)
    connections += 1
    while True:
        if game not in games:
            break
        try:
            # receive data from server
            d = conn.recv(8192*3)
            data = d.decode('utf-8')
            if not d:
                break
            else:
                # if selected a piece or a pos
                if data.count('select')==1:
                    all = data.split(" ")
                    col = int(all[1])
                    row = int(all[2])
                    color = all[3]
                    bo.select(col,row,color)
                # if game has a winner
                if data == "winner b":
                    bo.winner="b"
                    print("Player b won in game", game)
                if data == "winner w":
                    bo.winner="w"
                    print("Player w won in game", game)
                # if update moves
                if data == "update moves":
                    bo.update_moves()
                # if receive a player name
                if data.count("name") == 1:
                    name=data.split(" ")[1]
                    if currentID == 'b':
                        bo.p2Name = name
                    elif currentID == 'w':
                        bo.p1Name = name
                # start the timer if game is ready
                if bo.ready:
                    if bo.turn == "w":
                        bo.time1 = 900 - (time.time()-bo.startTime) - bo.storedTime1
                    else:
                        bo.time2 = 900 - (time.time()-bo.startTime) - bo.storedTime2
                sendData=pickle.dumps(bo)
            conn.sendall(sendData)
        except Exception as e:
            print(e)

    # disconnected
    connections -= 1
    # end a game
    try:
        del games[game]
        print("Game", game, "ended")
    except:
        pass
    print("Player",name,"left game", game)
    conn.close()

while True:
    if connections < 6:
        # return a socket object when a client connects
        conn,addr=s.accept()
        g=-1
        print("New Connection")

        # assign the new connection to a non-ready game
        for game in games.keys():
            if games[game].ready == False:
                g=game

        # assign a game key
        if g==-1:
            try:
                g=list(games.keys())[-1]+1
                games[g]=Board(8,8)
            except:
                g=0
                games[g]=Board(8,8)

        print("Number of connections:", connections+1)
        print("Number of games:", len(games))

        start_new_thread(threaded_client,(conn,g))


