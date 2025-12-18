---
description: 如何在持续集成流水线中设置 Docker Scout
keywords: 扫描, 漏洞, Hub, 供应链, 安全, ci, 持续集成, github actions, gitlab
title: 在持续集成中使用 Docker Scout
linkTitle: 持续集成
aliases:
- /scout/ci/
---

你可以使用 GitHub Action 或 Docker Scout CLI 插件，在构建 Docker 镜像时通过持续集成流水线分析它们。

可用的集成方式：

- [GitHub Actions](gha.md)
- [GitLab](gitlab.md)
- [Microsoft Azure DevOps Pipelines](azure.md)
- [Circle CI](circle-ci.md)
- [Jenkins](jenkins.md)

你也可以在 CI/CD 流水线中添加运行时集成，这样在部署镜像时可以将其分配到某个环境，例如 `production` 或 `staging`。更多信息，请参见 [环境监控](../environment/_index.md)。