import pickle
from socket import *

host = "127.0.0.1"
port = 4446

s=socket(AF_INET, SOCK_STREAM)
s.bind((host,port))

s.listen(3)

def terminarPartida(estado):
    fimJogo = []
    e = pickle.loads(estado)
    if isinstance(e, (int, long)):
        if e == 1:
            fimJogo = ["Voce ganhou!", "Voce perdeu!", "O jogador 1 ganhou!"]
        elif e == -1:
            fimJogo = ["Voce perdeu!", "Voce ganhou!", "O jogador 2 ganhou!"]
        else:
            fimJogo = ["A partida foi declarada empatada!"] * 3
        jogador1.send(pickle.dumps(fimJogo[0]))
        jogador2.send(pickle.dumps(fimJogo[1]))
        espectador.send(pickle.dumps(fimJogo[2]))
        return True

print "Aguardando conexoes..."

jogador1, addr1 = s.accept() # jogador 1
jogador1.send(pickle.dumps((0, 204, 0)))
print "Jogador1 conectado"
    
jogador2, addr2 = s.accept() # jogador 2
jogador2.send(pickle.dumps((0, 0, 255)))
print "Jogador2 conectado"

espectador, addr3 = s.accept() # espectador
print "Espectador conectado"

jogador1.send(pickle.dumps((0, 0, 255)))
jogador2.send(pickle.dumps((0, 204, 0)))

print "Comecar"

try:
    while True:
        msg = jogador1.recv(8192)
        if terminarPartida(msg): break
        
        jogador2.send(msg)
        espectador.send(msg)
        
        msg = jogador2.recv(8192)
        if terminarPartida(msg): break
        
        jogador1.send(msg)
        espectador.send(msg)
    
finally:
    s.close()