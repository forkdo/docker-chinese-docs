# 在容器中运行多个进程

容器的主要运行进程是 `Dockerfile` 末尾的 `ENTRYPOINT` 和/或 `CMD`。最佳实践是通过每个容器运行一个服务来分离关注点。该服务可能会分叉成多个进程（例如，Apache Web 服务器会启动多个工作进程）。拥有多个进程是可以的，但为了充分利用 Docker 的优势，应避免一个容器负责应用程序的多个方面。您可以使用用户定义的网络和共享卷来连接多个容器。

容器的主进程负责管理它启动的所有进程。在某些情况下，主进程设计不佳，在容器退出时无法妥善处理子进程的“收割”（停止）。如果您的进程属于此类，可以在运行容器时使用 `--init` 选项。`--init` 标志会在容器中插入一个微小的 init 进程作为主进程，并在容器退出时处理所有进程的收割。以这种方式处理此类进程优于使用 `sysvinit` 或 `systemd` 等成熟的 init 进程来处理容器内的进程生命周期。

如果需要在容器内运行多个服务，可以通过几种不同的方式实现。

## 使用包装脚本

将所有命令放入一个包装脚本中，并包含测试和调试信息。将包装脚本作为您的 `CMD` 运行。以下是一个简单的示例。首先是包装脚本：

```bash
#!/bin/bash

# 启动第一个进程
./my_first_process &

# 启动第二个进程
./my_second_process &

# 等待任意进程退出
wait -n

# 以首先退出的进程的状态退出
exit $?
```

接下来是 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_first_process my_first_process
COPY my_second_process my_second_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## 使用 Bash 作业控制

如果您有一个需要首先启动并保持运行的主进程，但暂时需要运行一些其他进程（也许是为了与主进程交互），那么您可以使用 bash 的作业控制。首先是包装脚本：

```bash
#!/bin/bash

# 开启 bash 的作业控制
set -m

# 启动主进程并将其置于后台
./my_main_process &

# 启动辅助进程
./my_helper_process

# my_helper_process 可能需要知道如何等待主进程启动，
# 然后再执行其工作并返回

# 现在我们将主进程带回前台
# 并保持在那里
fg %1
```

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_main_process my_main_process
COPY my_helper_process my_helper_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## 使用进程管理器

使用像 `supervisord` 这样的进程管理器。这比其他选项更复杂，因为它要求您将 `supervisord` 及其配置捆绑到您的镜像中（或者将您的镜像建立在包含 `supervisord` 的镜像之上），以及它管理的不同应用程序。然后您启动 `supervisord`，它会为您管理进程。

以下 Dockerfile 示例展示了这种方法。该示例假设这些文件存在于构建上下文的根目录：

- `supervisord.conf`
- `my_first_process`
- `my_second_process`

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY my_first_process my_first_process
COPY my_second_process my_second_process
CMD ["/usr/bin/supervisord"]
```

如果您想确保两个进程都将它们的 `stdout` 和 `stderr` 输出到容器日志，可以将以下内容添加到 `supervisord.conf` 文件中：

```ini
[supervisord]
nodaemon=true
logfile=/dev/null
logfile_maxbytes=0

[program:app]
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0
redirect_stderr=true
```
