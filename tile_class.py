import pygame
class Tile(object):
    def __init__(self, position_x, position_y, size, variant):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.variant = variant
        self.size = size
        if variant == 0:
            self.color = (50, 50, 60)
        if variant == 1:
            self.color = (200, 200, 210)
        if variant == 2:
            self.color = (200, 50, 60)
        if variant == 3:
            self.color = (50, 50, 210)
        if variant == 4:
            self.color = (250, 50, 60)
