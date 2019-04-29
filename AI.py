import copy

class AI():
    def __init__(self):
        self.color = ""
        self.depth = 0
        self.depth_look = 4
        self.dummy_board = []
        self.dummy_p_score = 0
        self.dummy_AI_score = 0

        self.state_num_to_list = {}

        #states layout : [x_cord, y_cord, num_tokens_turned_over, depth, parent]
        self.states = {}
        

    def get_move(self,s):
        self.dummy_p_score = s.p_score
        self.dummy_AI_score = s.a_score
        self.dummy_board = copy.deepcopy(s.board)

        possible_moves = self.get_eligable_moves(self.color)

        if self.color == 'B':
            p_color = 'W'
        else:
            p_color = 'B'
        #GEN TREE
        self.generate_tree(possible_moves)

        #TODO
        #self.prune_the_tree()

        #self.return_best_move()

    def generate_tree(self, possible_moves):
       i = 0

       self.state_num_to_list[i] = copy.deepcopy(self.dummy_board)
       self.states[i] = possible_moves

       if self.color == 'B':
            p_color = 'W'
            color_not_move = 'B'
       else:
            p_color = 'B'
            color_not_move = 'W'

       color_to_move = p_color

       parent = 0
  
       while self.states[parent][0][3] < self.depth_look:
            if self.states[parent][0][3] % 2 == 0:
                color_not_move = 'B'
                color_to_move = 'W'
            else:
                color_not_move = 'W'
                color_to_move = 'B'

            if color_to_move != p_color:
                negate = False
            else:
                negate = True



            #GENERATE TREE
            self.depth = self.states[parent][0][3] + 1
            for move in possible_moves:
                i += 1
                #change board so that it looks like the current board in the system

                self.dummy_change_board(move[0],move[1], color_not_move)

                #keep track of them the same way we did in the A/B pruning homework, with a ditionary
                self.state_num_to_list[i] = copy.deepcopy(self.dummy_board)
                
                #self.states[i] = self.get_eligable_moves(p_color)
                move_holder = self.get_eligable_moves(color_to_move)
                for row in move_holder:
                    #check it it needs to be negated
                    if negate:
                        row[2] = -(row[2])

                    #add parent
                    row.append(parent)
                self.states[i] = move_holder
                
                self.dummy_board = copy.deepcopy(self.state_num_to_list[parent])

            self.dummy_board = copy.deepcopy(self.state_num_to_list[parent + 1])
            possible_moves = self.states[parent+1]


            parent = parent + 1
            
            for key, val in self.state_num_to_list.items():
                print(key, "=>")
                for item in val:
                    print(item)

            for key, val in self.states.items():
                print(key, "=>")
                for item in val:
                    print(item)


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
        try:
            while self.dummy_board[x-i][y] == oppositeColor:
                tempList.append([x-i,y])
                i += 1
            if self.dummy_board[x-i][y] == color:
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.dummy_board[newX][newY] = color
                    changeColorList.append(pair)
        except IndexError:
            pass

        #places tokens below where the one was placed
        i = 1
        tempList = []
        try:
            while self.dummy_board[x+i][y] == oppositeColor:
                tempList.append([x+i,y])
                i += 1
            if self.dummy_board[x+i][y] == color:
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.dummy_board[newX][newY] = color

                    changeColorList.append(pair)
        except IndexError:
            pass

        try:
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
        except IndexError:
            pass


        try:    
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
        except IndexError:
            pass

        try:
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
        except IndexError:
            pass


        try:
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
        except IndexError:
            pass

        try:
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
        except IndexError:
            pass

        try:
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
        except IndexError:
            pass

        for pair in changeColorList:
            if color == self.color:
                self.dummy_AI_score += 1
                self.dummy_p_score -= 1
            else:
                self.dummy_AI_score -= 1
                self.dummy_p_score += 1
 

