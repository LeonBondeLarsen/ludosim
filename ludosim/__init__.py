# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 43):
# This software was written by Leon Bonde Larsen <leon@bondelarsen.dk> 
# As long as you retain this notice you can do whatever you want with it. 
# If we meet some day, and you think this stuff is worth it, you can 
# buy me a beer in return.
# ----------------------------------------------------------------------------
# Should this software ever become self-aware, remember that I am your master
#
# To install run: python setup.py install
# ----------------------------------------------------------------------------
''' 
    Rules implemented:
        A six must be rolled to leave start
        Token hitting a star is transported to next star
        Exact number must be rolled to hit home
        
    Rules not implemented
        Token hit by enemy must restart
        Two tokens on same tile are safe
        Token on globe is safe
        
'''
import numpy as np

class LudoSim(object):
    def __init__(self, printout=True):
        # Parse parameters
        self.printout = printout
        
        # Setup
        self.globes = [1,9,14,22,27,35,40,48]
        self.stars = [6,12,19,25,32,38,45,51]
        self.start = 0
        self.home = 57
        self.runway_start = 52
        
        # Class variables
        self.state = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
        self.goal_state = [self.home,self.home,self.home,self.home]

    def move(self, player, token, steps):
        self.state[player][token] += steps
        
    def moveTo(self, player, token, tile):
        self.state[player][token] = tile
        
    def getPossibleMoves(self, player, roll):
        out = []
        for token in self.state[player]:
            if self.tokenAtStart(token) :
                if roll == 6 :
                    out.append(1)
                else :
                    out.append(0)
                  
            elif self.tokenAtHome(token):
                out.append(token)
                
            elif self.tokenAtRunway(token+roll):
                if token + roll == self.home :
                    out.append(self.home)
                else:
                    out.append(self.home - ((token+roll)%self.home))
                
            else:
                if (token+roll) in self.stars :
                    index = self.stars.index(token+roll)
                    if index + 1 < len(self.stars) - 1 :
                        index = (index + 1)
                    out.append(self.stars[index])
                else :
                    out.append(token + roll)
        return out
    
    def tokenAtStart(self, token):
        return token == self.start
    
    def tokenAtHome(self, token):
        return token >= self.home
    
    def tokenAtRunway(self, token):
        return token > self.runway_start
    
    def getDieRoll(self):
        return np.random.randint(1,7)
    
    def selectMove(self, player, possible_moves, move):
        self.moveTo(player, move, possible_moves[move])
        
    def playGame(self, players):
        winner = None
        player_index = 0
        turn = 0
        while not winner:
            player_index = (player_index + 1) % len(players)
            turn += 1
            player = players[player_index]
            if self.printout :
                print "Turn number " + str(turn)
                print player.name + " player:"
                print "  state: " + str(self.state[player_index])
                
            
            roll = self.getDieRoll()   
            if self.printout :
                print "  rolled a " + str(roll)
                                     
            moves = self.getPossibleMoves(player_index, roll)    
            if self.printout :
                print "    possible moves: " + str(moves)
            
            if not moves == self.state[player_index] :                       
                selection = player.decideMove(self.state, roll, moves)
                self.selectMove(player_index, moves, selection)
                if self.printout :
                    print "      selected token " + str(selection)
            else :
                if self.printout :
                    print "      no moves possible - passing "
                           
                       
            winner = self.wonGame(player_index)
            if self.printout :
                print "  new state: " + str(self.state[player_index])
            
        return players[player_index]                
        #return players[self.state.index(self.goal_state)]
            
    def wonGame(self, player):
        out = True
        for token in range(len(self.state[player])):
            if self.state[player][token] < 51 :
                out = False
        return out
    
    def printOut(self, state):
        self.printout = state

class RandomPlayer(object):
    def __init__(self, index, name):
        self.name = name
        self.index = index
        
    def decideMove(self, state, roll, possible_moves):
        change = []
        for token_index, move in enumerate(possible_moves) :
            change.append(move - state[self.index][token_index])
        move = np.random.randint(0,len(possible_moves))
        while(change[move] == 0):
            move = np.random.randint(0,len(possible_moves))
        return move
    
    
    