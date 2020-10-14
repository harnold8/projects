import time

board = [
    [0,0,0,0,0,0,0,0,1],
    [0,0,0,0,1,0,2,3,0],
    [0,0,8,4,3,0,0,0,7],
    [0,9,6,0,2,7,0,4,8],
    [0,0,0,0,0,9,0,0,0],
    [0,5,0,0,0,0,0,0,0],
    [0,0,4,0,0,5,0,0,0],
    [0,0,0,0,9,0,1,0,0],
    [9,8,2,7,0,0,0,0,0]
]

#board output
def output_sudoku(sudoku):
    for i in range(len(sudoku)):
        if i % 3 == 0 :
            print(" - - - - - - - - - - - - - - ")
        for j in range(len(sudoku[1])):
            if j % 3 == 0:
                print(" | ",end="")
            if j == 8:
                print(str(sudoku[i][j])+" | ")
            else:
                print(str(sudoku[i][j]) + " ",end="")

#checking whether the value in x,y fulfills the sudoku rules
def check_rules(x,y,sudoku):
    value=sudoku[y][x]
    #checking if the value is already in the same row or column
    for i in range(len(sudoku)):
        if sudoku[y][i] == value and i != x:
            return False
        if sudoku[i][x] == value and i != y:
            return False
    #checking if the value is in the same box
    #finding the box
    xmin = x // 3
    ymin = y // 3
    for i in range(ymin * 3, ymin * 3 + 3):
        for j in range(xmin * 3, xmin * 3 + 3):
            if sudoku[i][j] == value and i != y and j != x:
                return False
    return True

#if empty entry found, return the coordinates, if not return (-1,-1)
#just have to look at the entries for j>=y
def find_empty(y,sudoku):
    for j in range(y, len(sudoku)):
        for i in range(len(sudoku)):
            if sudoku[j][i] == 0:
                return (i,j)
    return (-1,-1)

#the backtracking solver
def backtracking_solver(sudoku):
    #instead of recursion, I used a stack
    stack = []
    #starting point (x,y)-coordinate
    pos=(0,0)
    pos = find_empty(pos[1],sudoku)
    #until there are zeros in the array
    while pos[0] != -1:
        #since it makes no sense to begin at 0
        sudoku[pos[1]][pos[0]] = 1
        value = 1
        #backtracking algo
        while not check_rules(pos[0],pos[1],sudoku):
            #if value == 9 and still no solution found, we want to go back in the list
            if value == 9:
                sudoku[pos[1]][pos[0]] = 0
                pos = stack.pop()
                #increase the popped value (backtracking algo)
                value = sudoku[pos[1]][pos[0]] + 1
                sudoku[pos[1]][pos[0]] = value
                #special case, if we grab a 9, we want to go back further
                if value > 9:
                    sudoku[pos[1]][pos[0]] = 0
                    pos = stack.pop()
                    value = sudoku[pos[1]][pos[0]] + 1
                    sudoku[pos[1]][pos[0]] = value
            else:
                #iterate from 1-8
                sudoku[pos[1]][pos[0]] += 1
                value = sudoku[pos[1]][pos[0]]
        #append the entry and look for the next zero
        stack.append(pos)
        pos = find_empty(pos[1],sudoku)

start_time = time.time()
backtracking_solver(board)
output_sudoku(board)
print("\n\n%s seconds" % (time.time() - start_time))
