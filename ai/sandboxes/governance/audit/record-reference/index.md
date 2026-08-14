# 审计记录参考


Docker AI 治理审计记录在各种投递模式下使用同一套 schema。本地 JSON Lines 文件与云端投递的记录包含相同的元数据字段。

记录仅捕获元数据，不包含提示内容、智能体输出或参数值。当参数键有助于识别某个动作时，它们可能会出现。

## 公共字段

| 字段               | 说明                                                                                                             |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `audit_event_id`   | 审计事件的唯一 ID。                                                                                              |
| `timestamp`        | Docker 记录该事件时的 UTC 时间。                                                                                 |
| `schema_version`   | 记录 schema 的版本。请将 SIEM 字段映射固定到该值。                                                               |
| `category`         | 事件类别，例如 `AUDIT_CATEGORY_MANAGEMENT`、`AUDIT_CATEGORY_EVALUATION` 或 `AUDIT_CATEGORY_EXECUTION`。          |
| `decision`         | 评估记录的治理决策。                                                                                             |
| `username`         | 已登录 Docker 用户的 Docker Hub 用户名。                                                                         |
| `user_email`       | 已登录 Docker 用户的电子邮件地址。                                                                               |
| `org_id`           | 其治理策略正在生效的组织的 ID。                                                                                  |
| `org_name`         | 其治理策略正在生效的组织的显示名称。                                                                             |
| `audit_session_id` | 标识产生该记录的守护进程会话。                                                                                   |
| `resource_id`      | 评估的目标，例如主机与端口、文件路径或工具。                                                                     |
| `os`               | 产生该记录的操作系统。                                                                                           |
| `app_version`      | 产生该记录的 Docker 组件版本。                                                                                   |
| `client_name`      | 来源组件，例如 Docker 沙箱对应的 `sbx`。                                                                         |
| `hostname`         | 产生该记录的机器的主机名。                                                                                       |
| `deny_reason`      | 被拒绝的请求为何被阻止。出现在拒绝决策中。                                                                       |
| `action_type`      | 载荷判别字段，用于标识记录中特定动作的对象。                                                                     |
| `agent`            | 与该事件关联的 AI 智能体（在 Docker 已知的情况下）。                                                             |

## 类别

| 类别                        | 说明                                             |
| --------------------------- | ------------------------------------------------ |
| `AUDIT_CATEGORY_MANAGEMENT` | 会话生命周期、策略同步与配置事件。               |
| `AUDIT_CATEGORY_EVALUATION` | 治理策略决策，例如允许、拒绝或同意。             |
| `AUDIT_CATEGORY_EXECUTION`  | 被评估的动作执行后的结果。                       |

## 决策

| 决策                               | 说明                               |
| ---------------------------------- | ---------------------------------- |
| `AUDIT_DECISION_ALLOW`             | Docker 允许了该动作。              |
| `AUDIT_DECISION_DENY`              | Docker 拒绝了该动作。              |
| `AUDIT_DECISION_APPROVAL_REQUIRED` | Docker 要求在动作执行前取得同意。  |
| `AUDIT_DECISION_APPROVED`          | 同意请求已被批准。                 |
| `AUDIT_DECISION_REJECTED`          | 同意请求已被拒绝。                 |

## 动作类型

`action_type` 字段标识记录中特定动作的载荷。

| 动作类型               | 说明                             |
| ---------------------- | -------------------------------- |
| `session`              | 沙箱守护进程会话生命周期事件。   |
| `network_egress`       | 网络访问评估。                   |
| `filesystem_mount`     | 文件系统挂载或路径访问评估。     |
| `tool_invocation`      | 工具调用评估。                   |
| `resource_read`        | 资源读取评估。                   |
| `server_registration`  | 服务器注册事件。                 |
| `prompt`               | 与提示相关的元数据事件。         |
| `network_execution`    | 网络动作的执行结果。             |
| `filesystem_execution` | 文件系统动作的执行结果。         |
| `tool_execution`       | 工具调用的执行结果。             |
| `resource_execution`   | 资源读取的执行结果。             |
| `policy_sync`          | 策略同步事件。                   |
| `pii_detection`        | 数据检测结果的元数据事件。       |
| `c_score_report`       | C-score 报告的元数据事件。       |
| `policy_action`        | 策略配置或策略动作事件。         |

## 记录示例

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

