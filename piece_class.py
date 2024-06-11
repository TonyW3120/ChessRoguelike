import pygame

class Piece(object):
    def __init__(self, position_x, position_y, variant, tile):
        self.rect = 0
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.tile = tile
        self.variant = variant
        self.target = 0
        self.temp_tile = tile
        self.delta_x = 0
        self.delta_y = 0
        if variant == 0:
            self.size = (pygame.image.load("pawn_undamaged.png").get_size()[0]*3.5, pygame.image.load("pawn_undamaged.png").get_size()[1]*3.5)
            self.color = (70, 70, 80)
            self.health = 3

        if variant == 1:
            self.size = (pygame.image.load("knight_undamaged.png").get_size()[0]*3.5, pygame.image.load("knight_undamaged.png").get_size()[1]*3.5)
            self.color = (60, 60, 90)
            self.health = 10

        if variant == 2:
            self.size = (pygame.image.load("bishop_undamaged.png").get_size()[0]*3.5, pygame.image.load("bishop_undamaged.png").get_size()[1]*3.5)
            self.color = (60, 80, 70)
            self.health = 10

        if variant == 3:
            self.size = (pygame.image.load("rook_undamaged.png").get_size()[0]*3.5, pygame.image.load("rook_undamaged.png").get_size()[1]*3.5)
            self.color = (80, 60, 70)
            self.health = 20

        if variant == 4:
            self.size = (pygame.image.load("queen_undamaged.png").get_size()[0]*3.5, pygame.image.load("queen_undamaged.png").get_size()[1]*3.5)
            self.color = (70, 70, 80)
            self.health = 50

class Consumable(object):
    def __init__(self, position_x, position_y, size, variant, tile):
        self.rect = 0
        self.visual = 0
        self.position_x = position_x
        self.position_y = position_y
        self.tile = tile
        self.variant = variant
        self.pickup_timer = 0
        if variant == 0:
            self.improvement_quantity = 10 #additive
            self.improvement_attribute = 0 #health
            self.color = (150, 200, 150)
            self.image = pygame.image.load("health_item.png")
            self.size = (pygame.image.load("health_item.png").get_size()[0]*4,
                         pygame.image.load("health_item.png").get_size()[1]*4)

        if variant == 1:
            self.improvement_quantity = 1 #additive
            self.improvement_attribute = 1 #damage
            self.color = (200, 100, 100)
            self.image = pygame.image.load("damage_item.png")

        if variant == 2:
            self.improvement_quantity = 0.9 #multiplicative
            self.improvement_attribute = 2 #attack_speed
            self.color = (200, 150, 150)
            self.image = pygame.image.load("attack_speed_item.png")

        if variant == 3:
            self.improvement_quantity = 1 #additive, caps at 20
            self.improvement_attribute = 3 #movement_speed
            self.color = (150, 150, 200)
            self.image = pygame.image.load("movement_item.png")


        if variant == 4:
            self.improvement_quantity = 0.05 #additive, caps at 1
            self.improvement_attribute = 4 #critical_chance, crits do 200% damage
            self.color = (200, 100, 200)
            self.image = pygame.image.load("critical_item.png")

        if variant == 5:
            self.improvement_quantity = 0.05 #additive, caps 0.50
            self.improvement_attribute = 5 #dodge
            self.color = (200, 200, 100)
            self.image = pygame.image.load("dodge_item.png")

        self.size = (self.image.get_size()[0] * 4, self.image.get_size()[1] * 4)
