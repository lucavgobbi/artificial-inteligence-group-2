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
        
        # Chamada para renderizacao inicial do score
        self.render_score(surf_rect, 0)
    
    ## Atualiza o score em uma nova surface para refletir pontos feitos pelo jogador
    #  @param surf_rect: retangulo que orienta a posicao do texto de score. no nosso caso, a blockbox
    #  @param score_value: valor a a ser adicionado ao score
    def render_score(self, surf_rect, score_value):
         
        self.value += score_value
        self.image = self.font.render("SCORE: " + str(self.value), 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left = surf_rect.left + 20
        self.rect.top = surf_rect.top - 30
        
    ## Funcao de calculo de novo score, baseado no numero de blocos eliminados
    #  @param surf_rect: retangulo que orienta a posicao do texto de score. no nosso caso, a blockbox
    #  @param number_clear: numero de blocos eliminados na chamada
    #  @param chain: numero de chain
    def increase_score(self, surf_rect, number_clear, chain):
        add = 90 + (number_clear-3)*130
        self.render_score(surf_rect, add)