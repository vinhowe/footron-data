#!/bin/bash

xhost +local:root

sudo docker run -it \
  --rm \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  -e QUALITY=low \
  pccl/app_ifs:0.3
