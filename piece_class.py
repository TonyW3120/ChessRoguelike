class Piece(object):
    def __init__(self, position_x, position_y, size, color, health):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.color = color
        self.health = health

class Consumable(object):
    def __init__(self, position_x, position_y, size, color, variant):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.color = color
        if variant == 0:
            self.improvement_quantity = 10 #additive
            self.improvement_attribute = 0 #health

        if variant == 1:
            self.improvement_quantity = 1 #additive
            self.improvement_attribute = 1 #damage

        if variant == 2:
            self.improvement_quantity = 0.9 #multiplicative
            self.improvement_attribute = 2 #attack_speed

        if variant == 3:
            self.improvement_quantity = 1 #additive, caps at 20
            self.improvement_attribute = 3 #movement_speed

        if variant == 4:
            self.improvement_quantity = 0.05 #additive, caps at 1
            self.improvement_attribute = 4 #critical_chance, crits do 200% damage

        if variant == 5:
            self.improvement_quantity = 0.05 #additive, caps 0.50
            self.improvement_attribute = 5 #dodge
