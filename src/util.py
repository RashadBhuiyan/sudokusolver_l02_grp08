from solver import solve
from random import choice

def isBoardValid(board):
    copy = [x[:] for x in board]
    if solve(copy):
        return True
    return False

def generateRandomValidBoard(hints):
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
    for i in range(hints):
        removed = False
        while not removed:
            coordinate = choice(coordinates)
            coordinates.remove(coordinate)
            x = coordinate[1]
            y = coordinate[0]
            value = board[y][x]
            board[y][x] = 0
            removed = True
            if isBoardValid(board):
                removed = True
            else:
                board[y][x] = value
    return board

def convertInput(inp):
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
    for i in range(len(inp)):
        row = i // 9
        column = i % 9
        board[row][column] = inp[i]
    return board


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

