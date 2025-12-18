---
title: 计费常见问题
linkTitle: 常见问题
description: 关于计费的常见问题
keywords: billing, renewal, payments, faq
tags: [FAQ]
weight: 60
---

### 如果我的订阅付款失败会怎样？

如果您的订阅付款失败，将有 15 天的宽限期（包括到期日）。Docker 会根据以下时间表最多尝试 3 次重新扣款：

- 到期日后 3 天
- 上次尝试后 5 天
- 上次尝试后 7 天

Docker 还会在每次付款失败后发送一封邮件通知 `Action Required - Credit Card Payment Failed`，并附上未支付的账单。

一旦宽限期结束且账单仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。

### 我可以手动重试失败的付款吗？

不可以。Docker 会按照[重试时间表](/manuals/billing/faqs.md#what-happens-if-my-subscription-payment-fails)自动重试失败的付款。

为确保重试付款成功，请确认您的默认付款方式已更新。如果需要更新默认付款方式，请参阅
[管理付款方式](/manuals/billing/payment-method.md#manage-payment-method)。

### Docker 是否收取销售税和/或增值税？

Docker 从以下地区客户收取销售税和/或增值税：

- 对于美国客户，Docker 从 2024 年 7 月 1 日开始收取销售税。
- 对于欧洲客户，Docker 从 2025 年 3 月 1 日开始收取增值税。
- 对于英国客户，Docker 从 2025 年 5 月 1 日开始收取增值税。

为确保税费计算正确，请更新您的账单信息和增值税/税务 ID（如适用）。请参阅
[更新账单信息](/billing/details/)。

如果您符合销售税豁免条件，请参阅
[注册税务证书](/billing/tax-certificate/)。

### Docker 是否提供学术定价？

如需学术定价，请联系
[Docker 销售团队](https://www.docker.com/company/contact)。

### 我可以使用账单付款来升级或购买额外席位吗？

不可以。账单付款仅适用于续订年度订阅，不适用于购买升级或额外席位。对于这些变更，您必须使用信用卡或美国银行账户付款。

有关支持的付款方式列表，请参阅
[添加或更新付款方式](/manuals/billing/payment-method.md)。