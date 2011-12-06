#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from adds import *

# Representa mensagens que apareçam na tela
class MSG(pygame.sprite.Sprite):
    # Inicializacao
    def __init__(self, surf_rect, text, size, (pos_x, pos_y), color):

        # Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)

        # Fonte a ser usada
        self.font = pygame.font.Font(None, size)

        # Surface aonde a mensagem deve aparecer
        self.surf_rect = surf_rect

        # Chamada para renderizacao inicial do score
        self.render_msg(text, (pos_x, pos_y), color)

    ## Atualiza a mensagem em uma nova surface
    #  @param score_value: valor a a ser adicionado ao score
    def render_msg(self, text, (pos_x, pos_y), color):

        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.rect.top = pos_y