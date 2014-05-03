'''
Created on Apr 29, 2014

@author: leon@bondelarsen.dk
'''

import ludosim
import TDLearning
            
if __name__ == '__main__':      
    wins = [0]*4
    runs = 20
    games = 1000
    
    for simulations in range(runs):
        players = [ TDLearning.Player(0, 'TD-active'),
                    TDLearning.Player(1, 'TD-passive', passive=True), 
                    TDLearning.Player(2, 'TD-optimal', optimal_policy=True),
                    ludosim.RandomPlayer(3, 'Random')]
             
        for i in range(games) :
            sim = ludosim.LudoSim(printout=False)
            winner = sim.playGame(players).index
            wins[winner] = wins[winner]+1

    print str(runs) + " runs of " + str(games) + " games"
    print wins
    print(', '.join('{0:.0f}%'.format(float(k)/sum(wins) * 100) for k in wins))
        


