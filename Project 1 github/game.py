#TODO implement game, which takes in two different types of agents, may be the same type of agent,
#also knows whose turn it is, the current representation of the board - updates the board interface
#after a player move -- checks if a space is already occupied, checks end of game conditions after
#every move

from agent import *
import sys
import time


class game(object):
    
    def __init__(self, player1, player2):
        self.spaces = self.initFormattedSpaces()
        self.player1 = player1
        self.player2 = player2
        self.occupiedSpaces = []
        self.openSpaces = self.initSpaces()
        self.winConditions = self.initWinConditions()
        self.winner = False
        self.turnLabel = ""
        self.winnerLabel = ""
        
    
    def initWinConditions(self):
        condition1 = [self.tl, self.m, self.br]
        condition2 = [self.tl, self.tm, self.tr]
        condition3 = [self.l,self.m, self.r]
        condition4 = [self.bl, self.bm, self.br]
        condition5 = [self.tr, self.m, self.bl]
        condition6 = [self.tl, self.l, self.bl]
        condition7 = [self.tm, self.m,self.bm]
        condition8 = [self.tr, self.r, self.br]
        return [condition1, condition2, condition3, condition4, condition5, condition6, condition7, condition8]
    
    def startGame(self):
        self.player1.turn = True
        self.player2.turn = False
        self.turnLabel = "Player 1 Just Made a Move!"
        self.move()
        
    def move(self):
        chosenSpace = None
        if self.player1.turn == True:
            #call player1 move method
            chosenSpace = self.player1.move(self.openSpaces, self.player1, self.player2.ownedSpaces, self.winConditions)
        else:
            chosenSpace = self.player2.move(self.openSpaces, self.player2, self.player1.ownedSpaces, self.winConditions)
        self.openSpaces.remove(chosenSpace)
        self.occupiedSpaces.append(chosenSpace)
        
        self.draw()
        
        time.sleep(3)                                   #have a pause so can see the progress of the game on the board
        
        if not (self.checkWin()):
            if(self.checkTie()):
                self.draw()
                self.endGame("There was a draw!")
        else:
            self.draw()
            self.endGame("Congratulations to the Winner!")
            self.winner = True
        
        #time.sleep(3)                                   #have a pause so can see the progress of the game on the board
        
        if self.player1.turn == True:
            self.player1.turn = False
            self.player2.turn = True
            self.turnLabel = "Player 2 Just Made a Move!"
        elif self.player2.turn == True:
            self.player1.turn = True
            self.player2.turn = False
            self.turnLabel = "Player 1 Just Made a Move!"
            
        self.move()
    
    def endGame(self, endMessage):
        sys.exit(endMessage)
        
           
    def checkTie(self):
        if len(self.openSpaces) == 0 and len(self.occupiedSpaces) == 9:
            self.winnerLabel = "There seems to have been a draw!"
            return True
        return False
    
    def checkWin(self):
        for cond in self.winConditions:
            countPlayer1 = 0
            countPlayer2 = 0
            for space in cond:
                if space in self.player1.ownedSpaces:
                    countPlayer1 += 1
                elif space in self.player2.ownedSpaces:
                    countPlayer2 += 1
            if countPlayer1 == 3:
                self.winner = self.player1
                self.player1.winner = True
                self.winnerLabel = "Player 1 Is The Winner!"
                return True
            elif countPlayer2 == 3:
                self.winner = self.player2
                self.player2.winner = True
                self.winnerLabel = "Player 2 Is The Winner!"
                return True
            else: 
                pass
        return False
    
    def draw(self):
        for row in self.spaces:
            print "%s | %s | %s" % (row[0].__str__(), row[1].__str__(), row[2].__str__())
        print self.turnLabel
        print self.winnerLabel
                
            
            
    def initFormattedSpaces(self):
        spaces = []
        row1 = []
        row2 = []
        row3 = []
        self.tl = space('tl', False)
        self.tm = space('tm', False)
        self.tr = space('tr', False)
        row1.append(self.tl), row1.append(self.tm), row1.append(self.tr)
        self.l = space('l', False)
        self.m = space('m', False)
        self.r = space('r', False)
        row2.append(self.l), row2.append(self.m), row2.append(self.r)
        self.bl = space('bl', False)
        self.bm = space('bm', False)
        self.br = space('br', False)
        row3.append(self.bl), row3.append(self.bm), row3.append(self.br)
        spaces.append(row1), spaces.append(row2), spaces.append(row3)
        return spaces
    
    def initSpaces(self):
        spaces = []
        for row in self.spaces:
            for space in row:
                spaces.append(space)
        return spaces
    
    def checkOccupied(self, space):
        return space.occupied
        
        
class space(object):
    
    def __init__(self, spacePos, occupied):
        self.symbol = "#"
        self.spacePos = spacePos
        self.occupied = occupied
    
    def setOwner(self, owner):
        self.owner = owner
        self.symbol = self.owner.symbol
        self.occupied = True
    
    def hasOwner(self):
        if self.owner is not None:
            return True
        else:
            return False
    
    def getSymbol(self):
        return self.symbol
    
    def __str__(self):
        return self.symbol
    
    
        
        
    
    

def main():
    #print sys.argv
    #can change the two players below to be any type
    args = sys.argv
    
    player1 = None
    player2 = None
    
    if args[1] == 'naive':
        player1 = naiveAgent('X', False)
        print "Player 1 is a Naive Agent and their symbol is X"
    elif args[1] == 'smart':
        player1 = smartAgent('X', False)
        print "Player 1 is a Smart Agent and their symbol is X"
        
    if args[2] == 'naive':
        player2 = naiveAgent('O', False)
        print "Player 2 is a Naive Agent and their symbol is O"
    elif args[2] == 'smart':
        player2 = smartAgent('O', False)
        print "Player 2 is a Smart Agent and their symbol is O"
        
    
        
    
    #player1 = smartAgent('X', False)
    #player2 = smartAgent('O', False)
    print
    tictactoe = game(player1, player2)
    tictactoe.startGame() 
    
    
    
if __name__ == "__main__":
    main()      
    
    
    
    