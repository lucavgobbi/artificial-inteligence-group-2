#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import pygame
import random
from pygame.locals import *
from blockbox import Blockbox
from cpu import Cpu
from adds import *
from ia import *
import copy
from chron import chronometer
from msg import MSG

if not pygame.font: 
    print "Warning: Fonts nao disponivel"
if not pygame.mixer: 
    print "Warning: Mixer nao disponivel"

# Cuida dos aspectos principais do jogo
class Main:
    
    # Inicializa classe main
    def __init__(self, width = 640, height = 480):
        ## Construtor
        #  @param width: largura da tela
        #  @param height: altura da tela
    
        # Inicializa pygame
        pygame.init()
        
        # largura e altura da tela
        self.width = width
        self.height = height
        
        # Seta o seguramento de teclas. Quando uma tecla e pressionada e segurada, da o efeito
        # de aperta-la diversas vezes
        pygame.key.set_repeat(60, 60)
        
        # areas 'sujas' da tela que devem ser atualizadas
        self.rectlist = []
        
        self.max_update_value = 36
        self.update_timer = self.max_update_value
        self.update_counter = 0
        self.rise_value = 3        
        self.stop_update_timer = 0
        self.stop_update = True
        self.font = pygame.font.Font(None, 24)
        
        # Inicializa janela principal com os tamanhos dados
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("Puzzle League")
        pygame.display.set_icon(load_image("icon.png"))
        
        # Inicializa o clock
        self.clock = pygame.time.Clock()
        self.clock_teste = pygame.time.Clock()
        
        # cria um background e anexa a tela
        self.background = pygame.Surface((self.width, self.height)).convert()
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        
        self.bb_list = []
        
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

        self.args = {'static': 1, 'file': 'no', 'height': 5, 'time': 3}
        self.read_args()

    def read_args(self):
        """
        ## Le argumentos passados na inicializa��o do programa
        """
        
        if len(sys.argv) == 1:
            return
        
        if len(sys.argv) != 9:
            print "Erro nos argumentos!"
            print "Formato: python main.py file file_name static value height value"
            print "file: Arquivo de base. file_name: nome (no para nenhum)"
            print "static: jogo dinamico ou estatico. value: 1/0"
            print "height: altura maxima inicial. value: 1 a 12"
            print "time: tempo de jogo. value: maior que 0. 0 significa jogo infinito"
            sys.exit()
        
        self.args = {}
        self.args[sys.argv[1]] = sys.argv[2]
        self.args[sys.argv[3]] = int(sys.argv[4])
        self.args[sys.argv[5]] = int(sys.argv[6])
        self.args[sys.argv[7]] = int(sys.argv[8])
        
        print self.args
 
    def load_sprites(self):
        """
        ## Carrega sprites e cria grupos de sprites de inicializacao. Inicializa tbm as blockboxes
        """
        
        # objetos principais da tela. Blox e o quadro que contem os blocos.
        self.blox = Blockbox(152, 262, 100, 150, self.screen, False, self.args["height"])
        self.cpu = Cpu((152, 262, 388, 150), self.screen, self.args["height"])
        
        # Grupo de sprites unico para o cursor e para a caixa de blocos.
        self.blockbox_sprite = pygame.sprite.RenderUpdates(self.blox)
        self.blockbox_sprite.add(self.cpu.blockbox)
        
        # Configuracao inicial de blocos. Se houver arquivo de par�metro, abre ele. Sen�o, inicia aleat�rio
        if self.args["file"] != "no":
            self.blox.file_initiate_blocks(self.args["file"])
            self.cpu.blockbox.file_initiate_blocks(self.args["file"])
        else:
            self.blox.initiate_blocks()
            self.cpu.blockbox.initiate_blocks()
        
        self.bb_list.append(self.blox)
        self.bb_list.append(self.cpu.blockbox)
        self.cpu.last_m = copy.deepcopy(self.cpu.blockbox.block_config)
        self.cpu.init_ia()
    
    def fall(self, bb):
        """
        ## Chama a funcao de checagem de queda para os blocos necessarios
        """
        clear_test = []
        
        for block_set in bb.falling_blocks:
            if bb.block_fall(block_set):
                clear_test.append(block_set)
        
        if clear_test != []:
            for block_set in clear_test:
                bb.falling_blocks.remove(block_set)
                if not bb.check_clear(block_set):
                    for block in block_set:
                        pos_x, pos_y = block
                        bb.block_matrix[pos_y][pos_x].chain_number = 0
    
    def change(self, bb):
        """
        ## Caso tenha sido dado o comando para mudar dois blocos de posicao, esse metodo chama o metodo
        ## que muda os dois blocos na posicao desejada de lugar
        """
        
        for block in bb.changing_blocks:
            bb.change_fin = bb.block_change(block)


    def clear(self, bb):
        """
        ## Checa se existem blocos de uma determinada blockbox que devem ser eliminados. Quando eliminar blocos,
        ## para de atualizar a tela por alguns frames
        """
        
        for block_set in bb.cleared_blocks:
            bb.block_clear(block_set)
        
        if bb.cleared_blocks != []:
            self.stop_update_timer = 35 + 15*len(bb.cleared_blocks)
    
    def update_blockbox(self, bb):  
        """
        ## Atualiza a blockbox dada, subindo um pouco a pilha de blocos. Caso tenha subido o suficiente para adicionar
        ## uma nova linha, adiciona.
        """
        
        if bb.update_timer > 0:
            if not self.args["static"]: bb.update_timer -= 1
        
        else:
            bb.block_group.update(self.rise_value)
            bb.cursor_group.update(self.rise_value)
            bb.update_counter += 1
            bb.update_timer = bb.max_update_value
            
            if bb.update_counter == 7:
                bb.update_counter = 0
                bb.update_blocks()
                # Se a blockbox for CPU, mata a thread, atualiza a posi��o do cursor e se nao tiver falhado,
                # reinicia a IA
                if bb.cpu:
                    kill_thread()
                    self.cpu.cursor_final_position[1] += 1
                    if not bb.fail: self.cpu.init_ia()
        
        bb.rise_value = 3
    
    def main_loop(self):
        """
        # Loop principal do programa
        """
        
        running = 1
        pos_x = 0
        pos_y = 0
        
        aux_x = 0
        aux_y = 0
        
        q = 0
        
        self.load_sprites()
        Start = False

        # Mensagem da tela inicial
        self.msg1 = MSG("APERTE ESPA�O PARA COME�AR", 24, (170, 100), (255,255,255))
        self.msg_group = pygame.sprite.RenderUpdates(self.msg1)
        self.rectlist = self.msg_group.draw(self.screen)
        pygame.display.update(self.rectlist)
        
        # Tela inicial pedindo para apertar espa�o
        while running == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                    kill_thread()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:                   
                        running = 2

        self.msg_group.clear(self.screen, self.background)
        pygame.display.update(self.rectlist)
        self.msg_group.remove(self.msg1)

        self.timer = chronometer(pygame.time.get_ticks(), 10, 10)
        self.timer_group = pygame.sprite.RenderUpdates()
        self.timer_group.add(self.timer)

        # Tela de jogo. Trata todas as keys poss�veis, e trata os elementos e chamadas principais do jogo
        while running == 2:
            if self.args["time"] != 0:
                if self.timer.min_elapsed >= self.args["time"] or self.timer.min_elapsed >= 10:
                    kill_thread()
                    break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                    self.cpu.saveKnowMoves()
                    kill_thread()

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
                        print "{0:d}".format(len(self.blox.block_group))

                    # Tecla adicional para fechar
                    elif event.key == pygame.K_q:
                        running = 0
                        self.cpu.saveKnowMoves()
                        kill_thread()

                    # Teste
                    elif event.key == pygame.K_l:
                        if not Start:
                            Start = True
                        else:
                            Start = False
                            self.cpu.t_move_queue = []
                            self.cpu.raw_move_queue = []

                    # For�a subida de blocos
                    elif event.key == pygame.K_SPACE:
                        self.blox.update_timer = 0

                    # Teste
                    elif event.key == pygame.K_p:
                        if self.blox.stop_update != 0:
                            self.blox.stop_update = 0
                            self.cpu.blockbox.stop_update = 0
                        else: 
                            self.blox.stop_update = -1
                            self.cpu.blockbox.stop_update = -1
                    # Teste
                    elif event.key == pygame.K_r:
                        self.cpu.call_ia()
                        """if self.r_flag == False:
                            self.r_flag = True
                            self.r_limit = random.randint(100, 200)"""
                    # Teste
                    elif event.key == pygame.K_k:
                        if self.k_flag == False:
                            self.k_flag = True
                            self.blox.changing_blocks.append([self.blox.cursor.pos_rel_x, self.blox.cursor.pos_rel_y])
            
            # Testes
            self.p_count()
            self.k_count()   
            self.r_count()
            # /Testes

            # Chama a IA toda vez do loop. Detalhes adicionais na fun��o chamada
            self.cpu.call_ia2()

            # Se A IA quiser linha, nao tiver thread viva, a fila de movimentos estiver vazia, e nao tiver blocos caindo, for�a
            # adi��o de linhas
            if self.cpu.need_line and not self.cpu.ia.isAlive() and self.cpu.t_move_queue == [] and self.cpu.blockbox.falling_blocks == []:
                self.cpu.rise_line()
                    
            # Se houver movimentos para executar, executa eles
            if self.cpu.t_move_queue != []:
                self.cpu.execute_cpu_movements()
            
            # Para todos os blockboxes presentes na tela, ve se h� trocas, v� se h� quedas e v� se h� elimina��es.
            # S� faz isso tudo se o blockbox nao estiver em estado de falha
            for blockbox in self.bb_list:
                if not blockbox.fail:
                    self.change(blockbox)
                    self.fall(blockbox)
                    self.clear(blockbox)
                    if blockbox.stop_update == 0:
                        self.update_blockbox(blockbox)
                    
                    elif blockbox.stop_update > 0: blockbox.stop_update -= 1
                else:
                    # Se o tratamento de falha terminar e for blockbox de CPU, reinicia a IA
                    if blockbox.failure() and blockbox.cpu:
                        self.cpu.init_ia()
            
            # Desenha a blockbox e depois seus elementos. Retorna a area em que desenhamos a blockbox para atualiza-la
            self.rectlist = self.blockbox_sprite.draw(self.screen)
            
            # Adiciona o retangulo do score na lista de retangulos a ser atualizados. Devemos fazer
            # isso pois o score fica fora da blockbox
            self.rectlist.append(self.blox.score.rect)
            self.rectlist.append(self.cpu.blockbox.score.rect)
            self.rectlist.append(self.timer.update_chronometer())
            
            # Desenha os elementos da blockbox na tela
            for blockbox in self.bb_list:          
                blockbox.block_group.draw(self.screen)
                blockbox.cursor_group.draw(self.screen)
            Blockbox.score_group.draw(self.screen)
            self.timer_group.draw(self.screen)
            
            
            # Atualiza a tela apenas na area da blockbox e do score. Subsequentemente limpa a tela com o background
            pygame.display.update(self.rectlist)
            for blockbox in self.bb_list: 
                blockbox.block_group.clear(self.screen, self.background)
                blockbox.cursor_group.clear(self.screen, self.background)
            Blockbox.score_group.clear(self.screen, self.background)
            self.timer_group.clear(self.screen, self.background)
            
            # Como o score fica fora da blockbox, devemos limpar tambem a area ocupada por ele
            self.blockbox_sprite.clear(self.screen, self.background)
            
            # Jogo rodando em 30fps
            self.frame_number += 1
            self.frame_counter += self.clock.tick(30)


        # Ultima atualiza���o da tela limpando todos os elementos do jogo (chamada quando acaba o jogo)
        pygame.display.update(self.rectlist)
        for blockbox in self.bb_list:
            blockbox.block_group.clear(self.screen, self.background)
            blockbox.cursor_group.clear(self.screen, self.background)
        Blockbox.score_group.clear(self.screen, self.background)
        self.timer_group.clear(self.screen, self.background)
        self.blockbox_sprite.clear(self.screen, self.background)
        pygame.display.update(self.rectlist)


        # Cria as mensagens da �ltima tela
        msg_player = MSG("PLAYER", 38, (70, 140), (0,0,255))
        msg_cpu = MSG("CPU", 38, (350, 140), (255,0,0))

        score_player = MSG("SCORE: " + str(self.blox.score.value), 24, (70, 190), (255,255,255))
        score_cpu = MSG("SCORE: " + str(self.cpu.blockbox.score.value), 24, (350, 190), (255,255,255))

        l_combo_player = MSG("MAIOR COMBO: " + str(self.blox.largest_combo), 24, (70, 240), (255,255,255))
        l_combo_cpu = MSG("MAIOR COMBO: " + str(self.cpu.blockbox.largest_combo), 24, (350, 240), (255,255,255))

        l_chain_player = MSG("MAIOR CHAIN: " + str(self.blox.largest_chain), 24, (70, 290), (255,255,255))
        l_chain_cpu = MSG("MAIOR CHAIN: " + str(self.cpu.blockbox.largest_chain), 24, (350, 290), (255,255,255))


        if self.blox.score.value >= self.cpu.blockbox.score.value:
            msg_vitoria = MSG("VITORIA!", 38, (70, 90), (0,0,255))
        else:
            msg_vitoria = MSG("VITORIA!", 38, (350, 90), (255,0,0))

        self.msg_group.add(msg_player, msg_cpu, score_player, score_cpu, l_combo_player, l_combo_cpu, l_chain_player, l_chain_cpu, msg_vitoria)

        # Controla a �ltima tela, de mostra dos scores
        running = 3
        while running == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                    kill_thread()
                    
            self.rectlist = self.msg_group.draw(self.screen)
            pygame.display.update(self.rectlist)
            self.msg_group.clear(self.screen, self.background)
            
    
    
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
