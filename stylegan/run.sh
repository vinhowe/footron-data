#!/bin/bash

xhost +local:root

sudo docker run -it \
  --rm \
  --gpus all \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  --cap-add=SYS_ADMIN \
  --shm-size=1g \
  pccl/app_stylegan2:0.4

