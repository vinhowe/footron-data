#
# A basic environment that provides most of what's necessary for GPU accelerated opengl applications
#

FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel

ENV NVIDIA_DRIVER_CAPABILITIES all

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl2-dev pkg-config libglvnd-dev libgl1-mesa-dev libegl1-mesa-dev libgles2-mesa-dev libxext6 libx11-6 && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install --upgrade pygame jax jaxlib==0.1.67+cuda111 -f https://storage.googleapis.com/jax-releases/jax_releases.html
