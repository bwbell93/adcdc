FROM adcdc:v0.1
# NOTE: adcdc automatically fills the FROM tag

### DevContainer Install Steps
# Install neovim
USER root
WORKDIR /tmp
RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
RUN chmod 755 nvim.appimage
# by default, FUSE is not installed. Use the extra steps from nvim readme
RUN ./nvim.appimage --appimage-extract
RUN ./squashfs-root/AppRun --version
# Optional: exposing nvim globally
RUN mv squashfs-root / && ln -s /squashfs-root/AppRun /usr/bin/nvim
### End DevContainer Install Steps

# adcdc automatically restores the last WORKDIR or you can change it in adcdc-config.yaml
# adcdc automatically restores the last USER or you can change it in adcdc-config.yaml
# CMD/ENTRYPOINT is overridden in the adcdc-config.yaml

USER docker
WORKDIR /home/docker/adcdc
