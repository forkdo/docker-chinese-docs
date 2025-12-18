---
title: 高级配置
linkTitle: 高级
description: Docker 访问、卷挂载、环境变量、自定义模板和沙盒管理。
weight: 40
---

{{< summary-bar feature_name="Docker 沙盒" >}}

本指南涵盖在本地运行的沙盒代理的高级配置。

## 管理沙盒

### 重建沙盒

由于 Docker 强制每个工作区只能有一个沙盒，因此在给定目录中每次运行 `docker sandbox run <agent>` 时都会重用同一个沙盒。要创建一个全新的沙盒，您需要先删除现有的沙盒：

```console
$ docker sandbox ls  # 查找沙盒 ID
$ docker sandbox rm <sandbox-id>
$ docker sandbox run <agent>  # 创建新沙盒
```

### 何时重建沙盒

沙盒会记住其初始配置，不会从后续的 `docker sandbox run` 命令中获取更改。您必须重建沙盒才能修改以下内容：

- 环境变量（`-e` 标志）
- 卷挂载（`-v` 标志）
- Docker 套接字访问（`--mount-docker-socket` 标志）
- 凭据模式（`--credentials` 标志）

### 列出和检查沙盒

查看您所有的沙盒：

```console
$ docker sandbox ls
```

获取特定沙盒的详细信息：

```console
$ docker sandbox inspect <sandbox-id>
```

这会显示沙盒的配置，包括环境变量、卷和创建时间。

### 删除沙盒

删除特定沙盒：

```console
$ docker sandbox rm <sandbox-id>
```

一次性删除所有沙盒：

```console
$ docker sandbox rm $(docker sandbox ls -q)
```

这在项目完成或想要重新开始时很有用。

## 为代理提供 Docker 访问权限

挂载 Docker 套接字以使代理能够在容器内访问 Docker 命令。代理可以构建镜像、运行容器，并使用 Docker Compose 设置。

> [!CAUTION]
> 挂载 Docker 套接字会授予代理对您的 Docker 守护进程的完全访问权限，该权限在您的系统上具有 root 级别权限。代理可以启动或停止任何容器、访问卷，甚至可能逃逸沙盒。只有在完全信任代理处理的代码时才使用此选项。

### 启用 Docker 套接字访问

使用 `--mount-docker-socket` 标志：

```console
$ docker sandbox run --mount-docker-socket claude
```

这会将主机的 Docker 套接字（`/var/run/docker.sock`）挂载到容器中，使代理能够访问 Docker 命令。

> [!IMPORTANT]
> 代理可以看到并与主机上的所有容器交互，而不仅仅是沙盒内创建的容器。

### 示例：测试容器化应用程序

如果您的项目有 Dockerfile，代理可以构建并测试它：

```console
$ cd ~/my-docker-app
$ docker sandbox run --mount-docker-socket claude
```

示例对话：

```plaintext
您：“构建 Docker 镜像并运行测试”

Claude：*运行*
  docker build -t myapp:test .
  docker run myapp:test npm test
```

### 代理在启用 Docker 套接字访问后可以做什么

启用 Docker 访问后，代理可以：

- 使用 Docker Compose 启动多容器应用程序
- 为多个架构构建镜像
- 管理主机上的现有容器
- 验证 Dockerfile 并测试构建流程

## 环境变量

使用 `-e` 标志传递环境变量以配置沙盒环境：

```console
$ docker sandbox run \
  -e NODE_ENV=development \
  -e DATABASE_URL=postgresql://localhost/myapp_dev \
  -e DEBUG=true \
  claude
```

这些变量对容器中的所有进程都可用，包括代理和它运行的任何命令。使用多个 `-e` 标志来设置多个变量。

### 示例：开发环境设置

设置完整的开发环境：

```console
$ docker sandbox run \
  -e NODE_ENV=development \
  -e DATABASE_URL=postgresql://localhost/myapp_dev \
  -e REDIS_URL=redis://localhost:6379 \
  -e LOG_LEVEL=debug \
  claude
```

示例对话：

```plaintext
您：“运行数据库迁移并启动开发服务器”

Claude：*使用 DATABASE_URL 和其他环境变量*
  npm run migrate
  npm run dev
```

### 常见用例

测试用的 API 密钥：

```console
$ docker sandbox run \
  -e STRIPE_TEST_KEY=sk_test_xxx \
  -e SENDGRID_API_KEY=SG.xxx \
  claude
```

> [!CAUTION]
> 仅在沙盒中使用测试/开发 API 密钥，切勿使用生产密钥。

从 .env 文件加载：

沙盒不会自动从您的工作区加载 `.env` 文件，但您可以要求 Claude 使用它们：

```plaintext
您：“从 .env.development 加载环境变量并启动服务器”
```

Claude 可以使用 `dotenv` 工具或直接导入该文件。

## 卷挂载

挂载额外的目录或文件以共享数据，超出您的主要工作区。使用 `-v` 标志，语法为 `host-path:container-path`：

```console
$ docker sandbox run -v ~/datasets:/data claude
```

这使得 `~/datasets` 在容器内的 `/data` 处可用。代理可以在此位置读写文件。

只读挂载：

添加 `:ro` 以防止修改：

```console
$ docker sandbox run -v ~/configs/app.yml:/config/app.yml:ro claude
```

多个挂载：

使用多个 `-v` 标志来挂载多个位置：

```console
$ docker sandbox run \
  -v ~/datasets:/data:ro \
  -v ~/models:/models \
  -v ~/.cache/pip:/root/.cache/pip \
  claude
```

### 示例：机器学习工作流

设置具有共享数据集、模型存储和持久缓存的 ML 环境：

```console
$ docker sandbox run \
  -v ~/datasets:/data:ro \
  -v ~/models:/models \
  -v ~/.cache/pip:/root/.cache/pip \
  claude
```

这提供了对数据集的只读访问（防止意外修改）、对保存训练模型的读写访问，以及跨会话的持久 pip 缓存以实现更快的包安装。

示例对话：

```plaintext
您：“在 MNIST 数据集上训练模型并将其保存到 /models”

Claude：*运行*
  python train.py --data /data/mnist --output /models/mnist_model.h5
```

### 常见用例

共享配置文件：

```console
$ docker sandbox run -v ~/.aws:/root/.aws:ro claude
```

构建缓存：

```console
$ docker sandbox run \
  -v ~/.cache/go-build:/root/.cache/go-build \
  -v ~/go/pkg/mod:/go/pkg/mod \
  claude
```

自定义工具：

```console
$ docker sandbox run -v ~/bin:/shared-bin:ro claude
```

## 自定义模板

创建自定义沙盒模板以重用配置的环境。不必每次启动代理时都安装工具，而是构建一个预装所有内容的 Docker 镜像：

```dockerfile
# syntax=docker/dockerfile:1
FROM docker/sandbox-templates:claude-code
RUN <<EOF
curl -LsSf https://astral.sh/uv/install.sh | sh
. ~/.local/bin/env
uv tool install ruff@latest
EOF
ENV PATH="$PATH:~/.local/bin"
```

构建镜像后，使用 [`docker sandbox run --template`](/reference/cli/docker/sandbox/run#template) 标志启动基于该镜像的新沙盒。

```console
$ docker build -t my-dev-env .
$ docker sandbox run --template my-dev-env claude
```

### 使用标准镜像

您可以将标准 Docker 镜像用作沙盒模板，但它们不包含代理二进制文件、shell 配置或 Docker 沙盒模板提供的运行时依赖项。直接使用标准 Python 镜像会失败：

```console
$ docker sandbox run --template python:3-slim claude
The claude binary was not found in the sandbox; please check this is the correct sandbox for this agent.
```

要使用标准镜像，请创建一个 Dockerfile，在基础镜像之上安装代理二进制文件、依赖项和 shell 配置。当您需要特定的基础镜像（例如，精确的操作系统版本或具有特定构建工具的专业镜像）时，此方法很有意义。