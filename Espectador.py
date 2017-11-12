import pygame
from pygame.locals import *
from Modelo import Tabuleiro
from client_jogador import Client

pygame.init()

dimensaoTela = 640
dimensaoGrade = 80
offset = int(dimensaoTela / dimensaoGrade)

screen = pygame.display.set_mode((dimensaoTela, dimensaoTela), 0, 32)

pygame.display.set_caption('Game of Damas')

clock = pygame.time.Clock()

t = Tabuleiro()

def atualizarTela():
    t.desenharTabuleiro(screen)
    t.desenharPecas(screen)
    pygame.display.update()
    
atualizarTela()
c = Client()

try: 
    c.conectar()
    while True:
        t = c.receber()
        if isinstance(t, (int, long)):break
        atualizarTela()
finally:
    print c.receber()    
    c.encerrarConexao()