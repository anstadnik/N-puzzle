from Vis import Vis

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
