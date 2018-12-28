import random
from Puzzle import Puzzle


def generate_random_puzzle(n):
    nums = list(range(1, n * n))
    nums.append(None)
    random.shuffle(nums)
    puzzle = [[nums[j * n + i] for i in range(n)] for j in range(n)]
    return Puzzle(n, puzzle)


def generate_snail_form(n):
    DIRS = {"r": (0, 1), "l": (0, -1), "u": (-1, 0), "d": (1, 0)}

    puzzle = [[None for _ in range(n)] for _ in range(n)]
    pos = [0, 0]
    direction = 'r'
    cur_el = 1
    while cur_el != n * n:
        puzzle[pos[0]][pos[1]] = cur_el
        cur_el += 1

        if direction == 'r' and (pos[1] == n - 1 or puzzle[pos[0]][pos[1] + 1] is not None):
            direction = 'd'
        elif direction == 'd' and (pos[0] == n - 1 or puzzle[pos[0] + 1][pos[1]] is not None):
            direction = 'l'
        elif direction == 'l' and (pos[1] == 0 or puzzle[pos[0]][pos[1] - 1] is not None):
            direction = 'u'
        elif direction == 'u' and (pos[0] == 0 or puzzle[pos[0] - 1][pos[1]] is not None):
            direction = 'r'

        pos[0] += DIRS[direction][0]
        pos[1] += DIRS[direction][1]
    return Puzzle(n, puzzle)
