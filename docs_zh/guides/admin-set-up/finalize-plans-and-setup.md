---
title: 完成规划并开始设置
description: 与您的 MDM 团队协作分发配置，并设置 SSO 和 Docker 产品试用。
weight: 20
---

## 将最终设置文件发送给 MDM 团队

在与相关团队就上一节中概述的基础配置和安全配置达成一致后，请使用 [Docker Admin Console](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 或 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 配置 Settings Management。

文件准备就绪后，请与您的 MDM 团队协作部署您选择的设置，以及您选择的 [强制登录方法](/manuals/enterprise/security/enforce-sign-in/_index.md)。

> [!IMPORTANT]
>
> 请先在少量 Docker Desktop 开发者中进行测试，以验证功能是否按预期工作，然后再广泛部署。

## 管理您的组织

如果您有多个组织，请考虑将它们 [合并为一个组织](/manuals/admin/organization/orgs.md)，或创建一个 [Docker 公司](/manuals/admin/company/_index.md) 来管理多个组织。

## 开始设置

### 设置单点登录和域名验证

单点登录 (SSO) 允许开发者使用其身份提供商 (IdP) 进行身份验证，以访问 Docker。SSO 可用于整个公司及所有关联组织，或具有 Docker Business 订阅的单个组织。更多信息，请参阅 [文档](/manuals/enterprise/security/single-sign-on/_index.md)。

您还可以启用 [SCIM](/manuals/enterprise/security/provisioning/scim.md) 以进一步自动化用户的配置和取消配置。

### 设置订阅中包含的 Docker 产品授权

[Docker Build Cloud](/manuals/build-cloud/_index.md) 通过提供专用远程构建器和共享缓存，显著减少本地和 CI 中的构建时间。借助云技术，开发者的本地时间和资源得以释放，团队可以专注于更重要的事情，比如创新。要开始使用，请[设置云构建器](https://app.docker.com/build/)。

[Docker Scout](manuals/scout/_index.md) 是一种主动增强软件供应链安全的解决方案。通过分析您的镜像，Docker Scout 会编译组件清单，也称为软件物料清单 (SBOM)。SBOM 会与持续更新的漏洞数据库匹配，以识别安全弱点。要开始使用，请参阅 [快速入门](/manuals/scout/quickstart.md)。

[Testcontainers Cloud](https://testcontainers.com/cloud/docs/) 允许开发者在云端运行容器，无需在本地机器上运行重型容器。

[Docker Hardened Images](/manuals/dhi/_index.md) 是由 Docker 维护的最小化、安全且可直接用于生产的容器基础镜像和应用镜像。DHIs 旨在减少漏洞并简化合规性，可轻松集成到您现有的 Docker 工作流中，几乎无需重新配置。

### 确保您运行的是受支持的 Docker Desktop 版本

> [!WARNING]
>
> 此步骤可能会影响使用旧版 Docker Desktop 用户的体验。

现有用户可能正在运行过时或不受支持的 Docker Desktop 版本。所有用户都应更新到受支持的版本。Docker Desktop 支持发布于最新版本前 6 个月内的版本。

使用 MDM 解决方案来管理用户的 Docker Desktop 版本。用户也可以直接从 Docker 获取 Docker Desktop，或通过公司软件门户获取。