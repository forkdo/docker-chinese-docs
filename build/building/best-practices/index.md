# 构建最佳实践


## 使用多阶段构建（Use multi-stage builds）

多阶段构建通过更清晰地分离镜像的构建与最终输出，让你减小最终镜像的大小。将你的
Dockerfile 指令拆分为不同的阶段，以确保最终输出仅包含运行应用程序所需的文件。

使用多个阶段还可以通过并行执行构建步骤，让构建更高效。

有关更多信息，参见 [多阶段构建](/manuals/build/building/multi-stage.md)。

### 创建可复用的阶段（Create reusable stages）

如果你有多个共同点很多的镜像，考虑创建一个包含共享组件的可复用阶段，并让你的独特阶段
基于它。Docker 只需构建一次公共阶段。这意味着你的派生镜像能更高效地使用 Docker 主机上的
内存，并加载得更快。

维护一个公共基础阶段（「不要重复自己」）也比维护多个做类似事情的不同的阶段更容易。

## 选择正确的基础镜像（Choose the right base image）

实现安全镜像的第一步是选择正确的基础镜像。选择镜像时，确保它来自受信任的来源，并保持较小。

- [Docker 官方镜像](https://hub.docker.com/search?badges=official)
  是一组经过策展的集合，拥有清晰的文档、倡导最佳实践，并定期更新。它们为许多应用程序
  提供了可信的起点。

- [Verified Publisher](https://hub.docker.com/search?badges=verified_publisher) 镜像
  是由与 Docker 合作的组织发布和维护的高质量镜像，Docker 会验证其仓库中内容的真实性。

- [Docker-Sponsored Open Source](https://hub.docker.com/search?badges=open_source)
  由 Docker 通过 [开源计划](../../docker-hub/image-library/trusted-content.md#docker-sponsored-open-source-software-images)
  赞助的开源项目发布和维护。

当你选择基础镜像时，留意表明该镜像属于这些计划的徽章。

![Docker Hub 官方镜像与验证发布者镜像](../images/hub-official-images.webp)

当从 Dockerfile 构建自己的镜像时，确保选择一个满足你需求的最小基础镜像。更小的基础镜像
不仅提供可移植性和快速下载，还能缩小镜像大小，并最大限度地减少通过依赖引入的漏洞数量。

你还应该考虑使用两类基础镜像：一类用于构建和单元测试，另一类（通常更精简）用于生产。在
开发的后期阶段，你的镜像可能不再需要编译器、构建系统和调试工具等构建工具。依赖最少的
小镜像可以显著降低攻击面。

## 经常重建你的镜像（Rebuild your images often）

Docker 镜像不可变。构建镜像就是在该时刻对镜像拍摄快照。这包括你在构建中使用的任何基础镜像、
库或其他软件。为了让镜像保持最新和安全，请定期使用更新的依赖重建镜像。

### 使用 --pull 获取最新的基础镜像（Use --pull to get fresh base images）

以下 Dockerfile 使用 `ubuntu` 镜像的 `24.04` 标签。随着时间的推移，随着发布者用新的安全补丁
和更新的库重建镜像，该标签可能解析为 `ubuntu` 镜像的不同底层版本。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:24.04
RUN apt-get -y update && apt-get install -y --no-install-recommends python3
```

要获取基础镜像的最新版本，请使用 `--pull` 标志：

```console
$ docker build --pull -t my-image:my-tag .
```

`--pull` 标志强制 Docker 检查并下载基础镜像的更新版本，即使本地已有缓存版本。

### 使用 --no-cache 进行干净构建（Use --no-cache for clean builds）

`--no-cache` 标志禁用构建缓存，强制 Docker 从零重建所有层：

```console
$ docker build --no-cache -t my-image:my-tag .
```

这会从 `apt-get` 或 `npm` 等包管理器获取依赖的最新可用版本。它不会拉取新的基础镜像——为此
请使用 `--pull`。

这两个标志用途不同，可以组合使用。同时使用两者可获取新的基础镜像并重新执行所有构建步骤：

```console
$ docker build --pull --no-cache -t my-image:my-tag .
```

另请考虑 [固定基础镜像版本](#pin-base-image-versions)。

## 使用 .dockerignore 排除（Exclude with .dockerignore）

要排除与构建无关的文件，而无需重新组织你的源代码仓库，请使用 `.dockerignore` 文件。该文件
支持类似于 `.gitignore` 文件的排除模式。

例如，要排除所有 `.md` 扩展名的文件：

```plaintext
*.md
```

有关创建该文件的信息，参见
[Dockerignore 文件](/manuals/build/concepts/context.md#dockerignore-files)。

## 创建临时容器（Create ephemeral containers）

你的 Dockerfile 定义的镜像应生成尽可能临时的容器。临时意味着容器可以被停止和销毁，然后以
绝对最小化的设置和配置重建并替换。

参考 _The Twelve-factor App_ 方法论下的 [Processes](https://12factor.net/processes)，以理解
以这种无状态方式运行容器的动机。

## 不要安装不必要的包（Don't install unnecessary packages）

避免仅仅因为可能有用就安装额外或不必要的包。例如，你不需要在数据库镜像中包含文本编辑器。

当你避免安装额外或不必要的包时，你的镜像复杂度更低、依赖更少、文件更小、构建时间更短。

## 解耦应用程序（Decouple applications）

每个容器应该只有一个关注点。将应用程序解耦到多个容器中，便于水平扩展和复用容器。例如，一个
Web 应用栈可能由三个独立的容器组成，每个容器各有其独特的镜像，以解耦的方式管理 Web 应用、
数据库和内存缓存。

将每个容器限制为一个进程是一个很好的经验法则，但并非硬性规定。例如，容器不仅可以
[带 init 进程生成](/manuals/engine/containers/multi-service_container.md)，某些程序也可能
自行生成额外的进程。例如，[Celery](https://docs.celeryq.dev/) 可以生成多个工作进程，而
[Apache](https://httpd.apache.org/) 可以为每个请求创建一个进程。

运用你的最佳判断，让容器尽可能整洁和模块化。如果容器相互依赖，你可以使用
[Docker 容器网络](/manuals/engine/network/_index.md) 来确保这些容器能够通信。

## 对多行参数排序（Sort multi-line arguments）

只要可能，按字母数字顺序对多行参数排序，以方便维护。这有助于避免包重复，并使列表更易于更新。
这也让 PR 更容易阅读和审查。在反斜杠（`\`）前加一个空格也会有帮助。

以下是 [buildpack-deps 镜像](https://github.com/docker-library/buildpack-deps) 的示例：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
  bzr \
  cvs \
  git \
  mercurial \
  subversion \
  && rm -rf /var/lib/apt/lists/*
```

## 利用构建缓存（Leverage build cache）

构建镜像时，Docker 会按指定的顺序逐步执行 Dockerfile 中的指令。对于每条指令，Docker 都会
检查是否能从构建缓存中复用该指令。

理解构建缓存的工作方式以及缓存何时失效，对于确保更快的构建至关重要。有关 Docker 构建缓存
以及如何优化构建的更多信息，参见 [Docker 构建缓存](/manuals/build/cache/_index.md)。

## 固定基础镜像版本（Pin base image versions）

镜像标签是可变的，意味着发布者可以更新一个标签以指向新的镜像。这很有用，因为它让发布者可以
更新标签以指向镜像的新版本。作为镜像使用者，这意味着当你重新构建镜像时会自动获得新版本。

例如，如果你在 Dockerfile 中指定 `FROM alpine:3.21`，`3.21` 会解析为 `3.21` 的最新补丁版本。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:3.21
```

在某个时间点，`3.21` 标签可能指向镜像的 3.21.1 版本。如果你在 3 个月后重建镜像，同一标签可能
指向不同的版本，例如 3.21.4。这种发布流程是最佳实践，大多数发布者都使用这种标记策略，但它
并非强制。

这样做的缺点是，你无法保证每次构建都获得相同的版本。这可能导致破坏性变更，也意味着你没有
正在使用的确切镜像版本的审计记录。

要完全确保供应链完整性，你可以将镜像版本固定到特定的摘要（digest）。通过将镜像固定到摘要，
即使发布者用新镜像替换了标签，你也保证始终使用相同的镜像版本。例如，以下 Dockerfile 将 Alpine
镜像固定为与之前相同的标签 `3.21`，但这次还带有摘要引用。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine:3.21@sha256:a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c
```

使用此 Dockerfile，即使发布者更新了 `3.21` 标签，你的构建仍会使用固定的镜像版本：
`a8560b36e8b8210634f77d9f7f9efd7ffa463e380b75e2e74aff4511df3ef88c`。

虽然这有助于避免意外变更，但每次想要更新时都必须手动查找并包含基础镜像版本的摘要，这也很繁琐。
而且你放弃了自动安全修复，而这很可能是你想获得的。

Docker Scout 默认的 [**最新的基础镜像** 策略](../../scout/policy/_index.md#up-to-date-base-images)
会检查你使用的基础镜像版本是否确实是最新版本。该策略还会检查 Dockerfile 中固定的摘要是否
对应正确的版本。如果发布者更新了你固定的镜像，策略评估会返回不合规状态，提示你应该更新镜像。

Docker Scout 还支持一个自动修复工作流，用于保持基础镜像最新。当有新的镜像摘要可用时，Docker Scout
可以自动在你的仓库上发起一个 pull request，将你的 Dockerfile 更新为使用最新版本。这比使用会自动
更改版本的标签更好，因为你掌控着，并且拥有变更发生时间和方式的审计记录。

有关使用 Docker Scout 自动更新基础镜像的更多信息，参见
[修复](/manuals/scout/policy/dashboard.md)。

## 在 CI 中构建并测试你的镜像（Build and test your images in CI）

当你向源码控制提交变更或创建 pull request 时，使用
[GitHub Actions](../ci/github-actions/_index.md) 或其他 CI/CD 流水线自动构建并标记 Docker 镜像
并测试它。

## Dockerfile 指令（Dockerfile instructions）

遵循以下关于如何正确使用 [Dockerfile 指令](/reference/dockerfile.md) 的建议，以创建高效且可维护的
Dockerfile。

> [!TIP]
>
> 要在 Visual Studio Code 中改进 Dockerfile 的 lint、代码导航和漏洞扫描，
> 请参阅 [Docker DX](https://marketplace.visualstudio.com/items?itemName=docker.docker) 扩展。

### FROM

只要可能，使用当前的官方镜像作为你镜像的基础。Docker 推荐 [Alpine 镜像](https://hub.docker.com/_/alpine/)，
因为它受严格控制且体积小（小于 6 MB），同时仍然是一个完整的 Linux 发行版。

有关 `FROM` 指令的更多信息，参见
[FROM 指令的 Dockerfile 参考](/reference/dockerfile.md#from)。

### LABEL

你可以向镜像添加标签，以帮助按项目组织镜像、记录许可信息、辅助自动化或其他目的。对于每个标签，
添加一行以 `LABEL` 开头、带一个或多个键值对的指令。以下示例展示了不同的可接受格式。说明性注释
内联在其中。

带空格的字符串必须加引号，或者空格必须被转义。内部的引号字符（`"`）也必须被转义。例如：

```dockerfile
# Set one or more individual labels
LABEL com.example.version="0.0.1-beta"
LABEL vendor1="ACME Incorporated"
LABEL vendor2=ZENITH\ Incorporated
LABEL com.example.release-date="2015-02-12"
LABEL com.example.version.is-production=""
```

一个镜像可以有多个标签。在 Docker 1.10 之前，建议将所有标签合并到一条 `LABEL` 指令中，以防止
创建额外的层。这已不再必要，但合并标签仍受支持。例如：

```dockerfile
# Set multiple labels on one line
LABEL com.example.version="0.0.1-beta" com.example.release-date="2015-02-12"
```

上面的示例也可以写成：

```dockerfile
# Set multiple labels at once, using line-continuation characters to break long lines
LABEL vendor=ACME\ Incorporated \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2015-02-12"
```

参见 [理解对象标签](/manuals/engine/manage-resources/labels.md)，了解关于可接受标签键和值的指南。
有关查询标签的信息，请参考
[管理对象上的标签](/manuals/engine/manage-resources/labels.md#manage-labels-on-objects) 中与过滤
相关的条目。另请参阅 Dockerfile 参考中的 [LABEL](/reference/dockerfile.md#label)。

### RUN

将长或复杂的 `RUN` 语句拆分为用反斜杠分隔的多行，使你的 Dockerfile 更具可读性、可理解性和可
维护性。

例如，你可以用 `&&` 运算符串联命令，并使用转义字符将长命令拆成多行。

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
```

默认情况下，反斜杠转义换行符，但你可以用 [`escape` 指令](/reference/dockerfile.md#escape) 更改它。

你还可以使用 here 文档（here documents）运行多个命令，而无需用管道运算符串联它们：

```dockerfile
RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
EOF
```

有关 `RUN` 的更多信息，参见 [RUN 指令的 Dockerfile 参考](/reference/dockerfile.md#run)。

#### apt-get

在基于 Debian 的镜像中，`RUN` 指令的一个常见用例是使用 `apt-get` 安装软件。因为 `apt-get` 安装
包，`RUN apt-get` 命令有几个需要注意的反直觉行为。

始终将 `RUN apt-get update` 与 `apt-get install` 放在同一条 `RUN` 语句中。例如：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo
```

在 `RUN` 语句中单独使用 `apt-get update` 会导致缓存问题，并使后续的 `apt-get install` 指令失败。
例如，以下问题会出现在以下 Dockerfile 中：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y --no-install-recommends curl
```

构建镜像后，所有层都在 Docker 缓存中。假设你后来通过添加额外的包来修改 `apt-get install`，如以下
Dockerfile 所示：

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y --no-install-recommends curl nginx
```

Docker 将初始指令和修改后的指令视为相同，并复用之前步骤的缓存。结果 `apt-get update` 没有执行，
因为构建使用了缓存版本。由于 `apt-get update` 没有运行，你的构建可能会获得 `curl` 和 `nginx` 包
的过时版本。

使用 `RUN apt-get update && apt-get install -y --no-install-recommends` 可确保你无需进一步编码或
手动干预即可安装最新的包版本。这种技术被称为缓存破坏（cache busting）。你也可以通过指定包版本
来实现缓存破坏，这被称为版本固定（version pinning）。例如：

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package-bar \
    package-baz \
    package-foo=1.3.*
```

版本固定强制构建检索特定版本，而不管缓存中的内容。这种技术还可以减少因所需包发生意外变更而导致
的失败。

下面是一个格式良好的 `RUN` 指令，展示了所有 `apt-get` 建议。

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    aufs-tools \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    libsqlite3-dev \
    mercurial \
    reprepro \
    ruby1.9.1 \
    ruby1.9.1-dev \
    s3cmd=1.1.* \
    && rm -rf /var/lib/apt/lists/*
```

`s3cmd` 参数指定了版本 `1.1.*`。如果镜像之前使用了较旧的版本，指定新版本会导致 `apt-get update`
的缓存破坏，并确保安装新版本。将每个包列在单独一行也可以防止包重复的错误。

此外，当你通过删除 `/var/lib/apt/lists` 清理 apt 缓存时，由于 apt 缓存不存储在层中，它减小了镜像
大小。由于 `RUN` 语句以 `apt-get update` 开头，包缓存总是在 `apt-get install` 之前刷新。

官方 Debian 和 Ubuntu 镜像 [自动运行 `apt-get clean`](https://github.com/debuerreotype/debuerreotype/blob/c9542ab785e72696eb2908a6dbc9220abbabef39/scripts/debuerreotype-minimizing-config#L87-L109)，
因此无需显式调用。

#### 使用管道（Using pipes）

某些 `RUN` 命令依赖使用管道字符（`|`）将一个命令的输出管道到另一个命令的能力，如下例所示：

```dockerfile
RUN wget -O - https://some.site | wc -l > /number
```

Docker 使用 `/bin/sh -c` 解释器执行这些命令，它只评估管道中最后一个操作的退出码来确定成功。在
上面的示例中，只要 `wc -l` 命令成功，此构建步骤就会成功并生成新镜像，即使 `wget` 命令失败。

如果你希望命令因管道中任何阶段的错误而失败，请在前面加上 `set -o pipefail &&`，以确保意外错误会
阻止构建无意中成功。例如：

```dockerfile
RUN set -o pipefail && wget -O - https://some.site | wc -l > /number
```

> [!NOTE]
>
> 并非所有 shell 都支持 `-o pipefail` 选项。
>
> 在基于 Debian 的镜像上的 `dash` shell 等情况下，考虑使用 `RUN` 的 _exec_ 形式显式选择
> 支持 `pipefail` 选项的 shell。例如：
>
> ```dockerfile
> RUN ["/bin/bash", "-c", "set -o pipefail && wget -O - https://some.site | wc -l > /number"]
> ```

### CMD

`CMD` 指令应该用于运行镜像中包含的软件及其任何参数。`CMD` 几乎总应该以 `CMD ["executable", "param1", "param2"]`
形式使用。因此，如果镜像用于服务（如 Apache 和 Rails），你会运行类似 `CMD ["apache2","-DFOREGROUND"]`
的内容。实际上，对于任何基于服务的镜像都推荐这种指令形式。

在大多数其他情况下，`CMD` 应该给定一个交互式 shell，如 bash、Python 和 perl。例如 `CMD ["perl", "-de0"]`、
`CMD ["python"]` 或 `CMD ["php", "-a"]`。使用这种形式意味着当你执行类似 `docker run -it python` 的命令时，
你会进入一个可用的 shell，随时可用。`CMD` 很少应该以 `CMD ["param", "param"]` 的方式与
[`ENTRYPOINT`](/reference/dockerfile.md#entrypoint) 结合使用，除非你和你的预期用户已经非常熟悉 `ENTRYPOINT`
的工作方式。

有关 `CMD` 的更多信息，参见 [CMD 指令的 Dockerfile 参考](/reference/dockerfile.md#cmd)。

### EXPOSE

`EXPOSE` 指令指示容器监听连接的端口。因此，你应该为你的应用程序使用常见、传统的端口。例如，包含
Apache Web 服务器的镜像会使用 `EXPOSE 80`，而包含 MongoDB 的镜像会使用 `EXPOSE 27017`，依此类推。

对于外部访问，你的用户可以用一个标志执行 `docker run`，指示如何将指定端口映射到他们选择的端口。
对于容器链接，Docker 提供从接收容器返回到源的路径的环境变量（例如 `MYSQL_PORT_3306_TCP`）。

有关 `EXPOSE` 的更多信息，参见 [EXPOSE 指令的 Dockerfile 参考](/reference/dockerfile.md#expose)。

### ENV

为了让新软件更容易运行，你可以使用 `ENV` 更新容器安装的软件的 `PATH` 环境变量。例如
`ENV PATH=/usr/local/nginx/bin:$PATH` 确保 `CMD ["nginx"]` 直接可用。

`ENV` 指令对于提供你想要容器化的服务所需的特定环境变量也很有用，例如 Postgres 的 `PGDATA`。

最后，`ENV` 也可用于设置常用版本号，以便版本升级更容易维护，如下例所示：

```dockerfile
ENV PG_MAJOR=9.3
ENV PG_VERSION=9.3.4
RUN curl -SL https://example.com/postgres-$PG_VERSION.tar.xz | tar -xJC /usr/src/postgres && …
ENV PATH=/usr/local/postgres-$PG_MAJOR/bin:$PATH
```

类似于在程序中使用常量变量而非硬编码值，这种方法让你更改一条 `ENV` 指令即可自动升级容器中的软件
版本。

每条 `ENV` 行都会创建一个新中间层，就像 `RUN` 命令一样。这意味着即使你在后续层中取消设置该环境
变量，它仍在此层中持久存在，并且其值可以被转储。你可以通过创建一个如下的 Dockerfile 然后构建它
来测试这一点。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ENV ADMIN_USER="mark"
RUN echo $ADMIN_USER > ./mark
RUN unset ADMIN_USER
```

```console
$ docker run --rm test sh -c 'echo $ADMIN_USER'

mark
```

要防止这种情况并取消设置环境变量，请使用带有 shell 命令的 `RUN` 命令，在一个层中完成变量的设置、
使用和取消设置。你可以用 `;` 或 `&&` 分隔命令。如果使用第二种方法，且其中一个命令失败，`docker build`
也会失败。这通常是个好主意。在 Linux Dockerfile 中使用 `\` 作为行继续符可提高可读性。你也可以将所有
命令放入一个 shell 脚本，并让 `RUN` 命令只运行该 shell 脚本。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN export ADMIN_USER="mark" \
    && echo $ADMIN_USER > ./mark \
    && unset ADMIN_USER
CMD sh
```

```console
$ docker run --rm test sh -c 'echo $ADMIN_USER'

```

有关 `ENV` 的更多信息，参见 [ENV 指令的 Dockerfile 参考](/reference/dockerfile.md#env)。

### ADD 或 COPY（ADD or COPY）

`ADD` 和 `COPY` 功能相似。`COPY` 支持将文件从 [构建上下文](/manuals/build/concepts/context.md) 或从
[多阶段构建](/manuals/build/building/multi-stage.md) 中的某个阶段基本复制到容器中。`ADD` 支持从远程
HTTPS 和 Git URL 获取文件，以及在从构建上下文添加文件时自动解压 tar 文件的功能。

在多阶段构建中，你多半想用 `COPY` 将文件从一个阶段复制到另一个阶段。如果你需要从构建上下文临时
向容器添加文件以执行 `RUN` 指令，通常可以用绑定挂载（bind mount）替代 `COPY` 指令。例如，为
`RUN pip install` 指令临时添加 `requirements.txt` 文件：

```dockerfile
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt
```

绑定挂载比 `COPY` 更高效，用于将构建上下文中的文件包含到容器中。注意绑定挂载的文件仅为单条 `RUN`
指令临时添加，不会持久化在最终镜像中。如果你需要将构建上下文中的文件包含在最终镜像中，请使用 `COPY`。

`ADD` 指令最适用于需要在构建中获取远程制品时。与手动使用 `wget` 和 `tar` 等方式添加文件相比，`ADD`
更好，因为它能确保更精确的构建缓存。`ADD` 还对远程资源的内置校验和验证，以及用于从
[Git URL](/reference/cli/docker/buildx/build/) 解析分支、标签和子目录的协议提供支持。

以下示例使用 `ADD` 下载 .NET 安装程序。结合多阶段构建，只有 .NET 运行时保留在最终阶段，没有中间
文件。

```dockerfile
# syntax=docker/dockerfile:1

FROM scratch AS src
ARG DOTNET_VERSION=8.0.0-preview.6.23329.7
ADD --checksum=sha256:270d731bd08040c6a3228115de1f74b91cf441c584139ff8f8f6503447cebdbb \
    https://dotnetcli.azureedge.net/dotnet/Runtime/$DOTNET_VERSION/dotnet-runtime-$DOTNET_VERSION-linux-arm64.tar.gz /dotnet.tar.gz

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0.0-preview.6-bookworm-slim-arm64v8 AS installer

# Retrieve .NET Runtime
RUN --mount=from=src,target=/src <<EOF
mkdir -p /dotnet
tar -oxzf /src/dotnet.tar.gz -C /dotnet
EOF

FROM mcr.microsoft.com/dotnet/runtime-deps:8.0.0-preview.6-bookworm-slim-arm64v8

COPY --from=installer /dotnet /usr/share/dotnet
RUN ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet
```

有关 `ADD` 或 `COPY` 的更多信息，请参阅：

- [ADD 指令的 Dockerfile 参考](/reference/dockerfile.md#add)
- [COPY 指令的 Dockerfile 参考](/reference/dockerfile.md#copy)

### ENTRYPOINT

`ENTRYPOINT` 的最佳用途是设置镜像的主命令，使该镜像可以像该命令一样运行，然后用 `CMD` 作为默认
标志。

以下是命令行工具 `s3cmd` 的镜像示例：

```dockerfile
ENTRYPOINT ["s3cmd"]
CMD ["--help"]
```

你可以使用以下命令运行镜像并显示命令的帮助：

```console
$ docker run s3cmd
```

或者，你可以使用正确的参数执行命令，如下例所示：

```console
$ docker run s3cmd ls s3://mybucket
```

这很有用，因为镜像名称可以像上面的命令所示那样兼作对二进制的引用。

`ENTRYPOINT` 指令也可以与辅助脚本结合使用，使其以上述类似方式运行，即使在启动工具可能需要多个
步骤时也是如此。

例如，[Postgres 官方镜像](https://hub.docker.com/_/postgres/) 使用以下脚本作为其 `ENTRYPOINT`：

```bash
#!/bin/sh
set -e

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"
```

此脚本使用 [the `exec` builtin](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#exec)，
使最终运行的应用程序成为容器的 PID 1。这让应用程序能接收发送到容器的任何 Unix 信号。有关更多信息，
参见 [`ENTRYPOINT` 参考](/reference/dockerfile.md#entrypoint)。

在以下示例中，辅助脚本被复制到容器，并在容器启动时通过 `ENTRYPOINT` 运行：

```dockerfile
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["postgres"]
```

此脚本让你以多种方式与 Postgres 交互。

它可以简单地启动 Postgres：

```console
$ docker run postgres
```

或者，你可以用它运行 Postgres 并向服务器传递参数：

```console
$ docker run postgres postgres --help
```

最后，你可以用它启动完全不同的工具，例如 Bash：

```console
$ docker run --rm -it postgres bash
```

有关 `ENTRYPOINT` 的更多信息，参见
[ENTRYPOINT 指令的 Dockerfile 参考](/reference/dockerfile.md#entrypoint)。

### VOLUME

你应该使用 `VOLUME` 指令暴露任何数据库存储区、配置存储，或你的 Docker 容器创建的文件和文件夹。强烈
建议你对镜像中任何可变的或用户可维护的部分使用 `VOLUME`。

有关 `VOLUME` 的更多信息，参见 [VOLUME 指令的 Dockerfile 参考](/reference/dockerfile.md#volume)。

### USER

如果服务可以在无特权下运行，请使用 `USER` 切换到非 root 用户。首先从 Dockerfile 中用类似以下示例的方式
创建用户和组：

```dockerfile
RUN groupadd -r postgres && useradd --no-log-init -r -g postgres postgres
```

> [!NOTE]
>
> 考虑显式指定 UID/GID。
>
> 镜像中的用户和组被分配了一个非确定性的 UID/GID，因为无论镜像是否重建，「下一个」UID/GID 都会被
> 分配。所以，如果这很关键，你应该分配一个显式的 UID/GID。

> [!NOTE]
>
> 由于 Go archive/tar 包处理稀疏文件的 [一个未解决的 bug](https://github.com/golang/go/issues/13548)，
> 在 Docker 容器内尝试创建具有非常大 UID 的用户可能导致磁盘耗尽，因为容器层中的 `/var/log/faillog` 被
> 填充了 NULL（\0）字符。一个解决方法是向 `useradd` 传递 `--no-log-init` 标志。Debian/Ubuntu 的 `adduser`
> 包装器不支持此标志。

避免安装或使用 `sudo`，因为它有不可预测的 TTY 和信号转发行为，可能导致问题。如果你确实需要类似 `sudo`
的功能（例如以 `root` 初始化守护进程，但以非 `root` 运行它），考虑使用
[“gosu”](https://github.com/tianon/gosu)。

最后，为了减少层和复杂性，避免频繁来回切换 `USER`。

有关 `USER` 的更多信息，参见 [USER 指令的 Dockerfile 参考](/reference/dockerfile.md#user)。

### WORKDIR

为了清晰和可靠，你应该始终为 `WORKDIR` 使用绝对路径。你还应该使用 `WORKDIR` 而不是大量使用像
`RUN cd … && do-something` 这样的指令，后者难以阅读、排查和维护。

有关 `WORKDIR` 的更多信息，参见 [`WORKDIR` 指令的 Dockerfile 参考](/reference/dockerfile.md#workdir)。

### ONBUILD

`ONBUILD` 命令在当前 Dockerfile 构建完成后执行。`ONBUILD` 在从当前镜像派生的任何子镜像中执行。把
`ONBUILD` 命令看作父 Dockerfile 给子 Dockerfile 的一条指令。

Docker 构建在子 Dockerfile 中任何命令之前执行 `ONBUILD` 命令。

`ONBUILD` 对将从给定镜像构建 `FROM` 的镜像很有用。例如，你会将 `ONBUILD` 用于语言栈镜像，该镜像在
Dockerfile 中构建用该语言编写的任意用户软件，如
[Ruby 的 `ONBUILD` 变体](https://github.com/docker-library/ruby/blob/c43fef8a60cea31eb9e7d960a076d633cb62ba8d/2.4/jessie/onbuild/Dockerfile)。

用 `ONBUILD` 构建的镜像应获得单独的标签。例如 `ruby:1.9-onbuild` 或 `ruby:2.0-onbuild`。

将 `ADD` 或 `COPY` 放入 `ONBUILD` 时要小心。如果新构建的上下文缺少要添加的资源，镜像会灾难性地失败。如上
所述添加单独的标签有助于缓解这种情况，让 Dockerfile 作者可以做出选择。

有关 `ONBUILD` 的更多信息，参见 [ONBUILD 指令的 Dockerfile 参考](/reference/dockerfile.md#onbuild)。

