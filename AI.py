import time

class AI():
    def __init__(self):
        self.color = ""

    def get_move(self,s):
        #time.sleep(10)
        move = False
        moveNumber = -1
        for x in range(8):
            for y in range(8):
                try:
                    i = 1
                    while s.board[x-i][y] != self.color and s.board[x-i][y] != '-':
                        i += 1
                    if s.board[x-i][y]  == self.color and i > 1:
                        move=True
                        moveNumber = 0
                        i0 = i
                except IndexError:
                    pass

                try:
                    #places tokens below where the one was placed
                    i = 1
                    while s.board[x+i][y] != self.color and s.board[x+i][y] != '-':
                        i += 1
                    if s.board[x+i][y] == self.color and i > 1:
                        move=True
                        moveNumber = 1
                        i1 = i
                except IndexError:
                    pass

                try:
                    i = 1
                    while s.board[x][y+i] != self.color and s.board[x][y+i] != '-':
                        i += 1
                    if s.board[x][y+i] == self.color and i > 1:
                        move=True
                        moveNumber = 2
                        i2 = i
                except IndexError:
                    pass
                 
                try:
                       
                    i = 1
                    while s.board[x][y-i] != self.color and s.board[x][y-i] != '-':
                        i += 1
                    if s.board[x][y-i] == self.color and i > 1:
                        move=True
                        moveNumber = 3
                        i3 = i
                except IndexError:
                    pass

                try:
                    #CHECK DIAGNOALS
                    i = 1
                    while s.board[x-i][y-i] != self.color and s.board[x-i][y-i] != '-':
                        i += 1
                    if s.board[x-i][y-i] == self.color and i > 1:
                        move=True
                        moveNumber = 4
                        i4 = i
                except IndexError:
                    pass

                try:
                    i = 1
                    while s.board[x+i][y-i] != self.color and s.board[x+i][y-i] != '-':
                        i += 1
                    if s.board[x+i][y-i] == self.color and i > 1:
                       move=True
                       moveNumber = 5
                       i5 = i
                except IndexError:
                    pass

                try:
                    i = 1
                    while s.board[x-i][y+i] != self.color and s.board[x-i][y+i] != '-':
                        i += 1
                    if s.board[x-i][y+i] == self.color and i > 1:
                         move=True
                         moveNumber = 6
                         i6 = i
                except IndexError:
                    pass
                
                try:
                    i = 1
                    while s.board[x+i][y+i] != self.color and s.board[x+i][y+i] != '-':
                        i += 1
                    if s.board[x+i][y+i] == self.color and i > 1:
                        move=True
                        moveNumber = 7
                        i7 = i
                except IndexError:
                    pass

                if move and s.board[x][y] == '-' :
                    '''
                    if moveNumber == 0:
                        s.board[x-i0][y] = '$'
                    elif moveNumber == 1:
                        s.board[x+i1][y] = '$'
                    elif moveNumber == 2:
                        s.board[x][y+i2] = '$'
                    elif moveNumber == 3:
                        s.board[x][y-i3] = '$'
                    elif moveNumber == 4:
                        s.board[x-i4][y-i4] = '$'
                    elif moveNumber == 5:
                        s.board[x+i5][y-i5] = '$'
                    elif moveNumber == 6:
                        s.board[x-i6][y+i6] = '$'
                    else:
                        s.board[x+i7][x+i7] = '$'
                    '''

                    return x,y
                else:
                    move = False
        #no move so return -1
        return -1,-1



