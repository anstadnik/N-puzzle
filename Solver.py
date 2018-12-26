from heapq import heappush, heappop
from Puzzle import Puzzle
from heuristics import *


REVERSED_MOVES = {"d": 'u', 'r': 'l', 'l': 'r', "u": 'd'}


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.dequeues = 0
        self.max_elems = 0

    def dequeue(self):
        self.dequeues += 1
        return heappop(self.queue)[1]

    def enqueue(self, cost, item):
        heappush(self.queue, (cost, item))
        self.max_elems = max(self.max_elems, self.size())

    def size(self):
        return len(self.queue)


class Solver:
    def __init__(self, start_puzzle, end_puzzle):
        self.start_puzzle = start_puzzle
        self.end_puzzle = end_puzzle
        self.end_puzzle_table = {}
        for i in range(end_puzzle.size):
            for j in range(end_puzzle.size):
                self.end_puzzle_table[end_puzzle.state[i][j]] = (i, j)

    def solve(self, heuristic):

        visited = set([self.start_puzzle])

        to_visit = PriorityQueue()
        to_visit.enqueue(0, (self.start_puzzle, []))

        while to_visit.size() > 0:

            cur_puzzle, cur_moves_seq = to_visit.dequeue()

            if cur_puzzle == self.end_puzzle:
                return (cur_moves_seq, to_visit.dequeues, to_visit.max_elems)

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

                new_puzzle = Puzzle(cur_puzzle.size, [row[:] for row in cur_puzzle.state], cur_puzzle.empty_cell[:])
                new_puzzle.make_move(move)
                visited.add(new_puzzle)

                new_moves_seq = cur_moves_seq[:]
                new_moves_seq.append(move)

                heuristic_cost = heuristic(new_puzzle, self.end_puzzle_table)
                total_cost = len(new_moves_seq) + heuristic_cost
                to_visit.enqueue(total_cost, (new_puzzle, new_moves_seq))
        return None
