from validate import *
from ia import *
import sys
import pygame
import threading

class Main:
    
    # Inicializa classe main
    def __init__(self, mrec):
        m1 = [[1,1,2,1,2,2],[0,0,1,1,3,2],[0,0,2,3,3,0],[0,0,3,3,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        m2 = [[1,1,2,1,2,2],[4,4,3,0,0,0],[0,3,5,0,0,0],[0,4,3,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        m2 = [[0,0,1,2,0,0],[0,0,2,1,0,0],[0,0,1,2,0,0],[0,0,2,1,0,0],[0,0,1,2,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        m3 = [[1,0,1,0,0,1],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        
        m5 = [[1,1,2,1,2,2],[0,0,1,1,3,2],[5,5,2,3,3,5],[0,4,3,3,1,1],[0,4,0,2,0,5],[0,0,0,3,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

        m = mrec
            
        p = analize(m)
        printMatrix(m)
        
        ia = IaThread(m);
        ia.start();
        while ia.isAlive():
            print "run"
         
        
#printMatrix(ia.path[2].m)
        for move in ia.path:
            print move.c, move.r
            printMatrix(move.m)
        #ia = IaThread(ia.path[2].m)
        #ia.start();
            #while ia.isAlive():
    #aux = 1
        
                #for move in ia.path:
                #print move.c, move.r
                #printMatrix(move.m)
#print "$$$$$$$$$$"

def printMoves(m):
    for i in m:
        printMove(i)

def printMove(m):
    print str(m.p) + " - " + str(m.r) + ":" + str(m.c)

def printTree(tree, h):
    print "Altura: " + str(h)
    for move in tree:
        printMove(move)
    for move in tree:
        if(move.child != None):
            print "Filhos de: "
            printMove(move)
            printMatrix(move.m)
            printTree(move.child, h + 1)
        
    
def printMatrix(m):
        for i in range(11, -1, -1):
            new = []
            for k in range(0, 6):
                if m[i][k] == 0:
                    new.append(" ")
                elif m[i][k] == 1:
                    new.append('\033[1;45m'+str(m[i][k])+'\033[1;m')
                elif m[i][k] == 2:
                    new.append('\033[1;46m'+str(m[i][k])+'\033[1;m')
                elif m[i][k] == 3:
                    new.append('\033[1;43m'+str(m[i][k])+'\033[1;m')
                elif m[i][k] == 4:
                    new.append('\033[1;41m'+str(m[i][k])+'\033[1;m')
                elif m[i][k] == 5:
                    new.append('\033[1;42m'+str(m[i][k])+'\033[1;m')
            print new[0], "", new[1], "", new[2], "", new[3], "", new[4], "", new[5]

if __name__ == "__main__":
    # Inicializa objeto main e entra no loop principal
    m = [[1,0,0,1,1,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    
    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
        m = []
        
        for i in range(11, -1, -1):
            line = f.readline().strip(" \n").split()
            number_row = []
            for k in range(0, 6):
                btype = int(line[k])
                number_row.append(btype)
            
            m.insert(0, number_row)
    
    clock = pygame.time.Clock()
    main_window = Main(m)
    print "TEMPO: " + str(clock.tick())