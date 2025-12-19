---
title: 使用 YAML 配置 MCP 服务器
description: 在 Gordon 中使用 MCP 服务器
keywords: ai, mcp, gordon, yaml, configuration, docker compose, mcp servers, extensibility
aliases:
 - /desktop/features/gordon/mcp/yaml/
---

Docker 与 Anthropic 合作，为 MCP 服务器的[参考实现](https://github.com/modelcontextprotocol/servers/)提供容器镜像。这些镜像在 Docker Hub 的 [mcp 命名空间](https://hub.docker.com/u/mcp)下提供。

当你在终端中运行 `docker ai` 命令时，Gordon 会检查当前工作目录中是否存在 `gordon-mcp.yml` 文件。如果存在，该文件会列出 Gordon 在此上下文中应使用的 MCP 服务器。`gordon-mcp.yml` 文件是一个 Docker Compose 文件，它将 MCP 服务器配置为 Compose 服务，供 Gordon 访问。

以下最小示例展示了如何使用 [mcp-time server](https://hub.docker.com/r/mcp/time) 为 Gordon 提供时间功能。有关更多详细信息，请参阅[源代码和文档](https://github.com/modelcontextprotocol/servers/tree/main/src/time)。

在工作目录中创建 `gordon-mcp.yml` 文件并添加 time 服务器：

```yaml
services:
  time:
    image: mcp/time
```

有了此文件后，你现在可以让 Gordon 告诉你另一个时区的时间：

```bash
$ docker ai '现在基里巴斯是几点？'

    • 调用 get_current_time

  基里巴斯（塔拉瓦）的当前时间是 2025 年 1 月 7 日晚上 9:38。
```

Gordon 会找到 MCP time 服务器，并在需要时调用其工具。

## 使用高级 MCP 服务器功能

某些 MCP 服务器需要访问你的文件系统或系统环境变量。Docker Compose 可以帮助实现这一点。由于 `gordon-mcp.yml` 是一个 Compose 文件，你可以使用标准的 Docker Compose 语法添加绑定挂载。这使你能够将文件系统资源提供给容器：

```yaml
services:
  fs:
    image: mcp/filesystem
    command:
      - /rootfs
    volumes:
      - .:/rootfs
```

`gordon-mcp.yml` 文件为 Gordon 添加了文件系统访问功能。由于所有内容都在容器内运行，Gordon 只能访问你指定的目录。

Gordon 可以使用任意数量的 MCP 服务器。例如，要使用 `mcp/fetch` 服务器为 Gordon 提供互联网访问：

```yaml
services:
  fetch:
    image: mcp/fetch
  fs:
    image: mcp/filesystem
    command:
      - /rootfs
    volumes:
      - .:/rootfs
```

你现在可以让 Gordon 获取内容并将其写入文件：

```bash
$ docker ai 你能获取 rumpl.dev 的内容并将摘要写入文件 test.txt 吗？

    • 调用 fetch ✔️
    • 调用 write_file ✔️

  rumpl.dev 网站的摘要已成功写入允许目录中的文件 test.txt。如果你需要进一步帮助，请告诉我！

$ cat test.txt
网站 rumpl.dev 包含由网站所有者撰写的各种博客文章和文章。以下是内容摘要：

1. **Wasmio 2023 (2023 年 3 月 25 日)**：回顾在巴塞罗那举行的 WasmIO 2023 会议。作者分享了作为演讲者的经历，并赞扬了组织者成功举办的活动。

2. **用 Rust 编写窗口管理器 - 第 2 部分 (2023 年 1 月 3 日)**：关于用 Rust 创建窗口管理器系列的第二部分。本部分重点介绍增强管理窗口的功能。

3. **2022 年回顾 (2022 年 12 月 29 日)**：对 2022 年的个人和职业回顾。作者反思了这一年中的高低起伏，强调了职业成就。

4. **用 Rust 编写窗口管理器 - 第 1 部分 (2022 年 12 月 28 日)**：关于用 Rust 构建窗口管理器系列的第一部分。作者讨论了设置 Linux 机器以及使用 X11 和 Rust 的挑战。

5. **将 docker/docker 添加到你的依赖项中 (2020 年 5 月 10 日)**：为 Go 开发者提供的关于如何在项目中使用 Docker 客户端库的指南。文章包含一个演示集成的代码片段。

6. **第一篇 (2019 年 10 月 11 日)**：博客上的首篇文章，展示了一个简单的 Go "Hello World" 程序。
```

## 下一步是什么？

现在你已经了解了如何在 Gordon 中使用 MCP 服务器，请尝试以下后续步骤：

- 实验：尝试将一个或多个经过测试的 MCP 服务器集成到你的 `gordon-mcp.yml` 文件中，并探索其功能。
- 探索生态系统。查看 [GitHub 上的参考实现](https://github.com/modelcontextprotocol/servers/)或浏览 [Docker Hub MCP 命名空间](https://hub.docker.com/u/mcp)，寻找更多可能适合你需求的服务器。
- 构建自己的服务器。如果现有服务器都不满足你的需求，或者你想了解更多信息，请开发一个自定义 MCP 服务器。使用 [MCP 规范](https://www.anthropic.com/news/model-context-protocol)作为指南。
- 分享你的反馈。如果你发现了与 Gordon 配合良好的新服务器或遇到问题，请[分享你的发现以帮助改进生态系统](https://docker.qualtrics.com/jfe/form/SV_9tT3kdgXfAa6cWa)。

通过 MCP 支持，Gordon 为你的用例提供了强大的可扩展性和灵活性，无论你需要时间感知、文件管理还是互联网访问。