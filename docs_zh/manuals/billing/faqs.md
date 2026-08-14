---
title: 计费常见问题
linkTitle: 常见问题
description: 查找关于 Docker 计费、付款失败、税费以及发票付款的常见问题解答
keywords: 计费, 续订, 付款失败, 销售税, 增值税, 学术定价, 发票付款
tags:
- FAQ
weight: 80
---

## 如果我的订阅付款失败会怎样？

如果您的订阅付款失败，将有 15 天的宽限期（包括到期日）。Docker 会按照以下时间表尝试扣款 3 次：

- 到期日后 3 天
- 上一次尝试后 5 天
- 上一次尝试后 7 天

每次付款尝试失败后，Docker 还会发送一封主题为 `Action Required - Credit Card Payment Failed`（需要操作 - 信用卡付款失败）的电子邮件通知，并附上未付发票。

如果宽限期结束后发票仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。

## 我可以手动重试失败的付款吗？

可以。如果您的付款失败，请选择 **Pay now**（立即付款）通过 Stripe 重试付款。

在重试之前，请确认您的默认付款方式是最新的。相关操作说明，请参阅[管理付款方式](/manuals/billing/payment-method.md#manage-payment-method)。

## Docker 会代收销售税和增值税（VAT）吗？

Docker 会从以下客户处代收销售税或增值税：

- 对于美国客户，Docker 自 2024 年 7 月 1 日起开始代收销售税。
- 对于欧洲客户，Docker 自 2025 年 3 月 1 日起开始代收增值税。
- 对于英国客户，Docker 自 2025 年 5 月 1 日起开始代收增值税。

为确保税务评估准确，请保持您的[账单信息](/manuals/billing/details.md)为最新状态。关于添加增值税号或提交美国税务豁免证明的详细信息，请参阅[税费](/manuals/billing/tax-certificate.md)。

## Docker 是否提供学术定价？

如需了解学术定价，请联系 [Docker 销售团队](https://www.docker.com/company/contact)。

## 我可以使用发票付款来升级或增加席位吗？

不可以。发票付款仅适用于续订年度订阅，不适用于购买升级或增加席位。对于这些变更，您必须使用信用卡付款或美国银行账户付款。
