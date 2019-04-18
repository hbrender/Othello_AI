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
    
    def place_start_tokens(self):
        self.board[3][3] = "W"
        self.board[4][3] = "B"
        self.board[4][4] = "W"
        self.board[3][4] = "B"
    
        self.prior_board[3][3] = "W"
        self.prior_board[4][3] = "B"
        self.prior_board[4][4] = "W"
        self.prior_board[3][4] = "B"
    
    def switch_config(self):
        self.board[3][3] = "B"
        self.board[4][3] = "W"
        self.board[4][4] = "B"
        self.board[3][4] = "W"
        
        self.prior_board[3][3] = "B"
        self.prior_board[4][3] = "W"
        self.prior_board[4][4] = "B"
        self.prior_board[3][4] = "W"
    
    def display_board(self):
        print
        print("  A B C D E F G H")
        for i in range(8):
            print(i + 1),
            for j in range(8):
                print(self.board[i][j]),
            print
        print("AI score: " + str(self.a_score))
        print("player score: " + str(self.p_score))
        print
    
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

    def ask_config(self):
        answer = raw_input("Do you want switch board configuration? (Y/N) ")
        if answer == "Y":
            self.switch_config()
            self.display_board()

    def play_game(self):
        while(not self.board_full()):
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
                    # count down 10 seconds
                    for i in range(10,0,-1):
                        print(i)
                        time.sleep(1)
                    answer = raw_input("Did AI forfeit? (Y/N) ")
                    if answer == "Y":
                        print("AI forefeits. Player wins.")
                        exit(0)
                    if self.AI.can_move():
                        x,y = self.AI.get_move()
                        moveX = x
                        moveY = y
                        moveC = self.AI.color
                        self.board[x][y] = self.AI.color
                    else:
                        print("AI cannot move.\n")
                        skip_turn = True
                    self.turn = 'p'
            else:
                ready = raw_input("P are you ready to make a move? (Q for quit) ")
                if ready == "Q":
                    self.end_game()
                else:
                    x,y = self.player.get_move()
                    moveX = x
                    moveY = y
                    moveC = self.player.color
                    self.board[x][y] = self.player.color
                    self.turn = 'a'
            # keep track of prior boards
            self.prior_a_score = self.a_score
            self.prior_p_score = self.p_score
            
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

    # TODO: a_score and p_score are not always correct
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
        
        #Changes tokens above where the one was placed
        i = 1
        tempList = []
        while self.board[x-i][y] == oppositeColor:
            tempList.append([x-i,y])
            i += 1
        if self.board[x-i][y] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color
                changeColorList.append(pair)

        #places tokens below where the one was placed
        i = 1
        tempList = []
        while self.board[x+i][y] == oppositeColor:
            tempList.append([x+i,y])
            i += 1
        if self.board[x+i][y] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color

                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.board[x][y+i] == oppositeColor:
            tempList.append([x,y+i])
            i += 1
        if self.board[x][y+i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color

                changeColorList.append(pair)
            
        i = 1
        tempList = []
        while self.board[x][y-i] == oppositeColor:
            tempList.append([x,y-i])
            i += 1
        if self.board[x][y-i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color
                changeColorList.append(pair)

        #CHECK DIAGNOALS
        i = 1
        tempList = []
        while self.board[x-i][y-i] == oppositeColor:
            tempList.append([x-i,y-i])
            i += 1
        if self.board[x-i][y-i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color
                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.board[x+i][y-i] == oppositeColor:
            tempList.append([x+i,y-i])
            i += 1
        if self.board[x+i][y-i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color
                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.board[x-i][y+i] == oppositeColor:
            tempList.append([x-i,y+i])
            i += 1
        if self.board[x-i][y+i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color
                changeColorList.append(pair)

        i = 1
        tempList = []
        while self.board[x+i][y+i] == oppositeColor:
            tempList.append([x+i,y+i])
            i += 1
        if self.board[x+i][y+i] == color:
            for pair in tempList:
                newX = pair[0]
                newY = pair[1]
                self.board[newX][newY] = color
                changeColorList.append(pair)



        #adjust scores
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
