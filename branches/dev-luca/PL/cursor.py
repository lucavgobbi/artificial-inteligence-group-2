#! /usr/bin/env python
import pygame
from adds import *

# Representa o cursor movimentado pelo jogador
class Choice_cursor(pygame.sprite.Sprite):
    # Inicializacao
    def __init__(self, screen, surf_rect, w, h):
	
	# Inicializa classe sprite
	pygame.sprite.Sprite.__init__(self)
	
	# Tamanho do cursor
	self.cs_w = w
	self.cs_h = h
	
	# Carrega a imagem do cursor
	self.image = load_image("cursor.png")
	self.image.set_colorkey((255,0,255))
	
	# Puxa o retangulo que contem o cursor e seta sua posicao inicial
	self.rect = self.image.get_rect()
	self.rect.topleft = (surf_rect.left+10 + self.cs_w*2 ,surf_rect.top+5 + self.cs_h)
	
	# Posicoes relativas do cursor em relacao a matriz de blocos
	self.pos_rel_x = 2
	self.pos_rel_y = 10


    # Desenha o cursor na tela. Borda de retangulo branca
    def draw_cursor(self, surf):
	surf.blit(self.image, self.rect)

    # Controla o movimento do cursor
    def move_cursor_UP(self, key, rect):    
	if self.rect.top - self.cs_h >= rect.top + 5:
	    self.rect.top -= self.cs_h
	    self.pos_rel_y += 1
	    
    def move_cursor_DOWN(self, key, rect):  	    
	if self.rect.top + self.cs_h <= rect.bottom - 20:
	    self.rect.top += self.cs_h
	    self.pos_rel_y -= 1
	    
    def move_cursor_LEFT(self, key, rect):  	
	if self.rect.left - self.cs_w >= rect.left:
	    self.rect.left -= self.cs_w
	    self.pos_rel_x -= 1
	    
    def move_cursor_RIGHT(self, key, rect):  	    
	if self.rect.right + self.cs_w <= rect.right:
	    self.rect.left += self.cs_w
	    self.pos_rel_x += 1