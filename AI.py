import copy

class AI():
    def __init__(self):
        self.color = ""
        self.depth = 0
        self.dummy_board = []
        self.dummy_p_score = 0
        self.dummy_AI_score = 0

        self.state_num_to_list = {}
        self.states = {}

    def get_move(self,s):
        self.dummy_p_score = s.p_score
        self.dummy_AI_score = s.a_score
        self.dummy_board = copy.deepcopy(s.board)

        possible_moves = self.get_eligable_moves(self.color)
        i = 0

        self.state_num_to_list[i] = copy.deepcopy(self.dummy_board)
        self.states[i] = possible_moves

        if self.color == 'B':
            p_color = 'W'
        else:
            p_color = 'B'

        #GENERATE TREE
        self.depth += 1
        for move in possible_moves:
            i += 1
            #change board so that it looks like the current board in the system
            self.dummy_change_board(move[0],move[1],self.color)


            #keep track of them the same way we did in the A/B pruning homework, with a ditionary
            self.state_num_to_list[i] = copy.deepcopy(self.dummy_board)
            self.states[i] = self.get_eligable_moves(p_color)
            
            self.dummy_board = copy.deepcopy(self.state_num_to_list[0])


        for key, val in self.state_num_to_list.items():
            print(key, "=>")
            for item in val:
                print(item)

        for key, val in self.states.items():
            print(key, "=>")
            for item in val:
                print(item)

        return possible_moves[0][0], possible_moves[0][1]


    def maxVal(graph,node,alpha,beta):
        print node
        if isinstance(node,int):
            return node
        v = float("-inf")
        for child in graph.get(node):
            v1 = minVal(graph,child,alpha,beta)
            if v is None or v1 > v:
                v = v1
            if beta is not None:
                if v1 >= beta:
                    return v
            if alpha is None or v1 > alpha:
                alpha = v1
        return v

    def minVal(graph,node,alpha,beta):
        print node
        if isinstance(node,int):
            return node
        v = float("inf")
        for child in graph.get(node):
            v1 = maxVal(graph,child,alpha,beta)
            if v is None or v1 < v:
                v = v1
            if alpha is not None:
                if v1 <= alpha:
                    return v
            if beta is None or v1 < beta:
                beta = v1
        return v

    def get_eligable_moves(self, color):
        move = False
        eligable_moves = []

        for x in range(8):
            for y in range(8):
                total = 0
                try:
                    i = 1
                    while self.dummy_board[x-i][y] != color and self.dummy_board[x-i][y] != '-':
                        i += 1
                    if self.dummy_board[x-i][y]  == color and i > 1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass


                try:
                    #places tokens below where the one was placed
                    i = 1
                    while self.dummy_board[x+i][y] != color and self.dummy_board[x+i][y] != '-':
                        i += 1
                    if self.dummy_board[x+i][y] == color and i > 1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass
                
                try:
                    i = 1
                    while self.dummy_board[x][y+i] != color and self.dummy_board[x][y+i] != '-':
                        i += 1
                    if self.dummy_board[x][y+i] == color and i > 1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass
                

                try:
                       
                    i = 1
                    while self.dummy_board[x][y-i] != color and self.dummy_board[x][y-i] != '-':
                        i += 1
                    if self.dummy_board[x][y-i] == color and i > 1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass


                try:
                    #CHECK DIAGNOALS
                    i = 1
                    while self.dummy_board[x-i][y-i] != color and self.dummy_board[x-i][y-i] != '-':
                        i += 1
                    if self.dummy_board[x-i][y-i] == color and i > 1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass
                
                
                try:
                    i = 1
                    while self.dummy_board[x+i][y-i] != color and self.dummy_board[x+i][y-i] != '-':
                        i += 1
                    if self.dummy_board[x+i][y-i] == color and i > 1:
                       move=True
                       total += i - 1
                except IndexError:
                    pass


                try:
                    i = 1
                    while self.dummy_board[x-i][y+i] != color and self.dummy_board[x-i][y+i] != '-':
                        i += 1
                    if self.dummy_board[x-i][y+i] == color and i > 1:
                         move=True
                         total += i - 1
                except IndexError:
                    pass
                

                try:
                    i = 1
                    while self.dummy_board[x+i][y+i] != color and self.dummy_board[x+i][y+i] != '-':
                        i += 1
                    if self.dummy_board[x+i][y+i] == color and i > 1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass


                if move and self.dummy_board[x][y] == '-' :
                    #each eligable move will get here
                    #append the total amount that they change
                    eligable_moves.append([x,y, total , self.depth])
                    
                    move = False
                else:
                    move = False
        return eligable_moves


    def dummy_change_board(self, x, y , color):
        # for each square around it, check and see if it starts with the opposite
        # color and then ends with the true color
        if color == 'B':
            oppositeColor = 'W'
        else:
            oppositeColor = 'B'

        self.dummy_board[x][y] = color
        if color == self.color:
            self.dummy_AI_score += 1
        else:
            self.dummy_p_score += 1

        #check all 4 moves around it
        changeColorList = []
        
        #Changes tokens above where the one was placed
        i = 1
        tempList = []
        while self.dummy_board[x-i][y] == oppositeColor:
            tempList.append([x-i,y])
            i += 1
        if self.dummy_board[x-i][y] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color
                changeColorList.append(pair)

        #places tokens below where the one was placed
        i = 1
        tempList = []
        while self.dummy_board[x+i][y] == oppositeColor:
            tempList.append([x+i,y])
            i += 1
        if self.dummy_board[x+i][y] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color

                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.dummy_board[x][y+i] == oppositeColor:
            tempList.append([x,y+i])
            i += 1
        if self.dummy_board[x][y+i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color

                changeColorList.append(pair)
            
        i = 1
        tempList = []
        while self.dummy_board[x][y-i] == oppositeColor:
            tempList.append([x,y-i])
            i += 1
        if self.dummy_board[x][y-i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color
                changeColorList.append(pair)

        #CHECK DIAGNOALS
        i = 1
        tempList = []
        while self.dummy_board[x-i][y-i] == oppositeColor:
            tempList.append([x-i,y-i])
            i += 1
        if self.dummy_board[x-i][y-i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color
                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.dummy_board[x+i][y-i] == oppositeColor:
            tempList.append([x+i,y-i])
            i += 1
        if self.dummy_board[x+i][y-i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color
                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.dummy_board[x-i][y+i] == oppositeColor:
            tempList.append([x-i,y+i])
            i += 1
        if self.dummy_board[x-i][y+i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color
                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.dummy_board[x+i][y+i] == oppositeColor:
            tempList.append([x+i,y+i])
            i += 1
        if self.dummy_board[x+i][y+i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.dummy_board[newX][newY] = color
                changeColorList.append(pair)

        for pair in changeColorList:
            if color == self.color:
                self.dummy_AI_score += 1
                self.dummy_p_score -= 1
            else:
                self.dummy_AI_score -= 1
                self.dummy_p_score += 1
 

