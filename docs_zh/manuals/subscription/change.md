---
title: 更改您的订阅
description: 升级或降级您的 Docker 订阅，并了解账单变更
keywords: 升级订阅, 降级订阅, docker 定价, 订阅变更
aliases:
- /docker-hub/upgrade/
- /docker-hub/billing/upgrade/
- /subscription/upgrade/
- /subscription/downgrade/
- /subscription/core-subscription/upgrade/
- /subscription/core-subscription/downgrade/
- /docker-hub/cancel-downgrade/
- /docker-hub/billing/downgrade/
- /billing/scout-billing/
- /billing/subscription-management/
weight: 30
---

{{% include "tax-compliance.md" %}}

您可以随时升级或降级您的 Docker 订阅，以满足不断变化的需求。本文档说明如何进行订阅变更，以及在账单和功能访问方面会发生什么变化。

> [!NOTE]
>
> 传统 Docker 订阅用户在进行订阅变更时使用不同的界面。传统订阅适用于在 2024 年 12 月 10 日之前最后一次购买或续订的订阅用户。详情请参阅 [Docker 计划升级公告](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

## 升级您的订阅

当您升级 Docker 订阅时，您将立即获得新订阅层级中的所有功能和权益。详细功能信息请参阅 [Docker 定价](https://www.docker.com/pricing)。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要升级您的订阅：

1. 登录到 [Docker Home](https://app.docker.com/)，并选择您要升级的组织。
1. 选择 **Billing**（账单）。
1. 可选：如果您从免费的 Personal 订阅升级到 Team 订阅，并且希望保留您的用户名，[将您的用户账户转换为组织](../admin/organization/convert-account.md)。
1. 选择 **Upgrade**（升级）。
1. 按照屏幕上的说明完成升级。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，您必须验证该账户。更多信息请参阅 [验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要将您的传统 Docker 订阅升级为包含所有工具访问权限的新 Docker 订阅，请联系 [Docker 销售](https://www.docker.com/pricing/contact-sales/)。

{{< /tab >}}
{{< /tabs >}}

## 降级您的订阅

您可以在续订日期之前的任何时间降级您的 Docker 订阅。未使用的部分不可退款，但您在下一个计费周期之前仍可继续使用付费功能。

### 降级注意事项

在降级之前，请考虑以下事项：

- 团队规模和仓库：您可能需要根据新订阅的限制，减少团队成员数量，或将私有仓库转换为公开仓库或删除它们。
- SSO 和 SCIM：如果您从 Docker Business 降级，且您的组织使用单点登录，需要先移除 SSO 连接和已验证的域名。通过 SCIM 自动配置的组织成员需要重置密码，才能在不使用 SSO 的情况下登录。
- 私有仓库协作者：Personal 订阅不包含私有仓库的协作者。从 Pro 降级到 Personal 时，所有协作者将被移除，额外的私有仓库将被锁定。

各层级的功能限制，请参阅 [Docker 定价](https://www.docker.com/pricing)。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

> [!IMPORTANT]
>
> 如果您有 [销售协助的 Docker Business 订阅](details.md#sales-assisted)，请联系您的客户经理来降级您的订阅。

要降级您的订阅：

1. 登录到 [Docker Home](https://app.docker.com/)，并选择您要降级的组织。
1. 选择 **Billing**（账单）。
1. 选择操作图标，然后选择 **Cancel subscription**（取消订阅）。
1. 填写反馈调查表以继续取消订阅。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

> [!IMPORTANT]
>
> 如果您有 [销售协助的 Docker Business 订阅](details.md#sales-assisted)，请联系您的客户经理来降级您的订阅。

要降级您的传统 Docker 订阅：

1. 登录到 [Docker Hub](https://hub.docker.com/billing)。
1. 选择您要降级的组织，然后选择 **Billing**（账单）。
1. 要降级，您必须导航到升级计划页面。选择 **Upgrade**（升级）。
1. 在升级页面上，在 **Free Team** 计划卡片中选择 **Downgrade**（降级）。
1. 按照屏幕上的说明完成降级。

要降级您的 Docker Build Cloud 订阅：

1. 登录到 [Docker Home](https://app.docker.com) 并选择 **Build Cloud**。
1. 选择 **Account settings**（账户设置），然后选择 **Downgrade**（降级）。
1. 要确认降级，在文本框中输入 **DOWNGRADE**，然后选择 **Yes, continue**（是的，继续）。
1. 账户设置页面将更新，显示一条通知栏，告知您的降级日期（下一个计费周期开始）。

{{< /tab >}}
{{< /tabs >}}

## 订阅暂停政策

您无法暂停或延迟订阅。如果订阅发票在到期日之前未支付，将从到期日起有 15 天的宽限期。