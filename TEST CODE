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
object_1_pos = [400, 400]
object_2_pos = [200, 200]
home_point = (0, 0)
camera_pos = [300, 300]
movement_speed = 1
user_size = 50
object_1_size = 10
object_2_size = 100
collision_allowance = 3
collision = False
min_border_thickness = 1

while run:

    clock.tick(fps)
    screen.fill((0, 0, 0))

    my_font = pygame.font.SysFont('Arial', int(scale_factor * 20))

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
                            (scale_factor * (object_pos[0] - (user_size / 2)) + size[0] / 2,
                             scale_factor * (object_pos[1] - (user_size / 2)) + size[1] / 2,
                             scale_factor * user_size, scale_factor * user_size),
                            max(int(10 * scale_factor), min_border_thickness))

    object_1_visual = 0

    object_1 = [object_1_visual, object_1_pos, object_1_size]

    object_2_visual = 0

    object_2 = [object_2_visual, object_2_pos, object_1_size]

    object_list = [object_1, object_2]

    for i in range(len(object_list)):
        object_list[i][0] = pygame.draw.rect(screen, (255, 100, 100),
                         (scale_factor * ((object_list[i][1][0] + camera_x_distance) - (object_list[i][2] / 2)) + size[0] / 2,
                          scale_factor * ((object_list[i][1][1] + camera_y_distance) - (user_size / 2)) + size[1] / 2,
                          scale_factor * object_list[i][2], scale_factor * object_list[i][2]))


    collision_top = False
    collision_bottom = False
    collision_left = False
    collision_right = False

    for i in range(len(object_list)):
        if collision_bottom == False:
            collision_bottom = (pygame.Rect.colliderect(user, (
            object_list[i][0], object_list[i][1] + scale_factor * collision_allowance * movement_speed,
            object_list[i][2], object_list[i][3])))

        if collision_top == False:
            collision_top = (pygame.Rect.colliderect(user, (
            object_list[i][0], object_list[i][1] - scale_factor * collision_allowance * movement_speed,
            object_list[i][2], object_list[i][3])))

        if collision_left == False:
            collision_left = (pygame.Rect.colliderect(user, (
            object_list[i][0] + scale_factor * collision_allowance * movement_speed, object_list[i][1],
            object_list[i][2], object_list[i][3])))

        if collision_right == False:
            collision_right = (pygame.Rect.colliderect(user, (
            object_list[i][0] - scale_factor * collision_allowance * movement_speed, object_list[i][1],
            object_list[i][2], object_list[i][3])))

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
