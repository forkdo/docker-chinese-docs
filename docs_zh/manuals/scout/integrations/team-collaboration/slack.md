---
title: 将 Docker Scout 与 Slack 集成
linkTitle: Slack
description: |
  将 Docker Scout 与 Slack 集成，以在 Slack 频道中接收关于漏洞和策略合规性的实时更新
keywords: scout, team collaboration, slack, notifications, updates
---

您可以通过创建 Slack Webhook 并将其添加到 Docker Scout 仪表板，从而将 Docker Scout 与 Slack 集成。当新的漏洞被披露并影响您一个或多个镜像时，Docker Scout 会通知您。

![来自 Docker Scout 的 Slack 通知](../../images/scout-slack-notification.png?border=true "来自 Docker Scout 的 Slack 通知示例")

## 工作原理

配置集成后，Docker Scout 会将有关您的仓库策略合规性和漏洞暴露情况变更的通知，发送到与 Webhook 关联的 Slack 频道。

> [!NOTE]
>
> 通知仅针对每个仓库的*最后推送*的镜像标签触发。“最后推送”指的是最近推送到注册表并由 Docker Scout 分析的镜像标签。如果最后推送的镜像不受新披露的 CVE 影响，则不会触发通知。

有关 Docker Scout 通知的更多信息，请参阅 [通知设置](/manuals/scout/explore/dashboard.md#notification-settings)。

## 设置

要添加 Slack 集成：

1.  创建一个 Webhook，请参阅 [Slack 文档](https://api.slack.com/messaging/webhooks)。
2.  转到 Docker Scout 仪表板中的 [Slack 集成页面](https://scout.docker.com/settings/integrations/slack/)。
3.  在 **How to integrate**（如何集成）部分，输入一个 **Configuration name**（配置名称）。
    Docker Scout 将此标签用作集成的显示名称，因此您可能希望将默认名称更改为更有意义的名称。
    例如 `#channel-name`，或者此配置所属团队的名称。
4.  在 **Slack webhook** 字段中粘贴您刚刚创建的 Webhook。

    如果您希望验证连接，请选择 **Test webhook**（测试 Webhook）按钮。
    Docker Scout 将向指定的 Webhook 发送测试消息。

5.  选择是为所有已启用 Scout 的镜像仓库启用通知，还是输入您希望发送通知的仓库名称。
6.  准备好启用集成时，选择 **Create**（创建）。

创建 Webhook 后，Docker Scout 开始向与 Webhook 关联的 Slack 频道发送通知更新。

## 删除 Slack 集成

要删除 Slack 集成：

1.  转到 Docker Scout 仪表板中的 [Slack 集成页面](https://scout.docker.com/settings/integrations/slack/)。
2.  选择您要删除的集成旁边的 **Remove**（删除）图标。
3.  在确认对话框中再次选择 **Remove**（删除）进行确认。