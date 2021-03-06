'''
    Class: CPSC 427
    Team Member 1: Hanna Brender
    Team Member 2: Reid Whitson
    File Name: system.py
'''

import copy

class AI():
    def __init__(self):
        self.color = ""
        self.depth = 0
        self.depth_look = 2
        self.dummy_board = []
        self.dummy_p_score = 0
        self.dummy_AI_score = 0
        self.show_prune = False
        
        # heustic: weighted based on best board position
        # from https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
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

    # returns a x and y position for an Othello move
    def get_move(self,s):
        #set the current scores and get a copy of the board 
        self.dummy_p_score = s.p_score
        self.dummy_AI_score = s.a_score
        self.dummy_board = copy.deepcopy(s.board)
        
        # gathers all possible moves
        possible_moves = self.get_eligable_moves(self.color)
        
        # no possible moves generated
        if possible_moves == []:
            return -1,-1

        if self.color == 'B':
            p_color = 'W'
        else:
            p_color = 'B'

        #Generate the tree
        self.generate_tree(possible_moves)

        #prune the tree 
        # AB Pruning occurs in prune_the_tree
        self.prune_the_tree()

        #find the best move
        x,y = self.return_best_move(possible_moves)
        
        return x,y
    
    # finds best move and returns the x and y position
    def return_best_move(self, possible_moves):
        total_values = [item[2] for item in self.states[0]]

        for val in range(len(self.states[0])):
            min_choice = min([choice[2] for choice in self.states[self.states[0][val][5]]])
            total_values[val] += min_choice

        max_move = max(total_values)
        move_index = total_values.index(max_move)
            
        print("AI Move ->  " + str(possible_moves[move_index][0] + 1) +  " " + str(chr(possible_moves[move_index][1]+65)))
    
        return possible_moves[move_index][0], possible_moves[move_index][1]
    
    # prunes the tree of moves using AB pruning
    def prune_the_tree(self):
        self.maxVal(0, None, None)

    # generates the tree of possible moves to depth bound
    def generate_tree(self, possible_moves):
       i = 0

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

       #create the tree based on our depth_look
       try: 
           while self.states[parent][0][3] < self.depth_look:
                # keep track of turn at each level
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
                    move.append(i) # appends the node number to end of move variables
                    
                    #change board so that it looks like the current board in the system
                    self.dummy_change_board(move[0],move[1], color_not_move)

                    #keep track of them the same way we did in the A/B pruning homework, with a ditionary
                    self.state_num_to_list[i] = copy.deepcopy(self.dummy_board)
                    
                    # gets the moves
                    move_holder = self.get_eligable_moves(color_to_move)
                    for row in move_holder:
                        #check it it needs to be negated (so we can minimize the other player's score)
                        if negate:
                            row[2] = -(row[2])
                        #add parent
                        row.append(parent)
                    # if no possible moves (no children) set default to guarentee this move is choosen
                    if move_holder == []:
                        self.states[i] = [[-1,-1,100,2,i]]
                    else:
                        self.states[i] = move_holder
                    # update
                    self.dummy_board = copy.deepcopy(self.state_num_to_list[parent])

                self.dummy_board = copy.deepcopy(self.state_num_to_list[parent + 1])
                possible_moves = self.states[parent+1]

                parent = parent + 1
       except IndexError:
           pass


    # Where AB-Pruning occurs
    def maxVal(self, node,alpha,beta):
        if self.show_prune:
            print node
        
        if self.states[node][0][3] == self.depth_look:
            return self.states[node][0][2]

        v = float("-inf")
        for child in self.states[node]:
            try: 
                v1 = self.minVal(child[5],alpha,beta)
                
                if v is None or v1 > v:
                    v = v1
                if beta is not None:
                    if v1 >= beta:
                        return v
                if alpha is None or v1 > alpha:
                    alpha = v1
            except IndexError:
                pass
           
        return v

    # Where AB-Pruning occurs
    def minVal(self, node,alpha,beta):
        if self.show_prune:
            print node

        if self.states[node][0][3] == self.depth_look:
            return self.states[node][0][2]

        v = float("inf")
        for child in self.states[node]:
            try:
                v1 = self.maxVal(child[5],alpha,beta)
                
                if v is None or v1 < v:
                    v = v1
                if alpha is not None:
                    if v1 <= alpha:
                        return v
                if beta is None or v1 < beta:
                    beta = v1

            except IndexError:
                pass

        return v


    # create a list of all eligable moves and how many tokens each one turns over plus the weights (our heuristic)
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
                    #append the total amount that they change + the weight of board positioning
                    # this is where our heuristic is assigned
                    eligable_moves.append([x,y, total + self.weights[x][y] , self.depth])
                    
                    move = False
                else:
                    move = False
        return eligable_moves

    # Change the current "dummy board" to what it shoud be
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
 

