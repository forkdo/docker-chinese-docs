# 将 Docker Scout 与 Jenkins 集成

您可以将以下 stage 和 steps 定义添加到 `Jenkinsfile` 中，以便在 Jenkins 流水线中运行 Docker Scout。该流水线需要一个包含用于向 Docker Hub 进行身份验证的用户名和密码的 `DOCKER_HUB` 凭据。它还需要为镜像和标签定义一个环境变量。

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

这将安装 Docker Scout，登录 Docker Hub，然后运行 Docker Scout 以生成镜像和标签的 CVE 报告。它仅显示严重或高危漏洞。

> [!NOTE]
>
> 如果您看到与镜像缓存相关的 `permission denied` 错误，请尝试将 [`DOCKER_SCOUT_CACHE_DIR`](/manuals/scout/how-tos/configure-cli.md) 环境变量设置为一个可写目录。或者，也可以使用 `DOCKER_SCOUT_NO_CACHE=true` 完全禁用本地缓存。
