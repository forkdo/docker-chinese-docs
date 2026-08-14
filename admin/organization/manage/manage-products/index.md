# 管理 Docker 产品的使用与访问




使用本页了解如何控制并监控组织成员的产品访问权限与使用情况。如果你在寻找设置和配置说明，请参阅每个产品手册下的 [后续步骤](#后续步骤)。

## 控制组织的访问权限

组织成员默认可以访问你的组织所订阅的 Docker 产品。以组织所有者身份登录后，你可以使用以下流程控制所有成员的访问权限。

### Docker Desktop 访问

要管理 Docker Desktop 访问：

1. [强制登录](../../../enterprise/security/enforce-sign-in/_index.md)。
1. [手动](./members.md) 管理成员或使用
   [配置](../../../enterprise/security/provisioning/_index.md)。

启用强制登录后，只有作为组织成员的用户才能在登录后使用 Docker Desktop。

### Docker Hub 访问

要管理 Docker Hub 访问：

1. 登录 [Docker Home](https://app.docker.com/) 并选择你的
   组织，然后选择 **Docker Desktop**。
1. 选择 **Registry Access**（仓库访问）以配置
   [仓库访问管理](../../../enterprise/security/hardened-desktop/registry-access-management.md)。
1. 选择 **Image Access**（镜像访问）以控制
   [镜像访问管理](../../../enterprise/security/hardened-desktop/image-access-management.md)。

### Docker Build Cloud 访问

要初次设置并配置 Docker Build Cloud，请登录
[Docker Build Cloud](https://app.docker.com/build) 并按照屏幕上的说明操作。

要管理 Docker Build Cloud 访问：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择
   [Docker Build Cloud](http://app.docker.com/build)。
1. 选择 **Account settings**（账户设置）。
1. 选择 **Lock access to Docker Build Account**（锁定对 Docker Build 账户的访问）。

### Docker Scout 访问

要初次设置并配置 Docker Scout，请登录
[Docker Scout](https://scout.docker.com/) 并按照屏幕上的说明操作。

要管理 Docker Scout 访问：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择
   [Docker Scout](https://scout.docker.com/)。
1. 选择你的组织，然后选择 **Settings**（设置）。
1. 要管理为 Docker Scout 分析启用的仓库，选择
   **Repository settings**（仓库设置）。更多信息，请参阅
   [仓库设置](../../../scout/explore/dashboard.md#repository-settings)。
1. 要管理与 Docker Desktop 一起在本地镜像上使用 Docker Scout 的访问权限，请使用
   [设置管理](../../../enterprise/security/hardened-desktop/settings-management/_index.md)
   并将 `sbomIndexing` 设置为 `false` 以禁用，或设置为 `true` 以启用。

### Testcontainers Cloud 访问

要初次设置并配置 Testcontainers Cloud，请登录
[Testcontainers Cloud](https://app.testcontainers.cloud/) 并按照屏幕上的说明操作。

要管理 Testcontainers Cloud 的访问：

1. 登录 [Testcontainers Cloud](https://app.testcontainers.cloud/)，
   然后选择菜单图标。
1. 选择 **Account**（账户），然后选择 **Settings**（设置）。
1. 选择 **Lock access to Testcontainers Cloud**（锁定对 Testcontainers Cloud 的访问）。

### Docker Offload 访问

> [!NOTE]
>
> Docker Offload 不包含在核心 Docker 订阅套餐中。要使 Docker Offload 可用，你必须
> [联系销售](https://www.docker.com/products/docker-offload/) 并订阅。

要使用 [设置管理](../../../enterprise/security/hardened-desktop/settings-management/_index.md) 管理组织的 Docker Offload 访问：

1. 登录 [Docker Home](https://app.docker.com/)，然后选择 **Docker
   Desktop**。
1. 选择 **Settings Management**（设置管理）。
1. 配置 **Enable Docker Offload**（启用 Docker Offload）设置，以控制 Docker Desktop 中是否提供 Docker Offload 功能。你可以将此设置配置为五种状态：
   - **始终启用**：Docker Offload 始终启用，用户无法禁用。Offload 开关始终在 Docker Desktop 标题栏中可见。推荐用于无法进行本地 Docker 执行的 VDI 环境。
   - **已启用**：Docker Offload 默认启用，但用户可以在 Docker Desktop 设置中禁用。适用于混合环境。
   - **已禁用**：Docker Offload 默认禁用，但用户可以在 Docker Desktop 设置中启用。
   - **始终禁用**：Docker Offload 已禁用，用户无法启用。该选项可见但被锁定。当组织不批准使用 Docker Offload 时使用。
   - **用户定义**：无强制默认值。用户在各自的 Docker Desktop 设置中选择启用或禁用 Docker Offload。
1. 选择 **Save**（保存）。

有关设置管理的更多详情，请参阅 [设置参考](../../../enterprise/security/hardened-desktop/settings-management/settings-reference.md#enable-docker-offload)。

## 监控组织的产品使用情况

你可以监控整个组织 Docker 产品的使用情况。使用下表了解可以在何处监控组织使用情况：

| 产品 | 监控使用情况 |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Docker Desktop | 从 [Docker Home](https://app.docker.com/)，查看 [**Insights**](../../insights.md) 页面。 |
| Docker Hub | 从 Docker Hub，查看 [**Usage**](https://hub.docker.com/usage) 页面。 |
| Docker Build Cloud | 从 [Docker Build Cloud](http://app.docker.com/build)，查看 **Build minutes** 页面。 |
| Docker Scout | 从 [Docker Home](https://app.docker.com/)，选择 **Go to Scout** 查看 [**Repository settings**](https://scout.docker.com/settings/repos) 页面。 |
| Testcontainers Cloud | 从 [Docker Home](https://app.docker.com/)，选择 **Go to Testcontainers Cloud**，然后选择菜单图标。转到 [**Billing**](https://app.testcontainers.cloud/dashboard/billing) 页面。 |
| Docker Offload | 从 [Docker Home](https://app.docker.com/)，选择 **Offload**，然后选择 **Offload activity**。更多详情请参阅 [Docker Offload 使用与计费](../../../offload/usage.md)。 |

要了解各 Docker 套餐包含的用量，请参阅
[Docker 订阅与功能](https://www.docker.com/pricing?ref=Docs&refAction=DocsAdminManageProducts)。

## 后续步骤

有关每个产品的更多详细信息，包括如何设置和配置它们，请参阅以下手册：

- [Docker Desktop](../../../desktop/_index.md)
- [Docker Hub](../../../docker-hub/_index.md)
- [Docker Build Cloud](../../../build-cloud/_index.md)
- [Docker Scout](../../../scout/_index.md)
- [Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started)
- [Docker Offload](../../../offload/_index.md)

