import socket
import pickle
import time

class Network:

    def __init__(self):
        # AF_INET: address-family IPV4; SOCK_STREAM: connection-oriented TCP protocol
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host="192.168.0.126"
        self.port=5555
        self.addr=(self.host,self.port)
        self.board=self.connect()
        # to load pickled data from a bytes string
        self.board=pickle.loads(self.board)

    def connect(self):
        """
        connect to the address
        :return: data received from socket
        """
        # connect to the server
        self.client.connect(self.addr)
        return self.client.recv(4096*8)

    def disconnect(self):
        """
        close connection
        :return: None
        """
        self.client.close()

    def send(self,data,pick=False):
        """
        send data to the server abd receive data from the server
        :param data: str
        :param pick: bool
        :return: str
        """
        start_time = time.time()
        while time.time()-start_time<5:
            try:
                # to send data on socket
                if pick:
                    # converts a Python object hierarchy into a byte stream
                    self.client.send(pickle.dumps(data))
                else:
                    # to send encoded string
                    self.client.send(str.encode(data))
                    reply=self.client.recv(4096*8)
                try:
                    reply=pickle.loads(reply)
                    break
                except Exception as e:
                    print(e)
            except socket.error as e:
                print(e)
        return reply