---
title: 使用 Docker Compose 连接服务
linkTitle: 使用 Docker Compose 连接服务
weight: 30 #
keywords: go, golang, prometheus, grafana, containerize, monitor
description: 了解如何使用 Docker Compose 连接服务，通过 Prometheus 和 Grafana 监控 Golang 应用。
---

现在你已经将 Golang 应用容器化，接下来将使用 Docker Compose 将服务连接在一起。你将把 Golang 应用、Prometheus 和 Grafana 服务连接起来，通过 Prometheus 和 Grafana 监控 Golang 应用。

## 创建 Docker Compose 文件

在 Golang 应用的根目录下创建一个名为 `compose.yml` 的新文件。Docker Compose 文件包含运行多个服务并将其连接在一起的指令。

以下是一个使用 Golang、Prometheus 和 Grafana 的项目的 Docker Compose 文件。你也可以在 `go-prometheus-monitoring` 目录中找到此文件。

```yaml
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
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    develop:
      watch:
        - path: .
          action: rebuild
      
  prometheus:
    container_name: prometheus
    image: prom/prometheus:v2.55.0
    volumes:
      - ./Docker/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
    networks:
      - go-network
  
  grafana:
    container_name: grafana
    image: grafana/grafana:11.3.0
    volumes:
      - ./Docker/grafana.yml:/etc/grafana/provisioning/datasources/datasource.yaml
      - grafana-data:/var/lib/grafana
    ports:
      - 3000:3000
    networks:
      - go-network
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password

volumes:
  grafana-data:

networks:
  go-network:
    driver: bridge
```

## 理解 Docker Compose 文件

Docker Compose 文件由三个服务组成：

- **Golang 应用服务**：此服务使用 Dockerfile 构建 Golang 应用并在容器中运行。它暴露应用的端口 `8000` 并连接到 `go-network` 网络。它还定义了一个健康检查来监控应用的健康状况。你使用 `healthcheck` 来监控应用的健康状况。健康检查每 30 秒运行一次，如果健康检查失败，最多重试 5 次。健康检查使用 `curl` 命令检查应用的 `/health` 端点。除了健康检查外，你还添加了 `develop` 部分来监控应用源代码的变化，并使用 Docker Compose Watch 功能重建应用。

- **Prometheus 服务**：此服务在容器中运行 Prometheus 服务器。它使用官方的 Prometheus 镜像 `prom/prometheus:v2.55.0`。它在端口 `9090` 上暴露 Prometheus 服务器并连接到 `go-network` 网络。你还将 `Docker` 目录中的 `prometheus.yml` 文件挂载到项目根目录。`prometheus.yml` 文件包含 Prometheus 配置，用于从 Golang 应用抓取指标。这就是你将 Prometheus 服务器连接到 Golang 应用的方式。

    ```yaml
    global:
      scrape_interval: 10s
      evaluation_interval: 10s

    scrape_configs:
      - job_name: myapp
        static_configs:
          - targets: ["api:8000"]
    ```

    在 `prometheus.yml` 文件中，你定义了一个名为 `myapp` 的任务，用于从 Golang 应用抓取指标。`targets` 字段指定抓取指标的目标。在这种情况下，目标是运行在端口 `8000` 上的 Golang 应用。`api` 是 Docker Compose 文件中 Golang 应用的服务名称。Prometheus 服务器将每 10 秒从 Golang 应用抓取一次指标。

- **Grafana 服务**：此服务在容器中运行 Grafana 服务器。它使用官方的 Grafana 镜像 `grafana/grafana:11.3.0`。它在端口 `3000` 上暴露 Grafana 服务器并连接到 `go-network` 网络。你还将 `Docker` 目录中的 `grafana.yml` 文件挂载到项目根目录。`grafana.yml` 文件包含 Grafana 配置，用于添加 Prometheus 数据源。这就是你将 Grafana 服务器连接到 Prometheus 服务器的方式。在环境变量中，你设置了 Grafana 管理员用户和密码，用于登录 Grafana 仪表板。

    ```yaml
    apiVersion: 1
    datasources:
    - name: Prometheus (Main)
      type: prometheus
      url: http://prometheus:9090
      isDefault: true
    ```
      
    在 `grafana.yml` 文件中，你定义了一个名为 `Prometheus (Main)` 的 Prometheus 数据源。`type` 字段指定数据源的类型，即 `prometheus`。`url` 字段指定用于获取指标的 Prometheus 服务器的 URL。在这种情况下，URL 是 `http://prometheus:9090`。`prometheus` 是 Docker Compose 文件中 Prometheus 服务器的服务名称。`isDefault` 字段指定数据源是否为 Grafana 中的默认数据源。

除了服务外，Docker Compose 文件还定义了一个名为 `grafana-data` 的卷来持久化 Grafana 数据，以及一个名为 `go-network` 的网络来连接服务。你创建了一个自定义网络 `go-network` 来连接服务。`driver: bridge` 字段指定用于网络的网络驱动。

## 构建和运行服务

现在你有了 Docker Compose 文件，可以使用 Docker Compose 构建服务并一起运行它们。

要构建和运行服务，请在终端中运行以下命令：

```console
$ docker compose up
```

`docker compose up` 命令构建 Docker Compose 文件中定义的服务并将它们一起运行。你会在终端中看到类似的输出：

```console
 ✔ Network go-prometheus-monitoring_go-network  Created                                                           0.0s 
 ✔ Container grafana                            Created                                                           0.3s 
 ✔ Container go-api                             Created                                                           0.2s 
 ✔ Container prometheus                         Created                                                           0.3s 
Attaching to go-api, grafana, prometheus
go-api      | [GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.
go-api      | 
go-api      | [GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
go-api      |  - using env:     export GIN_MODE=release
go-api      |  - using code:    gin.SetMode(gin.ReleaseMode)
go-api      | 
go-api      | [GIN-debug] GET    /metrics                  --> main.PrometheusHandler.func1 (3 handlers)
go-api      | [GIN-debug] GET    /health                   --> main.main.func1 (4 handlers)
go-api      | [GIN-debug] GET    /v1/users                 --> main.main.func2 (4 handlers)
go-api      | [GIN-debug] [WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.
go-api      | Please check https://pkg.go.dev/github.com/gin-gonic/gin#readme-don-t-trust-all-proxies for details.
go-api      | [GIN-debug] Listening and serving HTTP on :8000
prometheus  | ts=2025-03-15T05:57:06.676Z caller=main.go:627 level=info msg="No time or size retention was set so using the default time retention" duration=15d
prometheus  | ts=2025-03-15T05:57:06.678Z caller=main.go:671 level=info msg="Starting Prometheus Server" mode=server version="(version=2.55.0, branch=HEAD, revision=91d80252c3e528728b0f88d254dd720f6be07cb8)"
grafana     | logger=settings t=2025-03-15T05:57:06.865335506Z level=info msg="Config overridden from command line" arg="default.log.mode=console"
grafana     | logger=settings t=2025-03-15T05:57:06.865337131Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_DATA=/var/lib/grafana"
grafana     | logger=ngalert.state.manager t=2025-03-15T05:57:07.088956839Z level=info msg="State
.
.
grafana     | logger=plugin.angulardetectorsprovider.dynamic t=2025-03-15T05:57:07.530317298Z level=info msg="Patterns update finished" duration=440.489125ms
```

服务将开始运行，你可以通过 `http://localhost:8000` 访问 Golang 应用，通过 `http://localhost:9090/health` 访问 Prometheus，通过 `http://localhost:3000` 访问 Grafana。你也可以使用 `docker ps` 命令检查运行中的容器。

```console
$ docker ps
```

## 总结

在本节中，你学习了如何使用 Docker Compose 将服务连接在一起。你创建了一个 Docker Compose 文件来一起运行多个服务，并使用网络将它们连接起来。你还学习了如何使用 Docker Compose 构建和运行服务。

相关信息：

 - [Docker Compose 概述](/manuals/compose/_index.md)
 - [Compose 文件参考](/reference/compose-file/_index.md)

接下来，你将学习如何使用 Docker Compose 开发 Golang 应用，并使用 Prometheus 和 Grafana 监控它。

## 后续步骤

在下一节中，你将学习如何使用 Docker 开发 Golang 应用。你还将学习如何使用 Docker Compose Watch 在代码更改时重建镜像。最后，你将测试应用并使用 Prometheus 作为数据源在 Grafana 中可视化指标。