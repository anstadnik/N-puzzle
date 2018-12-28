from heapq import heappush, heappop


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


class PriorityQueue2:
    class Node:
        def __init__(self, val, item):
            self.val = val
            self.item = item
            self.children = []

    def __init__(self):
        self.root = None
        self.dequeues = 0
        self.max_elems = 0
        self._size = 0

    def size(self):
        return self._size

    def dequeue(self):
        self.dequeues += 1
        self._size -= 1
        m = self.root.item
        self.delete_min()
        return m

    def _merge(self, root1, root2):
        if root1 is None:
            return root2
        elif root2 is None:
            return root1
        elif root1.val < root2.val:
            root1.children.append(root2)
            return root1
        else:
            root2.children.append(root1)
            return root2

    def enqueue(self, val, item):
        self._size += 1
        self.max_elems = max(self.max_elems, self._size)
        self.root = self._merge(self.root, self.Node(val, item))

    def delete_min(self):
        self.root = self._merge_pairs(self.root.children)

    def _merge_pairs(self, l):
        if len(l) == 0:
            return None
        elif len(l) == 1:
            return l[0]
        else:
            return self._merge(self._merge(l[0], l[1]), self._merge_pairs(l[2:]))


class Solver:
    def __init__(self, start_puzzle, end_puzzle):
        self.start_puzzle = start_puzzle
        self.end_puzzle = end_puzzle
        self.end_puzzle_table = {}
        for i in range(end_puzzle.size):
            for j in range(end_puzzle.size):
                self.end_puzzle_table[end_puzzle.state[i][j]] = (i, j)

    def solve(self, heuristic, q=2):  #TODO remove queue1

        visited = set([self.start_puzzle])

        to_visit = PriorityQueue() if q == 1 else PriorityQueue2()
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

                new_puzzle = cur_puzzle.copy()
                new_puzzle.make_move(move)
                visited.add(new_puzzle)

                new_moves_seq = cur_moves_seq[:]
                new_moves_seq.append(move)

                heuristic_cost = heuristic(new_puzzle, self.end_puzzle_table)
                total_cost = len(new_moves_seq) + heuristic_cost
                to_visit.enqueue(total_cost, (new_puzzle, new_moves_seq))
        return None
