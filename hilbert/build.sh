#!/bin/bash

docker build -t pccl/app_hilbert:0.1 .
docker push pccl/app_hilbert:0.1
