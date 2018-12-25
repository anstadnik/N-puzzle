from helpers import def_beg, def_end
import pygame as pg
from Tile import Tile


class Vis(object):

    """Visualizes the solution of n-puzzle"""

    def __init__(self, solution: list, beg: tuple = None, end: tuple = None):
        """Initializer for Vis"""

        self._cur = list(beg) if beg else def_beg
        self._end = list(end) if end else def_end
        assert len(self._cur) == len(self._cur[0])
        assert len(self._end) == len(self._end[0])
        self._n = len(self._cur)
        self._solution = solution

        self._speed = 1  # pixels per frame
        self._is_moving = False

        self._pg_init()
        self._tiles_init(self._cur)

    def _pg_init(self):
        """Initializes pygame"""

        self._FPS = 60
        self._tile_s = 68
        self._pad = 2
        if (self._tile_s + 2) * self._n > 1000:
            raise RuntimeError("Can display puzzles with maximum size of" +
                               str(1000 / 20))

        pg.init()
        pg.display.set_caption("Easter egg")
        self._clock = pg.time.Clock()
        # TODO Play with a font size
        self._font = pg.font.SysFont('Arial', 25)
        width = height = (self._tile_s + self._pad) * self._n
        self._scr = pg.display.set_mode((width, height))

    def _tiles_init(self, beg):
        """Initializes tiles """

        self._tiles = {}
        for y in range(len(beg)):
            for x in range(len(beg[y])):
                n = beg[y][x]
                if n == 'X':
                    self._emp = (x, y)
                    continue
                s = self._tile_s
                top = (s + 2) * y + 1
                left = (s + 2) * x + 1
                self._tiles[n] = Tile(left, top, s, s, self._font, n)

    def _handler(self, events):
        """Handles events"""

        for event in pg.event.get():
            if event.type == pg.QUIT or\
                    (event.type == pg.KEYDOWN and event.key == pg.K_q):
                return True
        return False

    def _update(self):
        """Moves the tile"""

        if self._is_moving:
            self._moving_tile.move(*self._movement)
            self._counter -= 1
            if not self._counter:
                self._is_moving = False
        else:
            if len(self._solution):
                move = self._solution.pop(0)
                self._check_move(move)

                x, y = self._emp
                self._counter = (self._tile_s + self._pad) // self._speed
                if move == 'u':
                    self._movement = (0, self._speed)
                    self._moving_tile = self._tiles[self._cur[y - 1][x]]
                    self._cur[y][x], self._cur[y - 1][x] = self._cur[y - 1][x],\
                        self._cur[y][x]
                    self._emp = (x, y - 1)
                if move == 'd':
                    self._movement = (0, -1 * self._speed)
                    self._moving_tile = self._tiles[self._cur[y + 1][x]]
                    self._cur[y][x], self._cur[y + 1][x] = self._cur[y + 1][x],\
                        self._cur[y][x]
                    self._emp = (x, y + 1)
                if move == 'l':
                    self._movement = (self._speed, 0)
                    self._moving_tile = self._tiles[self._cur[y][x - 1]]
                    self._cur[y][x], self._cur[y][x - 1] = self._cur[y][x - 1],\
                        self._cur[y][x]
                    self._emp = (x - 1, y)
                if move == 'r':
                    self._movement = (-1 * self._speed, 0)
                    self._moving_tile = self._tiles[self._cur[y][x + 1]]
                    self._cur[y][x], self._cur[y][x + 1] = self._cur[y][x + 1],\
                        self._cur[y][x]
                    self._emp = (x + 1, y)
                print(move)
                print(x, y)
                print(self._moving_tile.get_n())
                self._is_moving = True
            else:
                # TODO visualize it
                assert self._cur == self._end

    def _check_move(self, move):
        """Checks whether or not the move is valid"""

        if move not in 'udlr':
            raise RuntimeError("Unknown move:", move)
        if move == 'u' and self._emp[1] == 0 or\
                move == 'd' and self._emp[1] == self._n - 1 or\
                move == 'l' and self._emp[0] == 0 or\
                move == 'r' and self._emp[0] == self._n - 1:
            print("OH NO")
            for line in self._cur:
                print(*line, sep=' ' * (self._n ** 2 // 10 + 1))
            print("Move -", move)
            raise RuntimeError("WTF wrong move r u serious man")

    def _draw(self):
        """Draws tiles
        :returns: TODO

        """
        # TODO add displaying of moves
        for tile in self._tiles.values():
            tile.draw(self._scr, (125, 74, 210))

    def loop(self):
        """The main loop"""
        while True:
            # TODO change color
            self._scr.fill(pg.Color(0, 0, 0))
            self._update()
            self._draw()
            pg.display.flip()
            self._clock.tick(self._FPS)
            if self._handler(pg.event.get()):
                break
