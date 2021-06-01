#!/bin/bash

xhost +local:root

sudo docker run -it \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  pccl/app_ifs:0.1
