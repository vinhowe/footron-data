import jax.numpy as jnp
import rtdisp_jax

WIDTH = 1024
HEIGHT = 1024

ind = 0
def draw( dt ):
    global ind
    colors = (ind%255)*jnp.ones((HEIGHT,WIDTH,4))
    colors = colors.astype(jnp.uint8)
    ind += 1

    return colors

rtdisp_jax.setup( WIDTH, HEIGHT )
rtdisp_jax.set_draw( draw )
rtdisp_jax.go()
