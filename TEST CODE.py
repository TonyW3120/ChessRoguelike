import pygame
import math
from ship_class import Ship
from bullet_class import Bullet

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)

size = (800, 800)
screen = pygame.display.set_mode(size)

run = True
clock = pygame.time.Clock()
frame = 0
fps = 120

user_pos = [0, 0]
user_size = 50

home_point = (0, 0)
camera_pos = [300, 300]

scale_factor = 1
movement_speed = 1
collision_allowance = 2
collision = False
min_border_thickness = 1
mouse_current_position = [400, 400]

# Objects: test = Ship((pos_x, pos_x), size, (r, g, b))

object_1 = Ship((400, 400), 10, (255, 100, 100))
object_2 = Ship((200, 200), 50, (100, 255, 100))
object_list = [object_1, object_2]
bullet_list = []

#INCOMPLETE
def slope(position1, position2):
    slope_value = (position2[1] - position1[1])/(position2[0] - position1[0])
    return slope_value

while run:

    clock.tick(fps)
    screen.fill((0, 0, 0))

    my_font = pygame.font.SysFont('Arial', int(scale_factor * 20))

    camera_x_distance = home_point[0] - camera_pos[0]
    camera_y_distance = home_point[1] - camera_pos[1]

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.MOUSEMOTION:
            mouse_current_position = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                object_list.append(
                    Ship(((event.pos[0] / scale_factor) - camera_x_distance + (10 / 2) - (size[0] / 2) / scale_factor,
                          (event.pos[1] / scale_factor) - camera_y_distance + (10 / 2) - (size[1] / 2) / scale_factor),
                         10, (255, 100, 100)))

            if event.button == 3:
                object_list.append(
                    Ship(((event.pos[0] / scale_factor) - camera_x_distance + (10 / 2) - (size[0] / 2) / scale_factor,
                          (event.pos[1] / scale_factor) - camera_y_distance + (10 / 2) - (size[1] / 2) / scale_factor),
                         50, (100, 255, 100)))

        if event.type == pygame.KEYDOWN:
            if event.unicode == " ":
                if movement_speed == 1:
                    movement_speed = 3

                elif movement_speed == 3:
                    movement_speed = 1

                print(movement_speed)

            if event.unicode == "f":
                bullet_list.append(Bullet(((400 / scale_factor) - camera_x_distance + (10 / 2) - (size[0] / 2) / scale_factor,
                                          (400 / scale_factor) - camera_y_distance + (10 / 2) - (size[1] / 2) / scale_factor),
                                          5, (255, 255, 100), mouse_current_position))
                print(bullet_list)

        if event.type == pygame.MOUSEWHEEL:

            # zoom in
            if event.y == 1:
                scale_factor += 0.05

            # zoom out
            if event.y == -1:
                scale_factor += -0.05

        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    user = pygame.draw.rect(screen, (100, 100, 255),
        (scale_factor * (user_pos[0] - (user_size / 2)) + size[0] / 2,
         scale_factor * (user_pos[1] - (user_size / 2)) + size[1] / 2,
         scale_factor * user_size, scale_factor * user_size),
         max(int(10 * scale_factor), min_border_thickness))

    object_1_visual = 0

    for i in range(len(object_list)):
        object_list[i].visual = pygame.draw.rect(screen, object_list[i].color,
                                (scale_factor * ((object_list[i].position[0] + camera_x_distance) - (object_list[i].size / 2)) + size[0] / 2,
                                 scale_factor * ((object_list[i].position[1] + camera_y_distance) - (object_list[i].size / 2)) + size[1] / 2,
                                 scale_factor * object_list[i].size, scale_factor * object_list[i].size))

    for i in range(len(bullet_list)):
        bullet_list[i].visual = pygame.draw.rect(screen, bullet_list[i].color,
                                (scale_factor * ((bullet_list[i].position[0] + camera_x_distance) - (bullet_list[i].size / 2)) + size[0] / 2,
                                 scale_factor * ((bullet_list[i].position[1] + camera_y_distance) - (bullet_list[i].size / 2)) + size[1] / 2,
                                 scale_factor * bullet_list[i].size, scale_factor * bullet_list[i].size))

    # INCOMPLETE
    for i in range(len(bullet_list)):
        slope(bullet_list[i].position, bullet_list[i].target)

    collision_top = False
    collision_bottom = False
    collision_left = False
    collision_right = False

    for i in range(len(object_list)):
        if collision_bottom == False:
            collision_bottom = (pygame.Rect.colliderect(user, (
                object_list[i].visual[0],
                object_list[i].visual[1] + scale_factor * collision_allowance * movement_speed,
                object_list[i].visual[2], object_list[i].visual[2])))

        if collision_top == False:
            collision_top = (pygame.Rect.colliderect(user, (
                object_list[i].visual[0],
                object_list[i].visual[1] - scale_factor * collision_allowance * movement_speed,
                object_list[i].visual[2], object_list[i].visual[3])))

        if collision_left == False:
            collision_left = (pygame.Rect.colliderect(user, (
                object_list[i].visual[0] + scale_factor * collision_allowance * movement_speed,
                object_list[i].visual[1],
                object_list[i].visual[2], object_list[i].visual[3])))

        if collision_right == False:
            collision_right = (pygame.Rect.colliderect(user, (
                object_list[i].visual[0] - scale_factor * collision_allowance * movement_speed,
                object_list[i].visual[1],
                object_list[i].visual[2], object_list[i].visual[3])))

    if keys[pygame.K_w] and collision_bottom == False:
        camera_pos[1] += -movement_speed

    if keys[pygame.K_s] and collision_top == False:
        camera_pos[1] += movement_speed

    if keys[pygame.K_d] and collision_right == False:
        camera_pos[0] += movement_speed

    if keys[pygame.K_a] and collision_left == False:
        camera_pos[0] += -movement_speed

    frame += 1
    pygame.display.update()
