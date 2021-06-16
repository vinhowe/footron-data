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


gravity_reversed = set()


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600


def mouse_coll_func(arbiter, space, data):
    """Simple callback that increases the radius of circles touching the mouse"""
    s1, s2 = arbiter.shapes
    # s2.unsafe_set_radius(s2.radius + 0.15)
    # s2.body.apply_force_at_local_point((0, 180000))
    return False

def box_coll_func(arbiter, space, data):
    s1, s2 = arbiter.shapes
    # s2.body.apply_force_at_local_point((0,1800))
    # gravity_reversed.add(s2)
    s2.body.apply_force_at_local_point((0, 1800.0 * s2.body.mass))
    return False


x_min = 500
x_max = 3188
y_min = 0
y_max = 1600


# x_min = 50*4
# x_max = 318*4
# y_min = 0*4
# y_max = 160*4

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
    screen = pygame.display.set_mode((3188, 1600))
    clock = pygame.time.Clock()
    running = True

    ### Physics stuff
    space = pymunk.Space()
    space.gravity = 0.0, -900.0

    ## Balls
    balls = []

    ## Antigravity-box
    # antigravity_box = pymunk.Body(body_type=pymunk.Body.STATIC)
    # box_vertices = [(-200, -200), (-200, 200), (200, 200), (200, -200)]
    # mass = 1.0
    # moment = pymunk.moment_for_circle(mass, inner_radius=0, outer_radius=4)
    # body = pymunk.Body(body_type=pymunk.Body.STATIC) 
    # body.position = (1600,0)
    # box_shape = pymunk.Poly(body, box_vertices)
    # box_shape.collision_type = COLLTYPE_BOX
    # box_shape.friction = 1
    # space.add(body, box_shape)


    ## OUTER BOUNDARIES
    boundaries = []
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (x_pos_adjust(.5), flipy(y_pos_adjust(1.)))
    space.add(body)

    shape = pymunk.Poly(body, ((-1290, flipy(700)),(-1400, flipy(700)),(-1290, flipy(-1800)),(-1400, flipy(-1800))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.5
    space.add(shape)
    boundaries.append(shape)

    shape = pymunk.Poly(body, ((1325, flipy(700)),(1400, flipy(700)),(1325, flipy(-1800)),(1400, flipy(-1800))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.5
    space.add(shape)
    boundaries.append(shape)

    shape = pymunk.Poly(body, ((-1400, flipy(-990)),(1400, flipy(-990)),(1400, flipy(-1900)),(-1400, flipy(-1900))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.5
    space.add(shape)
    boundaries.append(shape)

    shape = pymunk.Poly(body, ((-1400, flipy(600)),(1400, flipy(600)),(1400, flipy(1900)),(-1400, flipy(1900))), radius=1)
    shape.friction = .5
    shape.elasticity = .5
    space.add(shape)
    boundaries.append(shape)

    shape = pymunk.Poly(body, ((-1290, flipy(550)),(-500, flipy(600)),(-1290, flipy(600))), radius=1)
    shape.friction = .5
    shape.elasticity = .5
    space.add(shape)
    boundaries.append(shape)

    shape = pymunk.Poly(body, ((1325, flipy(550)),(500, flipy(600)),(1325, flipy(600))), radius=1)
    shape.friction = .5
    shape.elasticity = .5
    space.add(shape)
    boundaries.append(shape)


    ## PINS
    pins = []
    for i in range(12):
        for j in range(18):
            pin_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            pin_body.position = (x_pos_adjust(.705+(j/60)), flipy(y_pos_adjust(.3+(i/20))))
            # moment = pymunk.moment_for_circle(1., inner_radius=0, outer_radius=4)

            pin_shape = pymunk.Circle(body=pin_body, radius=4)
            pin_shape.collision_type = COLLTYPE_BALL
            pin_shape.friction = 0.5

            pin_shape.elasticity = 1.

            space.add(pin_body, pin_shape)
            pins.append(pin_shape)

    for i in range(12):
        for j in range(18):
            pin_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            pin_body.position = (x_pos_adjust(.705+.5/60+(j/60)), flipy(y_pos_adjust(.3+.5/20+(i/20))))
            # moment = pymunk.moment_for_circle(1., inner_radius=0, outer_radius=4)

            pin_shape = pymunk.Circle(body=pin_body, radius=4)
            pin_shape.friction = 0.5
            pin_shape.elasticity = 1.

            space.add(pin_body, pin_shape)
            pins.append(pin_shape)


    # for i in range(16):
    #     for j in range(12):
    #         pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.7+.5/40+(j/40)), y_pos_adjust(.3+.5/30+(i/30))), 4*diagonal_len/2000)


    ## BOUNCERS\
    bouncers = []
    for i in range(4):
        for j in range(3):
            bouncer_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            bouncer_body.position = (x_pos_adjust((j/9.5)), flipy(y_pos_adjust(.5+(i/8))))
            bouncer_shape = pymunk.Circle(bouncer_body, radius = 50)
            # pygame.draw.circle(screen, (100,100,100), (x_pos_adjust((j/15)), y_pos_adjust(.5+(i/15))), 15*diagonal_len/2000)
            # pygame.draw.circle(screen, (200,200,200), (x_pos_adjust((j/15)), y_pos_adjust(.5+(i/15))), 10*diagonal_len/2000)
            bouncer_shape.friction = .5
            bouncer_shape.elasticity = 1.5

            space.add(bouncer_body, bouncer_shape)
            bouncers.append(bouncer_shape)

    for i in range(3):
        for j in range(3):
            bouncer_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            bouncer_body.position = (x_pos_adjust(.5/9.5+(j/9.5)), flipy(y_pos_adjust(.5+.5/8+(i/8))))
            bouncer_shape = pymunk.Circle(bouncer_body, radius = 50)
            # pygame.draw.circle(screen, (100,100,100), (x_pos_adjust((j/15)), y_pos_adjust(.5+(i/15))), 15*diagonal_len/2000)
            # pygame.draw.circle(screen, (200,200,200), (x_pos_adjust((j/15)), y_pos_adjust(.5+(i/15))), 10*diagonal_len/2000)
            bouncer_shape.friction = .5
            bouncer_shape.elasticity = 1.5

            space.add(bouncer_body, bouncer_shape)
            bouncers.append(bouncer_shape)
            # pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.5/15+(j/15)), y_pos_adjust(.5+.5/15+(i/15))), 15*diagonal_len/2000)
            # pygame.draw.circle(screen, (200,200,200), (x_pos_adjust(.5/15+(j/15)), y_pos_adjust(.5+.5/15+(i/15))), 10*diagonal_len/2000)


    # ## SPINNERS
    # for j in range(5):
    #     pygame.draw.circle(screen, (100,100,100), (x_pos_adjust((j/15)), y_pos_adjust(.2)), 15*diagonal_len/2000)
    #     pygame.draw.circle(screen, (200,200,200), (x_pos_adjust((j/15)), y_pos_adjust(.2)), 10*diagonal_len/2000)

    # for j in range(4):
    #     pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.03+(j/15)), y_pos_adjust(.3)), 15*diagonal_len/2000)
    #     pygame.draw.circle(screen, (200,200,200), (x_pos_adjust(.03+(j/15)), y_pos_adjust(.3)), 10*diagonal_len/2000)



    # draw_adjusted_polygon(screen, ((0.,.95),(0.,1.),(.33,1.))) # bottem left wedge
    # draw_adjusted_polygon(screen, ((1.,.95),(1.,1.),(.67,1.))) # bottem right wedge

    ### LEFT ELEVATOR SHAFT
    left_shaft_shapes = []
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (x_pos_adjust(.3), flipy(y_pos_adjust(1.)))
    space.add(body)

    shape = pymunk.Poly(body, ((0, flipy(500)),(30, flipy(500)),(30, flipy(-680)),(0, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((30, flipy(-680)),(35, flipy(-710)),(0, flipy(-710)),(0, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((35, flipy(-710)),(40, flipy(-730)),(0, flipy(-730)),(0, flipy(-710))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((40, flipy(-730)),(50, flipy(-750)),(0, flipy(-750)),(0, flipy(-730))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((50, flipy(-750)),(70, flipy(-770)),(0, flipy(-770)),(0, flipy(-750))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((70, flipy(-770)),(110, flipy(-790)),(0, flipy(-790)), (0, flipy(-770))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((110, flipy(-790)),(130, flipy(-795)),(130, flipy(-830)),(0, flipy(-830)),(0, flipy(-790))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((80, flipy(600)),(110, flipy(600)),(110, flipy(-680)),(80, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((110, flipy(-700)),(110, flipy(-680)),(80, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    left_shaft_shapes.append(shape)


    ### RIGHT ELEVATOR SHAFT
    right_shaft_shapes = []
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (x_pos_adjust(.7), flipy(y_pos_adjust(1.)))
    space.add(body)

    shape = pymunk.Poly(body, ((0, flipy(500)),(-30, flipy(500)),(-30, flipy(-680)),(0, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-30, flipy(-680)),(-35, flipy(-710)),(0, flipy(-710)),(0, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-35, flipy(-710)),(-40, flipy(-730)),(0, flipy(-730)),(0, flipy(-710))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-40, flipy(-730)),(-50, flipy(-750)),(0, flipy(-750)),(0, flipy(-730))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-50, flipy(-750)),(-70, flipy(-770)),(0, flipy(-770)),(0, flipy(-750))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-70, flipy(-770)),(-110, flipy(-790)),(0, flipy(-790)), (0, flipy(-770))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-110, flipy(-790)),(-130, flipy(-795)),(-130, flipy(-830)),(0, flipy(-830)),(0, flipy(-790))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-80, flipy(600)),(-110, flipy(600)),(-110, flipy(-680)),(-80, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)

    shape = pymunk.Poly(body, ((-110, flipy(-700)),(-110, flipy(-680)),(-80, flipy(-680))), radius=1)
    shape.friction = .5
    shape.elasticity = 1.2
    space.add(shape)
    right_shaft_shapes.append(shape)



    ### Mouse
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    mouse_shape = pymunk.Circle(mouse_body, 3, (0, 0))
    mouse_shape.collision_type = COLLTYPE_MOUSE
    space.add(mouse_body, mouse_shape)

    space.add_collision_handler(
        COLLTYPE_MOUSE, COLLTYPE_BALL
    ).pre_solve = mouse_coll_func

    space.add_collision_handler(
        COLLTYPE_BOX, COLLTYPE_BALL
    ).pre_solve = box_coll_func


    # space.add_collision_handler(
    #     COLLTIPE_STATIC, COLLTYPE_BALL
    # ).pre_solve = 
    ### Plinko Course


    ### Static line
    line_point1 = None
    static_lines = []
    run_physics = True

    while running:
        # state = handle_inputs(state)
        # state = handle_physics(state)
        # state = handle_rendering(state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "balls_and_lines.png")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                p = event.pos[X], flipy(event.pos[Y])
                body = pymunk.Body(10, 100)
                body.position = p
                shape = pymunk.Circle(body, 15, (0, 0))
                shape.friction = 0.8
                shape.elasticity = .7
                shape.collision_type = COLLTYPE_BALL
                space.add(body, shape)
                balls.append(shape)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if line_point1 is None:
                    line_point1 = Vec2d(event.pos[X], flipy(event.pos[Y]))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if line_point1 is not None:

                    line_point2 = Vec2d(event.pos[X], flipy(event.pos[Y]))
                    shape = pymunk.Segment(
                        space.static_body, line_point1, line_point2, 0.0
                    )
                    shape.friction = 0.99
                    space.add(shape)
                    static_lines.append(shape)
                    line_point1 = None

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run_physics = not run_physics

        p = pygame.mouse.get_pos()
        mouse_pos = Vec2d(p[X], flipy(p[Y]))
        mouse_body.position = mouse_pos

        if pygame.key.get_mods() & pygame.KMOD_SHIFT and pygame.mouse.get_pressed()[0]:
            body = pymunk.Body(10, 10)
            body.position = mouse_pos
            shape = pymunk.Circle(body, 10, (0, 0))
            shape.collision_type = COLLTYPE_BALL
            shape.elasticity = .7
            space.add(body, shape)
            balls.append(shape)

        for s in gravity_reversed:
            s.body.apply_force_at_local_point((0, 1800.0 * s.body.mass))

        ### Update physics
        if run_physics:
            dt = 1.0 / 60.0
            for x in range(1):
                space.step(dt)

        ### Draw stuff
        screen.fill(pygame.Color("white"))

        # Display some text
        font = pygame.font.Font(None, 16)
        text = """LMB: Create ball
        LMB + Shift: Create many balls
        RMB: Drag to create wall, release to finish
        Space: Pause physics simulation"""
        y = 5

        for line in text.splitlines():
            text = font.render(line, True, pygame.Color("black"))
            screen.blit(text, (5, y))
            y += 10

        for ball in balls:
            r = ball.radius
            v = ball.body.position
            rot = ball.body.rotation_vector
            p = int(v.x), int(flipy(v.y))
            p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
            p2 = int(p2.x), int(p2.y)
            pygame.draw.circle(screen, pygame.Color("blue"), p, int(r), 2)
            pygame.draw.line(screen, pygame.Color("red"), p, p2)

        if line_point1 is not None:
            p1 = int(line_point1.x), int(flipy(line_point1.y))
            p2 = mouse_pos.x, flipy(mouse_pos.y)
            pygame.draw.lines(screen, pygame.Color("black"), False, [p1, p2])

        for line in static_lines:
            body = line.body

            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = int(pv1.x), int(flipy(pv1.y))
            p2 = int(pv2.x), int(flipy(pv2.y))
            pygame.draw.lines(screen, pygame.Color("lightgray"), False, [p1, p2])


        ## PINS
        for pin in pins:
            pygame.draw.circle(screen, (200,0,0), (pin.body.position[0], flipy(pin.body.position[1])), pin.radius)


        # BOUNCERS
        for bouncer in bouncers:
            pygame.draw.circle(screen, (100,100,100), (bouncer.body.position[0], flipy(bouncer.body.position[1])), bouncer.radius)
            pygame.draw.circle(screen, (200,200,200), (bouncer.body.position[0], flipy(bouncer.body.position[1])), bouncer.radius - 4)




        # ## SPINNERS
        # for j in range(5):
        #     pygame.draw.circle(screen, (100,100,100), (x_pos_adjust((j/15)), y_pos_adjust(.2)), 15*diagonal_len/2000)
        #     pygame.draw.circle(screen, (200,200,200), (x_pos_adjust((j/15)), y_pos_adjust(.2)), 10*diagonal_len/2000)

        # for j in range(4):
        #     pygame.draw.circle(screen, (100,100,100), (x_pos_adjust(.03+(j/15)), y_pos_adjust(.3)), 15*diagonal_len/2000)
        #     pygame.draw.circle(screen, (200,200,200), (x_pos_adjust(.03+(j/15)), y_pos_adjust(.3)), 10*diagonal_len/2000)



        # draw_adjusted_polygon(screen, ((0.,.95),(0.,1.),(.33,1.))) # bottem left wedge
        # draw_adjusted_polygon(screen, ((1.,.95),(1.,1.),(.67,1.))) # bottem right wedge

        ## LEFT ELEVATOR SHAFT

        for shape in left_shaft_shapes:
            y_flipped_vertices = []
            for vertice in shape.get_vertices():
                y_flipped_vertices.append((vertice[0] + shape.body.position[0], flipy(vertice[1] + shape.body.position[1])))

            pygame.draw.polygon(screen, (150,0,0), y_flipped_vertices)

        for shape in right_shaft_shapes:
            y_flipped_vertices = []
            for vertice in shape.get_vertices():
                y_flipped_vertices.append((vertice[0] + shape.body.position[0], flipy(vertice[1] + shape.body.position[1])))

            pygame.draw.polygon(screen, (150,0,0), y_flipped_vertices)

        for shape in boundaries:
            y_flipped_vertices = []
            for vertice in shape.get_vertices():
                y_flipped_vertices.append((vertice[0] + shape.body.position[0], flipy(vertice[1] + shape.body.position[1])))

            pygame.draw.polygon(screen, (150,0,0), y_flipped_vertices)
        # draw_adjusted_polygon(screen, y_flipped_vertices)
        # draw_adjusted_polygon(screen, ((.3, .95),(.31, .95),(.31, .2),(.3, .2))) # outer wall
        # draw_adjusted_polygon(screen, ((.33, 1.),(.34, 1.),(.34, .2),(.33, .2))) # inner wall
        # draw_adjusted_polygon(screen, ((.3, .2),(.31, .2),(.32, .15),(.35, .12),(.35, .08),(.30, .08))) # ceiling
        # draw_adjusted_polygon(screen, ((.33,.2),(.34,.2),(.34,.19))) # inner wedge

        ## RIGHT ELEVATOR SHAFT
        # draw_adjusted_polygon(screen, ((.7, .95),(.69, .95),(.69, .2),(.7, .2))) # outer wall
        # draw_adjusted_polygon(screen, ((.67, 1.),(.66, 1.),(.66, .2),(.67, .2))) # inner wall
        # draw_adjusted_polygon(screen, ((.7, .2),(.69, .2),(.68, .15),(.65, .12),(.65, .08),(.7, .08))) # ceiling
        # draw_adjusted_polygon(screen, ((.67,.2),(.66,.2),(.66,.19))) # inner wedge


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