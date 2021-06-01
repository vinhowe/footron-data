#!/bin/bash

docker build -t pccl/cuda_cudnn_pytorch_pygame_jax:0.1 .
docker push pccl/cuda_cudnn_pytorch_pygame_jax:0.1
