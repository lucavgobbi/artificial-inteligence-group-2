from validate import *

class Main:
    
    # Inicializa classe main
    def __init__(self):
        i=0
        while(i < 10000):
            m = [[1,1,0,2,2,0],[0,0,1,1,3,2],[0,0,2,3,3,0],[0,0,3,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

            #printMatrix(m)
            analize(m)
            #printMatrix(m)
            i+=1
    
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
    main_window = Main()