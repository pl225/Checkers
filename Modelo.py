import pygame, math

class Jogo(object):

    def __init__(self):
        return None;

class Tabuleiro(object):

    def __init__(self, dimensao = 8, dGrade = 80, dTela = 640):
        self.dimensao = dimensao
        self.dGrade = dGrade
        self.dTela = dTela
        self.posicoes = criarMatriz(dTela, dGrade)
        self.pecas = None
        self.cliques = [0, None]

    def desenharTabuleiro(self, screen):
        for i in range(self.dimensao):
            for j in range(self.dimensao):
                pygame.draw.rect(screen, self.posicoes[i][j].cor, (self.posicoes[i][j].x,self.posicoes[i][j].y,self.dGrade,self.dGrade), 0)
    
    def desenharPecas(self, screen):
        for lista in self.posicoes:
            for p in lista:
                if p.peca:
                    xPeca = p.x + (self.dGrade / 2)
                    yPeca = p.y + (self.dGrade / 2)
                    pygame.draw.circle(screen, p.peca.cor, (int(yPeca),int(xPeca)), int(self.dGrade / 2), 0)

    def clickUsuario(self, player, pos):
        obrigadoComer = player.obrigadoComer(self)
        if self.cliques[0] == 0 and obrigadoComer[0]:
            self.cliques[0] = 1
            self.cliques[1] = [obrigadoComer[1].x + self.dGrade / 2, obrigadoComer[1].y + self.dGrade / 2]
            return (True, obrigadoComer[1]) # sou obrigado a comer, mando a peca q tem q comer
        else:
            pos = [pos[1], pos[0]]
            peca = self.procuraPeca(pos).peca
            if peca and peca.cor == player.cor and self.cliques[0] == 1:
                self.cliques[0] = 0
                self.cliques[1] = None    
            if self.cliques[0] == 0 and peca and peca.cor == player.cor:
                # muda cor da posicao pra dizer que clicou
                self.cliques[0] = 1 
                self.cliques[1] = pos
            elif self.cliques[0] == 1:
                if (pos[0] / self.dGrade, pos[1] / self.dGrade) in player.movimentosPossiveis(self.cliques[1], self):
                    player.atualizaTabuleiro(self.cliques[1], pos, self)
                self.cliques[0] = 0
                self.cliques[1] = None 
                return (False, True) # retorno que movi com sucesso
        return (False, False) # retorno q ainda nao me movi
             
    def procuraPeca(self, pos):
        for l in self.posicoes:
            for p in l:
                if p.linha == pos[0] / self.dGrade and p.coluna == pos[1] / self.dGrade:
                    return p    

def criarMatriz(dimensao, offset): 
    corPreta = (0,0,0)
    corBranca = (255,255,255)
    corAzul = (0, 0, 255)   
    corVerde = (0, 204, 0)
    matriz = []
    l = 0
    for i in range(0, dimensao, offset): # as coordenadas devem bater com as posicoes possiveis da grade
        linha = []
        c = 0
        for j in range(0, dimensao, offset):
            novaPosicao = Posicao(l, c)
            novaPosicao.x = i
            novaPosicao.y = j

            if l % 2 == 0:
                if c % 2 == 0:
                    novaPosicao.cor = corBranca
                else:
                    novaPosicao.cor = corPreta
            
            else:
                if c % 2 == 0:
                    novaPosicao.cor = corPreta
                else:
                    novaPosicao.cor = corBranca
                    
            if l == 0 or l == 1 or l == 2:
                if l % 2 == 0 and c % 2 == 1: novaPosicao.peca = Peca(corAzul)
                if l % 2 == 1 and c % 2 == 0: novaPosicao.peca = Peca(corAzul)
            
            if l == 5 or l == 6 or l == 7:
                if l % 2 == 1 and c % 2 == 0: novaPosicao.peca = Peca(corVerde)
                if l % 2 == 0 and c % 2 == 1: novaPosicao.peca = Peca(corVerde)
            
            linha.append(novaPosicao)
            c += 1
        matriz.append(linha)
        l += 1
    
    return matriz    

class Peca(object):
    def __init__(self, cor, dama = False):
        self.cor = cor
        self.dama = dama
        self.x = None
        self.y = None        

class Jogador(object):
    def __init__(self, pontuacao, cor):
        self.pontuacao = pontuacao
        self.cor = cor
        
    def obrigadoComer(self, tabuleiro):
        movs = [(1, -1), (-1, -1), (1, 1), (-1, 1)]
        minhasPosicoes = [p for l in tabuleiro.posicoes for p in l if p.peca and p.peca.cor == self.cor] # coleta posicoes do jogador
        
        for p in minhasPosicoes:
            for m in movs:
                p = tabuleiro.procuraPeca([p.x, p.y])
                i = p.linha + m[0]
                j = p.coluna + m[1]
                if i < 0 or j < 0 or i == tabuleiro.dimensao or j == tabuleiro.dimensao: continue # verifica posicao valida
                if tabuleiro.posicoes[i][j].peca == None: continue # ve se posicao esta vazia
                else:
                    if tabuleiro.posicoes[i][j].peca.cor == self.cor: continue # ve se eh uma peca do proprio jogador
                    else:
                        i += m[0] # pula
                        j += m[1]
                        if i < 0 or j < 0 or i == tabuleiro.dimensao or j == tabuleiro.dimensao: continue # verifica movimento valido
                        elif tabuleiro.posicoes[i][j].peca == None: # ve se a posicao esta sem peca 
                            return (True, p)
                        
        return (False, None)
    
    def movimentosPossiveis(self, pos, tabuleiro):
        raise NotImplementedError
    
    def atualizaTabuleiro(self, p1, p2, tabuleiro):
        p1 = [p1[0] / tabuleiro.dGrade, p1[1] / tabuleiro.dGrade]
        p2 = [p2[0] / tabuleiro.dGrade, p2[1] / tabuleiro.dGrade] 
        if math.fabs(p1[0] - p2[0]) == 1: # movimento simples
            tabuleiro.posicoes[p2[0]][p2[1]].peca = tabuleiro.posicoes[p1[0]][p1[1]].peca
            tabuleiro.posicoes[p1[0]][p1[1]].peca = None
        else:
            tabuleiro.posicoes[p2[0]][p2[1]].peca = tabuleiro.posicoes[p1[0]][p1[1]].peca
            tabuleiro.posicoes[p1[0]][p1[1]].peca = None
            tabuleiro.posicoes[(p1[0] + p2[0]) / 2][(p1[1] + p2[1])/2].peca = None            
            
class JogadorPlayer(Jogador):
    def __init__(self, cor):
        super(JogadorPlayer, self).__init__(0, cor)
        
    def movimentosPossiveis(self, pos, tabuleiro):
        # tem q decidir quais sao os possiveis e os obrigatirios dos movimentos abaixo (depende se o jogador esta em cima ou embaixo
        # vou supor q eh em cima
        movs = [(-1, 1), (-1, -1), (1, 1), (1, -1)]
        obrigatorio = []
        livre = []
        p = tabuleiro.procuraPeca(pos)
        for m in movs[2:]: # movimentos q nao posso fazer, mas se tiver peca eu tenho q fazer
            i = p.linha + m[0]
            j = p.coluna + m[1]
            if i < 0 or j < 0 or i == tabuleiro.dimensao or j == tabuleiro.dimensao: continue # verifica posicao valida
            if tabuleiro.posicoes[i][j].peca == None: continue # ve se posicao esta vazia
            else:
                if tabuleiro.posicoes[i][j].peca.cor == self.cor: continue # ve se eh uma peca do proprio jogador
                else:
                    i += m[0] # pula
                    j += m[1]
                    if i < 0 or j < 0 or i == tabuleiro.dimensao or j == tabuleiro.dimensao: continue # verifica movimento valido
                    elif tabuleiro.posicoes[i][j].peca == None: # ve se a posicao esta sem peca 
                        obrigatorio.append((i, j))
                        
        for m in movs[:2]: # movimentos q posso fazer, mas se tiver peca eu tenho q fazer
            i = p.linha + m[0]
            j = p.coluna + m[1]
            if i < 0 or j < 0 or i == tabuleiro.dimensao or j == tabuleiro.dimensao: continue # verifica posicao valida
            if tabuleiro.posicoes[i][j].peca == None: 
                livre.append((i, j))
            else:
                if tabuleiro.posicoes[i][j].peca.cor == self.cor: continue # ve se eh uma peca do proprio jogador
                else:
                    i += m[0] # pula
                    j += m[1]
                    if i < 0 or j < 0 or i == tabuleiro.dimensao or j == tabuleiro.dimensao: continue # verifica movimento valido
                    elif tabuleiro.posicoes[i][j].peca == None: # ve se a posicao esta sem peca 
                        obrigatorio.append((i, j))    
            
        if len(obrigatorio) > 0: return obrigatorio
        else: return livre
                           
class JogadorCPU(Jogador):
    def __init__(self, cor):
        super(JogadorCPU, self).__init__(0, cor)
        
    def movimentosPossiveis(self, pos):
        # minmax
        return None

class Posicao(object):
    def __init__(self, linha, coluna, peca = None, cor = None):
        self.cor = cor
        self.linha = linha
        self.coluna = coluna
        self.x = None
        self.y = None
        self.peca = peca 