---
title: 开发你的应用
linkTitle: 开发你的应用
weight: 40
keywords: go, golang, containerize, initialize
description: 了解如何使用 Docker 开发 Golang 应用。
---

在上一节中，你看到了如何使用 Docker Compose 将服务连接在一起。在本节中，你将学习如何使用 Docker 开发 Golang 应用。你还将看到如何使用 Docker Compose Watch 在代码更改时重建镜像。最后，你将测试应用，并使用 Prometheus 作为数据源在 Grafana 中可视化指标。

## 开发应用

现在，如果你在本地对 Golang 应用进行任何更改，它需要在容器中反映出来，对吧？要做到这一点，一种方法是在代码更改后使用 Docker Compose 的 `--build` 标志。这将重建 `compose.yml` 文件中包含 `build` 指令的所有服务，在你的情况下，是 `api` 服务（Golang 应用）。

```console
docker compose up --build
```

但是，这不是最好的方法。这并不高效。每次代码更改后，你都需要手动重建。这对于开发来说不是一个好的流程。

更好的方法是使用 Docker Compose Watch。在 `compose.yml` 文件中的 `api` 服务下，你已经添加了 `develop` 部分。所以，它更像是热重载。当你对代码（在 `path` 中定义）进行更改时，它将重建镜像（或重启，取决于操作）。这就是使用方法：

```yaml {hl_lines="17-20",linenos=true}
services:
  api:
    container_name: go-api
    build:
      context: .
      dockerfile: Dockerfile
    image: go-api:latest
    ports:
      - 8000:8000
    networks:
      - go-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    develop:
      watch:
        - path: .
          action: rebuild
```

一旦你在 `compose.yml` 文件中添加了 `develop` 部分，你就可以使用以下命令启动开发服务器：

```console
$ docker compose watch
```

现在，如果你修改 `main.go` 或项目中的任何其他文件，`api` 服务将自动重建。你会在终端中看到以下输出：

```bash
Rebuilding service(s) ["api"] after changes were detected...
[+] Building 8.1s (15/15) FINISHED                                                                                                        docker:desktop-linux
 => [api internal] load build definition from Dockerfile                                                                                                  0.0s
 => => transferring dockerfile: 704B                                                                                                                      0.0s
 => [api internal] load metadata for docker.io/library/alpine:3.17                                                                                        1.1s
  .                             
 => => exporting manifest list sha256:89ebc86fd51e27c1da440dc20858ff55fe42211a1930c2d51bbdce09f430c7f1                                                    0.0s
 => => naming to docker.io/library/go-api:latest                                                                                                          0.0s
 => => unpacking to docker.io/library/go-api:latest                                                                                                       0.0s
 => [api] resolving provenance for metadata file                                                                                                          0.0s
service(s) ["api"] successfully built
```

## 测试应用

现在你的应用正在运行，前往 Grafana 仪表板可视化你注册的指标。在浏览器中导航到 `http://localhost:3000`。你会看到 Grafana 登录页面。登录凭据是在 Compose 文件中提供的。

登录后，你可以创建一个新的仪表板。创建仪表板时，你会注意到默认数据源是 `Prometheus`。这是因为你已经在 `grafana.yml` 文件中配置了数据源。

![可选设置屏幕，包含指定的选项。](../images/grafana-dash.png)

你可以使用不同的面板来可视化指标。本指南不会详细介绍 Grafana。你可以参考 [Grafana 文档](https://grafana.com/docs/grafana/latest/) 了解更多信息。有一个 Bar Gauge 面板用于可视化来自不同端点的请求数量。你使用了 `api_http_request_total` 和 `api_http_request_error_total` 指标来获取数据。

![可选设置屏幕，包含指定的选项。](../images/grafana-panel.png)

你创建此面板是为了可视化来自不同端点的请求数量，以比较成功和失败的请求。对于所有成功的请求，条形将是绿色的，对于所有失败的请求，条形将是红色的。此外，它还会显示请求来自哪个端点，无论是成功请求还是失败请求。如果你想使用此面板，可以从你克隆的仓库中导入 `dashboard.json` 文件。

## 总结

你已经完成了本指南的学习。你学会了如何使用 Docker 开发 Golang 应用。你还看到了如何使用 Docker Compose Watch 在代码更改时重建镜像。最后，你测试了应用，并使用 Prometheus 作为数据源在 Grafana 中可视化了指标。