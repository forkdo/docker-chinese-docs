# Bun 语言专项指南


这份 Bun 入门指南将教你如何使用 Docker 创建一个容器化的 Bun 应用。

> **致谢**
>
> Docker 在此感谢 [Pradumna Saraf](https://twitter.com/pradumna_saraf) 对本指南的贡献。

## 你将学到什么？

- 使用 Docker 容器化并运行 Bun 应用
- 使用容器搭建本地环境来开发 Bun 应用

## 前提条件

- 假定你对 JavaScript 有基本了解。
- 你需要熟悉容器、镜像、Dockerfile 等 Docker 概念。如果你是 Docker 新手，可以从
  [Docker 基础](/get-started/docker-concepts/the-basics/what-is-a-container.md)指南开始。

完成 Bun 入门模块后，你应该能够参照本指南提供的示例和说明，容器化你自己的 Bun 应用。

首先从容器化一个现有的 Bun 应用开始。

## Containerize a Bun application（容器化 Bun 应用）

### 前提条件

- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git
  客户端，但你可以使用任意客户端。

### 概述

长期以来，Node.js 一直是服务端 JavaScript 应用事实上的运行时。近年来，生态中涌现出
新的替代运行时，其中包括 [Bun 官网](https://bun.sh/)。与 Node.js 一样，Bun 也是一个
JavaScript 运行时。Bun 相对轻量，设计目标是快速且高效。

为什么要用 Docker 来开发 Bun 应用？有多个运行时可供选择固然很好，但随着运行时数量增加，
要在各种环境中一致地管理不同运行时及其依赖就变得困难。这正是 Docker 的用武之地。按需
创建和销毁容器是管理不同运行时及其依赖的绝佳方式。此外，由于 Bun 是相当新的运行时，
为它获得一致的开发环境也颇具挑战。Docker 可以帮你为 Bun 搭建一致的开发环境。

### 获取示例应用

克隆本指南使用的示例应用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

现在你的 `bun-docker` 目录中应该有以下内容。

```text
├── bun-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.js
│ └── README.md
```

### 创建 Dockerfile

在创建 Dockerfile 之前，你需要选择一个基础镜像。你可以使用
[Bun 官方 Docker 镜像](https://hub.docker.com/r/oven/bun)，或者使用
[Hardened Image 目录](https://hub.docker.com/hardened-images/catalog)中的
Docker Hardened Image（DHI）。

选择 DHI 的优势在于获得一个轻量且安全的生产就绪镜像。更多信息参阅
[Docker Hardened Images](https://docs.docker.com/dhi/)。

**Using Docker Hardened Images**



Bun 的 Docker Hardened Images（DHI）可在
[Docker Hardened Images 目录](https://hub.docker.com/hardened-images/catalog/dhi/bun)
中获取。你可以直接从 `dhi.io` 镜像仓库拉取 DHI。

1. 登录 DHI 镜像仓库：

   ```console
   $ docker login dhi.io
   ```

2. 拉取 Bun DHI，即 `dhi.io/bun:1`。本例中的标签（`1`）表示 Bun 最新的 1.x 版本。

   ```console
   $ docker pull dhi.io/bun:1
   ```

其他可用版本请参阅[目录](https://hub.docker.com/hardened-images/catalog/dhi/bun)。

```dockerfile
# Use the DHI Bun image as the base image
FROM dhi.io/bun:1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port on which the API will listen
EXPOSE 3000

# Run the server when the container launches
CMD ["bun", "server.js"]
```

**Using the official image**



使用官方 Docker 镜像很简单。在下面的 Dockerfile 中，你会看到 `FROM` 指令使用
`oven/bun` 作为基础镜像。

你可以在 [Docker Hub](https://hub.docker.com/r/oven/bun) 上找到该镜像。这是由
Bun 背后的公司 Oven 创建的 Bun 官方 Docker 镜像，可在 Docker Hub 上获取。

```dockerfile
# Use the official Bun image
FROM oven/bun:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port on which the API will listen
EXPOSE 3000

# Run the server when the container launches
CMD ["bun", "server.js"]
```



除了指定基础镜像，这个 Dockerfile 还：

- 把容器中的工作目录设为 `/app`。
- 把当前目录的内容复制到容器的 `/app` 目录。
- 暴露 3000 端口，API 在该端口监听请求。
- 最后，在容器启动时用 `bun server.js` 命令启动服务器。

### 运行应用

在 `bun-docker` 目录中，于终端运行以下命令。

```console
$ docker compose up --build
```

打开浏览器访问 [http://localhost:3000](http://localhost:3000) 查看应用。你会在浏览器中
看到消息 `{"Status" : "OK"}`。

在终端中按 `ctrl`+`c` 停止应用。

#### 在后台运行应用

你可以加上 `-d` 选项，让应用与终端分离后运行。在 `bun-docker` 目录中，于终端运行以下命令。

```console
$ docker compose up --build -d
```

打开浏览器访问 [http://localhost:3000](http://localhost:3000) 查看应用。

在终端中运行以下命令停止应用。

```console
$ docker compose down
```

## 使用容器进行 Bun 开发

### 前提条件

完成 [Containerize a Bun application](#containerize-a-bun-application)。

### 概述

在本节中，你将学习如何为容器化应用搭建开发环境。这包括：

- 配置 Compose，使其在你编辑并保存代码时自动更新正在运行的 Compose 服务

### 获取示例应用

克隆本指南使用的示例应用。打开终端，切换到你想工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

### 自动更新服务

使用 Compose Watch，在你编辑并保存代码时自动更新正在运行的 Compose 服务。有关
Compose Watch 的更多细节，参阅[使用 Compose
Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yml` 文件，然后添加 Compose Watch 指令。
下面的示例展示了如何把 Compose Watch 添加到 `compose.yml` 文件中。

```yaml {hl_lines="9-12",linenos=true}
services:
  server:
    image: bun-server
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    develop:
      watch:
        - action: rebuild
          path: .
```

运行以下命令，以 Compose Watch 方式运行你的应用。

```console
$ docker compose watch
```

现在，如果你修改 `server.js`，就能实时看到变化，而无需重新构建镜像。

要测试这一点，用你喜欢的文本编辑器打开 `server.js` 文件，把消息从 `{"Status" : "OK"}`
改为 `{"Status" : "Updated"}`。保存文件并刷新浏览器中的 `http://localhost:3000`。
你应该会看到更新后的消息。

在终端中按 `ctrl+c` 停止应用。

### 小结

在本节中，你还学习了如何使用 Compose Watch，在更新代码时自动重新构建并运行容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose file watch](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

