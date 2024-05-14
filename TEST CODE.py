import pygame
import math
import random
from ship_class import Ship
from bullet_class import Bullet

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

home_point = (0, 0)
camera_pos = [300, 300]

scale_factor = 1
movement_speed = 1
bullet_movement_speed = 3
collision_allowance = 2
collision = False
min_border_thickness = 1
mouse_current_position = [400, 400]
enemy_accuracy = 50

# Objects: test = Ship(pos_x, pos_x, size, (r, g, b))

object_1 = Ship(400, 400, 10, (255, 100, 100))
object_2 = Ship(200, 200, 50, (100, 255, 100))
object_list = [object_1, object_2]
bullet_list = []
enemy_bullet_list = []


def angle(position1, position2):
    # angle = math.degrees(math.atan(-((position2[1] - position1[1])/((position2[0] - position1[0]) + 0.0000001))))

    angle = math.atan((position2[1] - position1[1])/(position2[0] - position1[0] + 0.0000001))
    # angle = math.atan((position2[1] - position1[1]) / ((position2[0] - position1[0]) + 0.0000001))
    print("radians:", angle)
    if math.degrees(angle) < 0:
        print("degrees:", 360 + math.degrees(angle))
    else:
        print("degrees:", math.degrees(angle))
    print("")
    return angle


def visual_position_modifier(position_x, position_y, camera_x_distance, camera_y_distance, screen_size, scale_factor):
    new_position = ((position_x / scale_factor) - camera_x_distance + (10 / 2) - (screen_size[0] / 2) / scale_factor,
                    (position_y / scale_factor) - camera_y_distance + (10 / 2) - (screen_size[1] / 2) / scale_factor)
    return new_position


def game_position_modifier(position_x, position_y, camera_x_distance, camera_y_distance, screen_size, object_size, scale_factor):
    new_position = (scale_factor * ((position_x + camera_x_distance) - (object_size / 2)) + screen_size[0] / 2,
                    scale_factor * ((position_y + camera_y_distance) - (object_size / 2)) + screen_size[1] / 2)
    return new_position


while run:

    clock.tick(fps)
    # if frame == 75:
    #     print(camera_pos)
    #     print(mouse_current_position)

    if frame == fps + 1:
        frame = 1

    screen.fill((0, 0, 0))

    my_font = pygame.font.SysFont('Arial', int(scale_factor * 20))

    camera_x_distance = home_point[0] - camera_pos[0]
    camera_y_distance = home_point[1] - camera_pos[1]

    if frame == 75:
        for i in range(len(object_list)):
            enemy_bullet_list.append(Bullet(
                visual_position_modifier(object_list[i].visual[0], object_list[i].visual[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                visual_position_modifier(object_list[i].visual[0] , object_list[i].visual[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                5, (255, 255, 100), (camera_pos[0] + random.randint(-50, 50)*scale_factor, camera_pos[1] + random.randint(-50, 50)*scale_factor)))
            if enemy_bullet_list[-1].course_set == False:
                if enemy_bullet_list[-1].target[0] < enemy_bullet_list[-1].position_x:
                    enemy_bullet_list[-1].delta_x = -math.cos(
                        angle((enemy_bullet_list[-1].position_x, enemy_bullet_list[-1].position_y), enemy_bullet_list[-1].target))
                    enemy_bullet_list[-1].delta_y = -math.sin(
                        angle((enemy_bullet_list[-1].position_x, enemy_bullet_list[-1].position_y), enemy_bullet_list[-1].target))
                    enemy_bullet_list[-1].course_set = True
                else:
                    enemy_bullet_list[-1].delta_x = math.cos(
                        angle((enemy_bullet_list[-1].position_x, enemy_bullet_list[-1].position_y), enemy_bullet_list[-1].target))
                    enemy_bullet_list[-1].delta_y = math.sin(
                        angle((enemy_bullet_list[-1].position_x, enemy_bullet_list[-1].position_y), enemy_bullet_list[-1].target))
                    enemy_bullet_list[-1].course_set = True


    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_current_position = visual_position_modifier(event.pos[0], event.pos[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                object_list.append(Ship(visual_position_modifier(event.pos[0], event.pos[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                        visual_position_modifier(event.pos[0], event.pos[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                        10, (255, 100, 100)))

            if event.button == 3:
                object_list.append(Ship(visual_position_modifier(event.pos[0], event.pos[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                        visual_position_modifier(event.pos[0], event.pos[1], camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                        50, (100, 255, 100)))

        if event.type == pygame.KEYDOWN:
            if event.unicode == " ":
                if movement_speed == 1:
                    movement_speed = 3

                elif movement_speed == 3:
                    movement_speed = 1

            if event.unicode == "f":
                bullet_list.append(Bullet(visual_position_modifier(400, 410, camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                          visual_position_modifier(400, 410, camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                          5, (255, 255, 100), mouse_current_position))
                if bullet_list[-1].target[0] < bullet_list[-1].position_x:
                    bullet_list[-1].delta_x = -math.cos(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                    bullet_list[-1].delta_y = -math.sin(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                else:
                    bullet_list[-1].delta_x = math.cos(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                    bullet_list[-1].delta_y = math.sin(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))

                bullet_list.append(Bullet(visual_position_modifier(400, 380, camera_x_distance, camera_y_distance, screen_size, scale_factor)[0],
                                          visual_position_modifier(400, 380, camera_x_distance, camera_y_distance, screen_size, scale_factor)[1],
                                          5, (255, 255, 100), mouse_current_position))
                if bullet_list[-1].target[0] < bullet_list[-1].position_x:
                    bullet_list[-1].delta_x = -math.cos(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                    bullet_list[-1].delta_y = -math.sin(angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                else:
                    bullet_list[-1].delta_x = math.cos(
                        angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))
                    bullet_list[-1].delta_y = math.sin(
                        angle((bullet_list[-1].position_x, bullet_list[-1].position_y), bullet_list[-1].target))

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
        (scale_factor * (user_pos[0] - (user_size / 2)) + screen_size[0] / 2,
         scale_factor * (user_pos[1] - (user_size / 2)) + screen_size[1] / 2,
         scale_factor * user_size, scale_factor * user_size),
         max(int(10 * scale_factor), min_border_thickness))

    for i in range(len(object_list)):
        object_list[i].visual = pygame.draw.rect(screen, object_list[i].color,
                           (game_position_modifier(object_list[i].position_x,object_list[i].position_x, camera_x_distance, camera_y_distance, screen_size, object_list[i].size, scale_factor)[0],
                                 game_position_modifier(object_list[i].position_x,object_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, object_list[i].size, scale_factor)[1],
                                 scale_factor * object_list[i].size, scale_factor * object_list[i].size))

    for i in range(len(bullet_list)):
        bullet_list[i].visual = pygame.draw.rect(screen, bullet_list[i].color,
                           (game_position_modifier(bullet_list[i].position_x, bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, bullet_list[i].size, scale_factor)[0],
                                 game_position_modifier(bullet_list[i].position_x, bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, bullet_list[i].size, scale_factor)[1],
                                 scale_factor * bullet_list[i].size, scale_factor * bullet_list[i].size))

    for i in range(len(enemy_bullet_list)):
        enemy_bullet_list[i].visual = pygame.draw.rect(screen, enemy_bullet_list[i].color,
                           (game_position_modifier(enemy_bullet_list[i].position_x, enemy_bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, enemy_bullet_list[i].size, scale_factor)[0],
                                 game_position_modifier(enemy_bullet_list[i].position_x, enemy_bullet_list[i].position_y, camera_x_distance, camera_y_distance, screen_size, enemy_bullet_list[i].size, scale_factor)[1],
                                 scale_factor * enemy_bullet_list[i].size, scale_factor * enemy_bullet_list[i].size))

    #DEBUG
    for h in range(bullet_movement_speed):
        for i in range(len(enemy_bullet_list)):
            enemy_bullet_list[i].position_x += enemy_bullet_list[i].delta_x
            enemy_bullet_list[i].position_y += enemy_bullet_list[i].delta_y
            if round(enemy_bullet_list[i].position_x, 0) == round(enemy_bullet_list[i].target[0], 0) and round(enemy_bullet_list[i].position_y, 0) == round(enemy_bullet_list[i].target[1], 0):
                enemy_bullet_list.pop(i)
                break
            else:
                continue

    bullet_collision_occurred = False
    for h in range(bullet_movement_speed):
        for i in range(len(bullet_list)):
            bullet_list[i].position_x += bullet_list[i].delta_x
            bullet_list[i].position_y += bullet_list[i].delta_y
            for j in range(len(object_list)):
                if pygame.Rect.colliderect(bullet_list[i].visual, object_list[j].visual) == True:
                    object_list.pop(j)
                    bullet_list.pop(i)
                    i -= 1
                    print(i)
                    bullet_collision_occurred = True
                    break
                else:
                    continue
                break
            if bullet_collision_occurred:
                break
            if round(bullet_list[i].position_x, 0) == round(bullet_list[i].target[0], 0) and round(bullet_list[i].position_y, 0) == round(bullet_list[i].target[1], 0):
                bullet_list.pop(i)
                break
            else:
                continue

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
