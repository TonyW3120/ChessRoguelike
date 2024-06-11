import random
import pygame
import math
import time
from piece_class import Piece
from piece_class import Consumable
from bullet_class import Bullet
from tile_class import Tile

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)

screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)

run = True
clock = pygame.time.Clock()
frame = 0
fps = 75

user_pos = [0, 0]
user_size = 50
user_cannon_1_position = (400, 400)
user_last_fired = 0

user_stats = [100, 1, 1, 1, 0, 0, 100]
user_max_health = user_stats[0]
user_damage = user_stats[1]
user_attack_speed = user_stats[2]
user_movement_speed = user_stats[3]
user_critical_chance = user_stats[4]
user_dodge_chance = user_stats[5]
user_health = user_stats[6]

user_regen_timer = time.time()
user_regen_time = 10

home_point = (0, 0)
camera_pos = [400, 400]

grid_square_size = 100
grid_size = 8
grid = []
grid_visual = []
grid_objects = []

#1 - 100, number refers to percentage
consumable_drop_rate = 100

scale_factor = 1
bullet_movement_speed = 3
collision_allowance = 2
collision = False
min_border_thickness = 1
mouse_current_position = [400, 400]
min_zoom_out = 0.5
max_zoom_out = 1.5
enemy_movement_cooldown = 3
enemy_movement_timer = 0

# Objects: test = Ship(pos_x, pos_x, size, (r, g, b), health)

piece_list = []
bullet_list = []
consumable_list = []
movement_weight_list = []
damage_source_tiles = []
selected_tile = (0, 0)


# Functions
def angle(position1, position2):
    angle = math.atan((position2[1] - position1[1]) / (position2[0] - position1[0] + 0.0000001))
    return angle


def visual_position_modifier(position_x, position_y, camera_x_distance, camera_y_distance, screen_size, scale_factor):
    new_position = ((position_x / scale_factor) - camera_x_distance + (10 / 2) - (screen_size[0] / 2) / scale_factor,
                    (position_y / scale_factor) - camera_y_distance + (10 / 2) - (screen_size[1] / 2) / scale_factor)
    return new_position


def game_position_modifier(position_x, position_y, camera_x_distance, camera_y_distance, screen_size, object_size, scale_factor):
    new_position = (scale_factor * ((position_x + camera_x_distance) - (object_size / 2)) + screen_size[0] / 2,
                    scale_factor * ((position_y + camera_y_distance) - (object_size / 2)) + screen_size[1] / 2)
    return new_position

def pawn_movement_search(list, position):
    max_value = float('-inf')
    max_index = None

    for i in range(position[1] - 1, position[1] + 2):
        for j in range(position[0] - 1, position[0] + 2):
            if 0 <= i < len(list) and 0 <= j < len(list[0]):
                if list[i][j] > max_value:
                    max_value = list[i][j]
                    max_index = (i - 1, j - 1)

    return max_index

# Grid creation
for i in range(grid_size):
    grid.append([])
    for j in range(grid_size):
        grid[i].append([])

for i in range(grid_size):
    grid_visual.append([])
    for j in range(grid_size):
        grid_visual[i].append([])

for i in range(grid_size):
    for j in range(grid_size):
        grid_visual[i][j] = (Tile((screen_size[0] - (grid_square_size * grid_size) / 2) + j * grid_square_size,
                                  (screen_size[1] - (grid_square_size * grid_size) / 2) + i * grid_square_size,
                                  grid_square_size, 0))

for i in range(grid_size):
    grid_objects.append([])
    for j in range(grid_size):
        grid_objects[i].append([])

for i in range(grid_size + 2):
    movement_weight_list.append([])
    for j in range(grid_size + 2):
        movement_weight_list[i].append(0.0)

# Game start

while run:

    clock.tick(fps)
    if frame == 75:
        enemy_movement_timer += 1

    if frame == fps + 1:
        frame = 1

    user_max_health = user_stats[0]
    user_damage = user_stats[1]
    user_attack_speed = user_stats[2]
    user_movement_speed = user_stats[3]
    user_critical_chance = user_stats[4]
    user_dodge_chance = user_stats[5]
    user_health = user_stats[6]

    screen.fill((230, 230, 230))

    my_font = pygame.font.SysFont('Arial', int(scale_factor * 20))

    camera_x_distance = home_point[0] - camera_pos[0]
    camera_y_distance = home_point[1] - camera_pos[1]

    mouse_current_position = visual_position_modifier(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)
    mouse_hitbox = pygame.Rect(int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1]), 1, 1)

    if time.time() - user_regen_timer > user_regen_time and user_max_health > user_health:
        user_stats[6] += 0.05

    # EVENT
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2 and grid_objects[selected_tile[0]][selected_tile[1]] == []:
                grid_objects[selected_tile[0]][selected_tile[1]] = (Consumable((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                                                               (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                                                               20, 0, (selected_tile[0], selected_tile[1])))

                consumable_list.append(Consumable((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                                  (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                                  20, 0, (selected_tile[0], selected_tile[1])))

        if event.type == pygame.KEYDOWN:
            if event.unicode == " ":
                if user_movement_speed == 1:
                    user_stats[3] = 3

                elif user_movement_speed == 3:
                    user_stats[3] = 1

            if event.unicode == "f" and time.time() - user_last_fired >= user_attack_speed:
                user_last_fired = time.time()
                bullet_list.append(Bullet(visual_position_modifier(400, 400, camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                          visual_position_modifier(400, 400, camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                          5, (255, 255, 100), mouse_current_position))

                if bullet_list[-1].target[0] < bullet_list[-1].position_x:
                    bullet_list[-1].delta_x = -math.cos(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                    bullet_list[-1].delta_y = -math.sin(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                else:
                    bullet_list[-1].delta_x = math.cos(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                    bullet_list[-1].delta_y = math.sin(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))

            # PAWN
            if event.unicode == "1" and grid_objects[selected_tile[0]][selected_tile[1]] == []:
                grid_objects[selected_tile[0]][selected_tile[1]] = (Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                                                          0, (selected_tile[0], selected_tile[1])))

                piece_list.append(Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                        (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                        0, (selected_tile[0], selected_tile[1])))

            # KNIGHT
            if event.unicode == "2" and grid_objects[selected_tile[0]][selected_tile[1]] == []:
                grid_objects[selected_tile[0]][selected_tile[1]] = (Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                                                          1, (selected_tile[0], selected_tile[1])))

                piece_list.append(Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                        (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                        1, (selected_tile[0], selected_tile[1])))

            # BISHOP
            if event.unicode == "3" and grid_objects[selected_tile[0]][selected_tile[1]] == []:
                grid_objects[selected_tile[0]][selected_tile[1]] = (Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                                                          2, (selected_tile[0], selected_tile[1])))

                piece_list.append(Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                        (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                        2, (selected_tile[0], selected_tile[1])))

            # ROOK
            if event.unicode == "4" and grid_objects[selected_tile[0]][selected_tile[1]] == []:
                grid_objects[selected_tile[0]][selected_tile[1]] = (Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                                                          3, (selected_tile[0], selected_tile[1])))

                piece_list.append(Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                        (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                        3, (selected_tile[0], selected_tile[1])))

            # QUEEN
            if event.unicode == "5" and grid_objects[selected_tile[0]][selected_tile[1]] == []:
                grid_objects[selected_tile[0]][selected_tile[1]] = (Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                                                          4, (selected_tile[0], selected_tile[1])))

                piece_list.append(Piece((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[1] + 0.5) * grid_square_size,
                                        (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (selected_tile[0] + 0.5) * grid_square_size,
                                        4, (selected_tile[0], selected_tile[1])))


        if event.type == pygame.MOUSEWHEEL:
            if scale_factor <= max_zoom_out and event.y == 1:
                scale_factor += 0.05

            if scale_factor >= min_zoom_out and event.y == -1:
                scale_factor += -0.05

        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # VISUALS
    if user_health/user_max_health >= 0.8:
        user_image = pygame.image.load("king_undamaged.png")
    if 0.8 >= user_health/user_max_health >= 0.3:
        user_image = pygame.image.load("king_damaged.png")
    if user_health/user_max_health <= 0.3:
        user_image = pygame.image.load("king_heavily_damaged.png")
    user_image = pygame.transform.scale(user_image, (user_image.get_size()[0]*3.5*scale_factor, user_image.get_size()[1]*3.5*scale_factor))
    user_size = user_image.get_size()

    user = pygame.Rect(scale_factor * (user_pos[0] - (user_size[0] / 2)/scale_factor) + screen_size[0] / 2,
                       scale_factor * (user_pos[1] - (user_size[1] / 2)/scale_factor) + screen_size[1] / 2,
                       scale_factor * user_size[0], scale_factor * user_size[1])


    for i in range(grid_size):
        for j in range(grid_size):
            grid_visual[i][j].visual = pygame.draw.rect(screen, grid_visual[i][j].color,
                                                        (game_position_modifier(grid_visual[i][j].position_x, grid_visual[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_visual[i][j].size, scale_factor)[0],
                                                         game_position_modifier(grid_visual[i][j].position_x, grid_visual[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_visual[i][j].size, scale_factor)[1],
                                                         (scale_factor * grid_visual[i][j].size) + int(round(2 * scale_factor, 0)), (scale_factor * grid_visual[i][j].size) + int(round(2 * scale_factor, 0))))

    for i in range(grid_size):
        for j in range(grid_size):
            if user.colliderect(grid_visual[i][j].visual):
                user_grid_position = (i, j)

            if mouse_hitbox.colliderect(grid_visual[i][j].visual):
                grid_visual[i][j] = (Tile((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (j+0.5) * grid_square_size,
                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (i+0.5) * grid_square_size,
                                          grid_square_size, 3))

                grid_visual[i][j].visual = pygame.draw.rect(screen, grid_visual[i][j].color,
                                                            (game_position_modifier(grid_visual[i][j].position_x, grid_visual[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_visual[i][j].size, scale_factor)[0],
                                                             game_position_modifier(grid_visual[i][j].position_x, grid_visual[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_visual[i][j].size, scale_factor)[1],
                                                             (scale_factor * grid_visual[i][j].size) + int(round(2 * scale_factor, 0)), (scale_factor * grid_visual[i][j].size) + int(round(2 * scale_factor, 0))))

                selected_tile = (i, j)

            elif (i + j) % 2 == 0:
                grid_visual[i][j] = (Tile((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (j+0.5) * grid_square_size,
                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (i+0.5) * grid_square_size,
                                          grid_square_size, 1))
            else:
                grid_visual[i][j] = (Tile((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (j+0.5) * grid_square_size,
                                          (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (i+0.5) * grid_square_size,
                                          grid_square_size, 0))

    for i in range(len(damage_source_tiles)):
        grid_visual[damage_source_tiles[i][0]][damage_source_tiles[i][1]] = (Tile((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (damage_source_tiles[i][1] + 0.5) * grid_square_size,
                                                                            (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (damage_source_tiles[i][0] + 0.5) * grid_square_size,
                                                                            grid_square_size, 4))

#IDK WHY IT WORKS WHEN I DELETE THIS CODE
    # for i in range(grid_size):
    #     for j in range(grid_size):
    #         if grid_objects[i][j]:
    #             grid_objects[i][j].visual = (game_position_modifier(grid_objects[i][j].position_x, grid_objects[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_objects[i][j].size[0], scale_factor)[0],
    #                                       game_position_modifier(grid_objects[i][j].position_x, grid_objects[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_objects[i][j].size[1], scale_factor)[1],
    #                                       scale_factor * grid_objects[i][j].size[0], scale_factor * grid_objects[i][j].size[1])

    #Enemy Death
    while len(piece_list) != 0:
        for i in range(len(piece_list)):
            if piece_list[i].health <= 0:
                if random.randint(0, 100) <= consumable_drop_rate:
                    grid_objects[piece_list[i].tile[0]][piece_list[i].tile[1]] = Consumable((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (piece_list[i].tile[1] + 0.5) * grid_square_size,
                                                                                            (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (piece_list[i].tile[0] + 0.5) * grid_square_size,
                                                                                            20, random.randint(0, 5), (piece_list[i].tile[0], piece_list[i].tile[1]))

                    consumable_list.append(Consumable((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + (piece_list[i].tile[1] + 0.5) * grid_square_size,
                                                      (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + (piece_list[i].tile[0] + 0.5) * grid_square_size,
                                                      20, grid_objects[piece_list[i].tile[0]][piece_list[i].tile[1]].variant, (piece_list[i].tile[0], piece_list[i].tile[1])))

                else:
                    grid_objects[piece_list[i].tile[0]][piece_list[i].tile[1]] = []
                piece_list.pop(i)

                break
            else:
                continue
        break

    for i in range(len(piece_list)):
        piece_list[i].rect = pygame.Rect((game_position_modifier(piece_list[i].position_x, piece_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, piece_list[i].size[0], scale_factor)[0],
                                          game_position_modifier(piece_list[i].position_x, piece_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, piece_list[i].size[1], scale_factor)[1],
                                          scale_factor * piece_list[i].size[0], scale_factor * piece_list[i].size[1]))

        if piece_list[i].variant == 0:
            if piece_list[i].health == 3:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("pawn_undamaged.png"),
                                                                          (piece_list[i].size[0]*scale_factor, piece_list[i].size[1]*scale_factor)), piece_list[i].rect)
            elif piece_list[i].health == 2:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("pawn_damaged.png"),
                                                                          (piece_list[i].size[0]*scale_factor, piece_list[i].size[1]*scale_factor)), piece_list[i].rect)
            else:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("pawn_heavily_damaged.png"),
                                                                          (piece_list[i].size[0] * scale_factor,
                                                                           piece_list[i].size[1] * scale_factor)),
                                                   piece_list[i].rect)

        if piece_list[i].variant == 1:
            if piece_list[i].health > 7:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("knight_undamaged.png"),
                                                                          (piece_list[i].size[0] * scale_factor,
                                                                           piece_list[i].size[1] * scale_factor)),
                                                   piece_list[i].rect)
            elif piece_list[i].health > 4:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("knight_damaged.png"),
                                                                          (piece_list[i].size[0] * scale_factor,
                                                                           piece_list[i].size[1] * scale_factor)),
                                                   piece_list[i].rect)
            else:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("knight_heavily_damaged.png"),
                                                                          (piece_list[i].size[0]*scale_factor, piece_list[i].size[1]*scale_factor)), piece_list[i].rect)

        if piece_list[i].variant == 2:
            if piece_list[i].health > 7:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("bishop_undamaged.png"),
                                                                          (piece_list[i].size[0] * scale_factor,
                                                                           piece_list[i].size[1] * scale_factor)),
                                                   piece_list[i].rect)

            elif piece_list[i].health > 4:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("bishop_damaged.png"),
                                                                          (piece_list[i].size[0]*scale_factor, piece_list[i].size[1]*scale_factor)), piece_list[i].rect)
            else:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("bishop_heavily_damaged.png"),
                                                                          (piece_list[i].size[0] * scale_factor,
                                                                           piece_list[i].size[1] * scale_factor)),
                                                   piece_list[i].rect)

        if piece_list[i].variant == 3:
            if piece_list[i].health > 15:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("rook_undamaged.png"),
                                                                          (piece_list[i].size[0]*scale_factor, piece_list[i].size[1]*scale_factor)), piece_list[i].rect)
            elif piece_list[i].health > 7:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("rook_damaged.png"),
                                                                          (piece_list[i].size[0]*scale_factor, piece_list[i].size[1]*scale_factor)), piece_list[i].rect)
            else:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("rook_heavily_damaged.png"),
                                                                          (piece_list[i].size[0]*scale_factor, piece_list[i].size[1]*scale_factor)), piece_list[i].rect)

        if piece_list[i].variant == 4:
            if piece_list[i].health > 15:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("queen_undamaged.png"),
                                                   (pygame.image.load("queen_undamaged.png").get_size()[0]*4*scale_factor, pygame.image.load("queen_undamaged.png").get_size()[1]*4*scale_factor)),
                                                   piece_list[i].rect)
            elif piece_list[i].health > 7:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("queen_damaged.png"),
                                                   (pygame.image.load("queen_damaged.png").get_size()[0] * 4 * scale_factor, pygame.image.load("queen_damaged.png").get_size()[1] * 4 * scale_factor)),
                                                   piece_list[i].rect)
            else:
                piece_list[i].visual = screen.blit(pygame.transform.scale(pygame.image.load("queen_heavily_damaged.png"),
                                                   (pygame.image.load("queen_heavily_damaged.png").get_size()[0]*4*scale_factor, pygame.image.load("queen_heavily_damaged.png").get_size()[1]*4*scale_factor)),
                                                   piece_list[i].rect)

    for i in range(len(bullet_list)):
        bullet_list[i].visual = pygame.draw.rect(screen, bullet_list[i].color,
                                                 (game_position_modifier(bullet_list[i].position_x, bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, bullet_list[i].size, scale_factor)[0],
                                                  game_position_modifier(bullet_list[i].position_x, bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, bullet_list[i].size, scale_factor)[1],
                                                  scale_factor * bullet_list[i].size, scale_factor * bullet_list[i].size))

    for i in range(len(consumable_list)):
        consumable_list[i].rect = pygame.Rect(game_position_modifier(consumable_list[i].position_x, consumable_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, consumable_list[i].size[0], scale_factor)[0],
                                              game_position_modifier(consumable_list[i].position_x, consumable_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, consumable_list[i].size[1], scale_factor)[1],
                                              scale_factor * consumable_list[i].size[0], scale_factor * consumable_list[i].size[1])

        consumable_list[i].visual = screen.blit(pygame.transform.scale(consumable_list[i].image, (consumable_list[i].size[0]*scale_factor, consumable_list[i].size[1]*scale_factor)), consumable_list[i].rect)

    screen.blit(user_image, user)

    pygame.draw.line(screen, (50, 150, 50), (400, 400), game_position_modifier(mouse_current_position[0], mouse_current_position[1], camera_x_distance, camera_y_distance, screen_size, 0, scale_factor))

    # MOVEMENT AND COLLISION
    bullet_collision_occurred = False
    for h in range(bullet_movement_speed):
        for i in range(len(bullet_list)):
            bullet_list[i].position_x += bullet_list[i].delta_x
            bullet_list[i].position_y += bullet_list[i].delta_y
            for j in range(len(piece_list)):
                if pygame.Rect.colliderect(bullet_list[i].visual, piece_list[j].visual):
                    piece_list[j].health -= 1
                    bullet_list.pop(i)
                    i -= 1
                    bullet_collision_occurred = True
                    break
                else:
                    continue
            if bullet_collision_occurred:
                break
            if bullet_list[i].position_x < (400 - (grid_size * grid_square_size / 2)) or bullet_list[i].position_x > (400 + (grid_size * grid_square_size / 2)) or \
               bullet_list[i].position_y < (400 - (grid_size * grid_square_size / 2)) or bullet_list[i].position_y > (400 + (grid_size * grid_square_size / 2)):
                bullet_list.pop(i)
                break
            else:
                continue

    for i in range(len(consumable_list)):
        if pygame.Rect.colliderect(user, consumable_list[i].visual):
            if consumable_list[i].variant != 2:
                user_stats[consumable_list[i].improvement_attribute] += consumable_list[i].improvement_quantity
            else:
                user_stats[consumable_list[i].improvement_attribute] *= consumable_list[i].improvement_quantity

            grid_objects[consumable_list[i].tile[0]][consumable_list[i].tile[1]] = []
            consumable_list.pop(i)
            print(user_stats)
            i -= 1
            break
        else:
            continue

    for i in range(len(consumable_list)):
        consumable_list[i].pickup_timer += 1
        if consumable_list[i].pickup_timer == 10*fps:
            grid_objects[consumable_list[i].tile[0]][consumable_list[i].tile[1]] = []
            consumable_list.pop(i)
            i -= 1
            break
        else:
            continue

    collision_top = False
    collision_bottom = False
    collision_left = False
    collision_right = False


    for i in range(len(piece_list)):
        if not collision_bottom:
            collision_bottom = (pygame.Rect.colliderect(user, (
                piece_list[i].rect[0],
                piece_list[i].rect[1] + scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].rect[2], piece_list[i].rect[3])))


        if not collision_top:
            collision_top = (pygame.Rect.colliderect(user, (
                piece_list[i].rect[0],
                piece_list[i].rect[1] - scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].rect[2], piece_list[i].rect[3])))


        if not collision_left:
            collision_left = (pygame.Rect.colliderect(user, (
                piece_list[i].rect[0] + scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].rect[1],
                piece_list[i].rect[2], piece_list[i].rect[3])))


        if not collision_right:
            collision_right = (pygame.Rect.colliderect(user, (
                piece_list[i].rect[0] - scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].rect[1],
                piece_list[i].rect[2], piece_list[i].rect[3])))


    if keys[pygame.K_w] and not collision_bottom:
        camera_pos[1] += -user_movement_speed

    if keys[pygame.K_s] and not collision_top:
        camera_pos[1] += user_movement_speed

    if keys[pygame.K_d] and not collision_right:
        camera_pos[0] += user_movement_speed

    if keys[pygame.K_a] and not collision_left:
        camera_pos[0] += -user_movement_speed

    for i in range(grid_size):
        for j in range(grid_size):
            movement_weight_list[i + 1][j + 1] = round(10 - math.sqrt(((user_grid_position[0] - i)**2) + ((user_grid_position[1] - j)**2)), 1)

    # if enemy_movement_timer == enemy_movement_cooldown:
    #     enemy_movement_timer = 0
    #     for i in range(grid_size+2):
    #         print(movement_weight_list[i])
    #     print("")

    if enemy_movement_timer == enemy_movement_cooldown:
        enemy_movement_timer = 0
        damage_source_tiles = []
        for i in range(len(piece_list)):
            if piece_list[i].variant == 0:
                piece_list[i].temp_tile = piece_list[i].tile
                piece_list[i].target = pawn_movement_search(movement_weight_list, (piece_list[i].tile[1] + 1, piece_list[i].tile[0] + 1))
                piece_list[i].tile = pawn_movement_search(movement_weight_list, (piece_list[i].tile[1] + 1, piece_list[i].tile[0] + 1))

                piece_list[i].position_x = piece_list[i].tile[1] * grid_square_size + 50 * scale_factor
                piece_list[i].position_y = piece_list[i].tile[0] * grid_square_size + 50 * scale_factor

                piece_list[i].rect = pygame.Rect((game_position_modifier(piece_list[i].position_x, piece_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, piece_list[i].size[0], scale_factor)[0],
                                                  game_position_modifier(piece_list[i].position_x, piece_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, piece_list[i].size[1], scale_factor)[1],
                                                  scale_factor * piece_list[i].size[0], scale_factor * piece_list[i].size[1]))

                if pygame.Rect.colliderect(user, piece_list[i].rect):
                    user_stats[6] -= 10
                    user_regen_timer = time.time()
                    print(user_stats)

                    #FIX SCALE FACTOR
                    piece_list[i].position_x = piece_list[i].temp_tile[1] * grid_square_size + 50 * scale_factor
                    piece_list[i].position_y = piece_list[i].temp_tile[0] * grid_square_size + 50 * scale_factor

                    piece_list[i].tile = piece_list[i].temp_tile

                    damage_source_tiles.append(piece_list[i].tile)

                    movement_weight_list[piece_list[i].tile[0] + 1][piece_list[i].tile[1] + 1] = 0.0

                else:
                    movement_weight_list[piece_list[i].target[0] + 1][piece_list[i].target[1] + 1] = 0.0

    # for i in range(len(piece_list)):
    #     piece_list[i].tile = (math.floor((piece_list[i].position_y - 50)/grid_square_size), math.floor((piece_list[i].position_x - 50)/grid_square_size))
    #
    #     if piece_list[i].tile != piece_list[i].target and piece_list[i].target != 0:
    #         if piece_list[i].target[0] < piece_list[i].tile[1]:
    #             piece_list[i].delta_x = -math.cos(angle(piece_list[i].tile, piece_list[i].target))
    #             piece_list[i].delta_y = -math.sin(angle(piece_list[i].tile, piece_list[i].target))
    #         else:
    #             piece_list[i].delta_x = math.cos(angle(piece_list[i].tile, piece_list[i].target))
    #             piece_list[i].delta_y = math.sin(angle(piece_list[i].tile, piece_list[i].target))
    #
    # for i in range(len(piece_list)):
    #     if piece_list[i].tile != piece_list[i].target:
    #         piece_list[i].position_x += piece_list[i].delta_x * 5
    #         piece_list[i].position_y += piece_list[i].delta_y * 5


    frame += 1
    pygame.display.update()
