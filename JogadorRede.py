import pygame
from pygame.locals import *
from sys import exit
from Modelo import Tabuleiro, JogadorPlayer, JogadorCPU
from client_jogador import Client

pygame.init()

dimensaoTela = 640
dimensaoGrade = 80
offset = int(dimensaoTela / dimensaoGrade)

screen = pygame.display.set_mode((dimensaoTela, dimensaoTela), 0, 32)

pygame.display.set_caption('Game of Damas')

clock = pygame.time.Clock()

def atualizarTela():
    t.desenharTabuleiro(screen)
    t.desenharPecas(screen)
    pygame.display.update()

t = Tabuleiro()
atualizarTela()
c = Client()
try: 
    c.conectar()
    cor1 = c.receber()
    cor2 = c.receber()
    if (0, 204, 0) == cor1:
        p1 = JogadorPlayer(cor1)
        p2 = JogadorCPU(cor2)
    else:
        p1 = JogadorCPU(cor1)
        p2 = JogadorPlayer(cor2)
    
    p1Clicou = False
    botoesMouse = None
    pecaObrigatoria = None
    
    if p1.cor == (0, 204, 0): turno = p1
    else: turno = p2
    
    while True:
        atualizarTela()
    
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                botoesMouse = pygame.mouse.get_pressed()
            if event.type == QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONUP and turno == p1:
                p1Clicou = True
                
        estado = t.estadoAtual(p2, p1)
        
        if estado != 0:
            c.enviar(estado)
            break
                
        if turno == p2:
            t = c.receber()
            turno = p1
        elif botoesMouse and botoesMouse[0] and p1Clicou:
            posMouse = t.clickUsuario(p1, pygame.mouse.get_pos())
            if posMouse[0] and posMouse[1]:
                pygame.mouse.set_pos(posMouse[1].y + t.dGrade / 2, posMouse[1].x + t.dGrade / 2)
                pecaObrigatoria = posMouse[1].peca
            elif not posMouse[0] and posMouse[1]:
                obrigatoriedade = p1.obrigadoComer(t)
                if not obrigatoriedade[0] or (obrigatoriedade[1].peca != pecaObrigatoria):
                    turno = p2
                    c.enviar(t)
                   
            botoesMouse = None
            p1Clicou = False
finally:
    print c.receber()    
    c.encerrarConexao()