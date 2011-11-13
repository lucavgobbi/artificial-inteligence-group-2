#! /usr/bin/env python

import os, sys
import pygame
import random
from pygame.locals import *
from blockbox import Blockbox
from cursor import Choice_cursor
from cpu import Cpu
from adds import *
from chron import chronometer

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

        self.max_update_value = 12
        self.update_timer = self.max_update_value
        self.update_counter = 0
        self.rise_value = 3        
        self.stop_update_timer = 0
        self.stop_update = True

        # Inicializa janela principal com os tamanhos dados
        self.screen = pygame.display.set_mode((self.width, self.height),pygame.DOUBLEBUF, 32)
        
        # Inicializa o clock
        self.clock = pygame.time.Clock()
        self.clock_teste = pygame.time.Clock()

        self.timer = chronometer(pygame.time.get_ticks(), 10, 10)
        self.timer_group = pygame.sprite.RenderUpdates()
        self.timer_group.add(self.timer)
        
        # cria um background e anexa a tela
        self.background = pygame.Surface((self.width, self.height)).convert()
        self.background.fill((0,0,0))
        self.screen.blit(self.background, (0,0))
    
        
        """ Variaveis de teste """
        self.frame_number = 0.0
        self.last_frame = 0.0
        self.frame_gap = 0.0
        self.frame_counter = 0
        self.frame_gap_total = 0.0
        
        self.p_counter = 0
        self.p_flag = False
        
        self.k_counter = 0
        self.k_flag = False
        
        self.r_counter = 0
        self.r_limit = 0
        self.r_flag = False
        
        """ Variaveis de teste """

    # Carrega sprites e cria grupos de sprites de inicializacao
    def load_sprites(self):
    
        # objetos principais da tela. Blox e o quadro que contem os blocos.
        self.blox = Blockbox(152, 262, 100, 150, self.screen)
        #self.cpu = Cpu((152, 262, 388, 150), self.screen)
        
        # Grupo de sprites unico para o cursor e para a caixa de blocos.
        self.blockbox_sprite = pygame.sprite.RenderUpdates(self.blox)
        #self.blockbox_sprite.add(self.cpu.blockbox)
        
        # Configuracao inicial de blocos
        #self.blox.initiate_blocks()

        if len(sys.argv) > 1:
            self.blox.file_initiate_blocks(sys.argv[1])
            #self.cpu.blockbox.initiate_blocks()
        else:
            self.blox.initiate_blocks()
            #self.cpu.blockbox.initiate_blocks()
    
    # Chama a funcao de checagem de queda para os blocos necessarios
    def fall(self, bb):
        clear_test = []
        
        for block_set in bb.falling_blocks:
            if bb.block_fall(block_set):
                clear_test.append(block_set)

        if clear_test != []:
            for block_set in clear_test:
                bb.falling_blocks.remove(block_set)
                bb.check_clear(block_set)
    
    # Caso tenha sido dado o comando para mudar dois blocos de posicao, esse metodo chama o metodo
    # que muda os dois blocos na posicao desejada de lugar
    def change(self, bb):
        for block in bb.changing_blocks:
            bb.change_fin = bb.block_change(block)
            
    def clear(self, bb):
        for block_set in bb.cleared_blocks:
            bb.block_clear(block_set)
            
        if bb.cleared_blocks != []:
            self.stop_update_timer = 35 + 15*len(bb.cleared_blocks)
       
       
    def update_blockbox(self):       
        if self.update_timer >= 0:
            self.update_timer -= 1
            
        else:
            Blockbox.block_group.update(self.rise_value)
            Blockbox.cursor_group.update(self.rise_value)
            self.update_counter += 1
            self.update_timer = self.max_update_value
        
            if self.update_counter == 7:
                self.update_counter = 0
                self.blox.update_blocks()
                
        self.rise_value = 3

    # Loop principal do programa
    def main_loop(self):
        running = 1
        pos_x = 0
        pos_y = 0
        
        aux_x = 0
        aux_y = 0
        
        q = 0
        
        self.load_sprites()
 
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.last_frame = self.frame_number
                        self.blox.cursor.move_cursor_UP(self.blox.rect) # Move Cursor pra cima
                        
                    elif event.key == pygame.K_DOWN:
                        self.last_frame = self.frame_number
                        self.blox.cursor.move_cursor_DOWN(self.blox.rect) # Move Cursor pra baixo
                        
                    elif event.key == pygame.K_LEFT:
                        self.last_frame = self.frame_number
                        self.blox.cursor.move_cursor_LEFT(self.blox.rect) # Move Cursor pra esquerda
                        
                    elif event.key == pygame.K_RIGHT:
                        self.last_frame = self.frame_number
                        self.blox.cursor.move_cursor_RIGHT(self.blox.rect) # Move Cursor pra direita
                        
                    # Tecla A inicia uma mudanca de blocos. Seta a flag change_fin e grava a posicao do cursor
                    elif event.key == pygame.K_a:
                        self.last_frame = self.frame_number
                        if [self.blox.cursor.pos_rel_x, self.blox.cursor.pos_rel_y] not in self.blox.changing_blocks:
                            self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x, self.blox.cursor.pos_rel_y])
                            #self.blox_cpu.changing_blocks.append((self.blox.cursor.pos_rel_x, self.blox.cursor.pos_rel_y))
            
                    # Tecla para testes. imprime as matrizes de blocos
                    elif event.key == pygame.K_f:
                        print "Matriz de configuracao de blocos"
                        self.blox.print_config_matrix()
                        print "Matriz de blocos"
                        self.blox.print_block_matrix()
                        print "Ativos"
                        self.blox.print_active()
                        print "Tempo Execucao medio"
                        print "{0:5f}".format(self.frame_counter/self.frame_number)
                        print "Numero de blocos no grupo"
                        print "{0:d}".format(len(Blockbox.block_group))
                    
                    elif event.key == pygame.K_q:
                        running = 0

                    elif event.key == pygame.K_l:
                        break
                        #self.cpu.raw_move_queue = [[0,1], [1,2], [1,3], [3,3], [5,6]]
                        #self.cpu.transform_movements()
                        #print self.cpu.raw_move_queue[0]

                    elif event.key == pygame.K_SPACE:
                        self.update_timer += 75
                        self.rise_value = 7

                    elif event.key == pygame.K_p:
                        if self.blox.stop_update:
                            self.blox.stop_update = False
                        else: self.blox.stop_update = True
                        #if self.p_flag == False:
                            #self.p_flag = True
                            #self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x, self.blox.cursor.pos_rel_y])
                            #self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x+1, self.blox.cursor.pos_rel_y])

                    elif event.key == pygame.K_r:
                        if self.r_flag == False:
                            self.r_flag = True
                            self.r_limit = random.randint(100, 200)

                    elif event.key == pygame.K_k:
                        if self.k_flag == False:
                            self.k_flag = True
                            self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x, self.blox.cursor.pos_rel_y])
                          

            self.p_count()
            
            self.k_count()
            
            self.r_count()
            
            #if self.cpu.t_move_queue != []:
                #self.cpu.execute_cpu_movements()
            
            if not self.blox.fail:
                self.change(self.blox)
                self.fall(self.blox)
                self.clear(self.blox)
            else:
                self.blox.failure()
            #self.change(self.cpu.blockbox)
            # process de queda de bloco
            #self.fall(self.cpu.blockbox)
            # processo de eliminacao de blocos
            #self.clear(self.cpu.blockbox)

            if not self.blox.stop_update:
                self.update_blockbox()            
            
            # Desenha a blockbox e depois seus elementos. Retorna a area em que desenhamos a blockbox para atualiza-la
            self.rectlist = self.blockbox_sprite.draw(self.screen)
            
            # Adiciona o retangulo do score na lista de retangulos a ser atualizados. Devemos fazer
            # isso pois o score fica fora da blockbox
            self.rectlist.append(self.blox.score.rect)
            self.rectlist.append(self.timer.update_chronometer())
            #self.rectlist.append(self.cpu.blockbox.score.rect)

            # Desenha os elementos da blockbox na tela
            Blockbox.block_group.draw(self.screen)
            Blockbox.cursor_group.draw(self.screen)
            Blockbox.score_group.draw(self.screen)
            self.timer_group.draw(self.screen)
            
            
            # Atualiza a tela apenas na area da blockbox e do score. Subsequentemente limpa a tela com o background
            pygame.display.update(self.rectlist)
            Blockbox.score_group.clear(self.screen, self.background)
            Blockbox.cursor_group.clear(self.screen, self.background)
            Blockbox.block_group.clear(self.screen, self.background)
            self.timer_group.clear(self.screen, self.background)
            
            # Como o score fica fora da blockbox, devemos limpar tambem a area ocupada por ele
            self.blockbox_sprite.clear(self.screen, self.background)

            # Jogo rodando em 60fps
            self.frame_number += 1
            self.frame_counter += self.clock.tick(30)
            
            
    """   METODOS PARA TESTES   """

    def p_count(self):
        if self.p_flag:
            self.p_counter += 1
            if self.p_counter == 1:
                 self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x, self.blox.cursor.pos_rel_y])
            if self.p_counter == 4:
                 self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x+1, self.blox.cursor.pos_rel_y])
                 self.p_counter = 0
                 self.p_flag = False
                 
    
    def k_count(self):
        if self.k_flag:
            self.k_counter += 1
            if self.k_counter == 1:
                 self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x-1, self.blox.cursor.pos_rel_y-1])
                 self.k_counter = 0
                 self.k_flag = False
                 
    # TESTE: Gera diversos movimentos aleatorios em espacos de frames pequeno para testar colisoes
    # entre operacoes
    def r_count(self):
        if self.r_flag:
            if self.r_counter < self.r_limit:
                if self.r_counter % 3 == 0:
                    aux_x = random.randint(0, 4)
                    aux_y = random.randint(0, 11)
                    print (aux_x, aux_y)
                    self.blox.changing_blocks.append([aux_x, aux_y])
            else:
                self.r_flag = False
                self.r_counter = 0
                self.r_limit = 0
                return
                
            self.r_counter += 1

        
if __name__ == "__main__":
    # Inicializa objeto main e entra no loop principal
    main_window = Main()
    main_window.main_loop()
