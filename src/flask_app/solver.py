# solver.py
# author: techwithtim
# https://github.com/techwithtim/Sudoku-GUI-Solver
from random import choice

def solve(bo):
    """
    Solves a sudoku board using backtracking
    :param bo: 2d list of ints
    :return: solution
    """
    find = find_empty(bo)
    if find:
        row, col = find
    else:
        return True

    values = list(range(1, 10))

    for i in range(1, 10):
        value = choice(values)
        values.remove(value)
        if valid(bo, (row, col), value):
            bo[row][col] = value
            # print("placing", value, "at ", row, ",", col, "was valid")
            # print_board(bo)

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, pos, num):
    """
    Returns if the attempted move is valid
    :param bo: 2d list of ints
    :param pos: (row, col)
    :param num: int
    :return: bool
    """

    # Check row
    for i in range(0, len(bo)):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check Col
    for i in range(0, len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box

    box_x = pos[1]//3
    box_y = pos[0]//3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True


def find_empty(bo):
    """
    finds an empty space in the board
    :param bo: partially complete board
    :return: (int, int) row col
    """

    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)

    return None

def getSolvedCoordinates(board):
    """
    Generates a list of coordinates that correspond to areas of the board that were filled in via the solver algorithm.
    For example:
    Input
    [2, 9, 5, 7, 4, 3, 8, 6, 1]
    [4, 3, 1, 8, 6, 5, 9, 0, 0]
    [8, 7, 4, 1, 9, 2, 5, 4, 3]
    [3, 8, 7, 4, 5, 9, 2, 1, 6]
    [6, 1, 2, 3, 8, 7, 4, 9, 5]
    [5, 4, 9, 2, 1, 6, 7, 3, 8]
    [7, 6, 3, 5, 2, 4, 1, 8, 9]
    [9, 2, 8, 6, 7, 1, 3, 5, 4]
    [1, 5, 4, 9, 3, 8, 6, 0, 0]
    Generates a list of coordinates [16, 17, 79, 80]
    :param board: input board
    :returns: list of coordinates
    """
    coordinates = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                coordinates.append(row * 9 + col)
    return coordinates


def __print_board(bo):
    """
    prints the board
    :param bo: 2d List of ints
    :return: None
    """
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - -")
        for j in range(len(bo[0])):
            if j % 3 == 0:
                print(" | ",end="")

            if j == 8:
                print(bo[i][j], end="\n")
            else:
                print(str(bo[i][j]) + " ", end="")