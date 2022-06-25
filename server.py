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
spectartor_ids = []
specs = 0

def read_specs():
    """
    read or write specs file
    :return: None
    """
    global spectartor_ids
    spectartor_ids=[]
    try:
        with open("specs.txt","r") as file:
            for line in file:
                spectartor_ids.append((line.strip()))
    except:
        print("No specs.txt file found, creating one ...")
        open("specs.txt","w")

def threaded_client(conn,game,spec=False):
    """
    connect client to the game
    :param conn: socket connection
    :param game: int
    :param spec: bool
    :return: None
    """
    global games,connections, specs

    if not spec:
        name = None
        bo = games[game]

        # assign a color to player
        if connections % 2 ==0:
            currentID = 'w'
        else:
            currentID = 'b'

        bo.start_user = currentID
        # pickle the object and send it to the server
        data_string = pickle.dumps(bo)

        # start the game and timer
        if currentID == 'b':
            bo.ready = True
            bo.startTime = time.time()

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
                    if data.count('select')>0:
                        all = data.split(" ")
                        col = int(all[1])
                        row = int(all[2])
                        color = all[3]
                        bo.select(col,row,color)
                    # if has a game winner
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
        connections -= 1
        # end a game
        try:
            del games[game]
            print("Game", game, "ended")
        except:
            pass
        print("Player",name,"left game", game)
        conn.close()

    else:
        available_games = list(games.keys())
        game_id = 0
        bo=games[available_games[game_id]]
        bo.start_user="s"
        date_string=pickle.dumps(bo)
        conn.send(date_string)
        while True:
            try:
                d=conn.recv(128)
                data=d.decode('utf-8')
                if not d:
                    break
                else:
                    try:
                        if data == 'forward':
                            print("Moved Games forward")
                            game_id+=1
                            if game_id>=len(available_games):
                                game_id=0
                        elif data == 'back':
                            print("Moved Games back")
                            game_id -= 1
                            if game_id <0:
                                game_id = len(available_games)-1
                        bo=games[available_games[game_id]]
                    except:
                        print("Invalid Game Received from Spectator")
                    sendData=pickle.dumps(bo)
                    conn.sendall(sendData)
            except Exception as e:
                print(e)
        print("Spectator left game",game)
        specs-=1
        conn.close()

while True:
    read_specs()
    if connections < 6:
        # return a socket object when a client connects
        conn,addr=s.accept()
        print(conn)
        print(addr)
        spec=False
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
                games(g)==Board(8,8)
            except:
                g=0
                games[g]=Board(8,8)

        print("Number of connections:", connections+1)
        print("Number of games:", len(games))

        start_new_thread(threaded_client,(conn,g,spec))


