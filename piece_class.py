class Piece(object):
    def __init__(self, position_x, position_y, size, color, health, tile):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.color = color
        self.health = health
        self.tile = tile

    # def __init__(self, position_x, position_y, variant, tile):
    #     self.visual = 0
    #     self.position_x = position_x
    #     self.position_y = position_y
    #     self.tile = tile
    #     if variant == 0:
    #         self.size = 10
    #         self.color = (70, 70, 80)
    #         self.health = health
    #
    #     if variant == 1:
    #         self.size = 15
    #         self.color = (60, 60, 90)
    #         self.health = health
    #
    #     if variant == 2:
    #         self.size = 15
    #         self.color = (60, 80, 70)
    #         self.health = health
    #
    #     if variant == 3:
    #         self.size = 15
    #         self.color = (80, 60, 70)
    #         self.health = health
    #
    #     if variant == 4:
    #         self.size = 25
    #         self.color = (70, 70, 80)
    #         self.health = health


class Consumable(object):
    def __init__(self, position_x, position_y, size, variant, tile):
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.tile = tile
        self.variant = variant
        self.pickup_timer = 0
        if variant == 0:
            self.improvement_quantity = 10 #additive
            self.improvement_attribute = 0 #health
            self.color = (150, 200, 150)

        if variant == 1:
            self.improvement_quantity = 1 #additive
            self.improvement_attribute = 1 #damage
            self.color = (200, 100, 100)

        if variant == 2:
            self.improvement_quantity = 0.9 #multiplicative
            self.improvement_attribute = 2 #attack_speed
            self.color = (200, 150, 150)

        if variant == 3:
            self.improvement_quantity = 1 #additive, caps at 20
            self.improvement_attribute = 3 #movement_speed
            self.color = (150, 150, 200)

        if variant == 4:
            self.improvement_quantity = 0.05 #additive, caps at 1
            self.improvement_attribute = 4 #critical_chance, crits do 200% damage
            self.color = (200, 100, 200)

        if variant == 5:
            self.improvement_quantity = 0.05 #additive, caps 0.50
            self.improvement_attribute = 5 #dodge
            self.color = (200, 200, 100)
