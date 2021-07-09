__docformat__ = "reStructuredText"

import pygame

import pymunk
from pymunk import Vec2d

X, Y = 0, 1
### Physics collision types
COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1
COLLTYPE_BALL = 2
COLLTYPE_BOX = 3

wall_color = (100,100,100)



# x_min = 500
# x_max = 3188
# y_min = 0
# y_max = 1600


x_min = 50*4
x_max = 318*4
y_min = 0*4
y_max = 160*4

diagonal_len = ((x_max - x_min)**2. + (y_max - y_min)**2.) ** .5


def x_pos_adjust(x):
    return (x * (x_max - x_min)) + x_min

def y_pos_adjust(y):
    return (y * (y_max - y_min)) + y_min

def draw_adjusted_polygon(screen, coords, color=(100,100,100)):
    adjusted_coords = []
    for i in range(len(coords)):
        adjusted_x = x_pos_adjust(coords[i][0])
        adjusted_y = y_pos_adjust(coords[i][1])
        adjusted_coords.append((adjusted_x, adjusted_y))

    pygame.draw.polygon(screen, color, adjusted_coords)

def main():

    pygame.init()
    screen = pygame.display.set_mode((318*4, 160*4))
    clock = pygame.time.Clock()
    running = True

    while running:

        ### Draw stuff
        screen.fill(pygame.Color("white"))
                

        ## PINS
        for i in range(16):
            for j in range(13):
                pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.7+(j/40)), y_pos_adjust(.3+(i/30))), 4*diagonal_len/2000)

        for i in range(16):
            for j in range(12):
                pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.7+.5/40+(j/40)), y_pos_adjust(.3+.5/30+(i/30))), 4*diagonal_len/2000)


        ## BOUNCERS
        for i in range(6):
            for j in range(5):
                pygame.draw.circle(screen, (100,100,100), (x_pos_adjust((j/15)), y_pos_adjust(.5+(i/15))), 15*diagonal_len/2000)
                pygame.draw.circle(screen, (200,200,200), (x_pos_adjust((j/15)), y_pos_adjust(.5+(i/15))), 10*diagonal_len/2000)

        for i in range(6):
            for j in range(5):
                pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.5/15+(j/15)), y_pos_adjust(.5+.5/15+(i/15))), 15*diagonal_len/2000)
                pygame.draw.circle(screen, (200,200,200), (x_pos_adjust(.5/15+(j/15)), y_pos_adjust(.5+.5/15+(i/15))), 10*diagonal_len/2000)


        ## SPINNERS
        for j in range(5):
            pygame.draw.circle(screen, (100,100,100), (x_pos_adjust((j/15)), y_pos_adjust(.2)), 15*diagonal_len/2000)
            pygame.draw.circle(screen, (200,200,200), (x_pos_adjust((j/15)), y_pos_adjust(.2)), 10*diagonal_len/2000)

        for j in range(4):
            pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.03+(j/15)), y_pos_adjust(.3)), 15*diagonal_len/2000)
            pygame.draw.circle(screen, (200,200,200), (x_pos_adjust(.03+(j/15)), y_pos_adjust(.3)), 10*diagonal_len/2000)



        draw_adjusted_polygon(screen, ((0.,.95),(0.,1.),(.33,1.))) # bottem left wedge
        draw_adjusted_polygon(screen, ((1.,.95),(1.,1.),(.67,1.))) # bottem right wedge

        ## LEFT ELEVATOR SHAFT
        draw_adjusted_polygon(screen, ((.3, .95),(.31, .95),(.31, .2),(.3, .2))) # outer wall
        draw_adjusted_polygon(screen, ((.33, 1.),(.34, 1.),(.34, .2),(.33, .2))) # inner wall
        draw_adjusted_polygon(screen, ((.3, .2),(.31, .2),(.32, .15),(.35, .12),(.35, .08),(.30, .08))) # ceiling
        draw_adjusted_polygon(screen, ((.33,.2),(.34,.2),(.34,.19))) # inner wedge

        ## RIGHT ELEVATOR SHAFT
        draw_adjusted_polygon(screen, ((.7, .95),(.69, .95),(.69, .2),(.7, .2))) # outer wall
        draw_adjusted_polygon(screen, ((.67, 1.),(.66, 1.),(.66, .2),(.67, .2))) # inner wall
        draw_adjusted_polygon(screen, ((.7, .2),(.69, .2),(.68, .15),(.65, .12),(.65, .08),(.7, .08))) # ceiling
        draw_adjusted_polygon(screen, ((.67,.2),(.66,.2),(.66,.19))) # inner wedge

        ### Flip screen
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    doprof = 0
    if not doprof:
        main()
    else:
        import cProfile
        import pstats

        prof = cProfile.run("main()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats("cumulative", "time", "calls")
        stats.print_stats(30)