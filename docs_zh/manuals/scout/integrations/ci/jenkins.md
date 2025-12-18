---
description: 如何将 Docker Scout 与 Jenkins 集成
keywords: 供应链, 安全, ci, 持续集成, jenkins
title: 将 Docker Scout 与 Jenkins 集成
linkTitle: Jenkins
---

您可以在 `Jenkinsfile` 中添加以下阶段和步骤定义，以在 Jenkins 流水线中运行 Docker Scout。该流水线需要一个名为 `DOCKER_HUB` 的凭据，其中包含用于登录 Docker Hub 的用户名和密码。同时还需要为镜像和标签定义环境变量。

```groovy
pipeline {
    agent {
        // Agent details
    }

    environment {
        DOCKER_HUB = credentials('jenkins-docker-hub-credentials')
        IMAGE_TAG  = 'myorg/scout-demo-service:latest'
    }

    stages {
        stage('Analyze image') {
            steps {
                // Install Docker Scout
                sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /usr/local/bin'

                // Log into Docker Hub
                sh 'echo $DOCKER_HUB_PSW | docker login -u $DOCKER_HUB_USR --password-stdin'

                // Analyze and fail on critical or high vulnerabilities
                sh 'docker-scout cves $IMAGE_TAG --exit-code --only-severity critical,high'
            }
        }
    }
}
```

此配置会安装 Docker Scout，登录到 Docker Hub，然后运行 Docker Scout 为指定镜像和标签生成 CVE 报告。仅显示严重或高危漏洞。

> [!NOTE]
>
> 如果看到与镜像缓存相关的 `permission denied` 错误，请尝试将 [`DOCKER_SCOUT_CACHE_DIR`](/manuals/scout/how-tos/configure-cli.md) 环境变量设置为可写目录。或者，您也可以通过 `DOCKER_SCOUT_NO_CACHE=true` 完全禁用本地缓存。