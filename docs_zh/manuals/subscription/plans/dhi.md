---
title: DHI 套餐
linkTitle: Docker Hardened Images (DHI)
description:
  为组织账户管理 Docker Hardened Images Select 和 Enterprise 仓库，
  包括购买、添加仓库和停用
keywords: dhi select, dhi enterprise, docker hardened images, hardened images,
  repositories, organization subscription, secure images
weight: 30
aliases:
  - /subscription/products/dhi-select/
  - /subscription/dhi-select/
  - /subscription/plans/dhi-select/
---

[Docker Hardened Images (DHI)](/manuals/dhi/_index.md) 是由 Docker 维护的安全、最小化、生产就绪的容器镜像。

- DHI Community 对每位开发者免费开放。
- DHI Select 是面向需要合规就绪镜像和 SLA 支持补丁的组织的付费套餐。您可以在计费门户中自助办理。
- DHI Enterprise 面向具有高级安全和定制需求的组织。要订阅，请<a href="https://www.docker.com/pricing/contact-sales/" id="dkr_docs_cs_plans_dhi_enterprise" class="link" rel="noopener">联系销售</a>。

完整的套餐对比，请参阅 [Docker 定价页面](https://www.docker.com/pricing/)。

## 用量

DHI Community 让您无需任何费用或额外设置即可从公共注册表访问加固的基础镜像。任何组织都可以直接从 `dhi.io` 拉取加固的基础镜像。

当您从 DHI Community 升级到 DHI Select 时，您会购买一组镜像仓库，这些仓库会被镜像到您组织的命名空间中。权益范围限定在结账时分配给它们的组织账户。然后，所有组织成员都可以从这些镜像仓库中拉取。

DHI Enterprise 在 DHI Select 的基础上进行了无限扩展，提供可选的完整目录访问、Hardened System Packages 仓库以及 Extended Lifecycle Support 附加组件。

有关设置和仓库管理的详细信息，请参阅 [DHI Select 和 Enterprise 入门](/manuals/dhi/how-to/select-enterprise.md)。

## 计费行为

DHI Select 是年度套餐，从套餐开始日期起按仓库计费。在周期中途添加的仓库会按剩余计费周期进行分摊。您可以通过计费门户中的 **Active plans（活动套餐）** 向 DHI Select 套餐添加更多仓库。步骤请参阅 [管理套餐](../manage.md#upgrade-plans)。

## 停用自动续费

如果您想将套餐恢复为 DHI Community，必须停用自动续费。停用自动续费会推迟到当前计费周期结束时生效，在此之前您的仓库访问权限保持有效。要停用自动续费：

1. 登录 [Docker Home](https://app.docker.com/) 并转到 **Billing（计费）**。
1. 在 **Active plans（活动套餐）** 中，选择 **Hardened Images** 旁边的 **Manage（管理）**。
1. 选择 **Disable auto-renewal（停用自动续费）**。

## 移除仓库

您也可以从套餐中移除仓库。移除仓库会推迟到当前计费周期结束时生效。您可以随时移除仓库，但无法在周期中途停止套餐以获得部分退款。仓库访问权限在周期结束前保持有效。

要移除仓库：

1. 登录 [Docker Home](https://app.docker.com/) 并转到 **Billing（计费）**。
1. 在 **Active plans（活动套餐）** 中，选择 **Hardened Images** 旁边的 **Manage（管理）**。
    - 选择 **Remove repositories（移除仓库）** 以调整您的仓库数量。
    - 要在续费后保持当前仓库数量，请选择 **Cancel scheduled change（取消已计划的变更）**。
    - 取消和仓库移除将在当前年度计费周期结束时生效。

如果您订阅了 DHI Enterprise，请联系您的销售代表更改您的 DHI 套餐。
