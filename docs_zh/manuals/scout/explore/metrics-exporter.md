---
title: Docker Scout 指标导出器
description: |
  了解如何使用 Prometheus 从 Docker Scout 中抓取数据，以 Grafana 创建自定义的漏洞和策略仪表板
keywords: scout, exporter, prometheus, grafana, metrics, dashboard, api, compose
aliases:
  - /scout/metrics-exporter/
---

Docker Scout 公开一个指标 HTTP 端点，允许你使用 Prometheus 或 Datadog 从 Docker Scout 抓取漏洞和策略数据。通过此功能，你可以创建自托管的 Docker Scout 仪表板，用于可视化供应链指标。

## 指标

指标端点公开以下指标：

| 指标                            | 描述                                | 标签                                | 类型  |
| ------------------------------- | ----------------------------------- | ----------------------------------- | ----- |
| `scout_stream_vulnerabilities`  | 流中的漏洞                          | `streamName`, `severity`            | Gauge |
| `scout_policy_compliant_images` | 策略在流中的合规镜像                | `id`, `displayName`, `streamName`   | Gauge |
| `scout_policy_evaluated_images` | 策略在流中评估的总镜像数            | `id`, `displayName`, `streamName`   | Gauge |

> **流（Streams）**
>
> 在 Docker Scout 中，流的概念是 [环境（environments）](/manuals/scout/integrations/environment/_index.md) 的超集。
> 流包括你定义的所有运行时环境，以及特殊的 `latest-indexed` 流。
> `latest-indexed` 流包含每个仓库最近推送（并分析）的标签。
>
> 流在 Docker Scout 中主要是内部概念，除了通过此指标端点暴露的数据。
{ #stream }

## 创建访问令牌

要从你的组织导出指标，首先确保你的组织已加入 Docker Scout。然后，创建一个个人访问令牌（PAT）——一个允许导出器使用 Docker Scout API 进行身份验证的密钥令牌。

PAT 不需要任何特定权限，但必须由 Docker 组织的所有者用户创建。要创建 PAT，请按照 [创建访问令牌](/manuals/security/access-tokens.md) 中的步骤操作。

创建 PAT 后，将其存储在安全位置。你将在抓取指标时向导出器提供此令牌。

## Prometheus

本节描述如何使用 Prometheus 抓取指标端点。

### 为你的组织添加任务

在 Prometheus 配置文件中，为你的组织添加新任务。任务应包含以下配置；将 `ORG` 替换为你的组织名称：

```yaml
scrape_configs:
  - job_name: <ORG>
    metrics_path: /v1/exporter/org/<ORG>/metrics
    scheme: https
    static_configs:
      - targets:
          - api.scout.docker.com
```

`targets` 字段中的地址设置为 Docker Scout API 的域名 `api.scout.docker.com`。确保没有防火墙规则阻止服务器与此端点通信。

### 添加承载令牌身份验证

要使用 Prometheus 从 Docker Scout 导出器端点抓取指标，你需要配置 Prometheus 使用 PAT 作为承载令牌。导出器要求在请求的 `Authorization` 标头中传递 PAT。

更新 Prometheus 配置文件，添加 `authorization` 配置块。此块将 PAT 定义为存储在文件中的承载令牌：

```yaml
scrape_configs:
  - job_name: $ORG
    authorization:
      type: Bearer
      credentials_file: /etc/prometheus/token
```

文件内容应为纯文本格式的 PAT：

```console
dckr_pat_...
```

如果你在 Docker 容器或 Kubernetes Pod 中运行 Prometheus，请使用卷或密钥将文件挂载到容器中。

最后，重启 Prometheus 以应用更改。

### Prometheus 示例项目

如果你没有设置 Prometheus 服务器，可以使用 Docker Compose 运行 [示例项目](https://github.com/dockersamples/scout-metrics-exporter)。
该示例包括一个从加入 Docker Scout 的 Docker 组织抓取指标的 Prometheus 服务器，以及带有预配置仪表板的 Grafana，用于可视化漏洞和策略指标。

1. 克隆用于引导一组 Compose 服务的启动模板，以抓取和可视化 Docker Scout 指标端点：

   ```console
   $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
   $ cd scout-metrics-exporter/prometheus
   ```

2. [创建 Docker 访问令牌](/manuals/security/access-tokens.md) 并将其存储在模板目录中的 `/prometheus/prometheus/token` 纯文本文件中。

   ```plaintext {title=token}
   $ echo $DOCKER_PAT > ./prometheus/token
   ```

3. 在 Prometheus 配置文件 `/prometheus/prometheus/prometheus.yml` 中，将第 6 行 `metrics_path` 属性中的 `ORG` 替换为你的 Docker 组织命名空间。

   ```yaml {title="prometheus/prometheus.yml",hl_lines="6",linenos=1}
   global:
     scrape_interval: 60s
     scrape_timeout: 40s
   scrape_configs:
     - job_name: Docker Scout policy
       metrics_path: /v1/exporter/org/<ORG>/metrics
       scheme: https
       static_configs:
         - targets:
             - api.scout.docker.com
       authorization:
         type: Bearer
         credentials_file: /etc/prometheus/token
   ```

4. 启动 compose 服务。

   ```console
   docker compose up -d
   ```

   此命令启动两个服务：Prometheus 服务器和 Grafana。Prometheus 从 Docker Scout 端点抓取指标，Grafana 使用预配置的仪表板可视化指标。

要停止演示并清理创建的资源，请运行：

```console
docker compose down -v
```

### 访问 Prometheus

启动服务后，你可以通过访问 <http://localhost:9090> 访问 Prometheus 表达式浏览器。Prometheus 服务器在 Docker 容器中运行，在端口 9090 上可访问。

几秒钟后，你应该在 Prometheus UI 的 <http://localhost:9090/targets> 中看到指标端点作为目标。

![Docker Scout metrics exporter Prometheus target](../images/scout-metrics-prom-target.png "Docker Scout metrics exporter Prometheus target")

### 在 Grafana 中查看指标

要查看 Grafana 仪表板，请访问 <http://localhost:3000/dashboards>，并使用 Docker Compose 文件中定义的凭据登录（用户名：`admin`，密码：`grafana`）。

![Vulnerability dashboard in Grafana](../images/scout-metrics-grafana-vulns.png "Vulnerability dashboard in Grafana")

![Policy dashboard in Grafana](../images/scout-metrics-grafana-policy.png "Policy dashboard in Grafana")

仪表板已预配置为可视化 Prometheus 抓取的漏洞和策略指标。

## Datadog

本节描述如何使用 Datadog 抓取指标端点。Datadog 通过运行可自定义的 [代理](https://docs.datadoghq.com/agent/?tab=Linux) 来拉取监控数据，该代理会抓取可用端点的指标。OpenMetrics 和 Prometheus 检查已包含在代理中，因此你不需要在容器或主机上安装其他内容。

本指南假设你有 Datadog 账户和 Datadog API 密钥。请参阅 [Datadog 文档](https://docs.datadoghq.com/agent) 开始使用。

### 配置 Datadog 代理

要开始收集指标，你需要编辑代理的 OpenMetrics 检查配置文件。如果你将代理作为容器运行，该文件必须挂载到 `/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml`。

以下示例显示了 Datadog 配置，包括：

- 指定针对 `dockerscoutpolicy` Docker 组织的 OpenMetrics 端点
- 所有收集的指标将被前缀的 `namespace`
- 你希望代理抓取的 [`metrics`](#metrics)（`scout_*`）
- 用于代理使用 Docker PAT 作为承载令牌对指标端点进行身份验证的 `auth_token` 部分

```yaml
instances:
  - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/dockerscoutpolicy/metrics"
    namespace: "scout-metrics-exporter"
    metrics:
      - scout_*
    auth_token:
      reader:
        type: file
        path: /var/run/secrets/scout-metrics-exporter/token
      writer:
        type: header
        name: Authorization
        value: Bearer <TOKEN>
```

> [!IMPORTANT]
>
> 不要替换前面配置示例中的 `<TOKEN>` 占位符。它必须保持不变。只需确保 Docker PAT 正确挂载到指定文件路径的 Datadog 代理中。将文件保存为 `conf.yaml` 并重启代理。

创建自己的 Datadog 代理配置时，确保编辑 `openmetrics_endpoint` 属性以针对你的组织，通过将 `dockerscoutpolicy` 替换为你的 Docker 组织命名空间。

### Datadog 示例项目

如果你没有设置 Datadog 服务器，可以使用 Docker Compose 运行 [示例项目](https://github.com/dockersamples/scout-metrics-exporter)。该示例包括一个作为容器运行的 Datadog 代理，从加入 Docker Scout 的 Docker 组织抓取指标。此示例项目假设你有 Datadog 账户、API 密钥和 Datadog 站点。

1. 克隆用于引导 Datadog Compose 服务的启动模板，以抓取 Docker Scout 指标端点：

   ```console
   $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
   $ cd scout-metrics-exporter/datadog
   ```

2. [创建 Docker 访问令牌](/manuals/security/access-tokens.md) 并将其存储在模板目录中的 `/datadog/token` 纯文本文件中。

   ```plaintext {title=token}
   $ echo $DOCKER_PAT > ./token
   ```

3. 在 `/datadog/compose.yaml` 文件中，使用你的 Datadog 部署值更新 `DD_API_KEY` 和 `DD_SITE` 环境变量。

   ```yaml {hl_lines="5-6"}
     datadog-agent:
       container_name: datadog-agent
       image: gcr.io/datadoghq/agent:7
       environment:
         - DD_API_KEY=${DD_API_KEY} # e.g. 1b6b3a42...
         - DD_SITE=${DD_SITE} # e.g. datadoghq.com
         - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock:ro
         - ./conf.yaml:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml:ro
         - ./token:/var/run/secrets/scout-metrics-exporter/token:ro
   ```

   `volumes` 部分将 Docker 套接字从主机挂载到容器。这是为了在作为容器运行时获得准确的主机名（[更多详情](https://docs.datadoghq.com/agent/troubleshooting/hostname_containers/)）。

   它还挂载了代理的配置文件和 Docker 访问令牌。

4. 编辑 `/datadog/config.yaml` 文件，将 `openmetrics_endpoint` 属性中的占位符 `<ORG>` 替换为你想要收集指标的 Docker 组织命名空间。

   ```yaml {hl_lines=2}
   instances:
     - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/<<ORG>>/metrics"
       namespace: "scout-metrics-exporter"
   # ...
   ```

5. 启动 Compose 服务。

   ```console
   docker compose up -d
   ```

如果配置正确，当你运行代理的状态命令时，你应该在运行检查下看到 OpenMetrics 检查，其输出应类似于：

```text
openmetrics (4.2.0)
-------------------
  Instance ID: openmetrics:scout-prometheus-exporter:6393910f4d92f7c2 [OK]
  Configuration Source: file:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml
  Total Runs: 1
  Metric Samples: Last Run: 236, Total: 236
  Events: Last Run: 0, Total: 0
  Service Checks: Last Run: 1, Total: 1
  Average Execution Time : 2.537s
  Last Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
  Last Successful Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
```

有关选项的完整列表，请查看此 [示例配置文件](https://github.com/DataDog/integrations-core/blob/master/openmetrics/datadog_checks/openmetrics/data/conf.yaml.example) 以获取通用 OpenMetrics 检查。

### 可视化你的数据

配置代理以获取 Prometheus 指标后，你可以使用它们构建全面的 Datadog 图形、仪表板和警报。

进入你的 [指标摘要页面](https://app.datadoghq.com/metric/summary?filter=scout_prometheus_exporter) 查看从此示例收集的指标。此配置将收集所有以 `scout_` 开头并在命名空间 `scout_metrics_exporter` 下暴露的指标。

![datadog_metrics_summary](../images/datadog_metrics_summary.png)

以下截图显示了包含特定 [流](#stream) 漏洞和策略合规性图表的 Datadog 仪表板示例。

![datadog_dashboard_1](../images/datadog_dashboard_1.png)
![datadog_dashboard_2](../images/datadog_dashboard_2.png)

> 图表中线条看起来平坦的原因是漏洞数据本身的性质以及日期选择器中选择的短时间间隔。

## 抓取间隔

默认情况下，Prometheus 和 Datadog 以 15 秒间隔抓取指标。由于漏洞数据本身的性质，通过此 API 暴露的指标不太可能频繁变化。因此，指标端点默认有 60 分钟缓存，建议设置 60 分钟或更长的抓取间隔。如果你将抓取间隔设置为小于 60 分钟，你将在该时间窗口内多次抓取中看到相同的数据。

要更改抓取间隔：

- Prometheus：在 Prometheus 配置文件的全局或任务级别设置 `scrape_interval` 字段。
- Datadog：在 Datadog 代理配置文件中设置 `min_collection_interval` 属性，请参阅 [Datadog 文档](https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval)。

## 撤销访问令牌

如果你怀疑 PAT 已泄露或不再需要，你可以随时撤销它。要撤销 PAT，请按照 [创建和管理访问令牌](/manuals/security/access-tokens.md) 中的步骤操作。

撤销 PAT 会立即使令牌失效，并防止 Prometheus 使用该令牌抓取指标。你需要创建新的 PAT 并更新 Prometheus 配置以使用新令牌。