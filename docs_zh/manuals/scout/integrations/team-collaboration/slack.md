---
title: 将 Docker Scout 与 Slack 集成
linkTitle: Slack
description: |
  将 Docker Scout 与 Slack 集成，实时接收漏洞和策略合规性通知
keywords: scout, team collaboration, slack, notifications, updates
---

您可以通过创建 Slack Webhook 并将其添加到 Docker Scout 仪表板，来将 Docker Scout 与 Slack 集成。Docker Scout 将在新漏洞披露并影响您的镜像时，向您发送通知。

![Docker Scout 发送的 Slack 通知](../../images/scout-slack-notification.png?border=true "Docker Scout Slack 通知示例")

## 工作原理

配置集成后，Docker Scout 会向 Webhook 关联的 Slack 频道发送有关您的仓库策略合规性和漏洞暴露情况变化的通知。

> [!NOTE]
>
> 通知仅针对每个仓库的*最后推送*的镜像标签触发。“最后推送”指的是最近推送到注册表并被 Docker Scout 分析的镜像标签。如果最后推送的镜像不是由新披露的 CVE 引起的，则不会触发通知。

有关 Docker Scout 通知的更多信息，请参阅 [通知设置](/manuals/scout/explore/dashboard.md#notification-settings)

## 配置步骤

添加 Slack 集成：

1. 创建一个 Webhook，参见 [Slack 文档](https://api.slack.com/messaging/webhooks)。
2. 转到 Docker Scout 仪表板中的 [Slack 集成页面](https://scout.docker.com/settings/integrations/slack/)。
3. 在**如何集成**部分，输入**配置名称**。Docker Scout 使用此标签作为集成的显示名称，因此您可能需要将默认名称更改为更有意义的名称。例如 `#channel-name`，或此配置所属团队的名称。
4. 在**Slack Webhook**字段中粘贴您刚创建的 Webhook。

   如果需要验证连接，请选择**测试 Webhook**按钮。Docker Scout 将向指定的 Webhook 发送测试消息。

5. 选择是否要为所有启用 Scout 的镜像仓库启用通知，或输入要发送通知的仓库名称。
6. 准备好启用集成时，选择**创建**。

创建 Webhook 后，Docker Scout 开始向关联的 Slack 频道发送通知更新。

## 移除 Slack 集成

移除 Slack 集成：

1. 转到 Docker Scout 仪表板中的 [Slack 集成页面](https://scout.docker.com/settings/integrations/slack/)。
2. 选择要移除的集成的**移除**图标。
3. 在确认对话框中再次选择**移除**以确认。