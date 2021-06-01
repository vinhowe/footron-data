import sys, pygame, cv2
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm 
from PIL import Image
import math

cells_per_side = 2 ** 10
total_cells = cells_per_side ** 2
zoom = 1.35
pixels_per_side = int(cells_per_side * zoom)
black = 0, 0, 0
space = False
running = True
number_keycodes = {pygame.K_0:0, pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4,
                   pygame.K_5:5, pygame.K_6:6, pygame.K_7:7, pygame.K_8:8, pygame.K_9:9}

screen = pygame.display.set_mode((pixels_per_side,pixels_per_side))
screen.fill(black)

img = cv2.imread('studying.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (cells_per_side, cells_per_side))

def rotate(side_len, r, c, rbit, cbit):
    if cbit == 0:
        if rbit == 1:
            r = side_len - 1 - r
            c = side_len - 1 - c
        temp = r
        r = c
        c = temp
    return r, c

def coord2index(side_len, r, c):
    result = 0
    i = side_len / 2
    while i > 0:
        rbit = (r & i) > 0
        cbit = (c & i) > 0
        result += (i ** 2) * ((3 * rbit) ^ cbit)
        r, c = rotate(side_len, r, c, rbit, cbit)
        i = i / 2


def index2coord(side_len, index):
    r = 0
    c = 0
    i = 1
    temp_index = index

    while i < side_len:
        rbit = 1 & (temp_index // 2)
        cbit = 1 & (temp_index ^ rbit)
        r, c = rotate(i, r, c, rbit, cbit)
        r += i * rbit 
        c += i * cbit
        temp_index = temp_index // 4
        i = i * 2
    return r, c



coordinate_array = np.zeros([total_cells, 2]).astype(int)
color_array = np.zeros([total_cells, 3]).astype(int)


for i in tqdm(range(cells_per_side ** 2)):

    r, c = index2coord(cells_per_side, i)
    coordinate_array[i] = [r, c]
    color_array[i] = img[c,r]

np.save('studying_color_array', color_array)
np.save('studying_coordinate_array', coordinate_array)


speed = 1
speed_sign = 1
i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # if event.type == pygame.KEYDOWN:
        #     if event.key in number_keycodes.keys():
        #         speed = speed_sign * number_keycodes[event.key] ** 3
        #     elif event.key == pygame.K_MINUS:
        #         speed_sign = -speed_sign
        #         speed = speed_sign * np.abs(speed)


    coordinate_array = np.roll(coordinate_array, speed, axis=0)
    i += speed
    i = i % total_cells
    img[coordinate_array[:, 0], coordinate_array[:, 1]] = color_array[:]

    speed = int(1000 * math.sin(math.pi * i / total_cells) ** .9 + 1)
    # print()
    # print(i)
    # print(1000 * math.sin(math.pi * i / total_cells) ** .9)
    # print(speed)

    display_img = cv2.resize(img, (pixels_per_side, pixels_per_side))

    mysurf = pygame.surfarray.make_surface(display_img)
    pygame.display.update(screen.blit(mysurf, (0, 0)))


