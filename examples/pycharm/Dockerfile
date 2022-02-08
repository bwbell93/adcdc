# TODO: this image must be filled by the cli
FROM adcdc:v0.1

USER root
# install xserver for gui, java requires fonts
RUN apt update && apt install -y xserver-xorg libfontconfig1

# Install pycharm
WORKDIR /tmp
RUN curl -LO https://download.jetbrains.com/python/pycharm-community-2021.3.1.tar.gz
RUN tar xzf pycharm-community-2021.3.1.tar.gz -C /opt/

USER docker
# Alias charm to run pycharm
RUN echo 'alias charm="bash /opt/pycharm-community-2021.3.1/bin/pycharm.sh"' >> ~/.bashrc

# TODO: cli should auto restore user & WORKDIR
WORKDIR /home/docker/code
CMD /bin/bash
