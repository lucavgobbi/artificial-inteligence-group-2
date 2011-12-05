#! /usr/bin/env python

import os, sys
import pygame
import random
from blockbox import Blockbox
from adds import *
from ia import *
from move import *
import threading
import copy
from pprint import pprint
import cPickle

class Cpu:
    
    def __init__(self, pos_size, surf):
        
        self.blockbox = Blockbox(pos_size[0], pos_size[1], pos_size[2], pos_size[3], surf, True)
        
        self.raw_move_queue = []        
        self.t_move_queue = []
        
        self.cursor_final_position = [2,10]
        
        self.max_move_timer = 5
        self.move_timer = self.max_move_timer
        
        self.ia = None
        
        self.stop_ia = False
        
        self.last_m = []
        
        self.need_line = False
        
        if(os.path.isfile("know.moves")):
            f = open("know.moves", 'r')
            self.knowMoves = cPickle.load(f)
        else:
            self.knowMoves = dict()

#forca uma nova linha a surgir
    def rise_line(self):
        self.blockbox.block_group.update(3)
        self.blockbox.cursor_group.update(3)
        self.blockbox.update_counter += 1

        if self.blockbox.update_counter == 7:
            self.blockbox.update_counter = 0
            self.need_line = False
            self.cursor_final_position[1] += 1
            self.blockbox.update_blocks()
            self.init_ia()
            
#self.init_ia()
      
#salva o arquivo de KnowMoves
    def saveKnowMoves(self):
        f = open('know.moves', 'w')
        cPickle.dump(self.knowMoves, f)
        f.close()

#chama ia sem thread
    def call_ia(self):
        tree = buildTree(self.last_m, 3)
        best = maxPath(tree)
        l = []
        print best
        
        for m in best:
            l.append([m.c, m.r])
            
        print "$$$$$$$$$$$$$$$$$$$$"
        printMatrix(best[-1].m)
        print "$$$$$$$$$$$$$$$$$$$$"
        self.last_m = copy.deepcopy(best[-1].m)
        self.raw_move_queue.append(l)
        self.transform_movements()

#inicia a ia com thread
    def init_ia(self):
        printMatrix(self.blockbox.block_config)
        self.ia = IaThread(self.blockbox.block_config, self.knowMoves)
        self.ia.start()
        self.raw_move_queue = []        
        self.t_move_queue = []
        self.stop_ia = False

#looping da ia com thread
    def call_ia2(self):
        l = []
        
        if self.ia.isAlive() or self.stop_ia:
            return
        else:
            if len(self.ia.path) > 0:
                for move in self.ia.path:
                    l.append([move.c, move.r])
                    #print move.c, move.r
                
                end_matrix = copy.deepcopy(self.ia.path[-1].m)
                if end_matrix != []:
                    #print "$$$$$$$$$$$$$$$$$$$$"
                    #printMatrix(end_matrix)
                    #print "$$$$$$$$$$$$$$$$$$$$"
                    self.ia = None
                    self.ia = IaThread(end_matrix, self.knowMoves)
                    self.ia.start()
                else:
                    self.stop_ia = True
                    self.need_line = True
                self.raw_move_queue.append(l)
                self.transform_movements()
            else:
                self.stop_ia = True;
                self.need_line = True
            #self.stop_ia = True

#gera movimentos aleatorios
    def gen_random_movements(self):
        
        if len(self.t_move_queue) < 8:
        
            if self.blockbox.fail: return
            number = random.randint(3, 6)
            moves = []
        
            for i in range(0, number):
                
                x = random.randint(0, 5)
                y = random.randint(0, 11)
                
                try: 
                    if self.blockbox.block_config[y][x] != 0:
                        moves.append([x,y])
                except IndexError:
                    print "X Y"
                    print y, x
                    print "CONFIGURACAO"
                    print self.blockbox.block_config
                    print "BLOCOS"
                    self.blockbox.print_block_matrix()
                    break
            
            if moves != []: self.raw_move_queue.append(moves)

    def transform_movements(self):
        moves_to_transform = self.raw_move_queue.pop(0)
        size = len(moves_to_transform)
        move_list = []
        
        move = moves_to_transform[0]
        
        pos_x, pos_y = self.cursor_final_position
        
        hor = move[0] - pos_x
        ver = move[1] - pos_y
        
        if hor > 0:
            new_move = ["right", hor]
            move_list.append(new_move)
        elif hor < 0:
            new_move = ["left", hor]
            move_list.append(new_move)
        
        
        if ver > 0:
            new_move = ["up", ver]
            move_list.append(new_move)
        elif ver < 0:
            new_move = ["down", ver]
            move_list.append(new_move)
        
        move_list.append(["change"])


        for i in range(0, size-1):
            move = moves_to_transform[i]
            next_move = moves_to_transform[i+1]
            
            hor = next_move[0] - move[0]
            ver = next_move[1] - move[1]
            
            if hor > 0:
                new_move = ["right", hor]
                move_list.append(new_move)
            elif hor < 0:
                new_move = ["left", hor]
                move_list.append(new_move)
        
            if ver > 0:
                new_move = ["up", ver]
                move_list.append(new_move)
            elif ver < 0:
                new_move = ["down", ver]
                move_list.append(new_move)
                
            move_list.append(["change"])
        
        self.t_move_queue.append(move_list)
        self.cursor_final_position = moves_to_transform[-1]
        
#executa os movimentos que estao na fila
    def execute_cpu_movements(self):
        
        if self.t_move_queue == []:
            return
        
        new_move = self.t_move_queue[0][0]
        #print self.t_move_queue[0][0]
        
        
        if new_move[0] == "change":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            if self.blockbox.cleared_blocks != [] or self.blockbox.falling_blocks != []:
                self.move_timer += 4
                return
            self.move_timer = self.max_move_timer
            self.blockbox.changing_blocks.append([self.blockbox.cursor.pos_rel_x, self.blockbox.cursor.pos_rel_y])
            self.t_move_queue[0].pop(0)
            #print [self.blockbox.cursor.pos_rel_x, self.blockbox.cursor.pos_rel_y]
            
        elif new_move[0] == "left":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = self.max_move_timer
            self.blockbox.cursor.move_cursor_LEFT(self.blockbox.rect)
            new_move[1] += 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
                
        elif new_move[0] == "right":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = self.max_move_timer
            self.blockbox.cursor.move_cursor_RIGHT(self.blockbox.rect)
            new_move[1] -= 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
                
        elif new_move[0] == "up":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = self.max_move_timer
            self.blockbox.cursor.move_cursor_UP(self.blockbox.rect)
            new_move[1] -= 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
                
        elif new_move[0] == "down":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = self.max_move_timer
            self.blockbox.cursor.move_cursor_DOWN(self.blockbox.rect)
            new_move[1] += 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
        elif new_move[0] > 0:
            new_move[0] -= 1
        else: self.t_move_queue[0].pop(0)
        
        if self.t_move_queue[0] == []:
            self.t_move_queue.pop(0)