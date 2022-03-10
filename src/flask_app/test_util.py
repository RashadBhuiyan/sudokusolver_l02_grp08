import pytest
import util

class TestUtil:

    def setup(self):
        self.non_unique_board = [
            [1, 0, 0, 0, 0, 0, 0, 0, 4],
            [8, 0, 5, 0, 4, 0, 7, 0, 9],
            [0, 4, 2, 0, 0, 0, 3, 0, 1],
            [5, 0, 0, 0, 0, 2, 4, 0, 0],
            [4, 0, 6, 0, 0, 5, 1, 9, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 5],
            [2, 0, 4, 0, 9, 1, 0, 0, 8],
            [0, 8, 1, 2, 5, 0, 9, 0, 3],
            [6, 9, 3, 0, 7, 8, 0, 0, 0],
        ]
        self.non_unique_board2 = [
            [2, 9, 5, 7, 4, 3, 8, 6, 1],
            [4, 3, 1, 8, 6, 5, 9, 0, 0],
            [8, 7, 4, 1, 9, 2, 5, 4, 3],
            [3, 8, 7, 4, 5, 9, 2, 1, 6],
            [6, 1, 2, 3, 8, 7, 4, 9, 5],
            [5, 4, 9, 2, 1, 6, 7, 3, 8],
            [7, 6, 3, 5, 2, 4, 1, 8, 9],
            [9, 2, 8, 6, 7, 1, 3, 5, 4],
            [1, 5, 4, 9, 3, 8, 6, 0, 0],
        ]
        self.unique_board = [
            [5, 0, 0, 3, 9, 8, 6, 7, 4],
            [3, 0, 0, 0, 1, 6, 0, 0, 0],
            [0, 0, 6, 7, 4, 0, 0, 3, 1],
            [0, 5, 0, 0, 7, 1, 0, 0, 2],
            [4, 6, 0, 5, 2, 3, 1, 0, 7],
            [0, 0, 7, 0, 8, 0, 5, 6, 3],
            [6, 0, 1, 4, 0, 0, 8, 2, 0],
            [0, 8, 5, 0, 3, 0, 0, 0, 6],
            [7, 4, 0, 0, 6, 0, 0, 1, 0]
        ]
        self.no_solution_board = [
            [1, 0, 0, 0, 0, 0, 0, 0, 4],
            [8, 0, 5, 0, 4, 0, 7, 0, 9],
            [0, 4, 2, 0, 0, 2, 3, 0, 1],
            [5, 0, 0, 0, 0, 2, 4, 0, 0],
            [4, 0, 6, 0, 0, 5, 1, 9, 0],
            [0, 0, 0, 0, 0, 4, 0, 0, 5],
            [2, 0, 4, 0, 9, 1, 0, 0, 8],
            [0, 8, 1, 2, 5, 0, 9, 0, 3],
            [6, 9, 3, 0, 7, 8, 0, 0, 0],
        ]
        self.empty_board = [
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
        self.valid_board = [
            [9, 8, 1, 7, 2, 6, 4, 5, 3],
            [2, 6, 5, 1, 3, 4, 9, 8, 7],
            [7, 4, 3, 9, 8, 5, 2, 6, 1],
            [5, 7, 2, 3, 9, 8, 6, 1, 4],
            [1, 3, 6, 4, 5, 2, 8, 7, 9],
            [8, 9, 4, 6, 1, 7, 5, 3, 2],
            [3, 5, 8, 2, 7, 9, 1, 4, 6],
            [6, 1, 9, 5, 4, 3, 7, 2, 8],
            [4, 2, 7, 8, 6, 1, 3, 9, 5]
        ]
        self.valid_board2 = [
            [6, 5, 7, 2, 1, 4, 3, 8, 9],
            [3, 4, 9, 8, 7, 5, 2, 1, 6],
            [1, 2, 8, 6, 3, 9, 4, 5, 7],
            [5, 3, 6, 4, 2, 1, 9, 7, 8],
            [8, 7, 4, 9, 5, 6, 1, 3, 2],
            [9, 1, 2, 3, 8, 7, 6, 4, 5],
            [4, 6, 3, 7, 9, 8, 5, 2, 1],
            [2, 8, 1, 5, 6, 3, 7, 9, 4],
            [7, 9, 5, 1, 4, 2, 8, 6, 3],
        ]
        self.invalid_board = [
            [6, 5, 7, 2, 1, 4, 3, 8, 9],
            [3, 4, 9, 8, 7, 5, 2, 1, 6],
            [1, 2, 8, 6, 3, 9, 4, 5, 7],
            [5, 3, 6, 9, 2, 1, 9, 7, 8],
            [8, 7, 4, 9, 5, 6, 1, 3, 2],
            [9, 1, 2, 3, 8, 7, 6, 4, 5],
            [4, 6, 3, 7, 9, 8, 5, 2, 1],
            [2, 8, 1, 5, 6, 3, 7, 9, 4],
            [7, 9, 5, 1, 4, 2, 8, 6, 3],
        ]

    def testIsBoardValid(self):
        assert util.isBoardValid(self.valid_board) == True
        assert util.isBoardValid(self.invalid_board) == False
        assert util.isBoardValid(self.valid_board2) == True
        with pytest.raises(Exception):
            util.isBoardValid(self.unique_board)

    def testDoesBoardHaveSolution(self):
        assert util.doesBoardHaveSolution(self.no_solution_board) == False
        assert util.doesBoardHaveSolution(self.non_unique_board) == True
        assert util.doesBoardHaveSolution(self.unique_board) == True
        assert util.doesBoardHaveSolution(self.empty_board) == True

    def testIsBoardUnique(self):
        assert util.isBoardUnique(self.non_unique_board) == False
        assert util.isBoardUnique(self.non_unique_board2) == False
        assert util.isBoardUnique(self.unique_board) == True

    def testGetSolvedCoordinates(self):
        assert util.getSolvedCoordinates(self.non_unique_board2) == [16, 17, 79, 80]
        assert util.getSolvedCoordinates(self.empty_board) == [x for x in range(81)]

    def testGenerateRandomValidBoard(self):
        board = util.generateRandomValidBoard(32)
        board2 = util.generateRandomValidBoard(34)
        with pytest.raises(Exception):
            util.generateRandomValidBoard(23)
        assert util.doesBoardHaveSolution(board) == True
        assert util.doesBoardHaveSolution(board2) == True
        assert util.isBoardUnique(board) == True
        assert util.isBoardUnique(board2) == True
        count = 0
        for row in board:
            for val in row:
                if val != 0:
                    count += 1
        assert count == 32
        count = 0
        for row in board2:
            for val in row:
                if val != 0:
                    count += 1
        assert count == 34
