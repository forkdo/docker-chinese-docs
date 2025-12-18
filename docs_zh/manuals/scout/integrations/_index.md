---
description: 如何将 Docker Scout 与其他系统集成。
keywords: 供应链、安全、集成、注册表、CI、环境
title: 将 Docker Scout 与其他系统集成
linkTitle: 集成
weight: 80
---

默认情况下，Docker Scout 会与您的 Docker 组织以及 Docker Hub 上启用了 Docker Scout 的仓库集成。您还可以将 Docker Scout 与额外的第三方系统集成，以获取更多洞察信息，包括有关运行中工作负载的实时信息。

## 集成类别

根据您选择集成 Docker Scout 的位置和方式，您将获得不同的洞察信息。

### 容器注册表

将 Docker Scout 与第三方容器注册表集成，可让 Docker Scout 对这些仓库运行镜像分析，即使这些镜像未托管在 Docker Hub 上，您也能了解其组成。

以下容器注册表集成可用：

- [Amazon Elastic Container Registry](./registry/ecr.md)
- [Azure Container Registry](./registry/acr.md)
- [JFrog Artifactory](./registry/artifactory.md)

### 持续集成

将 Docker Scout 与持续集成（CI）系统集成，是获取安全态势即时自动反馈的好方法，这些反馈来自您的内部循环。在 CI 中运行的分析还能获得额外上下文信息，有助于获取更深入的洞察。

以下 CI 集成可用：

- [GitHub Actions](./ci/gha.md)
- [GitLab](./ci/gitlab.md)
- [Microsoft Azure DevOps Pipelines](./ci/azure.md)
- [Circle CI](./ci/circle-ci.md)
- [Jenkins](./ci/jenkins.md)

### 环境监控

环境监控指的是将 Docker Scout 与您的部署集成。这可以实时提供有关运行中容器工作负载的信息。

与环境集成后，您可以将生产工作负载与其他版本（镜像仓库中或其他环境中的版本）进行比较。

以下环境监控集成可用：

- [Sysdig](./environment/sysdig.md)

有关环境集成的更多信息，请参阅 [环境](./environment/_index.md)。

### 代码质量

将 Docker Scout 与代码分析工具集成，可直接在源代码上执行质量检查，帮助您跟踪错误、安全问题、测试覆盖率等。除了镜像分析和环境监控外，代码质量门禁还能让您将供应链管理左移，借助 Docker Scout 实现。

启用代码质量集成后，Docker Scout 会将代码质量评估作为策略评估结果包含在您已启用集成的仓库中。

以下代码质量集成可用：

- [SonarQube](sonarqube.md)

### 源代码管理

将 Docker Scout 与您的版本控制系统集成，可直接在仓库中获得关于如何解决 Docker Scout 镜像分析检测到的问题的指导性修复建议。

以下源代码管理集成可用：

- [GitHub](source-code-management/github.md) {{< badge color=blue text=Beta >}}

### 团队协作

此类别中的集成允许您将 Docker Scout 与协作平台集成，以便将有关软件供应链的通知实时广播到团队通信平台。

以下团队协作集成可用：

- [Slack](./team-collaboration/slack.md)