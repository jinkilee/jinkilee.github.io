# WARNING: These steps seem to not work anymore!

#!/bin/bash

UBUNTU=ubuntu1804
CUDA_VERSION=10.1
CUDA_SUBVERSION=243
CUDA_APT=cuda-10-1

# Purge existign CUDA first
sudo apt --purge remove "cublas*" "cuda*"
sudo apt --purge remove "nvidia*"

# Install CUDA Toolkit 10
wget https://developer.download.nvidia.com/compute/cuda/repos/${UBUNTU}/x86_64/cuda-repo-${UBUNTU}_${CUDA_VERSION}.${CUDA_SUBVERSION}-1_amd64.deb
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/${UBUNTU}/x86_64/7fa2af80.pub && sudo apt update
sudo dpkg -i cuda-repo-${UBUNTU}_${CUDA_VERSION}.${CUDA_SUBVERSION}-1_amd64.deb

sudo apt update
sudo apt install -y ${CUDA_APT}

# Install CuDNN 7 and NCCL 2
wget https://developer.download.nvidia.com/compute/machine-learning/repos/${UBUNTU}/x86_64/nvidia-machine-learning-repo-${UBUNTU}_1.0.0-1_amd64.deb
sudo dpkg -i nvidia-machine-learning-repo-${UBUNTU}_1.0.0-1_amd64.deb

sudo apt update
sudo apt install -y libcudnn7 libcudnn7-dev libnccl2 libc-ares-dev

sudo apt autoremove -y
sudo apt upgrade -y

# Link libraries to standard locations
sudo mkdir -p /usr/local/cuda-${CUDA_VERSION}/nccl/lib
sudo ln -s /usr/lib/x86_64-linux-gnu/libnccl.so.2 /usr/local/cuda-${CUDA_VERSION}/nccl/lib/
sudo ln -s /usr/lib/x86_64-linux-gnu/libcudnn.so.7 /usr/local/cuda-${CUDA_VERSION}/lib64/

echo 'If everything worked fine, reboot now.'
