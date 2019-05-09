'''
    Class: CPSC 427
    Team Member 1: Hanna Brender
    Team Member 2: Reid Whitson
    Submitted By Hanna Brender
    GU Username: hbrender
    Description: Othello AI
    File Name: othello.py
    Usage: python othello.py
    (need AI.py, player.py, and system.py in the same folder)
'''

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
