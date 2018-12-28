def find_blank_puzzle_pos(puzzle):
    n = len(puzzle)
    for i in range(n):
        for j in range(n):
            if puzzle[i][j] is None:
                return [i, j]