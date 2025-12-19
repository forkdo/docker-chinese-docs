---
title: 管理订阅席位
linkTitle: 管理席位
description: 为 Docker Team 和 Business 订阅添加或移除席位
keywords: 管理席位, 添加席位, 移除席位, 订阅计费, 团队成员
aliases:
- /docker-hub/billing/add-seats/
- /subscription/add-seats/
- /docker-hub/billing/remove-seats/
- /subscription/remove-seats/
- /subscription/core-subscription/add-seats/
- /subscription/core-subscription/remove-seats/
weight: 20
---

您可以随时为 Docker Team 或 Business 订阅添加或移除席位，以适应团队变动。在计费周期中途添加席位时，系统会按额外席位的比例收取费用。

{{% include "tax-compliance.md" %}}

## 为订阅添加席位

{{< tabs >}}
{{< tab name="Docker subscription" >}}

> [!IMPORTANT]
>
> 如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来添加席位。

添加席位的方法如下：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing**。
1. 选择 **Add seats** 并按照屏幕上的说明完成席位添加。请注意，购买额外席位时不能使用发票支付，必须使用信用卡或美国银行账户。

> [!NOTE]
>
> 如果您选择使用美国银行账户支付，则必须验证账户。更多信息，请参阅 [验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

现在您可以向组织中添加更多成员。更多信息，请参阅 [管理组织成员](../admin/organization/members.md)。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

> [!IMPORTANT]
>
> 如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来添加席位。

为 Legacy Docker 订阅添加席位的方法如下：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 在 Billing 页面，选择 **Add seats**。
1. 选择您要添加的席位数量，然后选择 **Purchase**。

为 Docker Build Cloud 添加席位的方法如下：

1. 登录 [Docker Home](https://app.docker.com) 并选择 **Build Cloud**。
1. 选择 **Account settings**，然后选择 **Add seats**。
1. 选择您要添加的席位数量，然后选择 **Add seats**。

{{< /tab >}}
{{< /tabs >}}

## 批量定价

Docker 为 Docker Business 订阅提供批量定价，起订量为 25 个席位。请联系 [Docker 销售团队](https://www.docker.com/pricing/contact-sales/) 获取更多信息。

## 从订阅中移除席位

您可以随时从 Team 或 Business 订阅中移除席位。变更将在下一个计费周期生效，未使用的部分不予退款。

例如，如果您每月 8 日为 10 个席位付费，并在 15 日移除了 2 个席位，则这 2 个席位仍可使用，直到下一个计费周期开始。从下一个计费周期开始，您将只需支付 8 个席位的费用。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

> [!IMPORTANT]
>
> 如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来移除席位。

移除席位的方法如下：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing**。
1. 在 **Seats** 行中，选择操作图标，然后选择 **Remove seats**。
1. 按照屏幕上的说明完成席位移除。

在下一个计费周期开始之前，您可以取消席位移除操作。如需取消，请选择 **Cancel change**。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

> [!IMPORTANT]
>
> 如果您使用的是销售协助的 Docker Business 订阅，请联系您的客户经理来移除席位。

从 Legacy Docker 订阅中移除席位的方法如下：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**。
1. 在 Billing 页面，选择 **Remove seats**。
1. 按照屏幕上的说明完成席位移除。

从 Docker Build Cloud 中移除席位的方法如下：

1. 登录 [Docker Home](https://app.docker.com) 并选择 **Build Cloud**。
1. 选择 **Account settings**，然后选择 **Remove seats**。
1. 按照屏幕上的说明完成席位移除。

{{< /tab >}}
{{< /tabs >}}