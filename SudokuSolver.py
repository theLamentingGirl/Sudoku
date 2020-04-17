import numpy as np
from itertools import *

class SudokuSolver:

    def __init__(self,gameArea):
        self.gameArea=gameArea
        self.choices=np.linspace(1,10)
        self.n=9

    def isEmptySpace(self,index):
        '''Checks if there is an empty space'''
        for row in range(len(self.gameArea[0])):
            for col in range(len(self.gameArea[:,0])):
                if self.gameArea[row,col]==0:
                    #index is a list with 2 elements
                    index[0]=row
                    index[1]=col
                    return True

        return False

    def rowCheck(self,row,num):
        #returns True when same num
        #false when dif num
        for i in range(len(self.gameArea[0])):
            if self.gameArea[row,i]==num:
                return True
        return False

    def colCheck(self,col,num):
        #returns True when same num
        #false when dif num
        for i in range(len(self.gameArea[:,0])):
            if self.gameArea[i,col]==num:
                return True
        return False

    def gridCheck(self,row,col,num):
        #returns True when same num
        #false when dif num
        #to change the grid dimension, change from 3 to n; where n is an integer
        for i in range(int(np.sqrt(self.n))):
            for j in range(int(np.sqrt(self.n))):
                #checks if 3x3 grid after the specified row and col in which num is entered
            #    print(type(i),type(j))
                if self.gameArea[int(i+row),int(j+col)]==num:
                    return True
        return False
    
    def noRepeat(self,row,col,num):
        return(self.rowCheck(row,num)==False and self.colCheck(col,num)==False and (self.gridCheck(row - row%np.sqrt(self.n),col - col%np.sqrt(self.n),num)==False))
     # checks if no. repeats in given row or column or grid
     #returns True if no repeat
#----------------------------------------------------------------------------------
    def algorithm(self):
    #returns True when the board is filled and arrives at a solution to the puzzle

        #initialising row and col
        index=[0,0] 

        #if there is no empty space-> board filled
        if not(self.isEmptySpace(index)):#==False:    
            return True
#            return print(self.gameArea)

        #if there is empty space:
        #value of row and col get updated from isEmptySpace
        row=index[0]
        col=index[1]
        #recursive algorithm to figure out the which num is appropriate
        for num in range(1,10):#self.choices:
            if self.noRepeat(row,col,num):
    #            print("This is the number to be entered",num)
                self.gameArea[row,col]=num
    #            print(self.gameArea)
                if self.algorithm()==True:
                    return True
                self.gameArea[row,col]=0
    #            self.choices.remove(num)
        return False
#
                

def main():
    trial=np.array([[3,0,6,5,0,8,4,0,0], 
          [5,2,0,0,0,0,0,0,0], 
          [0,8,7,0,0,0,0,3,1], 
          [0,0,3,0,1,0,0,8,0], 
          [9,0,0,8,6,3,0,0,5], 
          [0,5,0,0,9,0,6,0,0], 
          [1,3,0,0,0,0,2,5,0], 
          [0,0,0,0,0,0,0,7,4], 
          [0,0,5,2,0,6,3,0,0]])

    trial2=np.array([[0,0,0,2,6,0,7,0,1],
                    [6,8,0,0,7,0,0,9,0],
                    [1,9,0,0,0,4,5,0,0],
                    [8,2,0,1,0,0,0,4,0],
                    [0,0,4,6,0,2,9,0,0],
                    [0,5,0,0,0,3,0,2,8],
                    [0,0,9,3,0,0,0,7,4],
                    [0,4,0,0,5,0,0,3,6],
                    [7,0,3,0,1,8,0,0,0]])

    trial3=np.array([[0,0,0,9,5,2,3,0,0],
                    [0,0,9,8,0,3,7,0,4],
                    [8,3,6,0,0,0,2,5,9],
                    [5,0,8,3,7,6,0,4,0],
                    [0,6,0,2,8,0,0,9,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0]])

    solver=SudokuSolver(trial3)
    if solver.algorithm()==True:
        print(solver.gameArea)
    else:
        print("no sol")

if __name__ == "__main__":main()