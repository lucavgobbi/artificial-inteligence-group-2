#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
from adds import *

class chronometer(pygame.sprite.Sprite):
    """
    # Controla um cronometro na tela
    """

    def __init__(self, elapsed_time, pos_top, pos_left):

        pygame.sprite.Sprite.__init__(self)
        
        # inicializa a fonte
        self.font = pygame.font.Font(None, 32)
        
        # milisegundos, segundos e minutos passados desde o inicio
        self.ms_elapsed = 0
        self.seg_elapsed = 0
        self.min_elapsed = 0
        
        # clock que será usado para contagem de tempo do cronômetro
        self.chron_clock = pygame.time.Clock()
        
        # posição do cronometro
        self.pos_top = pos_top
        self.pos_left = pos_left
        
        # atualiza o cronometro com o tempo passado
        self.update_chronometer()

    def update_chronometer(self):
        """
        # Atualiza o cronometro com o tempo que passou no último frame
        """

        self.ms_elapsed += self.chron_clock.tick()
        self.seg_elapsed += self.ms_elapsed/1000
        self.min_elapsed += self.seg_elapsed/60
        self.seg_elapsed = self.seg_elapsed % 60
        self.ms_elapsed = self.ms_elapsed % 1000

        return self.render_chronometer()

    def render_chronometer(self):
        """
        # Renderiza o cronometro na tela, segundo a sua ultima atualização
        """
        
        self.image = self.font.render("TIME: {0:1.0f}:{1:02.0f}:{2:03.0f}".format(self.min_elapsed, self.seg_elapsed, self.ms_elapsed), 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = self.pos_top
        self.rect.top = self.pos_left
        self.rect.width += 10

        return self.rect