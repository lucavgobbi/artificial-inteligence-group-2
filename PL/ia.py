from validate import *
from vteste import *
from move import *
import copy

#IA Decision
def IA(originalM):
    steps = 3
    tree = buildTree(originalM, steps)
    path = maxPath(tree)
    while(path[0].p > 0):
        for step in path:
            printMove(step)
            printMatrix(step.m)
        tree = buildTree(path[steps-1].m, steps)
        path = maxPath(tree)

#End of IA Decision

#Tree building
def buildMoves(m, hashTabu):
    moves = []
    p = 0
    for r in range (0, 12):
        for c in range(0,5):
            if(m[r][c] != m[r][c+1]):
                mt = copy.deepcopy(m)
                aux = mt[r][c]
                mt[r][c] = mt[r][c+1]
                mt[r][c+1] = aux
                if(checkHash(mt, hashTabu)):
                    p = analize(mt)
                    move = Move(p, r, c, mt)
                    moves.append(move)
    return moves

def buildTree(m, h):
    hashTabu = dict()
    moves = buildMoves(m, hashTabu)
    fillNodes(moves, h-2, hashTabu)
    return moves
    
def fillNodes(moves, h, hashTabu):
        for move in moves:
            move.addChild(buildMoves(move.m, hashTabu))
            if(h > 0):
                fillNodes(move.child, h-1, hashTabu)

#End of Tree building

#Path finding

def maxPath(moves):
    #create a fake root
    move = Move(0,0,0,[])
    move.addChild(moves)
    #search the max
    max = updateMoves(move)
    bestMoves = []
    findMax(move.child, bestMoves)
    return bestMoves
        
def updateMoves(move):
    maxP = 0
    if (move.child == None):
        return move.p
    else:
        for node in move.child:
            maxNode = updateMoves(node)
            if(maxP <= maxNode):
                maxP = maxNode
        move.p += maxP 
        return maxP

def findMax(moves, bestMoves):
    maxMove = Move(0,0,0,[])
    for move in moves:
        if(maxMove.p <= move.p):
            maxMove = move
    bestMoves.append(maxMove)
    if(maxMove.child != None):
        findMax(maxMove.child, bestMoves)

#End of Path finding

#Hashing

def makeImage(m):
    newHash = ""
    value = str(m[0][0])
    valuesToHash = dict()
    valuesToHash[value] = "0"
    newHashValue = 0
    for y in range(0,12):
        for x in range(0,6):
            value = str(m[y][x])
            if(value in valuesToHash):
                newHash += valuesToHash[value]
            else:
                newHashValue += 1
                valuesToHash[value] = str(newHashValue)
                newHash += valuesToHash[value]
    return newHash

def checkHash(m, myhash):
    hashItem = makeImage(m)
    if(hashItem in myhash):
        return False
    else:
        myhash[hashItem] = 0
    return True

#End of Hashing
