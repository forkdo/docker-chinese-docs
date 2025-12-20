# 在持续集成中使用 Docker Scout

您可以使用 GitHub action 或 Docker Scout CLI 插件，在持续集成流水线中构建 Docker 镜像时对其进行分析。

可用的集成选项：

- [GitHub Actions](gha.md)
- [GitLab](gitlab.md)
- [Microsoft Azure DevOps Pipelines](azure.md)
- [Circle CI](circle-ci.md)
- [Jenkins](jenkins.md)

您还可以添加运行时集成作为 CI/CD 流水线的一部分，这使您能够在部署时将一个镜像分配给某个环境（例如 `production` 或 `staging`）。有关更多信息，请参阅 [环境监控](../environment/_index.md)。

- [将 Docker Scout 与 Microsoft Azure DevOps Pipelines 集成](/scout/integrations/ci/azure/)

- [将 Docker Scout 与 Circle CI 集成](/scout/integrations/ci/circle-ci/)

- [将 Docker Scout 与 GitHub Actions 集成](/scout/integrations/ci/gha/)

- [将 Docker Scout 与 GitLab CI/CD 集成](/scout/integrations/ci/gitlab/)

- [将 Docker Scout 与 Jenkins 集成](/scout/integrations/ci/jenkins/)

