#!/bin/bash

xhost +local:root

sudo docker run -it \
  --rm \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /home/wingated:/home/wingated \
  --net host\
  -w /home/wingated/projects/wall/cstv-apps/style_transfer \
  --device=/dev/video1:/dev/video0 \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  pccl/app_styletransfer:0.2 /bin/bash
