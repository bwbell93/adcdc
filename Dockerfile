# Dockerfile used to develop this project, see README.md # Developer Workflow

# Python 3.6, the minimum supported by this project
FROM python:3.6-buster

# Create a docker user
RUN useradd -m docker
USER docker
WORKDIR /home/docker

# Install the adcdc package with develop
COPY --chown=docker:docker ./ /home/docker/adcdc
RUN pip install /home/docker/adcdc/
WORKDIR /home/docker/adcdc

CMD /bin/bash
