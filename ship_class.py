class Ship(object):
    def __init__(self, position_x, position_y, size, color, health):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.color = color
        self.health = health
