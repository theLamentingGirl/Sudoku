from SudokuGenerator import *
from SudokuSolver import *
import numpy as np

class SudokuGame:
    def __init__(self,solver,generator):
        super().__init__()
        self.gameOver=False
        self.solver=solver
        self.generator=generator
        self.puzzle=np.zeros((9,9))
        self.startPuzzle=self.generator.printGame()
        self.unsolvedPuzzle=self.startPuzzle
        self.solvedPuzzle=np.zeros((9,9))
    #    self.puzzle=self.startPuzzle
        self.start()
        

#----------------------------------------------------------
# #setting the generated gameArea to startPuzzle 
#     def newGameArea(self):
#         if self.generator.createFilledBoard()==True:
#             self.generator.shuffleBoard()
#             return (self.generator.createGameArea())#-> returns gameArea created

    def checkWin(self):
        if self.rowSweep()==False:
            return False
        if self.colSweep()==False:
            return False
        for row in range(3):
            for col in np.arange(3):    
                if self.gridSweep(row,col)==False:
                    return False
        return True
    
    def solve(self):
        self.solver.gameArea=self.unsolvedPuzzle
        print("This is the unsolved puzzle",self.solver.gameArea)
        if self.solver.algorithm()==True:
            self.solvedPuzzle=self.solver.gameArea
            return self.solvedPuzzle

#----------------------------------------------
# --------------------------------
    #HELPER METHODS FOR CHECKWIN

    def rowSweep(self):
        #if True->no numbers repeat row-wise
        #if false-> numbers repeat
        for row in range(9):
            return set(self.puzzle[row])==set(np.arange(1,10))

    def colSweep(self):
        #True if no nums repeat col-wise
        for col in range(9):
            return set(self.puzzle[:,col])==set(np.arange(1,10))

    def gridSweep(self,row,col):
        #True-> when no nums repeat in 3x3 grid
        gridVal=[]
        for r in range(row*3,(row+1)*3):
            for c in range(col*3,(col+1)*3):
                gridVal.append(self.puzzle[r,c])
        return set(gridVal)==set(range(1,10))

#---------------------------------------------------------------------------
#LETS THE USER START THE GAME
#gameOver is set as false initially
    def start(self):
        #self.puzzle is a copy of the gameArea
        for i in range(9):
            for j in range(9):
                #print(type(self.puzzle))
                self.puzzle[i,j]=int(self.startPuzzle[i,j])
                