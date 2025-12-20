# 查看容器日志

`docker logs` 命令显示正在运行的容器记录的信息。`docker service logs` 命令显示服务中所有容器记录的信息。记录的信息以及日志的格式几乎完全取决于容器的端点命令。

默认情况下，`docker logs` 或 `docker service logs` 显示命令的输出，就像在终端中交互式运行该命令时一样。Unix 和 Linux 命令在运行时通常会打开三个 I/O 流，分别称为 `STDIN`、`STDOUT` 和 `STDERR`。`STDIN` 是命令的输入流，可能包含来自键盘的输入或来自另一个命令的输入。`STDOUT` 通常是命令的正常输出，而 `STDERR` 通常用于输出错误消息。默认情况下，`docker logs` 显示命令的 `STDOUT` 和 `STDERR`。要了解有关 I/O 和 Linux 的更多信息，请参阅 [Linux Documentation Project 关于 I/O 重定向的文章](https://tldp.org/LDP/abs/html/io-redirection.html)。

在某些情况下，除非采取额外步骤，否则 `docker logs` 可能无法显示有用的信息。

- 如果您使用将日志发送到文件、外部主机、数据库或其他日志后端的[日志驱动程序](configure.md)，并且禁用了["双重日志记录"](dual-logging.md)，则 `docker logs` 可能无法显示有用的信息。
- 如果您的镜像运行的是非交互式进程（例如 Web 服务器或数据库），该应用程序可能会将其输出发送到日志文件，而不是 `STDOUT` 和 `STDERR`。

在第一种情况下，您的日志会以其他方式处理，您可能选择不使用 `docker logs`。在第二种情况下，官方 `nginx` 镜像展示了一种解决方法，而官方 Apache `httpd` 镜像展示了另一种方法。

官方 `nginx` 镜像从 `/var/log/nginx/access.log` 创建一个符号链接到 `/dev/stdout`，并从 `/var/log/nginx/error.log` 创建另一个符号链接到 `/dev/stderr`，覆盖日志文件并导致日志被发送到相应的特殊设备。请参阅 [Dockerfile](https://github.com/nginxinc/docker-nginx/blob/8921999083def7ba43a06fabd5f80e4406651353/mainline/jessie/Dockerfile#L21-L23)。

官方 `httpd` 驱动程序更改了 `httpd` 应用程序的配置，以将其正常输出直接写入 `/proc/self/fd/1`（即 `STDOUT`），并将其错误写入 `/proc/self/fd/2`（即 `STDERR`）。请参阅 [Dockerfile](https://github.com/docker-library/httpd/blob/b13054c7de5c74bbaa6d595dbe38969e6d4f860c/2.2/Dockerfile#L72-L75)。

## 下一步

- 配置[日志驱动程序](configure.md)。
- 编写 [Dockerfile](/reference/dockerfile.md)。

- [使用日志记录驱动插件](/engine/logging/plugins/)

- [将 docker logs 与远程日志记录驱动程序结合使用](/engine/logging/dual-logging/)

- [自定义日志驱动输出](/engine/logging/log_tags/)

- [配置日志驱动程序](/engine/logging/configure/)

