FROM pccl/rtdisp:0.1

RUN pip install opencv-python torchfile asyncio
RUN pip install git+https://github.com/BYU-PCCL/footron-protocol-python.git
RUN pip install git+https://github.com/BYU-PCCL/footron-messaging-python.git

COPY . /app
WORKDIR /app
ENV WIDTH=1280
CMD python camera_demo.py demo --model models/21styles.model --style-folder images/wallstyles/
