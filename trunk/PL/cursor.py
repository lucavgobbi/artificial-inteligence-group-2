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
    
        # limite superior que o bloco nao pode passar
        self.top_limit = surf_rect.top + 5
    
        self.update_counter = 0
    
        # Posicoes relativas do cursor em relacao a matriz de blocos
        self.pos_rel_x = 2
        self.pos_rel_y = 10

    def update(self, rise_value):
        if self.rect.top - rise_value <= self.top_limit:
            self.rect.top += self.cs_h
            self.pos_rel_y -= 1
            
        self.rect.top -= rise_value
        self.update_counter += rise_value
        if self.update_counter == 21:
            self.update_counter = 0
            self.pos_rel_y += 1

    # Desenha o cursor na tela. Borda de retangulo branca
    def draw_cursor(self, surf):
        surf.blit(self.image, self.rect)

    # Controla o movimento do cursor
    def move_cursor_UP(self, key, surf_rect):    
        if self.rect.top - self.cs_h >= self.top_limit:
            self.rect.top -= self.cs_h
            self.pos_rel_y += 1
        
    def move_cursor_DOWN(self, key, surf_rect):    
        if self.rect.top + self.cs_h <= surf_rect.bottom - 20:
            self.rect.top += self.cs_h
            self.pos_rel_y -= 1
        
    def move_cursor_LEFT(self, key, surf_rect):
        if self.rect.left - self.cs_w >= surf_rect.left:
            self.rect.left -= self.cs_w
            self.pos_rel_x -= 1
        
    def move_cursor_RIGHT(self, key, surf_rect):   
        if self.rect.right + self.cs_w <= surf_rect.right:
            self.rect.left += self.cs_w
            self.pos_rel_x += 1
        
    