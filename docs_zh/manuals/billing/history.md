---
title: 发票和账单历史记录
weight: 40
description: 了解如何查看发票和账单历史记录
keywords: payments, billing, subscription, invoices, renewals, invoice management, billing administration, pay invoice
aliases:
    - /billing/core-billing/history/
---

了解如何查看和支付发票、查看账单历史记录以及核实账单续订日期。所有月度和年度订阅都会在订阅期结束时使用您的默认支付方式自动续订。

{{% include "tax-compliance.md" %}}

## 查看发票

您的发票包含以下内容：

- 发票编号
- 签发日期
- 到期日
- 您的“账单接收方”信息
- 应付金额（美元）
- 在线支付：选择此链接在线支付发票
- 订单描述、适用时的单位、单价和金额（美元）
- 小计、折扣（如适用）和总计

发票“账单接收方”部分列出的信息基于您的账单信息。并非所有字段都是必填项。账单信息包括：

- 姓名（必填）：管理员或公司的名称
- 地址（必填）
- 电子邮件地址（必填）：接收账户所有与账单相关邮件的电子邮件地址
- 电话号码
- 税号或增值税号

您无法修改已支付或未支付的账单发票。当您更新账单信息时，此更改不会更新现有发票。

如果您需要更新账单信息，请确保在订阅续订日期之前完成，此时您的发票已最终确定。

更多信息，请参阅[更新账单信息](details.md)。

## 支付发票

> [!NOTE]
>
> 仅年度账单周期的订阅者可以使用发票支付。要更改您的账单周期，请参阅[更改账单周期](/manuals/billing/cycle.md)。

如果您已为订阅选择发票支付，您将在到期日前 10 天、到期日当天以及到期日后 15 天收到支付发票的电子邮件提醒。

您可以通过 Docker 账单控制台支付发票：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 选择 **Invoices**（发票）并找到您要支付的发票。
4. 在 **Actions**（操作）列中，选择 **Pay invoice**（支付发票）。
5. 填写您的支付详细信息，然后选择 **Pay**（支付）。

当您的支付处理完毕后，发票的 **Status**（状态）列将更新为 **Paid**（已支付），您将收到一封确认邮件。

如果您选择使用美国银行账户支付，则必须验证该账户。更多信息，请参阅[验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。

### 查看续订日期

{{< tabs >}}
{{< tab name="Docker subscription" >}}

您会在订阅续订时收到发票。要核实您的续订日期，请登录 [Docker Home 账单](https://app.docker.com/billing)。您的续订日期和金额会显示在订阅计划卡片上。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

您会在订阅续订时收到发票。要核实您的续订日期：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的用户头像以打开下拉菜单。
3. 选择 **Billing**（账单）。
4. 选择用户或组织账户以查看账单详细信息。在此处您可以找到您的续订日期和续订金额。

{{< /tab >}}
{{< /tabs >}}

## 在发票上包含您的增值税号

> [!NOTE]
>
> 如果增值税号字段不可用，请填写[联系支持表单](https://hub.docker.com/support/contact/)。此字段可能需要手动添加。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要添加或更新您的增值税号：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Billing information**（账单信息）。
4. 在您的账单信息卡片上选择 **Change**（更改）。
5. 确保选中 **I'm purchasing as a business**（我是以企业身份购买）复选框。
6. 在税号部分输入您的增值税号。

    > [!IMPORTANT]
    >
    > 您的增值税号必须包含国家/地区前缀。例如，如果您要输入德国的增值税号，则应输入 `DE123456789`。

7. 选择 **Update**（更新）。

您的增值税号将包含在您的下一张发票上。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要添加或更新您的增值税号：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Billing address**（账单地址）链接。
4. 在 **Billing Information**（账单信息）部分，选择 **Update information**（更新信息）。
5. 在税号部分输入您的增值税号。

    > [!IMPORTANT]
    >
    > 您的增值税号必须包含国家/地区前缀。例如，如果您要输入德国的增值税号，则应输入 `DE123456789`。

6. 选择 **Save**（保存）。

您的增值税号将包含在您的下一张发票上。

{{< /tab >}}
{{< /tabs >}}

## 查看账单历史记录

您可以查看个人账户或组织的账单历史记录并下载过去的发票。

### 个人账户

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要查看账单历史记录：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Invoices**（发票）。
4. （可选）选择 **Invoice number**（发票编号）以打开发票详情。
5. （可选）选择 **Download**（下载）按钮以下载发票。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要查看账单历史记录：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Payment methods and billing history**（支付方式和账单历史记录）链接。

您可以在 **Invoice History**（发票历史记录）部分找到过去的发票，并可以下载发票。

{{< /tab >}}
{{< /tabs >}}

### 组织

您必须是组织的所有者才能查看账单历史记录。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要查看账单历史记录：

1. 登录 [Docker Home](https://app.docker.com/) 并选择您的组织。
2. 选择 **Billing**（账单）。
3. 从左侧菜单中选择 **Invoices**（发票）。
4. （可选）选择 **invoice number**（发票编号）以打开发票详情。
5. （可选）选择 **download**（下载）按钮以下载发票。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要查看账单历史记录：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择您的组织，然后选择 **Billing**（账单）。
3. 选择 **Payment methods and billing history**（支付方式和账单历史记录）链接。

您可以在 **Invoice History**（发票历史记录）部分找到过去的发票，并可以下载发票。

{{< /tab >}}
{{< /tabs >}}