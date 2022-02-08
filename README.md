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

## Workflow
Without the CLI you can peruse the docker-compose.yaml & examples folders for the relevant files used.
The CLI just helps automate creating the docker-compose.yaml but you'll have to make your own config similar to the examples.

# NOTES
This isn't super easy, but it is possible with some knowledge and doing.
Below are some more detailed notes on why some decisions were made or what has to be done to get this working.

## Mounting volumes & UID/GID
Docker compose does not support pulling the $UID & $GID since they're not env variables. See: https://github.com/docker/compose/issues/2380.

You can simply do `export UID=$(id -u) && export GID=$(id -g)` or add these as env variables in your `.bashrc`
