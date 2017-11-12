import pickle
from socket import *

class Client:
    serverHost = "127.0.0.1"
    serverPort = 4446
     
    def __init__(self):
        self.data = None
        self.socket = socket(AF_INET, SOCK_STREAM) 
        
    def conectar(self):
        self.socket.connect((Client.serverHost, Client.serverPort))
        
    def receber(self):
        return pickle.loads(self.socket.recv(8192))
    
    def enviar(self, data):
        self.socket.send(pickle.dumps(data))

    def encerrarConexao(self):
        self.socket.close()            
