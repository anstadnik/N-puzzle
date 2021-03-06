from Vis import Vis


def_beg = [[1, 2,   3],
           [4, 5,   6],
           [7, 8,   'X']]

def_end = [[1, 2,   3],
           [8, 'X', 4],
           [7, 6,   5]]

if __name__ == "__main__":
    # __import__('ipdb').set_trace()

    beg = [['X', 1, 2],
           [5,   6, 3],
           [4,   7, 8]]

    end = [[1, 2, 3],
           [4, 5, 6],
           [7, 8, 'X']]

    vis = Vis(['l', 'l', 'u', 'r', 'r', 'u', 'l', 'd', 'u', 'l'],
              beg=beg, end=end)
    vis.loop()
