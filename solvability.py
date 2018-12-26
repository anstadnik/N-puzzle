from helpers import find_blank_puzzle_pos


def count_inverses(puzzle_):
    n = puzzle_.size
    puzzle = puzzle_.state
    inv = 0
    for i in range(n*n):
        i_row = i // n
        i_col = i % n
        if puzzle[i_row][i_col] is None: continue
        for j in range(i, n*n):
            j_row = j // n
            j_col = j % n
            if i == j or puzzle[j_row][j_col] is None: continue
            if puzzle[i_row][i_col] > puzzle[j_row][j_col]:
                inv += 1
    return inv


def is_solvable(start_puzzle, end_state):
    n = start_puzzle.size
    start_inv = count_inverses(start_puzzle)
    end_inv = count_inverses(end_state)
    if n % 2 == 1:
        if start_inv % 2 == end_inv % 2:
            return True
        else:
            return False
    else:
        i1, j1 = find_blank_puzzle_pos(start_puzzle.state)
        i2, j2 = find_blank_puzzle_pos(end_state.state)
        if ((start_inv % 2 == end_inv % 2 and i1 % 2 == i2 % 2) or
            (start_inv % 2 != end_inv % 2 and i1 % 2 != i2 % 2)):
            return True
        else:
            return False
