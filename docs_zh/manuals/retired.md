---
title: 已弃用和停用的 Docker 产品和功能
linkTitle: 已弃用的产品和功能
description: '探索已弃用和停用的 Docker 功能、产品和开源项目，包括已过渡工具和已归档计划的详细信息。

  '
keywords: deprecated, retired, docker products, docker features, legacy
params:
  sidebar:
    group: Application development
aliases:
- /docker-hub/service-accounts/
- /cloud/
- /cloud/aci-container-features/
- /cloud/aci-integration/
- /cloud/ecs-architecture/
- /cloud/ecs-integration/
- /engine/context/aci-integration/
- /engine/context/ecs-integration/
- /machine/
- /machine/drivers/hyper-v/
- /machine/get-started/
- /machine/install-machine/
- /machine/overview/
- /registry/
- /registry/compatibility/
- /registry/configuration/
- /registry/deploying/
- /registry/deprecated/
- /registry/garbage-collection/
- /registry/help/
- /registry/insecure/
- /registry/introduction/
- /registry/notifications/
- /registry/recipes/
- /registry/recipes/apache/
- /registry/recipes/nginx/
- /registry/recipes/osx-setup-guide/
- /registry/spec/
- /registry/spec/api/
- /registry/spec/auth/
- /registry/spec/auth/jwt/
- /registry/spec/auth/oauth/
- /registry/spec/auth/scope/
- /registry/spec/auth/token/
- /registry/spec/deprecated-schema-v1/
- /registry/spec/implementations/
- /registry/spec/json/
- /registry/spec/manifest-v2-1/
- /registry/spec/manifest-v2-2/
- /registry/spec/menu/
- /registry/storage-drivers/
- /registry/storage-drivers/azure/
- /registry/storage-drivers/filesystem/
- /registry/storage-drivers/gcs/
- /registry/storage-drivers/inmemory/
- /registry/storage-drivers/oss/
- /registry/storage-drivers/s3/
- /registry/storage-drivers/swift/
- /toolbox/
- /toolbox/overview/
- /toolbox/toolbox_install_mac/
- /toolbox/toolbox_install_windows/
- /desktop/features/dev-environments/
- /compose/migrate/
- /scout/policy/scores/
- /scout/integrations/environment/sysdig/
---

本文档概述了已弃用、停用或已过渡的 Docker 功能、产品和开源项目。

> [!NOTE]
>
> 此页面不涵盖已弃用和移除的 Docker Engine 功能。
> 有关已弃用的 Docker Engine 功能的详细列表，请参阅
> [Docker Engine 已弃用功能文档](/manuals/engine/deprecated.md)。

## 产品和功能

Docker, Inc. 不再为这些已弃用或停用的功能提供支持。已过渡给第三方的项目将继续由其新的维护者提供更新。

### Docker Machine

Docker Machine 是一个用于在各种平台（包括虚拟机和云提供商）上配置和管理 Docker 主机的工具。它已不再维护，鼓励用户在支持的平台上直接使用 [Docker Desktop](/manuals/desktop/_index.md) 或 [Docker Engine](/manuals/engine/_index.md)。Machine 创建和配置主机的方法已被更现代化的工作流程所取代，这些工作流程与 Docker Desktop 集成得更紧密。

### Docker Toolbox

Docker Toolbox 用于无法运行 Docker Desktop 的旧系统。它将 Docker Machine、Docker Engine 和 Docker Compose 打包到一个安装程序中。Toolbox 已不再维护，并实际上已被当前系统上的 [Docker Desktop](/manuals/desktop/_index.md) 取代。Docker Toolbox 的引用偶尔会出现在旧文档或社区教程中，但不建议用于新安装。

### Docker Cloud 集成

Docker 以前提供与 Amazon Elastic Container Service (ECS) 和 Azure Container Instances (ACI) 的集成，以简化容器工作流程。这些集成已被弃用，用户现在应依靠原生云工具或第三方解决方案来管理工作负载。向特定平台或通用编排工具的转变减少了对专用 Docker Cloud 集成的需求。

您仍然可以在 [Compose CLI 仓库](https://github.com/docker-archive/compose-cli/tree/main/docs) 中查看这些集成的相关文档。

### Docker Enterprise Edition

Docker Enterprise Edition (EE) 是 Docker 用于部署和管理大规模容器环境的商业平台。它于 2019 年被 Mirantis 收购，寻求企业级功能的用户现在可以探索 Mirantis Kubernetes Engine 或 Mirantis 提供的其他产品。Docker EE 中的许多技术和功能已被吸收到 Mirantis 产品线中。

> [!TIP]
> 有关 Docker 当今提供的企业级功能的信息，请参阅 [Docker Business 订阅](https://www.docker.com/pricing?ref=Docs&refAction=DocsRetired)。

### Docker Data Center 和 Docker Trusted Registry

Docker Data Center (DDC) 是一个涵盖 Docker Universal Control Plane (UCP) 和 Docker Trusted Registry (DTR) 的总称。这些组件为在企业环境中管理容器、安全性和注册表服务提供了全栈解决方案。在 Docker Enterprise 被收购后，它们现在归 Mirantis 旗下。仍然遇到 DDC、UCP 或 DTR 引用的用户应参考 Mirantis 的文档以获取现代等效产品的指导。

### Dev Environments

Dev Environments 是在 Docker Desktop 中引入的一项功能，允许开发人员快速启动开发环境。它在 Docker Desktop 4.42 及更高版本中被弃用并移除。类似的工作流程可以通过 Docker Compose 或创建针对特定项目需求定制的自定义配置来实现。

### Docker Desktop 沙箱（sandboxes）

Docker Desktop 沙箱让用户可以通过 `docker sandbox` 命令在隔离的微虚拟机 (microVM) 中运行 AI 编码代理（coding agents）。`docker sandbox` 插件已在 Docker Desktop 4.80.0 中移除。请改用独立的 [`sbx` CLI](/manuals/ai/sandboxes/_index.md)。

### Docker Scout 功能

以下 Docker Scout 功能已停用或弃用。有关详细信息，请参阅 [Scout 平台版本说明](/manuals/scout/release-notes/platform.md)。

- **健康评分（Health scores）和 Scout Everywhere**：根据策略合规性对 Docker Hub 镜像按 A 到 F 进行评级，并展示在 Docker Hub 各处。已于 2026 年 7 月 1 日停用。
- **Sysdig 集成**：通过 Sysdig API 检测集群中运行的镜像。已于 2026 年 7 月 1 日停用。
- **GitHub 源代码管理集成**：将镜像链接到其源仓库，并通过 PR 自动更新基础镜像。已于 2026 年 7 月 1 日停用。有关迁移选项，请参阅 [GitHub 集成](/manuals/scout/integrations/source-code-management/github.md)。
- **通知（Notifications）**：在产品内和通过电子邮件向用户提示新披露的 CVE。已弃用，将于 2026 年 9 月 1 日停用。
- **Slack 集成**：向 Slack 频道发送漏洞和策略合规性通知。已弃用，将于 2026 年 7 月 30 日停用。有关详细信息，请参阅 [Slack 集成](/manuals/scout/integrations/team-collaboration/slack.md)。
- **Amazon ECR 集成**：自动分析推送到 ECR 注册表的镜像。已弃用，将于 2026 年 9 月 1 日停用。有关迁移选项，请参阅 [ECR 集成](/manuals/scout/integrations/registry/ecr.md)。
- **Azure Container Registry 集成**：自动分析推送到 ACR 注册表的镜像。已弃用，将于 2026 年 9 月 1 日停用。有关迁移选项，请参阅 [ACR 集成](/manuals/scout/integrations/registry/acr.md)。
- **仪表板中的策略（Policies）页面**：`docker scout policy` CLI 仍可正常工作。已弃用，将于 2026 年 9 月 1 日停用。请参阅 [评估策略](/manuals/scout/policy/local.md)。
- **SonarQube 集成**：将 SonarQube 质量门禁结果作为 Docker Scout 策略展示。已弃用，将于 2026 年 9 月 1 日停用。

### GitHub Copilot 扩展

Docker for GitHub Copilot 扩展将 Docker 功能与 GitHub Copilot Chat 集成，帮助开发者通过对话提示容器化应用程序、生成 Docker 资产和分析漏洞。该扩展在 GitHub Marketplace 上提供早期访问。GitHub [弃用了 Copilot 扩展](https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/)，这导致 Docker for GitHub Copilot 扩展停用。如果您正在寻找 AI 辅助的 Docker 工作流程，可以探索 Docker MCP Toolkit 和 MCP Catalog，或者在 Docker Desktop 和 Docker CLI 中使用 Gordon。

### 增强型服务账户（Enhanced Service Account）附加组件

增强型服务账户附加组件为访问 Docker Hub 的自动化工作流和服务账户提供分层的拉取速率限制。

Docker 建议迁移到[组织访问令牌 (OATs)](/manuals/enterprise/security/access-tokens.md)，它提供对 Docker Hub 安全的、可编程的访问，具有细粒度的仓库权限、令牌过期和更好的安全审计能力。OATs 包含在 Docker Team 和 Business 订阅中，并提供类似的功能，且无需单独购买附加组件。

### Docker Hub 自动构建（Automated Builds）

Docker Hub 自动构建是 Docker Hub 的一项功能，允许从外部仓库中的源代码构建 Docker 镜像，并自动将构建好的镜像推送到您的 Docker 仓库。此功能已被弃用，并将于 2027 年 4 月 1 日移除。

### Docker Content Trust (DCT)

Docker Content Trust (DCT) 以及 `notary.docker.io` 上的 Notary v1 服务正在全面停用。如果您从未设置过 `DOCKER_CONTENT_TRUST=1` 或使用过 `docker trust` 命令，此变更不会影响您。该服务将在 7 月和 8 月的间歇中断（brownout）窗口之后，于 2026 年 12 月 8 日完全关闭。有关时间线、迁移指引以及 Sigstore/Cosign 和 Notation 等现代替代方案，请参阅 [Docker Content Trust 停用与迁移博客文章](https://www.docker.com/blog/docker-content-trust-retirement-and-migration-guidance/)。


## 开源项目

一些最初由 Docker 维护的开源项目已被归档、停止开发或过渡给其他维护者或组织。

### Registry（现为 CNCF Distribution）

Docker Registry 是容器镜像注册表的开源实现。它于 2019 年捐赠给云原生计算基金会 (CNCF)，并以 "Distribution" 的名称进行维护。它仍然是管理和分发容器镜像的基石。

[CNCF Distribution](https://github.com/distribution/distribution)

### Docker Compose v1（由 Compose v2 取代）

Docker Compose v1 (`docker-compose`) 是一个基于 Python 的工具，用于定义多容器应用程序，它已被 Compose v2 (`docker compose`) 取代。Compose v2 用 Go 编写，并与 Docker CLI 集成。Compose v1 不再维护，用户应迁移到 Compose v2。

[Compose v2 文档](/manuals/compose/_index.md)

### Docker SBOM CLI 插件

Docker SBOM CLI 插件提供 `docker sbom` 命令，用于生成和查看容器镜像的软件物料清单 (SBOMs)。该插件已停止维护。请使用 [`docker scout sbom`](/reference/cli/docker/scout/sbom/) 来生成和检查 SBOM。

[查看 Docker SBOM CLI 插件版本说明以获取迁移指引](https://github.com/docker/sbom-cli-plugin/releases/tag/v0.7.0)

### InfraKit

InfraKit 是一个开源工具包，旨在管理声明式基础设施并自动化容器部署。它已被归档，鼓励用户探索诸如 Terraform 之类的工具进行基础设施配置和编排。

[InfraKit GitHub 仓库](https://github.com/docker/infrakit)

### Docker Notary（现为 CNCF Notary）

Docker Notary 是一个用于签署和验证容器内容真实性的系统。它于 2017 年捐赠给 CNCF，并继续作为 "Notary" 进行开发。寻求安全内容验证的用户应查阅 CNCF Notary 项目。

[CNCF Notary](https://github.com/notaryproject/notary)

### SwarmKit

SwarmKit 通过为容器部署提供编排来支持 Docker Swarm 模式。虽然 Swarm 模式仍然可用，但开发已经放缓，更倾向于基于 Kubernetes 的解决方案。评估容器编排选项的个人应调查 SwarmKit 是否满足现代工作负载要求。

[SwarmKit GitHub 仓库](https://github.com/docker/swarmkit)
