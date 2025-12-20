# 最终确定计划并开始设置

## 将最终确定的设置文件发送给 MDM 团队

在与相关团队就上一节中概述的基线和安全配置达成一致后，使用 [Docker 管理控制台](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 或 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 配置设置管理。

文件准备就绪后，与 MDM 团队协作部署您选择的设置，以及您选择的[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)方法。

> [!重要]
>
> 在广泛部署之前，首先与少量 Docker Desktop 开发人员一起测试，以验证功能是否按预期工作。

## 管理您的组织

如果您有多个组织，请考虑[将它们合并为一个组织](/manuals/admin/organization/orgs.md)或创建一个 [Docker 公司](/manuals/admin/company/_index.md) 来管理多个组织。

## 开始设置

### 设置单点登录和域验证

单点登录 (SSO) 允许开发人员使用其身份提供商 (IdP) 进行身份验证以访问 Docker。SSO 可用于整个公司及其所有关联组织，或拥有 Docker Business 订阅的单个组织。有关更多信息，请参阅[文档](/manuals/enterprise/security/single-sign-on/_index.md)。

您还可以启用 [SCIM](/manuals/enterprise/security/provisioning/scim.md)，以进一步自动化用户的配置和取消配置。

### 设置订阅中包含的 Docker 产品权限

[Docker Build Cloud](/manuals/build-cloud/_index.md) 通过提供专用远程构建器和共享缓存，显著减少本地和 CI 中的构建时间。借助云技术，开发人员的时间和本地资源得以释放，使您的团队能够专注于更重要的事情，例如创新。要开始使用，请[设置云构建器](https://app.docker.com/build/)。

[Docker Scout](manuals/scout/_index.md) 是一种主动增强软件供应链安全性的解决方案。通过分析您的镜像，Docker Scout 会编制组件清单（也称为软件物料清单 (SBOM)）。SBOM 会与持续更新的漏洞数据库进行匹配，以查明安全弱点。要开始使用，请参阅[快速入门](/manuals/scout/quickstart.md)。

[Testcontainers Cloud](https://testcontainers.com/cloud/docs/) 允许开发人员在云中运行容器，无需在本地计算机上运行重型容器。

[Docker 加固镜像 (DHIs)](/manuals/dhi/_index.md) 是由 Docker 维护的最小、安全且可用于生产的容器基础镜像和应用程序镜像。DHIs 旨在减少漏洞并简化合规性，可轻松集成到您现有的基于 Docker 的工作流程中，几乎无需重新配置。

### 确保您运行的是受支持的 Docker Desktop 版本

> [!警告]
>
> 此步骤可能会影响使用旧版本 Docker Desktop 的用户的体验。

现有用户可能正在运行过时或不受支持的 Docker Desktop 版本。所有用户都应更新到受支持的版本。Docker Desktop 在过去 6 个月内发布的版本（相对于最新版本）是受支持的。

使用 MDM 解决方案管理用户的 Docker Desktop 版本。用户也可以直接从 Docker 或通过公司软件门户获取 Docker Desktop。
