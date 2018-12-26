def manhattan_heuristic(puzzle, end_table):
    cost = 0
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            elem = puzzle.state[i][j]
            if elem is None: continue
            cur_cost = abs(i - end_table[elem][0]) + abs(j - end_table[elem][1])
            cost += cur_cost
    return cost


def euclidean_heuristic(puzzle, end_table):
    cost = 0
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            elem = puzzle.state[i][j]
            cur_cost = ((i - end_table[elem][0])**2 + abs(j - end_table[elem][1])**2)**0.5
            cost += cur_cost
    return cost


def hamming_heuristic(puzzle, end_table):
    cost = 0
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            elem = puzzle.state[i][j]
            cur_cost = 0 if end_table[elem][0] == i and end_table[elem][1] == j else 1
            cost += cur_cost
    return cost
