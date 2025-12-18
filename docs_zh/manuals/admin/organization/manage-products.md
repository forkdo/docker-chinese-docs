---
title: 管理 Docker 产品
weight: 45
description: 了解如何为你的组织管理 Docker 产品的访问和使用
keywords: organization, tools, products, product access, organization management
---

{{< summary-bar feature_name="Admin orgs" >}}

在本节中，了解如何为你的组织管理 Docker 产品的访问和使用情况。有关每个产品的详细信息，包括如何设置和配置，请参阅以下手册：

- [Docker Desktop](../../desktop/_index.md)
- [Docker Hub](../../docker-hub/_index.md)
- [Docker Build Cloud](../../build-cloud/_index.md)
- [Docker Scout](../../scout/_index.md)
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started)
- [Docker Offload](../../offload/_index.md)

## 管理组织的产品访问

默认情况下，订阅中包含的 Docker 产品访问权限对所有用户启用。有关订阅中包含的产品概述，请参阅
[Docker 订阅和功能](/manuals/subscription/details.md)。

{{< tabs >}}
{{< tab name="Docker Desktop" >}}

### 管理 Docker Desktop 访问

要管理 Docker Desktop 访问：

1. [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。
1. 手动[管理成员](./members.md)或使用
[配置](/manuals/enterprise/security/provisioning/_index.md)。

启用强制登录后，只有组织成员在登录后才能使用 Docker Desktop。

{{< /tab >}}
{{< tab name="Docker Hub" >}}

### 管理 Docker Hub 访问

要管理 Docker Hub 访问，登录到
[Docker Home](https://app.docker.com/)并配置[注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md)
或[镜像访问管理](/manuals/enterprise/security/hardened-desktop/image-access-management.md)。

{{< /tab >}}
{{< tab name="Docker Build Cloud" >}}

### 管理 Docker Build Cloud 访问

要首次设置和配置 Docker Build Cloud，请登录到
[Docker Build Cloud](https://app.docker.com/build)并按照屏幕上的说明操作。

要管理 Docker Build Cloud 访问：

1. 以组织所有者的身份登录到
[Docker Build Cloud](http://app.docker.com/build)。
1. 选择 **Account settings**。
1. 选择 **Lock access to Docker Build Account**。

{{< /tab >}}
{{< tab name="Docker Scout" >}}

### 管理 Docker Scout 访问

要首次设置和配置 Docker Scout，请登录到
[Docker Scout](https://scout.docker.com/)并按照屏幕上的说明操作。

要管理 Docker Scout 访问：

1. 以组织所有者的身份登录到 [Docker Scout](https://scout.docker.com/)。
1. 选择你的组织，然后选择 **Settings**。
1. 要管理启用 Docker Scout 分析的仓库，选择
**Repository settings**。更多信息请参阅
[仓库设置](../../scout/explore/dashboard.md#repository-settings)。
1. 要管理在 Docker Desktop 上使用本地镜像的 Docker Scout 访问，请使用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)
并将 `sbomIndexing` 设置为 `false` 以禁用，或设置为 `true` 以启用。

{{< /tab >}}
{{< tab name="Testcontainers Cloud" >}}

### 管理 Testcontainers Cloud 访问

要首次设置和配置 Testcontainers Cloud，请登录到
[Testcontainers Cloud](https://app.testcontainers.cloud/)并按照屏幕上的说明操作。

要管理 Testcontainers Cloud 访问：

1. 登录到 [Testcontainers Cloud](https://app.testcontainers.cloud/)并选择 **Account**。
1. 选择 **Settings**，然后选择 **Lock access to Testcontainers Cloud**。

{{< /tab >}}
{{< tab name="Docker Offload" >}}

### 管理 Docker Offload 访问

> [!NOTE]
>
> Docker Offload 不包含在核心 Docker 订阅计划中。要使用 Docker Offload，你必须[注册](https://www.docker.com/products/docker-offload/)并订阅。

要为你的组织管理 Docker Offload 访问，请使用[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)：

1. 以组织所有者的身份登录到 [Docker Home](https://app.docker.com/)。
1. 选择 **Admin Console** > **Desktop Settings Management**。
1. 配置 **Enable Docker Offload** 设置以控制 Docker Desktop 中是否可用 Docker Offload 功能。你可以将此设置配置为五种状态：
   - **Always enabled**：Docker Offload 始终启用，用户无法禁用。Docker Desktop 标题中始终显示 Offload 切换。推荐用于无法进行本地 Docker 执行的 VDI 环境。
   - **Enabled**：Docker Offload 默认启用，但用户可以在 Docker Desktop 设置中禁用它。适用于混合环境。
   - **Disabled**：Docker Offload 默认禁用，但用户可以在 Docker Desktop 设置中启用它。
   - **Always disabled**：Docker Offload 被禁用，用户无法启用它。选项可见但被锁定。当 Docker Offload 未获组织使用批准时使用。
   - **User defined**：无强制默认值。用户在 Docker Desktop 设置中选择是否启用或禁用 Docker Offload。
1. 选择 **Save**。

有关设置管理的更多详细信息，请参阅[设置参考](/manuals/enterprise/security/hardened-desktop/settings-management/settings-reference.md#enable-docker-offload)。

{{< /tab >}}
{{< /tabs >}}

## 监控组织的产品使用情况

要查看 Docker 产品的使用情况：

- Docker Desktop：在 [Docker Home](https://app.docker.com/)中查看 **Insights** 页面。更多详细信息请参阅[Insights](./insights.md)。
- Docker Hub：在 Docker Hub 中查看[**Usage** 页面](https://hub.docker.com/usage)。
- Docker Build Cloud：在 [Docker Build Cloud](http://app.docker.com/build)中查看 **Build minutes** 页面。
- Docker Scout：在 Docker Scout 中查看[**Repository settings** 页面](https://scout.docker.com/settings/repos)。
- Testcontainers Cloud：在 Testcontainers Cloud 中查看[**Billing** 页面](https://app.testcontainers.cloud/dashboard/billing)。
- Docker Offload：在 [Docker Home](https://app.docker.com/)中查看 **Offload** > **Offload overview** 页面。更多详细信息请参阅
  [Docker Offload 使用和计费](/offload/usage/)。

如果你的使用量或席位数超过订阅量，你可以
[扩展订阅](../../subscription/scale.md)以满足需求。