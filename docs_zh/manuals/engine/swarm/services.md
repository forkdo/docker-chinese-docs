---
description: 将服务部署到集群
keywords: 指南, 集群模式, 集群, 服务
title: 将服务部署到集群
toc_max: 4
---

Swarm 服务使用声明式模型，这意味着你定义服务的期望状态，然后依赖 Docker 来维护该状态。状态包括（但不限于）以下信息：

- 服务容器应运行的镜像名称和标签
- 有多少容器参与该服务
- 是否有任何端口暴露给集群外部的客户端
- 服务是否应在 Docker 启动时自动启动
- 服务重启时的特定行为（例如是否使用滚动重启）
- 服务可以运行的节点的特征（如资源约束和位置偏好）

有关 Swarm 模式的概述，请参阅 [Swarm 模式关键概念](key-concepts.md)。有关服务工作原理的概述，请参阅
[服务工作原理](how-swarm-mode-works/services.md)。

## 创建服务

要创建一个无额外配置的单副本服务，你只需提供镜像名称。此命令启动一个 Nginx 服务，具有随机生成的名称且无公开端口。这是一个简单的示例，因为你无法与 Nginx 服务交互。

```console
$ docker service create nginx
```

该服务被调度到一个可用节点上。要确认服务已成功创建并启动，请使用 `docker service ls` 命令：

```console
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE                                                                                             PORTS
a3iixnklxuem        quizzical_lamarr    replicated          1/1                 docker.io/library/nginx@sha256:41ad9967ea448d7c2b203c699b429abe1ed5af331cd92533900c6d77490e0268
```

创建的服务可能不会立即运行。如果其镜像不可用、没有节点满足你为服务配置的要求，或其他原因，服务可能处于待处理状态。有关更多信息，请参阅
[待处理服务](how-swarm-mode-works/services.md#pending-services)。

要为你的服务提供名称，请使用 `--name` 标志：

```console
$ docker service create --name my_web nginx
```

与独立容器一样，你可以指定服务容器应运行的命令，方法是在镜像名称后添加命令。此示例启动一个名为 `helloworld` 的服务，使用 `alpine` 镜像并运行命令 `ping docker.com`：

```console
$ docker service create --name helloworld alpine ping docker.com
```

你也可以指定服务应使用的镜像标签。此示例修改了前面的示例，使用 `alpine:3.6` 标签：

```console
$ docker service create --name helloworld alpine:3.6 ping docker.com
```

有关镜像标签解析的更多详细信息，请参阅
[指定服务应使用的镜像版本](#specify-the-image-version-a-service-should-use)。

### Swarm 的 gMSA

> [!NOTE]
>
> 此示例仅适用于 Windows 容器。

Swarm 现在允许将 Docker 配置用作 gMSA 凭据规范——这是 Active Directory 认证应用程序的要求。这减轻了将凭据规范分发到其使用节点的负担。

以下示例假设 gMSA 及其凭据规范（称为 credspec.json）已存在，并且部署到的节点已正确配置为 gMSA。

要使用配置作为凭据规范，首先创建包含凭据规范的 Docker 配置：

```console
$ docker config create credspec credspec.json
```

现在，你应该有了一个名为 credspec 的 Docker 配置，可以创建使用此凭据规范的服务。为此，使用 `--credential-spec` 标志和配置名称，如下所示：

```console
$ docker service create --credential-spec="config://credspec" <your image>
```

你的服务在启动时使用 gMSA 凭据规范，但与典型的 Docker 配置（通过 `--config` 标志传递）不同，凭据规范不会挂载到容器中。

### 使用私有注册表中的镜像创建服务

如果你的镜像在需要登录的私有注册表中可用，请在登录后使用 `--with-registry-auth` 标志与 `docker service create`。如果你的镜像存储在 `registry.example.com`（一个私有注册表）上，请使用如下命令：

```console
$ docker login registry.example.com

$ docker service  create \
  --with-registry-auth \
  --name my_service \
  registry.example.com/acme/my_image:latest
```

这会将登录令牌从你的本地客户端传递到服务部署的集群节点，使用加密的 WAL 日志。有了这些信息，节点能够登录注册表并拉取镜像。

### 为托管服务账户提供凭据规范

在企业版 3.0 中，通过使用 Docker 配置功能集中分发和管理 Group Managed Service Account (gMSA) 凭据来提高安全性。Swarm 现在允许将 Docker 配置用作 gMSA 凭据规范，这减轻了将凭据规范分发到其使用节点的负担。

> [!NOTE]
>
> 此选项仅适用于使用 Windows 容器的服务。

凭据规范文件在运行时应用，消除了对基于主机的凭据规范文件或注册表条目的需求——gMSA 凭据不会写入工作节点的磁盘。你可以在容器启动之前使 Docker Engine 运行的集群工作节点能够访问凭据规范。部署使用基于 gMSA 的配置的服务时，凭据规范直接传递给该服务中容器的运行时。

`--credential-spec` 必须采用以下格式之一：

- `file://<filename>`：引用的文件必须存在于 docker 数据目录的 `CredentialSpecs` 子目录中，默认情况下在 Windows 上为 `C:\ProgramData\Docker\`。例如，指定 `file://spec.json` 会加载 `C:\ProgramData\Docker\CredentialSpecs\spec.json`。
- `registry://<value-name>`：凭据规范从守护进程主机的 Windows 注册表中读取。
- `config://<config-name>`：配置名称在 CLI 中自动转换为配置 ID。
使用指定 `config` 中包含的凭据规范。

以下简单示例从你的 Active Directory (AD) 实例检索 gMSA 名称和 JSON 内容：

```console
$ name="mygmsa"
$ contents="{...}"
$ echo $contents > contents.json
```

确保你要部署到的节点已正确配置为 gMSA。

要使用配置作为凭据规范，请在凭据规范文件 `credpspec.json` 中创建一个 Docker 配置。
你可以为 `config` 的名称指定任何名称。

```console
$ docker config create --label com.docker.gmsa.name=mygmsa credspec credspec.json
```

现在你可以创建使用此凭据规范的服务。指定带有配置名称的 `--credential-spec` 标志：

```console
$ docker service create --credential-spec="config://credspec" <your image>
```

你的服务在启动时使用 gMSA 凭据规范，但与典型的 Docker 配置（通过 `--config` 标志传递）不同，凭据规范不会挂载到容器中。

## 更新服务

你可以使用 `docker service update` 命令更改现有服务的几乎所有内容。当你更新服务时，Docker 会停止其容器并使用新的配置重新启动它们。

由于 Nginx 是一个 Web 服务，如果将端口 80 公开给集群外部的客户端，它的工作效果会更好。你可以在创建服务时使用 `-p` 或 `--publish` 标志指定这一点。当更新现有服务时，标志是 `--publish-add`。还有一个 `--publish-rm` 标志用于删除之前公开的端口。

假设前一节中的 `my_web` 服务仍然存在，请使用以下命令将其更新为公开端口 80。

```console
$ docker service update --publish-add 80 my_web
```

要验证是否成功，请使用 `docker service ls`：

```console
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE                                                                                             PORTS
4nhxl7oxw5vz        my_web              replicated          1/1                 docker.io/library/nginx@sha256:41ad9967ea448d7c2b203c699b429abe1ed5af331cd92533900c6d77490e0268   *:0->80/tcp
```

有关如何公开端口的更多信息，请参阅
[公开端口](#publish-ports)。

你可以更新现有服务的几乎所有配置细节，包括它运行的镜像名称和标签。请参阅
[创建后更新服务的镜像](#update-a-services-image-after-creation)。

## 删除服务

要删除服务，请使用 `docker service remove` 命令。你可以通过其 ID 或名称（如 `docker service ls` 命令的输出所示）删除服务。以下命令删除 `my_web` 服务。

```console
$ docker service remove my_web
```

## 服务配置详情

以下部分提供有关服务配置的详细信息。此主题不涵盖每个标志或场景。在几乎所有你可以在创建服务时定义配置的情况下，你也可以以类似的方式更新现有服务的配置。

请参阅
[`docker service create`](/reference/cli/docker/service/create.md) 和
[`docker service update`](/reference/cli/docker/service/update.md) 的命令行参考，或使用 `--help` 标志运行其中一个命令。

### 配置运行时环境

你可以为容器中的运行时环境配置以下选项：

* 使用 `--env` 标志的环境变量
* 使用 `--workdir` 标志的容器内工作目录
* 使用 `--user` 标志的用户名或 UID

以下服务的容器具有一个环境变量 `$MYVAR` 设置为 `myvalue`，从 `/tmp/` 目录运行，并以 `my_user` 用户身份运行。

```console
$ docker service create --name helloworld \
  --env MYVAR=myvalue \
  --workdir /tmp \
  --user my_user \
  alpine ping docker.com
```

### 更新现有服务运行的命令

要更新现有服务运行的命令，你可以使用 `--args` 标志。以下示例更新一个名为 `helloworld` 的现有服务，使其运行命令 `ping docker.com`，而不是之前运行的任何命令：

```console
$ docker service update --args "ping docker.com" helloworld
```

### 指定服务应使用的镜像版本

当你创建服务而未指定要使用的镜像版本的任何详细信息时，服务使用标记为 `latest` 标签的版本。你可以通过几种不同的方式强制服务使用镜像的特定版本，具体取决于你的期望结果。

镜像版本可以用几种不同的方式表示：

- 如果你指定一个标签，管理器（或如果你使用
  [内容信任](../security/trust/_index.md)，则为 Docker 客户端）将该标签解析为摘要。当在工作节点上接收到创建容器任务的请求时，工作节点只看到摘要，而不是标签。

  ```console
  $ docker service create --name="myservice" ubuntu:16.04
  ```

  某些标签代表离散版本，如 `ubuntu:16.04`。像这样的标签几乎总是在一段时间内解析为稳定的摘要。建议你在可能的情况下使用这种类型的标签。

  其他类型的标签，如 `latest` 或 `nightly`，可能根据镜像作者更新标签的频率经常解析为新摘要。不建议对服务使用频繁更新的标签，以防止不同的服务副本任务使用不同的镜像版本。

- 如果你根本不指定版本，按约定，镜像的 `latest` 标签解析为摘要。工作节点在创建服务任务时使用此摘要。

  因此，以下两个命令是等效的：

  ```console
  $ docker service create --name="myservice" ubuntu

  $ docker service create --name="myservice" ubuntu:latest
  ```

- 如果你直接指定摘要，该特定版本的镜像在创建服务任务时始终被使用。

  ```console
  $ docker service create \
      --name="myservice" \
      ubuntu:16.04@sha256:35bc48a1ca97c3971611dc4662d08d131869daa692acb281c7e9e052924e38b1
  ```

当你创建服务时，镜像的标签解析为标签在**服务创建时**指向的特定摘要。该服务的每个工作节点永远使用该特定摘要，除非服务被明确更新。如果使用经常更改的标签（如 `latest`），此功能特别重要，因为它确保所有服务任务使用相同版本的镜像。

> [!NOTE]>
>
> 如果启用了 [内容信任](../security/trust/_index.md)，客户端实际上在联系集群管理器之前将镜像的标签解析为摘要，以验证镜像是否已签名。
> 因此，如果你使用内容信任，集群管理器会收到预解析的请求。
> 在这种情况下，如果客户端无法将镜像解析为摘要，请求将失败。

如果管理器无法将标签解析为摘要，每个工作节点负责将标签解析为摘要，不同的节点可能使用不同版本的镜像。如果发生这种情况，会记录如下警告，占位符替换为真实信息。

```text
unable to pin image <IMAGE-NAME> to digest: <REASON>
```

要查看镜像的当前摘要，请发出命令
`docker inspect <IMAGE>:<TAG>` 并查找 `RepoDigests` 行。以下是编写此内容时 `ubuntu:latest` 的当前摘要。输出已被截断以保持清晰。

```console
$ docker inspect ubuntu:latest
```

```json
"RepoDigests": [
    "ubuntu@sha256:35bc48a1ca97c3971611dc4662d08d131869daa692acb281c7e9e052924e38b1"
],
```

创建服务后，其镜像永远不会更新，除非你明确运行带有 `--image` 标志的 `docker service update`，如下所述。其他更新操作，如扩展服务、添加或删除网络或卷、重命名服务或任何其他类型的更新操作，都不会更新服务的镜像。

### 创建后更新服务的镜像

每个标签代表一个摘要，类似于 Git 哈希。某些标签（如 `latest`）经常更新以指向新摘要。其他标签（如 `ubuntu:16.04`）代表发布的软件版本，预计不会经常更新以指向新摘要。当你创建服务时，它被限制为使用镜像的特定摘要创建任务，直到你使用 `service update` 和 `--image` 标志更新服务。

当你使用 `--image` 标志运行 `service update` 时，集群管理器查询 Docker Hub 或你的私有 Docker 注册表，获取标签当前指向的摘要，并更新服务任务以使用该摘要。

> [!NOTE]
>
> 如果你使用 [内容信任](../security/trust/_index.md)，Docker
> 客户端解析镜像，集群管理器接收镜像和摘要，而不是标签。

通常，集群管理器可以将标签解析为新摘要，服务更新，重新部署每个任务以使用新镜像。如果管理器无法解析标签或发生其他问题，接下来的两节概述了预期情况。

#### 如果管理器解析标签

如果集群管理器可以将镜像标签解析为摘要，它会指示工作节点重新部署任务并使用该摘要处的镜像。

- 如果工作节点缓存了该摘要处的镜像，它会使用它。

- 如果没有，它会尝试从 Docker Hub 或私有注册表拉取镜像。

  - 如果成功，任务使用新镜像部署。

  - 如果工作节点拉取镜像失败，服务无法在该工作节点上部署。Docker 再次尝试部署任务，可能在不同的工作节点上。

#### 如果管理器无法解析标签

如果集群管理器无法将镜像解析为摘要，情况并非无望：

- 管理器指示工作节点使用该标签处的镜像重新部署任务。

- 如果工作节点有本地缓存的镜像解析到该标签，它会使用该镜像。

- 如果工作节点没有本地缓存的镜像解析到标签，工作节点尝试连接到 Docker Hub 或私有注册表以在该标签处拉取镜像。

  - 如果成功，工作节点使用该镜像。

  - 如果失败，任务无法部署，管理器再次尝试部署任务，可能在不同的工作节点上。

### 公开端口

当你创建 Swarm 服务时，可以通过两种方式将服务的端口公开给集群外部的主机：

- [你可以依赖路由网格](#publish-a-services-ports-using-the-routing-mesh)。
  当你公开服务端口时，Swarm 使服务在每个节点上的目标端口上可访问，无论该节点上是否有该服务的任务运行。这比较简单，适合许多类型的服务。

- [你可以直接在 Swarm 节点](#publish-a-services-ports-directly-on-the-swarm-node) 上公开服务任务的端口。
  这绕过了路由网格，提供了最大的灵活性，包括为你自己的路由框架开发的能力。但是，你需要负责跟踪每个任务在哪里运行，并将请求路由到任务，以及在节点之间进行负载均衡。

继续阅读以获取有关每种方法的更多信息和用例。

#### 使用路由网格公开服务的端口

要将服务的端口公开到集群外部，请使用
`--publish <PUBLISHED-PORT>:<SERVICE-PORT>` 标志。Swarm 使服务在每个 Swarm 节点上的公开端口上可访问。如果外部主机连接到任何 Swarm 节点上的该端口，路由网格会将其路由到任务。外部主机不需要知道服务任务的 IP 地址或内部使用的端口即可与服务交互。当用户或进程连接到服务时，任何运行服务任务的工作节点都可能响应。有关 Swarm 服务网络的更多详细信息，请参阅
[管理 Swarm