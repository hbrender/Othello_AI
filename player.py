
class Player():
    def __init__(self):
        self.color = ""

    def get_move(self, s):
        x = int(raw_input("Enter row position (1-8): "))
        y = raw_input("Enter column position (A-H): ")
        y = ord(y) - 65
        return x-1,y
