#! /usr/bin/env python
import pygame
import random
from adds import *
from block import Block
from cursor import Choice_cursor

# Caixa que contem os blocos
class Blockbox(pygame.sprite.Sprite):
    # cria um grupo de sprites para os blocos
    block_group = pygame.sprite.RenderUpdates()
    
    # cria um grupo de sprites para os cursores
    cursor_group = pygame.sprite.RenderUpdates()
    
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
        
        # lista contendo grupo de blocos que devem cair
        self.falling_blocks = []
        
        # lista contendo grupos de blocos que devm ser eliminados
        self.cleared_blocks = []
        
        self.teste = 1

        self.image = load_image("blockbox.PNG")
        self.image.set_alpha(128)       
        self.rect = self.image.get_rect()
        
        self.rect.topleft = ((self.pos_x, self.pos_y))
        
        # inicia um cursor
        self.cursor = Choice_cursor(screen, self.rect, 22, 21)
           
        self.cursor_group.add(self.cursor)


    # Desenha a blockbox na tela
    def draw_elements(self, surf):
        return

    # Cria a configuracao inicial de blocos na tela. Aleatoria, com maximo de 5 linhas preenchidas.
    def initiate_blocks(self):
	# Matriz de blocos a serem mostrados na tela
	self.block_matrix = [[]]
	
	# Matriz que representa abstracao da configuracao de blocos atual da tela
	self.block_config = [[]]
	
	# Altura da tela
	#self.max_height = random.randint(2,5)
	self.max_height = 8
	
	# Loop especifico para a primeira linha. Nunca adiciona bloco vazio
	for k in range(0,6):
	    # Escolhe um bloco aleatoriamente. Se 0, a posicao e vazia
	    btype = random.randint(1,5)
	    
	     # Cria um novo bloco de cor indicada por btype
	    b = Block((self.rect.left, self.rect.top, k, 0), 22, 21, btype)
	    
	    # Apenda o novo bloco na matriz de blocos, e o numero correspondente na de
	    # configuracao
	    self.block_matrix[0].append(b)
	    self.block_config[0].append(b.block_type)
	    
	    # Adiciona o novo bloco criado ao grupo de sprites dos blocos e seta sua posicao
	    Blockbox.block_group.add(b)



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
	        b = Block((self.rect.left, self.rect.top, k, i), 22, 21, btype)
	            
	        # Apenda o novo bloco na matriz de blocos, e o numero correspondente na de
	        # configuracao
	        self.block_matrix[i].append(b)
	        self.block_config[i].append(b.block_type)
	            
	        # Adiciona o novo bloco criado ao grupo de sprites dos blocos e seta sua posicao
	        if(b.block_type != 0): Blockbox.block_group.add(b)


	for i in range(self.max_height, 12):
	    # Adiciona uma nova linha as matrizes
	    self.block_matrix.append([])
	    self.block_config.append([])
	    
	    for k in range(0,6):
                # Caso o tipo de bloco seja 0, apenda na matriz de blocos None na de config 0
                b = Block((self.rect.left, self.rect.top, k, i), 22, 21, 0)
                self.block_config[i].append(0)
	        self.block_matrix[i].append(b)
		    
	    	
    # Cuida da troca de lugar entre dois blocos
    def block_change(self, pos_x, pos_y):
	
	block_left = self.block_matrix[pos_y][pos_x]
	block_right = self.block_matrix[pos_y][pos_x+1]
	
	block_number_left = self.block_config[pos_y][pos_x]
	block_number_right = self.block_config[pos_y][pos_x+1]
	
	if block_left.isClearing or block_right.isClearing or block_left.isFalling or block_right.isFalling: 
	    return True
	
	# Se a posicao dos blocos na tela nao tiver sido trocada completamente ainda, movimenta
	# cada bloco a ser trocado um pouco mais e retorna falso
	if self.move_value < 22:
	    #
	    block_left.change_position("right", 11)
	    block_right.change_position("left", 11)
	    self.move_value += 11
	    return False
	    
	# Se tiver terminado de trocar dois blocos de lugar, troca eles de lugar nas
	# determinadas matrizes
	else:
	    
	    # Flag checa se foi trocado um bloco inativo por um ativo. So e necessario checar se um
	    # blocos devem cair se em trocas se for trocado um inativo com um ativo
	    check = False
	    check = (block_left.isActive != block_right.isActive)
	    
	    # Troca os valores no bloco. Primeiro da esquerda depois da direita
	    block_left.col += 1
	    block_right.col -= 1
	    	    
	    # Troca os blocos na matriz de blocos
	    self.block_matrix[pos_y][pos_x+1] = block_left
	    self.block_matrix[pos_y][pos_x] = block_right
	    
	    # Troca os valores na matriz de configuracao
	    self.block_config[pos_y][pos_x+1] = block_number_left
	    self.block_config[pos_y][pos_x] = block_number_right
	    
	    if check:		
	        self.changed.append((block_left.col, block_left.line))
	        self.changed.append((block_right.col, block_right.line))
	        
	    #if block_left.block_type != block_right.block_type:
		#clear_left = []
		#clear_right = []
		#self.check_clear_down((block_left.col, block_left.line), clear_left)
		#self.check_clear_up((block_left.col, block_left.line), clear_left)
		#self.check_clear_down((block_right.col, block_right.line), clear_right)
		#self.check_clear_up((block_right.col, block_right.line), clear_right)
		#if len(clear_left) >= 3: self.cleared_blocks.append(clear_left)
		#if len(clear_right) >= 3: self.cleared_blocks.append(clear_right)
	    
	    # reseta o valor de movimento
	    self.move_value = 0	
	    
	    return True
    
    # Checa se um bloco deve cair, e se sim, quantas posicoes
    def check_fall(self, (pos_x, pos_y)):
	
	# Se o bloco for ativo, checa se ele proprio deve cair
	if self.block_matrix[pos_y][pos_x].isActive:
	    if pos_y-1 >=0 and (not self.block_matrix[pos_y-1][pos_x].isActive):
		self.falling_blocks.append([self.block_matrix[pos_y][pos_x]])
		self.block_matrix[pos_y][pos_x].isFalling = True
	        self.block_matrix[pos_y][pos_x].fall_timer = 5        
	        
	# Se o bloco for inativo, checa se os blocos acima dele devem cair. Se devem, cria uma
	# lista com esses blocos e adiciona na lista de blocos em queda. Essa lista representa
	# um grupo de blocos que deve cair, e o seu timer e o do primeiro bloco da lista
	else:
	    k = pos_y+1
	    if self.block_matrix[k][pos_x].isClearing:
		return
	    bl = []
	    while k < 12 and self.block_matrix[k][pos_x].isActive:
		bl.append(self.block_matrix[k][pos_x])
		self.block_matrix[k][pos_x].isFalling = True
		self.block_matrix[k][pos_x].fall_timer = 5
		k+=1
	    if bl != []: self.falling_blocks.append(bl)
		
	self.changed.remove((pos_x, pos_y))
        return
        
    # Cuida da queda de blocos. Recebe um grupo de blocos que deve cair. A logica e que temos um bloco
    # mestre no grupo, que e o primeiro da lista, ou seja o bloco na linha de menor numero. Ele sempre
    # olha o bloco abaixo de si. Caso ess seja inativo, troca uma posicao para baixo sua e de todos os
    # outros blocos da lista. Caso nao, para de cair
    def block_fall(self, block_set):
	
	# Timer no primeiro elemento do grupo de blocos que deve cair. Assim que zerar, o
	# grupo comeca a cair
	if block_set[0].fall_timer != 0:
	    for b in block_set:
	        b.fall_timer -= 1
	    return

	pos_y = block_set[0].line
	pos_x = block_set[0].col
	
	# Se a posicao do primeiro bloco do grupo de blocos em queda nao for linha 0 e o 
	# bloco abaixo dele for inativo, o grupo cai uma posicao. Essa queda e feita
	# trocando-se o bloco de lugar com o que esta abaixo dele
	
	if pos_y-1 >=0 and (not self.block_matrix[pos_y-1][pos_x].isActive):
	    
	    # Movimenta cada bloco do grupo de blocos que deve cair uma posicao para baixo
	    # trocando ele de lugar com o bloco abaixo dele.
	    for block in block_set:
		pos_y = block.line
	        pos_x = block.col
	        
	        # Movimenta o bloco para baixo e o abaixo dele para cima
	        self.block_matrix[pos_y][pos_x].change_position("down", 21)
	        
	        # Troca os valores no bloco. Primeiro da cima depois baixo
	        self.block_matrix[pos_y][pos_x].line -= 1
	    	    
	        # Troca os blocos na matriz de blocos
	        self.block_matrix[pos_y-1][pos_x] = self.block_matrix[pos_y][pos_x]
	    
	        # Troca os valores na matriz de configuracao
	        self.block_config[pos_y-1][pos_x] = self.block_config[pos_y][pos_x]
	        
	    self.block_matrix[pos_y][pos_x] = Block((self.rect.left, self.rect.top, pos_x, pos_y), 22, 21, 0)
	    self.block_config[pos_y][pos_x] = 0
	    
	else:
	    # Se o bloco inicial do grupo nao estiver na linha 0, iguala seu timer ao bloco abaixo dele
	    # fazemos isso pois possivel que o grupo de blocos tenha sido parado no ar por um bloco que
	    # deve cair. Se o timer copiado for diferente de 0, temos essa situacao, entao devemos
	    # "sincronizar" o grupo de blocos em queda com o bloco parado no ar esperando para cair
	    # e derrubar todos juntos
	    if pos_y != 0:
		 for b in block_set:
		     b.fall_timer = self.block_matrix[pos_y-1][pos_x].fall_timer
		
	    if self.block_matrix[pos_y-1][pos_x].fall_timer == 0:
		for b in block_set: b.isFalling = False
		#self.check_clear(block_set)
		self.falling_blocks.remove(block_set)	

    # Checa se ha eliminacao de blocos em grupos de blocos que cairam. Comeca checando toda a volta
    # do bloco mais inferior do grupo, adicionano a um novo grupo de blocos que devem ser eliminados
    # os que tiverem que ser. Depois, para cada bloco mais acima, checa a direita e a esquerda, adic
    # ionando ao grupo conforme necessario. Se no final dos testes mais de tres blocos tiverem sido
    # adicionandos, signiica que esse grupo deve ser eliminado, entao adiciona o grupo a lista que
    # contem os grupos de blocos que devem ser eliminados.
    def check_clear(self, block_set):
	added = 0
	clear = []
	#added += self.check_clear_down((block_set[0].col, block_set[0].line), clear)
	#added += self.check_clear_up((block_set[0].col, block_set[0].line), clear)
	#added += self.check_clear_left((block_set[0].col, block_set[0].line), clear)
	#added += self.check_clear_right((block_set[0].col, block_set[0].line), clear)
	#if added < 3: clear = []
	for b in block_set:
	    added_sides = 0
	    clear_sides = [(b.col, b.line)]
	    added_down = 0
	    clear_down = [(b.col, b.line)]
	    new_added += self.check_clear_left((b.col, b.line), clear_sides)
	    new_added += self.check_clear_right((b.col, b.line), clear_sides)
	    new_added += self.check_clear_down((b.col, b.line), new_clear)
	    if new_added >= 3: 
	        clear.extend(new_clear)
	        added += new_added
	        
	print clear    
	if added >= 3: self.cleared_blocks.append(clear)

    # Auxiliar de eliminacao. Checa se o blocos abaixo de determinando bloco sao iguais a ele
    def check_clear_down(self, (pos_x, pos_y), clear):
	c = 0
	"""if (pos_x, pos_y) not in clear: 
	    clear.append((pos_x, pos_y))
	    c += 1"""
	    
	if self.look_down((pos_x, pos_y)):
	    if (pos_x, pos_y-1) not in clear: 
	        clear.append((pos_x, pos_y-1))
	        c += 1
	        
	    if self.look_down((pos_x, pos_y-1)): 
	        clear.append((pos_x, pos_y-2))
	        c += 1
	return c
	        
    # Auxiliar de eliminacao. Checa se o blocos acima de determinando bloco sao iguais a ele	        
    def check_clear_up(self, (pos_x, pos_y), clear):
	c = 0
        """if (pos_x, pos_y) not in clear: 
	    clear.append((pos_x, pos_y))
	    c += 1"""
	    
	if self.look_up((pos_x, pos_y)):
	    if (pos_x, pos_y+1) not in clear: 
	        clear.append((pos_x, pos_y+1))
	        c += 1
	        
	    if self.look_up((pos_x, pos_y+1)): 
	        clear.append((pos_x, pos_y+2))
	        c += 1
	return c
	
    # Auxiliar de eliminacao. Checa se o blocos a esquerda de determinando bloco sao iguais a ele	
    def check_clear_left(self, (pos_x, pos_y), clear):
	c = 0
        """if (pos_x, pos_y) not in clear: 
	    clear.append((pos_x, pos_y))
	    c += 1"""
	    
	if self.look_left((pos_x, pos_y)):
	    if (pos_x-1, pos_y) not in clear: 
	        clear.append((pos_x-1, pos_y))
	        c += 1
	        
	    if self.look_left((pos_x-1, pos_y)): 
	        clear.append((pos_x-2, pos_y))
	        c += 1
	return c
	
    # Auxiliar de eliminacao. Checa se o blocos a direita de determinando bloco sao iguais a ele	
    def check_clear_right(self, (pos_x, pos_y), clear):
	c = 0
        """if (pos_x, pos_y) not in clear: 
	    clear.append((pos_x, pos_y))
	    c += 1"""
	    
	if self.look_right((pos_x, pos_y)):
	    if (pos_x+1, pos_y) not in clear: 
	        clear.append((pos_x+1, pos_y))
	        c += 1
	        
	    if self.look_right((pos_x+1, pos_y)): 
	        clear.append((pos_x+2, pos_y))
	        c += 1
	return c


    # Responsavel pela eliminacao de fato dos blocos. E chamada em grupos de blocos marcados para
    # eliminacao. Cuida da animacao da elminacao e da remocao dos blocos nesses grupos dos blocos
    # ativos
    def block_clear(self, block_set):
	pos_x, pos_y = block_set[0]
	
	if not self.block_matrix[pos_y][pos_x].isClearing:
	    for bpos in block_set:
		pos_x, pos_y = bpos
	        self.block_matrix[pos_y][pos_x].isClearing = True
	        self.block_matrix[pos_y][pos_x].blinking = 25
	        self.block_matrix[pos_y][pos_x].block_blinking()
	    return
        for bpos in block_set:
	    pos_x, pos_y = bpos
	    self.block_matrix[pos_y][pos_x].block_blinking()
	    
	if self.block_matrix[pos_y][pos_x].blinking == 0:
	    aux = []
	    for bpos in block_set:
		pos_x, pos_y = bpos
		self.changed.append(bpos)
		self.block_matrix[pos_y][pos_x].clear()
		self.block_config[pos_y][pos_x] = 0
		Blockbox.block_group.remove(self.block_matrix[pos_y][pos_x])
	    self.cleared_blocks.remove(block_set)
	    return
	
	        
	
	
    # Checa se bloco da esquerda e da mesma cor que o bloco de coord pos_x,pos_y
    def look_left(self, (pos_x, pos_y)):
	if pos_x == 0 or self.block_matrix[pos_y][pos_x-1].isFalling or self.block_matrix[pos_y][pos_x-1].isClearing: 
	    return False
	else: return self.block_config[pos_y][pos_x] == self.block_config[pos_y][pos_x-1]
	
    # Checa se bloco da esquerda e da mesma cor que o bloco de coord pos_x,pos_y	
    def look_right(self, (pos_x, pos_y)):
	if pos_x == 5 or self.block_matrix[pos_y][pos_x+1].isFalling or self.block_matrix[pos_y][pos_x+1].isClearing:
	    return False
	else: return self.block_config[pos_y][pos_x] == self.block_config[pos_y][pos_x+1]
	
    # Checa se bloco da esquerda e da mesma cor que o bloco de coord pos_x,pos_y	
    def look_up(self, (pos_x, pos_y)):
	if pos_y == 11 or self.block_matrix[pos_y+1][pos_x].isFalling or self.block_matrix[pos_y+1][pos_x].isClearing: 
	    return False
	else: return self.block_config[pos_y][pos_x] == self.block_config[pos_y+1][pos_x]
	
    # Checa se bloco da esquerda e da mesma cor que o bloco de coord pos_x,pos_y	
    def look_down(self, (pos_x, pos_y)):
	if pos_y == 0 or self.block_matrix[pos_y-1][pos_x].isFalling or self.block_matrix[pos_y-1][pos_x].isClearing: 
	    return False
	else: return self.block_config[pos_y][pos_x] == self.block_config[pos_y-1][pos_x]	
	
    # TESTE: Printa matriz de configuracao de blocos
    def print_config_matrix(self):
        for i in range(11, -1, -1):
	    new = []
            for k in range(0, 6):
	        if self.block_config[i][k] == 0	:
		    new.append(" ")
	        elif self.block_config[i][k] == 1:
		    new.append('\033[1;45m'+str(self.block_config[i][k])+'\033[1;m')
	        elif self.block_config[i][k] == 2:
		    new.append('\033[1;46m'+str(self.block_config[i][k])+'\033[1;m')
	        elif self.block_config[i][k] == 3:
		    new.append('\033[1;43m'+str(self.block_config[i][k])+'\033[1;m')
	        elif self.block_config[i][k] == 4:
		    new.append('\033[1;41m'+str(self.block_config[i][k])+'\033[1;m')
	        elif self.block_config[i][k] == 5:
		    new.append('\033[1;42m'+str(self.block_config[i][k])+'\033[1;m')
            print new[0], "", new[1], "", new[2], "", new[3], "", new[4], "", new[5]

    # TESTE: Printa matriz de blocos
    def print_block_matrix(self):
        line = ""
	for i in range(11, -1, -1):
	    line = line + "Linha{0:02d}:".format(i)
	    for k in range(0,6):
	        line = line + " B:{0:2d}  L:{1:2d}  C:{2:2d},".format(self.block_matrix[i][k].block_type, self.block_matrix[i][k].line, self.block_matrix[i][k].col)
	    print line
	    line = ""
	    
    # TESTE: Printa situacao dos blocos (Ativo ou inativo)
    def print_active(self):
        line = ""
	for i in range(11, -1, -1):
	    line = line + "Linha {0:02d}:".format(i)
	    for k in range(0,6):
	        line = line + "{0:10s}".format(str(self.block_matrix[i][k].isActive))
            print line
	    line = ""
        
