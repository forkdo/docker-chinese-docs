---
title: Compose 的工作原理
weight: 10
description: 了解 Docker Compose 的工作原理，从应用程序模型到 Compose 文件和 CLI，同时通过一个详细的示例进行说明。
keywords: docker compose, compose.yaml, docker compose model, compose cli, multi-container application, compose example 
aliases:
- /compose/compose-file/02-model/
- /compose/compose-yaml-file/
- /compose/compose-application-model/

使用 Docker Compose 时，您需要使用一个名为 [Compose 文件](#the-compose-file) 的 YAML 配置文件来配置应用程序的服务，然后通过 [Compose CLI](#cli) 根据配置创建并启动所有服务。

Compose 文件（或 `compose.yaml` 文件）遵循 [Compose 规范](/reference/compose-file/_index.md) 中关于如何定义多容器应用程序的规则。这是 Docker Compose 对正式 [Compose 规范](https://github.com/compose-spec/compose-spec) 的实现。

{{< accordion title="Compose 应用程序模型" >}}

应用程序的计算组件被定义为 [服务](/reference/compose-file/services.md)。服务是一个抽象概念，在平台上通过运行相同的容器镜像和配置一次或多次来实现。

服务通过 [网络](/reference/compose-file/networks.md) 相互通信。在 Compose 规范中，网络是一个平台能力抽象，用于在连接在一起的服务中的容器之间建立 IP 路由。

服务将持久数据存储到 [卷](/reference/compose-file/volumes.md) 中。该规范将这种持久数据描述为具有全局选项的高级文件系统挂载。

某些服务需要依赖于运行时或平台的配置数据。为此，规范定义了一个专门的 [配置](/reference/compose-file/configs.md) 概念。在容器内部，配置的行为类似于卷——它们被挂载为文件。但是，配置在平台级别的定义方式有所不同。

[机密](/reference/compose-file/secrets.md) 是一种特定类型的配置数据，用于不应在没有安全考虑的情况下暴露的敏感数据。机密作为文件挂载到服务的容器中，但提供敏感数据的平台特定资源足够特殊，值得在 Compose 规范中拥有独立的概念和定义。

> [!NOTE]
>
> 使用卷、配置和机密时，您可以在顶层进行简单声明，然后在服务级别添加更多平台特定的信息。

项目是应用程序规范在平台上的单个部署。项目名称通过顶层的 [`name`](/reference/compose-file/version-and-name.md) 属性设置，用于将资源分组在一起，并将其与其他应用程序或具有不同参数的相同 Compose 规范应用程序的其他安装隔离开来。如果您要在平台上创建资源，必须按项目为资源名称添加前缀，并设置标签 `com.docker.compose.project`。

Compose 提供了一种设置自定义项目名称并覆盖此名称的方法，这样相同的 `compose.yaml` 文件就可以在同一基础设施上部署两次，而无需更改，只需传递一个不同的名称即可。

{{< /accordion >}} 

## Compose 文件

Compose 文件的默认路径是工作目录中的 `compose.yaml`（首选）或 `compose.yml`。
为了向后兼容早期版本，Compose 还支持 `docker-compose.yaml` 和 `docker-compose.yml`。如果这两个文件都存在，Compose 会优先选择标准的 `compose.yaml`。

您可以使用 [片段](/reference/compose-file/fragments.md) 和 [扩展](/reference/compose-file/extension.md) 来保持 Compose 文件的高效性和易维护性。

多个 Compose 文件可以 [合并](/reference/compose-file/merge.md) 在一起以定义应用程序模型。YAML 文件的组合是通过根据您设置的 Compose 文件顺序追加或覆盖 YAML 元素来实现的。
简单属性和映射会被最高优先级的 Compose 文件覆盖，列表则通过追加进行合并。相对路径基于第一个 Compose 文件的父文件夹进行解析，无论被合并的补充文件托管在哪个文件夹中。由于某些 Compose 文件元素既可以表示为单个字符串，也可以表示为复杂对象，因此合并适用于扩展形式。有关更多信息，请参阅 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

如果您想重用其他 Compose 文件，或者将应用程序模型的部分内容分解到单独的 Compose 文件中，您也可以使用 [`include`](/reference/compose-file/include.md)。如果您的 Compose 应用程序依赖于由其他团队管理的另一个应用程序，或者需要与其他人共享，这将非常有用。

## CLI

Docker CLI 允许您通过 `docker compose` 命令及其子命令与 Docker Compose 应用程序进行交互。如果您使用的是 Docker Desktop，则默认包含 Docker Compose CLI。

使用 CLI，您可以管理在 `compose.yaml` 文件中定义的多容器应用程序的生命周期。CLI 命令使您能够轻松启动、停止和配置应用程序。

### 关键命令 

要启动 `compose.yaml` 文件中定义的所有服务：

```console
$ docker compose up
```

要停止并移除正在运行的服务：

```console
$ docker compose down 
```

如果要监控正在运行的容器的输出并调试问题，可以使用以下命令查看日志： 

```console
$ docker compose logs
```

要列出所有服务及其当前状态：

```console
$ docker compose ps
```

有关所有 Compose CLI 命令的完整列表，请参阅 [参考文档](/reference/cli/docker/compose/_index.md)。

## 示例说明

以下示例说明了上述 Compose 概念。该示例是非规范性的。

考虑一个分为前端 Web 应用程序和后端服务的应用程序。

前端在运行时通过基础设施管理的 HTTP 配置文件进行配置，提供外部域名，并通过平台的安全机密存储注入 HTTPS 服务器证书。

后端将数据存储在持久卷中。

两个服务在隔离的后端网络上相互通信，而前端还连接到前端网络，并公开端口 443 以供外部使用。

![Compose 应用程序示例](../images/compose-application.webp)

示例应用程序由以下部分组成：

- 两个服务，由 Docker 镜像支持：`webapp` 和 `database`
- 一个机密（HTTPS 证书），注入到前端
- 一个配置（HTTP），注入到前端
- 一个持久卷，附加到后端
- 两个网络

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate

  backend:
    image: example/database
    volumes:
      - db-data:/etc/data
    networks:
      - back-tier

volumes:
  db-data:
    driver: flocker
    driver_opts:
      size: "10GiB"

configs:
  httpd-config:
    external: true

secrets:
  server-certificate:
    external: true

networks:
  # 这些对象的存在足以定义它们
  front-tier: {}
  back-tier: {}
```

`docker compose up` 命令启动 `frontend` 和 `backend` 服务，创建必要的网络和卷，并将配置和机密注入到前端服务中。

`docker compose ps` 提供了服务当前状态的快照，可以轻松查看哪些容器正在运行、它们的状态以及它们使用的端口：

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## 下一步 

- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
- [探索一些示例应用程序](https://github.com/docker/awesome-compose)
- [熟悉 Compose 规范](/reference/compose-file/_index.md)