class Move():
    
    def __init__(self, point, row, col, matrix):
        self.p = point
        self.r = row
        self.c = col
        self.m = matrix
        self.child = None

    def addChild(self, child):
        self.child = child