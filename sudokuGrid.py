import random as rand
from tkinter import *
from tkinter import ttk
import numpy as np

rows, cols = 9, 9
root = Tk()
entryIndex = 0


class DisplaySudoku():

    def __init__(self, root, grid, entryIndex):
        self.root = root
        self.grid = grid
        self.root.title("Sudoku")
        self.root.geometry("2000x800")
        
        self.guess = 0
        self.entries = []
        self.entryVars = []
        self.updatedBoard = []
        self.entryIndex = entryIndex
        self.wrongValueLabels = []

    def display(self, grid):
        #self.entries = []
        
        for row in range(9):
            for col in range(9):
                entryVar = StringVar()

                entry = Entry(self.root,  textvariable=entryVar, width=3, highlightthickness=1, highlightbackground='#000000', justify="center")
                padx = (0, 0)
                pady = (0, 0)

                if (row+1) % 3 == 0 and (row+1) < 9:
                    pady = (0, 10)
                if (col+1) % 3 == 0 and (col+1) < 9:
                    padx = (0, 10)

                entry.grid(row=row, column=col, ipadx=5, ipady=5, padx=padx, pady=pady)
                entry.insert(0, self.grid[row][col])
                self.entries.append(entry)
                self.entryVars.append(entryVar)

    def checkLegality(self, grid, row, col):
        
        boardLabel = Text(root)

        if not self.isLegal(self.grid, row, col, self.grid[row][col]):
            text = f"The Value " + str(self.grid[row][col]) + " at position (" + str(row) + "," + str(col) + ") does not fit on this board.\n"
            self.wrongValueLabels.append(text)

        if len(self.wrongValueLabels) > 0:
            boardLabel.place(x=700, y=0)
            for i in self.wrongValueLabels:
                boardLabel.insert(END, i)
                print(i)
            boardLabel.config(state="disabled")
        else:
            boardLabel = Text(root)
            boardLabel.config(state="disabled")
            boardLabel.place(x=700, y=0)
            

    def checkBoard(self, *args, button):

        self.wrongValueLabels = []
        updatedBoard = []

        for i in range((self.entryIndex-81), len(self.entries)):
            updatedBoard.append(int(self.entries[i].get()))

        updatedBoard = np.array(updatedBoard).reshape(9, 9)

        for row in range(9):
            for col in range(9):
                self.grid[row][col] = int(updatedBoard[row][col])

        self.entryIndex += 81
        self.display(self.grid)
                
        for row in range(9):
            for col in range(9):
                self.checkLegality(self.grid, row, col)

        self.wrongValueLabels = []


    def solutionButton(self, *args):
        self.grid = self.solveGrid(self.grid)

 
    def generateGrid(self, grid):  # Grid of rows * cols blocks

        for i in range(9):
            grid.append([None]*9)

        return grid


    def noDupesGrid(self, grid):

        row, column = self.nextCell(grid)

        choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        if row == None:
            return True

        rand.shuffle(choices)

        for choice in choices:
            if self.isLegal(grid, row, column, choice):
                grid[row][column] = choice

                if self.noDupesGrid(grid):
                    return True

            grid[row][column] = None
        return


    def isLegal(self, grid, row, col, num):

        if type(num) is not int:
            return False

        for i in range(9):
            if (row, i) != (row,col):
                if grid[row][i] == num or num == 0:
                    return False
            
        for i in range(9):
            if (i, col) != (row,col):
                if grid[i][col] == num or num == 0:
                    return False

        subGridRow = (row // 3) * 3
        subGridCol = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                if (subGridRow + i, subGridCol + j) != (row,col):
                    if grid[subGridRow + i][subGridCol + j] == num or num == 0:
                        return False
        return True


    def nextCell(self, grid):

        for i in range(9):
            for j in range(9):
                if grid[i][j] == None:
                    return i, j
        return None, None


    def removeRandomValues(self, grid):

        for i in range(9):
            for j in range(9):
                xRand = rand.choice(list(range(0, 9)))
                yRand = rand.choice(list(range(0, 9)))
                if i == xRand or j == yRand:
                    grid[xRand][yRand] = 0
        return grid


    def solveGrid(self, grid):

        choices = list(range(1, 10))

        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for choice in choices:
                        if self.isLegal(grid, i, j, choice):
                            grid[i][j] = choice

        for i in range(9):
            for j in range(9):
                if not self.isLegal(grid, i, j, grid[i][j]):
                    for choice in choices:
                        if self.isLegal(grid, i, j, choice):
                            grid[i][j] = choice

        self.entryIndex += 81
        self.display(grid)
        return grid


    def returnGrid(self, grid):

        grid = self.generateGrid(grid)  # Create board
        self.noDupesGrid(grid)  # add values 1-9 without duplicates
        grid = self.removeRandomValues(grid)  # remove values to make sudoku puzzle

        return grid
    
    def returnGridButton(self, *args):
        newGrid = []

        newGrid = self.returnGrid(newGrid)
        self.grid = newGrid
        self.entryIndex += 81
        self.display(self.grid)
    

def main():
    grid = []
    board = DisplaySudoku(root, grid, entryIndex)
    
    grid = board.returnGrid(grid)


    # Buttons    
    solveButton = Button(root, text="Solve", justify="center", relief="raised", command=board.solutionButton)
    solveButton.place(x=200, y=600) 

    checkBoardButton = Button(root, text="Check Board", justify="center", relief="raised")
    checkBoardButton.config(command=lambda button=checkBoardButton: board.checkBoard(button=checkBoardButton))
    checkBoardButton.place(x=0, y=600) 

    newBoardButton = Button(root, text="Generate New Board", justify="center", relief="raised", command=board.returnGridButton)
    newBoardButton.place(x=0, y=500)

    root.mainloop()

    for line in board.grid:
        print(line, sep="\t\n")


if __name__ == "__main__":
    main()
