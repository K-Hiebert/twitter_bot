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

