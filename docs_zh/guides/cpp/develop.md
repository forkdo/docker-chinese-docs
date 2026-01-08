---
title: 使用容器进行 C++ 开发
linkTitle: 开发您的应用程序
weight: 20
keywords: C++, 本地, 开发
description: 了解如何在本地开发您的 C++ 应用程序。
aliases:
- /language/cpp/develop/
- /guides/language/cpp/develop/
---

## 先决条件

已完成 [容器化 C++ 应用程序](containerize.md)。

## 概述

在本节中，您将学习如何为容器化应用程序设置开发环境。这包括：

- 配置 Compose，以便在您编辑并保存代码时自动更新正在运行的 Compose 服务

## 获取示例应用程序

克隆示例应用程序以供本指南使用。打开终端，切换到您想要工作的目录，然后运行以下命令来克隆仓库：

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git && cd c-plus-plus-docker
```

## 自动更新服务

使用 Compose Watch，以便在您编辑并保存代码时自动更新正在运行的 Compose 服务。有关 Compose Watch 的更多详细信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

在 IDE 或文本编辑器中打开您的 `compose.yml` 文件，然后添加 Compose Watch 指令。以下示例展示了如何将 Compose Watch 添加到您的 `compose.yml` 文件中。

```yaml {hl_lines="11-14",linenos=true}
services:
  ok-api:
    image: ok-api
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    develop:
      watch:
        - action: rebuild
          path: .
```

运行以下命令以使用 Compose Watch 运行您的应用程序。

```console
$ docker compose watch
```

现在，如果您修改 `ok_api.cpp`，您将实时看到更改，而无需重新构建镜像。

要进行测试，请在您喜欢的文本编辑器中打开 `ok_api.cpp` 文件，并将消息从 `{"Status" : "OK"}` 更改为 `{"Status" : "Updated"}`。保存文件，并在浏览器中刷新 [http://localhost:8080](http://localhost:8080)。您应该会看到更新后的消息。

在终端中按 `ctrl+c` 停止您的应用程序。

## 总结

在本节中，您还学习了如何使用 Compose Watch，在更新代码时自动重新构建并运行您的容器。

相关信息：

- [Compose 文件参考](/reference/compose-file/)
- [Compose 文件监视](/manuals/compose/how-tos/file-watch.md)
- [多阶段构建](/manuals/build/building/multi-stage.md)

## 下一步

在下一节中，您将了解如何使用 GitHub Actions 设置 CI/CD 管道。