---
title: Docker CLI 的 OpenTelemetry
description: 了解如何为 Docker 命令行捕获 OpenTelemetry 指标
keywords: otel, opentelemetry, telemetry, traces, tracing, metrics, logs
aliases:
  - /config/otel/
---

{{< summary-bar feature_name="Docker CLI OpenTelemetry" >}}

Docker CLI 支持 [OpenTelemetry](https://opentelemetry.io/docs/) 检测，用于发出有关命令调用的指标。默认情况下，此功能是禁用的。您可以配置 CLI 以开始向指定的端点发出指标。这允许您捕获有关 `docker` 命令调用的信息，以便更深入地了解 Docker 的使用情况。

导出指标是选择性的，您可以通过指定指标收集器的目标地址来控制数据的发送位置。

## 什么是 OpenTelemetry？

OpenTelemetry（简称 OTel）是一个用于创建和管理遥测数据（例如跟踪、指标和日志）的开源可观测性框架。OpenTelemetry 与供应商和工具无关，这意味着它可以与各种可观测性后端一起使用。

Docker CLI 中对 OpenTelemetry 检测的支持意味着 CLI 可以使用 OpenTelemetry 规范中定义的协议和约定发出有关发生事件的信息。

## 工作原理

Docker CLI 默认不会发出遥测数据。只有在系统上设置了环境变量的情况下，Docker CLI 才会尝试向指定的端点发出 OpenTelemetry 指标。

```bash
DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT=<endpoint>
```

该变量指定 OpenTelemetry 收集器的端点，应将有关 `docker` CLI 调用的遥测数据发送到此端点。要捕获数据，您需要一个在此端点上监听的 OpenTelemetry 收集器。

收集器的目的是接收遥测数据，处理它，并将其导出到后端。后端是存储遥测数据的地方。您可以从多种不同的后端中进行选择，例如 Prometheus 或 InfluxDB。

一些后端提供了直接可视化指标的工具。或者，您也可以运行一个专用的前端，支持生成更有用的图表，例如 Grafana。

## 设置

要开始为 Docker CLI 捕获遥测数据，您需要：

- 将 `DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT` 环境变量设置为指向 OpenTelemetry 收集器端点
- 运行一个 OpenTelemetry 收集器，用于接收来自 CLI 命令调用的信号
- 运行一个后端，用于存储从收集器接收的数据

以下 Docker Compose 文件引导一组服务以开始使用 OpenTelemetry。它包括一个 CLI 可以发送指标的 OpenTelemetry 收集器，以及一个从收集器抓取指标的 Prometheus 后端。

```yaml {collapse=true,title=compose.yaml}
name: cli-otel
services:
  prometheus:
    image: prom/prometheus
    command:
      - "--config.file=/etc/prometheus/prom.yml"
    ports:
      # 在 localhost:9091 上发布 Prometheus 前端
      - 9091:9090
    restart: always
    volumes:
      # 将 Prometheus 数据存储在卷中：
      - prom_data:/prometheus
      # 挂载 prom.yml 配置文件
      - ./prom.yml:/etc/prometheus/prom.yml
  otelcol:
    image: otel/opentelemetry-collector
    restart: always
    depends_on:
      - prometheus
    ports:
      - 4317:4317
    volumes:
      # 挂载 otelcol.yml 配置文件
      - ./otelcol.yml:/etc/otelcol/config.yaml

volumes:
  prom_data:
```

此服务假定以下两个配置文件与 `compose.yaml` 文件位于同一目录：

- ```yaml {collapse=true,title=otelcol.yml}
  # 通过 gRPC 和 HTTP 接收信号
  receivers:
    otlp:
      protocols:
        grpc:
        http:

  # 为 Prometheus 建立抓取端点
  exporters:
    prometheus:
      endpoint: "0.0.0.0:8889"

  service:
    pipelines:
      metrics:
        receivers: [otlp]
        exporters: [prometheus]
  ```

- ```yaml {collapse=true,title=prom.yml}
  # 配置 Prometheus 以抓取 OpenTelemetry 收集器端点
  scrape_configs:
    - job_name: "otel-collector"
      scrape_interval: 1s
      static_configs:
        - targets: ["otelcol:8889"]
  ```

有了这些文件后：

1. 启动 Docker Compose 服务：

   ```console
   $ docker compose up
   ```

2. 配置 Docker CLI 以将遥测数据导出到 OpenTelemetry 收集器。

   ```console
   $ export DOCKER_CLI_OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   ```

3. 运行一个 `docker` 命令以触发 CLI 向 OpenTelemetry 收集器发送指标信号。

   ```console
   $ docker version
   ```

4. 要查看 CLI 创建的遥测指标，请通过访问 <http://localhost:9091/graph> 打开 Prometheus 表达式浏览器。

5. 在 **Query** 字段中输入 `command_time_milliseconds_total`，然后执行查询以查看遥测数据。

## 可用指标

Docker CLI 目前导出一个指标 `command.time`，用于测量命令的执行持续时间（以毫秒为单位）。此指标具有以下属性：

- `command.name`：命令的名称
- `command.status.code`：命令的退出代码
- `command.stderr.isatty`：如果 stderr 连接到 TTY，则为 true
- `command.stdin.isatty`：如果 stdin 连接到 TTY，则为 true
- `command.stdout.isatty`：如果 stdout 连接到 TTY，则为 true