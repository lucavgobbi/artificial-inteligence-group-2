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
        
        # Lista contendo blocos mudando de posicao
        self.changing_blocks = []
        
        # Matriz de blocos a serem mostrados na tela
        self.block_matrix = []
        
        # Matriz que representa abstracao da configuracao de blocos atual da tela
        self.block_config = []
        
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
        
        self.block_matrix.append([])
        self.block_config.append([])
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
    def block_change(self, (pos_x, pos_y)):
	
	# referencia para o bloco da esquerda e da direita
	block_left = self.block_matrix[pos_y][pos_x]
	block_right = self.block_matrix[pos_y][pos_x+1]
	
	# referencia para o numero do bloco da esquerda e da direita
	block_number_left = self.block_config[pos_y][pos_x]
	block_number_right = self.block_config[pos_y][pos_x+1]
	
	# Flags que indicam se algum dos blocos esta sendo eliminado, algum esta caindo
        # ou algum dos dois ja esta sendo eliminado
	clearing = block_left.isClearing or block_right.isClearing
	falling = block_left.isFalling or block_right.isFalling
	changing = block_left.isChanging != block_right.isChanging
	
	if clearing or changing or falling:
	    self.changing_blocks.remove((pos_x, pos_y))
	    return
	
	# Se a posicao dos blocos na tela nao tiver sido trocada completamente ainda, movimenta
	# cada bloco a ser trocado um pouco mais e retorna falso
	if self.move_value < 22:
	    #
	    block_left.change_position("right", 11)
	    block_right.change_position("left", 11)
	    self.move_value += 11
	    
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
	        
	    if block_left.block_type != block_right.block_type:
                pair = []
                if block_left.block_type != 0: pair.append((pos_x, pos_y))
                if block_right.block_type != 0: pair.append((pos_x+1, pos_y))
                self.check_clear([(pos_x, pos_y), (pos_x+1, pos_y)])
	    
	    # reseta o valor de movimento
	    self.move_value = 0
	    self.changing_blocks.remove((pos_x, pos_y))
	    
	    return True
    
    # Checa se um bloco deve cair, e se sim, quantas posicoes
    def check_fall(self, (pos_x, pos_y)):
	
	# Se o bloco for ativo, checa se ele proprio deve cair
	if self.block_matrix[pos_y][pos_x].isActive:
	    if pos_y-1 >=0 and (not self.block_matrix[pos_y-1][pos_x].isActive):
                self.falling_blocks.append([[pos_x, pos_y]])
		self.block_matrix[pos_y][pos_x].isFalling = True
	        self.block_matrix[pos_y][pos_x].fall_timer = 15        
	        
	# Se o bloco for inativo, checa se os blocos acima dele devem cair. Se devem, cria uma
	# lista com esses blocos e adiciona na lista de blocos em queda. Essa lista representa
	# um grupo de blocos que deve cair, e o seu timer e o do primeiro bloco da lista
	else:
	    k = pos_y+1
	    if self.block_matrix[k][pos_x].isClearing or self.block_matrix[k][pos_x].isChanging:
		return
	    bl = []
	    while k < 12 and self.block_matrix[k][pos_x].isActive:
		bl.append([pos_x, k])
		self.block_matrix[k][pos_x].isFalling = True
		self.block_matrix[k][pos_x].fall_timer = 15
		k+=1
	    if bl != []: self.falling_blocks.append(bl)
		
	self.changed.remove((pos_x, pos_y))
        return
        
    # Cuida da queda de blocos. Recebe um grupo de blocos que deve cair. A logica e que temos um bloco
    # mestre no grupo, que e o primeiro da lista, ou seja o bloco na linha de menor numero. Ele sempre
    # olha o bloco abaixo de si. Caso ess seja inativo, troca uma posicao para baixo sua e de todos os
    # outros blocos da lista. Caso nao, para de cair
    def block_fall(self, block_set):
	
	pos_x, pos_y = block_set[0]
	# Timer no primeiro elemento do grupo de blocos que deve cair. Assim que zerar, o
	# grupo comeca a cair
	if self.block_matrix[pos_y][pos_x].fall_timer != 0:
	    for block in block_set:
	        self.block_matrix[block[1]][block[0]].fall_timer -= 1
	    return
	
	# Se a posicao do primeiro bloco do grupo de blocos em queda nao for linha 0 e o 
	# bloco abaixo dele for inativo, o grupo cai uma posicao. Essa queda e feita
	# trocando-se o bloco de lugar com o que esta abaixo dele
	
	if pos_y-1 >=0 and (not self.block_matrix[pos_y-1][pos_x].isActive):
	    
	    # Movimenta cada bloco do grupo de blocos que deve cair uma posicao para baixo
	    # trocando ele de lugar com o bloco abaixo dele.
	    for block in block_set:
		pos_x, pos_y = block
		block[1] -= 1
	        
	        # Movimenta o bloco para baixo e o abaixo dele para cima
	        self.block_matrix[pos_y][pos_x].change_position("down", 21)
	        
	        # Troca os valores no bloco. Primeiro da cima depois baixo
	        self.block_matrix[pos_y][pos_x].change_coord("down")
	    	    
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
	    new = pos_y-1
	    if pos_y != 0:
	        for block in block_set:
                    pos_x, pos_y = block
		    self.block_matrix[pos_y][pos_x].fall_timer = self.block_matrix[new][pos_x].fall_timer
		
	    if self.block_matrix[new][pos_x].fall_timer == 0:
		for block in block_set: self.block_matrix[block[1]][block[0]].isFalling = False
		self.check_clear(block_set)
		self.falling_blocks.remove(block_set)	

    def check_clear_teste(self, block_set):
	added_ver = 0
	added_hor = 0
	added = 0
	clear_ver = []
	clear_hor = []
	clear = []
	pos_x, pos_y = block_set[0]
	
	added_ver += self.check_clear_down((pos_x, pos_y), clear_ver)
	added_ver += self.check_clear_up((pos_x, pos_y), clear_ver)
	added_hor += self.check_clear_left((pos_x, pos_y), clear_hor)
	added_hor += self.check_clear_right((pos_x, pos_y), clear_hor)
	if added_ver >= 2:
            clear.extend(clear_ver)
            added += added_ver
        if added_hor >= 2:
            clear.extend(clear_hor)
            added += added_hor
        if clear != []:
            clear.append((pos_x, pos_y))
                  
	for block in block_set[1:]:
            pos_x, pos_y = block
            clear_hor = []
	    added_hor = 0
	    added_hor += self.check_clear_left((pos_x, pos_y), clear_hor)
	    added_hor += self.check_clear_right((pos_x, pos_y), clear_hor)
	    if added_hor >= 2:
                if not (pos_x, pos_y) in clear:
                    clear_hor.append((pos_x, pos_y))
	        clear.extend(clear_hor)
	        added += added_hor
            
        if added >= 2:
            self.cleared_blocks.append(clear)
            
    ## Checa em um determinado grupo de blocos se ha blocos que devem ser eliminados
    ## olhando os vizinhos desses blocos
    # param block_set: grupo de blocos testado
    def check_clear(self, block_set):
        added = 0
        clear = []
                     
        for block in block_set:
            pos_x, pos_y = block
            if self.block_matrix[pos_y][pos_x].isActive:
                clear_ver  = []
                clear_hor = []
                added_ver = 0
                added_hor = 0
            
                added_ver += self.check_clear_down((pos_x, pos_y), clear_ver, clear)
                added_ver += self.check_clear_up((pos_x, pos_y), clear_ver, clear)
                added_hor += self.check_clear_left((pos_x, pos_y), clear_hor, clear)
                added_hor += self.check_clear_right((pos_x, pos_y), clear_hor, clear)
                if added_ver >= 2:
                    added += added_ver + 1
                    clear.extend(clear_ver)
                    if not (pos_x, pos_y) in clear:
                        clear.append((pos_x, pos_y)) 
                
                if added_hor >= 2:
                    added += added_hor + 1
                    clear.extend(clear_hor)
                    if not (pos_x, pos_y) in clear:
                        clear.append((pos_x, pos_y))
                    
        if added >= 3:
            self.cleared_blocks.append(clear)

    ## Auxiliar de eliminacao. Checa se o blocos abaixo de determinando bloco sao iguais a ele
    ## Retorna o numero de blocos adicionados a lista parcial
    # param (pos_x, pos_y): coordenadas do bloco na matriz
    # param clear: lista de eliminacao parcial a que pertencera o bloco
    # param total: lista total de eliminacao gerada ate o momento 
    def check_clear_down(self, (pos_x, pos_y), clear, total):
        
	c = 0
	    
	if self.look_down((pos_x, pos_y)):
	    if (pos_x, pos_y-1) not in total: 
	        clear.append((pos_x, pos_y-1))
	        c += 1
	        
	    if self.look_down((pos_x, pos_y-1)):
                if (pos_x, pos_y-2) not in total:
	            clear.append((pos_x, pos_y-2))
	            c += 1
	return c
	        
    ## Auxiliar de eliminacao. Checa se o blocos acima de determinando bloco sao iguais a ele
    ## Retorna o numero de blocos adicionados a lista parcial
    # param (pos_x, pos_y): coordenadas do bloco testado na matriz
    # param clear: lista de eliminacao parcial a que pertencera o bloco
    # param total: lista total de eliminacao gerada ate o momento 
    def check_clear_up(self, (pos_x, pos_y), clear, total):
	c = 0
	    
	if self.look_up((pos_x, pos_y)):
	    if (pos_x, pos_y+1) not in total: 
	        clear.append((pos_x, pos_y+1))
	        c += 1
	        
	    if self.look_up((pos_x, pos_y+1)):
                if (pos_x, pos_y+2) not in total:
	            clear.append((pos_x, pos_y+2))
	            c += 1
	return c
	
    ## Auxiliar de eliminacao. Checa se o blocos a esquerda de determinando bloco sao iguais a ele
    ## Retorna o numero de blocos adicionados a lista parcial
    # param (pos_x, pos_y): coordenadas do bloco testado na matriz
    # param clear: lista de eliminacao parcial a que pertencera o bloco
    # param total: lista total de eliminacao gerada ate o momento 
    def check_clear_left(self, (pos_x, pos_y), clear, total):
	c = 0
	    
	if self.look_left((pos_x, pos_y)):
	    if (pos_x-1, pos_y) not in total: 
	        clear.append((pos_x-1, pos_y))
	        c += 1
	        
	    if self.look_left((pos_x-1, pos_y)):
                if (pos_x-2, pos_y) not in total:
	            clear.append((pos_x-2, pos_y))
	            c += 1
	return c
	
    ## Auxiliar de eliminacao. Checa se o blocos a direita de determinando bloco sao iguais a ele
    ## Retorna o numero de blocos adicionados a lista parcial
    # param (pos_x, pos_y): coordenadas do bloco testado na matriz
    # param clear: lista de eliminacao parcial a que pertencera o bloco
    # param total: lista total de eliminacao gerada ate o momento 
    def check_clear_right(self, (pos_x, pos_y), clear, total):
	c = 0
	    
	if self.look_right((pos_x, pos_y)):
	    if (pos_x+1, pos_y) not in total: 
	        clear.append((pos_x+1, pos_y))
	        c += 1
	        
	    if self.look_right((pos_x+1, pos_y)):
                if (pos_x+2, pos_y) not in total:
	            clear.append((pos_x+2, pos_y))
	            c += 1
	return c


    ## Elimina os blocos da tela. Responsavel pela animacao de eliminacao, remocao do bloco da tela
    ## e limpeza de seus atributos.
    # param block_set: conjunto de blocos que deve ser eliminado simultaneamente
    def block_clear(self, block_set):
	pos_x, pos_y = block_set[0]
	
	if not self.block_matrix[pos_y][pos_x].isClearing:
	    for block in block_set:
		pos_x, pos_y = block
	        self.block_matrix[pos_y][pos_x].isClearing = True
	        self.block_matrix[pos_y][pos_x].blinking = 45
	        self.block_matrix[pos_y][pos_x].block_blinking()
	    return
        for block in block_set:
	    pos_x, pos_y = block
	    self.block_matrix[pos_y][pos_x].block_blinking()
	    
	if self.block_matrix[pos_y][pos_x].blinking == 0:
	    aux = []
	    for block in block_set:
		pos_x, pos_y = block
		self.changed.append(block)
		self.block_matrix[pos_y][pos_x].clear()
		self.block_config[pos_y][pos_x] = 0
		Blockbox.block_group.remove(self.block_matrix[pos_y][pos_x])
	    #print "BLOCK_SET\n\n", block_set, "\n\nBLOCK_SET"
	    #print len(block_set)
	    self.cleared_blocks.remove(block_set)
	    return
	
	        	
    ## Checa se bloco da esquerda e da mesma cor que o bloco dado
    # param (pos_x, pos_y): coordenadas do bloco testado na matriz
    def look_left(self, (pos_x, pos_y)):
	if pos_x == 0 or self.block_matrix[pos_y][pos_x-1].isFalling or self.block_matrix[pos_y][pos_x-1].isClearing: 
	    return False
	else: return self.block_config[pos_y][pos_x] == self.block_config[pos_y][pos_x-1]
	
    ## Checa se bloco da esquerda e da mesma cor que o bloco dado
    # param (pos_x, pos_y): coordenadas do bloco testado na matriz
    def look_right(self, (pos_x, pos_y)):
	if pos_x == 5 or self.block_matrix[pos_y][pos_x+1].isFalling or self.block_matrix[pos_y][pos_x+1].isClearing:
	    return False
	else: return self.block_config[pos_y][pos_x] == self.block_config[pos_y][pos_x+1]
	
    ## Checa se bloco da esquerda e da mesma cor que o bloco dado
    # param (pos_x, pos_y): coordenadas do bloco testado na matriz
    def look_up(self, (pos_x, pos_y)):
	if pos_y == 11 or self.block_matrix[pos_y+1][pos_x].isFalling or self.block_matrix[pos_y+1][pos_x].isClearing: 
	    return False
	else: return self.block_config[pos_y][pos_x] == self.block_config[pos_y+1][pos_x]
	
    ## Checa se bloco da esquerda e da mesma cor que o bloco dado
    # param (pos_x, pos_y): coordenadas do bloco testado na matriz
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
	    
    # TESTE: Inicia os blocos a partir de uma matriz de configuracao definida em um arquivo. 'name' e
    # o nome do arquivo
    def file_initiate_blocks(self, name):
        f = open(name, 'r')
        
        for i in range(11, -1, -1):
            line = f.readline().strip(" \n").split()
            block_row = []
            number_row = []
            for k in range(0, 6):
                btype = int(line[k])
                
                b = Block((self.rect.left, self.rect.top, k, i), 22, 21, btype)
                if btype != 0: Blockbox.block_group.add(b)
            
                block_row.append(b)
                number_row.append(btype)
            
            self.block_matrix.insert(0, block_row)
            self.block_config.insert(0, number_row)
