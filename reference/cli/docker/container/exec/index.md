---
title: docker container exec
url: /reference/cli/docker/container/exec/
parent:
  title: docker container
  url: /reference/cli/docker/container/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker container
    url: /reference/cli/docker/container/
  - title: docker container exec
    url: /reference/cli/docker/container/exec/
next:
  title: docker container diff
  url: /reference/cli/docker/container/diff/
prev:
  title: docker container export
  url: /reference/cli/docker/container/export/
---

**Description:** Execute a command in a running container

**Usage:** `docker container exec [OPTIONS] CONTAINER COMMAND [ARG...]`

**Aliases:** `docker exec`



  

<blockquote
  
  class="admonition not-prose">
  <p><strong>Docker Debug 简介</strong></p>
<p>要轻松获取任何容器的调试 shell，请使用 <code>docker debug</code>。Docker Debug 是 <code>docker exec</code> 调试的替代方案。使用它，您可以获取任何容器或镜像的 shell，即使是精简的容器或镜像，也无需修改。此外，您还可以将其可自定义的工具箱中携带您最喜欢的调试工具。</p>
<p>立即探索 <a class="link" href="/reference/cli/docker/debug/">Docker Debug</a>。</p>

  </blockquote>

<!--
此页面由 Docker 的源代码自动生成。如果您想建议对此处显示的文本进行更改，请在 GitHub 上的源存储库中打开工单或拉取请求：

https://github.com/docker/cli
-->








## Description

The `docker exec` command runs a new command in a running container.

The command you specify with `docker exec` only runs while the container's
primary process (`PID 1`) is running, and it isn't restarted if the container
is restarted.

The command runs in the default working directory of the container.

The command must be an executable. A chained or a quoted command doesn't work.

- This works: `docker exec -it my_container sh -c "echo a && echo b"`
- This doesn't work: `docker exec -it my_container "echo a && echo b"`


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--detach` |  |  Detached mode: run command in the background |
| `--detach-keys` |  |  Override the key sequence for detaching a container |
| `-e`, `--env` |  | API 1.25+ Set environment variables |
| `--env-file` |  | API 1.25+ Read in a file of environment variables |
| `-i`, `--interactive` |  |  Keep STDIN open even if not attached |
| `--privileged` |  |  Give extended privileges to the command |
| `-t`, `--tty` |  |  Allocate a pseudo-TTY |
| `-u`, `--user` |  |  Username or UID (format: `<name|uid>[:<group|gid>]`) |
| `-w`, `--workdir` |  | API 1.35+ Working directory inside the container |



## Examples

### Run `docker exec` on a running container

First, start a container.

```console
$ docker run --name mycontainer -d -i -t alpine /bin/sh
```

This creates and starts a container named `mycontainer` from an `alpine` image
with an `sh` shell as its main process. The `-d` option (shorthand for `--detach`)
sets the container to run in the background, in detached mode, with a pseudo-TTY
attached (`-t`). The `-i` option is set to keep `STDIN` attached (`-i`), which
prevents the `sh` process from exiting immediately.

Next, execute a command on the container.

```console
$ docker exec -d mycontainer touch /tmp/execWorks
```

This creates a new file `/tmp/execWorks` inside the running container
`mycontainer`, in the background.

Next, execute an interactive `sh` shell on the container.

```console
$ docker exec -it mycontainer sh
```

This starts a new shell session in the container `mycontainer`.

### Set environment variables for the exec process (--env, -e) {#env}

Next, set environment variables in the current bash session.

The `docker exec` command inherits the environment variables that are set at the
time the container is created. Use the `--env` (or the `-e` shorthand) to
override global environment variables, or to set additional environment
variables for the process started by `docker exec`.

The following example creates a new shell session in the container `mycontainer`,
with environment variables `$VAR_A` set to `1`, and `$VAR_B` set to `2`.
These environment variables are only valid for the `sh` process started by that
`docker exec` command, and aren't available to other processes running inside
the container.

```console
$ docker exec -e VAR_A=1 -e VAR_B=2 mycontainer env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=f64a4851eb71
VAR_A=1
VAR_B=2
HOME=/root
```

### Escalate container privileges (--privileged) {#privileged}

See [`docker run --privileged`](/reference/cli/docker/container/run/#privileged).

### Set the working directory for the exec process (--workdir, -w) {#workdir}

By default `docker exec` command runs in the same working directory set when
the container was created.

```console
$ docker exec -it mycontainer pwd
/
```

You can specify an alternative working directory for the command to execute
using the `--workdir` option (or the `-w` shorthand):

```console
$ docker exec -it -w /root mycontainer pwd
/root
```

### Try to run `docker exec` on a paused container

If the container is paused, then the `docker exec` command fails with an error:

```console
$ docker pause mycontainer
mycontainer

$ docker ps

CONTAINER ID   IMAGE     COMMAND     CREATED          STATUS                   PORTS     NAMES
482efdf39fac   alpine    "/bin/sh"   17 seconds ago   Up 16 seconds (Paused)             mycontainer

$ docker exec mycontainer sh

Error response from daemon: Container mycontainer is paused, unpause the container before exec

$ echo $?
1
```



