# 通过 MCP 将 Gemini 连接到 Grafana


本指南介绍如何使用 **Docker MCP Toolkit** 将 Gemini CLI 连接到 Grafana 实例。

## 先决条件

- 已安装并完成认证的 **Gemini CLI**。
- 已启用 **MCP Toolkit** 扩展的 **Docker Desktop**。
- 一个正在运行的 **Grafana** 实例。

## 步骤 1：配置 Grafana 访问权限

MCP 服务器需要 **服务账号令牌（Service Account Token）** 才能与 Grafana API 交互。相比个人 API 密钥，更推荐使用服务账号令牌，因为它们可以被单独吊销而不影响用户访问，并且权限范围可以设置得更精细。

1. 在 Grafana 仪表板中依次进入 **Administration > Users and access > Service accounts**。
2. 创建一个新的服务账号（例如 `gemini-mcp-connector`）。
3. 分配 **Viewer** 角色（如果需要告警管理能力，则分配 **Editor**）。
4. 生成一个新令牌。请立即复制该令牌——之后将无法再次查看。


## 步骤 2：配置 MCP 服务器

Docker MCP Toolkit 提供了预配置的 Grafana 目录项。它将 LLM 连接到 Grafana API。

1. 在 Docker Desktop 中打开 **MCP Toolkit**。
2. 在目录（Catalog）中找到 **Grafana**，并将其添加到你启用的服务器中。
3. 在 **Configuration** 视图中，设置以下内容：

- **Grafana URL：** 你的实例的端点或 URL。
- **Service Account Token：** 上一步中生成的令牌。

## 步骤 3：集成 Gemini CLI

要在 Gemini 中注册 Docker MCP 网关，请更新位于 `~/.gemini/settings.json` 的全局配置文件。

确保 `mcpServers` 对象包含以下条目：

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"]
    }
  }
}
```

## 步骤 4：验证配置

重启 Gemini CLI 会话以加载新配置。运行以下命令验证 MCP 工具的状态：

```bash
> /mcp list

```

连接成功时，`MCP_DOCKER` 会显示为 **Ready**，并暴露数十个用于数据获取、仪表板搜索和告警检查的工具。

## 使用场景

### 数据源发现

_列出所有 Prometheus 和 Loki 数据源。_

![列出数据源；权限提示](images/gemini-grafana-list-datasources.webp)

![列出数据源；结果](images/list-datasources-result.webp)

### 日志检查

Gemini 会解析用户意图，并将请求转换为精确的 LogQL 查询：`{device_name="edge-device-01"} |= "nginx"`。一旦系统识别出 Loki 为当前活跃的数据源，AI 就会自主构造该命令，弥合人类意图与复杂语法之间的鸿沟。该查询定位到特定的 Kubernetes Pod 日志，提取原始的 OpenTelemetry (OTel) 数据——包括 Pod UID、容器元数据和系统标签——Gemini 随后据此定位容器化环境中问题的根因。

![基于 Loki 标签过滤日志](images/mcp-docker-grafana-loki-1.webp)


![Gemini 通过 MCP docker 获取 Grafana 日志](images/mcp-docker-grafana-loki-2.webp)

在最后一步，Gemini 会对原始遥测数据进行推理。在筛查数百行日志确认 Nginx 日志存在之后，Gemini 从日志流中提取出一条隐藏其中的 node_filesystem_device_error。通过揭示这一关键事件，它提醒 DevOps 工程师边缘节点上存在卷挂载问题，从而把原始数据转化为可执行的事件报告。

![Gemini 给出发现的总体结论](images/mcp-docker-grafana-loki-3.webp)

### 仪表板导航

_我们有多少个仪表板？_

![我们有多少个仪表板？](images/mcp-grafana-dashboards.webp)

_告诉我 X 仪表板的概要_

![X 仪表板的概要](images/mcp-grafana-summary-dashboard.webp)

### 其他场景

假设你收到告警，某个应用变慢了。你可以：

1.  使用 `list_alert_rules` 查看哪条告警正在触发。
2.  使用 `search_dashboards` 找到相关的应用仪表板。
3.  对关键面板使用 `get_panel_image`，直观地查看性能尖峰。
4.  使用 `query_loki_logs` 搜索尖峰时间段内的 "error" 或 "timeout" 消息。
5.  如果找到了根因，使用 create_incident 启动正式响应流程，并使用 `add_activity_to_incident` 记录你的发现。

## 后续步骤

- 了解 [高级 LogQL 查询](https://grafana.com/docs/loki/latest/query/log_queries/)
- 设置 [团队级 MCP 配置](https://modelcontextprotocol.io/docs/develop/connect-local-servers)
- 探索 [使用 MCP 的 Grafana 告警](https://github.com/grafana/mcp-grafana)
- 在 [Docker 社区论坛](https://forums.docker.com) 获取帮助

在搭建 Docker MCP 环境或定制 Gemini 提示词时需要帮助？请访问 [Docker 社区论坛](https://forums.docker.com) 或参阅 [入门指南](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/)。

