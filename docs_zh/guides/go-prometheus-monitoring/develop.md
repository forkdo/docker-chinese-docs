---
title: 开发你的应用程序
linkTitle: 开发你的应用
weight: 40
keywords: go, golang, containerize, initialize
description: 学习如何使用 Docker 开发 Golang 应用程序。
---

在上一节中，你已经了解了如何使用 Docker Compose 将服务连接在一起。在本节中，你将学习如何使用 Docker 开发 Golang 应用程序。你还将了解如何使用 Docker Compose Watch 在代码发生更改时自动重建镜像。最后，你将测试应用程序并使用 Prometheus 作为数据源在 Grafana 中可视化指标。

## 开发应用程序

现在，如果你在本地对 Golang 应用程序进行了任何更改，这些更改需要反映到容器中，对吧？为此，一种方法是在代码更改后使用 Docker Compose 的 `--build` 标志。这将重建 `compose.yml` 文件中有 `build` 指令的所有服务，在你的例子中就是 `api` 服务（Golang 应用程序）。

```console
docker compose up --build
```

但这并不是最佳方法，效率不高。每次更改代码后都需要手动重建，这不是良好的开发流程。

更好的方法是使用 Docker Compose Watch。在 `compose.yml` 文件中，你在 `api` 服务下添加了 `develop` 部分，这更像是一种热重载机制。每当你更改代码（在 `path` 中定义）时，它都会重建镜像（或根据操作重启）。使用方法如下：

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

在 `compose.yml` 文件中添加 `develop` 部分后，你可以使用以下命令启动开发服务器：

```console
$ docker compose watch
```

现在，如果你修改了 `main.go` 或项目中的任何其他文件，`api` 服务将自动重建。你将在终端中看到以下输出：

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

## 测试应用程序

现在你的应用程序已经运行，前往 Grafana 仪表板查看你正在记录的指标。打开浏览器并导航到 `http://localhost:3000`。你将看到 Grafana 登录页面，登录凭据是 Compose 文件中提供的那些。

登录后，你可以创建新的仪表板。创建仪表板时会注意到默认数据源是 `Prometheus`，这是因为在 `grafana.yml` 文件中已经配置了数据源。

![带有指定选项的可选设置屏幕。](../images/grafana-dash.png)

你可以使用不同的面板来可视化指标。本指南不会详细介绍 Grafana，更多信息请参考 [Grafana 文档](https://grafana.com/docs/grafana/latest/)。有一个条形图面板可以可视化来自不同端点的请求总数，你使用了 `api_http_request_total` 和 `api_http_request_error_total` 指标来获取数据。

![带有指定选项的可选设置屏幕。](../images/grafana-panel.png)

你创建这个面板是为了可视化来自不同端点的请求总数，以比较成功和失败的请求。所有成功的请求条将为绿色，所有失败的请求条将为红色。此外，它还会显示请求来自哪个端点，是成功请求还是失败请求。如果你想使用这个面板，可以从你克隆的仓库中导入 `dashboard.json` 文件。

## 总结

你已经完成了本指南的学习。你学会了如何使用 Docker 开发 Golang 应用程序，了解了如何使用 Docker Compose Watch 在代码更改时自动重建镜像。最后，你测试了应用程序并使用 Prometheus 作为数据源在 Grafana 中可视化了指标。