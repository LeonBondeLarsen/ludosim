# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# This software was written by Leon Bonde Larsen <leon@bondelarsen.dk> 
# As long as you retain this notice you can do whatever you want with it. 
# If we meet some day, and you think this stuff is worth it, you can 
# buy me a beer in return.
# ----------------------------------------------------------------------------
# Should this software ever become self-aware, remember that I am your master
# ----------------------------------------------------------------------------

''' 
    To install run: python setup.py install
    
    To use:

import ludosim
            
if __name__ == '__main__':      
    sim = ludosim.LudoSim(printout=True)
    players = [ludosim.RandomPlayer('Yellow'), 
               ludosim.RandomPlayer('Red'), 
               ludosim.RandomPlayer('Green'), 
               ludosim.RandomPlayer('Blue') ]
    winner = sim.playGame(players)
    print winner.name + " won the game"
'''
import numpy as np

class LudoSim(object):
    def __init__(self, printout=True):
        self.state = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
        self.globes = [1,9,14,22,27,35,40,48]
        self.stars = [6,12,19,25,32,38,45,51]
        self.printout = printout

    def move(self, player, token, steps):
        self.state[player][token] += steps
        
    def moveTo(self, player, token, tile):
        self.state[player][token] = tile
        
    def getPossibleMoves(self, player, roll):
        out = []
        for token in self.state[player]:
            if self.tokenAtStart(token) and (roll == 6) :
                out.append(1)
            elif self.tokenAtHome(token):
                out.append(token)
            else:
                if (token + roll) > 51 :
                    out.append(51)
                elif (token+roll) in self.stars :           # The token jumps to the next star
                    index = self.stars.index(token+roll)
                    index = (index + 1) % len(self.stars)
                    out.append(self.stars[index])
                else :
                    out.append(token + roll)
        return out
    
    def tokenAtStart(self, token):
        return token == 0
    
    def tokenAtHome(self, token):
        return token >= 51
    
    def getDieRoll(self):
        return np.random.randint(1,7)
    
    def selectMove(self, player, possible_moves, move):
        self.moveTo(player, move, possible_moves[move])
        
    def playGame(self, players):
        winner = None
        player_index = 0
        turn = 0
        while not winner:
            player = players[player_index]
            roll = self.getDieRoll()                        
            moves = self.getPossibleMoves(player_index, roll)                       
            selection = player.decideMove(self.state, roll, moves)           
            self.selectMove(player_index, moves, selection)           
            winner = self.testState(player_index)
            player_index = (player_index + 1) % len(players)
            
            if self.printout :
                print "Turn number " + str(turn)
                print player.name + " player:"
                print "  rolled a " + str(roll)
                print "    possible moves: " + str(moves)
                print "      selected token " + str(selection)
                print "  new state: " + str(self.state[player_index])
                
        return players[self.state.index([51,51,51,51])]
            
    def testState(self, player):
        out = True
        for token in range(len(self.state[player])):
            if self.state[player][token] < 51 :
                out = False
        return out
    
    def printOut(self, state):
        self.printout = state

class RandomPlayer(object):
    def __init__(self, name):
        self.name = name
        
    def decideMove(self, state, roll, possible_moves):
        return np.random.randint(0,len(possible_moves))