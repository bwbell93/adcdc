# TODO: this image must be filled by the cli
FROM adcdc:v0.1

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

# Install lunarvim
# requires gcc for treesitter
RUN apt-get update && apt-get install -y build-essential
# requires npm/node > 10 for lsp
RUN curl -sL https://deb.nodesource.com/setup_16.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get install -y nodejs
# requires yarn for lsp
RUN npm install -g yarn
# TODO: this user must be filled by the cli
USER docker
RUN curl https://raw.githubusercontent.com/lunarvim/lunarvim/master/utils/installer/install.sh > install.sh
# lvim requires input for installing. Thank you user277591. https://unix.stackexchange.com/a/427363
# yes node (for lsp), yes python, not rust
RUN { echo "y"; echo "y"; echo "n"; } | bash install.sh
# Alias lvim
RUN echo 'alias lvim="/home/docker/.local/bin/lvim"' >> ~/.bashrc

# TODO: cli should auto restore user & WORKDIR
WORKDIR /home/docker/code
CMD /bin/bash
