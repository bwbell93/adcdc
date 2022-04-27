# Any docker-compose devcontainer (ADCDC)
The of this project is to allow any development workflow in a docker container.

# Installation and Usage
`pip install adcdc`

`adcdc create`
`adcdc build`
`adcdc run`

### Enable Tab Complete
Tab completion is provided natively by click for `bash`, `zsh`, and `fish` shells. See [](https://click.palletsprojects.com/en/8.1.x/shell-completion/#enabling-completion) and use
`ADCDC` and `adcdc` to replace `FOO_BAR` and `foo-bar` respectively.


## TODO Magic command
`adcdc magic` automatically walks you through the steps by making many assumptions.
Generally I recommend using this command only initially to do the setup.
First it checks the `.devcontainer` folder for `adcdc-docker-template` and `adcdc-config.yaml` files. 

## TODO Composing multiple adcdc templates together
TODO: we need to support this workflow, but it conflicts with the current config layout.
Often times you will want to keep project specific dev requirements (testing, doc generation, etc.) separate from your own development workflow (installing neovim, tmux, etc.).
For this use case, adcdc supports multiple adcdc-docker-templates and simply appends the contents of each list item sequentially.
To use this feature, change the `adcdc-docker-template` in your `adcdc-config.yaml` from a single value to a list.

# Developer Workflow
This project is developed using itself! This way it can serve as a living example of adcdc's capabilities. Otherwise there are minimal requirements so a `pip install -e .` in a conda or virtual env works well.
