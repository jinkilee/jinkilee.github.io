## This is how I utilize docker
--------
#### 1. Creating my own dev environment
I create my own docker environments for GPU/NPU usage. 
```
./gpu-base-docker
├── Dockerfile.v1.0
├── Dockerfile.v1.1
├── Dockerfile.v2.1
└── Dockerfile.v2.2

./npu-base-docker
├── Dockerfile.v1.0
├── Dockerfile.v1.2
├── Dockerfile.v1.3
├── Dockerfile.v1.4
└── Dockerfile.v1.5
```

See how Dockerfile was written
```
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# add remain...
```

The above Dockerfile contains the following
- Base OS Environment -> Ubuntu 22.04
- Utilities and libraries
    - Basic utils: vim, cmake, build-essential, openssh-server, wget, curl, iputils-ping, net-tools, git, htop and etc
    - Libraries for installing custom OpenCV: python3-dev, python3-numpy python3-pip, libgtk2.0-dev, libgstreamer-plugins-base1.0-dev, gstreamer1.0-alsa, gstreamer1.0-libav
- Staging opencv installation for reducing the image size
<br>

`Basic utils` are libraries that are commonly used for using ubuntu. `Libraries for installing custom OpenCV` are pre-requisites for installing custom-built OpenCV. Since I use GStreamer for cv::VideoCapture, Gstreamer libraries are necessary before building the OpenCV. Custom building OpenCV requires a lot of disk space. This is why I `Staging opencv installation for reducing the image size`
<br>

Once done, I can list docker images with docker CLI command
```
$ docker images | grep base
ubuntu/npu-base-image    1.5     e00383a1e4le    4 weeks ago     4.87GB
```

#### 2. Why I am doing this?
This helps me to create my coding environment quicker and easier.
- Commonly used libraries are listed and versioned properly
- No need to type all time-consuming but necessary building commands.
- Well-managed `CHANGLOG.md` helps me to recognize version history.
- For example, all the Dockerfile of NPU project starts from npu-base-image:version
```
FROM npu-base-image:1.5

# Rest are different project by project.
apt-get update && apt-get install -y \
    ...
```

#### 3. Future plan
I am planning to prepare my own dev environment based on Custom-built Python 3.14. 
```
RUN wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tar.xz && \
    tar-xf Python-3.14.0.tar.xz && \
    cd Python-3.14.0 && \
    ./configure --disable-gil --prefix=/workspace/python3.14-nogil && \
    make -j`nproc` && \
    make install
```

Building Python 3.14 with `--disable-gil` option makes `no-gil python` which can maximize CPU usage.



