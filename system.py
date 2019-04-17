
class System():
    def __init__(self, player, AI):
        self.board =  [['-' for j in range(8)] for i in range(8)]
        self.place_start_tokens()
        self.p_score = 2
        self.a_score = 2
        self.player = player
        self.AI = AI
        self.turn = '' # 'p' = players turn, 'a' is ai turn
        self.play = True
    
    def place_start_tokens(self):
        self.board[3][3] = "W"
        self.board[4][3] = "B"
        self.board[4][4] = "W"
        self.board[3][4] = "B"

    def display_board(self):
        print("  A B C D E F G H")
        for i in range(8):
            print(i + 1),
            for j in range(8):
                print(self.board[i][j]),
            print
        print("AI score: " + str(self.a_score))
        print("player score: " + str(self.p_score))

    def ask_color(self):
        color = raw_input("Asking P for color (W/B): ")
        self.player.color = color
        
        if color == "W":
            self.AI.color = "B"
            self.turn = 'a'
        else:
            self.AI.color = "W"
            self.turn = 'p'

    def play_game(self):
        while(not self.board_full()):
            if self.turn == 'a':
                ready = raw_input("AI is about to make a move. P are you ready? (Y/Q)")
                if ready == "Q":
                    self.end_game()
                else:
                    if self.AI.can_move():
                        x,y = self.AI.get_move()
                        moveX = x
                        moveY = y
                        moveC = self.AI.color
                        self.board[x][y] = self.AI.color
                    else:
                        print("AI cannot move")
                    self.turn = 'p'
        
            else:
                ready = raw_input("P are you ready to make a move? (Y/Q)")
                if ready == "Q":
                    self.end_game()
                else:
                    x,y = self.player.get_move()
                    moveX = x
                    moveY = y
                    moveC = self.AI.color
                    self.board[x][y] = self.player.color
                    self.turn = 'a'
            self.update_scores(moveX, moveY, moveC)
            self.display_board()

    def update_scores(self, x, y , color):
        # for each square around it, check and see if it starts with the opposite
        # color and then ends with the true color
        if color == 'B':
            oppositeColor = 'W'
        else:
            oppositeColor = 'B'

        #check all 4 moves around it
        changeColorList = []

        i = 1
        tempList = []
        while self.board[x-i][y] == oppositeColor:
            tempList.append([x,y])
            i += 1
        if self.board[x-i][y] == color:
            for item in tempList:
                changeColorList.append(item)

        i = 1
        tempList = []
        while self.board[x+i][y] == oppositeColor:
            tempList.append([x,y])
            i += 1
        if self.board[x+i][y] == color:
            for item in tempList:
                changeColorList.append(item)

        i = 1
        tempList = []
        while self.board[x][y+i] == oppositeColor:
            tempList.append([x,y])
            i += 1
        if self.board[x][y+i] == color:
            for item in tempList:
                changeColorList.append(item)

        i = 1
        tempList = []
        while self.board[x][y-i] == oppositeColor:
            tempList.append([x,y])
            i += 1
        if self.board[x][y-i] == color:
            for item in tempList:
                changeColorList.append(item)


        for pair in changeColorList:
            newX = pair[0]
            newY = pair[1]
            self.board[newX][newY+1] = color 
            
            if color == self.AI.color:
                self.a_score += 1
                self.p_score -= 1
            else:
                self.p_score += 1
                self.a_score -= 1

    def end_game(self):
        print("Ending game")
        if self.p_score > self.a_score:
            print("Player won")
        elif self.p_score < self.a_score:
            print("AI won")
        else:
            print("Tie")
        exit(0)

    def board_full(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == '-':
                    return False
        return True


