# 为公司的成功设置 Docker



Docker 的工具提供了一个可扩展、安全的平台，让您的开发人员能够更快地创建、交付和运行应用程序。作为管理员，您可以精简工作流、标准化开发环境，并确保跨组织顺畅部署。

通过配置 Docker 产品以满足贵公司的需求，您可以优化性能、简化用户管理，并保持对资源的控制。本指南帮助您设置和配置 Docker 产品，在满足合规与安全策略的同时，最大化团队的生产力和成功。

## 这是为谁准备的？

- 负责管理其组织内 Docker 环境的管理员
- 希望精简开发和部署工作流的 IT 负责人
- 旨在跨多个用户标准化应用程序环境的团队
- 寻求优化 Docker 产品使用以获得更高可扩展性和效率的组织
- 拥有 [Docker Business 订阅](https://www.docker.com/pricing?ref=DocsGuides&refAction=DocsGuidesCTAClicked) 的组织

## 您将学到什么

- 为什么登录贵公司的 Docker 组织可以提供对使用数据的访问以及增强的功能
- 如何标准化 Docker Desktop 版本和设置，为所有用户创建一致的基线，同时为高级开发人员保留灵活性
- 实施 Docker 安全配置以满足公司 IT 和软件开发安全要求的策略，同时不妨碍开发人员的生产力

## 涵盖的功能

本指南涵盖以下 Docker 功能：

- [组织](/manuals/admin/organization/_index.md)：管理 Docker 环境的核心结构，对用户、团队和镜像仓库进行分组。您的组织是随订阅创建的，并由一个或多个所有者管理。登录到组织的用户会根据所购买的订阅分配席位。
- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)：默认情况下，Docker Desktop 不要求登录。您可以配置设置来强制此要求，并确保您的开发人员登录到您的 Docker 组织。
- [SSO](/manuals/enterprise/security/single-sign-on/_index.md)：如果没有 SSO，Docker 组织中的用户管理是手动的。在您的身份提供商和 Docker 之间建立 SSO 连接可确保符合您的安全策略并自动化用户配置。添加 SCIM 可以进一步自动化用户的配置和取消配置。
- 常规和安全设置：配置关键设置可确保在您的环境中顺利接入和使用 Docker 产品。您还可以根据公司的具体安全需求启用安全功能。

## 需要谁参与

- Docker 组织所有者：必须参与该过程，并且多个关键步骤都需要其在场
- DNS 团队：在 SSO 设置期间需要验证公司域名
- MDM 团队：负责将 Docker 特定的配置文件分发到开发人员机器
- 身份提供商团队：负责配置身份提供商并在设置期间建立 SSO 连接
- 开发负责人：具备 Docker 配置知识的开发负责人，帮助建立开发人员设置的基线
- IT 团队：熟悉公司桌面策略的 IT 代表，协助将 Docker 配置与这些策略对齐
- 安全团队：具备公司开发安全策略知识的安全团队成员，帮助配置安全功能
- Docker 测试人员：一小群开发人员，在全面部署之前测试新设置和配置

## 工具集成

本指南涵盖与以下工具的集成：

- Okta
- Entra ID SAML 2.0
- Azure Connect (OIDC)
- Intune 等 MDM 解决方案

## 沟通与信息收集

### 与您的开发人员和 IT 团队沟通

在您的组织内全面推广 Docker Desktop 之前，与关键利益相关者协调以确保平稳过渡。

#### 通知 Docker Desktop 用户

您的公司中可能已经有 Docker Desktop 用户。此接入过程中的某些步骤可能会影响他们与平台的交互方式。

尽早与用户沟通，告知他们：

- 作为订阅接入的一部分，他们将被升级到受支持的 Docker Desktop 版本
- 将对设置进行审查和优化以提高生产力
- 他们需要使用其企业邮箱登录公司的 Docker 组织以访问订阅权益

#### 与您的 MDM 团队合作

设备管理解决方案（如 Intune 和 Jamf）通常用于企业内的软件分发。这些工具通常由专门的 MDM 团队管理。

尽早与该团队合作以：

- 了解他们的要求和部署变更的提前期
- 协调配置文件的分布

本指南中的几个设置步骤需要将 JSON 文件、注册表项或 .plist 文件分发到开发人员机器。使用 MDM 工具部署这些配置文件并确保其完整性。

### 识别 Docker 组织

一些公司可能已经创建了多个 [Docker 组织](/manuals/admin/organization/_index.md)。这些组织可能是为特定目的创建的，或者可能已经不再需要。

如果您怀疑贵公司有多个 Docker 组织：

- 调查您的团队，看他们是否拥有自己的组织
- 联系您的 Docker 支持，以获取用户邮箱与您域名匹配的组织列表

### 收集需求

[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md) 允许您为 Docker Desktop 预设大量配置参数。

与以下利益相关者合作，以建立贵公司的基线配置：

- Docker 组织所有者
- 开发负责人
- 信息安全代表

一起审查以下方面：

- Docker Desktop 用户的安全功能和[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)
- 订阅中包含的其他 Docker 产品

要查看可以预设的参数，请参阅 [配置设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md#step-two-configure-the-settings-you-want-to-lock-in)。

### 可选：与 Docker 实施团队会面

Docker 实施团队可以帮助您设置组织、配置 SSO、强制登录以及配置 Docker Desktop。

要安排会议，请发送电子邮件至 successteam@docker.com。

## 敲定计划并开始设置

### 将最终确定的设置文件发送给 MDM 团队

在与相关团队就上一节中概述的基线和安配置达成共识后，通过 [Docker Home](/manuals/enterprise/security/hardened-desktop/settings-management/configure-admin-console.md) 或 [`admin-settings.json` 文件](/manuals/enterprise/security/hardened-desktop/settings-management/configure-json-file.md) 配置设置管理。

文件准备好后，与您的 MDM 团队合作部署您选择的设置，以及您选择的[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)方法。

> [!IMPORTANT]
>
> 首先使用少量的 Docker Desktop 开发人员进行测试，以验证功能按预期工作，然后再进行更广泛的部署。

### 管理您的组织

如果您有多个组织，请考虑[将它们合并为一个组织](/manuals/admin/organization/setup/orgs.md)，或者创建一个 [Docker 公司](/manuals/admin/company/_index.md) 来管理多个组织。

### 开始设置

#### 设置单点登录和域名验证

单点登录 (SSO) 允许开发人员使用其身份提供商 (IdP) 进行身份验证以访问 Docker。SSO 可用于整个公司及其所有关联组织，或拥有 Docker Business 订阅的单个组织。有关更多信息，请参阅[文档](/manuals/enterprise/security/single-sign-on/_index.md)。

您还可以启用 [SCIM](/manuals/enterprise/security/provisioning/scim/_index.md) 以进一步自动化用户的配置和取消配置。

#### 设置订阅中包含的 Docker 产品权益

[Docker Build Cloud](/manuals/build-cloud/_index.md) 通过提供专用的远程构建器和共享缓存，显著减少本地和 CI 中的构建时间。借助云的支持，可以释放开发人员的时间和本地资源，让您的团队专注于更重要的事情，例如创新。要开始使用，请[设置一个云构建器](https://app.docker.com/build/)。

[Docker Scout](manuals/scout/_index.md) 是一种主动增强软件供应链安全的解决方案。通过分析您的镜像，Docker Scout 编制一个组件清单，也称为软件物料清单 (SBOM)。该 SBOM 会与持续更新的漏洞数据库进行匹配，以 pinpoint 安全弱点。要开始使用，请参阅 [Quickstart](/manuals/scout/quickstart.md)。

[Testcontainers Cloud](https://testcontainers.com/cloud/docs/) 允许开发人员在云中运行容器，无需在本地机器上运行繁重的容器。

[Docker Hardened Images](/manuals/dhi/_index.md) 是由 Docker 维护的最小、安全和生产就绪的容器基础镜像及应用程序镜像。旨在减少漏洞并简化合规，DHI 可轻松集成到您现有的基于 Docker 的工作流中，几乎不需要或完全不需要重新调整工具。

#### 确保您运行受支持的 Docker Desktop 版本

> [!WARNING]
>
> 此步骤可能会影响运行较旧版本 Docker Desktop 的用户的使用体验。

现有用户可能正在运行过时或不受支持的 Docker Desktop 版本。所有用户都应更新到受支持的版本。最新版本发布前 6 个月内发布的 Docker Desktop 版本受支持。

使用 MDM 解决方案来管理用户的 Docker Desktop 版本。用户也可以直接从 Docker 或通过公司软件门户获取 Docker Desktop。

## 测试

### SSO 和 SCIM 测试

使用与已验证域名下的 Docker 账户关联的电子邮件地址登录 Docker Desktop 或 Docker Hub 来测试 SSO 和 SCIM。使用其 Docker 用户名登录的开发人员不受 SSO 和 SCIM 设置的影响。

> [!IMPORTANT]
>
> 某些用户可能需要通过 CLI 登录 Docker Hub，为此他们将需要[个人访问令牌 (PAT)](/manuals/security/access-tokens.md)。

### 测试注册表访问管理和镜像访问管理

> [!WARNING]
>
> 在继续之前与您的用户沟通，因为此步骤将影响登录到您 Docker 组织的所有现有用户。

如果您计划使用 [注册表访问管理 (RAM)](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 和/或 [镜像访问管理 (IAM)](/manuals/enterprise/security/hardened-desktop/image-access-management.md)：

1. 确保您的测试开发人员使用其组织凭据登录 Docker Desktop
2. 让他们尝试通过 Docker CLI 拉取未授权的镜像或来自不允许的注册表的镜像
3. 验证他们是否收到一条错误消息，指出该注册表被组织限制

### 向测试组部署设置并强制登录

通过 MDM 为小群测试用户部署 Docker 设置并强制登录。让该组在 Docker Desktop 和 Docker Hub 上测试其使用容器的开发工作流，以确保所有设置以及登录强制功能按预期工作。

### 测试 Docker Build Cloud 功能

让您的某位 Docker Desktop 测试人员[连接到您创建的云构建器并使用它进行构建](/manuals/build-cloud/usage.md)。

### 测试 Testcontainers Cloud

让一位测试开发人员[连接到 Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started) 并在云中运行一个容器，以验证设置是否正常工作。

### 验证 Docker Scout 对仓库的监控

检查 [Docker Scout 仪表板](https://scout.docker.com/) 以确认已为启用了 Docker Scout 的仓库正确接收数据。

### 验证对 Docker Hardened Images 的访问

让一位测试开发人员尝试[拉取 Docker Hardened Image](/manuals/dhi/get-started.md)，以确认团队拥有适当的访问权限，并可将这些镜像集成到其工作流中。

## 部署您的 Docker 设置

> [!WARNING]
>
> 在继续之前与您的用户沟通，并确认您的 IT 和 MDM 团队已准备好处理任何意外问题，因为这些步骤将影响登录到您 Docker 组织的所有现有用户。

### 强制 SSO

强制 SSO 意味着任何拥有与您验证域名匹配的电子邮件地址的 Docker 配置文件的用户，都必须使用您的 SSO 连接登录。确保与您的 SSO 连接关联的身份提供商组涵盖您希望获得 Docker 订阅访问权限的所有开发组。

有关如何强制 SSO 的说明，请参阅 [强制 SSO](/manuals/enterprise/security/single-sign-on/connect.md)。

### 向用户部署配置设置并强制登录

让 MDM 团队为所有用户部署 Docker 的配置文件。

### 后续步骤

恭喜，您已成功完成 Docker 的管理员实施过程。

要继续优化您的 Docker 环境：

- 查看您的[组织使用数据](/manuals/admin/insights.md) 以跟踪采用情况
- 监控 [Docker Scout 发现结果](/manuals/scout/explore/analysis.md) 以获取安全洞察
- 探索[其他安全功能](/manuals/enterprise/security/_index.md) 以增强您的配置

