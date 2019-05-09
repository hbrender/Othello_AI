import copy

class AI():
    def __init__(self):
        self.color = ""
        self.depth = 0
        self.depth_look = 2
        self.dummy_board = []
        self.dummy_p_score = 0
        self.dummy_AI_score = 0
        self.weights = [[ 4,-3, 2, 2, 2, 2,-3, 4],
                        [-3,-4,-1,-1,-1,-1,-4,-3],
                        [ 2,-1, 1, 0, 0, 1,-1, 2],
                        [ 2,-1, 0, 1, 1, 0,-1, 2],
                        [ 2,-1, 0, 1, 1, 0,-1, 2],
                        [ 2,-1, 1, 0, 0, 1,-1, 2],
                        [-3,-4,-1,-1,-1,-1,-4,-3],
                        [ 4,-3, 2, 2, 2, 2,-3, 4]]

        self.state_num_to_list = {}

        #states layout : [x_cord, y_cord, num_tokens_turned_over + weigths, depth, parent, state_num]
        self.states = {}
        

    def get_move(self,s):
        self.dummy_p_score = s.p_score
        self.dummy_AI_score = s.a_score
        self.dummy_board = copy.deepcopy(s.board)
        
        print(self.color)
        possible_moves = self.get_eligable_moves(self.color)
        print(possible_moves)
        
        if possible_moves == []:
            return -1,-1

        if self.color == 'B':
            p_color = 'W'
        else:
            p_color = 'B'
        #GEN TREE
        self.generate_tree(possible_moves)

        #self.prune_the_tree()

        x,y = self.return_best_move(possible_moves)
        return x,y
        
    def return_best_move(self, possible_moves):
        total_values = [item[2] for item in self.states[0]]

        for val in range(len(self.states[0])):
            min_choice = min([choice[2] for choice in self.states[self.states[0][val][5]]])
            total_values[val] += min_choice

        max_move = max(total_values)
        move_index = total_values.index(max_move)
            
            #list_of_vals = []
            #for move in val:
            #    if len(move) < 5:
            #        break
            #    else:
            #       list_of_vals.append(move[2])
            #print(list_of_vals)
        print("AI Move ->  " + str(possible_moves[move_index][0] + 1) +  " " + str(chr(possible_moves[move_index][1]+65)))
    
        return possible_moves[move_index][0], possible_moves[move_index][1]
            
    def prune_the_tree(self):
        self.maxVal(0, None, None)

    def generate_tree(self, possible_moves):
       i = 0

       counter = 0

       self.state_num_to_list[i] = copy.deepcopy(self.dummy_board)
       self.states[i] = possible_moves
       for move in possible_moves:
           move.append(0)


       if self.color == 'B':
            p_color = 'W'
            color_not_move = 'B'
       else:
            p_color = 'B'
            color_not_move = 'W'
       
       parent = 0
       for child in self.states[0]:
           child[3] = 0

       color_to_move = p_color
       try: 
           while self.states[parent][0][3] < self.depth_look: #or self.states[parent][0][0] == -1:
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
                    move.append(i)
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
                    print(i)
                    if move_holder == []:
                        self.states[i] = [[-1,-1,100,2,i]]
                        
                    else:
                        self.states[i] = move_holder
                    print("self.states[i] : ", self.states[i])
                    
                    self.dummy_board = copy.deepcopy(self.state_num_to_list[parent])

                self.dummy_board = copy.deepcopy(self.state_num_to_list[parent + 1])
                possible_moves = self.states[parent+1]

                parent = parent + 1
       except IndexError:
           pass

       for key, val in self.states.items():
           print(key, "=>")
           for item in val:
               print(item)


    def maxVal(self, node,alpha,beta):
        
        print node
        
        #below check for leaf
        
        if self.states[node][0][3] == self.depth_look:
            return self.states[node][0][2]

        v = float("-inf")
        for child in self.states[node]:
            
            v1 = self.minVal(child[5],alpha,beta)
            
            if v is None or v1 > v:
                v = v1
            if beta is not None:
                if v1 >= beta:
                    return v
            if alpha is None or v1 > alpha:
                alpha = v1
       
        return v

    def minVal(self, node,alpha,beta):
        

        print node

        if self.states[node][0][3] == self.depth_look:
            return self.states[node][0][2]

        v = float("inf")
        for child in self.states[node]:
            
            v1 = self.maxVal(child[5],alpha,beta)
            
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
                        if x-i > -1:
                            i += 1
                        else:
                            break
                    if self.dummy_board[x-i][y]  == color and i > 1 and x-i > -1:
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
                        if y-i > -1:
                            i += 1
                        else:
                            break
                    if self.dummy_board[x][y-i] == color and i > 1 and y-i > -1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass


                try:
                    #CHECK DIAGNOALS
                    i = 1
                    while self.dummy_board[x-i][y-i] != color and self.dummy_board[x-i][y-i] != '-':
                        if x-i > -1 and y-i > -1:
                            i += 1
                        else:
                            break
                    if self.dummy_board[x-i][y-i] == color and i > 1 and x-i > -1 and y-i > -1:
                        move=True
                        total += i - 1
                except IndexError:
                    pass
                
                
                try:
                    i = 1
                    while self.dummy_board[x+i][y-i] != color and self.dummy_board[x+i][y-i] != '-':
                        if y-i > -1:
                            i += 1
                        else:
                            break
                    if self.dummy_board[x+i][y-i] == color and i > 1 and y-i > -1:
                       move=True
                       total += i - 1
                except IndexError:
                    pass


                try:
                    i = 1
                    while self.dummy_board[x-i][y+i] != color and self.dummy_board[x-i][y+i] != '-':
                        if x-i > -1:
                            i += 1
                        else:
                            break
                    if self.dummy_board[x-i][y+i] == color and i > 1 and x-i > -1:
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
                    eligable_moves.append([x,y, total + self.weights[x][y] , self.depth])
                    
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
 

