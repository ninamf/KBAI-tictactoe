#the parent class of the two different types of agents, going to use polymorphism to pass in
#the two agents into the program

#shared properties include: symbol...
#shared methods include: 

import random

class Agent(object):
    
    def __init__(self, symbol, turn, winner):
        self.turn = False
        self.symbol = symbol
        
        #changes the properties of the chosen state
    def updateSpace(self, chosenSpace, player):
        chosenSpace.symbol = player.symbol
        chosenSpace.occupied = True
        chosenSpace.owner = player
        
class naiveAgent(Agent):
    
    def __init__(self, symbol, turn):
        Agent.__init__(self, symbol, turn, False)
        self.turn = turn
        self.symbol = symbol
        self.ownedSpaces = []
        self.winner = False
        
    def move(self, openSpaces, player, opponentSpaces, winConds):
        numSpaces = len(openSpaces)
        chosenSpaceIndex = random.randint(0, numSpaces-1)     #picks a random index
        chosenSpace = openSpaces[chosenSpaceIndex]          #choose what move to make based on random index
        self.updateSpace(chosenSpace, player)               #change the properties of the chosen space
        self.ownedSpaces.append(chosenSpace)
        return chosenSpace                                  
    

class smartAgent(Agent):
    
    def __init__(self, symbol, turn):
        Agent.__init__(self, symbol, turn, False)
        self.symbol = symbol
        self.turn = turn
        self.ownedSpaces = []
        self.winner = False
        
    #will implement either generate and test or means end analysis for smart agent
    
    #move selects the best move of the smart agent by generating all possible solutions, checks to see if a solution
    #results in a goal state(win) or if none result in goal state checks if should choose a move that blocks the
    #naive agent or choose a move that will move closer to goal state
    
    def move(self, openSpaces, player, opponentSpaces, winConditions):
        possibleSolutions = openSpaces
        for move in possibleSolutions:
            if self.checkIfWin(move, winConditions):
                self.ownedSpaces.append(move)
                self.winner = True
                self.updateSpace(move, self)
                self.ownedSpaces.append(move)
                return move
        move = self.getMove(opponentSpaces, winConditions, openSpaces)
        self.updateSpace(move, player)
        self.ownedSpaces.append(move)
        return move
            #choose best space, probably should have some type of check that chooses spaces closest to a win condition
    
    def checkIfWin(self, move, winConditions):
        #print "check if win"
        checkWin = []
        for s in self.ownedSpaces:
            checkWin.append(s)
        checkWin.append(move)
        for cond in winConditions:
            if move in cond:                                #want to make sure that it is this new move resulting in win, not that a previous win wasn't detected
                count = 1
                for space in cond:
                    if space in self.ownedSpaces:
                        count += 1
                if count == len(cond):
                    return True
        return False
    
    def getMove(self, opponentSpaces, winConditions, openSpaces):
        return self.block(opponentSpaces, winConditions, openSpaces)
        
    def block(self, opponentSpaces, winConditions, openSpaces):
        #print "block"
        for cond in winConditions:
            count = 0
            spaces= []
            for space in cond:
                if space in opponentSpaces:
                    count += 1
                    spaces.append(space)
            if count == 2:
                for space in cond:
                    if (space not in spaces and space in self.ownedSpaces) or space in spaces:
                        pass
                    else:
                        return space
        return self.bestMove(winConditions, opponentSpaces, openSpaces)
        
    def bestMove(self, winConditions, opponentSpaces, openSpaces):
        #print"best move"
        for cond in winConditions:
            count = 0
            for space in cond:
                if space in self.ownedSpaces:
                    count += 1
            if count == 1:
                cnt = 0
                spaces = []
                for space in cond:
                    if space not in self.ownedSpaces and space not in opponentSpaces and space in openSpaces:
                        cnt += 1
                        spaces.append(space)
                if cnt == 2:
                    spaceIndex = random.randint(0, len(spaces)-1)
                    return spaces[spaceIndex]
        return self.firstMove(winConditions, opponentSpaces, openSpaces)
        
    def firstMove(self, winConditions, opponentSpaces, openSpaces):
        # "first move"
        numSpaces = len(openSpaces)
        chosenSpaceIndex = random.randint(0, numSpaces-1)     #picks a random index
        chosenSpace = openSpaces[chosenSpaceIndex]          #choose what move to make based on random index
        self.updateSpace(chosenSpace, self)               #change the properties of the chosen space
        self.ownedSpaces.append(chosenSpace)
        return chosenSpace
    

    
            
            
            
            
            
            
            
        
        
        