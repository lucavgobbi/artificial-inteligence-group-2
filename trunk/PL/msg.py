#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from adds import *

# Representa o score na tela
class MSG(pygame.sprite.Sprite):
    # Inicializacao
    def __init__(self, surf_rect, text, size, (pos_x, pos_y), color):

        # Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)

        # Valor de pontos
        self.value = 0

        # Fonte a ser usada
        self.font = pygame.font.Font(None, size)

        self.surf_rect = surf_rect

        # Chamada para renderizacao inicial do score
        self.render_score(text, (pos_x, pos_y), color)

    ## Atualiza o score em uma nova surface para refletir pontos feitos pelo jogador
    #  @param score_value: valor a a ser adicionado ao score
    def render_score(self, text, (pos_x, pos_y), color):

        self.image = self.font.render(text, 1, color)
        self.rect = self.image.get_rect()
        self.rect.left = pos_x
        self.rect.top = pos_y