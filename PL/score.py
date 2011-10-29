#! /usr/bin/env python
import pygame
from adds import *

# Representa o score na tela
class Score(pygame.sprite.Sprite):
    # Inicializacao
    def __init__(self, surf_rect, initial_score):
    
        # Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)
        
        # Valor de pontos
        self.value = 0
        
        # Fonte a ser usada
        self.font = pygame.font.Font(None, 24)

        self.surf_rect = surf_rect
        
        # Chamada para renderizacao inicial do score
        self.render_score(0)
    
    ## Atualiza o score em uma nova surface para refletir pontos feitos pelo jogador
    #  @param score_value: valor a a ser adicionado ao score
    def render_score(self, score_value):
         
        self.value += score_value
        self.image = self.font.render("SCORE: " + str(self.value), 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = self.surf_rect.left + 20
        self.rect.top = self.surf_rect.top - 50
        self.rect.width += 50
        
    ## Funcao de calculo de novo score, baseado no numero de blocos eliminados
    #  @param number_clear: numero de blocos eliminados na chamada
    #  @param chain: numero de chain
    def increase_score(self, number_clear, chain):
        add = 90 + (number_clear-3)*130
        self.render_score(add)

    def change_score(self, value):
        self.render_score(-value)