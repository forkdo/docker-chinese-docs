---
title: 发票和账单历史
weight: 40
description: 了解如何查看发票和账单历史，以及如何验证账单续订日期
keywords: 支付, 账单, 订阅, 发票, 续订, 发票管理, 账单管理, 支付发票
aliases:
    - /billing/core-billing/history/
---

了解如何查看和支付发票、查看账单历史，以及验证账单续订日期。所有月度和年度订阅将在订阅期结束时使用您的默认支付方式自动续订。

{{% include "tax-compliance.md" %}}

## 查看发票

您的发票包含以下内容：

- 发票编号
- 开票日期
- 到期日期
- 您的“账单寄送”信息
- 应付金额（USD）
- 在线支付：选择此链接在线支付您的发票
- 订单描述（如适用数量）、单价和金额（USD）
- 小计、折扣（如适用）和总计

发票中“账单寄送”部分的信息基于您的账单信息。并非所有字段都是必需的。账单信息包括以下内容：

- 姓名（必填）：管理员或公司的名称
- 地址（必填）
- 电子邮件地址（必填）：接收账户所有账单相关邮件的邮箱
- 电话号码
- 税号或增值税号（VAT）

您无法修改已支付或未支付的账单发票。当您更新账单信息时，此更改不会更新现有发票。

如果您需要更新账单信息，请务必在订阅续订日期之前完成，此时发票将被最终确定。

更多信息，请参阅 [更新账单信息](details.md)。

## 支付发票

> [!NOTE]
>
> 按发票支付仅适用于选择年度计费周期的订阅用户。要更改您的计费周期，请参阅 [更改您的计费周期](/manuals/billing/cycle.md)。

如果您为订阅选择了按发票支付，您将在到期日前 10 天、到期日当天和到期日后 15 天收到邮件提醒以支付发票。

您可以通过 Docker 账单控制台支付发票：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing（账单）**。
1. 选择 **Invoices（发票）**，找到您要支付的发票。
1. 在 **Actions（操作）** 列中，选择 **Pay invoice（支付发票）**。
1. 填写您的支付详细信息，然后选择 **Pay（支付）**。

当您的付款处理完成后，发票的 **Status（状态）** 列将更新为 **Paid（已支付）**，您将收到确认邮件。

如果您选择使用美国银行账户支付，您必须验证该账户。更多信息，请参阅 [验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

### 查看续订日期

{{< tabs >}}
{{< tab name="Docker subscription" >}}

您在订阅续订时收到发票。要验证您的续订日期，请登录 [Docker Home Billing](https://app.docker.com/billing)。您的续订日期和金额将显示在订阅计划卡片上。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

您在订阅续订时收到发票。要验证您的续订日期：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的用户头像以打开下拉菜单。
1. 选择 **Billing（账单）**。
1. 选择用户或组织账户以查看账单详细信息。在这里您可以找到续订日期和续订金额。

{{< /tab >}}
{{< /tabs >}}

## 在发票上包含您的增值税号（VAT）

> [!NOTE]
>
> 如果 VAT 号字段不可用，请填写 [联系支持表格](https://hub.docker.com/support/contact/)。此字段可能需要手动添加。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

添加或更新您的 VAT 号：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing（账单）**。
1. 从左侧菜单选择 **Billing information（账单信息）**。
1. 在您的账单信息卡片上选择 **Change（更改）**。
1. 确保勾选 **I'm purchasing as a business（以企业身份购买）** 复选框。
1. 在 Tax ID（税号）部分输入您的 VAT 号。

    > [!IMPORTANT]
    >
    > 您的 VAT 号必须包含国家前缀。例如，如果您为德国输入 VAT 号，您应输入 `DE123456789`。

1. 选择 **Update（更新）**。

您的 VAT 号将包含在您的下一张发票上。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

添加或更新您的 VAT 号：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing（账单）**。
1. 选择 **Billing address（账单地址）** 链接。
1. 在 **Billing Information（账单信息）** 部分，选择 **Update information（更新信息）**。
1. 在 Tax ID（税号）部分输入您的 VAT 号。

    > [!IMPORTANT]
    >
    > 您的 VAT 号必须包含国家前缀。例如，如果您为德国输入 VAT 号，您应输入 `DE123456789`。

1. 选择 **Save（保存）**。

您的 VAT 号将包含在您的下一张发票上。

{{< /tab >}}
{{< /tabs >}}

## 查看账单历史

您可以查看个人账户或组织的账单历史，并下载过去的发票。

### 个人账户

{{< tabs >}}
{{< tab name="Docker subscription" >}}

查看账单历史：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing（账单）**。
1. 从左侧菜单选择 **Invoices（发票）**。
1. 可选：选择 **Invoice number（发票编号）** 以打开发票详细信息。
1. 可选：选择 **Download（下载）** 按钮下载发票。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

查看账单历史：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing（账单）**。
1. 选择 **Payment methods and billing history（支付方式和账单历史）** 链接。

您可以在 **Invoice History（发票历史）** 部分找到过去的发票，并下载发票。

{{< /tab >}}
{{< /tabs >}}

### 组织

您必须是组织的所有者才能查看账单历史。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

查看账单历史：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
1. 选择 **Billing（账单）**。
1. 从左侧菜单选择 **Invoices（发票）**。
1. 可选：选择 **invoice number（发票编号）** 以打开发票详细信息。
1. 可选：选择 **download（下载）** 按钮下载发票。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

查看账单历史：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择您的组织，然后选择 **Billing（账单）**。
1. 选择 **Payment methods and billing history（支付方式和账单历史）** 链接。

您可以在 **Invoice History（发票历史）** 部分找到过去的发票，并下载发票。

{{< /tab >}}
{{< /tabs >}}