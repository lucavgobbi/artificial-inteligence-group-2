from validate import *
from vteste import *
import copy

def ia(m):
    print "Matriz Original"
    for r in range (0, 12):
        for c in range(0,5):
            if(m[r][c] != m[r][c+1]):
                mt = copy.deepcopy(m)
                aux = mt[r][c]
                mt[r][c] = mt[r][c+1]
                mt[r][c+1] = aux
                print "Matriz Modificada"
                printMatrix(mt)
                print "Matriz Analizada"
                p = analize(mt)
                printMatrix(mt)
                print " ------------- " 
                