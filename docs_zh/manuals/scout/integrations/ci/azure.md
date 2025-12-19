---
description: 如何将 Docker Scout 与 Microsoft Azure DevOps Pipelines 集成
keywords: 供应链, 安全, ci, 持续集成, azure, devops
title: 将 Docker Scout 与 Microsoft Azure DevOps Pipelines 集成
linkTitle: Azure DevOps Pipelines
---

以下示例在连接到 Azure DevOps 的仓库中运行，该仓库包含 Docker 镜像的定义和内容。当向主分支提交代码时，该流水线会被触发，构建镜像并使用 Docker Scout 创建 CVE 报告。

首先，设置工作流的其余部分，并配置可供所有流水线步骤使用的变量。将以下内容添加到 _azure-pipelines.yml_ 文件中：

```yaml
trigger:
  - main

resources:
  - repo: self

variables:
  tag: "$(Build.BuildId)"
  image: "vonwig/nodejs-service"
```

这将设置工作流，为应用程序使用特定的容器镜像，并使用构建 ID 为每个新的镜像构建打上标签。

将以下内容添加到 YAML 文件中：

```yaml
stages:
  - stage: Build
    displayName: Build image
    jobs:
      - job: Build
        displayName: Build
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: Docker@2
            displayName: Build an image
            inputs:
              command: build
              dockerfile: "$(Build.SourcesDirectory)/Dockerfile"
              repository: $(image)
              tags: |
                $(tag)
          - task: CmdLine@2
            displayName: Find CVEs on image
            inputs:
              script: |
                # Install the Docker Scout CLI
                curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
                # Login to Docker Hub required for Docker Scout CLI
                echo $(DOCKER_HUB_PAT) | docker login -u $(DOCKER_HUB_USER) --password-stdin
                # Get a CVE report for the built image and fail the pipeline when critical or high CVEs are detected
                docker scout cves $(image):$(tag) --exit-code --only-severity critical,high
```

这将创建前面提到的流程。它使用检出的 Dockerfile 构建并标记镜像，下载 Docker Scout CLI，然后针对新标签运行 `cves` 命令以生成 CVE 报告。它仅显示严重或高危漏洞。