FROM nvidia/cuda:10.2-cudnn7-runtime-ubuntu20.04

### Initial docker setup and creation of a docker user
RUN apt-get update
# Fix TZDATA prompt issue, https://serverfault.com/questions/949991/how-to-install-tzdata-on-a-ubuntu-docker-image
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -y sudo curl git tmux
RUN echo "docker ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers
# Add a docker user
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
USER docker
WORKDIR /home/docker
# Install python 3 through conda
# Set up conda
RUN curl -o ~/miniconda.sh -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
  chmod +x ~/miniconda.sh && \
  ~/miniconda.sh -b && \
  rm ~/miniconda.sh
ENV PATH /home/docker/miniconda3/bin:$PATH
### End initial setup
WORKDIR /home/docker/code

CMD /bin/bash
