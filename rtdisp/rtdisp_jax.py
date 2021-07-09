from contextlib import contextmanager
import numpy as np
import pycuda.driver
from pycuda.gl import graphics_map_flags
from glumpy import app, gloo, gl
import jax.numpy as jnp

@contextmanager
def cuda_activate(img):
    """Context manager simplifying use of pycuda.gl.RegisteredImage"""
    mapping = img.map()
    yield mapping.array(0,0)
    mapping.unmap()

def create_shared_texture(w, h, c=4,
        map_flags=graphics_map_flags.WRITE_DISCARD,
        dtype=np.uint8):
    """Create and return a Texture2D with gloo and pycuda views."""
    tex = np.zeros((h,w,c), dtype).view(gloo.Texture2D)
    tex.activate() # force gloo to create on GPU
    tex.deactivate()
    cuda_buffer = pycuda.gl.RegisteredImage( int(tex.handle), tex.target, map_flags )
    return tex, cuda_buffer

def setup(w, h, fullscreen=False):
    global screen, cuda_buffer, window

    # create window with OpenGL context
    app.use('glfw')
    window = app.Window(w,h,fullscreen=fullscreen)
    window.on_draw = on_draw
    window.on_close = on_close

    # setup pycuda and torch
    import pycuda.gl.autoinit
    import pycuda.gl

    # XXX I don't know why, but this line is critical.  I think it somehow initializes jax?
    state = jnp.ones((1,1))

    # create a buffer with pycuda and gloo views
    tex, cuda_buffer = create_shared_texture(w,h,4)

    # create a shader to program to draw to the screen
    vertex = """
    uniform float scale;
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        v_texcoord = texcoord;
        gl_Position = vec4(scale*position, 0.0, 1.0);
    } """

    fragment = """
    uniform sampler2D tex;
    varying vec2 v_texcoord;
    void main()
    {
        gl_FragColor = texture2D(tex, v_texcoord);
    } """

    # Build the program and corresponding buffers (with 4 vertices)
    screen = gloo.Program(vertex, fragment, count=4)

    # Upload data into GPU
#    screen['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
    screen['position'] = [(-1,+1), (+1,+1), (-1,-1), (+1,-1)]
    screen['texcoord'] = [(0,0), (0,1), (1,0), (1,1)]
    screen['scale'] = 1.0
    screen['tex'] = tex

def jax_draw( frame ):
    tex = screen['tex']
    h,w = tex.shape[:2]
    # copy from jax into buffer
    assert tex.nbytes == frame.nbytes
    with cuda_activate(cuda_buffer) as ary:
        cpy = pycuda.driver.Memcpy2D()
        cpy.set_src_device(frame.unsafe_buffer_pointer())
        cpy.set_dst_array(ary)
        cpy.width_in_bytes = cpy.src_pitch = cpy.dst_pitch = tex.nbytes//h
        cpy.height = h
        cpy(aligned=False)

def on_draw(dt):
    global draw_func

    frame = draw_func( dt )

    window.set_title(str(window.fps).encode("ascii"))

    jax_draw( frame )

    window.clear()
    screen.draw(gl.GL_TRIANGLE_STRIP)

# not sure why this doesn't work right
def on_close():
    pycuda.gl.autoinit.context.pop()

def set_draw( f ):
    global draw_func
    draw_func = f

def go():
    app.run()
