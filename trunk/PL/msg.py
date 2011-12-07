#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from adds import *

class MSG(pygame.sprite.Sprite):
    """
    # Cria e renderiza menagens para aparecer na tela
    """
    
    def __init__(self, text, size, (pos_x, pos_y), color):
        """
        ## Construtor
        #  @param surf_rect: rect da superficie base para o score
        #  @param text: texto a ser mostrado
        #  @param size: tamanho da fonte
        #  @param (pos_x, pos_y): tupla com a coordenada onde será posicionada o texto (canto superior esquerdo)
        #  @param color: cor do texto
        """

        # Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)

        # Inicializa fonte a ser usada
        self.font = pygame.font.Font(None, size)

        # Chamada para renderizacao inicial da mensagem
        self.render_msg(text, (pos_x, pos_y), color)

    def render_msg(self, text, (pos_x, pos_y), color):
        """
        ## Renderiza a mensagem, criando seu rect para ser grudada na tela
        #  @param text: texto a ser mostrado
        #  @param (pos_x, pos_y): tupla com a coordenada onde será posicionada o texto (canto superior esquerdo)
        #  @param color: cor do texto
        """

        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.rect.top = pos_y