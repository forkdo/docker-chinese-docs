---
description: 了解如何使用 Claude Code 和 Docker MCP Toolkit，通过 Docker Hub MCP 服务器从自然语言生成生产就绪的 Docker Compose 文件。
keywords: mcp, model context protocol, docker, docker desktop, claude code, docker hub, compose, automation
title: 使用 Claude Code 和 Docker MCP Toolkit 生成 Docker Compose 文件
summary: |
  本指南展示了如何将 Claude Code 连接到 Docker MCP Toolkit，使其能够搜索 Docker Hub 镜像并从自然语言生成完整的 Docker Compose 堆栈。
  你将启用 Docker Hub MCP 服务器，连接 Claude Code，验证 MCP 访问，并通过对话式提示创建一个 Node.js + PostgreSQL 堆栈。
tags: [ai]
aliases:
  - /guides/use-case/genai-claude-code-mcp/
params:
  time: 15 minutes
---

本指南介绍如何将 Claude Code 与 Docker MCP Toolkit 结合使用，使 Claude 能够实时搜索 Docker Hub 并从自然语言生成完整的 `docker-compose.yaml`。

你无需手动编写 YAML 或查找镜像标签，只需用自然语言描述你的堆栈——Claude 会通过 Model Context Protocol (MCP) 查询 Docker Hub 并构建生产就绪的 Compose 文件。

在本指南中，你将学习如何：

- 在 Docker Desktop 中启用 Docker MCP Toolkit  
- 添加 Docker Hub MCP 服务器  
- 连接 Claude Code 到 MCP 网关（GUI 或 CLI）  
- 在 Claude 中验证 MCP 连接性  
- 要求 Claude 生成并保存 Node.js + PostgreSQL 应用的 Compose 文件  
- 使用 `docker compose up` 立即部署  

---

## 使用 Claude Code 和 Docker MCP Toolkit 从自然语言生成 Docker Compose 文件


- **设置**：启用 MCP Toolkit → 添加 Docker Hub MCP 服务器 → 连接 Claude Code  
- **使用 Claude**：用简单英文描述你的堆栈  
- **自动化**：Claude 通过 MCP 查询 Docker Hub 并构建完整的 `docker-compose.yaml`  
- **部署**：运行 `docker compose up` → Node.js + PostgreSQL 在 `localhost:3000` 上运行  
- **优势**：零 YAML 编写。零镜像搜索。描述一次 → Claude 完成构建。

**预估时间**：约 15 分钟

---

## 1. 你要构建什么

目标很简单：使用 Claude Code 和 Docker MCP Toolkit 搜索 Docker Hub 镜像，并为 Node.js 和 PostgreSQL 设置生成完整的 Docker Compose 文件。

Model Context Protocol (MCP) 在 Claude Code 和 Docker Desktop 之间架起桥梁，让 Claude 实时访问 Docker 工具。你无需在 Docker、终端命令和 YAML 编辑器之间来回切换，只需描述你的需求，Claude 就会处理基础设施细节。

**为什么这很重要**：这种模式可以扩展到复杂的多服务设置、数据库迁移、网络、安全策略——全部通过对话式提示完成。

---

## 2. 前置要求

确保你已安装：

- Docker Desktop
- 启用支持 [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/#setup) 的 Docker Desktop 更新

- Claude Code

---

## 3. 安装 Docker Hub MCP 服务器

1. 打开 **Docker Desktop**  
1. 选择 **MCP Toolkit**  
1. 进入 **Catalog** 选项卡  
1. 搜索 **Docker Hub**  
1. 选择 **Docker Hub** MCP 服务器
1. 添加 MCP 服务器，然后打开 **Configuration** 选项卡
1. 输入你的 Docker Hub 用户名
1. [创建一个只读个人访问令牌](/security/access-tokens/#create-a-personal-access-token) 并在 **Secrets** 下输入你的访问令牌
1. 保存配置

![Docker Hub](./Images/catalog_docker_hub.avif "Docker Hub")

公共镜像无需凭据即可工作。对于私有仓库，你可以稍后添加 Docker Hub 用户名和令牌。

![Docker Hub Secrets](./Images/dockerhub_secrets.avif "Docker Hub Secrets")


---

## 4. 将 Claude Code 连接到 Docker MCP Toolkit

你可以通过 Docker Desktop 或 CLI 连接。

### 选项 A. 使用 Docker Desktop 连接

1. 打开 **MCP Toolkit**  
1. 进入 **Clients** 选项卡  
1. 找到 **Claude Code**  
1. 选择 **Connect**

![Docker Connection](./Images/docker-connect-claude.avif)

### 选项 B. 使用 CLI 连接

```console
$ claude mcp add MCP_DOCKER -s user -- docker mcp gateway run
```

---

## 5. 在 Claude Code 中验证 MCP 服务器

1. 导航到你的项目文件夹：

```console
$ cd /path/to/project
```

1. 启动 Claude Code：

```console
$ claude
```

1. 在输入框中输入：

```console
/mcp
```

你应该看到：

- MCP 网关（例如 `MCP_DOCKER`）
- Docker Hub MCP 服务器提供的工具

![mcp-docker](./Images/mcp-servers.avif)

如果没有，请重启 Claude Code 或检查 Docker Desktop 以确认连接。

---

## 6. 创建一个基本的 Node.js 应用

Claude Code 在检查真实项目时能生成更准确的 Compose 文件。现在设置应用代码，以便代理稍后可以绑定挂载它。

在项目文件夹内，创建一个名为 `app` 的文件夹：

```console
$ mkdir app
$ cd app
$ npm init -y
$ npm install express
```

创建 `index.js`：

```console
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Node.js, Docker, and MCP Toolkit are working together!");
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
```

在 `package.json` 中添加启动脚本：

```console
"scripts": {
  "start": "node index.js"
}
```

准备就绪后返回项目根目录（`cd ..`）。

---

## 7. 要求 Claude Code 设计你的 Docker Compose 堆栈

将以下消息粘贴到 Claude Code 中：

```console
使用 Docker Hub MCP 服务器：

在 Docker Hub 中搜索官方 Node.js 镜像和 PostgreSQL 镜像。
选择稳定的、常用标签，如 Node LTS 版本和最近的主要 Postgres 版本。

生成一个 Docker Compose 文件（`docker-compose.yaml`），包含：
- app:
  - 在端口 3000 上运行
  - 将现有的 ./app 目录绑定挂载到 /usr/src/app
  - 设置 /usr/src/app 为工作目录并运行 `npm install && npm start`
- db: 在端口 5432 上运行，使用命名卷

包含：
- Postgres 的环境变量
- 共享桥接网络
- 适当的健康检查
- 使用标签 + 索引摘要固定镜像版本
```

Claude 将通过 MCP 搜索镜像，检查 `app` 目录，并生成一个挂载和运行你本地代码的 Compose 文件。

---

## 8. 保存生成的 Docker Compose 文件

告诉 Claude：

```console
将最终的 Docker Compose 文件（docker-compose.yaml）保存到当前项目目录中。
```

你应该看到类似这样的内容：

```console
services:
  app:
    image: node:<tag>
    working_dir: /usr/src/app
    volumes:
      - .:/usr/src/app
    ports:
      - "3000:3000"
    depends_on:
      - db
    networks:
      - app-net

  db:
    image: postgres:18
    environment:
      POSTGRES_USER: example
      POSTGRES_PASSWORD: example
      POSTGRES_DB: appdb
    volumes:
      - db-data:/var/lib/postgresql
    ports:
      - "5432:5432"
    networks:
      - app-net

volumes:
  db-data:

networks:
  app-net:
    driver: bridge
```

---

## 9. 运行 Docker Compose 堆栈

从你的项目根目录：

```console
$ docker compose up
```

Docker 将：

- 拉取通过 Docker Hub MCP 选择的 Node 和 Postgres 镜像  
- 创建网络和卷  
- 启动容器  

打开浏览器：

```console
http://localhost:3000
```
![Local Host](./Images/Localhost.avif)

你的 Node.js 应用现在应该正在运行。

---

## 结论

通过将 Claude Code 与 Docker MCP Toolkit、Docker Desktop 和 Docker Hub MCP 服务器结合使用，你可以用自然语言描述你的堆栈，让 MCP 处理细节。这消除了上下文切换，取而代之的是由模型上下文协议集成驱动的流畅、引导式工作流。

---

### 下一步

- 探索 [Docker MCP 目录](https://hub.docker.com/mcp) 中可用的 220 多个 MCP 服务器
- 将 Claude Code 连接到你的数据库、内部 API 和团队工具  
- 与你的团队分享你的 MCP 设置，让每个人都能一致地工作  

开发的未来不是工具之间的切换。它是关于工具以简单、安全、可预测的方式协同工作。Docker MCP Toolkit 将这一未来带入你的日常工作中。

## 了解更多

- **[探索 MCP 目录](https://hub.docker.com/mcp):** 发现容器化、安全加固的 MCP 服务器  
- **[在 Docker Desktop 中开始使用 MCP Toolkit](https://hub.docker.com/open-desktop?url=https://open.docker.com/dashboard/mcp):** 需要 4.48 或更高版本才能自动启动  
- **[阅读 MCP Horror Stories 系列](https://www.docker.com/blog/mcp-horror-stories-the-supply-chain-attack/):** 了解常见的 MCP 安全陷阱及如何避免它们