import time

class AI():
    def __init__(self):
        self.color = ""

    def get_move(self,s):
        #time.sleep(10)
        move = False
        for x in range(8):
            for y in range(8):
                try:
                    i = 1
                    while s.board[x-i][y] != self.color and s.board[x-i][y] != '-':
                        i += 1
                    if s.board[x-i][y]  == self.color and i > 1:
                        move=True
                except IndexError:
                    pass

                try:
                    #places tokens below where the one was placed
                    i = 1
                    while s.board[x+i][y] != self.color and s.board[x+i][y] != '-':
                        i += 1
                    if s.board[x+i][y] == self.color and i > 1:
                        move=True
                except IndexError:
                    pass

                try:
                    i = 1
                    while s.board[x][y+i] != self.color and s.board[x][y+i] != '-':
                        i += 1
                    if s.board[x][y+i] == self.color and i > 1:
                        move=True
                except IndexError:
                    pass
                 
                try:
                       
                    i = 1
                    while s.board[x][y-i] != self.color and s.board[x][y-i] != '-':
                        i += 1
                    if s.board[x][y-i] == self.color and i > 1:
                        move=True
                except IndexError:
                    pass

                try:
                    #CHECK DIAGNOALS
                    i = 1
                    while s.board[x-i][y-i] != self.color and s.board[x-i][y-i] != '-':
                        i += 1
                    if s.board[x-i][y-i] == self.color and i > 1:
                        move=True
                except IndexError:
                    pass

                try:
                    i = 1
                    while s.board[x+i][y-i] != self.color and s.board[x+i][y-i] != '-':
                        i += 1
                    if s.board[x+i][y-i] == self.color and i > 1:
                       move=True
                except IndexError:
                    pass

                try:
                    i = 1
                    while s.board[x-i][y+i] != self.color and s.board[x-i][y+i] != '-':
                        i += 1
                    if s.board[x-i][y+i] == self.color and i > 1:
                         move=True
                except IndexError:
                    pass
                
                try:
                    i = 1
                    while s.board[x+i][y+i] != self.color and s.board[x+i][y+i] != '-':
                        i += 1
                    if s.board[x+i][y+i] == self.color and i > 1:
                        move=True
                except IndexError:
                    pass

                if move and s.board[x][y] == '-' :
                    return x,y
                else:
                    move = False
        #no move so return -1
        return -1,-1



