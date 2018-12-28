from copy import deepcopy
from helpers import find_blank_puzzle_pos


class Puzzle:
    def __init__(self, n, state, empty_cell=None):
        self.size = n
        self.state = [row[:] for row in state]
        self.empty_cell = find_blank_puzzle_pos(state) if empty_cell is None else empty_cell

    def __str__(self):
        el_len = len(str(max([el for row in self.state for el in row], key=lambda x: len(str(x)) if x is not None else 0)))
        rows = []
        for row in self.state:
            row = ["{:>{width}}".format(el if el is not None else 'X', width=el_len) for el in row]
            rows.append(" ".join(row))
        return '\n'.join(rows)

    def get_valid_moves(self):
        moves = []
        if self.empty_cell[1] > 0:
            moves.append("r")
        if self.empty_cell[1] < (self.size - 1):
            moves.append("l")
        if self.empty_cell[0] > 0:
            moves.append("d")
        if self.empty_cell[0] < (self.size - 1):
            moves.append("u")
        return moves

    def make_move(self, move):
        i, j = self.empty_cell
        if move == 'r':
            self.state[i][j] = self.state[i][j - 1]
            self.state[i][j-1] = None
            self.empty_cell[1] -= 1
        elif move == 'l':
            self.state[i][j] = self.state[i][j + 1]
            self.state[i][j+1] = None
            self.empty_cell[1] += 1
        elif move == 'd':
            self.state[i][j] = self.state[i - 1][j]
            self.state[i-1][j] = None
            self.empty_cell[0] -= 1
        elif move == 'u':
            self.state[i][j] = self.state[i + 1][j]
            self.state[i+1][j] = None
            self.empty_cell[0] += 1

        # TODO remove
        assert 0<=self.empty_cell[0]<self.size and 0<=self.empty_cell[1]<self.size, "Out of bounds"

    def copy(self):
        return Puzzle(self.size, [row[:] for row in self.state], self.empty_cell[:])

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.state))

    def __eq__(self, other):
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] != other.state[i][j]:
                    return False
        return True

    def __lt__(self, other):
        return True