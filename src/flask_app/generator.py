from solver import solve
from random import choice

def __hasSolution(board):
    """
    Function that uses backtracking to check if the Sudoku board has a solution or not.
    :param board: The input board.
    :return: boolean
    """
    copy = [x[:] for x in board]
    if solve(copy):
        return True
    return False

# def checkRowAndColumn(num, row, column, board):
#     for i in range(len(board)):
#         if board[row][i] == num and column != i:
#             return False
    
#     for i in range(len(board)):
#         if board[i][column] == num and row != i:
#             return False
    
#     return True

# def isBoardValid(board):
#     """
#     Function that checks if the completed Sudoku board follows all Sudoku rules.
#     :param board: The input board.
#     :raises Exception: if the board is incomplete, an exception is raised
#     :return: boolean
#     """
#     for row in range(0, len(board)):
#         for column in range(0, len(board)):
#             if board[row][column] == 0:
#                 raise Exception("The inputted sudoku board is not complete")
#             if not checkRowAndColumn(board[row][column], row, column, board):
#                 return False

#             box_x = column//3
#             box_y = row//3

#             for i in range(box_y*3, box_y*3 + 3):
#                 for j in range(box_x*3, box_x*3 + 3):
#                     if board[i][j] == board[row][column] and (i,j) != (row, column):
#                         return False

#     return True

def hasUniqueSolution(board, attempts=5):
    """
    Function that checks if the inputted board is unique (i.e. has only one solution)
    :param board: The input board
    :param attempts: Attempts the function makes to find another solution
    :return: board
    """
    if not __hasSolution(board):
        raise Exception("The inputted board does not have a solution.")
    solutions = []
    copy = [x[:] for x in board]
    solve(copy)
    solutions.append(copy) # initial solution
    for _ in range(attempts):
        copy = [x[:] for x in board]
        solve(copy)
        if copy not in solutions: # checking if the solution of the board has not been found before
            return False
    return True

def generateRandomValidBoard(hints, uniquenessLikelihood=5):
    """
    Generates a random valid unique board
    :param hints: The number of hints on the sudoku board
    :param uniquenessLikelihood: The amount of times to check for multiple solutions in each iteration of the random board generation. The higher the number, the greater the likelihood of generating a board with one solution.
    :raises Exception: If the number of hints is less than 24, an exception is raised.
    :return: board
    """
    if hints < 24:
        raise Exception("The number of hints must not be less than 24.")
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    solve(board) 
    coordinates = [(x, y) for x in range(0, 9) for y in range(0, 9)]
    print(coordinates)
    for i in range(81-hints):
        removed = False
        while not removed:
            coordinate = choice(coordinates)
            coordinates.remove(coordinate)
            x = coordinate[1]
            y = coordinate[0]
            value = board[y][x]
            board[y][x] = 0
            removed = True
            if __hasSolution(board) and hasUniqueSolution(board, uniquenessLikelihood):
                removed = True
            else:
                board[y][x] = value
                removed = False
    return board

# board = generateRandomValidBoard(24)
# for row in board:
#     print(row)

# solve(board3)
# for row in board3:
#     print(row)

# print(isBoardValid(board3))

# print(isBoardValid(valid_board))

# testing if board is valid
# board = generateRandomValidBoard(21)
# count = 0
# while isBoardValid(board):
#     board = generateRandomValidBoard(21)
#     print(str(isBoardValid(board)) + " " + str(count))
#     count += 1

# print("not valid")
# for row in board:
#     print(row)

