from SudokuGame import *
import numpy as np

from tkinter import *

# global MARGIN, SIDE, HEIGHT, WIDTH

# MARGIN=20
# SIDE=50
# HEIGHT=WIDTH=MARGIN*2 + SIDE*9


class SudokuUI:
    def __init__(self):
        super().__init__()

        self.parent=Tk()
        self.game=SudokuGame(SudokuSolver(None),SudokuGenerator())
        # Frame.__init__(self,parent)
        self.MARGIN=20
        self.SIDE=50
        self.HEIGHT=self.MARGIN*2 + self.SIDE*9
        self.WIDTH=self.MARGIN*2 + self.SIDE*9
        self.parent.title("Sudoku")

        #sets up the frame in which all the other widgets go into
        
        
        #fill tells the widget to grow to as much space is available
        #fill=BOTH tells to fill in x & y direction
        # fill=X/Y/BOTH 
        # expand tells the master(here parent) to take up any space 
        # not assigned to any widget and distribute to all widgets that 
        # have non-zero expand value
        # side-> tells where to keep the widget relative to each other
        
        self.bottomFrame= Frame(self.parent)
        self.bottomFrame.pack(fill = BOTH, side = BOTTOM)

        self.frame= Frame(self.parent)
        self.frame.pack(fill=BOTH,side = BOTTOM)

        self.topFrame= Frame(self.parent)
        self.topFrame.pack(fill= BOTH, side = BOTTOM)

        self.row=0
        self.col=0

        self.initializingUI()
        self.parent.mainloop()

    def initializingUI(self):
        
        #initialising the canvas

        self.canvas = Canvas(self.frame,width=self.WIDTH,height=self.HEIGHT)
        
        #buttons needed in the UI
        
        self.resetButton = Button(self.bottomFrame,text="RESET",command = self.reset)
        self.resetButton.pack(fill = BOTH, side = LEFT, expand=1)

        self.newGameButton = Button(self.bottomFrame,text="New Game", command = self.newGame)
        self.newGameButton.pack(fill = BOTH, side = RIGHT, expand=1)

        self.checkAnswerButton = Button(self.topFrame , text= "Check", command = self.checkAnswer)
        self.checkAnswerButton.pack(fill = BOTH, side = LEFT, expand=1)

        self.showAnswerButton = Button(self.topFrame, text = "Show Answer", command = self.showAnswer)
        self.showAnswerButton.pack(fill = BOTH, side = RIGHT, expand=1)

        #helper methods
        self.drawGrid()
        self.drawPuzzle()

        #binding actions to left mouse click and number entered
        #general format-> widget.bind(event,function)
        #event->eg. left mouse click; function-> what the mouse click leads to
        self.canvas.bind("<Button-1>",self.cellClicked)#<Button-1> refers to left mouse click
        self.canvas.bind("<Key>",self.keyPressed)#<Key> key that user presses on keyboard
        self.canvas.pack(fill=BOTH)
#-------------------------------------------------------------------------------------------------
    #HELPER METHODS
    def drawGrid(self):
        '''Draws 9x9 grid in gray and 3x3 subgrid in blue'''

        for i in range(10):
            if i%3==0:
                color = "blue"
            else:
                color = "gray"

            #draws vertical lines
            x0 = self.MARGIN + i*self.SIDE
            y0 = self.MARGIN
            x1 = self.MARGIN + i*self.SIDE
            y1 = self.HEIGHT - self.MARGIN
            self.canvas.create_line(x0,y0,x1,y1, fill=color)

            #draws horizontal lines
            x0 = self.MARGIN
            y0 = self.MARGIN + i*self.SIDE
            x1 = self.WIDTH - self.MARGIN
            y1 = self.MARGIN + i*self.SIDE
            self.canvas.create_line(x0,y0,x1,y1,fill=color)

    def drawPuzzle(self):
        '''Enters clues of the Sudoku puzzle into the 9x9 grid'''
        #makes it an empty board to start over
        self.canvas.delete("numbers")
        self.canvas.delete("answer")
    
        for i in range(9):
            for j in range(9):
                #print(self.game.puzzle)
                
                userAnswer=self.game.puzzle[i,j]
                
                if userAnswer!=0:
                    x=self.MARGIN+ j*self.SIDE + self.SIDE/2
                    y=self.MARGIN + i*self.SIDE + self.SIDE/2
                    clues=self.game.startPuzzle[i,j]
                    if userAnswer==clues:
                        color="black"
                    else:
                        color="green"
                    #create_text(xcoord, ycoord,text,etc.)
                    self.canvas.create_text(x,y,text=userAnswer,tags="numbers",fill=color)
                 
# #----------------------------------------------------------------------------------------------
    #BUTTON FUNCTIONS
    def reset(self):
        
        #copies self.startPuzzle to puzzle
        
        #delete's the show answer if clicked
        self.canvas.delete("answer")
        #if user wants to start playing again the same puzzle

        #if user has clicked already on check delete the drawresult
        self.canvas.delete("greenCircle")
        self.canvas.delete("redCircle")
        self.canvas.delete("won")
        self.canvas.delete("lost")
        
        #draw the puzzle again
        self.game.start()
        self.drawPuzzle()

    def newGame(self):

        self.checkAnswerButton.configure(state=NORMAL)
        self.resetButton.configure(state=NORMAL)

        #delete nums n answer if there before
        self.canvas.delete("numbers")
        self.canvas.delete("answer")

        self.canvas.delete("greenCircle")
        self.canvas.delete("redCircle")
        self.canvas.delete("won")
        self.canvas.delete("lost")
        
        self.game.puzzle = np.zeros((9,9))
        generator = SudokuGenerator()
        self.game.startPuzzle = generator.printGame()
        self.game.unsolvedPuzzle = self.game.startPuzzle
        self.game.start()
        self.drawPuzzle()

    def checkAnswer(self):
        self.drawResult()

    def showAnswer(self):

        self.checkAnswerButton.configure(state=DISABLED)
        self.resetButton.configure(state=DISABLED)

        self.canvas.delete("greenCircle")
        self.canvas.delete("redCircle")
        self.canvas.delete("won")
        self.canvas.delete("lost")
        
        #deletes the nums entered by user & clues to give an empty board
        self.canvas.delete("numbers")
        #self.canvas.delete("answer")
        #calls the solve method to get answer to the puzzle
        self.game.solve()
        #in the empty board, the answer is inputted in gray
        for i in range(9):
            for j in range(9):
                
                answer=self.game.solvedPuzzle[i,j]
                x=self.MARGIN+ j*self.SIDE + self.SIDE/2
                y=self.MARGIN + i*self.SIDE + self.SIDE/2

                self.canvas.create_text(x,y,text=answer,tags="answer",fill="gray")  
         
#-------------------------------------------------------------------------------------------------
    #BIND FUNCTIONS

    #event will give us x & y coord of where the user clicked
    def cellClicked(self,event):
        if self.game.gameOver==True:
            return 
        
        x,y= event.x , event.y

        #if user clicks inside the sudoku puzzle gameArea
        if (self.MARGIN< x <self.WIDTH - self.MARGIN) and (self.MARGIN< y <self.HEIGHT-self.MARGIN):
            #focus_set sets focus on a widget
            self.canvas.focus_set()
            #get row and col numbers from x and y coord
            row, col =int((y - self.MARGIN)/self.SIDE) , int((x - self.MARGIN)/self.SIDE)
            
            #if cell was selected already deselect
            if (row,col) == (self.row,self.col):
                #some negative number so it can't be focussed
                self.row,self.col == -1,-1
            
            #select a cell
            elif self.game.puzzle[row,col]==0:
                self.row,self.col = row,col

        self.drawCursor()
        
    #binds <Key> to keyPressed    
    def keyPressed(self,event):
        if self.game.gameOver:
            return 

        if self.row >= 0 and self.col>=0 and event.char in "1234567890":
            self.game.puzzle[self.row,self.col] = int(event.char)
            self.col,self.row=-1,-1
            self.drawPuzzle()
            self.drawCursor()
    

    def drawCursor(self):
        #deleting the highlighted grid before proceeding
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 =self.MARGIN + self.col*self.SIDE+1
            y0 =self.MARGIN + self.row*self.SIDE+1
            x1 =self.MARGIN + (self.col+1)*self.SIDE-1
            y1 =self.MARGIN + (self.row+1)*self.SIDE-1

            self.canvas.create_rectangle(x0,y0,x1,y1,outline="red",tags="cursor")

#--------------------------------------------------------------------------------------------------
    #displays win/lose to the user on the board 
    def drawResult(self):
        #draw a circle which will contain the result
        x0=y0= self.MARGIN + self.SIDE*2
        x1=y1= self.MARGIN + self.SIDE*7
        if self.game.checkWin()==True:
            self.canvas.create_oval(x0,y0,x1,y1,fill="green", outline="dark green",tags="greenCircle")

            x=y=self.MARGIN + 4*self.SIDE+ self.SIDE/2
            self.canvas.create_text(x,y,text="You Win!",tags="won",fill="white",font=("Arial",32))
        else:
            self.canvas.create_oval(x0,y0,x1,y1,fill="red", outline="dark red",tags="redCircle")

            x=y=self.MARGIN + 4*self.SIDE+ self.SIDE/2
            self.canvas.create_text(x,y,text="You Lose!",tags="lost",fill="white",font=("Arial",32))

def main():
    SudokuUI()

if __name__=="__main__": main()