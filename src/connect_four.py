import numpy as np

NONE = '[ ]'
RED = 'R'           # player has RED and moves first
BLACK = 'B'         # AI has BLACK and moves second
NUM_ROWS = 6
NUM_COLUMNS = 7
PLAYER = True
AI = False


class Game:
    def __init__(self):
        self.board = np.full((NUM_ROWS, NUM_COLUMNS), NONE)
        self.player_to_move = True

    # REQUIRES: 1 <= column <= 7
    def make_move(self, column):
        row = self.get_row_pos(column)
        if self.player_to_move:
            self.board[row][column] = RED
        else:
            self.board[row][column] = BLACK
        self.player_to_move = not self.player_to_move

    def get_row_pos(self, column):
        for row in range(NUM_ROWS):
            if self.board[row][column] == NONE:
                return row

    def is_valid_move(self, column):
        return self.board[NUM_ROWS - 1][column] == NONE

    def check_winning_move(self, color):
        # Check horizontal locations for win
        for c in range(NUM_COLUMNS - 3):
            for r in range(NUM_ROWS):
                if self.board[r][c] == color and self.board[r][c + 1] == color and self.board[r][c + 2] == color and self.board[r][
                    c + 3] == color:
                    return True

        # Check vertical locations for win
        for c in range(NUM_COLUMNS):
            for r in range(NUM_ROWS - 3):
                if self.board[r][c] == color and self.board[r + 1][c] == color and self.board[r + 2][c] == color and self.board[r + 3][
                    c] == color:
                    return True

        # Check positively sloped diaganols
        for c in range(NUM_COLUMNS - 3):
            for r in range(NUM_ROWS - 3):
                if self.board[r][c] == color and self.board[r + 1][c + 1] == color and self.board[r + 2][c + 2] == color and \
                        self.board[r + 3][c + 3] == color:
                    return True

        # Check negatively sloped diaganols
        for c in range(NUM_COLUMNS - 3):
            for r in range(3, NUM_ROWS):
                if self.board[r][c] == color and self.board[r - 1][c + 1] == color and self.board[r - 2][c + 2] == color and \
                        self.board[r - 3][c + 3] == color:
                    return True

    def to_string(self):
        s = ""
        for row in range(NUM_ROWS):
            if row != 0:
                s += '\n'
            for column in range(NUM_COLUMNS):
                s += self.board[5-row][column].center(5)
        return s

    def get_valid_locations(self):
        valid_locations = []
        for col in range(NUM_COLUMNS):
            if self.is_valid_move(col):
                valid_locations.append(col)
        return valid_locations

    def is_over(self):
        return len(self.get_valid_locations()) == 0


def main():
    g = Game()
    print(g.to_string())


if __name__ == "__main__":
    main()














# from itertools import groupby, chain
#
# NONE = '[ ]'
# RED = 'R'
# BLACK = 'B'
#
# def diagonalsPos(matrix, cols, rows):
#     """Get positive diagonals, going from bottom-left to top-right."""
#     for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
#         yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]
#
#
# def diagonalsNeg(matrix, cols, rows):
#     """Get negative diagonals, going from top-left to bottom-right."""
#     for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
#         yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < cols and j < rows]
#
#
# class Game:
#     """
#     [0][0] [1][0]      ...      [6][0]
#     [0][1] [1][1]               [6][1]
#     .                              .
#     .                              .
#     .                              .
#     [0][5] [1][5]      ...      [6][5]
#     """
#     def __init__(self, cols=7, rows=6, requiredToWin=4):
#         self.cols = cols
#         self.rows = rows
#         self.win = requiredToWin
#         self.board = [[NONE] * rows for _ in range(cols)]  # board is list of columns
#         self.black_to_move = True
#
#
#     def __repr__(self):
#         s = ""
#         for i in range(self.rows):
#             if i != 0:
#                 s += '\n'
#             for j in range(self.cols):
#                 s += self.board[j][i].center(5)
#         return s
#
#     def insert(self, column):
#         column = column - 1
#         c = self.board[column]
#         if c[0] != NONE:
#             raise Exception('Column is full')
#         i = -1
#         while c[i] != NONE:
#             i -= 1
#         c[i] = BLACK if self.black_to_move else RED
#         self.black_to_move = not self.black_to_move
#
#     # def checkForWin(self):
#     #     """Check the current board for a winner."""
#     #     w = self.getWinner()
#     #     if w:
#     #         if w == BLACK:
#     #             print("Black WON! Final position is the following:\n")
#     #         else:
#     #             print("Red WON! Final position is the following:\n")
#
#     def getWinner(self):
#         """Get the winner on the current board."""
#         lines = (
#             self.board,  # columns
#             zip(*self.board),  # rows
#             diagonalsPos(self.board, self.cols, self.rows),  # positive diagonals
#             diagonalsNeg(self.board, self.cols, self.rows)  # negative diagonals
#         )
#
#         for line in chain(*lines):
#             for color, group in groupby(line):
#                 if color != NONE and len(list(group)) >= self.win:
#                     return color
#
#     def isDraw(self):
#         for i in range(self.cols) :
#             for j in range(self.rows):
#                 if self.board[i][j] == NONE:
#                     return False
#         return True
#
#
# def main():
#     g = Game()
#     g.insert(1)
#     g.insert(6)
#     g.insert(1)
#     g.insert(3)
#     g.insert(1)
#     g.insert(2)
#     g.insert(1)
#     print(g)
#     print(g.board[5][5])
#
# if __name__ == "__main__":
#     main()