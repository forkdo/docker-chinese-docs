---
title: 本地审计日志
linkTitle: 本地审计日志
weight: 10
description: 从沙箱守护进程写入的本地 JSON Lines 文件中收集 Docker AI 治理审计记录。
keywords: docker sandboxes, audit log, local audit logs, audit logging, jsonl, SIEM, splunk, filebeat
---

沙箱守护进程以 JSON Lines（`.jsonl`）文件的形式写入本地审计记录。本地审计日志保留在产生它们的主机上，可由你自己的日志采集器收集。本地投递独立于[云端投递](configure.md)，因此无论云端投递开启还是关闭，你都可以使用本地文件。

沙箱守护进程仅为已登录、拥有 AI 治理许可证且受强制执行的集中式[组织策略](../access-controls/organization.md)管辖的用户写入本地审计记录。不同时满足这两个条件的 Docker 沙箱用户不会向审计日志发送审计数据。要确认治理已生效，请运行 `sbx policy ls`。当组织策略正在生效时，其输出会包含一行 `Governance: Managed by <org>`。

## 记录哪些内容

守护进程会写入两类本地记录：

- 评估记录捕获每一次策略决策：资源、动作、判定结果，以及拒绝的原因。
- 会话生命周期记录标记每次守护进程运行的开始和结束。评估记录共享该次运行的 `audit_session_id`，因此你可以将每一次决策关联回某个守护进程会话。

记录仅包含元数据，不包含提示内容、智能体输出或参数值。有关字段细节，请参阅[审计记录参考](record-reference.md)。

一条网络评估记录形如：

```json
{
  "audit_event_id": "95e7257f-93c9-4f29-bde7-88830e2dae80",
  "timestamp": "2026-05-28T19:15:00.728933Z",
  "schema_version": "1.82.0",
  "category": "AUDIT_CATEGORY_EVALUATION",
  "decision": "AUDIT_DECISION_DENY",
  "username": "jordandoe",
  "user_email": "jordandoe@example.com",
  "org_id": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "org_name": "Acme Inc",
  "audit_session_id": "8a3bc076-79d0-4502-baf3-cc6ad35fb578",
  "resource_id": "example.com:443",
  "os": "macos",
  "app_version": "v0.31.0",
  "client_name": "sbx",
  "hostname": "host-machine",
  "deny_reason": [
    "no applicable policies for op(action=net:connect:tcp, resource=net:domain:example.com:443)"
  ],
  "action_type": "network_egress",
  "network_egress": { "protocol": "tcp" },
  "agent": "claude"
}
```

## 记录存储位置

写入审计记录的是守护进程，而不是 CLI。运行诸如 `sbx create` 之类的命令会向守护进程发送请求，守护进程则将由此产生的记录发出到其自身的审计目录。

默认位置取决于你的操作系统：

| 操作系统 | 默认路径                                                          |
| -------- | ----------------------------------------------------------------- |
| macOS    | `~/Library/Logs/com.docker.sandboxes/sandboxes/auditkit/`         |
| Linux    | `${XDG_STATE_HOME:-~/.local/state}/sandboxes/sandboxes/auditkit/` |
| Windows  | `%LOCALAPPDATA%\DockerSandboxes\sandboxes\logs\auditkit\`         |

由于每种操作系统会将应用日志放在各自约定的位置，因此目录布局因平台而异。

文件命名为 `audit-<utc-timestamp>-<process-uuid>-<seq>.jsonl`。

守护进程将进行中的记录写入临时的 `.tmp` 文件，并通过原子重命名将其最终确定为 `.jsonl` 文件。最终确定发生在轮转阈值处：默认为 5 分钟、1000 个事件或 50 MiB，以先达到者为准。守护进程正常关闭时也会进行最终确定。只有 `.jsonl` 文件是完整的。请将 `.tmp` 文件视为不完整，不要收集它们。

沙箱永远不会删除 `.jsonl` 文件。留存与清理由你的日志采集器或你自己的维护工作负责。

## 使用 SIEM 收集记录

将你的日志采集器指向审计目录，并将其配置为只收集 `.jsonl` 文件。诸如 Splunk Universal Forwarder、Filebeat 和 CrowdStrike Falcon LogScale 等工具会读取该目录，并将每一行作为一个事件转发。由于进行中的记录在最终确定之前存放于 `.tmp` 文件中，采集器永远不会看到不完整的记录。
