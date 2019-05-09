'''
    Class: CPSC 427
    Team Member 1: Hanna Brender
    Team Member 2: Reid Whitson
    File Name: system.py
'''

import time

class System():
    def __init__(self, player, AI):
        self.board =  [['-' for j in range(8)] for i in range(8)]
        self.prior_board = [['-' for j in range(8)] for i in range(8)]
        self.place_start_tokens()

        self.p_score = 2
        self.a_score = 2
        self.prior_a_score = 2
        self.prior_p_score = 2
        
        self.player = player
        self.AI = AI
        
        self.turn = '' # p = players turn, a is ai turn
    
    # set the initial board state
    def place_start_tokens(self):
        self.board[3][3] = "W"
        self.board[4][3] = "B"
        self.board[4][4] = "W"
        self.board[3][4] = "B"
    
        self.prior_board[3][3] = "W"
        self.prior_board[4][3] = "B"
        self.prior_board[4][4] = "W"
        self.prior_board[3][4] = "B"
    
    # switch board configuration at start of game
    def switch_config(self):
        self.board[3][3] = "B"
        self.board[4][3] = "W"
        self.board[4][4] = "B"
        self.board[3][4] = "W"
        
        self.prior_board[3][3] = "B"
        self.prior_board[4][3] = "W"
        self.prior_board[4][4] = "B"
        self.prior_board[3][4] = "W"
    
    # displays an Othello board
    def display_board(self):
        print
        print("  A B C D E F G H")
        for i in range(8):
            print(i + 1),
            for j in range(8):
                print(self.board[i][j]),
            print
        if self.AI.color == "W":
            print("White score: " + str(self.a_score))
            print("Black score: " + str(self.p_score))
        else:
            print("White score: " + str(self.p_score))
            print("Black score: " + str(self.a_score))
        print
    
    # determine colors of each player
    def ask_color(self):
        color = raw_input("Asking P for color (W/B): ")
        self.player.color = color
        print
        
        if color == "W":
            self.AI.color = "B"
            self.turn = 'a'
        else:
            self.AI.color = "W"
            self.turn = 'p'

    # allowing for configuration to be swapped at start
    def ask_config(self):
        answer = raw_input("Do you want switch board configuration? (Y/N) ")
        if answer == "Y":
            self.switch_config()
            self.display_board()

    # play an Othello game
    def play_game(self):
        isGameNotOver = True
        while(not self.board_full() and isGameNotOver):
            skip_turn = False
            # keep track of prior board
            for i in range(8):
                for j in range(8):
                    self.prior_board[i][j] = self.board[i][j]
        

            if self.turn == 'a':
                print("AI is about to make a move.")
                ready = raw_input("P are you ready? (Q for quit) ")
                if ready == "Q":
                    self.end_game()
                else:
                    start_time = time.time()
                    x,y = self.AI.get_move(self)
                    end_time = time.time()
                    total_time = format(end_time-start_time, '.2f')
                    if (end_time-start_time > 10):
                        print("AI generated a move in " + total_time + " seconds")
                        print("Player forefits game")
                        exit(0)
                    print("AI generated a move in " + total_time + " seconds")
                    moveX = x
                    moveY = y
                    moveC = self.AI.color

                    #below sees if we cannot move
                    if x == -1 and y == -1:
                        print("Player AI cannot move")
                        skip_turn = True
                    else:
                        self.board[x][y] = '$'
                    self.turn = 'p'
            else:
                ready = raw_input("P are you ready to make a move? (Q for quit) ")
                if ready == "Q":
                    self.end_game()
                else:
                    # ask player if they can move
                    answer = raw_input("Can P make a move? (Y/N) ")
                    if answer != "N":
                        x,y = self.player.get_move(self)
                        moveX = x
                        moveY = y
                        moveC = self.player.color
                        self.board[x][y] = '$'
                    else:
                        skip_turn = True
                    self.turn = 'a'
            # keep track of prior boards
            self.prior_a_score = self.a_score
            self.prior_p_score = self.p_score
            
            #see if turn skipped or not
            if not skip_turn:
                self.update_scores(moveX, moveY, moveC)
                self.display_board()

                answer = raw_input("Return to prior board? (Y/N) ")
                if answer == "Y":
                    # return to prior states
                    for i in range(8):
                        for j in range(8):
                            self.board[i][j] = self.prior_board[i][j]
                    self.a_score = self.prior_a_score
                    self.p_score = self.prior_p_score
                    # swap turns back
                    if self.turn == 'a':
                        self.turn = 'p'
                    elif self.turn == 'p':
                        self.turn = 'a'
                    self.display_board()
                else:
                    #run over board and change all $ tokens to the color
                    if self.turn == 'a':
                        cur_color = self.player.color
                    else:
                        cur_color = self.AI.color
                    for x in range(8):
                        for y in range(8):
                            if self.board[x][y] == '$':
                                self.board[x][y] = cur_color
                    self.display_board()


            if self.a_score == 0 or self.p_score == 0:
                isGameNotOver = False

    # update board scores
    def update_scores(self, x, y , color):
        # for each square around it, check and see if it starts with the opposite
        # color and then ends with the true color
        if color == 'B':
            oppositeColor = 'W'
        else:
            oppositeColor = 'B'

        if color == self.AI.color:
            self.a_score += 1
        else:
            self.p_score += 1

        #check all 4 moves around it
        changeColorList = []

        #keep track for if it is players move
        
        try:
        #Changes tokens above where the one was placed
            i = 1
            tempList = []
            while self.board[x-i][y] == oppositeColor:
                x_to_add = x-i
                y_to_add = y
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x-i,y])
                i += 1
            if self.board[x-i][y] == color and x-i > -1:
                if tempList != [] and x-i > -1 and y > -1:
                    self.board[x-i][y] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] = '$'
                    changeColorList.append(pair)
        except IndexError:
            pass

        #places tokens below where the one was placed
        try:

            i = 1
            tempList = []
            while self.board[x+i][y] == oppositeColor:
                x_to_add = x+i
                y_to_add = y
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x+i,y])
                i += 1
            if self.board[x+i][y] == color:
                if tempList != [] and x+i > -1 and y > -1:
                    self.board[x+i][y] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] = '$'
                    changeColorList.append(pair)

        except IndexError:
            pass

        try:

            i = 1
            tempList = []
            while self.board[x][y+i] == oppositeColor:
                x_to_add = x
                y_to_add = y+i
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x,y+i])
                i += 1
            if self.board[x][y+i] == color:
                if tempList != [] and x > -1 and y+i > -1:
                    self.board[x][y+i] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] ='$'
                    changeColorList.append(pair)

        except IndexError:
            pass
            
        try:
            i = 1
            tempList = []
            while self.board[x][y-i] == oppositeColor:
                x_to_add = x
                y_to_add = y-i
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x,y-i])
                i += 1
            if self.board[x][y-i] == color and y-i > -1:
                if tempList != [] and y-i > -1 and x > -1:
                    self.board[x][y-i] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] ='$'
                    changeColorList.append(pair)
        except IndexError:
            pass

        try:
        #CHECK DIAGNOALS
            i = 1
            tempList = []
            while self.board[x-i][y-i] == oppositeColor:
                x_to_add = x-i
                y_to_add = y-i
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x-i,y-i])
                i += 1
            if self.board[x-i][y-i] == color and x-i > -1 and y-i > -1:
                if tempList != [] and x-i > -1 and y-i > -1:
                    self.board[x-i][y-i] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] ='$'
                    changeColorList.append(pair)
        except IndexError:
            pass


        try:
            i = 1
            tempList = []
            while self.board[x+i][y-i] == oppositeColor:
                x_to_add = x+i
                y_to_add = y-i
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x+i,y-i])
                i += 1
            if self.board[x+i][y-i] == color and y-i > -1:
                if tempList != [] and x+i > -1 and y-i > -1:
                    self.board[x+i][y-i] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] ='$'
                    changeColorList.append(pair)
        except IndexError:
            pass

        try:
            i = 1
            tempList = []
            while self.board[x-i][y+i] == oppositeColor:
                x_to_add = x-i
                y_to_add = y+i
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x-i,y+i])
                i += 1
            if self.board[x-i][y+i] == color and x-i > -1:
                if tempList != [] and x-i > -1 and y+i > -1:
                    self.board[x-i][y+i] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] ='$'
                    changeColorList.append(pair)
        except IndexError:
            pass


        try:
            i = 1
            tempList = []
            while self.board[x+i][y+i] == oppositeColor:
                x_to_add = x+i
                y_to_add = y+i
                if x_to_add > -1 and y_to_add > -1:
                    tempList.append([x+i,y+i])
                i += 1
            if self.board[x+i][y+i] == color:
                if tempList != [] and x+i > -1 and y+i > -1:
                    self.board[x+i][y+i] = '$'
                for pair in tempList:
                    newX = pair[0]
                    newY = pair[1]
                    self.board[newX][newY] ='$'
                    changeColorList.append(pair)
        except IndexError:
            pass

        #adjust scores
        if changeColorList == []:
            print
            print("----------------------------------")
            print("       ILLEGAL MOVE ")
            print("-----------------------------------")
            print
        else:
            for pair in changeColorList:
                if color == self.AI.color:
                    self.a_score += 1
                    self.p_score -= 1
                else:
                    self.p_score += 1
                    self.a_score -= 1
           

    def end_game(self):
        print
        print("Ending game.")
        if self.p_score > self.a_score:
            print("Player won!")
        elif self.p_score < self.a_score:
            print("AI won!")
        else:
            print("Tie!")
        exit(0)

    def board_full(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == '-':
                    return False
        return True
