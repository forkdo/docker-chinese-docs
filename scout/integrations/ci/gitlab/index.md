# 将 Docker Scout 与 GitLab CI/CD 集成

以下示例在 GitLab CI 中运行，该 CI 位于包含 Docker 镜像定义和内容的仓库中。由提交触发，管道会构建镜像。如果提交到默认分支，则使用 Docker Scout 获取 CVE 报告。如果提交到其他分支，则使用 Docker Scout 将新版本与当前发布的版本进行比较。

## 步骤

首先，设置工作流的其余部分。其中有很多内容并非 Docker Scout 特有，但需要创建要比较的镜像。

将以下内容添加到仓库根目录下的 `.gitlab-ci.yml` 文件中。

```yaml
docker-build:
  image: docker:latest
  stage: build
  services:
    - docker:dind
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY

    # Install curl and the Docker Scout CLI
    - |
      apk add --update curl
      curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- 
      apk del curl 
      rm -rf /var/cache/apk/*
    # Login to Docker Hub required for Docker Scout CLI
    - echo "$DOCKER_HUB_PAT" | docker login -u "$DOCKER_HUB_USER" --password-stdin
```

这会设置工作流，以 Docker-in-Docker 模式构建 Docker 镜像，在容器内运行 Docker。

然后下载 `curl` 和 Docker Scout CLI 插件，使用仓库设置中定义的环境变量登录 Docker 注册表。

将以下内容添加到 YAML 文件中：

```yaml
script:
  - |
    if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
      tag=""
      echo "Running on default branch '$CI_DEFAULT_BRANCH': tag = 'latest'"
    else
      tag=":$CI_COMMIT_REF_SLUG"
      echo "Running on branch '$CI_COMMIT_BRANCH': tag = $tag"
    fi
  - docker build --pull -t "$CI_REGISTRY_IMAGE${tag}" .
  - |
    if [[ "$CI_COMMIT_BRANCH" == "$CI_DEFAULT_BRANCH" ]]; then
      # Get a CVE report for the built image and fail the pipeline when critical or high CVEs are detected
      docker scout cves "$CI_REGISTRY_IMAGE${tag}" --exit-code --only-severity critical,high    
    else
      # Compare image from branch with latest image from the default branch and fail if new critical or high CVEs are detected
      docker scout compare "$CI_REGISTRY_IMAGE${tag}" --to "$CI_REGISTRY_IMAGE:latest" --exit-code --only-severity critical,high --ignore-unchanged
    fi

  - docker push "$CI_REGISTRY_IMAGE${tag}"
```

这会创建前面提到的流程。如果提交到默认分支，Docker Scout 会生成 CVE 报告。如果提交到其他分支，Docker Scout 会将新版本与当前发布的版本进行比较。它仅显示严重或高危漏洞，并忽略自上次分析以来未发生变化的漏洞。

将以下内容添加到 YAML 文件中：

```yaml
rules:
  - if: $CI_COMMIT_BRANCH
    exists:
      - Dockerfile
```

这些最后几行确保仅当提交包含 Dockerfile 且提交到 CI 分支时，管道才会运行。

## 视频演练

以下是使用 GitLab 设置工作流过程的视频演练。

<iframe class="border-0 w-full aspect-video mb-8" allow="fullscreen" src="https://www.loom.com/embed/451336c4508c42189532108fc37b2560?sid=f912524b-276d-417d-b44a-c2d39719aa1a"></iframe>
