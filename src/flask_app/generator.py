from solver import solve_randomly, find_empty, valid
from random import choice

def hasSolution(board):
    """
    Function that uses backtracking to check if the Sudoku board has a solution or not.
    :param board: The input board.
    :return: boolean
    """
    copy = [x[:] for x in board]
    if solve_randomly(copy):
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

def isBoardValid(board):
    """
    Function that checks if the completed Sudoku board follows all Sudoku rules.
    :param board: The input board.
    :raises Exception: if the board is incomplete, an exception is raised
    :return: boolean
    """
    for row in range(0, len(board)):
        for column in range(0, len(board)):
            if board[row][column] == 0:
                raise Exception("The inputted sudoku board is not complete")
            if not valid(board, (row, column), board[row][column]):
                return False

    return True

# def hasUniqueSolution(board, attempts=5):
#     """
#     Function that checks if the inputted board is unique (i.e. has only one solution)
#     :param board: The input board
#     :param attempts: Attempts the function makes to find another solution
#     :return: board
#     """
#     if not hasSolution(board):
#         raise Exception("The inputted board does not have a solution.")
#     solutions = []
#     copy = [x[:] for x in board]
#     solve_randomly(copy)
#     solutions.append(copy) # initial solution
#     for _ in range(attempts):
#         copy = [x[:] for x in board]
#         solve_randomly(copy)
#         if copy not in solutions: # checking if the solution of the board has not been found before
#             return False
#     return True

def __hasUniqueSolutionsAux(bo, solutions):
    find = find_empty(bo)
    if not find:
        return solutions + 1
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, (row, col), i):
            bo[row][col] = i

            cache = __hasUniqueSolutionsAux(bo, solutions)

            if not cache:
                return False

            if cache > solutions:
                solutions = cache

            if solutions > 1:
                return False

            bo[row][col] = 0

    return solutions

def hasUniqueSolution(bo):
    """
    Checks if the inputted board is unique.
    :param bo: 2d list of ints
    :return: boolean
    """
    if not hasSolution(bo):
         raise Exception("The inputted board does not have a solution.")
    copy = [x[:] for x in bo]
    solns = __hasUniqueSolutionsAux(copy, 0)
    if solns == 1:
        return True
    return False

def generateRandomValidBoard(hints):
    """
    Generates a random valid unique board
    :param hints: The number of hints on the sudoku board
    :raises Exception: If the number of hints is less than 26, an exception is raised.
    :return: board
    """
    if hints < 26:
        raise Exception("The number of hints must not be less than 26.")
    generatedBoard = False
    while not generatedBoard:
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
        solve_randomly(board) 
        coordinates = [(x, y) for x in range(0, 9) for y in range(0, 9)]
        numsRemoved = 0
        for i in range(81-hints):
            removed = False
            while not removed:
                if len(coordinates) == 0: # ran out of coordinates, no board can be generated with current randomly generated board
                    break
                coordinate = choice(coordinates)
                coordinates.remove(coordinate)
                x = coordinate[1]
                y = coordinate[0]
                value = board[y][x]
                board[y][x] = 0
                removed = True
                if hasSolution(board) and hasUniqueSolution(board):
                    numsRemoved += 1
                    removed = True
                else:
                    board[y][x] = value
                    removed = False
            if len(coordinates) == 0:
                break
        if numsRemoved == 81 - hints:
            generatedBoard = True
    return board

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

