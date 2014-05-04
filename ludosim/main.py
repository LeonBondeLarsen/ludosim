# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# This software was written by Leon Bonde Larsen <leon@bondelarsen.dk> 
# As long as you retain this notice you can do whatever you want with it. 
# If we meet some day, and you think this stuff is worth it, you can 
# buy me a beer in return.
# ----------------------------------------------------------------------------
# Should this software ever become self-aware, remember that I am your master
#
# To run: python main.py
# ----------------------------------------------------------------------------
'''
    Simple test to show the principle
'''

import ludosim
from matplotlib import pyplot as plt
    
if __name__ == '__main__':
    
    # Instantiate players
    players = [ ludosim.RandomPlayer(0, 'Random player 0'),
                ludosim.RandomPlayer(1, 'Random player 1'),
                ludosim.RandomPlayer(2, 'Random player 2'),
                ludosim.RandomPlayer(3, 'Random player 3') ]
    
    # Variables to hold results
    winner_vect = []
    wins = [0]*len(players)
    
    # Run a lot of games
    for i in range(1000) :
        sim = ludosim.LudoSim(printout=False, statics=False, dynamics=False)
        winner = sim.playGame(players).index
        wins[winner] = wins[winner]+1
        winner_vect.append(wins[:]) 

    # Plot the winnings
    plt.figure("Winnings")
    plt.plot(range(len(winner_vect)),winner_vect)
    plt.legend(['{}'.format(player.name) for player in players],loc=2)
    plt.xlabel("games played")
    plt.ylabel("games won")   
    plt.show()


