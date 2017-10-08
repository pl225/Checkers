import pygame
from pygame.locals import *
from sys import exit
from Modelo import Tabuleiro, JogadorCPU, JogadorPlayer, Jogo, Peca

pygame.init()

dimensaoTela = 640
dimensaoGrade = 80
offset = int(dimensaoTela / dimensaoGrade)

screen = pygame.display.set_mode((dimensaoTela, dimensaoTela), 0, 32)

pygame.display.set_caption('Game of Damas')

clock = pygame.time.Clock()

t = Tabuleiro()

cpu = JogadorCPU((0, 0, 255))
p1 = JogadorPlayer((0, 204, 0))

p1Clicou = False
botoesMouse = None
pecaObrigatoria = None

turno = p1
#t.procuraPeca((350, 100)).peca = Peca((0, 0, 255))
#t.procuraPeca((300, 220)).peca = Peca((0, 204, 0))
#t.procuraPeca((150, 350)).peca = Peca((0, 204, 0))

#for l in t.posicoes:
#   for p in l:
  #      print p.linha, p.coluna,
        
   # print ''
    
#exit()
while True:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            botoesMouse = pygame.mouse.get_pressed()
        if event.type == QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONUP and turno == p1:
            p1Clicou = True
            
    estado = t.estadoAtual(cpu, p1)
    
    if estado != 0:
        if estado == 1:
            print "P1 ganhou!"
        else:
            print "CPU ganhou!"
        exit()  
            
    if turno == cpu:
        #tabuleiro = recebe novo tabuleiro do minmax
        print "cpu"
        t = Jogo.minmax(cpu, p1, t, 4)
        turno = p1
        
    elif botoesMouse and botoesMouse[0] and p1Clicou:
        # se tem movimentos obrigatorios, seta cursor
        # se nao pega click do usuario
        posMouse = t.clickUsuario(p1, pygame.mouse.get_pos())
        if posMouse[0] and posMouse[1]:
            pygame.mouse.set_pos(posMouse[1].y + t.dGrade / 2, posMouse[1].x + t.dGrade / 2)
            pecaObrigatoria = posMouse[1].peca
        elif not posMouse[0] and posMouse[1]:
            obrigatoriedade = p1.obrigadoComer(t)
            if not obrigatoriedade[0] or (obrigatoriedade[1].peca != pecaObrigatoria):
                turno = cpu
               
        botoesMouse = None
        p1Clicou = False

    t.desenharTabuleiro(screen)
    t.desenharPecas(screen)

    pygame.display.update()