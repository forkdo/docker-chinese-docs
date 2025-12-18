---
description: 了解如何在单个容器中运行多个进程
keywords: docker, supervisor, 进程管理
title: 在容器中运行多个进程
weight: 20
aliases:
  - /articles/using_supervisord/
  - /engine/admin/multi-service_container/
  - /engine/admin/using_supervisord/
  - /engine/articles/using_supervisord/
  - /config/containers/multi-service_container/
---

容器的主要运行进程是 `Dockerfile` 末尾的 `ENTRYPOINT` 和/或 `CMD`。最佳实践是通过每个容器运行一个服务来分离关注点。该服务可能会派生多个进程（例如，Apache Web 服务器启动多个工作进程）。拥有多个进程是可以的，但为了最大化 Docker 的优势，请避免一个容器负责整体应用程序的多个方面。你可以使用用户自定义网络和共享卷连接多个容器。

容器的主要进程负责管理它启动的所有进程。在某些情况下，主要进程设计不佳，在容器退出时无法优雅地“收割”（停止）子进程。如果你的进程属于这种情况，可以在运行容器时使用 `--init` 选项。`--init` 标志会在容器中插入一个微小的 init 进程作为主进程，并在容器退出时处理所有进程的收割。这种方式比在容器内使用完整的 init 进程（如 `sysvinit` 或 `systemd`）来管理进程生命周期更优。

如果你需要在容器内运行多个服务，可以通过几种不同的方式实现。

## 使用包装脚本

将所有命令放入一个包装脚本中，包含测试和调试信息。将包装脚本作为你的 `CMD` 运行。以下是一个简单的示例。首先，包装脚本：

```bash
#!/bin/bash

# 启动第一个进程
./my_first_process &

# 启动第二个进程
./my_second_process &

# 等待任一进程退出
wait -n

# 以第一个退出的进程状态退出
exit $?
```

然后是 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_first_process my_first_process
COPY my_second_process my_second_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## 使用 Bash 作业控制

如果你有一个需要首先启动并持续运行的主要进程，但临时需要运行一些其他进程（可能是为了与主要进程交互），那么可以使用 Bash 的作业控制。首先，包装脚本：

```bash
#!/bin/bash

# 开启 Bash 的作业控制
set -m

# 启动主要进程并将其放入后台
./my_main_process &

# 启动辅助进程
./my_helper_process

# my_helper_process 可能需要知道如何等待
# 主进程启动后再执行其工作并返回


# 现在我们将主要进程带回前台
# 并让它保持在那里
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

使用像 `supervisord` 这样的进程管理器。这比其他选项更复杂，因为它要求你将 `supervisord` 及其配置打包到镜像中（或基于包含 `supervisord` 的镜像），以及它管理的不同应用程序。然后启动 `supervisord`，它会为你管理进程。

以下 Dockerfile 示例展示了这种方法。示例假设在构建上下文的根目录下存在以下文件：

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

如果你想确保两个进程都将 `stdout` 和 `stderr` 输出到容器日志，可以在 `supervisord.conf` 文件中添加以下内容：

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