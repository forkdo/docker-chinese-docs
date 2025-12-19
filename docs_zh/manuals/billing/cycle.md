---
title: 更改账单周期
weight: 50
description: 了解如何更改 Docker 订阅的账单周期
keywords: billing, cycle, payments, subscription
---

购买订阅时，您可以在月度或年度账单周期之间进行选择。如果您当前是月度账单周期，可以选择切换到年度账单周期。

如果您使用的是月度计划，可以随时切换到年度计划。但是，不支持从年度计划切换到月度计划。

当您更改账单周期时：

- 您的下一个账单日期将反映新的周期。要查找下一个账单日期，请参阅[查看续订日期](history.md#view-renewal-date)。
- 您的订阅开始日期将重置。例如，如果月度订阅从 3 月 1 日开始，到 4 月 1 日结束，那么在 2024 年 3 月 15 日切换账单周期时，新的开始日期将重置为 2024 年 3 月 15 日，结束日期为 2025 年 3 月 15 日。
- 月度订阅中任何未使用的部分将按比例折算，并作为信用额度用于年度订阅。例如，如果您的月度费用为 10 美元，您的已使用价值为 5 美元，当您切换到年度周期（100 美元）时，最终费用为 95 美元（100 美元 - 5 美元）。

{{% include "tax-compliance.md" %}}

## 将个人账户更改为年度周期

{{< tabs >}}
{{< tab name="Docker subscription" >}}

> [!IMPORTANT]
>
> 订阅升级或更改不支持通过发票付款。

更改账单周期的步骤：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 在计划和用量页面上，选择 **Switch to annual billing**（切换到年度账单）。
4. 验证您的账单信息。
5. 选择 **Continue to payment**（继续付款）。
6. 验证付款信息并选择 **Upgrade subscription**（升级订阅）。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，则必须验证该账户。有关更多信息，请参阅[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

计划和用量页面现在将显示您的新年度计划详细信息。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

请按照以下步骤将旧版 Docker 订阅从月度切换到年度账单周期：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 在 **Plan**（计划）选项卡的右下角，选择 **Switch to annual billing**（切换到年度账单）。
4. 查看 **Change to an Annual subscription**（更改为年度订阅）页面上显示的信息，然后选择 **Accept Terms and Purchase**（接受条款并购买）进行确认。

{{< /tab >}}
{{< /tabs >}}

## 将组织更改为年度周期

您必须是组织所有者才能更改付款信息。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

> [!IMPORTANT]
>
> 订阅升级或更改不支持通过发票付款。

请按照以下步骤将组织的 Docker 订阅从月度切换到年度账单周期：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 在计划和用量页面上，选择 **Switch to annual billing**（切换到年度账单）。
4. 验证您的账单信息。
5. 选择 **Continue to payment**（继续付款）。
6. 验证付款信息并选择 **Upgrade subscription**（升级订阅）。

> [!NOTE]
>
> 如果您选择使用美国银行账户付款，则必须验证该账户。有关更多信息，请参阅[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

请按照以下步骤将旧版 Docker 组织订阅从月度切换到年度账单周期：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Switch to annual billing**（切换到年度账单）。
4. 查看 **Change to an Annual subscription**（更改为年度订阅）页面上显示的信息，然后选择 **Accept Terms and Purchase**（接受条款并购买）进行确认。

{{< /tab >}}
{{< /tabs >}}