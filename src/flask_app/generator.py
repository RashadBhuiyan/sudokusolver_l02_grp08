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

