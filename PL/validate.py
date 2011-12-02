def fall(m):
    f = False
    for c in range(0,6):
        for l in range(0, 11):
            if(m[l][c] == 0):
                for l1 in range(l+1,12):
                    if(m[l1][c] != 0):
                        m[l1-1][c] = m[l1][c]
                        m[l1][c] = 0
                        f = True
    return f   


def analLine(m, l):
    kill = 0
    col = 0
    for i in range(0,4):
        if(m[l][i] == m[l][i+1] == m[l][i+2] != 0):
            kill = 3
            col = i
            v = m[l][i]
            for i2 in range(i+3, 6):
                if(m[l][i2] == v):
                     kill+=1
                else:
                    break
            break
    if(kill > 0):
        for i in range(0,kill):
            m[l][col+i] = 0    
        #verifica se ainda ha blocos para eliminar
        if(kill + col == 3):
            if(m[l][3] == m[l][4] == m[l][5] != 0):
                m[l][3] = m[l][4] = m[l][5] = 0
                kill+=3
    return kill
        
def analCol(m, c):
    kill = 0
    lin = 0
    for i in range(0,10):
        if(m[i][c] == m[i+1][c] == m[i+2][c] != 0):
            kill = 3
            lin = i
            v = m[i][c]
            m[i][c] = m[i+1][c] = m[i+2][c] = 0
            for i2 in range(i+3,12):
                if(m[i2][c] == v):
                    kill+=1
                    m[i2][c] = 0
            break
    return kill

def analCols(m):
    kill = 0
    for i in range(0,6):
        kill += analCol(m,i)
    return kill

def analLines(m):
    kill = 0
    for i in range(0,12):
        kill += analLine(m,i)
    return kill

def analize(m):
    kill = 0
    killnow = 0
    repeat = True
    while(repeat):
        killnow = analCols(m) + analLines(m)
        if(killnow > 0):
            kill += killnow
            while(fall(m)): pass
        else:
            repeat = False
    return kill

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


            
