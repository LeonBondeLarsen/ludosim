'''
Created on Apr 29, 2014

@author: leon@bondelarsen.dk
'''
import ludosim
            
if __name__ == '__main__':      
    sim = ludosim.LudoSim(printout=False)
    players = [ludosim.RandomPlayer('Yellow'), 
               ludosim.RandomPlayer('Red'), 
               ludosim.RandomPlayer('Green'), 
               ludosim.RandomPlayer('Blue') ]
    winner = sim.playGame(players)
    print winner.name + " won the game"


