import sys, pygame, cv2
import numpy as np
import math
from image_map import image_map

cells_per_side = 2 ** 10
total_cells = cells_per_side ** 2
zoom = 1.35
pixels_per_side = int(cells_per_side * zoom)
black = 0, 0, 0
space = False
running = True

image_index = 6  # max == 10
img_data = image_map[image_index]

img = cv2.imread(img_data['image'])
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (cells_per_side, cells_per_side))

screen = pygame.display.set_mode((pixels_per_side,pixels_per_side), pygame.RESIZABLE)
screen.fill(black)

color_array = np.load(img_data['color_arr'])
coordinate_array = np.load(img_data['coord_arr'])

speed = 1
i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            screen.fill(black)


    coordinate_array = np.roll(coordinate_array, speed, axis=0)
    i += speed
    i = i % total_cells
    img[coordinate_array[:, 0], coordinate_array[:, 1]] = color_array[:]

    speed = int(1000 * math.sin(math.pi * i / total_cells) ** .9 + 1)

    display_img = cv2.resize(img, (pixels_per_side, pixels_per_side))

    mysurf = pygame.surfarray.make_surface(display_img)
    pygame.display.update(screen.blit(mysurf, (0, 0)))
