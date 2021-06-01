FROM pccl/cuda_cudnn_pytorch_pygame_jax:0.1

RUN pip install opencv-python
COPY . /app
WORKDIR /app
CMD python hilbert_app.py
