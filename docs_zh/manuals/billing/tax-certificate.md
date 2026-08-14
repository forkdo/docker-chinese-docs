---
title: 销售税豁免与增值税
linkTitle: 税费
description: >
  了解 Docker 如何征收销售税和增值税、如何提交美国税务豁免证明，以及如何在结账时添加增值税号。
keywords:
  billing, sales tax, VAT, tax exemption certificate, tax ID, VAT number,
  United States tax exemption, Docker Support, billing portal
weight: 70
---

根据您所在的位置，Docker 可能会就您的订阅征收销售税或增值税。两种情况的免税概念相同，但流程不同：

- 美国客户通过 Docker 支持团队提交税务豁免证明来申请豁免。计费门户中没有面向美国客户的自助税务 ID 字段。
- 增值税国家的客户在购买 Docker 套餐时自行填写税务 ID 或增值税号。

## 美国税务豁免

美国客户需提交包含有效税务豁免证明的支持工单以获得免税状态。Docker 会审核该证明并将豁免应用到您的计费资料中。您可以在以下情况下申请免税状态：

- 在购买之前，提交您的证明并等待 Docker 审批。审批通过后，您可以在不缴销售税的情况下购买。
- 如果您已被征收销售税，请提交支持工单与 Docker 支持团队协调免税状态。

### 先决条件

提交证明前，请确认以下事项：

- 客户名称与证明上的名称一致。
- 证明将 Docker, Inc. 列为卖家或供应商，并填写了所有相关字段。
- 证明已签署、注明日期且未过期。
- 您已提供该证明适用的所有账户的 Docker ID 或命名空间。

> [!TIP]
>
> 如果适用，您可以将同一份证明用于多个命名空间。

### 联系信息

在证明上使用以下联系信息：

```text
Docker, Inc.
3790 El Camino Real #1052
Palo Alto, CA 94306
(415) 941-0376
```

### 提交税务豁免证明

1. [提交 Docker 支持工单](https://hub.docker.com/support/contact?topic=Billing&subtopic=Tax%20information) 以启动税务证明文件注册流程。
2. 在支持工单的 **Subject**（主题）中输入 **Tax certificate**。
3. 在 **Details**（详情）字段中，输入 **Submitting a tax certificate**。
4. 按照出现的说明提交税务证明。
5. 填写支持表单上的所有必填字段。
6. 在文件上传部分，通过拖放文件或选择 **Browse files**（浏览文件）来添加税务证明。
7. 选择 **Submit**（提交）。

如果需要额外信息，Docker 支持团队会与您联系。在将免税状态应用到您的账户后，Docker 会发送一封电子邮件确认。

## 添加增值税号或税务 ID

当您在结账时选择适用增值税的国家/地区时，会出现一个税务 ID 字段。增值税国家的客户在结账时填写其税务 ID 或增值税号，无需提交支持工单。

您的增值税号必须包含国家/地区前缀。例如，德国增值税号应输入 `DE123456789`。

> [!NOTE]
>
> 税务 ID 字段仅在您选择 **I'm purchasing as a business**（我是以企业身份购买）时出现在结账页面。在计费设置中编辑现有支付方式或账单明细时不会显示该字段。

在[设置新套餐](/manuals/subscription/manage.md#set-up-a-new-plan)时添加增值税号或税务 ID。
