#!/bin/bash

docker build -t pccl/app_ifs:0.3 .
docker push pccl/app_ifs:0.3
