class AI():
    def __init__(self):
        self.color = ""

    def get_move(self):
        x = int(raw_input("Enter row position (1-8): "))
        y = raw_input("Enter column position (A-H): ")
        y = ord(y) - 65
        return x-1,y

    def can_move(self):
        answer = raw_input("Can AI move (Y/N)? ")
        if answer == "Y":
            return True
        else:
            return False


