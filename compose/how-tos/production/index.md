# 在生产环境中使用 Compose

当您在开发过程中使用 Compose 定义应用程序时，您可以使用此定义在不同的环境（如 CI、预发布和生产环境）中运行您的应用程序。

部署应用程序最简单的方法是在单台服务器上运行它，类似于您运行开发环境的方式。如果想要扩展应用程序，您可以在 Swarm 集群上运行 Compose 应用。

### 修改您的 Compose 文件以适应生产环境

您可能需要对应用程序配置进行更改，以使其准备好投入生产。这些更改可能包括：

- 移除任何应用程序代码的卷绑定，以便代码保留在容器内部，无法从外部更改
- 绑定到主机上的不同端口
- 不同地设置环境变量，例如减少日志的详细程度，或为外部服务（如电子邮件服务器）指定设置
- 指定重启策略，如 [`restart: always`](/reference/compose-file/services.md#restart)，以避免停机
- 添加额外的服务，例如日志聚合器

因此，考虑定义一个额外的 Compose 文件，例如 `compose.production.yaml`，其中包含特定于生产的配置细节。此配置文件只需要包含您希望从原始 Compose 文件中进行的更改。然后，将额外的 Compose 文件应用到原始的 `compose.yaml` 之上，以创建新的配置。

拥有第二个配置文件后，您可以使用 `-f` 选项来使用它：

```console
$ docker compose -f compose.yaml -f compose.production.yaml up -d
```

请参阅 [使用多个 Compose 文件](multiple-compose-files/_index.md) 以获取更完整的示例和其他选项。

### 部署更改

当您对应用程序代码进行更改时，请记住重建您的镜像并重新创建应用程序的容器。要重新部署名为 `web` 的服务，请使用：

```console
$ docker compose build web
$ docker compose up --no-deps -d web
```

第一条命令会重建 `web` 的镜像，然后停止、销毁并重新创建 `web` 服务。`--no-deps` 标志会阻止 Compose 重新创建 `web` 依赖的任何服务。

### 在单台服务器上运行 Compose

您可以通过适当设置 `DOCKER_HOST`、`DOCKER_TLS_VERIFY` 和 `DOCKER_CERT_PATH` 环境变量，使用 Compose 将应用程序部署到远程 Docker 主机。更多信息，请参阅 [预定义环境变量](environment-variables/envvars.md)。

设置好环境变量后，所有常规的 `docker compose` 命令无需进一步配置即可工作。

## 下一步

- [使用多个 Compose 文件](multiple-compose-files/_index.md)
