FROM nvidia/cuda:10.2-cudnn8-runtime-ubuntu20.04

# Set the default Python version to Python 3.8
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH /usr/local/cuda/bin:${PATH}

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3.8-venv \
    python3.8-dev \
    python3-pip \
    libssl-dev \
    libffi-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Ensure pip is installed and upgraded
RUN python3.8 -m pip install --upgrade pip

# Install TensorRT dependencies
RUN apt-get update && apt-get install -y \
    libnvinfer8 \
    libnvonnxparsers8 \
    libnvparsers8 \
    libnvinfer-plugin8 \
    libnvinfer-dev \
    libnvonnxparsers-dev \
    libnvparsers-dev \
    libnvinfer-plugin-dev \
    python3-libnvinfer \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /workspace

# Install additional Python packages
RUN pip3.8 install numpy opencv-python

# Default command
CMD ["bash"]
