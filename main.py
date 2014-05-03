'''
Created on Apr 29, 2014

@author: leon@bondelarsen.dk
'''
import numpy as np  
import ludosim
import TDLearning
from matplotlib import pyplot as plt
      
def printUtilitiy(player):   
    plt.figure("Utility player " + players[player].name)
    for i in range(6):
        plt.subplot(611+i)  
        width = 0.35
        plt.bar(np.arange(len(players[player].utility[i][:58])), players[player].utility[i][:58], width)
        plt.xticks(np.arange(len(players[player].utility[i][:58]))+width/2., range(len(players[player].utility[i][:58])) )
        plt.ylabel("Utility roll " + str(i+1))

def printWinnings():
    plt.figure("Winnings")
    plt.plot(range(len(winner_vect)),winner_vect)
    plt.legend(['{}'.format(player.name) for player in players],loc=2)
    plt.xlabel("games played")
    plt.ylabel("games won")
      
if __name__ == '__main__':      
    winner_vect = []
    
    players = [ TDLearning.Player(0, 'TD-active'),
                TDLearning.Player(1, 'TD-passive', passive=True), 
                TDLearning.Player(2, 'TD-optimal', optimal_policy=True),
                ludosim.RandomPlayer(3, 'Random')]
    
    wins = [0]*len(players)
    
    for i in range(1000) :
        sim = ludosim.LudoSim(printout=False)
        winner = sim.playGame(players).index
        wins[winner] = wins[winner]+1
        winner_vect.append(wins[:]) 

    printUtilitiy(0)
    printUtilitiy(1)
    printUtilitiy(2)
    printWinnings()
    plt.show()


