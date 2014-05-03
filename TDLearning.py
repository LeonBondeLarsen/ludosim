'''
Created on Mar 2, 2014

@author: leon
'''
import numpy as np

class Player():
    def __init__(self, index, name, passive=False, max_updates=200, printout=False, optimal_policy=False):
        # Parse constructor parameters
        self.index = index
        self.name = name
        self.passive = passive
        self.max_updates = max_updates
        self.printout = printout
        self.optimal_policy = optimal_policy
        
        # Class variables
        self.utility = []
        self.visits = [[0.0]*60]*6
        self.updates = 0
        self.home = 57

        self.initUtility()
        
    def initUtility(self):
        stars = [6,12,19,25,32,38,45]
        globes = [1,9,14,22,27,35,40,48]
        
        if self.optimal_policy :    
            for roll in range(6):
                tmp = []
                for tile in range(self.home+6):
                    if tile+roll+1 in stars :
                        tmp.append(1.0)
                    elif tile == self.home:
                        tmp.append(1.0)
                    elif tile == 0:
                        tmp.append(-1.0)
                    else :
                        tmp.append(0.0)
                self.utility.append(tmp)
            self.utility[5][0] = -1.0 # Start+roll6 gives star, which is wrong 
        else :
            for tile in range(self.home+6) :
                if tile == 0 :
                    self.utility.append(-1.0)
                elif tile == self.home :
                    self.utility.append(1.0)
                elif tile == 1 :
                    self.utility.append(0.0)
                elif tile in globes :
                    self.utility.append(0.0)
                elif tile in stars :
                    self.utility.append(0.0)
                else:
                    self.utility.append(0.0)

            self.utility = [self.utility[:],self.utility[:],self.utility[:],self.utility[:],self.utility[:],self.utility[:]] # Extend state space to cover die roll too                      
                                      
    def decideMove(self, state, roll, possible_moves):
        if self.updates < self.max_updates and self.passive :
            token = self.randomMove(state, roll, possible_moves)
            self.update(state[self.index][token], roll, possible_moves[token])
            return self.randomMove(state, roll, possible_moves)
        else :
            best_reward = 0
            token = -1
            for i in range(len(possible_moves)):
                if self.printout :
                    print "Evaluating move " + str(i) + " in " + str(possible_moves) + " rewarding " + str(self.utility[roll-1][possible_moves[i]])
                    
                if self.utility[roll-1][state[self.index][i]] > best_reward and not state[self.index][i] == self.home :
                    if self.printout :
                        print " better than old reward " + str(best_reward)
                    best_reward = self.utility[roll-1][state[self.index][i]]
                    token = i

            if not token == -1 :
                self.visits[roll-1][state[self.index][token]] += 1                
                
                if self.printout :
                    print "  selecting move " + str(token) + " for reward " + str(self.utility[roll-1][possible_moves[token]])
                return token
            else :
                if self.printout :
                    print "No rewarding moves possible"
                token = self.randomMove(state, roll, possible_moves)
            self.update(state[self.index][token], roll, possible_moves[token]) 
            return token
            
                
    def randomMove(self, state, roll, possible_moves):
        change = []
        for token_index, move in enumerate(possible_moves) :
            change.append(move - state[self.index][token_index])
        move = np.random.randint(0,len(possible_moves))
        while(change[move] == 0):
            move = np.random.randint(0,len(possible_moves))
        return move
        
    
    def update(self, old_tile, roll, new_tile):
        self.updates += 1
        if not self.optimal_policy :
            hit_tile = (old_tile + roll)
            learning_rate = (1/(1+(self.visits[roll-1][old_tile])))
            if self.updates > self.max_updates :
                learning_rate /= self.updates
            reward = 0.5*(new_tile - hit_tile)
            temporal_difference = (reward + self.utility[roll-1][hit_tile] - self.utility[roll-1][old_tile])
            self.utility[roll-1][old_tile] += learning_rate * temporal_difference
            
            if self.printout :
                print "Updating transition from " + str(old_tile) + " to " + str(hit_tile) + " visited: " + str(self.visits[roll-1][old_tile])
                print "  Rewards: " + str(self.utility[roll-1][old_tile]) + " and " + str(self.utility[roll-1][hit_tile])
                print " learning rate: " + str(learning_rate) + " and temporal difference: " + str(temporal_difference)
                print "   New utility: " +str(self.utility[roll-1][old_tile])
        