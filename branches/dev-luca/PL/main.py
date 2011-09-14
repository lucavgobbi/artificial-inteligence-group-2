#! /usr/bin/env python

import os, sys
import pygame
from pygame.locals import *
from blockbox import Blockbox
from cursor import Choice_cursor
from adds import *

if not pygame.font: print "Warning: Fonts nao disponivel"
if not pygame.mixer: print "Warning: Mixer nao disponivel"

# Cuida dos aspectos principais do jogo
class Main:

    # Inicializa classe main
    def __init__(self, w = 640, h = 480):
        # Inicializa pygame
        pygame.init()
        
        # largura e altura da tela
        self.width = w
        self.height = h
        
        # Seta o seguramento de teclas. Quando uma tecla e pressionada e segurada, da o efeito
        # de aperta-la diversas vezes
        pygame.key.set_repeat(60,60)
               
        # areas 'sujas' da tela que devem ser atualizadas
        self.rectlist = []

        # Inicializa janela principal com os tamanhos dados
        self.screen = pygame.display.set_mode((self.width, self.height),pygame.DOUBLEBUF, 32)
        
        # Inicializa o clock
        self.clock = pygame.time.Clock()
        
        # cria um background e anexa a tela
        self.background = pygame.Surface((self.width, self.height)).convert()
        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
        

    # Carrega sprites e cria grupos de sprites de inicializacao
    def load_sprites(self):
	
	# objetos principais da tela. Blox e o quadro que contem os blocos.
        self.blox = Blockbox(152, 262, 150, 150, self.screen)
        
        # Grupo de sprites unico para o cursor e para a caixa de blocos.
        self.blockbox_sprite = pygame.sprite.RenderUpdates(self.blox)
        
        # Configuracao inicial de blocos
        self.blox.initiate_blocks()
    
    # Chama a funcao de checagem de queda para os blocos necessarios
    def fall(self, bb):
	for block in bb.changed:
	    print "passa"
	    bb.check_fall(block.col, block.line)
	for block_set in bb.falling_blocks:
	    bb.block_fall(block_set)
    
    # Caso tenha sido dado o comando para mudar dois blocos de posicao, esse metodo chama o metodo
    # que muda os dois blocos na posicao desejada de lugar
    def change(self, bb, pos_x, pos_y):
        if bb.change_fin == False:
            bb.change_fin = bb.block_change(pos_x, pos_y)

    # Loop principal do programa
    def main_loop(self):
        running = 1
        
        pos_x = 0
        pos_y = 0
        
        self.load_sprites()
 
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.KEYDOWN:
		    if event.key == pygame.K_UP:
                        self.blox.cursor.move_cursor_UP(event.key, self.blox.rect) # Move Cursor pra cima
                        
		    elif event.key == pygame.K_DOWN:
                        self.blox.cursor.move_cursor_DOWN(event.key, self.blox.rect) # Move Cursor pra baixo
                        
		    elif event.key == pygame.K_LEFT:
                        self.blox.cursor.move_cursor_LEFT(event.key, self.blox.rect) # Move Cursor pra esquerda
                        
		    elif event.key == pygame.K_RIGHT:
                        self.blox.cursor.move_cursor_RIGHT(event.key, self.blox.rect) # Move Cursor pra direita
                        
                    # Tecla A inicia uma mudanca de blocos. Seta a flag change_fin e grava a posicao do cursor
                    elif event.key == pygame.K_a:
                        if self.blox.cursor.pos_rel_y < self.blox.max_height:
			    self.blox.change_fin = False
			    pos_x = self.blox.cursor.pos_rel_x
			    pos_y = self.blox.cursor.pos_rel_y
			
		    # Tecla para testes. imprime as matrizes de blocos
		    elif event.key == pygame.K_f:
			print "Matriz de configuracao de blocos"
			self.blox.print_config_matrix()
			print "Matriz de blocos"
			self.blox.print_block_matrix()
			print "Ativos"
			self.blox.print_active()
			
		    elif event.key == pygame.K_q:
			running = 0
			
			
	    # processo de mudanca de bloco
            self.change(self.blox, pos_x, pos_y)
            
            self.fall(self.blox)
            
            # Desenha a blockbox e depois seus elementos. Retorna a area em que desenhamos a blockbox para atualiza-la
            self.rectlist = self.blockbox_sprite.draw(self.screen)
            self.blox.draw_elements(self.screen)
            
            # Atualiza a tela apenas na area da blockbox. Subsequentemente limpa a tela com o background
            pygame.display.update(self.rectlist)
            self.blockbox_sprite.clear(self.screen, self.background)
            
            # Jogo rodando em 60fps
            self.clock.tick(60)


if __name__ == "__main__":
    # Inicializa objeto main e entra no loop principal
    main_window = Main()
    main_window.main_loop()
