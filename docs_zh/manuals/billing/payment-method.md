---
title: 添加或更新付款方式
weight: 20
description: 了解如何在 Docker Hub 中添加或更新付款方式
keywords: 付款, 账单, 订阅, 支持的付款方式, 付款失败, 添加信用卡, 银行转账, Stripe Link, 付款失败
aliases:
    - /billing/core-billing/payment-method/
---

本文档介绍如何为你的个人账户或组织添加或更新付款方式。

你可以随时添加付款方式或更新账户现有的付款方式。

> [!IMPORTANT]
>
> 如果你想要移除所有付款方式，你必须先将订阅降级为免费订阅。参见 [降级](../subscription/change.md)。

以下付款方式受支持：

- 卡片
  - Visa
  - MasterCard
  - American Express
  - Discover
  - JCB
  - Diners
  - UnionPay
- 钱包
  - Stripe Link
- 银行账户
  - 使用已
  [验证](manuals/billing/payment-method.md#verify-a-bank-account) 的美国
  银行账户进行自动清算所 (ACH) 转账
- [发票付款](/manuals/billing/history.md)

所有费用均以美元 (USD) 计价。

{{% include "tax-compliance.md" %}}

## 管理付款方式

### 个人账户

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的组织。
1. 选择 **Billing**。
1. 从左侧菜单选择 **Payment methods**。
1. 选择 **Add payment method**。
1. 输入你的新付款信息：
    - 添加卡片：
        - 选择 **Card** 并填写卡片信息表单。
    - 添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入你的
        Link **email address** 和 **phone number**。
        - 如果你尚未使用 Link，你必须填写卡片信息表单以存储 Link 付款的卡片。
    - 添加银行账户：
        - 选择 **US bank account**。
        - 验证你的 **Email** 和 **Full name**。
        - 如果你的银行在列表中，选择你银行的名称。
        - 如果你的银行不在列表中，选择 **Search for your bank**。
        - 要验证你的银行账户，请参见
        [验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。
1. 选择 **Add payment method**。
1. 可选。你可以通过选择 **Set as default** 操作来设置默认付款方式。
1. 可选。你可以通过选择 **Delete** 操作来移除非默认付款方式。

> [!NOTE]
>
> 如果你想将美国银行账户设置为默认付款方式，你必须先
> [验证账户](#verify-a-bank-account)。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择 **Billing**。
1. 选择 **Payment methods** 链接。
1. 选择 **Add payment method**。
1. 输入你的新付款信息：
    - 添加卡片：
        - 选择 **Card** 并填写卡片信息表单。
    - 添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入你的
        Link **email address** 和 **phone number**。
        - 如果你不是现有的 Link 客户，你必须填写卡片信息表单以存储 Link 付款的卡片。
1. 选择 **Add**。
1. 选择 **Actions** 图标，然后选择 **Make default** 以确保你的新付款方式适用于所有购买和订阅。
1. 可选。你可以通过选择 **Actions** 图标，然后选择 **Delete** 来移除非默认付款方式。

{{< /tab >}}
{{< /tabs >}}

### 组织

> [!NOTE]
>
> 你必须是组织所有者才能更改付款信息。

{{< tabs >}}
{{< tab name="Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的组织。
1. 选择 **Billing**。
1. 从左侧菜单选择 **Payment methods**。
1. 选择 **Add payment method**。
1. 输入你的新付款信息：
    - 添加卡片：
        - 选择 **Card** 并填写卡片信息表单。
    - 添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入你的
        Link **email address** 和 **phone number**。
        - 如果你不是现有的 Link 客户，你必须填写卡片信息表单以存储 Link 付款的卡片。
    - 添加银行账户：
        - 选择 **US bank account**。
        - 验证你的 **Email** 和 **Full name**。
        - 如果你的银行在列表中，选择你银行的名称。
        - 如果你的银行不在列表中，选择 **Search for your bank**。
        - 要验证你的银行账户，请参见 [验证银行账户](manuals/billing/payment-method.md#verify-a-bank-account)。
1. 选择 **Add payment method**。
1. 可选。你可以通过选择 **Set as default** 操作来设置默认付款方式。
1. 可选。你可以通过选择 **Delete** 操作来移除非默认付款方式。

> [!NOTE]
>
> 如果你想将美国银行账户设置为默认付款方式，你必须先验证账户。

{{< /tab >}}
{{< tab name="Legacy Docker subscription" >}}

要添加付款方式：

1. 登录 [Docker Hub](https://hub.docker.com)。
1. 选择你的组织，然后选择 **Billing**。
1. 选择 **Payment methods** 链接。
1. 选择 **Add payment method**。
1. 输入你的新付款信息：
    - 添加卡片：
        - 选择 **Card** 并填写卡片信息表单。
    - 添加 Link 付款：
        - 选择 **Secure, 1-click checkout with Link** 并输入你的
        Link **email address** 和 **phone number**。
        - 如果你不是现有的 Link 客户，你必须填写卡片信息表单以存储 Link 付款的卡片。
1. 选择 **Add payment method**。
1. 选择 **Actions** 图标，然后选择 **Make default** 以确保你的新付款方式适用于所有购买和订阅。
1. 可选。你可以通过选择 **Actions** 图标，然后选择 **Delete** 来移除非默认付款方式。

{{< /tab >}}
{{< /tabs >}}

## 启用发票付款

{{< summary-bar feature_name="Pay by invoice" >}}

发票付款适用于年度订阅的 Teams 和 Business 客户，从首次续订开始。当你选择此付款方式时，你将使用付款卡或 ACH 银行转账预先支付你的首次订阅期费用。

在续订时，你将收到一封通过电子邮件发送的发票，而不是自动付款，你必须手动支付。发票付款不适用于订阅升级或更改。

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的组织。
1. 选择 **Billing**。
1. 选择 **Payment methods**，然后选择 **Pay by invoice**。
1. 要启用发票付款，选择切换按钮。
1. 确认你的账单联系人详细信息。如果需要更改，请选择 **Change** 并输入你的新详细信息。

## 验证银行账户

有两种方法可以将银行账户验证为付款方式：

- 即时验证：Docker 支持多家主要银行的即时验证。
- 手动验证：所有其他银行必须手动验证。

{{< tabs >}}
{{< tab name="Instant verification" >}}

### 即时验证

要即时验证你的银行账户，你必须从 Docker 账单流程中登录到你的银行账户：

1. 选择 **US bank account** 作为你的付款方式。
1. 验证你的 **Email** 和 **Full name**。
1. 如果你的银行在列表中，选择你银行的名称或选择 **Search for your bank**。
1. 登录到你的银行并查看条款和条件。此协议允许 Docker 从你连接的银行账户中扣款。
1. 选择 **Agree and continue**。
1. 选择要链接和验证的账户，然后选择 **Connect account**。

当账户验证成功后，你将在弹出的模态框中看到成功消息。

{{< /tab >}}
{{< tab name="Manual verification" >}}

### 手动验证

要手动验证你的银行账户，你必须输入银行对账单中的微存款金额：

1. 选择 **US bank account** 作为你的付款方式。
1. 验证你的 **Email** 和 **First and last name**。
1. 选择 **Enter bank details manually instead**。
1. 输入你的银行详细信息：**Routing number** 和 **Account number**。
1. 选择 **Submit**。
1. 你将收到一封包含如何手动验证说明的电子邮件。

手动验证使用微存款。你将在 1-2 个工作日内在你的银行账户中看到一笔小额存款（例如 $0.01）。打开你的手动验证电子邮件并输入此存款金额以验证你的账户。

{{< /tab >}}
{{< /tabs >}}

## 付款失败

> [!NOTE]
>
> 你不能手动重试失败的付款。Docker 将根据重试时间表重试失败的付款。

如果你的订阅付款失败，将有 15 天的宽限期，包括到期日。Docker 会尝试 3 次收集付款，时间安排如下：

- 到期日后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

Docker 还会在每次付款失败尝试后发送一封电子邮件通知
`Action Required - Credit Card Payment Failed`，并附上未付款发票。

一旦宽限期结束且发票仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。