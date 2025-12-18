---
title: 使用容器进行 Deno 开发
linkTitle: 开发你的应用
weight: 20
keywords: deno, 本地, 开发
description: 了解如何在本地开发你的 Deno 应用程序。
aliases:
- /language/deno/develop/
---

## 前置条件

完成 [容器化 Deno 应用](containerize.md)。

## 概述

在本节中，你将学习如何为你的容器化应用程序设置开发环境。这包括：

- 配置 Compose，使其在你编辑和保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用程序

克隆示例应用程序以配合本指南使用。打开终端，将目录切换到你想要工作的目录，然后运行以下命令克隆仓库：

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

## 自动更新服务

使用 Compose Watch 来自动更新你的运行中 Compose 服务，当你编辑和保存代码时。
有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开你的 `compose.yml` 文件，然后添加 Compose Watch 指令。以下示例展示了如何将 Compose Watch 添加到你的 `compose.yml` 文件中。

```yaml {hl_lines="9-12",linenos=true}
services:
  server:
    image: deno-server
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    develop:
      watch:
        - action: rebuild
          path: .
```

运行以下命令以使用 Compose Watch 启动你的应用程序。

```console
$ docker compose watch
```

现在，如果你修改 `server.ts`，你将实时看到更改，而无需重新构建镜像。

要测试它，用你最喜欢的文本编辑器打开 `server.ts` 文件，将消息从 `{"Status" : "OK"}` 改为 `{"Status" : "Updated"}`。保存文件并在浏览器中刷新 `http://localhost:8000`。你应该能看到更新后的消息。

在终端中按 `ctrl+c` 停止你的应用程序。

## 总结

在本节中，你还学习了如何使用 Compose Watch 来在更新代码时自动重建和运行你的容器。

相关信息：
 - [Compose 文件参考](/reference/compose-file/)
 - [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
 - [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，你将了解如何使用 GitHub Actions 设置 CI/CD 流水线。