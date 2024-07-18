import time


def read_sudoku_boards_v2(boards):
    with open(boards, 'r') as f:
        content = f.read()
    # split the content into a list of strings, each string is a board
    raw_boards = content.strip().split('\n\n') # remove the trailing whitespace and split the string into a list of boards
    sudoku_boards = [] # create an empty list to store the boards

    for raw_board in raw_boards: # loop through each board
        board = [] # create an empty list to store the rows / one sudoku board per element
        for row in raw_board.split('\n'): # split the string_board into a list of string_rows
            # convert the string_row to a list of integers(1 list per row of integers) and append it to the board list
            board.append([int(num) for num in row.strip()])
        sudoku_boards.append(board) # append the board to the list of boards
    return sudoku_boards # return the list of rows of a list of the board, to the list of all the boards

def is_complete(board):
    # iterate through each row
    for row in board:
        # and check if there is a 0 in the current row
        for cell in row:
            if cell == 0:
                return False
    return True


def select_unassigned_variable(board): # selects the first unassigned variable (cell) in the Sudoku board
    # first for loop is for indentation of the rows in the sudoku board
    for i in range(9):
        # second for loop is for indentation of single cells in the current row, which is the same as the column
        for j in range(9):
            # if the current cell is empty (i = row, j = column)
            if board[i][j] == 0:
                # return the row and column of the current cell
                return i, j
    return None


# The is_consistent function is used during the backtracking process
# to determine whether an assignment is valid before making a recursive call.
# If the assignment is consistent, the algorithm proceeds with the search;
# otherwise, it continues to the next possible value for the cell.
def is_consistent(board, var, value):
    # extract the row and column indices from the var tuple.
    row, col = var

    # Check constraint for the current row
    if value in board[row]: #checks if the current value is in the current row (which is a list)
        return False

    # Check contraint for the current column
    # by iterating through the rows and checking the value of the current column
    # every row is a list, so we can use the column index to get the value of the current column
    for i in range(9):
        if board[i][col] == value:
            return False

    # Check the 3x3 box
    # floor division is used to get the top left cell of the 3x3 box
    row_start, col_start = 3 * (row // 3), 3 * (col // 3)
    # row_start and col_start are the indices of the top left cell of the 3x3 box
    # the for loops iterate through the 3x3 box
    for i in range(row_start, row_start + 3): # iterate through the rows of the 3x3 box
        # if the value is already in the 3x3 box, return False
        for j in range(col_start, col_start + 3): # iterate through the columns of the 3x3 box
            if board[i][j] == value: #
                return False

    return True


def backtrack(board):
    # if the board is complete, return the board
    if is_complete(board): # after the first call returns the board, go to line 104
        return board #  the function returns to the previous call in the recursion,
        # and the completed board is assigned to the result variable:
    # if the board is not complete, select the next unassigned variable
    var = select_unassigned_variable(board)

    for value in range(1, 10):
        # if the value is consistent with the current board
        if is_consistent(board, var, value):
            # update the board with the new value
            board[var[0]][var[1]] = value # var[0] is the row, var[1] is the column in the tuple
            # recursively call the backtrack function
            result = backtrack(board) # the backtrack stops if the val is not consistent for any number in the domain
            if result is not None: # while backtracking, the run time stack is popped and the value is set to 0
                return result # This return statement ensures that the completed board keeps
                # getting returned up the call stack until it reaches the original call to the backtrack function.
            board[var[0]][var[1]] = 0 # after this line, the value is set to 0 and the next value is tried
            # and a new path in the search tree is explored

    return None # signal that the current path is not a solution

def main():
    sudoku_boards = read_sudoku_boards_v2("boards.txt")
    solved_sudoku_boards = []

    start_time = time.time()

    for board in sudoku_boards:
        solved_board = backtrack(board) # the backtrack function returns the solved board
        solved_sudoku_boards.append(solved_board)


    end_time = time.time()

    for i, board in enumerate(solved_sudoku_boards): # enumerate yields both (index, element)
        time.sleep(1)
        print(" ")
        print(f"Solved Sudoku Board {i + 1}:")
        for row in board:
            print(row)

    time_taken = end_time - start_time
    print(f"Time taken to solve 10 Sudoku boards: {time_taken:.4f} seconds")


if __name__ == "__main__":
    main()



