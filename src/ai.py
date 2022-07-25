from connect_four import *
import math
import random
from copy import deepcopy
WINDOW_LENGTH = 4

class Ai:
    def __init__(self, game = None):
        self.game = game

    def set_game(self, game):
        self.game = game

    def evaluate_window(self, window, color):
        score = 0
        opp_piece = RED
        if color == RED:
            opp_piece = BLACK

        if window.count(color) == 4:
            score += 100
        elif window.count(color) == 3 and window.count(NONE) == 1:
            score += 5
        elif window.count(color) == 2 and window.count(NONE) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(NONE) == 1:
            score -= 4

        return score

    def convert(self, s):
        if s == NONE:
            return 0
        elif s == RED:
            return 1
        else:
            return 2

    def score_position(self, game, color):
        score = 0

        ## Score center column
        center_array = [self.convert(i) for i in list(game.board[:, NUM_COLUMNS//2])]
        center_count = center_array.count(color)
        score += center_count * 3

        ## Score Horizontal
        for r in range(NUM_ROWS):
            row_array = [self.convert(i) for i in list(game.board[r,:])]
            for c in range(NUM_COLUMNS-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, color)

        ## Score Vertical
        for c in range(NUM_COLUMNS):
            col_array = [self.convert(i) for i in list(game.board[:,c])]
            for r in range(NUM_ROWS-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, color)

        ## Score posiive sloped diagonal
        for r in range(NUM_ROWS-3):
            for c in range(NUM_COLUMNS-3):
                window = [game.board[r+self.convert(i)][c+self.convert(i)] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, color)

        for r in range(NUM_ROWS-3):
            for c in range(NUM_COLUMNS-3):
                window = [game.board[r+3-self.convert(i)][c+self.convert(i)] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, color)

        return score

    def minimax(self, curr_game, depth, alpha, beta, maximizingPlayer):
        valid_locations = curr_game.get_valid_locations()
        is_over = curr_game.game.is_over()
        if depth == 0 or is_over:
            if is_over:
                if curr_game.check_winning_move(BLACK):
                    return (None, 100000000000000)
                elif curr_game.check_winning_move(RED):
                    return (None, -10000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, curr_game.score_position(BLACK))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                # row = curr_game.get_row_pos(col) <- not needed.
                b_copy = deepcopy(curr_game)
                b_copy.make_move(col)
                new_score = self.minimax(b_copy, curr_game, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                #row = curr_game.get_row_pos(col) <- not needed.
                b_copy = deepcopy(curr_game)
                b_copy.make_move(col)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def pick_best_move(self, color):
        valid_locations = self.game.get_valid_locations()
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            temp_game = deepcopy(self.game)
            temp_game.make_move(col)
            score = self.score_position(temp_game, color)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def make_best_move(self):
        self.game.make_move(self.pick_best_move(BLACK))

# For testing
def main():
    g = Game()
    a = Ai(g)
    g.make_move(4)
    a.make_best_move()
    g.make_move(3)
    a.make_best_move()
    g.make_move(1)
    a.make_best_move()
    g.make_move(4)
    a.make_best_move()
    g.make_move(0)
    a.make_best_move()
    g.make_move(2)
    print(g.check_winning_move(RED))


    print(g.to_string())


if __name__ == "__main__":
    main()
