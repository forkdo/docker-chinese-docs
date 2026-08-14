---
title: SIEM 转发
linkTitle: SIEM 转发
weight: 35
description: 将 Docker AI 治理审计事件转发到 Splunk、Dynatrace、Datadog 或自定义 HTTPS 端点。
keywords: docker sandboxes, SIEM, audit logs, Splunk, Dynatrace, Datadog, AI Governance, forwarding, NDJSON
---

Docker 可以将审计事件转发到你的安全信息与事件管理（SIEM）系统，让你能够将 Docker 治理数据与其他安全信号集中在一起。Docker 在保存之前会使用所提供的凭据验证该端点是否可达。

## 支持的目标

| 目标                             | 说明                                                     |
| -------------------------------- | -------------------------------------------------------- |
| Splunk Cloud (HEC)               | 使用 HTTP Event Collector 的托管 Splunk                  |
| Splunk Enterprise（自托管）      | 使用 HTTP Event Collector 的自托管 Splunk                |
| Dynatrace                        | 使用 Log Ingest API 的 Dynatrace Log Management          |
| Datadog                          | 使用 HTTP log intake API 的 Datadog Logs                 |
| 自定义 HTTPS 端点（高级）        | 任何接受带自定义认证头的 HTTPS 的 SIEM                   |

对于任何没有原生集成的 SIEM，请使用自定义 HTTPS 端点选项。自定义端点接收 JSON Lines（NDJSON），其中每一行都是一条完整的审计记录。

## 准备工作

SIEM 转发要求你的组织已启用 Docker Cloud 投递。如果尚未启用，请在配置 SIEM 目标之前，在 **AI Platform** > **Audit logs** > **Audit delivery** 下将其启用。请参阅[配置审计投递](configure.md)。

在配置转发之前，先从你的 SIEM 收集凭据：

- **Splunk Cloud**：HEC 摄取 URL 和一个 HEC 令牌。可选地，提供一个 Splunk 索引名称。请参阅 [Splunk 文档](https://docs.splunk.com/)。
- **Splunk Enterprise**：HEC 端点 URL（通常为 8088 端口）和一个 HEC 令牌。该端点必须提供公开受信任的 TLS 证书。可选地，提供一个 Splunk 索引名称。请参阅 [Splunk 文档](https://docs.splunk.com/)。
- **Dynatrace**：Log Ingest API URL 和一个具有 `logs.ingest` 作用域的 API 令牌。请参阅 [Dynatrace 文档](https://docs.dynatrace.com/)。
- **Datadog**：对应你的 Datadog 站点的 Logs 摄取 URL 和一个 API 密钥。请参阅 [Datadog 文档](https://docs.datadoghq.com/)。
- **自定义 HTTPS 端点**：你的端点 URL、认证头名称，以及包含任意方案（例如 `Bearer <token>`）在内的完整头值。

## 添加 SIEM 目标

1. 登录 [Docker Home](https://app.docker.com/)。
1. 打开你的组织。
1. 前往 **AI Platform** > **Audit logs**。
1. 打开 **Export & Connectors**。
1. 选择 **Add destination**。
1. 选择你的目标并完成表单填写。
1. 选择 **Save**。

如果验证失败，请检查 URL 和凭据是否正确，以及该端点是否可从互联网访问。

## 管理目标

在 **SIEM forwarding** 列表中，选择某个目标旁边的菜单以编辑或删除它。编辑表单允许你更新凭据，并为该目标开启或关闭转发。删除某个目标会永久移除该端点及其存储的凭据，且无法撤销。
