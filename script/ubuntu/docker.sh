# WARNING: These steps seem to not work anymore!
# reference
# - https://big-snow.github.io/docker-1/

#!/bin/bash

# Purge existign CUDA first
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# add-apt-repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# update and install
sudo apt-get update
sudo apt-get install docker-ce -y
#sudo apt-get install docker-ce=18.06.3~ce~3-0~ubuntu

# check status
sudo service docker status
# sudo docker run hello-world

