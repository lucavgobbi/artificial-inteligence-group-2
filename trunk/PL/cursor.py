#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from adds import *


class Choice_cursor(pygame.sprite.Sprite):
    """
    # Representa o cursor de troca movimentado pelo jogador
    """
    
    def __init__(self, surf_rect, w, h):
        """
        ## Construtor
        # @param surf_rect: superficie de orientação para o cursor (no caso, a blockbox)
        # @param w: largura do cursor
        # @param h: altura do cursor
        """
    
        # Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)
    
        # Tamanho do cursor
        self.cs_w = w
        self.cs_h = h
    
        # Carrega a imagem do cursor
        self.image = load_image("cursor.png")
        self.image.set_colorkey((255,0,255))

        self.surf_rect = surf_rect
    
        # Puxa o retangulo que contem o cursor e seta sua posicao inicial
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.surf_rect.left+10 + self.cs_w*2 ,self.surf_rect.top+5 + self.cs_h)
    
        # limite superior que o cursor nao pode passar
        self.top_limit = surf_rect.top + 5
        
        # Contador para controle de atualização de tela e portanto reposicionamento do cursor
        self.update_counter = 0
    
        # Posicoes relativas do cursor em relacao a matriz de blocos
        self.pos_rel_x = 2
        self.pos_rel_y = 10

    
    def update(self, rise_value):
        """
        ## Atualiza a posicao do cursor, fazendo com que ele suba uma quantidade de pixels dada
        # @param rise_value: numero de pixels queo cursor deve subir
        """
        
        # se o topo do cursor ultrapassar o limite da tela, ao inves de fazelo subir, joga ele
        # uma posição para baixo
        if self.rect.top - rise_value <= self.top_limit:
            self.rect.top += self.cs_h
            self.pos_rel_y -= 1
        
        # sobe o cursor o número de pixels dado, e caos ultrapasse 21, aumenta sua posição relativa
        # e reseta o contador
        self.rect.top -= rise_value
        self.update_counter += rise_value
        if self.update_counter == 21:
            self.update_counter = 0
            self.pos_rel_y += 1


    def draw_cursor(self, surf):
        """
        ## Desenha o cursor na superficie dada
        # @param surf: superficie em que deve ser desenhado o cursor
        """
        
        surf.blit(self.image, self.rect)

    def reset_cursor(self):
        """
        ## Reseta o cursor para a posição inicial coluna 2 e linha 10
        """
        self.rect.topleft = (self.surf_rect.left+10 + self.cs_w*2 ,self.surf_rect.top+5 + self.cs_h)
        self.pos_rel_x = 2
        self.pos_rel_y = 10


    def move_cursor_UP(self, surf_rect):
        """
        ## Movimenta cursor para cima de acordo com a superficie a qual ele se orienta
        #  @param surf_rect: superficie que orienta o cursor
        """
        if self.rect.top - self.cs_h >= self.top_limit:
            self.rect.top -= self.cs_h
            self.pos_rel_y += 1
        
    def move_cursor_DOWN(self, surf_rect): 
        """
        ## Movimenta cursor para baixo de acordo com a superficie a qual ele se orienta
        #  @param surf_rect: superficie que orienta o cursor
        """
        if self.rect.top + self.cs_h <= surf_rect.bottom - 20:
            self.rect.top += self.cs_h
            self.pos_rel_y -= 1
        
    def move_cursor_LEFT(self, surf_rect):
        """
        ## Movimenta cursor para esquerda de acordo com a superficie a qual ele se orienta
        #  @param surf_rect: superficie que orienta o cursor
        """
        if self.rect.left - self.cs_w >= surf_rect.left:
            self.rect.left -= self.cs_w
            self.pos_rel_x -= 1
        
    def move_cursor_RIGHT(self, surf_rect):
        """
        ## Movimenta cursor para direita de acordo com a superficie a qual ele se orienta
        #  @param surf_rect: superficie que orienta o cursor
        """
        if self.rect.right + self.cs_w <= surf_rect.right:
            self.rect.left += self.cs_w
            self.pos_rel_x += 1
        
    