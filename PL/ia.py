from validate import *
from vteste import *
from move import *
import copy

#Tree building
def buildMoves(m):
    moves = []
    p = 0
    for r in range (0, 12):
        for c in range(0,5):
            if(m[r][c] != m[r][c+1]):
                mt = copy.deepcopy(m)
                aux = mt[r][c]
                mt[r][c] = mt[r][c+1]
                mt[r][c+1] = aux
                p = analize(mt)
                move = Move(p, r, c, mt)
                moves.append(move)
    return moves

def buildTree(m):
    moves = buildMoves(m)
    fillNodes(moves, 1)
    return moves
    
def fillNodes(moves, h):
        for move in moves:
            move.addChild(buildMoves(move.m))
            if(h > 0):
                fillNodes(move.child, h-1)

#End of Tree building

#Path finding

def maxPath(moves):
    #create a fake root
    move = Move(0,0,0,[])
    move.addChild(moves)
    #search the max
    list = []
    max = findMax(move)
    print list
    print max
        
def findMax(move):
    maxP = 0
    if (move.child == None):
        return move.p
    else:
        for node in move.child:
            maxNode = findMax(node)
            if(maxP <= maxNode):
                maxP = maxNode
        return maxP + move.p

            