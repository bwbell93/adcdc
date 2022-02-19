# Dockerfile used to develop this project, see README.md # Developer Workflow

# 18.04 by default comes with python 3.6, the minimum supported by this project
FROM ubuntu:18.04

# Create a docker user
RUN useradd -m docker
USER docker
WORKDIR /home/docker

# Install the adcdc package with develop
COPY --chown=docker:docker ./ /home/docker/adcdc
# RUN pip install /home/docker/adcdc/setup.py
WORKDIR /home/docker/adcdc

CMD /bin/bash
