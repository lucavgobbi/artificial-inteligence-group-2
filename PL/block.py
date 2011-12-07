#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
from adds import *

class Block(pygame.sprite.Sprite):
    """
    ## Representa um bloquinho que aparece na tela
    """
    
    
    # Dicionario guarda as imagens correspondentes aos blocos e suas animacoes. Indexado pelo
    # nome das cores. Cada cor guarda uma lista com as imagens da cor correspondente
    block_colors = {}
    block_colors["purple"] = []
    block_colors["blue"] = []    
    block_colors["yellow"] = []   
    block_colors["red"] = []   
    block_colors["green"] = []
    block_colors["grey"] = []
    
    
    # Inicializacao
    def __init__(self, def_position, bw, bh, btype = None):
        """
        ## Construtor
        # @param def_position: valores que orientam posição inicial do bloco e suas coordenadas
        # @param bw: largura do bloco
        # @param bh: altura do bloco
        # @btype: numero que representa a cor do bloco
        """
        
        # Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)
        
        # seta largura e altura do bloco
        self.block_width = bw
        self.block_height = bh
        
        
        # timer para o bloco comecar a cair
        self.fall_timer = 0
        
        # contador pra efeito de piscar o bloco
        self.max_blinking_value = 25
        self.blinking = 0
        self.b_counter = 1

        # indica que o bloco está no meio da animação de queda
        self.isFalling = False
        
        # indica que o bloco esta no meio da animacao de eliminacao. Nada pode acontecer com ele durante
        # essa animacao
        self.isClearing = False
        
        # indica que o bloco esta no meio da animacao de troca
        self.isChanging = False
        
        # indica a qual numero de chain o bloco pertence se ele estiver sendo eliminado
        self.chain_number = 0
        
        # valores controlam atualização dos blocos na tela
        self.move_value = 0   
        self.update_counter = 0
        
        # se o tipo passado para o bloc for None, randomiza uma cor para ele
        if btype == None:
            self.block_type = random.randint(1,5)
        else: self.block_type = btype
        
        # carrgea a imagem do bloco
        self.load_block_images()
        
        # posiciona bloco na tela
        self.set_position(def_position)
             
    def set_position(self, (bb_rect_left, bb_rect_top, col_number, line_number)):
        """
        ## Seta posição inicial do bloco na tela e suas coordenadas
        # @param (bb_rect_left, bb_rect_top, col_number, line_number): orienta valores de posicionamento do bloco
        """
        
        self.line = line_number
        self.col = col_number
        
        self.rect.left = bb_rect_left + 10 + self.col*self.block_width
        self.rect.top = bb_rect_top + 5 + (11-self.line)*self.block_height


    def update(self, rise_value):
        """
        ## Atualiza blocos na tela após subida parcial ou total de uma nova linha, dado uma quantidade
        ## de pixels que deve subir
        #  @param rise_value: quantidade de pixels que o blocodeve subir
        """
        
        self.change_position("up", rise_value)
        self.update_counter += rise_value
        if self.update_counter == 21:
            self.update_counter = 0
            
    
    def change_position(self, direction, value):
        """
        ## Muda posicao do bloco dada uma direção e um valor de pixels
        #  @param direction: direção da mudança
        #  @param value: valor de pixels
        """
        
        if direction == "left":
            self.rect.left -= value
        if direction == "right":
            self.rect.left += value
        if direction == "down":
            self.rect.top += value
        if direction == "up":
            self.rect.top -= value
 
    def change_coord(self, direction, value=1):
        """
        ## Muda coordenada do bloco dada uma direção e um valor
        #  @param direction: direção da mudança
        #  @param value: número de posições
        """
        
        if direction == "left":
            self.col -= value
        if direction == "right":
            self.col += value
        if direction == "down":
            self.line -= value 
        if direction == "up":
            self.line += value 

    def set_clearing(self, flag):
        """
        ## Coloca ou tira o bloco de condição de eliminação
        #  @param flag: booleano que diz se deve ser colocado ou tirado na condição
        """
        if flag:
            self.isClearing = True
            self.blinking = self.max_blinking_value
        else:
            self.isClearing = False
            self.blinking = 0

    def block_blinking(self):
        """
        ## Efeito de piscar que acontece na eliminação de um bloco
        """
        
        # vai diminuindo um contador que controla o efeito de piscar até que ele seja 0. Enquanto
        # não for zero, cicla pelas imagens que tem diferentes tonalidades de brilho para o bloco
        # de acordo com o contador
        self.blinking -= self.b_counter
        if self.block_type == 0:
            return
        else:
            self.image = Block.block_colors[self.color_name][self.blinking%6]
            return
    
    def load_block_images(self):
        """
        # Carrega as imagens referentes aos blocos em variaveis da classe, e seta elas para o objeto bloco
        # que estiver sendo instanciado. Evita que seja carregada uma imagem sempre que criado um bloco.
        """
        
        # Se o tipo do bloco for 0, inicia ele como inativo, e sem imagem
        if self.block_type == 0:
            self.color_name = "white"
            self. isActive = False
            self.rect = pygame.Rect(0, 0, self.block_width, self.block_height)
            return
        
        # Se o tipo do bloco for 6, inicia ele com imagem de bloco cinza, mas inativo ("bloco morto")
        elif self.block_type == 6:
            self.color_name = "grey"
            if Block.block_colors[self.color_name] == []:
                Block.block_colors[self.color_name] = [load_image(self.color_name+"_B0.png")]
            self.image = Block.block_colors[self.color_name][0]
            self.image_ref = Block.block_colors[self.color_name][0]          
            self.rect = self.image.get_rect()
            self.isActive = False
        
        # Qualquer outro tipo de bloco, seta o nome e depois cicla carregando os blocos em suas tonalidades
        # para a lista de imagens do bloco instanciado
        if self.block_type == 1:
            self.color_name = "purple"

        elif self.block_type == 2:
            self.color_name = "blue"

        elif self.block_type == 3:
            self.color_name = "yellow"
            
        elif self.block_type == 4:
            self.color_name = "red"

        elif self.block_type == 5:
            self.color_name = "green"
            
        try:
            if Block.block_colors[self.color_name] == []:
                Block.block_colors[self.color_name] = [load_image(self.color_name+"_B"+str(i)+".png") for i in range(0,7)]
                Block.block_colors[self.color_name].set_colorkey((255,0,255))
                Block.block_colors[self.color_name].set_alpha(128)
        except AttributeError:
            print self.block_type

        self.image = Block.block_colors[self.color_name][0]
        self.image_ref = Block.block_colors[self.color_name][0]
            
        self.rect = self.image.get_rect()
        self.isActive = True


    def clear(self):
        """
        # Limpa todas as informações de um bloco qualquer, ou seja, torna ele inativo
        """
        self.block_type = 0
        self.isActive = False
        self.color_name = "white"
        self.image = None
        self.isClearing = False
        self.isFalling = False
        self.isChanging = False
        self.same_ver = False
        self.same_hor = False
        
        