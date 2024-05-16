class Bullet(object):
    def __init__(self, position_x, position_y, size, color, target):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.color = color
        self.target = target
        self.delta_x = 0
        self.delta_y = 0
        self.course_set = False
        self.initial_scale_factor = 0
