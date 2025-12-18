---
title: 在 CI 中使用 Docker Build Cloud
linkTitle: 持续集成
weight: 30
description: 使用 Docker Build Cloud 加速你的持续集成流水线
keywords: build, cloud build, ci, gha, gitlab, buildkite, jenkins, circle ci
aliases:
  - /build/cloud/ci/
---

在 CI 中使用 Docker Build Cloud 可以加速你的构建流水线，减少等待和上下文切换的时间。你像往常一样控制 CI 工作流，将构建执行委托给 Docker Build Cloud。

在 CI 中使用 Docker Build Cloud 构建包含以下步骤：

1. 登录 Docker 账户。
2. 设置 Buildx 并连接到构建器。
3. 运行构建。

在 CI 中使用 Docker Build Cloud 时，建议你直接将结果推送到注册表，而不是先加载镜像再推送。直接推送可以加速构建并避免不必要的文件传输。

如果你只是想构建并丢弃输出，可以将结果导出到构建缓存或不标记镜像进行构建。使用 Docker Build Cloud 时，如果你构建的是标记镜像，Buildx 会自动加载构建结果。详情请参阅 [加载构建结果](./usage/#loading-build-results)。

> [!NOTE]
>
> Docker Build Cloud 上的构建有 90 分钟的超时限制。运行时间超过 90 分钟的构建会被自动取消。

## 为 CI/CD 设置凭据

为了让你的 CI/CD 系统能够使用 Docker Build Cloud 构建和推送镜像，需要同时提供访问令牌和用户名。令牌类型和用户名取决于你的账户类型和权限。

- 如果你是组织管理员或有权限创建 [组织访问令牌 (OAT)](/manuals/enterprise/security/access-tokens.md)，请使用 OAT 并将 `DOCKER_ACCOUNT` 设置为你的 Docker Hub 组织名称。
- 如果你没有权限创建 OAT 或使用个人账户，请使用 [个人访问令牌 (PAT)](/security/access-tokens/) 并将 `DOCKER_ACCOUNT` 设置为你的 Docker Hub 用户名。

### 创建访问令牌

#### 组织账户

如果你是组织管理员：

- 创建一个 [组织访问令牌 (OAT)](/manuals/enterprise/security/access-tokens.md)。令牌必须具有以下权限：
    1. **cloud-connect** 范围
    2. **读取公共仓库** 权限
    3. **仓库访问** 权限，对目标仓库具有 **Image push** 权限：
        - 展开 **Repository** 下拉菜单。
        - 选择 **Add repository** 并选择你的目标仓库。
        - 为目标仓库设置 **Image push** 权限。

如果你不是组织管理员：

- 向组织管理员请求具有上述权限的访问令牌，或使用个人访问令牌。

#### 个人账户

- 创建一个 [个人访问令牌 (PAT)](/security/access-tokens/)，具有以下权限：
   1. **读写** 访问权限。
        - 注意：使用 Docker Build Cloud 构建只需要读取权限，但要将镜像推送到 Docker Hub 仓库，你需要写入权限。

## CI 平台示例

> [!NOTE]
>
> 在你的 CI/CD 配置中，设置以下变量/密钥：
> - `DOCKER_ACCESS_TOKEN` — 你的访问令牌（PAT 或 OAT）。使用密钥存储令牌。
> - `DOCKER_ACCOUNT` — 你的 Docker Hub 组织名称（OAT）或用户名（PAT）
> - `CLOUD_BUILDER_NAME` — 你在 [Docker Build Cloud Dashboard](https://app.docker.com/build/) 中创建的云构建器名称
>
> 这确保你的构建能够正确地向 Docker Build Cloud 进行身份验证。

### GitHub Actions

```yaml
name: ci

on:
  push:
    branches:
      - "main"

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_ACCOUNT }}
          password: ${{ secrets.DOCKER_ACCESS_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
        with:
          driver: cloud
          endpoint: "${{ vars.DOCKER_ACCOUNT }}/${{ vars.CLOUD_BUILDER_NAME }}" # 例如，"acme/default"
      
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: "<IMAGE>" # 例如，"acme/my-image:latest"
          # 对于拉取请求，将结果导出到构建缓存。
          # 否则，推送到注册表。
          outputs: ${{ github.event_name == 'pull_request' && 'type=cacheonly' || 'type=registry' }}
```

上面的示例使用 `docker/build-push-action`，它会自动使用 `setup-buildx-action` 设置的构建器。如果你需要直接使用 `docker build` 命令，有两种选择：

- 使用 `docker buildx build` 代替 `docker build`
- 设置 `BUILDX_BUILDER` 环境变量以使用云构建器：

  ```yaml
  - name: Set up Docker Buildx
    id: builder
    uses: docker/setup-buildx-action@v3
    with:
      driver: cloud
      endpoint: "${{ vars.DOCKER_ACCOUNT }}/${{ vars.CLOUD_BUILDER_NAME }}"

  - name: Build
    run: |
      docker build .
    env:
      BUILDX_BUILDER: ${{ steps.builder.outputs.name }}
  ```

有关 `BUILDX_BUILDER` 环境变量的更多信息，请参阅
[构建变量](/manuals/build/building/variables.md#buildx_builder)。

### GitLab

```yaml
default:
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - docker info
    - echo "$DOCKER_ACCESS_TOKEN" | docker login --username "$DOCKER_ACCOUNT" --password-stdin
    - |
      apk add curl jq
      ARCH=${CI_RUNNER_EXECUTABLE_ARCH#*/}
      BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
      mkdir -vp ~/.docker/cli-plugins/
      curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
      chmod a+x ~/.docker/cli-plugins/docker-buildx
    - docker buildx create --use --driver cloud ${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}

variables:
  IMAGE_NAME: <IMAGE>
  DOCKER_ACCOUNT: <DOCKER_ACCOUNT> # 你的 Docker Hub 组织名称（或使用个人账户时的用户名）
  CLOUD_BUILDER_NAME: <CLOUD_BUILDER_NAME> # 你在 [Docker Build Cloud Dashboard](https://app.docker.com/build/) 中创建的云构建器名称

# 构建多平台镜像并推送到注册表
build_push:
  stage: build
  script:
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}" \
        --push .

# 构建镜像并丢弃结果
build_cache:
  stage: build
  script:
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}" \
        --output type=cacheonly \
        .
```

### Circle CI

```yaml
version: 2.1

jobs:
  # 构建多平台镜像并推送到注册表
  build_push:
    machine:
      image: ubuntu-2204:current
    steps:
      - checkout

      - run: |
          mkdir -vp ~/.docker/cli-plugins/
          ARCH=amd64
          BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          chmod a+x ~/.docker/cli-plugins/docker-buildx

      - run: echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ --password-stdin
      - run: docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

      - run: |
          docker buildx build \
          --platform linux/amd64,linux/arm64 \
          --push \
          --tag "<IMAGE>" .

  # 构建镜像并丢弃结果
  build_cache:
    machine:
      image: ubuntu-2204:current
    steps:
      - checkout

      - run: |
          mkdir -vp ~/.docker/cli-plugins/
          ARCH=amd64
          BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          chmod a+x ~/.docker/cli-plugins/docker-buildx

      - run: echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ --password-stdin
      - run: docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

      - run: |
          docker buildx build \
          --tag temp \
          --output type=cacheonly \
          .
```

### Buildkite

以下示例使用 Docker Build Cloud 设置 Buildkite 流水线。示例假设流水线名称为 `build-push-docker`，并且你使用环境钩子管理 Docker 访问令牌，但你可以根据需要调整。

在 agent 的钩子目录中添加以下 `environment` 钩子：

```bash
#!/bin/bash
set -euo pipefail

if [[ "$BUILDKITE_PIPELINE_NAME" == "build-push-docker" ]]; then
 export DOCKER_ACCESS_TOKEN="<DOCKER_ACCESS_TOKEN>"
fi
```

创建使用 `docker-login` 插件的 `pipeline.yml`：

```yaml
env:
  DOCKER_ACCOUNT: <DOCKER_ACCOUNT> # 你的 Docker Hub 组织名称（或使用个人账户时的用户名）
  CLOUD_BUILDER_NAME: <CLOUD_BUILDER_NAME> # 你在 [Docker Build Cloud Dashboard](https://app.docker.com/build/) 中创建的云构建器名称
  IMAGE_NAME: <IMAGE>

steps:
  - command: ./build.sh
    key: build-push
    plugins:
      - docker-login#v2.1.0:
          username: DOCKER_ACCOUNT
          password-env: DOCKER_ACCESS_TOKEN # 环境钩子中的变量名
```

创建 `build.sh` 脚本：

```bash
DOCKER_DIR=/usr/libexec/docker

# 获取最新 buildx 二进制文件的下载链接。
# 将 $ARCH 设置为 CPU 架构（例如 amd64, arm64）
UNAME_ARCH=`uname -m`
case $UNAME_ARCH in
  aarch64)
    ARCH="arm64";
    ;;
  amd64)
    ARCH="amd64";
    ;;
  *)
    ARCH="amd64";
    ;;
esac
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")

# 下载支持 Build Cloud 的 docker buildx
curl --silent -L --output $DOCKER_DIR/cli-plugins/docker-buildx $BUILDX_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx

# 连接到你的构建器并将其设置为默认构建器
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# 仅缓存镜像构建
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag "$IMAGE_NAME:$BUILDKITE_COMMIT" \
    --output type=cacheonly \
    .

# 构建、标记并推送多架构 docker 镜像
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --push \
    --tag "$IMAGE_NAME:$BUILDKITE_COMMIT" \
    .
```

### Jenkins

```groovy
pipeline {
  agent any

  environment {
    ARCH = 'amd64'
    DOCKER_ACCESS_TOKEN = credentials('docker-access-token')
    DOCKER_ACCOUNT = credentials('docker-account')
    CLOUD_BUILDER_NAME = '<CLOUD_BUILDER_NAME>'
    IMAGE_NAME = '<IMAGE>'
  }

  stages {
    stage('Build') {
      environment {
        BUILDX_URL = sh (returnStdout: true, script: 'curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\\"linux-$ARCH\\"))"').trim()
      }
      steps {
        sh 'mkdir -vp ~/.docker/cli-plugins/'
        sh 'curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL'
        sh 'chmod a+x ~/.docker/cli-plugins/docker-buildx'
        sh 'echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin'
        sh 'docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"'
        // 仅缓存构建
        sh 'docker buildx build --platform linux/amd64,linux/arm64 --tag "$IMAGE_NAME" --output type=cacheonly .'
        // 构建并推送多平台镜像
        sh 'docker buildx build --platform linux/amd64,linux/arm64 --push --tag "$IMAGE_NAME" .'
      }
    }
  }
}
```

### Travis CI

```yaml
language: minimal 
dist: jammy 

services:
  - docker

env:
  global:
    - IMAGE_NAME=<IMAGE> # 例如，"acme/my-image:latest"

before_install: |
  echo "$DOCKER_ACCESS_TOKEN" | docker login --username "$DOCKER_ACCOUNT" --password-stdin

install: |
  set -e 
  BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$TRAVIS_CPU_ARCH\"))")
  mkdir -vp ~/.docker/cli-plugins/
  curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
  chmod a+x ~/.docker/cli-plugins/docker-buildx
  docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

script: |
  docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  --tag "$IMAGE_NAME" .
```

### BitBucket Pipelines 

```yaml
# 前提条件：$DOCKER_ACCOUNT, $CLOUD_BUILDER_NAME, $DOCKER_ACCESS_TOKEN 已设置为部署变量
# 此流水线假设 $BITBUCKET_REPO_SLUG 为镜像名称

image: atlassian/default-image:3

pipelines:
  default:
    - step:
        name: Build multi-platform image
        script:
          - mkdir -vp ~/.docker/cli-plugins/
          - ARCH=amd64
          - BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          - curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          - chmod a+x ~/.docker/cli-plugins/docker-buildx
          - echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin
          - docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"
          - IMAGE_NAME=$BITBUCKET_REPO_SLUG
          - docker buildx build
            --platform linux/amd64,linux/arm64
            --push
            --tag "$IMAGE_NAME" .
        services:
          - docker
```

### Shell 脚本

```bash
#!/bin/bash

# 获取最新 buildx 二进制文件的下载链接。将 $ARCH 设置为 CPU 架构（例如 amd64, arm64）
ARCH=amd64
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")

# 下载支持 Build Cloud 的 docker buildx
mkdir -vp ~/.docker/cli-plugins/
curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx

# 使用访问令牌登录 Docker Hub。参见 https://docs.docker.com/build-cloud/ci/#creating-access-tokens
echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin

# 连接到你的构建器并将其设置为默认构建器
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# 仅缓存镜像构建
docker buildx build \
    --tag temp \
    --output type=cacheonly \
    .

# 构建、标记并推送多架构 docker 镜像
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --push \
    --tag "<IMAGE>" \
    .
```

### Docker Compose

如果你想要在 CI 中使用 `docker compose build` 和 Docker Build Cloud，请使用此实现。

```bash
#!/bin/bash

# 获取最新 buildx 二进制文件的下载链接。将 $ARCH 设置为 CPU 架构（例如 amd64, arm64）
ARCH=amd64
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
COMPOSE_URL=$(curl -sL \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <GITHUB_TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/docker/compose-desktop/releases \
  | jq "[ .[] | select