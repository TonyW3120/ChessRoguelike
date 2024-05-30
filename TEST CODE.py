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

user_stats = [100, 1, 1, 1, 0, 0]
user_health = user_stats[0]
user_damage = user_stats[1]
user_attack_speed = user_stats[2]
user_movement_speed = user_stats[3]
user_critical_chance = user_stats[4]
user_dodge_chance = user_stats[5]


home_point = (0, 0)
camera_pos = [400, 400]

grid_square_size = 100
grid_size = 20
grid = []
grid_visual = []
grid_objects = []

scale_factor = 1
bullet_movement_speed = 3
collision_allowance = 2
collision = False
min_border_thickness = 1
mouse_current_position = [400, 400]
min_zoom_out = 0.5
max_zoom_out = 1.5


# Objects: test = Ship(pos_x, pos_x, size, (r, g, b), health)

object_1 = Piece(600, 600, 10, (255, 100, 100), 1)
object_2 = Piece(200, 200, 50, (100, 255, 100), 10)
piece_list = [object_1, object_2]
bullet_list = []
consumable_list = []

# Functions
def angle(position1, position2):
    angle = math.atan((position2[1] - position1[1])/(position2[0] - position1[0] + 0.0000001))
    return angle


def visual_position_modifier(position_x, position_y, camera_x_distance, camera_y_distance, screen_size, scale_factor):
    new_position = ((position_x / scale_factor) - camera_x_distance + (10 / 2) - (screen_size[0] / 2) / scale_factor,
                    (position_y / scale_factor) - camera_y_distance + (10 / 2) - (screen_size[1] / 2) / scale_factor)
    return new_position


def game_position_modifier(position_x, position_y, camera_x_distance, camera_y_distance, screen_size, object_size, scale_factor):
    new_position = (scale_factor * ((position_x + camera_x_distance) - (object_size / 2)) + screen_size[0] / 2,
                    scale_factor * ((position_y + camera_y_distance) - (object_size / 2)) + screen_size[1] / 2)
    return new_position

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

#INCOMPLETE, TRY TO ALIGN ENEMIES WITH GRID
for i in range(grid_size):
    grid_objects.append([])
    for j in range(grid_size):
        grid_objects[i].append([])



# Game start

while run:

    clock.tick(fps)
    # if frame == 75:
    #     print(camera_pos)
    #     print(mouse_current_position)

    if frame == fps + 1:
        frame = 1

    user_health = user_stats[0]
    user_damage = user_stats[1]
    user_attack_speed = user_stats[2]
    user_movement_speed = user_stats[3]
    user_critical_chance = user_stats[4]
    user_dodge_chance = user_stats[5]

    screen.fill((230, 230, 230))

    my_font = pygame.font.SysFont('Arial', int(scale_factor * 20))

    camera_x_distance = home_point[0] - camera_pos[0]
    camera_y_distance = home_point[1] - camera_pos[1]

    mouse_current_position = visual_position_modifier(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)
# EVENTS
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # FIX, DOESNT WORK WHEN MOVING
                piece_list.append(Piece(visual_position_modifier(round((event.pos[0]/grid_square_size), 0) * grid_square_size, round((event.pos[1]/grid_square_size), 0) * grid_square_size, camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                        visual_position_modifier(round((event.pos[0]/grid_square_size), 0) * grid_square_size, round((event.pos[1]/grid_square_size), 0) * grid_square_size, camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                        10, (255, 100, 100), 1))
            if event.button == 3:
                # FIX, DOESNT WORK WHEN MOVING
                piece_list.append(Piece(visual_position_modifier(round((event.pos[0]/grid_square_size), 0) * grid_square_size, round((event.pos[1]/grid_square_size), 0) * grid_square_size, camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                        visual_position_modifier(round((event.pos[0]/grid_square_size), 0) * grid_square_size, round((event.pos[1]/grid_square_size), 0) * grid_square_size, camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                        50, (100, 255, 100), 10))

            if event.button == 2:
                consumable_list.append(Consumable(visual_position_modifier(event.pos[0], event.pos[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                                  visual_position_modifier(event.pos[0], event.pos[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                                  20, (255, 200, 200), 0))

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

        if event.type == pygame.MOUSEWHEEL:
            if scale_factor <= max_zoom_out and event.y == 1:
                scale_factor += 0.05

            if scale_factor >= min_zoom_out and event.y == -1:
                scale_factor += -0.05

        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

# VISUALS
    user = pygame.draw.rect(screen, (100, 100, 255),
                            (scale_factor * (user_pos[0] - (user_size / 2)) + screen_size[0] / 2,
                             scale_factor * (user_pos[1] - (user_size / 2)) + screen_size[1] / 2,
                             scale_factor * user_size, scale_factor * user_size),
                            max(int(10 * scale_factor), min_border_thickness))

    for i in range(grid_size):
        for j in range(grid_size):
            grid_visual[i][j].visual = pygame.draw.rect(screen, grid_visual[i][j].color,
                           (game_position_modifier(grid_visual[i][j].position_x, grid_visual[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_visual[i][j].size, scale_factor)[0],
                            game_position_modifier(grid_visual[i][j].position_x, grid_visual[i][j].position_y, camera_x_distance, camera_y_distance, screen_size, grid_visual[i][j].size, scale_factor)[1],
                           (scale_factor * grid_visual[i][j].size) + int(round(2*scale_factor, 0)), (scale_factor * grid_visual[i][j].size) + int(round(2*scale_factor, 0))))

    for i in range(grid_size):
        for j in range(grid_size):
            if user.colliderect(grid_visual[i][j].visual):
                grid_visual[i][j] = (Tile((screen_size[0]/2 - (grid_square_size * grid_size) / 2) + j * grid_square_size,
                                          (screen_size[1]/2 - (grid_square_size * grid_size) / 2) + i * grid_square_size,
                                          grid_square_size, 2))
            if (i + j)%2 == 0:
                grid_visual[i][j] = (Tile((screen_size[0] / 2 - (grid_square_size * grid_size) / 2) + j * grid_square_size,
                                    (screen_size[1] / 2 - (grid_square_size * grid_size) / 2) + i * grid_square_size,
                                    grid_square_size, 1))
            else:
                grid_visual[i][j] = (Tile((screen_size[0]/2 - (grid_square_size * grid_size) / 2) + j * grid_square_size,
                                          (screen_size[1]/2 - (grid_square_size * grid_size) / 2) + i * grid_square_size,
                                          grid_square_size, 0))

    while len(piece_list) != 0:
        for i in range(len(piece_list)):
            if piece_list[i].health <= 0:
                piece_list.pop(i)
                break
            else:
                continue
        break

    for i in range(len(piece_list)):
        piece_list[i].visual = pygame.draw.rect(screen, piece_list[i].color,
                                               (game_position_modifier(piece_list[i].position_x, piece_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, piece_list[i].size, scale_factor)[0],
                                                game_position_modifier(piece_list[i].position_x, piece_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, piece_list[i].size, scale_factor)[1],
                                                scale_factor * piece_list[i].size, scale_factor * piece_list[i].size))

    for i in range(len(bullet_list)):
        bullet_list[i].visual = pygame.draw.rect(screen, bullet_list[i].color,
                                                (game_position_modifier(bullet_list[i].position_x, bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, bullet_list[i].size, scale_factor)[0],
                                                 game_position_modifier(bullet_list[i].position_x, bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, bullet_list[i].size, scale_factor)[1],
                                                 scale_factor * bullet_list[i].size, scale_factor * bullet_list[i].size))

    for i in range(len(consumable_list)):
        consumable_list[i].visual = pygame.draw.rect(screen, consumable_list[i].color,
                                                    (game_position_modifier(consumable_list[i].position_x, consumable_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, consumable_list[i].size, scale_factor)[0],
                                                     game_position_modifier(consumable_list[i].position_x, consumable_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, consumable_list[i].size, scale_factor)[1],
                                                     scale_factor * consumable_list[i].size, scale_factor * consumable_list[i].size))

    user = pygame.draw.rect(screen, (100, 100, 255),
        (scale_factor * (user_pos[0] - (user_size / 2)) + screen_size[0] / 2,
         scale_factor * (user_pos[1] - (user_size / 2)) + screen_size[1] / 2,
         scale_factor * user_size, scale_factor * user_size),
         max(int(10*scale_factor), min_border_thickness))

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
            if round(bullet_list[i].position_x, 0) == round(bullet_list[i].target[0], 0) and round(bullet_list[i].position_y, 0) == round(bullet_list[i].target[1], 0):
                bullet_list.pop(i)
                break
            else:
                continue

    for i in range(len(consumable_list)):
        if pygame.Rect.colliderect(user, consumable_list[i].visual):
            user_stats[consumable_list[i].improvement_attribute] += consumable_list[i].improvement_quantity
            consumable_list.pop(i)
            print(user_stats)
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
                piece_list[i].visual[0],
                piece_list[i].visual[1] + scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].visual[2], piece_list[i].visual[2])))

        if not collision_top:
            collision_top = (pygame.Rect.colliderect(user, (
                piece_list[i].visual[0],
                piece_list[i].visual[1] - scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].visual[2], piece_list[i].visual[3])))

        if not collision_left:
            collision_left = (pygame.Rect.colliderect(user, (
                piece_list[i].visual[0] + scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].visual[1],
                piece_list[i].visual[2], piece_list[i].visual[3])))

        if not collision_right:
            collision_right = (pygame.Rect.colliderect(user, (
                piece_list[i].visual[0] - scale_factor * collision_allowance * user_movement_speed,
                piece_list[i].visual[1],
                piece_list[i].visual[2], piece_list[i].visual[3])))

    if keys[pygame.K_w] and not collision_bottom:
        camera_pos[1] += -user_movement_speed

    if keys[pygame.K_s] and not collision_top:
        camera_pos[1] += user_movement_speed

    if keys[pygame.K_d] and not collision_right:
        camera_pos[0] += user_movement_speed

    if keys[pygame.K_a] and not collision_left:
        camera_pos[0] += -user_movement_speed

    frame += 1
    pygame.display.update()
