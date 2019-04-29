
class Player():
    def __init__(self):
        self.color = ""

    def get_move(self, s):
        x = int(raw_input("Enter row position (1-8): "))
        while x < 0 or x > 8:
            print("Error -> invalid row position")
            x = int(raw_input("Enter row position (1-8): "))
        
        y = raw_input("Enter column position (A-H): ")
        eligable_col = ['A','B','C','D','E','F','G','H']
        while y not in eligable_col:
            print("Error -> invalid column position")
            y = raw_input("Enter column position (A-H): ")
        y = ord(y) - 65

        
        return x-1,y
