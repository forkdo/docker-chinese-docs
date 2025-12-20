# 将 Docker Scout 与其他系统集成

默认情况下，Docker Scout 会与您的 Docker 组织以及您在 Docker Hub 上启用 Docker Scout 的仓库进行集成。您还可以将 Docker Scout 与额外的第三方系统集成，以获取更多洞察，包括关于您正在运行的工作负载的实时信息。

## 集成类别

根据您选择集成 Docker Scout 的位置和方式，您将获得不同的洞察。

### 容器镜像仓库

将 Docker Scout 与第三方容器镜像仓库集成，使 Docker Scout 能够在这些仓库上运行镜像分析，这样即使它们没有托管在 Docker Hub 上，您也可以深入了解这些镜像的构成。

提供以下容器镜像仓库集成：

- [Amazon Elastic Container Registry](./registry/ecr.md)
- [Azure Container Registry](./registry/acr.md)
- [JFrog Artifactory](./registry/artifactory.md)

### 持续集成 (Continuous Integration)

将 Docker Scout 与持续集成 (CI) 系统集成，是在内部开发循环中获取关于您安全状况的即时、自动反馈的绝佳方式。在 CI 中运行的分析还能获得额外上下文的优势，这对于获取更多洞察非常有用。

提供以下 CI 集成：

- [GitHub Actions](./ci/gha.md)
- [GitLab](./ci/gitlab.md)
- [Microsoft Azure DevOps Pipelines](./ci/azure.md)
- [Circle CI](./ci/circle-ci.md)
- [Jenkins](./ci/jenkins.md)

### 环境监控

环境监控指的是将 Docker Scout 与您的部署进行集成。这可以为您提供关于正在运行的容器工作负载的实时信息。

与环境集成可以让您将生产工作负载与镜像仓库中或其他环境中的其他版本进行比较。

提供以下环境监控集成：

- [Sysdig](./environment/sysdig.md)

有关环境集成的更多信息，请参见 [环境](./environment/_index.md)。

### 代码质量

将 Docker Scout 与代码分析工具集成，可以直接在源代码上进行质量检查，帮助您跟踪错误、安全问题、测试覆盖率等。除了镜像分析和环境监控之外，代码质量门禁让您能够使用 Docker Scout 将供应链管理左移。

启用代码质量集成后，Docker Scout 会将代码质量评估作为策略评估结果包含在您已启用集成的仓库中。

提供以下代码质量集成：

- [SonarQube](sonarqube.md)

### 源代码管理

将 Docker Scout 与您的版本控制系统集成，以获取关于如何解决 Docker Scout 镜像分析检测到的问题的指导性补救建议，直接在您的仓库中进行。

提供以下源代码管理集成：

- [GitHub](source-code-management/github.md) 

<span
  class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white"
  >Beta
</span>



### 团队协作

此类别中的集成允许您将 Docker Scout 与协作平台集成，以便将关于您的软件供应链的通知实时广播到团队沟通平台。

提供以下团队协作集成：

- [Slack](./team-collaboration/slack.md)

- [](https://docs.docker.com/scout/integrations/team-collaboration/)

- [将 Docker Scout 与环境集成](https://docs.docker.com/scout/integrations/environment/)

- [在持续集成中使用 Docker Scout](https://docs.docker.com/scout/integrations/ci/)

