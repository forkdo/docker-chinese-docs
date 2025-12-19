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

您可以随时升级或降级您的 Docker 订阅，以满足不断变化的需求。本页介绍如何更改订阅，以及账单和功能访问方面会发生什么变化。

> [!NOTE]
>
> 旧版 Docker 订阅者更改订阅的界面有所不同。旧版订阅适用于在 2024 年 12 月 10 日之前最后一次购买或续订的订阅者。有关详细信息，请参阅[宣布升级后的 Docker 计划](https://www.docker.com/blog/november-2024-updated-plans-announcement/)。

## 升级您的订阅

当您升级 Docker 订阅时，您将立即获得新订阅层级中的所有功能和权益。有关详细的功能信息，请参阅 [Docker 定价](https://www.docker.com/pricing)。

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

要升级您的订阅：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您要升级的组织。
2. 选择 **Billing**（账单）。
3. （可选）如果您要从免费的 Personal 订阅升级到 Team 订阅并希望保留您的用户名，请[将您的用户帐户转换为组织](../admin/organization/convert-account.md)。
4. 选择 **Upgrade**（升级）。
5. 按照屏幕上的说明完成升级。

> [!NOTE]
>
> 如果您选择使用美国银行帐户付款，则必须验证该帐户。有关更多信息，请参阅[验证银行帐户](manuals/billing/payment-method.md#verify-a-bank-account)。

{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

要将您的旧版 Docker 订阅升级为包含所有工具访问权限的新版 Docker 订阅，请联系 [Docker 销售团队](https://www.docker.com/pricing/contact-sales/)。

{{< /tab >}}
{{< /tabs >}}

## 降级您的订阅

您可以在续订日期之前的任何时间降级您的 Docker 订阅。未使用的部分不予退款，但您在下一个计费周期之前仍可继续使用付费功能。

### 降级注意事项

在降级之前，请考虑以下几点：

- **团队规模和仓库**：您可能需要减少团队成员，并根据新订阅的限制将私有仓库转换为公共仓库或删除它们。
- **SSO 和 SCIM**：如果您要从 Docker Business 降级，并且您的组织使用了单点登录 (SSO)，请先移除您的 SSO 连接和已验证的域名。通过 SCIM 自动配置的组织成员需要重置其密码才能在没有 SSO 的情况下登录。
- **私有仓库协作者**：个人订阅不包含私有仓库的协作者。当从 Pro 降级到 Personal 时，所有协作者都会被移除，额外的私有仓库将被锁定。

有关每个层级的功能限制，请参阅 [Docker 定价](https://www.docker.com/pricing)。

{{< tabs >}}
{{< tab name="Docker 订阅" >}}

> [!IMPORTANT]
>
> 如果您拥有通过销售协助购买的 Docker Business 订阅，请联系您的客户经理以降级您的订阅。

要降级您的订阅：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您要降级的组织。
2. 选择 **Billing**（账单）。
3. 选择操作图标，然后选择 **Cancel subscription**（取消订阅）。
4. 填写反馈调查以继续取消。

{{< /tab >}}
{{< tab name="旧版 Docker 订阅" >}}

> [!IMPORTANT]
>
> 如果您拥有通过销售协助购买的 Docker Business 订阅，请联系您的客户经理以降级您的订阅。

要降级您的旧版 Docker 订阅：

1. 登录 [Docker Hub](https://hub.docker.com/billing)。
2. 选择您要降级的组织，然后选择 **Billing**（账单）。
3. 要降级，您必须导航到升级计划页面。选择 **Upgrade**（升级）。
4. 在升级页面上，在 **Free Team** 计划卡片中选择 **Downgrade**（降级）。
5. 按照屏幕上的说明完成降级。

要降级您的 Docker Build Cloud 订阅：

1. 登录 [Docker Home](https://app.docker.com) 并选择 **Build Cloud**。
2. 选择 **Account settings**（帐户设置），然后选择 **Downgrade**（降级）。
3. 要确认降级，请在文本字段中输入 **DOWNGRADE**，然后选择 **Yes, continue**（是，继续）。
4. 帐户设置页面将更新一个通知栏，告知您的降级日期（下一个计费周期开始时）。

{{< /tab >}}
{{< /tabs >}}

## 订阅暂停政策

您无法暂停或延迟订阅。如果订阅发票在到期日未支付，则从到期日开始有 15 天的宽限期。