import os
import cv2
import numpy as np
import torch
from torch.autograd import Variable
import time

from net import Net
from option import Options
import utils
from utils import StyleLoader
import rtdisp_torch

# for messages from the user's UI
import asyncio
import foomsg
from threading import Thread

FRAMES_PER_STYLE = 300

simg = None
swidth = 0
sheight = 0
sdiv = 2

interactive_mode = False
style_index = 0
requested_style = -1

#
# ----------------------------------------------------------------------------
#

def change_style( new_style_index ):
    global style_index, simg, swidth, sheight, sdiv

    style_index = new_style_index

    style_v = style_loader.get(style_index)
    style_v = Variable(style_v.data, requires_grad=False)
    style_model.setTarget(style_v)

    # create the style thumbnail
    simg = style_v.cpu().numpy()
    simg = style_v.squeeze().clamp(0, 255).permute(1,2,0).byte().cpu().numpy()
    swidth = int(simg.shape[1]/sdiv)
    sheight = int(simg.shape[0]/sdiv)
    simg = cv2.resize(simg,(swidth, sheight), interpolation = cv2.INTER_CUBIC)
    simg = torch.Tensor( simg ).to("cuda")

def draw( dt ):
    global idx, img, simg, swidth, sheight, style_index
    global requested_style, interactive_mode

    idx += 1

    # read frame
    ret_val, img = cam.read() # CV2 loads in BGR by default.  That's what the model wants, so we leave it.
    img = cv2.flip(img, 1)  # horizontal mirroring improves the effect
    img = np.array(img).transpose(2, 0, 1)  # reorder for torch

    # changing style
    if not interactive_mode and idx%FRAMES_PER_STYLE == 1:
        change_style( int(idx/FRAMES_PER_STYLE) )

    if interactive_mode and requested_style != -1:
        change_style( requested_style )
        requested_style = -1

    # ship to gpu
    img = torch.from_numpy(img).unsqueeze(0).float()
    img.requires_grad = False
    img = img.cuda()

    # run the model
    with torch.no_grad():
        img = Variable(img,requires_grad=False)
        img = style_model(img)
        img = img.squeeze().clamp(0, 255).permute(1,2,0).byte()

        # copy the style thumbnail
        border = 4
        ofs = 12

        xstart = WIDTH-swidth-ofs
        xend = xstart+swidth
        ystart = ofs
        yend = ystart+sheight

        img[ ystart-border:yend+border, xstart-border:xend+border, : ] = 0
        img[ ystart:yend, xstart:xend, : ] = simg

        (b, g, r) = torch.chunk( img, 3, dim=2 ) # convert from CV2 BGR -> RGB
        img = torch.cat( [r, g, b, alpha_channel], dim=2 )

    return img

#
# ----------------------------------------------------------------------------
#

def message_handler(message):
    global interactive_mode, requested_style
    interactive_mode = True
    requested_style = message;

async def main_loop():
    while True:
        await asyncio.sleep( 0.25 )

def thread_start( loop ):
    asyncio.set_event_loop(loop)
    messaging = foomsg.Messaging()
    messaging.add_message_listener( message_handler )
    messaging_loop = loop.create_task( messaging.start() )
    loop.create_task(main_loop())
    loop.run_until_complete(messaging_loop)

#
# ----------------------------------------------------------------------------
#

# getting things ready
args = Options().parse()

style_model = Net(ngf=args.ngf)
model_dict = torch.load( "models/21styles.model" )

model_dict_clone = model_dict.copy()
for key, value in model_dict_clone.items():
    if key.endswith(('running_mean', 'running_var')):
        del model_dict[key]
style_model.load_state_dict(model_dict, False)
style_model.eval()

style_loader = StyleLoader(args.style_folder, args.style_size)
style_model.cuda()

# Define the codec and create VideoWriter object

if 'WIDTH' in os.environ and os.environ['WIDTH']=="1920":
    WIDTH = 1920
    HEIGHT = 1080
    sdiv = 1

elif 'WIDTH' in os.environ and os.environ['WIDTH']=="1280":
    WIDTH = 1280
    HEIGHT = 720
    sdiv = 2

else:
    WIDTH = 1024
    HEIGHT = 576
    sdiv = 3

cam = cv2.VideoCapture(0)
cam.set(3, WIDTH)
cam.set(4, HEIGHT)
key = 0
idx = 0

# allocate this once
alpha_channel = 255*torch.ones((HEIGHT,WIDTH,1),dtype=torch.uint8).cuda()

ret_val, img = cam.read()

# fire up the footron messaging stuff
loop = asyncio.new_event_loop()
t = Thread( target=thread_start, args=(loop,) )
t.start()

# start the real time display loop
rtdisp_torch.setup( WIDTH, HEIGHT )
rtdisp_torch.set_draw( draw )
rtdisp_torch.go()
