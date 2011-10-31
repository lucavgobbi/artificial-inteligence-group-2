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
            for i2 in range(i+3, i+4):
                if(m[l][i2] == v):
                     kill+=1
            break
    if(kill > 0):
        for i in range(0,kill):
            m[l][col+i] = 0    
        #verifica se ainda ha blocos para eliminar
        if(kill + col == 3):
            if(m[l][3] == m[l][4] == m[l][5]):
                m[l][3] = m[l][4] = m[l][5] = 0
                kill+=3
    return kill
        
def analCol(m, c):
    kill = 0
    lin = 0
    for i in range(0,10):
        if(m[i][c] == m[i+1][c] == m[i+2][c]):
            kill = 3
            lin = i
            v = m[i][c]
            for i2 in range(i+3,i+4):
                if(m[i2][c] == v):
                    kill+=1
            break
    if(kill > 0):
        for i in range(0,kill):
            m[lin+i][c] = 0 
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
    while(fall(m) or kill == 0):
        kill += analCols(m) + analLines(m)
    return kill
            
