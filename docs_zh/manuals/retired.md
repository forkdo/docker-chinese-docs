---
title: 已弃用和停用的 Docker 产品与功能
linkTitle: 已弃用的产品和功能
description: |
  了解已弃用和停用的 Docker 功能、产品和开源项目，包括已迁移工具和归档计划的详细信息。
params:
  sidebar:
    group: Products
aliases:
  - /cloud/
  - /cloud/aci-compose-features/
  - /cloud/aci-container-features/
  - /cloud/aci-integration/
  - /cloud/ecs-architecture/
  - /cloud/ecs-compose-examples/
  - /cloud/ecs-compose-features/
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
  - /desktop/features/dev-environments/create-dev-env/
  - /desktop/features/dev-environments/set-up/
  - /desktop/features/dev-environments/share/
  - /desktop/features/dev-environments/dev-cli/
  - /desktop/dev-environments/
---

本文档概述了已弃用、停用或迁移的 Docker 功能、产品和开源项目。

> [!NOTE]
>
> 本文档不涵盖已弃用和移除的 Docker Engine 功能。
> 有关已弃用的 Docker Engine 功能的详细列表，请参阅
> [Docker Engine 已弃用功能文档](/manuals/engine/deprecated.md)。

## 产品和功能

Docker, Inc. 不再为这些已弃用或停用的功能提供支持。已迁移至第三方的项目继续由其新维护者更新。

### Docker Machine

Docker Machine 是一个用于在各种平台（包括虚拟机和云提供商）上配置和管理 Docker 主机的工具。它已不再维护，用户应直接使用 [Docker Desktop](/manuals/desktop/_index.md) 或 [Docker Engine](/manuals/engine/_index.md) 在支持的平台上运行。Machine 创建和配置主机的方法已被更现代的工作流取代，这些工作流与 Docker Desktop 集成更紧密。

### Docker Toolbox

Docker Toolbox 用于在 Docker Desktop 无法运行的旧系统上。它将 Docker Machine、Docker Engine 和 Docker Compose 打包到一个安装程序中。Toolbox 不再维护，实际上已被当前系统上的 [Docker Desktop](/manuals/desktop/_index.md) 取代。Docker Toolbox 的引用偶尔会出现在旧文档或社区教程中，但不建议用于新安装。

### Docker Cloud 集成

Docker 之前提供了 Amazon Elastic Container Service (ECS) 和 Azure Container Instances (ACI) 的集成，以简化容器工作流。这些集成已被弃用，用户现在应依赖原生云工具或第三方解决方案来管理工作负载。向平台特定或通用编排工具的迁移减少了对专用 Docker Cloud 集成的需求。

您仍可在 [Compose CLI 仓库](https://github.com/docker-archive/compose-cli/tree/main/docs) 中查看这些集成的相关文档。

### Docker Enterprise Edition

Docker Enterprise Edition (EE) 是 Docker 用于部署和管理大规模容器环境的商业平台。它于 2019 年被 Mirantis 收购，需要企业级功能的用户现在可以探索 Mirantis Kubernetes Engine 或 Mirantis 提供的其他产品。Docker EE 中的许多技术和功能已融入 Mirantis 产品线。

> [!NOTE]  
> 有关 Docker 当前提供的企业级功能信息，
> 请参阅 [Docker Business 订阅](/manuals/subscription/details.md#docker-business)。

### Docker Data Center 和 Docker Trusted Registry

Docker Data Center (DDC) 是一个总称，涵盖 Docker Universal Control Plane (UCP) 和 Docker Trusted Registry (DTR)。这些组件为企业环境提供了管理容器、安全和注册表服务的完整解决方案。它们在 Docker Enterprise 被收购后现归 Mirantis 投资组合所有。仍遇到 DDC、UCP 或 DTR 引用的用户应参考 Mirantis 的文档以获取现代等效方案的指导。

### Dev Environments

Dev Environments 是 Docker Desktop 中引入的一个功能，允许开发者快速启动开发环境。它已被弃用，并从 Docker Desktop 4.42 及更高版本中移除。类似的工作流可以通过 Docker Compose 或创建针对特定项目需求的自定义配置来实现。

### GitHub Copilot 扩展

Docker for GitHub Copilot 扩展将 Docker 功能与 GitHub Copilot Chat 集成，通过对话提示帮助开发者容器化应用、生成 Docker 资产并分析漏洞。该扩展早期可在 GitHub Marketplace 上获得。GitHub [弃用 Copilot Extensions](https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/)，导致 Docker for GitHub Copilot 扩展被停用。如果您正在寻找 AI 辅助的 Docker 工作流，请探索 Docker MCP Toolkit 和 MCP 目录，或在 Docker Desktop 和 Docker CLI 中使用 Ask Gordon。

## 开源项目

多个最初由 Docker 维护的开源项目已被归档、停用或迁移至其他维护者或组织。

### Registry（现为 CNCF Distribution）

Docker Registry 是容器镜像注册表的开源实现。它于 2019 年捐赠给云原生计算基金会 (CNCF)，现以 "Distribution" 的名称维护。它仍然是管理和分发容器镜像的基石。

[CNCF Distribution](https://github.com/distribution/distribution)

### Docker Compose v1（被 Compose v2 取代）

Docker Compose v1 (`docker-compose`) 是一个基于 Python 的定义多容器应用的工具，已被 Compose v2 (`docker compose`) 取代，后者使用 Go 编写并与 Docker CLI 集成。Compose v1 不再维护，用户应迁移到 Compose v2。

[Compose v2 文档](/manuals/compose/_index.md)

### InfraKit

InfraKit 是一个设计用于管理声明式基础设施和自动化容器部署的开源工具包。它已被归档，用户被鼓励探索 Terraform 等工具进行基础设施配置和编排。

[InfraKit GitHub 仓库](https://github.com/docker/infrakit)

### Docker Notary（现为 CNCF Notary）

Docker Notary 是一个用于签名和验证容器内容真实性的系统。它于 2017 年捐赠给 CNCF，现继续以 "Notary" 的名称开发。需要安全内容验证的用户应查阅 CNCF Notary 项目。

[CNCF Notary](https://github.com/notaryproject/notary)

### SwarmKit

SwarmKit 为 Docker Swarm 模式提供支持，通过为容器部署提供编排功能。虽然 Swarm 模式仍可正常工作，但开发速度已放缓，转而支持基于 Kubernetes 的解决方案。评估容器编排选项的个人应调查 SwarmKit 是否满足现代工作负载需求。

[SwarmKit GitHub 仓库](https://github.com/docker/swarmkit)