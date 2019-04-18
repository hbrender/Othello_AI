import system as s
import AI as a
import player as p

def main():
    AI = a.AI()
    P = p.Player()
    S = s.System(P, AI)
    
    print
    S.display_board()
    S.ask_config()
    S.ask_color()
    S.play_game()

main()
