---
title: 创建组织
linkTitle: 创建
weight: 10
description: 了解如何创建组织。
keywords: docker organizations, organization, create organization, docker teams, organization management
aliases:
  - /docker-hub/orgs/
  - /admin/organization/orgs/
---

{{< summary-bar feature_name="Admin orgs" >}}

创建组织有多种方式。你可以：

- 使用 Docker Home 中的 **Create Organization**（创建组织）选项创建一个新组织
- 将现有的用户账户转换为组织

## 先决条件

- 在创建组织之前，你需要一个 [Docker ID](/manuals/accounts/create-account.md)。
- 有关将现有用户账户转换为组织的先决条件和详细说明，请参阅
  [将账户转换为组织](/manuals/admin/organization/setup/convert-account.md)。

> [!TIP]
> 需要为团队需求选择不同的套餐？查看不同的 [Docker 订阅与功能](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminOrgs)，为你的组织选择合适的订阅。

## 创建组织

1. 登录 [Docker Home](https://app.docker.com/) 并导航到组织列表底部。选择 **Create new organization**（创建新组织）。
1. 为你的组织选择订阅、计费周期，并指定你需要的席位数。有关 Team 和 Business 订阅所提供功能的详情，请参阅 [Docker 定价](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminOrgs)。
1. 选择 **Continue to profile**（继续填写资料），然后选择 **Create an organization**（创建组织）以创建新组织。
1. 输入 **Organization namespace**（组织命名空间）。这是你的组织在 Docker Hub 中的官方唯一名称。
   - 组织创建后，无法更改组织名称。
   - 你的 Docker ID 和组织不能同名。
   - 如果你想使用你的 Docker ID 作为组织名称，则必须先 [将你的账户转换为组织](/manuals/admin/organization/setup/convert-account.md)。
1. 输入你的 **Company name**（公司名称）。这是你公司的完整名称。
   - Docker 会在你的组织页面以及你发布的任何公开镜像的详细信息中显示公司名称。
   - 你随时可以通过导航到组织的 **Settings**（设置）页面来更新公司名称。
1. 选择 **Continue to billing**（继续计费），然后输入组织的账单信息。选择 **Continue to payment**（继续支付）以进入账单门户。
1. 提供你的付款详细信息并选择 **Purchase**（购买）。

你现在已创建了一个组织。

## 查看组织

要查看组织：

1. 登录 [Docker Home](https://app.docker.com) 并选择你的
   组织。

Docker Home 包含许多选项，让你可以配置你的组织。

## 合并组织

> [!WARNING]
>
> 如果你要合并组织，建议在本计费周期 _结束_ 时进行。当你合并一个组织并降级另一个组织时，被降级组织的席位将会丢失。Docker 不对降级提供退款。

如果你有多个想要合并为一个的组织，请完成以下步骤：

1. 根据次要组织的席位数，为你要保留的主要组织账户 [购买额外席位](../manage/manage-seats.md)。
1. 手动将用户添加到主要组织，并从次要组织中移除现有用户。
1. 手动迁移你的所有数据，包括所有仓库。
1. 迁移完所有用户和数据后，将次要账户 [降级](../../../subscription/plans/docker.md#cancel-a-docker-plan) 为免费订阅。请注意，Docker 不对计费周期中途降级组织提供退款。

如果你的组织拥有带采购订单的 Docker Business 订阅，请联系 Docker 的支持团队或你的客户经理。

## 更多资源

- [视频：Docker Hub 组织](https://www.youtube.com/watch?v=WKlT1O-4Du8)
