#! /usr/bin/env python
import pygame
import random
from adds import *
from block import Block
from cursor import Choice_cursor

# Caixa que contem os blocos
class Blockbox(pygame.sprite.Sprite):
    # Inicializacao
    def __init__(self, w, h, pos_x, pos_y, screen, transp=128):

        # Inicia a classe Sprite
        pygame.sprite.Sprite.__init__(self)

        self.width = w
        self.height = h
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        # Trava o cursor enquanto dois blocos nao terminarem de mudar de posicao
        self.change_fin = True
        
        # valor que deve mudar a posicao de um bloco quando ele e mudado de lugar
        self.move_value = 0
        
        # lista contendo blocos afetados por mudancas
        self.changed = []
        
        # lista contendo os blocos que devem cair
        self.falling_blocks = []
        
        self.teste = 1

        self.image = load_image("blockbox.PNG")
        self.image.set_alpha(128)       
        self.rect = self.image.get_rect()
        
        self.rect.topleft = ((self.pos_x, self.pos_y))
        
        # inicia um cursor
        self.cursor = Choice_cursor(screen, self.rect, 22, 21)
        
        # cria um grupo de sprites para os blocos
        self.block_group = pygame.sprite.RenderUpdates()
        
        # cria um grupo de sprites para o cursor
        self.cursor_sprite = pygame.sprite.RenderUpdates(self.cursor)


    # Desenha a blockbox na tela
    def draw_elements(self, surf):
        self.block_group.draw(surf)
        self.cursor_sprite.draw(surf)


    # Cria a configuracao inicial de blocos na tela. Aleatoria, com maximo de 5 linhas preenchidas.
    def initiate_blocks(self):
	# Matriz de blocos a serem mostrados na tela
	self.block_matrix = [[]]
	
	# Matriz que representa abstracao da configuracao de blocos atual da tela
	self.block_config = [[]]
	
	# Altura da tela
	#self.max_height = random.randint(2,5)
	self.max_height = 8
	print self.max_height
	
	# Loop especifico para a primeira linha. Nunca adiciona bloco vazio
	for k in range(0,6):
	    # Escolhe um bloco aleatoriamente. Se 0, a posicao e vazia
	    btype = random.randint(1,5)
	    
	     # Cria um novo bloco de cor indicada por btype
	    b = Block((self.rect.left, self.rect.bottom-21), 22, 21, btype)
	    
	    # Apenda o novo bloco na matriz de blocos, e o numero correspondente na de
	    # configuracao
	    self.block_matrix[0].append(b)
	    self.block_config[0].append(b.block_type)
	    
	    # Adiciona o novo bloco criado ao grupo de sprites dos blocos e seta sua posicao
	    self.block_group.add(b)
	    b.set_position(self.rect, k, 0)



	# Percorre da segunda linha ate a altura maxima de inicio
	for i in range(1, self.max_height):
	    # Adiciona uma nova linha as matrizes
	    self.block_matrix.append([])
	    self.block_config.append([])
	    
	    # Loop que adiciona um bloco para cada coluna
	    for k in range(0,6):
	        
	        # Adiciona o bloco caso ele seja diferente de vazio, e existir bloco abaixo dele
	        if self.block_config[i-1][k] != 0: btype = random.randint(0,5)
	        else: btype = 0
		    
		# Cria um novo bloco de cor indicada por btype
	        b = Block((self.rect.left, self.rect.bottom-21), 22, 21, btype)
	            
	        # Apenda o novo bloco na matriz de blocos, e o numero correspondente na de
	        # configuracao
	        self.block_matrix[i].append(b)
	        self.block_config[i].append(b.block_type)
	            
	        # Adiciona o novo bloco criado ao grupo de sprites dos blocos e seta sua posicao
	        if(b.block_type != 0): self.block_group.add(b)
	        b.set_position(self.rect, k, i)


	for i in range(self.max_height, 12):
	    # Adiciona uma nova linha as matrizes
	    self.block_matrix.append([])
	    self.block_config.append([])
	    
	    for k in range(0,6):
                # Caso o tipo de bloco seja 0, apenda na matriz de blocos None na de config 0
                b = Block((self.rect.left, self.rect.bottom-21), 22, 21, 0)
                self.block_config[i].append(0)
	        self.block_matrix[i].append(b)
	        b.set_position(self.rect, k, i)
		    
	    	
    # Cuida da troca de lugar entre dois blocos
    def block_change(self, pos_x, pos_y):
	
	# Se a posicao dos blocos na tela nao tiver sido trocada completamente ainda, movimenta
	# cada bloco a ser trocado um pouco mais e retorna falso
	if self.move_value < 22:
	    #
	    self.block_matrix[pos_y][pos_x].change_position("right", 11)
	    self.block_matrix[pos_y][pos_x+1].change_position("left", 11)
	    self.move_value += 11
	    return False
	    
	# Se tiver terminado de trocar dois blocos de lugar, troca eles de lugar nas
	# determinadas matrizes
	else:
	    
	    # Flag checa se foi trocado um bloco inativo por um ativo. So e necessario checar se um
	    # blocos devem cair se em trocas se for trocado um inativo com um ativo
	    check = False
	    check = (self.block_matrix[pos_y][pos_x].isActive != self.block_matrix[pos_y][pos_x+1].isActive)
	    
	    # Troca os valores no bloco. Primeiro da esquerda depois da direita
	    self.block_matrix[pos_y][pos_x].col += 1
	    self.block_matrix[pos_y][pos_x+1].col -= 1
	    
	    
	    # Troca os blocos na matriz de blocos
	    aux_block = self.block_matrix[pos_y][pos_x+1]
	    self.block_matrix[pos_y][pos_x+1] = self.block_matrix[pos_y][pos_x]
	    self.block_matrix[pos_y][pos_x] = aux_block
	    
	    # Troca os valores na matriz de configuracao
	    aux_config = self.block_config[pos_y][pos_x+1]
	    self.block_config[pos_y][pos_x+1] = self.block_config[pos_y][pos_x]
	    self.block_config[pos_y][pos_x] = aux_config
	    
	    if check:		
	        self.changed.append(self.block_matrix[pos_y][pos_x])
	        self.changed.append(self.block_matrix[pos_y][pos_x+1])
	    
	    # reseta o valor de movimento
	    self.move_value = 0	
	    
	    return True
    
    # Checa se um bloco deve cair, e se sim, quantas posicoes
    def check_fall(self, pos_x, pos_y):
	
	# Se o bloco for ativo, checa se ele proprio deve cair
	if self.block_matrix[pos_y][pos_x].isActive:
	    if pos_y-1 >=0 and (not self.block_matrix[pos_y-1][pos_x].isActive):
		self.falling_blocks.append([self.block_matrix[pos_y][pos_x]])
	        self.block_matrix[pos_y][pos_x].fall_timer = 30
	# Se o bloco for inativo, checa se os blocos acima dele devem cair
	else:
	    k = pos_y+1
	    if self.block_matrix[k][pos_x].isActive:
		self.falling_blocks.append([self.block_matrix[k][pos_x]])
		self.block_matrix[k][pos_x].fall_timer = 30
		k+=1
	    while k < 12 and self.block_matrix[k][pos_x].isActive:
		self.falling_blocks[-1].append(self.block_matrix[k][pos_x])
		k+=1
		
	self.changed.remove(self.block_matrix[pos_y][pos_x])
        return
        
        
    def block_fall(self, block_set):
	
	if block_set[0].fall_timer != 0:
	    block_set[0].fall_timer -= 1
	    return

	pos_y = block_set[0].line
	pos_x = block_set[0].col

	if pos_y-1 >=0 and (not self.block_matrix[pos_y-1][pos_x].isActive):

	    for block in block_set:
		pos_y = block.line
	        pos_x = block.col
	        # Se a posicao dos blocos na tela nao tiver sido trocada completamente ainda, movimenta
	        # cada bloco a ser trocado um pouco mais e retorna falso
	        self.block_matrix[pos_y][pos_x].change_position("down", 21)
	        self.block_matrix[pos_y-1][pos_x].change_position("up", 21)
	    
	    # Se tiver terminado de trocar dois blocos de lugar, troca eles de lugar nas
	    # determinadas matrizes
	        
	    # Troca os valores no bloco. Primeiro da esquerda depois da direita
	        self.block_matrix[pos_y][pos_x].line -= 1
	        self.block_matrix[pos_y-1][pos_x].line += 1
	    	    
	    # Troca os blocos na matriz de blocos
	        aux_block = self.block_matrix[pos_y][pos_x]
	        self.block_matrix[pos_y][pos_x] = self.block_matrix[pos_y-1][pos_x]
	        self.block_matrix[pos_y-1][pos_x] = aux_block
	    
	    # Troca os valores na matriz de configuracao
	        aux_config = self.block_config[pos_y][pos_x]
	        self.block_config[pos_y][pos_x] = self.block_config[pos_y-1][pos_x]
	        self.block_config[pos_y-1][pos_x] = aux_config
	    
	    # reseta o valor de movimento
	        self.block_matrix[pos_y-1][pos_x].down_value = 0
	else:
	    self.falling_blocks.remove(block_set)
	    
	    
    def print_config_matrix(self):
        for i in range(11, -1, -1):
	    print self.block_config[i]
	    
    def print_block_matrix(self):
        line = ""
	for i in range(11, -1, -1):
	    line = line + "Linha{0:02d}:".format(i)
	    for k in range(0,6):
	        line = line + " B:{0:2d}  L:{1:2d}  C:{2:2d},".format(self.block_matrix[i][k].block_type, self.block_matrix[i][k].line, self.block_matrix[i][k].col)
	    print line
	    line = ""
	    
    def print_active(self):
        line = ""
	for i in range(11, -1, -1):
	    line = line + "Linha {0:02d}:".format(i)
	    for k in range(0,6):
	        line = line + "{0:10s}".format(str(self.block_matrix[i][k].isActive))
            print line
	    line = ""
        
