#! /usr/bin/env python
import pygame
import random
from adds import *

class Block(pygame.sprite.Sprite):
    blueblock = None
    purpleblock = None
    yellowblock = None
    redblock = None
    greenblock = None
    
    # Inicializacao
    def __init__(self, position, bw, bh, btype = None):
	
	# Inicializa classe sprite
        pygame.sprite.Sprite.__init__(self)
        
        self.block_width = bw
        self.block_height = bh
        
        # valor que controla a queda de um bloco
        self.falling = False
        
        # numero de posicoes que deve cair
        self.fall_number = 0
        
        # timer para o bloco comecar a cair
        self.fall_timer = 0
        
        # valor mudado para o efeito gravitacional no bloco
        self.down_value = 0
        
    	
	if btype == None:
	    self.block_type = random.randint(1,5)
	else: self.block_type = btype
	
	self.load_block_images()
             

    def set_position(self, bb_rect, col_number, line_number):
        self.line = line_number
        self.col = col_number
	
	self.rect.left = bb_rect.left + 10 + self.col*self.block_width
	self.rect.top = bb_rect.top + 5 + (11-self.line)*self.block_height
	
	
    def change_position(self, direction, value):
	if direction == "left":
            self.rect.left -= value
        if direction == "right":
	    self.rect.left += value
	if direction == "down":
	    self.rect.top += value
	    
    def change_coord(self, direction, value=1):
	if direction == "left":
            self.col -= value
        if direction == "right":
	    self.col += value
	if direction == "down":
	    self.line -= value 
	    
    def block_fall(self):
	if self.fall_timer == 0:
	        self.change_position("down", 21)
	        self.change_coord("down", 1)
	        return False
	else: self.fall_timer -= 1
	print self.fall_timer
	return False
	    
    def load_block_images(self):
	
	if self.block_type == 0:
	    self. isActive = False
	    self.rect = pygame.Rect(0, 0, self.block_width, self.block_height)
	    return
	
	if self.block_type == 1:
            if Block.purpleblock is None:
                Block.purpleblock = load_image("purple.PNG")

            self.image = Block.purpleblock

        elif self.block_type == 2:
            if Block.blueblock is None:
                Block.blueblock = load_image("blue.PNG")

            self.image = Block.blueblock

        elif self.block_type == 3:
            if Block.yellowblock is None:
                Block.yellowblock = load_image("yellow.PNG")

            self.image = Block.yellowblock
            
        elif self.block_type == 4:
            if Block.redblock is None:
                Block.redblock = load_image("red.PNG")

            self.image = Block.redblock

        elif self.block_type == 5:
            if Block.greenblock is None:
                Block.greenblock = load_image("green.PNG")

            self.image = Block.greenblock
            
        self.rect = self.image.get_rect()
        self. isActive = True
        