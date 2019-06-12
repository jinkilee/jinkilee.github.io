#FROM ubuntu:16.04

# set working directory
#WORKDIR /home/notebooks

# add requirements file 
#ADD requirements.txt /home/

# install something
#RUN apt-get update
#RUN apt-get install -y software-properties-common vim
#RUN add-apt-repository ppa:jonathonf/python-3.6
#RUN apt-get update
#RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
#RUN apt-get install -y git
#RUN apt-get install -y ipython ipython-notebook


# install dev tools
#RUN apt-get install -y software-properties-common vim \
# && apt-get install -y git

# run shell command for notebook on start 
#CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root

FROM nvidia/cuda:10.0-base-ubuntu16.04

ARG NB_USER="docker"
ARG NB_UID="1002"
ARG NB_GID="1002"

RUN echo $NB_USER
ADD container/lab/fix-permissions /usr/local/bin/fix-permissions
ENV JUPYTER_ENABLE_LAB true
USER root                                                                  

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    wget \
    git \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    # Pick up some TF dependencies
    build-essential \
    cuda-command-line-tools-10-0 \
    cuda-cublas-10-0 \
    cuda-cufft-10-0 \
    cuda-curand-10-0 \
    cuda-cusolver-10-0 \
    cuda-cusparse-10-0 \
    libcudnn7=7.4.1.5-1+cuda10.0 \
    libnccl2=2.3.7-1+cuda10.0 \
    libfreetype6-dev \
    libnccl-dev=2.3.7-1+cuda10.0 \
    libhdf5-serial-dev \
    libpng12-dev \
    libzmq3-dev \
    pkg-config \
    software-properties-common \
    unzip \
 && \
   apt-get clean && \
   rm -rf /var/lib/apt/lists/*



RUN apt-get update \
 && apt-get install nvinfer-runtime-trt-repo-ubuntu1604-5.0.2-ga-cuda10.0 \
 && apt-get update \
 && apt-get install -y libnvinfer5=5.0.2-1+cuda10.0 \
 && apt-get install -y libnvinfer-dev=5.0.2-1+cuda10.0 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ARG PYTHON=python3
ARG PIP=pip3
#
RUN apt-get update && apt-get install -y \
   ${PYTHON} \
   ${PYTHON}-pip

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    HOME=/home/$NB_USER

# Create jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
# RUN groupadd wheel -g 11 && \
#     echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
#     useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
#     mkdir -p $CONDA_DIR && \
#     chown $NB_USER:$NB_GID $CONDA_DIR && \
#     chmod g+w /etc/passwd && \
#     fix-permissions $HOME && \
#     fix-permissions $CONDA_DIR

# Setup work directory for backward-compatibility
# RUN mkdir /home/$NB_USER/test && \
#     mkdir /home/$NB_USER/.keras

# COPY test-notebooks /home/$NB_USER/test
# USER $NB_UID


#RUN ${PIP} install --upgrade \
#    pip \
#    tensorflow-gpu \
#    setuptools

# Install conda as jovyan and check the md5 sum provided on the download site
ENV MINICONDA_VERSION 4.5.11
RUN cd /tmp && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "e1045ee415162f944b6aebfe560b8fee *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda config --system --prepend channels conda-forge && \
    $CONDA_DIR/bin/conda config --system --set auto_update_conda false && \
    $CONDA_DIR/bin/conda config --system --set show_channel_urls true && \
    $CONDA_DIR/bin/conda install --quiet --yes conda="${MINICONDA_VERSION%.*}.*" && \
    $CONDA_DIR/bin/conda update --all --quiet --yes && \
    conda clean -tipsy && \
    rm -rf /home/$NB_USER/.cache/yarn


# Install Tini
RUN conda install --quiet --yes 'tini=0.18.0' && \
    conda list tini | grep tini | tr -s ' ' | cut -d ' ' -f 1,2 >> $CONDA_DIR/conda-meta/pinned && \
    conda clean -tipsy

ADD container/lab/environment.yml environment.yml



RUN conda update -n base conda -y && \
    conda env update && \
    conda clean -tipsy && \
    conda install nodejs && \
    jupyter labextension install @jupyterlab/hub-extension@^0.12.0 && \
    npm cache clean --force && \
    jupyter notebook --generate-config && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn

USER root

# RUN fix-permissions /home/$NB_USER && \
#     fix-permissions $CONDA_DIR && \
#     fix-permissions /home/$NB_USER/.keras && \
#     fix-permissions /home/$NB_USER/.theanorc
#    fix-permissions /home/$NB_USER/notebooks

RUN jupyter lab clean \
 && jupyter labextension install @jupyterlab/hub-extension \
 && jupyter labextension install @jupyter-widgets/jupyterlab-manager \
 && jupyter labextension install @jupyterlab/toc \
 && jupyter labextension install @krassowski/jupyterlab_go_to_definition \
 && jupyter labextension install @oriolmirosa/jupyterlab_materialdarker \
 && jupyter labextension install @jupyterlab/fasta-extension \
 && jupyter labextension install @jupyterlab/geojson-extension \
 && jupyter labextension install @jupyterlab/katex-extension \
 && jupyter labextension install @jupyterlab/mathjax3-extension \
 && jupyter labextension install @jupyterlab/plotly-extension \
 && jupyter labextension install @jupyterlab/vega4-extension \
 && jupyter labextension install @lckr/jupyterlab_variableinspector \
 && jupyter labextension install @ryantam626/jupyterlab_black \
 && jupyter labextension install @jupyterlab/latex \
 && jupyter labextension install jupyter-matplotlib \
 && jupyter labextension install jupyterlab-dash \
 && jupyter labextension install jupyterlab-drawio \
 && jupyter labextension install jupyterlab_voyager \
 && jupyter labextension install ipysheet \
 && jupyter labextension install ipyvolume \
 && jupyter labextension install jupyter-threejs

# Add local files as late as possible to avoid cache busting
#COPY container/lab/start.sh /usr/local/bin/
#COPY container/lab/jupyter_notebook_config.py /etc/jupyter/

# RUN fix-permissions /etc/jupyter/

# Switch back to jovyan to avoid accidental container runs as root
# USER $NB_UID

RUN mkdir /notebooks

#CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root
CMD jupyter lab --port=8888 --no-browser --ip=0.0.0.0

EXPOSE 8888
WORKDIR /notebooks
VOLUME /notebooks

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
# CMD ["start-notebook.sh"]


#VOLUME /home/$NB_USER/notebooks
