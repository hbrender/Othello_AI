'''
    Class: CPSC 427
    Team Member 1: Hanna Brender
    Team Member 2: Reid Whitson
    File Name: player.py
'''

class Player():
    def __init__(self):
        self.color = ""

    def get_move(self, s):
        x = -1
        while x < 0 or x > 8:
            try:
                x = int(raw_input("Enter row position (1-8): "))
            except ValueError:
                print("Error -> invalid row position")


        y = 'Z'
        eligable_col = ['A','B','C','D','E','F','G','H']
        while y not in eligable_col:
            try:
                y = raw_input("Enter column position (A-H): ")
            except ValueError:
                print("ERROR -> invalid column postion")

        y = ord(y) - 65

        
        return x-1,y
