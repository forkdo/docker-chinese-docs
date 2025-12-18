---
title: 更改账单周期
weight: 50
description: 了解如何更改 Docker 订阅的账单周期
keywords: billing, cycle, payments, subscription
---

购买订阅时，您可以选择按月或按年计费周期。如果您当前使用的是按月计费周期，可以选择切换到按年计费周期。

如果您使用的是月付计划，可以随时切换到年付计划。但是，不支持从年付切换到月付。

更改账单周期时：

- 您的下次账单日期将反映新的计费周期。要查看下次账单日期，请参阅 [查看续费日期](history.md#view-renewal-date)。
- 您订阅的开始日期会重置。例如，如果月度订阅从 3 月 1 日开始到 4 月 1 日结束，在 2024 年 3 月 15 日切换计费周期后，新的开始日期将重置为 2024 年 3 月 15 日，结束日期为 2025 年 3 月 15 日。
- 您月度订阅中未使用的部分将按比例折算，作为积分抵扣年付订阅费用。例如，如果您的月度费用是 10 美元，已使用价值为 5 美元，当您切换到年度周期（100 美元）时，最终收费为 95 美元（100 - 5）。

{{% include "tax-compliance.md" %}}

## 将个人账户更改为年度周期

{{< tabs >}}
{{< tab name="Docker subscription" >}}

> [!IMPORTANT]
>
> 订阅升级或变更不支持发票支付。

要更改账单周期：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing**（账单）。
1. 在计划和使用情况页面，选择 **Switch to annual billing**（切换到年度计费）。
1. 确认您的账单信息。
1. 选择 **Continue to payment**（继续支付）。
1. 确认支付信息，然后选择 **Upgrade subscription**（升级订阅）。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，必须验证该账户。更多信息，请参阅
> [验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

账单计划和使用情况页面现在将显示您的新年度计划详细信息。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

请按照以下步骤将旧版 Docker 订阅从月付切换到年付：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**（账单）。
1. 在 **Plan**（计划）选项卡的右下角，选择 **Switch to annual billing**（切换到年度计费）。
1. 查看 **Change to an Annual subscription**（更改为年度订阅）页面上显示的信息，然后选择 **Accept Terms and Purchase**（接受条款并购买）以确认。

{{< /tab >}}
{{< /tabs >}}

## 将组织更改为年度周期

您必须是组织所有者才能更改支付信息。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

> [!IMPORTANT]
>
> 订阅升级或变更不支持发票支付。

请按照以下步骤将组织的 Docker 订阅从月付切换到年付：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing**（账单）。
1. 在计划和使用情况页面，选择 **Switch to annual billing**（切换到年度计费）。
1. 确认您的账单信息。
1. 选择 **Continue to payment**（继续支付）。
1. 确认支付信息，然后选择 **Upgrade subscription**（升级订阅）。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，必须验证该账户。更多信息，请参阅
> [Verify a bank account](manuals/billing/payment-method.md#verify-a-bank-account)（验证银行账户）。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

请按照以下步骤将旧版 Docker 组织订阅从月付切换到年付：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing**（账单）。
1. 选择 **Switch to annual billing**（切换到年度计费）。
1. 查看 **Change to an Annual subscription**（更改为年度订阅）页面上显示的信息，然后选择 **Accept Terms and Purchase**（接受条款并购买）以确认。

{{< /tab >}}
{{< /tabs >}}