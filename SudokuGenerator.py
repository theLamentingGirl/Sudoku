import numpy as np
from SudokuSolver import *
import random
import time

class SudokuGenerator(SudokuSolver):
    def __init__(self):
        self.n=9
        gameArea=np.zeros((self.n,self.n))
        super().__init__(gameArea)
        self.choices=list(np.arange(1,self.n+1))

    def createFilledBoard(self):
        #initialising row and col
        index=[0,0]
    
        #if the board is filled then we have created a filled board
        if self.isEmptySpace(index)==False:#==False:        
        #    print("No empty space,BOARD FILLED")    
            return True
        #changing the row and cols 
        row=index[0]
        col=index[1]
    #    print(index)
        for i in range(len(self.gameArea[0])):#9 times loop
            #choosing a random num from choices
            num=int(random.choice(self.choices))
#            print(self.choices)

            #if this random num is not repeated then it's entered
            if self.noRepeat(row,col,num)==True:
                self.choices=list(np.arange(1,self.n +1))
                self.gameArea[row,col]=num
                
#                print(self.gameArea)

                #the gameArea after entering num is checked if it has a solution
                if self.algorithm()==True:
                     #if it has a solution then createFilledBoard is recursively
                     #called until the board is filled,i.e. createFilledBoard()==True 
                    if self.createFilledBoard()==True:
                        return True
                    
                #if the algorithm is not True then reverse the num entered to 0,
                # i.e wrong num
                self.gameArea[row,col]=0
            #from choices removed the num that didn't lead to a solution
#            print(self.choices)
            self.choices.remove(num)
            return False

    '''rearranged the gameArea to make it more random'''
    def shuffleBoard(self):
        #board->9x9 filled matrix
        np.random.shuffle(self.gameArea[0:3])
        np.random.shuffle(self.gameArea[3:6])
        np.random.shuffle(self.gameArea[6:9])
 
        board=np.transpose(self.gameArea)

        np.random.shuffle(self.gameArea[0:3])
        np.random.shuffle(self.gameArea[3:6])
        np.random.shuffle(self.gameArea[6:9])

        return self.gameArea


    def createGameArea(self):
        #dumbshit algo that removes n numbsers from the fully filled board
        remove=random.randint(35,45)
        for i in range(remove):
            row=random.randint(0,self.n - 1)
            col=random.randint(0,self.n - 1)
            self.gameArea[row,col]=0

        return self.gameArea

    def printGame(self):
        print("this is the puzzle")
        if self.createFilledBoard()==True:
        #    print(self.createGameArea())
            self.shuffleBoard()
            print(self.createGameArea())
            return self.createGameArea()


def main():

    '''Generates Sudoku puzzle'''
    startT=time.time()
    genSudoku=SudokuGenerator()
    
    genSudoku.printGame()
   
    '''Solves the generated Sudoku puzzle'''
    # trial=genSudoku.gameArea
    # solver=SudokuSolver(trial)
    # if solver.algorithm()==True:
    #     print(solver.gameArea)
    # else:
    #     print("no solution")
    
    endT=time.time()-startT
    print(endT*1000.0,'ms')



if __name__=="__main__":main()


