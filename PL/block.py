#! /usr/bin/env python
import pygame
import random
from adds import *

class Block(pygame.sprite.Sprite):
    # Dicionario guarda as imagens correspondentes aos blocos e suas animacoes. Indexado pelo
    # nome das cores. Cada cor guarda uma lista com as imagens da cor correspondente
    block_colors = {}
    block_colors["purple"] = []
    block_colors["blue"] = []    
    block_colors["yellow"] = []   
    block_colors["red"] = []   
    block_colors["green"] = []
    
    # Inicializacao
    def __init__(self, def_position, bw, bh, btype = None):
	
	# Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.block_width = bw
        self.block_height = bh
        
        
        # timer para o bloco comecar a cair
        self.fall_timer = 0
        
        # contador pra piscar o bloco
        self.blinking = 0
        self.b_counter = 1

        # valor que controla a queda de um bloco
        self.isFalling = False
        
        # indica queo bloco esta no meio da animacao de eliminacao. Nada pode acontecer com ele durante
        # essa animacao
        self.isClearing = False
        
        # indica que o bloco esta no meio da animacao de troca
        self.isChanging = False
    	
    	self.move_value = 0
    	
    	#
    	self.update_counter = 0
    	
	if btype == None:
	    self.block_type = random.randint(1,5)
	else: self.block_type = btype
	
	self.load_block_images()
	self.set_position(def_position)
             
    # Seta posicao inicial do bloco
    def set_position(self, (bb_rect_left, bb_rect_top, col_number, line_number)):
        self.line = line_number
        self.col = col_number
	
	self.rect.left = bb_rect_left + 10 + self.col*self.block_width
	self.rect.top = bb_rect_top + 5 + (11-self.line)*self.block_height
	
	
    def update(self, rise_value):
        self.change_position("up", rise_value)
        self.update_counter += rise_value
        if self.update_counter == 21:
            self.update_counter = 0
            self.change_coord("up", 1)
	
    # Muda posicao do bloco
    def change_position(self, direction, value):
	if direction == "left":
            self.rect.left -= value
        if direction == "right":
	    self.rect.left += value
	if direction == "down":
	    self.rect.top += value
	if direction == "up":
	    self.rect.top -= value
	    
    # Muda coordenada do bloco
    def change_coord(self, direction, value=1):
	if direction == "left":
            self.col -= value
        if direction == "right":
	    self.col += value
	if direction == "down":
	    self.line -= value 
	if direction == "up":
	    self.line += value 

    def set_clearing(self, flag):
        if flag:
            self.isClearing = True
            self.blinking = 45
        else:
            self.isClearing = False
            self.blinking = 0

    # efeito de piscar do bloco.
    def block_blinking(self):
	self.blinking -= self.b_counter
	if self.block_type == 0:
	    return
	else:
	    self.image = Block.block_colors[self.color_name][self.blinking%6]    
	return
    
    # Carrega as imagens referentes aos blocos em variaveis da classe, e seta elas para o objeto bloco
    # que estiver sendo instanciado
    def load_block_images(self):
	
	if self.block_type == 0:
	    self.color_name = "white"
	    self. isActive = False
	    self.rect = pygame.Rect(0, 0, self.block_width, self.block_height)
	    return
	
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
	    
        if Block.block_colors[self.color_name] == []:
            Block.block_colors[self.color_name] = [load_image(self.color_name+"_B"+str(i)+".PNG") for i in range(0,6)]

        self.image = Block.block_colors[self.color_name][0]
        self.image_ref = Block.block_colors[self.color_name][0]
            
        self.rect = self.image.get_rect()
        self. isActive = True

    # Limpa um bloco qualquer, ou seja, torna ele inativo
    def clear(self):
	self.block_type = 0
	self.isActive = False
	self.color_name = "white"
	self.image = None
	self.isClearing = False
	self.isFalling = False
	self.isChanging = False
	self.same_ver = False
	self.same_hor = False
        
        