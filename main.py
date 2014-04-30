'''
Created on Apr 29, 2014

@author: leon@bondelarsen.dk
'''
import ludosim
            
if __name__ == '__main__':      
    sim = ludosim.LudoSim(printout=False)
    players = [ludosim.RandomPlayer(0, 'Yellow'), 
               ludosim.RandomPlayer(1, 'Red'), 
               ludosim.RandomPlayer(2, 'Green'), 
               ludosim.RandomPlayer(3, 'Blue') ]
    winner = sim.playGame(players)
    print winner.name + " won the game"


