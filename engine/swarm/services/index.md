# 将服务部署到 swarm

Swarm 服务使用声明式模型，这意味着您需要定义服务的期望状态，并依赖 Docker 来维护该状态。该状态包括（但不限于）以下信息：

- 服务容器应运行的镜像名称和标签
- 参与服务的容器数量
- 是否向 swarm 外部的客户端暴露任何端口
- 服务是否应在 Docker 启动时自动启动
- 服务重启时的具体行为（例如是否使用滚动重启）
- 服务可以运行的节点的特性（例如资源限制和部署偏好）

有关 Swarm 模式的概述，请参见 [Swarm 模式关键概念](key-concepts.md)。有关服务如何工作的概述，请参见
[服务如何工作](how-swarm-mode-works/services.md)。

## 创建服务

要创建没有额外配置的单副本服务，您只需要提供镜像名称。以下命令启动一个具有随机生成名称且未发布端口的 Nginx 服务。这是一个简单的示例，因为您无法与该 Nginx 服务交互。

```console
$ docker service create nginx
```

服务被调度到可用节点上。要确认服务是否成功创建并启动，请使用 `docker service ls` 命令：

```console
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE                                                                                             PORTS
a3iixnklxuem        quizzical_lamarr    replicated          1/1                 docker.io/library/nginx@sha256:41ad9967ea448d7c2b203c699b429abe1ed5af331cd92533900c6d77490e0268
```

创建的服务并不总是立即运行。如果镜像不可用、没有节点满足您为服务配置的要求，或其他原因，服务可能处于挂起状态。有关更多信息，请参见
[挂起的服务](how-swarm-mode-works/services.md#pending-services)。

要为服务提供名称，请使用 `--name` 标志：

```console
$ docker service create --name my_web nginx
```

与独立容器一样，您可以通过在镜像名称后添加命令来指定服务容器应运行的命令。以下示例启动一个名为 `helloworld` 的服务，该服务使用 `alpine` 镜像并运行 `ping docker.com` 命令：

```console
$ docker service create --name helloworld alpine ping docker.com
```

您还可以指定服务要使用的镜像标签。以下示例修改了前一个示例，使用 `alpine:3.6` 标签：

```console
$ docker service create --name helloworld alpine:3.6 ping docker.com
```

有关镜像标签解析的更多详细信息，请参见
[指定服务应使用的镜像版本](#specify-the-image-version-a-service-should-use)。

### gMSA for Swarm

> [!NOTE]
>
> 此示例仅适用于 Windows 容器。

Swarm 现在允许使用 Docker 配置作为 gMSA 凭据规范，这是 Active Directory 认证应用程序的要求。这减少了将凭据规范分发到使用它们的节点的负担。

以下示例假定 gMSA 及其凭据规范（称为 credspec.json）已存在，并且要部署到的节点已正确配置为 gMSA。

要使用配置作为凭据规范，首先创建包含凭据规范的 Docker 配置：

```console
$ docker config create credspec credspec.json
```

现在，您应该有一个名为 credspec 的 Docker 配置，并且您可以使用此凭据规范创建服务。为此，请使用带有配置名称的 --credential-spec 标志，如下所示：

```console
$ docker service create --credential-spec="config://credspec" <your image>
```

服务在启动时使用 gMSA 凭据规范，但与典型的 Docker 配置（通过传递 --config 标志使用）不同，凭据规范不会挂载到容器中。

### 使用私有注册表上的镜像创建服务

如果您的镜像在需要登录的私有注册表上可用，请在登录后使用 `docker service create` 的 `--with-registry-auth` 标志。如果您的镜像存储在 `registry.example.com` 上，这是一个私有注册表，请使用以下命令：

```console
$ docker login registry.example.com

$ docker service  create \
  --with-registry-auth \
  --name my_service \
  registry.example.com/acme/my_image:latest
```

这将登录令牌从本地客户端传递到部署服务的 swarm 节点，使用加密的 WAL 日志。有了这些信息，节点可以登录到注册表并拉取镜像。

### 为托管服务账户提供凭据规范

在 Enterprise Edition 3.0 中，通过使用 Docker 配置功能集中分发和管理组托管服务账户（gMSA）凭据，安全性得到了改进。Swarm 现在允许使用 Docker 配置作为 gMSA 凭据规范，这减少了将凭据规范分发到使用它们的节点的负担。

> [!NOTE]
>
> 此选项仅适用于使用 Windows 容器的服务。

凭据规范文件在运行时应用，无需基于主机的凭据规范文件或注册表项 - 不会将 gMSA 凭据写入工作节点的磁盘。您可以在容器启动前使凭据规范对运行 swarm kit 工作节点的 Docker Engine 可用。当使用基于 gMSA 的配置部署服务时，凭据规范直接传递给该服务中容器的运行时。

`--credential-spec` 必须采用以下格式之一：

- `file://`：引用的文件必须存在于 docker 数据目录的 `CredentialSpecs` 子目录中，Windows 上默认为 `C:\ProgramData\Docker\`。例如，指定 `file://spec.json` 会加载 `C:\ProgramData\Docker\CredentialSpecs\spec.json`。
- `registry://<value-name>`：凭据规范从守护进程主机的 Windows 注册表中读取。
- `config://<config-name>`：配置名称在 CLI 中自动转换为配置 ID。
  使用指定 `config` 中包含的凭据规范。

以下简单示例从您的 Active Directory (AD) 实例中检索 gMSA 名称和 JSON 内容：

```console
$ name="mygmsa"
$ contents="{...}"
$ echo $contents > contents.json
```

确保您要部署到的节点已正确配置为 gMSA。

要使用配置作为凭据规范，请在名为 `credpspec.json` 的凭据规范文件中创建 Docker 配置。
您可以为 `config` 的名称指定任何名称。

```console
$ docker config create --label com.docker.gmsa.name=mygmsa credspec credspec.json
```

现在，您可以使用此凭据规范创建服务。使用带有配置名称的 `--credential-spec` 标志：

```console
$ docker service create --credential-spec="config://credspec" <your image>
```

服务在启动时使用 gMSA 凭据规范，但与典型的 Docker 配置（通过传递 --config 标志使用）不同，凭据规范不会挂载到容器中。

## 更新服务

您可以使用 `docker service update` 命令更改现有服务的几乎所有内容。当您更新服务时，Docker 会停止其容器并使用新配置重新启动它们。

由于 Nginx 是一个 Web 服务，如果您将端口 80 发布给 swarm 外部的客户端，它会工作得更好。您可以在创建服务时使用 `-p` 或 `--publish` 标志指定此设置。在更新现有服务时，该标志为 `--publish-add`。还有一个 `--publish-rm` 标志用于删除之前发布的端口。

假设上一节中的 `my_web` 服务仍然存在，请使用以下命令将其更新为发布端口 80。

```console
$ docker service update --publish-add 80 my_web
```

要验证是否成功，请使用 `docker service ls`：

```console
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE                                                                                             PORTS
4nhxl7oxw5vz        my_web              replicated          1/1                 docker.io/library/nginx@sha256:41ad9967ea448d7c2b203c699b429abe1ed5af331cd92533900c6d77490e0268   *:0->80/tcp
```

有关发布端口的更多信息，请参见
[发布端口](#publish-ports)。

您几乎可以更新现有服务的每个配置细节，包括它运行的镜像名称和标签。请参见
[创建后更新服务的镜像](#update-a-services-image-after-creation)。

## 删除服务

要删除服务，请使用 `docker service remove` 命令。您可以根据 `docker service ls` 命令的输出，通过其 ID 或名称删除服务。以下命令删除 `my_web` 服务。

```console
$ docker service remove my_web
```

## 服务配置详细信息

以下部分提供有关服务配置的详细信息。本主题不涵盖每个标志或场景。在几乎每个可以定义服务创建配置的地方，您也可以以类似的方式更新现有服务的配置。

请参见命令行参考
[`docker service create`](/reference/cli/docker/service/create.md) 和
[`docker service update`](/reference/cli/docker/service/update.md)，或运行这些命令并加上 `--help` 标志。

### 配置运行时环境

您可以为容器中的运行时环境配置以下选项：

* 使用环境变量，使用 `--env` 标志
* 使用 `--workdir` 标志配置容器内的工作目录
* 使用 `--user` 标志配置用户名或 UID

以下服务的容器具有设置为 `myvalue` 的环境变量 `$MYVAR`，从 `/tmp/` 目录运行，并以 `my_user` 用户身份运行。

```console
$ docker service create --name helloworld \
  --env MYVAR=myvalue \
  --workdir /tmp \
  --user my_user \
  alpine ping docker.com
```

### 更新现有服务运行的命令

要更新现有服务运行的命令，可以使用 `--args` 标志。以下示例更新名为 `helloworld` 的现有服务，使其运行 `ping docker.com` 命令，而不是之前运行的任何命令：

```console
$ docker service update --args "ping docker.com" helloworld
```

### 指定服务应使用的镜像版本

创建服务时，如果不指定要使用的镜像版本，服务将使用带有 `latest` 标签的版本。您可以以几种不同的方式强制服务使用镜像的特定版本，具体取决于您期望的结果。

镜像版本可以用几种不同的方式表示：

- 如果您指定标签，管理器（或 Docker 客户端，如果您使用
  [内容信任](../security/trust/_index.md)）会将该标签解析为摘要。当工作节点上收到创建容器任务的请求时，工作节点只看到摘要，而不是标签。

  ```console
  $ docker service create --name="myservice" ubuntu:16.04
  ```

  某些标签代表离散版本，例如 `ubuntu:16.04`。这类标签几乎总是随着时间的推移解析为稳定的摘要。建议尽可能使用这种类型的标签。

  其他类型的标签，例如 `latest` 或 `nightly`，可能会经常解析为新的摘要，具体取决于镜像作者更新标签的频率。不建议使用频繁更新的标签来运行服务，以防止不同的服务副本任务使用不同的镜像版本。

- 如果您根本不指定版本，按照惯例，镜像的 `latest` 标签会解析为摘要。工作节点在创建服务任务时使用此摘要的镜像。

  因此，以下两个命令是等效的：

  ```console
  $ docker service create --name="myservice" ubuntu

  $ docker service create --name="myservice" ubuntu:latest
  ```

- 如果您直接指定摘要，则在创建服务任务时始终使用该镜像的精确版本。

  ```console
  $ docker service create \
      --name="myservice" \
      ubuntu:16.04@sha256:35bc48a1ca97c3971611dc4662d08d131869daa692acb281c7e9e052924e38b1
  ```

创建服务时，镜像的标签会解析为标签在**服务创建时**指向的特定摘要。该服务的工作节点将永远使用那个特定的摘要，除非您明确使用 `service update` 和 `--image` 标志更新服务。如果您使用经常更改的标签（如 `latest`），此功能尤为重要，因为它确保所有服务任务都使用相同版本的镜像。

> [!NOTE]
>
> 如果启用了 [内容信任](../security/trust/_index.md)，客户端实际上会在联系 swarm 管理器之前将镜像的标签解析为摘要，以验证镜像是否已签名。
> 因此，如果您使用内容信任，swarm 管理器会收到已预先解析的请求。在这种情况下，如果客户端无法将镜像解析为摘要，请求将失败。

如果管理器无法将标签解析为摘要，每个工作节点负责将标签解析为摘要，不同的节点可能会使用不同版本的镜像。如果发生这种情况，将记录如下警告，将占位符替换为实际信息。

```text
unable to pin image <IMAGE-NAME> to digest: <REASON>
```

要查看镜像的当前摘要，请发出命令
`docker inspect <IMAGE>:<TAG>` 并查找 `RepoDigests` 行。以下是编写此内容时 `ubuntu:latest` 的当前摘要。为清晰起见，输出已截断。

```console
$ docker inspect ubuntu:latest
```

```json
"RepoDigests": [
    "ubuntu@sha256:35bc48a1ca97c3971611dc4662d08d131869daa692acb281c7e9e052924e38b1"
],
```

创建服务后，除非您显式运行
`docker service update` 并使用 `--image` 标志（如下所述），否则其镜像永远不会更新。其他更新操作（如扩展服务、添加或删除网络或卷、重命名服务或任何其他类型的更新操作）不会更新服务的镜像。

### 创建后更新服务的镜像

每个标签代表一个摘要，类似于 Git 哈希。某些标签（如 `latest`）经常更新以指向新的摘要。其他标签（如 `ubuntu:16.04`）代表已发布的软件版本，预计不会经常更新以指向新的摘要。创建服务时，它会受到约束，只能使用镜像的特定摘要创建任务，直到您使用 `service update` 和 `--image` 标志更新服务。

当您使用 `--image` 标志运行 `service update` 时，swarm 管理器会查询 Docker Hub 或您的私有 Docker 注册表，以获取标签当前指向的摘要，并更新服务任务以使用该摘要。

> [!NOTE]
>
> 如果您使用 [内容信任](../security/trust/_index.md)，Docker
> 客户端会解析镜像，swarm 管理器会接收镜像和摘要，而不是标签。

通常，管理器可以将标签解析为新的摘要，并且服务会更新，重新部署每个任务以使用新的镜像。如果管理器无法解析标签或发生其他问题，接下来的两个部分将概述预期情况。

#### 如果管理器解析了标签

如果 swarm 管理器可以将镜像标签解析为摘要，它会指示工作节点重新部署任务并使用该摘要的镜像。

- 如果工作节点已缓存该摘要的镜像，它会使用它。

- 如果没有，它会尝试从 Docker Hub 或私有注册表拉取镜像。

  - 如果成功，任务将使用新镜像部署。

  - 如果工作节点拉取镜像失败，服务将无法在该工作节点上部署。Docker 会尝试再次部署任务，可能会在不同的工作节点上。

#### 如果管理器无法解析标签

如果 swarm 管理器无法将镜像解析为摘要，一切并非都丢失：

- 管理器会指示工作节点使用带有该标签的镜像重新部署任务。

- 如果工作节点有本地缓存的镜像可以解析为该标签，它会使用该镜像。

- 如果工作节点没有本地缓存的镜像可以解析为该标签，工作节点会尝试连接到 Docker Hub 或私有注册表以拉取该标签的镜像。

  - 如果成功，工作节点会使用该镜像。

  - 如果失败，任务将无法部署，管理器会尝试再次部署任务，可能会在不同的工作节点上。

### 发布端口

创建 swarm 服务时，您可以通过两种方式向 swarm 外部的主机发布该服务的端口：

- [您可以依赖路由网格](#publish-a-services-ports-using-the-routing-mesh)。
  当您发布服务端口时，swarm 会在每个节点上的目标端口上使服务可访问，无论该节点上是否有服务的任务在运行。这不太复杂，是许多类型服务的正确选择。

- [您可以直接在运行服务的 swarm 节点上发布服务任务的端口](#publish-a-services-ports-directly-on-the-swarm-node)
  这绕过了路由网格，并提供了最大的灵活性，包括您开发自己的路由框架的能力。但是，您需要跟踪每个任务的运行位置并将请求路由到任务，并在节点之间进行负载均衡。

继续阅读以了解每种方法的更多信息和用例。

#### 使用路由网格发布服务的端口

要向外向 swarm 发布服务的端口，请使用
`--publish <PUBLISHED-PORT>:<SERVICE-PORT>` 标志。swarm 会在每个 swarm 节点上的发布端口上使服务可访问。如果外部主机连接到任何 swarm 节点上的该端口，路由网格会将其路由到任务。外部主机不需要知道服务任务的 IP 地址或内部使用的端口即可与服务交互。当用户或进程连接到服务时，任何运行服务任务的工作节点都可能响应。有关 swarm 服务网络连接的更多详细信息，请参见
[管理 swarm 服务网络](networking.md)。

##### 示例：在 10 节点 swarm 上运行三个任务的 Nginx 服务

假设您有一个 10 节点的 swarm，并在 10 节点 swarm 上部署一个运行三个任务的 Nginx 服务：

```console
$ docker service create --name my_web \
                        --replicas 3 \
                        --publish published=8080,target=80 \
                        nginx
```

三个任务在最多三个节点上运行。您不需要知道哪些节点正在运行任务；连接到 10 个节点中任何节点的端口 8080 都会连接到三个 `nginx` 任务之一。您可以使用 `curl` 测试这一点。以下示例假定 `localhost` 是 swarm 节点之一。如果不是，或者 `localhost` 无法解析为主机上的 IP 地址，请替换为主机的 IP 地址或可解析的主机名。

HTML 输出已截断：

```console
$ curl localhost:8080

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...truncated...
</html>
```

后续连接可能会路由到相同的 swarm 节点或不同的节点。

#### 直接在 swarm 节点上发布服务的端口

如果基于应用程序状态做出路由决策或需要完全控制将请求路由到服务任务的过程，使用路由网格可能不是您的应用程序的正确选择。要在运行服务的节点上直接发布服务的端口，请使用 `--publish` 标志的 `mode=host` 选项。

> [!NOTE]
>
> 如果您使用 `mode=host` 直接在 swarm 节点上发布服务的端口，并且还设置 `published=<PORT>`，这会创建一个隐式限制，即您只能在给定的 swarm 节点上运行该服务的一个任务。您可以通过指定 `published` 而不指定端口定义来绕过此限制，这会导致 Docker 为每个任务分配一个随机端口。
>
> 此外，如果您使用 `mode=host` 并且没有在 `docker service create` 上使用 `--mode=global` 标志，很难知道哪些节点正在运行服务以将工作路由到它们。

##### 示例：在每个 swarm 节点上运行 `nginx` Web 服务器服务

[nginx](https://hub.docker.com/_/nginx/) 是一个开源的反向代理、负载均衡器、HTTP 缓存和 Web 服务器。如果您使用路由网格运行 nginx 作为服务，连接到任何 swarm 节点上的 nginx 端口会显示（有效地）运行服务的随机 swarm 节点的网页。

以下示例在每个 swarm 节点上运行 nginx 作为服务，并在每个 swarm 节点上本地暴露 nginx 端口。

```console
$ docker service create \
  --mode global \
  --publish mode=host,target=80,published=8080 \
  --name=nginx \
  nginx:latest
```

您可以访问每个 swarm 节点上端口 8080 的 nginx 服务器。如果您向 swarm 添加节点，nginx 任务会在该节点上启动。您不能在绑定到端口 8080 的任何 swarm 节点上启动另一个服务或容器。

> [!NOTE]
>
> 这是一个纯粹说明性的示例。为多层服务创建应用程序层路由框架是复杂的，超出了本主题的范围。

### 将服务连接到覆盖网络

您可以使用覆盖网络在 swarm 内连接一个或多个服务。

首先，使用带有 `--driver overlay` 标志的 `docker network create` 命令在管理器节点上创建覆盖网络。

```console
$ docker network create --driver overlay my-network
```

在 swarm 模式下创建覆盖网络后，所有管理器节点都可以访问该网络。

您可以创建新服务并使用 `--network` 标志将服务附加到覆盖网络：

```console
$ docker service create \
  --replicas 3 \
  --network my-network \
  --name my-web \
  nginx
```

swarm 会将 `my-network` 扩展到运行服务的每个节点。

您还可以使用 `--network-add` 标志将现有服务连接到覆盖网络。

```console
$ docker service update --network-add my-network my-web
```

要从网络断开正在运行的服务，请使用 `--network-rm` 标志。

```console
$ docker service update --network-rm my-network my-web
```

有关覆盖网络和服务发现的更多信息，请参见
[将服务附加到覆盖网络](networking.md) 和
[Docker swarm 模式覆盖网络安全模型](/manuals/engine/network/drivers/overlay.md)。

### 授予服务访问机密的权限

要创建具有访问 Docker 管理机密权限的服务，请使用 `--secret` 标志。有关更多信息，请参见
[管理 Docker 服务的敏感字符串（机密）](secrets.md)

### 自定义服务的隔离模式

> [!IMPORTANT]
>
> 此设置仅适用于 Windows 主机，对 Linux 主机将被忽略。

Docker 允许您指定 swarm 服务的隔离模式。隔离模式可以是以下之一：

- `default`：使用为 Docker 主机配置的默认隔离模式，由 `-exec-opt` 标志或 `daemon.json` 中的 `exec-opts` 数组配置。如果守护进程未指定隔离技术，则 Windows Server 的默认值为 `process`，Windows 10 的默认值（也是唯一选择）为 `hyperv`。

- `process`：在主机上以单独的进程运行服务任务。

  > [!NOTE]
  >
  > `process` 隔离模式仅支持 Windows Server。
  > Windows 10 仅支持 `hyperv` 隔离模式。

- `hyperv`：以隔离的 `hyperv` 任务运行服务任务。这会增加开销，但提供更多的隔离。

您可以在创建或更新新服务时使用 `--isolation` 标志指定隔离模式。

### 控制服务部署

Swarm 服务为您提供了几种不同的方式来控制不同节点上服务的扩展和部署。

- 您可以指定服务是否需要运行特定数量的副本，或应在每个工作节点上全局运行。请参见
  [复制或全局服务](#replicated-or-global-services)。

- 您可以配置服务的
  [CPU 或内存要求](#reserve-memory-or-cpus-for-a-service)，服务只会在满足这些要求的节点上运行。

- [部署约束](#placement-constraints) 允许您配置服务，使其仅在设置了特定（任意）元数据的节点上运行，并在没有适当节点时导致部署失败。例如，您可以指定您的服务应仅在设置了任意标签 `pci_compliant` 为 `true` 的节点上运行。

- [部署偏好](#placement-preferences) 允许您为每个节点应用具有值范围的任意标签，并使用算法将服务的任务分散到这些节点上。目前，唯一支持的算法是 `spread`，它尝试均匀放置它们。例如，如果您用值从 1-10 的标签 `rack` 标记每个节点，然后指定基于 `rack` 的部署偏好，则在考虑其他部署约束、部署偏好和其他节点特定限制后，服务任务会尽可能均匀地分布在所有具有 `rack` 标签的节点上。

  与约束不同，部署偏好是尽力而为的，如果没有任何节点可以满足偏好，服务不会部署失败。如果您为服务指定部署偏好，当 swarm 管理器决定哪些节点应运行服务任务时，匹配该偏好的节点会被排名更高。其他因素，如服务的高可用性，也会影响哪些节点被调度运行服务任务。例如，如果您有 N 个具有 rack 标签的节点（然后还有一些其他节点），并且您的服务配置为运行 N+1 个副本，如果有一个节点没有服务，+1 会被调度到该节点上，无论该节点是否有 `rack` 标签。

#### 复制或全局服务

Swarm 模式有两种类型的服务：复制和全局。对于复制服务，您指定 swarm 管理器应调度到可用节点的副本任务数量。对于全局服务，调度器会在每个满足服务
[部署约束](#placement-constraints) 和
[资源要求](#reserve-memory-or-cpus-for-a-service) 的可用节点上放置一个任务。

您可以使用 `--mode` 标志控制服务类型。如果不指定模式，服务默认为 `replicated`。对于复制服务，您使用 `--replicas` 标志指定要启动的副本任务数量。例如，要启动具有 3 个副本任务的复制 nginx 服务：

```console
$ docker service create \
  --name my_web \
  --replicas 3 \
  nginx
```

要在每个可用节点上启动全局服务，请将 `--mode global` 传递给
`docker service create`。每当新节点可用时，调度器会在新节点上放置全局服务的任务。例如，要启动在 swarm 中每个节点上运行的 alpine 服务：

```console
$ docker service create \
  --name myservice \
  --mode global \
  alpine top
```

服务约束允许您设置节点在调度器将服务部署到节点之前必须满足的标准。您可以基于节点属性和元数据或引擎元数据对服务应用约束。有关约束的更多信息，请参见 `docker service create`
[CLI 参考](/reference/cli/docker/service/create.md)。

#### 为服务保留内存或 CPU

要为服务保留给定数量的内存或 CPU，请使用
`--reserve-memory` 或 `--reserve-cpu` 标志。如果没有可用节点可以满足要求（例如，如果您请求 4 个 CPU，而 swarm 中没有节点有 4 个 CPU），服务将保持挂起状态，直到有适当的节点可用于运行其任务。

##### 内存不足异常 (OOME)

如果您的服务尝试使用超过 swarm 节点可用内存的内存，您可能会遇到内存不足异常 (OOME)，容器或 Docker 守护进程可能会被内核 OOM 杀手杀死。为防止发生这种情况，请确保您的应用程序在具有足够内存的主机上运行，并参见
[了解内存不足的风险](/manuals/engine/containers/resource_constraints.md#understand-the-risks-of-running-out-of-memory)。

Swarm 服务允许您使用资源约束、部署偏好和标签，以确保您的服务部署到适当的 swarm 节点。

#### 部署约束

使用部署约束来控制可以分配服务的节点。在以下示例中，服务仅在设置了
[标签](manage-nodes.md#add-or-remove-label-metadata) `region` 为 `east` 的节点上运行。如果没有适当标记的节点可用，任务将等待，直到它们可用。`--constraint` 标志使用相等运算符（`==` 或 `!=`）。对于复制服务，所有服务可能运行在同一个节点上，或每个节点只运行一个副本，或某些节点不运行任何副本。对于全局服务，服务在每个满足部署约束和任何
[资源要求](#reserve-memory-or-cpus-for-a-service) 的节点上运行。

```console
$ docker service create \
  --name my-nginx \
  --replicas 5 \
  --constraint node.labels.region==east \
  nginx
```

您也可以在 `compose.yaml` 文件中使用 `constraint` 服务级键。

如果您指定多个部署约束，服务只会部署到满足所有约束的节点上。以下示例将服务限制为在所有 `region` 设置为 `east` 且 `type` 未设置为 `devel` 的节点上运行：

```console
$ docker service create \
  --name my-nginx \
  --mode global \
  --constraint node.labels.region==east \
  --constraint node.labels.type!=devel \
  nginx
```

您也可以将部署约束与部署偏好和 CPU/内存约束结合使用。请小心不要使用无法实现的设置。

有关约束的更多信息，请参见 `docker service create`
[CLI 参考](/reference/cli/docker/service/create.md)。

#### 部署偏好

虽然 [部署约束](#placement-constraints) 限制了服务可以运行的节点，但 _部署偏好_ 尝试以算法方式将任务放置在适当的节点上（目前，仅均匀分布）。例如，如果您为每个节点分配 `rack` 标签，您可以设置部署偏好，以按值均匀分布服务在具有 `rack` 标签的节点上。这样，如果您丢失一个机架，服务仍然在其它机架的节点上运行。

部署偏好不是严格强制的。如果您的偏好中指定的标签没有节点具有，服务将像没有设置偏好一样部署。

> [!NOTE]
>
> 全局服务的部署偏好被忽略。

以下示例设置偏好，以根据 `datacenter` 标签的值在节点之间分布部署。如果某些节点有
`datacenter=us-east`，而其他节点有 `datacenter=us-west`，服务将尽可能均匀地分布在两组节点上。

```console
$ docker service create \
  --replicas 9 \
  --name redis_2 \
  --placement-pref 'spread=node.labels.datacenter' \
  redis:7.4.0
```

> [!NOTE]
>
> 缺少用于分布的标签的节点仍然会接收任务分配。作为一个组，这些节点接收的任务与其他由特定标签值标识的组成比例。从某种意义上说，缺少标签等同于具有空值的标签。如果服务应仅在具有用于分布偏好的标签的节点上运行，则应将偏好与约束结合使用。

您可以指定多个部署偏好，并按遇到顺序处理它们。以下示例设置了具有多个部署偏好的服务。任务首先在各种数据中心之间分布，然后在机架之间分布（由各自的标签指示）：

```console
$ docker service create \
  --replicas 9 \
  --name redis_2 \
  --placement-pref 'spread=node.labels.datacenter' \
  --placement-pref 'spread=node.labels.rack' \
  redis:7.4.0
```

您也可以将部署偏好与部署约束或 CPU/内存约束结合使用。请小心不要使用无法实现的设置。

此图说明了部署偏好的工作方式：

![部署偏好如何工作](images/placement_prefs.png)

使用 `docker service update` 更新服务时，`--placement-pref-add`
在所有现有部署偏好之后附加新的部署偏好。
`--placement-pref-rm` 删除与参数匹配的现有部署偏好。

### 配置服务的更新行为

创建服务时，您可以指定滚动更新行为，以指定在运行 `docker service update` 时 swarm 应如何应用对服务的更改。您也可以将这些标志作为 `docker service update` 的参数指定。

`--update-delay` 标志配置服务任务或任务集更新之间的时间延迟。您可以将时间 `T` 描述为秒 `Ts`、分钟 `Tm` 或小时 `Th` 的组合。因此 `10m30s` 表示 10 分钟 30 秒的延迟。

默认情况下，调度器一次更新一个任务。您可以传递
`--update-parallelism` 标志来配置调度器同时更新的最大服务任务数。

当单个任务的更新返回 `RUNNING` 状态时，调度器通过继续更新另一个任务来继续更新，直到所有任务都更新。如果在更新期间的任何时间任务返回 `FAILED`，调度器会暂停更新。您可以使用 `docker service create` 或 `docker service update` 的 `--update-failure-action` 标志来控制行为。

在以下示例服务中，调度器一次最多应用 2 个副本的更新。当更新后的任务返回 `RUNNING` 或 `FAILED` 时，调度器在停止下一个任务更新之前等待 10 秒：

```console
$ docker service create \
  --replicas 10 \
  --name my_web \
  --update-delay 10s \
  --update-parallelism 2 \
  --update-failure-action continue \
  alpine
```

`--update-max-failure-ratio` 标志控制在更新期间可以失败的任务比例，然后整个更新被视为失败。例如，使用 `--update-max-failure-ratio 0.1 --update-failure-action pause`，在更新期间 10% 的任务失败后，更新将暂停。

如果任务未启动，或在 `--update-monitor` 标志指定的监控期内停止运行，则认为单个任务更新失败。`--update-monitor` 的默认值为 30 秒，这意味着任务在启动后前 30 秒内失败将计入服务更新失败阈值，之后的失败不计入。

### 回滚到服务的前一个版本

如果服务的更新版本未按预期工作，您可以使用 `docker service update` 的 `--rollback` 标志手动回滚到服务的前一个版本。这会将会话恢复到最近一次 `docker service update` 命令之前的配置。

其他选项可以与 `--rollback` 结合使用；例如，
`--update-delay 0s`，以在任务之间没有延迟的情况下执行回滚：

```console
$ docker service update \
  --rollback \
  --update-delay 0s
  my_web
```

您可以配置服务，以便在服务更新部署失败时自动回滚。请参见 [如果更新失败则自动回滚](#automatically-roll-back-if-an-update-fails)。

手动回滚在服务器端处理，这允许手动启动的回滚尊重新的回滚参数。请注意，`--rollback` 不能与 `docker service update` 的其他标志一起使用。

### 如果更新失败则自动回滚

您可以配置服务，以便如果服务更新导致重新部署失败，服务可以自动回滚到以前的配置。这有助于保护服务可用性。您可以在服务创建或更新时设置以下一个或多个标志。如果不设置值，则使用默认值。

| 标志                           | 默认 | 描述                                                                                                                                                                                                                                                                                                             |
|:-------------------------------|:--------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--rollback-delay`             | `0s`    | 回滚一个任务后等待回滚下一个任务的时间。值为 `0` 表示在第一个回滚任务部署后立即回滚第二个任务。                                                                                                                              |
| `--rollback-failure-action`    | `pause` | 当任务回滚失败时，是 `pause` 还是 `continue` 尝试回滚其他任务。                                                                                                                                                                                                                       |
| `--rollback-max-failure-ratio` | `0`     | 回滚期间可以容忍的失败率，指定为 0 到 1 之间的浮点数。例如，给定 5 个任务，失败率为 `.2` 将容忍一个任务回滚失败。值为 `0` 表示不容忍任何失败，而值为 `1` 表示容忍任意数量的失败。 |
| `--rollback-monitor`           | `5s`    | 每个任务回滚后监控失败的时间。如果任务在此时间段内停止，则认为回滚失败。                                                                                                                                                               |
| `--rollback-parallelism`       | `1`     | 并行回滚的最大任务数。默认情况下，一次回滚一个任务。值为 `0` 会导致所有任务并行回滚。                                                                                                                                                     |

以下示例配置了一个 `redis` 服务，如果 `docker service update` 部署失败，则自动回滚。两个任务可以并行回滚。任务在回滚后监控 20 秒以确保它们不退出，并容忍最多 20% 的失败率。使用 `--rollback-delay` 和 `--rollback-failure-action` 的默认值。

```console
$ docker service create --name=my_redis \
                        --replicas=5 \
                        --rollback-parallelism=2 \
                        --rollback-monitor=20s \
                        --rollback-max-failure-ratio=.2 \
                        redis:latest
```

### 授予服务访问卷或绑定挂载的权限

为了获得最佳性能和可移植性，您应避免将重要数据直接写入容器的可写层。您应改用数据卷或绑定挂载。此原则也适用于服务。

您可以在 swarm 中为服务创建两种类型的挂载：`volume` 挂载或 `bind` 挂载。无论使用哪种类型的挂载，在创建服务时都使用 `--mount` 标志进行配置，或在更新现有服务时使用 `--mount-add` 或 `--mount-rm` 标志。如果不指定类型，默认是数据卷。

#### 数据卷

数据卷是独立于容器存在的存储。数据卷在 swarm 服务下的生命周期与在容器下的生命周期类似。卷比任务和服务更持久，因此必须单独管理它们的删除。在部署服务之前可以创建卷，或者如果任务调度到特定主机时卷不存在，则根据服务
