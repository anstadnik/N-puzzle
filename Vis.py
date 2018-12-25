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

        self._speed = 10  # pixels per frame
        self._is_moving = False
        self._finished = False
        self._cur_move = ''

        self._pg_init()
        self._tiles_init(self._cur)

    def _pg_init(self):
        """Initializes pygame"""

        self._FPS = 60
        self._tile_s = 68
        self._pad = 2
        if self._n < 3:
            raise RuntimeError("Can display puzzles with minimum size of 3")
        if (self._tile_s + 2) * self._n > 1000:
            raise RuntimeError("Can display puzzles with maximum size of" +
                               str(1000 / 20))

        pg.init()
        pg.display.set_caption("Easter egg")
        self._clock = pg.time.Clock()
        # TODO Play with a font size
        self._font = pg.font.SysFont('Arial', 30)
        self._cap_font = pg.font.SysFont('Arial', 40)
        width = height = (self._tile_s + self._pad) * self._n
        height += 50  # Line with movements
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

    def _handler(self):
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
                self._set_move(move)
            else:
                assert self._cur == self._end
                self._cur_move = ''
                self._finished = True

    def _set_move(self, move):
        """Sets the move"""
        x, y = self._emp
        self._counter = (self._tile_s + self._pad) // self._speed
        if move == 'd':
            self._movement = (0, self._speed)
            self._moving_tile = self._tiles[self._cur[y - 1][x]]
            self._cur[y][x], self._cur[y - 1][x] = self._cur[y - 1][x],\
                self._cur[y][x]
            self._emp = (x, y - 1)
        if move == 'u':
            self._movement = (0, -1 * self._speed)
            self._moving_tile = self._tiles[self._cur[y + 1][x]]
            self._cur[y][x], self._cur[y + 1][x] = self._cur[y + 1][x],\
                self._cur[y][x]
            self._emp = (x, y + 1)
        if move == 'r':
            self._movement = (self._speed, 0)
            self._moving_tile = self._tiles[self._cur[y][x - 1]]
            self._cur[y][x], self._cur[y][x - 1] = self._cur[y][x - 1],\
                self._cur[y][x]
            self._emp = (x - 1, y)
        if move == 'l':
            self._movement = (-1 * self._speed, 0)
            self._moving_tile = self._tiles[self._cur[y][x + 1]]
            self._cur[y][x], self._cur[y][x + 1] = self._cur[y][x + 1],\
                self._cur[y][x]
            self._emp = (x + 1, y)
        self._is_moving = True
        self._cur_move = move

    def _check_move(self, move):
        """Checks whether or not the move is valid"""

        if move not in 'udlr':
            raise RuntimeError("Unknown move:", move)
        if move == 'd' and self._emp[1] == 0 or\
                move == 'u' and self._emp[1] == self._n - 1 or\
                move == 'r' and self._emp[0] == 0 or\
                move == 'l' and self._emp[0] == self._n - 1:
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
        if not self._finished:
            self._scr.blit(self._cap_font.render(self._cur_move,
                                                 True, (255, 0, 0)),
                           (5, (self._tile_s + self._pad * 2) * self._n))
            self._scr.blit(self._font.render(''.join(self._solution[1:10]),
                                             True, (255, 255, 255)),
                           (30, (self._tile_s + self._pad * 2) * self._n + 9))
        else:
            self._scr.blit(self._cap_font.render("Solved", True, (255, 0, 0)),
                           (5, (self._tile_s + self._pad * 2) * self._n))

    def loop(self):
        """The main loop"""
        while True:
            # TODO change color
            self._scr.fill(pg.Color(0, 0, 0))
            if not self._finished:
                self._update()
            self._draw()
            pg.display.flip()
            self._clock.tick(self._FPS)
            if self._handler():
                break
