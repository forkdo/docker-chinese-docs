---
title: Compose 的工作原理
weight: 10
description: 了解 Docker Compose 的工作原理，从应用模型到 Compose 文件和 CLI，通过一个详细的示例进行说明。
keywords: docker compose, compose.yaml, docker compose model, compose cli, multi-container application, compose example 
aliases:
- /compose/compose-file/02-model/
- /compose/compose-yaml-file/
- /compose/compose-application-model/
---

使用 Docker Compose，您需要使用 YAML 配置文件（称为 [Compose 文件](#the-compose-file)）来配置应用程序的服务，然后使用 [Compose CLI](#cli) 从配置中创建并启动所有服务。

Compose 文件，或 `compose.yaml` 文件，遵循 [Compose 规范](/reference/compose-file/_index.md) 提供的规则来定义多容器应用程序。这是正式 [Compose 规范](https://github.com/compose-spec/compose-spec) 的 Docker Compose 实现。

{{< accordion title="Compose 应用模型" >}}

应用程序的计算组件被定义为 [服务](/reference/compose-file/services.md)。服务是一个抽象概念，在平台上通过运行相同的容器镜像和配置，一次或多次实现。

服务通过 [网络](/reference/compose-file/networks.md) 相互通信。在 Compose 规范中，网络是建立连接在一起的服务中的容器之间 IP 路由的平台能力抽象。

服务将持久数据存储并共享到 [卷](/reference/compose-file/volumes.md) 中。规范将这种持久数据描述为具有全局选项的高级文件系统挂载。

某些服务需要依赖于运行时或平台的配置数据。为此，规范定义了一个专用的 [configs](/reference/compose-file/configs.md) 概念。在容器内部，configs 的行为类似于卷——它们作为文件挂载。然而，提供敏感数据的平台特定资源足够特殊，值得在 Compose 规范中拥有一个独立的概念和定义。

[secret](/reference/compose-file/secrets.md) 是配置数据的一种特定形式，用于不应在不考虑安全的情况下暴露的敏感数据。Secrets 作为挂载到其容器中的文件对服务可用，但提供敏感数据的平台特定资源足够特殊，值得在 Compose 规范中拥有一个独立的概念和定义。

> [!NOTE]
>
> 使用卷、configs 和 secrets，您可以在顶级进行简单声明，然后在服务级别添加更多平台特定信息。

项目是平台上应用程序规范的单个部署。项目的名称通过顶级 [`name`](/reference/compose-file/version-and-name.md) 属性设置，用于将资源分组在一起，并将它们与其他应用程序或具有不同参数的同一 Compose 指定应用程序的其他安装隔离。如果您在平台上创建资源，必须使用项目前缀资源名称并设置标签 `com.docker.compose.project`。

Compose 提供了一种方法，让您设置自定义项目名称并覆盖此名称，这样相同的 `compose.yaml` 文件可以在同一基础设施上部署两次，无需更改，只需传递不同的名称即可。

{{< /accordion >}} 

## Compose 文件

Compose 文件的默认路径是 `compose.yaml`（首选）或 `compose.yml`，放置在工作目录中。
Compose 也支持 `docker-compose.yaml` 和 `docker-compose.yml` 以保持与早期版本的向后兼容性。
如果两个文件都存在，Compose 优先选择规范的 `compose.yaml`。

您可以使用 [片段](/reference/compose-file/fragments.md) 和 [扩展](/reference/compose-file/extension.md) 来保持 Compose 文件的高效性和易维护性。

多个 Compose 文件可以 [合并](/reference/compose-file/merge.md) 在一起来定义应用模型。YAML 文件的组合是通过根据您设置的 Compose 文件顺序附加或覆盖 YAML 元素来实现的。
简单属性和映射会被最高顺序的 Compose 文件覆盖，列表则通过追加来合并。相对路径基于第一个 Compose 文件的父文件夹解析，当被合并的补充文件托管在其他文件夹中时也是如此。由于某些 Compose 文件元素既可以表示为单个字符串也可以表示为复杂对象，因此合并适用于展开形式。更多信息，请参见 [使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)。

如果您想重用其他 Compose 文件，或将应用模型的部分提取到单独的 Compose 文件中，您也可以使用 [`include`](/reference/compose-file/include.md)。如果您的 Compose 应用依赖于由不同团队管理的另一个应用，或者需要与他人共享，这非常有用。

## CLI

Docker CLI 让您通过 `docker compose` 命令及其子命令与 Docker Compose 应用进行交互。如果您使用 Docker Desktop，Docker Compose CLI 默认包含在内。

使用 CLI，您可以管理在 `compose.yaml` 文件中定义的多容器应用的生命周期。CLI 命令使您能够轻松地启动、停止和配置您的应用。

### 关键命令

启动 `compose.yaml` 文件中定义的所有服务：

```console
$ docker compose up
```

停止并移除正在运行的服务：

```console
$ docker compose down 
```

如果您想监控正在运行的容器的输出并调试问题，可以使用以下命令查看日志：

```console
$ docker compose logs
```

列出所有服务及其当前状态：

```console
$ docker compose ps
```

有关所有 Compose CLI 命令的完整列表，请参见 [参考文档](/reference/cli/docker/compose/_index.md)。

## 示例说明

以下示例说明了上述 Compose 概念。该示例是非规范性的。

考虑一个分为前端 Web 应用和后端服务的应用。

前端在运行时通过由基础设施管理的 HTTP 配置文件进行配置，提供外部域名，以及由平台的安全密钥存储注入的 HTTPS 服务器证书。

后端将数据存储在持久卷中。

两个服务在隔离的后端网络上相互通信，而前端也连接到前端网络并为外部使用暴露端口 443。

![Compose 应用示例](../images/compose-application.webp)

该示例应用由以下部分组成：

- 两个服务，由 Docker 镜像支持：`webapp` 和 `database`
- 一个密钥（HTTPS 证书），注入到前端
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

`docker compose up` 命令启动 `frontend` 和 `backend` 服务，创建必要的网络和卷，并将配置和密钥注入前端服务。

`docker compose ps` 提供您服务当前状态的快照，便于查看哪些容器正在运行、它们的状态以及它们使用的端口：

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## 接下来做什么

- [尝试快速入门指南](/manuals/compose/gettingstarted.md)
- [探索一些示例应用](https://github.com/docker/awesome-compose)
- [熟悉 Compose 规范](/reference/compose-file/_index.md)