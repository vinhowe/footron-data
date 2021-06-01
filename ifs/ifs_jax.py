import sys
import pygame
import jax
import jax.numpy as jnp
import numpy as np
import time

WIDTH = 1024
HEIGHT = 1024
#WIDTH = 2048
#HEIGHT = 2048
white = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen.fill(white)

PSEUDO_CNTS = 10
CNT = 20*10000000 # number of particles
NUM_BURN = 3
NUM_UPDATES = 2
SF = 7.0 # constant scale factor avoids flickering

PARAMS = jnp.atleast_2d([
    [ -2.950, 1,     -1,     1],
    [ -2.850, 2.793, -2.697, 1.128 ],
    [ 1.5,    2.5,   0.731,  2.5],
    ])

#
# ---------------------------------------------------------------------------
#

# the core de jong iterator. so simple, so beautiful!
def update( x, y, params ):
    return jnp.sin(params[0]*y) - jnp.cos(params[1]*x), jnp.sin(params[2]*x) - jnp.cos(params[3]*y)

def cnts_to_colors( cnts, SF=9.0 ):
    # adding pseudo counts help eliminate some graininess
    cnts = jnp.log(cnts+PSEUDO_CNTS)

    cnts = cnts - jnp.min(cnts)
    cnts = 255 * (cnts / SF)
    cnts = jnp.minimum( cnts, 255 )

    cnts = cnts.astype(jnp.uint8)
    cnts = 255 - jnp.stack( [cnts,cnts,0.7*cnts], axis=2 )
    return cnts

def bin_particles( x, y ):
    # map points in [-2,2] to image coordinates
    tmpx = ((x+2)/4) * WIDTH
    tmpy = ((y+2)/4) * HEIGHT
    tmpx = tmpx.astype( jnp.uint32 )
    tmpy = tmpy.astype( jnp.uint32 )

    # now count how many points land in each pixel
    linear_indices = ( tmpy*WIDTH+tmpx ).astype(jnp.uint32).flatten()
    newcnts = jnp.bincount( linear_indices, minlength=WIDTH*HEIGHT, length=WIDTH*HEIGHT )
    newcnts = newcnts.reshape((HEIGHT,WIDTH))

    return newcnts

@jax.jit
def do_everything( init_x, init_y, params ):
    cnts = jnp.zeros((HEIGHT,WIDTH))
    x = init_x
    y = init_y

    for n in range(NUM_BURN):
        x,y = update( x, y, params )
    for n in range(NUM_UPDATES):
        x,y = update( x, y, params )

    cnts += bin_particles( x, y )

    colors = cnts_to_colors( cnts, SF=SF )

    return colors

#
# ---------------------------------------------------------------------------
#

tgt_pind = 1
params = PARAMS[0,:]

# we use fixed initial conditions to make everything as smooth as possible
init_x = jnp.array( 4*np.random.rand( CNT, 1 ) - 2 )
init_y = jnp.array( 4*np.random.rand( CNT, 1 ) - 2 )

pind_cnter = 0
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            done = True

    pind_cnter += 1
    if pind_cnter == 500:
        pind_cnter = 0
        tgt_pind += 1
        if tgt_pind >= PARAMS.shape[0]:
            tgt_pind = 0
        print("CHANGE TARGET: ", PARAMS[tgt_pind,:])

    params = 0.995 * params + 0.005 * PARAMS[tgt_pind,:]

    t1 = time.time()
    colors = do_everything( init_x, init_y, params )
    etime = time.time() - t1

    t1 = time.time()
    colors = np.asarray( colors )
    ctime = time.time() - t1

    t1 = time.time()
    mysurf = pygame.surfarray.make_surface(colors)
    pygame.display.update(screen.blit(mysurf, (0, 0)))
    dtime = time.time() - t1

    print( f"etime:{etime}, ctime:{ctime}, dtime:{dtime}" )


# freeglut
# glew
# glfw
