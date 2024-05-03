import pygame

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)

size = (800, 800)
screen = pygame.display.set_mode(size)

run = True
clock = pygame.time.Clock()
frame = 0
fps = 120
scale_factor = 1
object_pos = [0, 0]
object_2_pos = [400, 400]
object_3_pos = [200, 200]
home_point = (0, 0)
camera_pos = [300, 300]
movement_speed = 1
object_size = 50
object_2_size = 10
object_3_size = 100
collision_allowance = 3
collision = False
collision_bottom = False
min_border_thickness = 1

while run:

    clock.tick(fps)
    screen.fill((0, 0, 0))

    my_font = pygame.font.SysFont('Arial', int(scale_factor*20))

    camera_x_distance = home_point[0] - camera_pos[0]
    camera_y_distance = home_point[1] - camera_pos[1]

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.unicode == " ":
                print("test")
                if movement_speed == 1:
                    movement_speed = 3

                elif movement_speed == 3:
                    movement_speed = 1

                print(movement_speed)

        if event.type == pygame.MOUSEWHEEL:
            #zoom in
            if event.y == 1:
                scale_factor += 0.05

            # zoom out
            if event.y == -1:
                scale_factor += -0.05

        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    object = pygame.draw.rect(screen, (100, 100, 255),
                        (scale_factor * (object_pos[0] - (object_size/2)) + size[0] / 2,
                               scale_factor * (object_pos[1] - (object_size/2)) + size[1] / 2, scale_factor * object_size, scale_factor * object_size),
                               max(int(10 * scale_factor), min_border_thickness))

    object_2 = pygame.draw.rect(screen, (255, 100, 100),
                         (scale_factor * ((object_2_pos[0] + camera_x_distance) - (object_2_size/2)) + size[0] / 2,
                               scale_factor * ((object_2_pos[1] + camera_y_distance) - (object_size/2)) + size[1] / 2,
                               scale_factor * object_2_size, scale_factor * object_2_size))

    object_3 = pygame.draw.rect(screen, (100, 255, 100),
                         (scale_factor * ((object_3_pos[0] + camera_x_distance) - (object_3_size/2)) + size[0] / 2,
                               scale_factor * ((object_3_pos[1] + camera_y_distance) - (object_size/2)) + size[1] / 2,
                               scale_factor * object_3_size, scale_factor * object_3_size))

    collision_bottom = (pygame.Rect.colliderect(object, (object_2[0], object_2[1] + scale_factor * collision_allowance * movement_speed, object_2[2], object_2[3]))
                        or
                        pygame.Rect.colliderect(object, (object_3[0], object_3[1] + scale_factor * collision_allowance * movement_speed, object_3[2], object_3[3])))

    collision_top = (pygame.Rect.colliderect(object, (object_2[0], object_2[1] - scale_factor * collision_allowance * movement_speed, object_2[2], object_2[3]))
                     or
                     pygame.Rect.colliderect(object, (object_3[0], object_3[1] - scale_factor * collision_allowance * movement_speed, object_3[2], object_3[3])))

    collision_left = (pygame.Rect.colliderect(object, (object_2[0] + scale_factor * collision_allowance * movement_speed, object_2[1], object_2[2], object_2[3]))
                      or
                      pygame.Rect.colliderect(object, (object_3[0] + scale_factor * collision_allowance * movement_speed, object_3[1], object_3[2], object_3[3])))

    collision_right = (pygame.Rect.colliderect(object, (object_2[0] - scale_factor * collision_allowance * movement_speed, object_2[1], object_2[2], object_2[3]))
                       or
                       pygame.Rect.colliderect(object, (object_3[0] - scale_factor * collision_allowance * movement_speed, object_3[1], object_3[2], object_3[3])))


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