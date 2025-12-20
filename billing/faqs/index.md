# 计费常见问题

### 如果我的订阅付款失败会怎样？

如果您的订阅付款失败，将有 15 天的宽限期（包括到期日）。Docker 会按照以下时间表尝试重新扣款 3 次：

- 到期日后 3 天
- 上一次尝试后 5 天
- 上一次尝试后 7 天

每次付款尝试失败后，Docker 还会发送一封主题为 `Action Required - Credit Card Payment Failed`（需要操作 - 信用卡付款失败）的电子邮件通知，并附上未付发票。

一旦宽限期结束且发票仍未支付，订阅将降级为免费订阅，所有付费功能将被禁用。

### 我可以手动重试失败的付款吗？

不可以。Docker 会按照[重试时间表](/manuals/billing/faqs.md#what-happens-if-my-subscription-payment-fails)自动重试失败的付款。

为确保重试付款成功，请确认您的默认付款方式已更新。如果您需要更新默认付款方式，请参阅[管理付款方式](/manuals/billing/payment-method.md#manage-payment-method)。

### Docker 会代收销售税和/或增值税（VAT）吗？

Docker 会从以下情况开始代收销售税和/或增值税：

- 对于美国客户，Docker 自 2024 年 7 月 1 日起开始代收销售税。
- 对于欧洲客户，Docker 自 2025 年 3 月 1 日起开始代收增值税。
- 对于英国客户，Docker 自 2025 年 5 月 1 日起开始代收增值税。

为确保税务评估准确，请确保您的账单信息以及增值税/税务 ID（如适用）已更新。请参阅[更新账单信息](/billing/details/)。

如果您享有销售税豁免，请参阅[注册税务证明](/billing/tax-certificate/)。

### Docker 是否提供学术定价？

如需了解学术定价，请联系 [Docker 销售团队](https://www.docker.com/company/contact)。

### 我可以使用发票付款来升级或增加席位吗？

不可以。发票付款仅适用于续订年度订阅，不适用于购买升级或增加席位。对于这些变更，您必须使用信用卡付款或美国银行账户付款。

有关支持的付款方式列表，请参阅[添加或更新付款方式](/manuals/billing/payment-method.md)。
