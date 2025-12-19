---
title: 创建您的组织
weight: 10
description: 了解如何创建组织。
keywords: docker 组织, organization, 创建组织, docker 团队, docker 管理控制台, 组织管理
aliases:
  - /docker-hub/orgs/
---

{{< summary-bar feature_name="Admin orgs" >}}

本页介绍如何创建组织。

## 先决条件

在开始创建组织之前：

- 您需要一个 [Docker ID](/accounts/create-account/)
- 查看 [Docker 订阅和功能](https://www.docker.com/pricing/)，以确定为您的组织选择哪种订阅

## 创建组织

有多种创建组织的方法。您可以：

- 使用管理控制台或 Docker Hub 中的 **创建组织** 选项创建新组织
- 将现有的用户帐户转换为组织

以下部分包含如何创建新组织的说明。有关将现有用户帐户转换为组织的先决条件和详细说明，请参阅[将帐户转换为组织](/manuals/admin/organization/convert-account.md)。

创建组织：

1. 登录 [Docker Home](https://app.docker.com/)，导航到组织列表底部。
2. 选择 **创建新组织**。
3. 为您的组织选择订阅、计费周期，并指定所需的席位数量。有关团队和商业订阅提供的功能的详细信息，请参阅 [Docker 定价](https://www.docker.com/pricing/)。
4. 选择 **继续到个人资料**。
5. 选择 **创建组织** 以创建新组织。
6. 输入**组织命名空间**。这是您在 Docker Hub 中的官方唯一名称。创建组织后无法更改组织名称。

   > [!NOTE]
   >
   > 您不能对组织和您的 Docker ID 使用相同的名称。如果您想将您的 Docker ID 用作组织名称，则必须先[将您的帐户转换为组织](/manuals/admin/organization/convert-account.md)。

7. 输入您的**公司名称**。这是您公司的全称。Docker 会在您的组织页面以及您发布的任何公共镜像的详细信息中显示公司名称。您可以随时导航到组织的**设置**页面来更新公司名称。
8. 选择 **继续到计费** 以继续。
9. 输入您组织的计费信息，然后选择 **继续到付款** 以继续进入计费门户。
10. 提供您的付款详细信息，然后选择**购买**。

您现在已经创建了一个组织。

## 查看组织

要在管理控制台中查看组织：

1. 登录 [Docker Home](https://app.docker.com) 并选择您的组织。
2. 从左侧导航菜单中，选择**管理控制台**。

管理控制台包含许多选项，可让您配置组织。

## 合并组织

> [!WARNING]
>
> 如果您要合并组织，建议在计费周期*结束*时进行。当您合并一个组织并降级另一个组织时，您将在降级的组织中失去席位。Docker 不提供降级退款。

如果您有多个组织想要合并为一个，请完成以下步骤：

1. 根据次要组织的席位数量，为您要保留的主要组织帐户[购买额外席位](../../subscription/manage-seats.md)。
2. 手动将用户添加到主要组织，并从次要组织中删除现有用户。
3. 手动迁移您的数据，包括所有仓库。
4. 完成所有用户和数据的迁移后，将次要帐户[降级](../../subscription/change.md)为免费订阅。请注意，Docker 不提供在计费周期中途降级组织的退款。

> [!TIP]
>
> 如果您的组织拥有带采购订单的 Docker Business 订阅，请联系 Docker 支持或您的客户经理。

## 更多资源

- [视频：Docker Hub 组织](https://www.youtube.com/watch?v=WKlT1O-4Du8)