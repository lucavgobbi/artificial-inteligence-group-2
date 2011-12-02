#! /usr/bin/env python

import os, sys
import pygame
import random
from blockbox import Blockbox
from adds import *
from ia import *
from move import *
from vteste import *

class Cpu:
    
    def __init__(self, pos_size, surf):
        
        self.blockbox = Blockbox(pos_size[0], pos_size[1], pos_size[2], pos_size[3], surf)
        
        self.raw_move_queue = []        
        self.t_move_queue = []
        
        self.cursor_final_position = [2,10]
        
        self.move_timer = 10

    def call_ia(self):
        best = IA(self.blockbox.block_config)
        l = []
        
        for m in best:
            l.append([m.c, m.r])
            
        self.raw_move_queue = l
        self.transform_movements()

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
        

    def execute_cpu_movements(self):
        
        if self.t_move_queue == []:
            return
        
        new_move = self.t_move_queue[0][0]
        #print self.t_move_queue[0][0]
        
        
        if new_move[0] == "change":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = 5
            self.blockbox.changing_blocks.append([self.blockbox.cursor.pos_rel_x, self.blockbox.cursor.pos_rel_y])
            self.t_move_queue[0].pop(0)
            
        elif new_move[0] == "left":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = 10
            self.blockbox.cursor.move_cursor_LEFT(self.blockbox.rect)
            new_move[1] += 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
                
        elif new_move[0] == "right":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = 10
            self.blockbox.cursor.move_cursor_RIGHT(self.blockbox.rect)
            new_move[1] -= 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
                
        elif new_move[0] == "up":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = 10
            self.blockbox.cursor.move_cursor_UP(self.blockbox.rect)
            new_move[1] -= 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
                
        elif new_move[0] == "down":
            if self.move_timer > 0:
                self.move_timer -= 1
                return
            self.move_timer = 10
            self.blockbox.cursor.move_cursor_DOWN(self.blockbox.rect)
            new_move[1] += 1
            if new_move[1] == 0:
                self.t_move_queue[0].pop(0)
                
        if self.t_move_queue[0] == []:
            self.t_move_queue.pop(0)