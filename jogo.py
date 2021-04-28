import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

largura = 640
altura = 480
branco = (250, 250, 200)
x = 0
y = 0

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('kenny, o tomate')


##SORTEIO DE INIMIGO
inimigo = choice([0, 1])

colidiu = False
pontos = 0
velocidade = 8

def exibitexto(msg, tamanho, cor):
    fonte = pygame.font.SysFont('arial', tamanho, True, False)
    mensagem = f'{msg}'
    texto_format = fonte.render(mensagem, True, cor)
    return texto_format

def reiniciar():
    global pontos, velocidade, colidiu, inimigo
    pontos = 0
    velocidade = 8
    colidiu = False
    caos.rect.x = largura
    alien.rect.x = largura
    inimigo = choice([0, 1])

####CLASSE DO KENNY
class Kenny(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('dados/mistken.png'))
        self.image = self.sprites[0]
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_in = 340
        self.rect.topleft = 0, 340
        self.pulo = False

####PULO DO KENNY
    def pular(self):
        self.pulo = True


####parte da lógca
    def update(self, *args):
        if self.pulo == True:
            if self.rect.y <= 100:
                self.pulo = False
            self.rect.y -= 20

        else:
            if self.rect.y < self.pos_y_in:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_in

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 10
        elif keys[pygame.K_d]:
            self.rect.x += 10
####        if keys[pygame.K_SPACE]:
###            self.rect.y -= 20

##### CLASSE CHÃO
class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dados/chablue.png')
        self.image = pygame.transform.scale(self.image, (320, 320))
###        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
###        self.rect.topleft = (0 * 2), 270
        self.rect.x = pos_x * 320
        self.rect.y = 390

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 2

########## classe alien
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dados/aliens.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = inimigo
        self.rect.center = (largura, altura - 150)

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade - 1



class Caos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('dados/butpc.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = inimigo
        self.rect = self.image.get_rect()
        self.rect.center = (largura, altura - 90)
        self.rect.x = largura

    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade


##PONTOS



all = pygame.sprite.Group()

#####FUNDO DA CIDADE
fundo = pygame.image.load('dados/southpark.png').convert()
fundo = pygame.transform.scale(fundo, (largura, altura))


#########LOOP DOS CHAO
for i in range(largura*2//320):
    chao = Chao(i)
    all.add(chao)

alien = Alien()
all.add(alien)
caos = Caos()
all.add(caos)

kenny = Kenny()
all.add(kenny)

####OBSTACULOS DO KENNY
obstaculo = pygame.sprite.Group()
obstaculo.add(alien)
obstaculo.add(caos)


#####TEMPO E LOOP
relogio = pygame.time.Clock()

while True:
    relogio.tick(70)
    tela.fill(branco)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if kenny.rect.y != kenny.pos_y_in:
                    pass
                else:
                    kenny.pular()
            if event.key == K_r and colidiu == True:
                reiniciar()
    tela.blit(fundo, (0, 0))


    all.draw(tela)

    if alien.rect.topright[0] <= 0 or caos.rect.topright[0] <= 0:
        inimigo = choice([0,1])
        alien.rect.x = largura
        caos.rect.x = largura
        alien.escolha = inimigo
        caos.escolha = inimigo

    colisoes = pygame.sprite.spritecollide(kenny, obstaculo, False, pygame.sprite.collide_mask)

    if colisoes and colidiu == False:
        Colidiu = True

    if colisoes:
        if pontos % 100 == 0:
            pontos += 1
        gameover = exibitexto("GAME OVER", 40, (0, 0, 0))
        tela.blit(gameover, (largura//2, altura// 2))
###        recomeco = exibitexto("pressione r para reiniciar", 19, (0, 0, 0))
##        tela.blit(recomeco,(largura//2, (altura//2) + 60))
    else:
        pontos += 1
        all.update()
        texto_ponto = exibitexto(pontos, 40, (0, 0, 0))

    if pontos % 100 == 0:
        if velocidade >= 23:
            velocidade += 0
        else:
            velocidade += 1


    tela.blit(texto_ponto,(520, 30))





    pygame.display.flip()
