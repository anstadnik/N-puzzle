from gen import make_puzzle
from random import seed
from solvability import count_inverses, is_solvable
from parser import parse_puzzle
from solvability import is_solvable
from puzzle_generators import generate_snail_form
from copy import deepcopy
from Solver import *
from Vis import Vis

seed(7)
solv = True
n = 3
w = len(str(n * n))

def solve_bfs(start_state, end_puzzle):
    visited = set([start_state])

    to_visit = [(start_state, [])]

    while len(to_visit) > 0:

        cur_puzzle, cur_moves_seq = to_visit.pop(0)

        if cur_puzzle == end_puzzle:
            return cur_moves_seq

        poss_moves = cur_puzzle.get_valid_moves()
        for move in poss_moves:
            # check if new state is cool before making copy
            cur_puzzle.make_move(move)
            skip = False
            if cur_puzzle in visited:
                skip = True
            cur_puzzle.make_move(REVERSED_MOVES[move])
            if skip:
                continue

            new_puzzle = cur_puzzle.copy()
            new_puzzle.make_move(move)
            visited.add(new_puzzle)

            new_moves_seq = cur_moves_seq[:]
            new_moves_seq.append(move)

            to_visit.append((new_puzzle, new_moves_seq))
    return None


def gen_puzzle(n, solv=True, iterations=10000):
    puzzle, shit = make_puzzle(n, solvable=solv, iterations=iterations)
    s = ""
    s += "# This puzzle is %s (by generator)\n" % ("solvable" if solv else "unsolvable")
    s += "%d\n" % n
    for y in range(n):
        for x in range(n):
            s += "%s " % (str(puzzle[x + y * n]).rjust(w))
        s += '\n'

    filename = "./test"
    open(filename, "w").write(s)
    puzzle = parse_puzzle(filename)
    return puzzle


# check that both queues generates same answer(not)
heuristic = manhattan_heuristic

for i in range(1000):
    puzzle = gen_puzzle(n, iterations=1000)
    end_puzzle = generate_snail_form(n)
    solver = Solver(puzzle, end_puzzle)
    moves, a, b = solver.solve(heuristic, q=2)
    moves2, _, _ = solver.solve(heuristic, q=1)
    if len(moves) != len(moves2):
        moves3 = solve_bfs(puzzle, end_puzzle)
        print(len(moves), len(moves2))
        print(moves)
        print(moves2)
        print(moves3)
        test1 = puzzle.copy()
        test2 = puzzle.copy()
        for move in moves:
            test1.make_move(move)
        for move in moves2:
            test2.make_move(move)
        print(test1, end='\n\n')
        print(test2)
        print(test1 == end_puzzle, test2 == end_puzzle)

# print(manhattan_heuristic(puzzle, solver.end_puzzle_table))
# print(euclidean_heuristic(puzzle, solver.end_puzzle_table))
# print(hamming_heuristic(puzzle, solver.end_puzzle_table))

#solve_bfs(puzzle, end_puzzle)

import timeit

# print(timeit.timeit('solver.solve(manhattan_heuristic, 1)', number=50, globals=globals()))
# print(timeit.timeit('solver.solve(manhattan_heuristic, 2)', number=20, globals=globals()))

exit(1)


# visual part
print(puzzle, end='\n\n')
print(end_puzzle, end='\n\n')
print(is_solvable(puzzle,  end_puzzle))
# print(solver.solve(manhattan_heuristic))
moves, a, b = solver.solve(manhattan_heuristic)
print(moves, a, b)
beg = puzzle.state
end = end_puzzle.state
for i in range(puzzle.size):
    for j in range(puzzle.size):
        if beg[i][j] is None: beg[i][j] = 'X'
        if end[i][j] is None: end[i][j] = 'X'

# vis = Vis(moves, puzzle.state, end_puzzle.state)
# vis.loop()
# print(solver.solve(euclidean_heuristic))
# print(solver.solve(hamming_heuristic))

exit(1)

# lot of shit...
for iters in range(0, 100000):
    print(iters)
    puzzle, shit = make_puzzle(n, solvable=solv, iterations=iters)
    s = ""
    s += "# This puzzle is %s (by generator)\n" % ("solvable" if solv else "unsolvable")
    s += "%d\n" % n
    for y in range(n):
        for x in range(n):
            s += "%s " % (str(puzzle[x + y * n]).rjust(w))
        s += '\n'

    filename = "./test"
    open(filename, "w").write(s)
    puzzle = parse_puzzle(filename)


    end_puzzle = generate_snail_form(puzzle.size)
    if is_solvable(puzzle, end_puzzle) != solv:
        print(iters)
        print(puzzle, end='\n\n')
        print(end_puzzle)
        print(shit)
        break
    solve_bfs(puzzle, end_puzzle)

exit(1)

puzzle, shit = make_puzzle(n, solvable=solv, iterations=1)
s = ""
s += "# This puzzle is %s (by generator)\n" % ("solvable" if solv else "unsolvable")
s += "%d\n" % n
for y in range(n):
    for x in range(n):
        s += "%s " % (str(puzzle[x + y * n]).rjust(w))
    s += '\n'

filename = "./test"
open(filename, "w").write(s)
puzzle = parse_puzzle(filename)


end_puzzle = generate_snail_form(puzzle.size)
s += "# This puzzle is %s (by checker)\n" % ("solvable" if is_solvable(puzzle, end_puzzle) else "unsolvable")

print("Start puzzle inverses: {}".format(count_inverses(puzzle)))
print(puzzle)
print("End puzzle inverses: {}".format(count_inverses(end_puzzle)))
print(end_puzzle)

print(is_solvable(puzzle, end_puzzle))

print(s)
print(puzzle)
print(puzzle == puzzle, puzzle == end_puzzle, end_puzzle == end_puzzle)

def cmp_state(first, second):
    n = first.size
    for i in range(n):
        for j in range(n):
            if first.state[i][j] != second.state[i][j]:
                return False
    return True



solve_bfs(puzzle, end_puzzle)
