# WARNING: These steps seem to not work anymore!

#!/bin/bash

#UBUNTU=ubuntu1804
#CUDA_VERSION=10.1
#CUDA_SUBVERSION=243
#CUDA_APT=cuda-10-1

UBUNTU=ubuntu1604
CUDA_VERSION=10.0
CUDA_SUBVERSION=130
CUDA_APT=cuda-10-0

# CUDA files
CUDA_DEB_FILE=cuda-repo-${UBUNTU}_${CUDA_VERSION}.${CUDA_SUBVERSION}-1_amd64.deb
CUDA_DEB_FOLDER=http://developer.download.nvidia.com/compute/cuda/repos/${UBUNTU}/x86_64
CUDA_PUB_FILE=7fa2af80.pub
CUDA_DEB_LINK=${CUDA_DEB_FOLDER}/${CUDA_DEB_FILE}
CUDA_PUB_LINK=${CUDA_DEB_FOLDER}/${CUDA_PUB_FILE}

# CuDNN file
CuDNN_DEB_FILE=nvidia-machine-learning-repo-${UBUNTU}_1.0.0-1_amd64.deb
CuDNN_DEB_FOLDER=http://developer.download.nvidia.com/compute/machine-learning/repos/${UBUNTU}/x86_64
CuDNN_DEB_LINK=${CuDNN_DEB_FOLDER}/${CuDNN_DEB_FILE}

# check if CUDA file exists
if ( wget -o/dev/null "${CUDA_DEB_LINK}" ); then
	echo "[OK] : ${CUDA_DEB_LINK}"
else
	echo "[FAIL] : ${CUDA_DEB_LINK}"
	exit
fi

# chec if pub file exists
if ( wget -o/dev/null "${CUDA_PUB_LINK}" ); then
	echo "[OK] : ${CUDA_PUB_LINK}"
else
	echo "[FAIL] : ${CUDA_PUB_LINK}"
	exit
fi

# chec if CuDNN file exists
if ( wget -o/dev/null "${CuDNN_DEB_LINK}" ); then
	echo "[OK] : ${CUDA_PUB_LINK}"
else
	echo "[FAIL] : ${CUDA_PUB_LINK}"
	exit
fi

# 
echo "check finished !! sleeping 10 seconds."
sleep 10

# Purge existign CUDA first
sudo apt --purge remove "cublas*" "cuda*"
sudo apt --purge remove "nvidia*"

# Install CUDA Toolkit 10
wget ${CUDA_DEB_LINK}
sudo apt-key adv --fetch-keys ${CUDA_PUB_FILE} && sudo apt update
sudo dpkg -i ${CUDA_DEB_FILE}

sudo apt update
sudo apt install -y ${CUDA_APT}

# Install CuDNN 7 and NCCL 2
wget ${CUDA_PUB_LINK}
sudo dpkg -i ${CuDNN_DEB_FILE}

sudo apt update
sudo apt install -y libcudnn7 libcudnn7-dev libnccl2 libc-ares-dev

sudo apt autoremove -y
sudo apt upgrade -y

# Link libraries to standard locations
sudo mkdir -p /usr/local/cuda-${CUDA_VERSION}/nccl/lib
sudo ln -s /usr/lib/x86_64-linux-gnu/libnccl.so.2 /usr/local/cuda-${CUDA_VERSION}/nccl/lib/
sudo ln -s /usr/lib/x86_64-linux-gnu/libcudnn.so.7 /usr/local/cuda-${CUDA_VERSION}/lib64/

# set environment varilables
echo "export CUDA_HOME=/usr/local/cuda-${CUDA_VERSION}" >> ~/.bashrc
echo "export PATH=${CUDA_HOME}/bin:$PATH" >> ~/.bashrc

# refresh ~/.bashrc
source ~/.bashrc

echo 'If everything worked fine, reboot now.'
