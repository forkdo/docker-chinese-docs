---
title: 管理 Docker 产品
weight: 45
description: 了解如何为您的组织管理 Docker 产品的访问权限和使用情况
keywords: organization, tools, products, product access, organization management
---

{{< summary-bar feature_name="Admin orgs" >}}

在本节中，您将学习如何为您的组织管理访问权限并查看 Docker 产品的使用情况。有关每个产品的更详细信息，包括如何设置和配置它们，请参阅以下手册：

- [Docker Desktop](../../desktop/_index.md)
- [Docker Hub](../../docker-hub/_index.md)
- [Docker Build Cloud](../../build-cloud/_index.md)
- [Docker Scout](../../scout/_index.md)
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started)
- [Docker Offload](../../offload/_index.md)

## 管理您组织的产品访问权限

您的订阅中包含的 Docker 产品的访问权限默认对所有用户开启。有关您订阅中包含的产品的概述，请参阅 [Docker 订阅和功能](https://www.docker.com/pricing/)。

{{< tabs >}}
{{< tab name="Docker Desktop" >}}

### 管理 Docker Desktop 访问权限

要管理 Docker Desktop 访问权限：

1. [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。
2. 手动管理成员 [手动](./members.md) 或使用 [配置](/manuals/enterprise/security/provisioning/_index.md)。

启用强制登录后，只有您组织的成员才能在登录后使用 Docker Desktop。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

### 管理 Docker Hub 访问权限

要管理 Docker Hub 访问权限，请登录 [Docker Home](https://app.docker.com/) 并配置 [Registry Access Management](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 或 [Image Access Management](/manuals/enterprise/security/hardened-desktop/image-access-management.md)。

{{< /tab >}}
{{< tab name="Docker Build Cloud" >}}

### 管理 Docker Build Cloud 访问权限

要初步设置和配置 Docker Build Cloud，请登录 [Docker Build Cloud](https://app.docker.com/build) 并按照屏幕上的说明进行操作。

要管理 Docker Build Cloud 访问权限：

1. 以组织所有者身份登录 [Docker Build Cloud](http://app.docker.com/build)。
2. 选择 **Account settings**。
3. 选择 **Lock access to Docker Build Account**。

{{< /tab >}}
{{< tab name="Docker Scout" >}}

### 管理 Docker Scout 访问权限

要初步设置和配置 Docker Scout，请登录 [Docker Scout](https://scout.docker.com/) 并按照屏幕上的说明进行操作。

要管理 Docker Scout 访问权限：

1. 以组织所有者身份登录 [Docker Scout](https://scout.docker.com/)。
2. 选择您的组织，然后选择 **Settings**。
3. 要管理为 Docker Scout 分析启用的仓库，请选择 **Repository settings**。有关更多信息，请参阅 [仓库设置](../../scout/explore/dashboard.md#repository-settings)。
4. 要管理对 Docker Scout 的访问以在 Docker Desktop 上用于本地镜像，请使用 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 并将 `sbomIndexing` 设置为 `false` 以禁用，或设置为 `true` 以启用。

{{< /tab >}}
{{< tab name="Testcontainers Cloud" >}}

### 管理 Testcontainers Cloud 访问权限

要初步设置和配置 Testcontainers Cloud，请登录 [Testcontainers Cloud](https://app.testcontainers.cloud/) 并按照屏幕上的说明进行操作。

要管理对 Testcontainers Cloud 的访问权限：

1. 登录 [Testcontainers Cloud](https://app.testcontainers.cloud/) 并选择 **Account**。
2. 选择 **Settings**，然后选择 **Lock access to Testcontainers Cloud**。

{{< /tab >}}
{{< tab name="Docker Offload" >}}

### 管理 Docker Offload 访问权限

> [!NOTE]
>
> Docker Offload 不包含在核心 Docker 订阅计划中。要使 Docker Offload 可用，您必须 [注册](https://www.docker.com/products/docker-offload/) 并订阅。

要管理您组织的 Docker Offload 访问权限，请使用 [Settings Management](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)：

1. 以组织所有者身份登录 [Docker Home](https://app.docker.com/)。
2. 选择 **Admin Console** > **Desktop Settings Management**。
3. 配置 **Enable Docker Offload** 设置以控制 Docker Offload 功能在 Docker Desktop 中是否可用。您可以将此设置配置为五种状态：
   - **Always enabled**：Docker Offload 始终启用，用户无法禁用。Offload 切换开关在 Docker Desktop 标题中始终可见。推荐用于无法在本地执行 Docker 的 VDI 环境。
   - **Enabled**：Docker Offload 默认启用，但用户可以在 Docker Desktop 设置中禁用它。适用于混合环境。
   - **Disabled**：Docker Offload 默认禁用，但用户可以在 Docker Desktop 设置中启用它。
   - **Always disabled**：Docker Offload 被禁用，用户无法启用它。该选项可见但被锁定。当 Docker Offload 未被批准用于组织使用时使用。
   - **User defined**：无强制默认值。用户可以选择在他们的 Docker Desktop 设置中启用或禁用 Docker Offload。
4. 选择 **Save**。

有关 Settings Management 的更多详细信息，请参阅 [设置参考](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md#enable-docker-offload)。

{{< /tab >}}
{{< /tabs >}}

## 监控您组织的产品使用情况

要查看 Docker 产品的使用情况：

- Docker Desktop：在 [Docker Home](https://app.docker.com/) 中查看 **Insights** 页面。有关更多详细信息，请参阅 [Insights](./insights.md)。
- Docker Hub：在 Docker Hub 中查看 [**Usage** 页面](https://hub.docker.com/usage)。
- Docker Build Cloud：在 [Docker Build Cloud](http://app.docker.com/build) 中查看 **Build minutes** 页面。
- Docker Scout：在 Docker Scout 中查看 [**Repository settings** 页面](https://scout.docker.com/settings/repos)。
- Testcontainers Cloud：在 Testcontainers Cloud 中查看 [**Billing** 页面](https://app.testcontainers.cloud/dashboard/billing)。
- Docker Offload：在 [Docker Home](https://app.docker.com/) 中查看 **Offload** > **Offload overview** 页面。有关更多详细信息，请参阅 [Docker Offload 使用和计费](/offload/usage/)。

如果您的使用量或席位数量超过订阅额度，您可以 [扩展您的订阅](../../subscription/scale.md) 以满足您的需求。