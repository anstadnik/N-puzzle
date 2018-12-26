from gen import make_puzzle
from random import seed
from solvability import count_inverses, is_solvable
from parser import parse_puzzle
from solvability import is_solvable
from puzzle_generators import generate_snail_form
from copy import deepcopy
from Solver import *
from Vis import Vis

seed(6)
solv = True
n = 5
w = len(str(n * n))

def solve_bfs(start_state, end_state):
    visited = set()
    next_states = [start_state]
    cur_state = start_state
    while cur_state != end_state:
        moves = cur_state.get_valid_moves()
        for move in moves:
            next_state = deepcopy(cur_state)
            next_state.make_move(move)
            if next_state not in visited:
                next_states.append(next_state)
                visited.add(next_state)
        cur_state = next_states.pop(0)
    print("Solved")

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


puzzle = gen_puzzle(n, iterations=200)
end_puzzle = generate_snail_form(n)
solver = Solver(puzzle, end_puzzle)

print(manhattan_heuristic(puzzle, solver.end_puzzle_table))
# print(euclidean_heuristic(puzzle, solver.end_puzzle_table))
# print(hamming_heuristic(puzzle, solver.end_puzzle_table))

#solve_bfs(puzzle, end_puzzle)

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

vis = Vis(moves, puzzle.state, end_puzzle.state)
vis.loop()
# print(solver.solve(euclidean_heuristic))
# print(solver.solve(hamming_heuristic))

exit(1)


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
