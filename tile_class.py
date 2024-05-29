import pygame
class Tile(object):
    def __init__(self, position_x, position_y, size, variant):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.variant = variant
        self.size = size
        if variant == 0:
            self.color = (50, 50, 50)
        if variant == 1:
            self.color = (200, 50, 50)
