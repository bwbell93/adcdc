# Any docker-compose devcontainer (ADCDC)
The of this project is to allow any development workflow in a docker container.
The main premise is to create a `-dev` docker-compose service that links to a Dockerfile which
has a `FROM` command that links to the tag of the service you want to create a devcontainer for.
This can be done manually if you know what you're doing so the goal of this project is just a simple
CLI to automate the annoying parts of doing this manually.
There are a number of gotcha's with trying to do devcontainers that VSCode handles by default in
interesting ways. This project alleviates some of those but does not hide complexity from the user
(see Notes below).

Running:
1. Due to reasons in the notes you'll need to set the UID & GID like:
```bash
export UID=$(id -u) && export GID=$(id -g)
```
You can add these to your `.bashrc` if you'd like.

2. To run for the first time, you'll obviously need to build the container & devcontainer. 
You only need to rebuild when you make changes to these containers (either the target or dev).
```bash
docker-compose build <target>
docker-compose build <target>-dev
```
3. Then you can start a devcontainer and either choose to remove it after exiting `--rm` or leave it around and attach to it later.
```bash
# To remove after exiting, use --rm
docker-compose run --rm adcdc-dev
# Otherwise after running, attach with TODO
```

For everything in one command use:
```bash
export UID=$(id -u) && export GID=$(id -g) && docker-compose build adcdc-dev && docker-compose run --rm adcdc-dev
```

## Magic command
`adcdc magic` automatically walks you through the steps by making many assumptions.
Generally I recommend using this command only initially to do the setup.
First it checks the `.devcontainer` folder for `adcdc-docker-template` and `adcdc-config.yaml` files. 

## Composing multiple adcdc templates together
TODO: we need to support this workflow, but it conflicts with the current config layout.
Often times you will want to keep project specific dev requirements (testing, doc generation, etc.) separate from your own development workflow (installing neovim, tmux, etc.).
For this use case, adcdc supports multiple adcdc-docker-templates and simply appends the contents of each list item sequentially.
To use this feature, change the `adcdc-docker-template` in your `adcdc-config.yaml` from a single value to a list.

## Workflow
Without the CLI you can peruse the docker-compose.yaml & examples folders for the relevant files used.
The CLI just helps automate creating the docker-compose.yaml but you'll have to make your own config similar to the examples.

# NOTES
This isn't super easy, but it is possible with some knowledge and doing.
Below are some more detailed notes on why some decisions were made or what has to be done to get this working.

## Mounting volumes & UID/GID
Docker compose does not support pulling the $UID & $GID since they're not env variables. See: https://github.com/docker/compose/issues/2380.

You can simply do `export UID=$(id -u) && export GID=$(id -g)` or add these as env variables in your `.bashrc`

# Workflow Steps
Assuming you've installed this package and created an `adcdc-config.yaml` and `adcdc-docker-template` in a `.devcontainer` directory inside your project run the following command:
```bash
adcdc create ./devcontainer/adcdc-config.yaml
```

# Developer Workflow
This project is developed using itself! This way it can serve as a living example of adcdc's capabilities.
Check out `examples/bwbell93/` to see my configuration or create your own and run the [Workflow
Steps](#markdown-header-workflow-steps)
