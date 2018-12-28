from Puzzle import Puzzle
import os


def parse_puzzle(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError
    content = open(filename, "r").read()
    lines = content.split('\n')
    puzzle_size = None
    puzzle = []
    for line in lines:
        words = line.strip().split()
        words = remove_comments(words)

        # parse puzzle_size
        if puzzle_size is None and words:
            if len(words) > 1 or not words[0].isdigit() or int(words[0]) <= 1:
                raise Exception("Shitty puzzle size")
            puzzle_size = int(words[0])
        # parse puzzle row
        else:
            for word in words:
                if not word.isdigit():
                    raise Exception("Bad shit {}".format(word))
            if len(words) > 0 and len(words) != puzzle_size:
                raise Exception("Too much/not enough shit in line")
            if words:
                puzzle.append(list(map(int, words)))
    if len(puzzle) != puzzle_size:
        raise Exception("Too much/not enough shit in file")

    for row in puzzle:
        if 0 in row:
            row[row.index(0)] = None
    return Puzzle(puzzle_size, puzzle)


def remove_comments(words):
    comment_word = None
    for i, word in enumerate(words):
        if word[0] == '#':
            comment_word = i
            break
    if comment_word is not None:
        words = words[:comment_word]
    return words