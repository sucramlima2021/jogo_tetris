import pygame as pg
import sys
import random
import time
pg.init()
_ = False
tela = pg.display.set_mode((800,800))
lines = [[] for x in range(0,800,40)]
colors =[[] for x in range(0,800,40)]

class Formas():
    def __init__(self):
        
        self.form1 = [
            [_,_,_],
            [_,1,_],
            [_,_,_]
        ]
        self.form2 = [
            [1,1,1],
            [1,1,1],
            [1,1,1]
        ]
        self.form3 = [
            [_,1,_],
            [1,1,1],
            [_,_,_]
        ]
        self.form4 = [
            [1,_,_],
            [1,1,1],
            [_,_,1]
        ]
        self.form5 = [
            [1,_,_],
            [1,_,_],
            [1,1,1]
        ]
        self.form6 = [
            [_,_,_],
            [1,1,1],
            [_,_,_]

        ]
        self.lista_formas = [self.form1, self.form2, self.form3, self.form4, self.form5, self.form6]
        self.bloco = 40
        self.forma = self.lista_formas[random.randint(0,5)]
        self.inix = random.randrange(0, 480, 40)
        self.iniy = 0
        self.rotacao = False
        self.largura = 0
        self.altura = 0
        self.forma_virada = []
        self.chegou = 1
        self.pontos = []
        self.adiciona_rects = True
        self.cor1 = random.randint(20,255)
        self.cor2 = random.randint(20,255)
        self.cor3 = random.randint(20,255)
    
    def desenha_forma(self):
        x = self.inix
        y = self.iniy
        tx_f = 0
        ty_f = 0
        for i in self.forma:
            tx = 0
            ty = 0
            for j in i:
                
                if j:
                    pg.draw.rect(tela, (self.cor1,self.cor2,self.cor3), (x,y,self.bloco,self.bloco))
                    if self.adiciona_rects:
                        self.pontos.append(pg.Rect(x,y,self.bloco,self.bloco))
                    tx += 40
                    ty = 1
                x+=self.bloco
            if tx_f < tx:
                tx_f = tx
            if ty == 1:
                ty_f += 40
            y+=self.bloco
            x=self.inix
        self.altura = ty_f
        self.largura = tx_f
        self.adiciona_rects = False


    def rotaciona_forma(self):
        girada = []
        girada.append([self.forma[2][0], self.forma[1][0], self.forma[0][0]])
        girada.append([self.forma[2][1], self.forma[1][1], self.forma[0][1]])
        girada.append([self.forma[2][2], self.forma[1][2], self.forma[0][2]])
        
        self.forma = girada
        self.adiciona_rects = True
        

        

    
            
class Game():
    def __init__(self):
        
        self.forma = Formas()
        self.mover = pg.USEREVENT + 1

        self.incremento = 1000
        self.cont = 0
        
    
    def checa_movimento(self, direcao):
        if direcao == 'baixo':
            for j in lines:
                for i in self.forma.pontos:
                
                    x,y,tx,ty = i
                    pt = pg.Rect(x, y+40, tx, ty)
                    if pt.collidelist(j) != -1 or y + 40 >= 800:
                        
                        return False
            return True
        if direcao == 'esquerda':
            
            for j in lines:
                for i in self.forma.pontos:
                
                    x,y,tx,ty = i
                    pt = pg.Rect(x-40, y, tx, ty)
                    if pt.collidelist(j) != -1 or x - 40 < 0:
                        
                        return False
            return True
        if direcao == 'direita':
            
            for j in lines:
                for i in self.forma.pontos:
                
                    x,y,tx,ty = i
                    pt = pg.Rect(x+40, y, tx, ty)
                    if pt.collidelist(j) != -1 or x + 40 >= 800:
                        
                        return False
            return True
        
    def move(self):
        
        if self.checa_movimento('baixo'):

            self.forma.iniy += self.forma.bloco
            self.forma.pontos = []
            self.forma.adiciona_rects = True
        else: self.forma.chegou = 2
        
        

                        
             
    def verifica(self):
        linha = []
        for i in lines:
            if len(i) == 20:
                linha.append(lines.index(i))
        if len(linha) > 0:
            for i in linha:
                
                for j in range(i):
                    for k in lines[j]:
                        x,y,tx,ty = k
                        k.update(x, y+40, tx,ty)

                lines.pop(i)
                colors.pop(i)
                lines.insert(0,[])
                colors.insert(0,[])
            linha.clear()


    def timer_movimento(self):
        pg.time.set_timer(self.mover, self.incremento)


    def run(self):
        self.timer_movimento()
        
        while True:
            pg.draw.rect(tela,(0,0,0), (0,0,800,800))
            #pg.draw.rect(tela, 'red', (self.preenche[0]))
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if e.type == self.mover:
                    self.move()

                if e.type == pg.KEYUP:
                    if e.key == pg.K_UP:
                        self.forma.rotaciona_forma()
                        
                    if e.key == pg.K_DOWN:
                        self.incremento = 100
                        self.timer_movimento()

                    if e.key == pg.K_m:
                        print(lines)
                        print(colors)

                    if e.key == pg.K_LEFT:
                        if self.checa_movimento('esquerda'):
                            self.forma.inix -= 40
                            self.forma.pontos = []
                            self.forma.adiciona_rects = True
                    if e.key == pg.K_RIGHT:
                        if self.checa_movimento('direita'):
                            self.forma.inix += 40
                            self.forma.pontos = []
                            self.forma.adiciona_rects = True
            
                  
            
            

            if self.forma.chegou == 1:
                pass    
            

            if self.forma.chegou == 2:
                
                self.incremento = 1000
                self.timer_movimento()
                
                for i in self.forma.pontos:
                    x,y,tx,ty = i
                     
                    ind = y //40
                    lines[ind].append(i)
                    colors[ind].append([self.forma.cor1, self.forma.cor2, self.forma.cor3])
                self.forma.chegou = 3
                self.forma = Formas()
                
            self.forma.desenha_forma()       

            
                
            for j in lines:
                
                cont = 0
                ind = lines.index(j)

                for i in j:
                    
                    pg.draw.rect(tela, colors[ind][cont], i)
                    cont += 1
                    
             

            self.verifica()

            
            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
