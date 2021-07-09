import torch
import rtdisp

WIDTH = 1024
HEIGHT = 1024

def draw( dt ):

    with torch.no_grad():
        colors = 255*torch.rand((HEIGHT,WIDTH,4))
        colors[:,:,3] = 255
        colors = colors.byte().to("cuda:0")

    return colors

rtdisp.setup( WIDTH, HEIGHT )
rtdisp.set_draw( draw )
rtdisp.go()
