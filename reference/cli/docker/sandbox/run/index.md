---
title: docker sandbox run
url: /reference/cli/docker/sandbox/run/
parent:
  title: Docker 沙箱
  url: /reference/cli/docker/sandbox/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: Docker 沙箱
    url: /reference/cli/docker/sandbox/
  - title: docker sandbox run
    url: /reference/cli/docker/sandbox/run/
next:
  title: docker sandbox ls
  url: /reference/cli/docker/sandbox/ls/
prev:
  title: docker sandbox 删除
  url: /reference/cli/docker/sandbox/rm/
---

**Description:** Run an AI agent inside a sandbox

**Usage:** `docker sandbox run [options] <agent> [agent-options]`












## Description

Run an AI agent inside a sandbox with access to a host workspace.

The agent argument must be one of: claude, gemini.
Agent-specific options can be passed after the agent name.
If no workspace is specified via the "--workspace" option, the current working directory is used.
The workspace is exposed inside the sandbox at the same path as on the host.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--credentials` | `sandbox` |  Credentials source (host, sandbox, or none) |
| `-d`, `--detached` |  |  Create sandbox without running agent interactively |
| `-e`, `--env` |  |  Set environment variables (format: KEY=VALUE) |
| `--mount-docker-socket` |  |  Mount the host's Docker socket into the sandbox |
| `--name` |  |  Name for the sandbox |
| `-q`, `--quiet` |  |  Suppress verbose output |
| `-t`, `--template` |  |  Container image to use for the sandbox (default: agent-specific image)<br> |
| `-v`, `--volume` |  |  Bind mount a volume or host file or directory into the sandbox (format: hostpath:sandboxpath[:readonly|:ro])<br> |
| `-w`, `--workspace` | `.` |  Workspace path |



## Examples

### Run Claude in the current directory

```console
$ docker sandbox run claude
```

### Specify a workspace directory (-w, --workspace) {#workspace}

```text
--workspace PATH
```

Run the agent in a specific directory:

```console
$ docker sandbox run --workspace ~/projects/my-app claude
```

The workspace directory is mounted at the same absolute path inside the sandbox.

### Enable Docker-in-Docker (--mount-docker-socket) {#mount-docker-socket}

```text
--mount-docker-socket
```

Mount the host's Docker socket into the sandbox, giving the agent access to Docker commands:

```console
$ docker sandbox run --mount-docker-socket claude
```

> [!CAUTION]
> This grants the agent full access to your Docker daemon with root-level
> privileges. Only use when you trust the code being executed.

The agent can now build images, run containers, and manage your Docker environment.

### Set environment variables (-e, --env) {#env}

```text
--env KEY=VALUE
```

Pass environment variables to the sandbox:

```console
$ docker sandbox run \
  --env NODE_ENV=development \
  --env DATABASE_URL=postgresql://localhost/myapp \
  claude
```

### Mount additional volumes (-v, --volume) {#volume}

```text
--volume HOST_PATH:CONTAINER_PATH[:ro]
```

Mount additional directories or files into the sandbox:

```console
$ docker sandbox run \
  --volume ~/datasets:/data:ro \
  --volume ~/models:/models \
  claude
```

Use `:ro` or `:readonly` to make mounts read-only.

### Configure credential access (--credentials) {#credentials}

```text
--credentials MODE
```

Control how the agent accesses credentials. Valid modes are:

- `sandbox` (default): Authenticate once and share credentials across sandboxes
- `host`: Share host credentials (~/.gitconfig, ~/.ssh, etc.)
- `none`: Handle authentication manually

```console
$ docker sandbox run --credentials host claude
```

### Use a custom base image (-t, --template) {#template}

```text
--template IMAGE
```

Specify a custom container image to use as the sandbox base:

```console
$ docker sandbox run --template python:3-alpine claude
```

By default, each agent uses a pre-configured image. The `--template` option
lets you substitute a different image.

### Name the sandbox (--name) {#name}

```text
--name NAME
```

Assign a custom name to the sandbox for easier identification:

```console
$ docker sandbox run --name my-project claude
```



