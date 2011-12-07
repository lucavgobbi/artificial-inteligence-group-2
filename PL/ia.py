from validate import *
from move import *
import random
import copy
import threading

#Variavel para controlar se a thread deve morrer
die = False

def kill_thread():
    die = True

#classe que herda de thread, metodo init para instanciar as variaveis e metodo run sobrescrevendo o run da thread
class IaThread (threading.Thread):
    def __init__ (self, m, knowMoves):
        self.matrix = m
        self.knowMoves = knowMoves
        threading.Thread.__init__ (self)
        die = False
        
    def run (self):
        print "New IA Thread"
        steps = defineHeight(self.matrix) #define a profundidade da execucao
        print "Altura: " + str(steps)
        matrixImage = makeImage(self.matrix) #cria uma imagem homogenea da matriz
        self.path = []
        if(matrixImage in self.knowMoves): #verifica se a matriz homogenea ja eh um knowmove
            self.path = self.knowMoves[matrixImage]
        else:
            tree = buildTree(self.matrix, steps) #senao constroi a arvore de decisao
            self.path = maxPath(tree) #e busca melhor caminho dentro dela
            for move in self.path: #caso encontre algum caminho que pontua, armazena a matriz em knowmove
                if move.p > 0:
                    print printMove(move)
                    self.knowMoves[matrixImage] = newKnowMove(self.path)
                else: #senao retorna lista vazia
                    print "No move"
                    self.path = [];
                    return


#Tree building

#Constroi e retorna a lista de movimentos para o estado M (M deve ser valido), utilizando o hashTabu
def buildMoves(m, hashTabu):
    moves = []
    p = 0
    for r in range (0, 12):
        for c in range(0,5):
            if(m[r][c] != m[r][c+1]): #calcula todos os movimentos possiveis, descartando os movimentos de pecas iguais
                mt = copy.deepcopy(m) #como python usa ponteiros, faz uma copia da matriz para permutar
                aux = mt[r][c]
                mt[r][c] = mt[r][c+1]
                mt[r][c+1] = aux
                if(checkHash(mt, hashTabu)): # se estado nunca explorado
                    if die: return [] #utilizado para parar execucao da thread
                    p = analize(mt) #analiza o novo estado e ve quantos blocos eliminaa
                    move = Move(p, r, c, mt) #cria o novo movimento e aciona na lista, o movimento contem a matriz final
                    moves.append(move)
    return moves

#controi arvor a partir da matriz valida M e com altura h
#obs: funcao utilizada para manter o padrao da arvore utilizando a estrutura escolhida
def buildTree(m, h):
    hashTabu = dict()
    moves = buildMoves(m, hashTabu) #cria lista de movimentos
    fillNodes(moves, h-2, hashTabu) # preenche os nos a partir
    return moves

#preencher os nos recusivamente
def fillNodes(moves, h, hashTabu):
    for move in moves: #para cada movimento na lista de movimentos chama buildMoves para a matriz do moviemtnos
            move.addChild(buildMoves(move.m, hashTabu))
        if die: return #utilizado para parar a execucao da thread
            if(h > 0): #se ainda deve recursar, recusrsa
                fillNodes(move.child, h-1, hashTabu)

#End of Tree building

#Heuristics

#estima a altura baseado no numero de blocos no estado (nao utilizada)
def estimateHeight(m):
    n = 0;
    for r in range(0,12):
        for c in range(0,6):
            if(m[r][c] != 0):
                n+=1
    if (n > 20):
        return 3
    if (n > 12):
        return 4
    if (n > 8):
        return 5
    return 6

#define altura do algoritimo baseado na altura que os blocos estao atingindo
def defineHeight(m):
    for r in range(7,12):
        for c in range(0,6):
            if(m[r][c] != 0): # se existe bloco acima da linha 7 forca altura 1
                return 1
    return 3
#End of Heuristics

#Path finding

#busca o maior caminho dentro de uma lista de movimentos
def maxPath(moves):
    #create a fake root
    move = Move(0,0,0,[])
    move.addChild(moves)
    #search the max
    max = updateMoves(move) #atualiza os valores totais que aquele no pode levar
    bestMoves = []
    findMax(move.child, bestMoves) #busca o melhor caminho dado os nos atualizados
    return bestMoves
        
#atualiza o valor dos nos gravando o valor do melhor filho no noh pai
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

#busca o caminho que da mais pontos, sempre retorna um caminho da raiz ate a folha
def findMax(moves, bestMoves):
    maxMove = Move(0,0,0,[])
    for move in moves:
        if(maxMove.p <= move.p): #acha o melhor movimento
            maxMove = move
bestMoves.append(maxMove) #adiciona na lista
    if(maxMove.child != None): #recursa nos filhos
        findMax(maxMove.child, bestMoves)

#End of Path finding

#Hashing

#monta o caminho utilizando o minimo de informacoes possives
def newKnowMove(path):
    newpath = []
    for move in path:
        newpath.append(Move(move.p, move.r, move.c, [])) #exclui a matriz que ocupa espaco e so e necessaria no ultimo movimento
    newpath[-1].m = path[-1].m
    return newpath

#homogeniza a matriz e lineariza
def makeImage(m):
    newHash = ""
    value = str(m[0][0])
    valuesToHash = dict() #armazena a conversao de cada numero da matriz original
    valuesToHash[value] = "0"
    newHashValue = 0
    for y in range(0,12):
        for x in range(0,6):
            value = str(m[y][x]) #converte o valor baseado nas conversoes ja criadas ou cria e armazena novas conversoes
            if(value in valuesToHash):
                newHash += valuesToHash[value]
            else:
                newHashValue += 1
                valuesToHash[value] = str(newHashValue)
                newHash += valuesToHash[value]
    return newHash

#verifica no hash se o estado deve ser explorado, se sim, retorna True
def checkHash(m, myhash):
    hashItem = makeImage(m)
    if(hashItem in myhash):
        return False
    else:
        myhash[hashItem] = 0
    return True

#End of Hashing

#Debbuging

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

def printMoves(m):
    for i in m:
        printMove(i)

def printMove(m):
    print str(m.p) + " - " + str(m.r) + ":" + str(m.c)