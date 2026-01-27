# docker sandbox exec

**Description:** Execute a command inside a sandbox

**Usage:** `docker sandbox exec [OPTIONS] SANDBOX COMMAND [ARG...]`












## Description

Execute a command in a sandbox that was previously created with 'docker sandbox create'.

The command and any additional arguments are executed inside the sandbox container.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--detach` |  |  Detached mode: run command in the background |
| `--detach-keys` |  |  Override the key sequence for detaching a container |
| `-e`, `--env` |  |  Set environment variables |
| `--env-file` |  |  Read in a file of environment variables |
| `-i`, `--interactive` |  |  Keep STDIN open even if not attached |
| `--privileged` |  |  Give extended privileges to the command |
| `-t`, `--tty` |  |  Allocate a pseudo-TTY |
| `-u`, `--user` |  |  Username or UID (format: <name|uid>[:<group|gid>]) |
| `-w`, `--workdir` |  |  Working directory inside the container |






