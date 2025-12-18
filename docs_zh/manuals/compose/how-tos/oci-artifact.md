---
title: 将 Docker Compose 应用打包并部署为 OCI 构件
linkTitle: OCI 构件应用
weight: 110
description: 了解如何将 Docker Compose 应用打包、发布并从符合 OCI 标准的注册表中安全运行。
keywords: cli, compose, oci, docker hub, artificats, publish, package, distribute, docker compose oci support
params:
  sidebar:
    badge:
      color: green
      text: 新功能
---

{{< summary-bar feature_name="Compose OCI artifact" >}}

Docker Compose 支持使用 [OCI 构件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)，允许你将 Compose 应用打包并通过容器注册表分发。这意味着你可以将 Compose 文件与容器镜像一起存储，从而更轻松地对多容器应用进行版本控制、共享和部署。

## 将你的 Compose 应用发布为 OCI 构件

要将 Compose 应用作为 OCI 构件分发，你可以使用 `docker compose publish` 命令将其发布到符合 OCI 标准的注册表。这样，其他人就可以直接从注册表部署你的应用。

发布功能支持 Compose 的大部分组合功能，如覆盖、扩展或包含，[但有一些限制](#limitations)。

### 一般步骤

1. 导航到你的 Compose 应用目录。  
   确保你在包含 `compose.yml` 文件的目录中，或者使用 `-f` 标志指定你的 Compose 文件。

2. 在终端中，登录到你的 Docker 账户，以便在 Docker Hub 上进行身份验证。

   ```console
   $ docker login
   ```

3. 使用 `docker compose publish` 命令将你的应用作为 OCI 构件推送：

   ```console
   $ docker compose publish username/my-compose-app:latest
   ```
   如果你有多个 Compose 文件，运行：

   ```console
   $ docker compose -f compose-base.yml -f compose-production.yml publish username/my-compose-app:latest
   ```

### 高级发布选项

发布时，你可以传递额外的选项：
- `--oci-version`：指定 OCI 版本（默认自动确定）。
- `--resolve-image-digests`：将镜像标签固定到摘要。
- `--with-env`：在发布的 OCI 构件中包含环境变量。

Compose 会检查你的配置中是否包含敏感数据，并显示你的环境变量以确认你是否要发布它们。

```text
...
you are about to publish sensitive data within your OCI artifact.
please double check that you are not leaking sensitive data
AWS Client ID
"services.serviceA.environment.AWS_ACCESS_KEY_ID": xxxxxxxxxx
AWS Secret Key
"services.serviceA.environment.AWS_SECRET_ACCESS_KEY": aws"xxxx/xxxx+xxxx+"
Github authentication
"GITHUB_TOKEN": ghp_xxxxxxxxxx
JSON Web Token
"": xxxxxxx.xxxxxxxx.xxxxxxxx
Private Key
"": -----BEGIN DSA PRIVATE KEY-----
xxxxx
-----END DSA PRIVATE KEY-----
Are you ok to publish these sensitive data? [y/N]:y

you are about to publish environment variables within your OCI artifact.
please double check that you are not leaking sensitive data
Service/Config  serviceA
FOO=bar
Service/Config  serviceB
FOO=bar
QUIX=
BAR=baz
Are you ok to publish these environment variables? [y/N]: 
```

如果你拒绝，发布过程将停止，不会向注册表发送任何内容。

## 限制

将 Compose 应用发布为 OCI 构件有一些限制。如果 Compose 配置满足以下任一条件，则无法发布：
- 包含绑定挂载的服务
- 仅包含 `build` 部分的服务
- 包含使用 `include` 属性的本地文件。要成功发布，请确保任何包含的本地文件也已发布。然后你可以使用 `include` 引用这些文件，因为支持远程 `include`。

## 启动 OCI 构件应用

要启动使用 OCI 构件的 Docker Compose 应用，你可以使用 `-f`（或 `--file`）标志，后跟 OCI 构件引用。这允许你指定存储在注册表中作为 OCI 构件的 Compose 文件。

`oci://` 前缀表示 Compose 文件应从符合 OCI 标准的注册表中拉取，而不是从本地文件系统加载。

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

然后要运行 Compose 应用，使用 `docker compose up` 命令，`-f` 标志指向你的 OCI 构件：

```console
$ docker compose -f oci://docker.io/username/my-compose-app:latest up
```

### 故障排除

当你从 OCI 构件运行应用时，Compose 可能会显示需要你确认的警告消息，以限制运行恶意应用的风险：

- 使用的插值变量列表及其值
- 应用使用的环境变量列表
- 如果你的 OCI 构件应用使用其他远程资源，例如通过 [`include`](/reference/compose-file/include/)。

```text 
$ REGISTRY=myregistry.com docker compose -f oci://docker.io/username/my-compose-app:latest up

Found the following variables in configuration:
VARIABLE     VALUE                SOURCE        REQUIRED    DEFAULT
REGISTRY     myregistry.com      command-line   yes         
TAG          v1.0                environment    no          latest
DOCKERFILE   Dockerfile          default        no          Dockerfile
API_KEY      <unset>             none           no          

Do you want to proceed with these variables? [Y/n]:y

Warning: This Compose project includes files from remote sources:
- oci://registry.example.com/stack:latest
Remote includes could potentially be malicious. Make sure you trust the source.
Do you want to continue? [y/N]: 
```

如果你同意启动应用，Compose 会显示从 OCI 构件下载的所有资源的目录：

```text
...
Do you want to continue? [y/N]: y

Your compose stack "oci://registry.example.com/stack:latest" is stored in "~/Library/Caches/docker-compose/964e715660d6f6c3b384e05e7338613795f7dcd3613890cfa57e3540353b9d6d"
```

`docker compose publish` 命令支持非交互式执行，通过包含 `-y`（或 `--yes`）标志可以跳过确认提示：

```console
$ docker compose publish -y username/my-compose-app:latest
```

## 下一步

- [了解 Docker Hub 中的 OCI 构件](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md)
- [Compose publish 命令](/reference/cli/docker/compose/publish.md)
- [理解 `include`](/reference/compose-file/include.md)