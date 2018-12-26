import pygame as pg


class Tile():

    """Rectangle with text"""

    def __init__(self, left, top, width, height, font, text):
        """Initializer for Rect_with_text
        """
        self._rect = pg.Rect(left, top, width, height)
        self._font = pg.font.SysFont('Arial', 25)
        self._text = str(text)

    def draw(self, surface, color):
        """Draws rectangle and text
        """
        pg.draw.rect(surface, color, self._rect)
        surface.blit(self._font.render(self._text, True, (255, 255, 255)),
                     (self._rect.left + 10, self._rect.top + 10))

    def move(self, x, y):
        """Moves the rectangle

        :x: TODO
        :y: TODO
        :returns: TODO

        """
        self._rect.move_ip(x, y)

    def get_n(self):
        """Returns tile's number"""
        return self._text
