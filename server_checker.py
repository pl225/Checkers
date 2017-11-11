import pickle
from socket import *

host = "127.0.0.1"
port = 4446

s=socket(AF_INET, SOCK_STREAM)
s.bind((host,port))

s.listen(3)

print "Aguardando conexoes..."

jogador1, addr1 = s.accept() # jogador 1
jogador1.send(pickle.dumps((0, 204, 0)))

print "Jogador1 conectado"
    
jogador2, addr2 = s.accept() # jogador 2
jogador2.send(pickle.dumps((0, 0, 255)))

print "Jogador2 conectado"

#espectador, addr2 = s.accept() # espectador

#print "Espectador conectado"

jogador1.send(pickle.dumps((0, 0, 255)))
jogador2.send(pickle.dumps((0, 204, 0)))

print "Comecar"

try:
    while True:
        msg = jogador1.recv(8192) # esse e o tamanho maximo dos dados a serem enviados
        
        jogador2.send(msg)
        #espectador.send(pickle.dumps(msg))
        
        msg = jogador2.recv(8192)
        
        jogador1.send(msg)
        #espectador.send(pickle.dumps(msg))
    
finally:
    s.close()