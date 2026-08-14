# Docker Build GitHub Actions


GitHub Actions 是一个流行的 CI/CD 平台，用于自动化你的构建、测试和部署流水线。Docker 提供了一组
官方 GitHub Actions 供你在工作流中使用。这些官方 action 是用于构建、注解和推送镜像的可复用、
易用的组件。

目前提供以下 GitHub Actions：

- [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images)：
  使用 BuildKit 构建并推送 Docker 镜像。
- [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake)：
  支持使用 [Bake](../../bake/_index.md) 进行高层构建。
- [Docker Login](https://github.com/marketplace/actions/docker-login)：
  登录到 Docker 注册表。
- [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx)：
  创建并启动一个 BuildKit 构建器。
- [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action)：
  从 Git reference 和 GitHub 事件中提取元数据，以生成标签、标注和注解。
- [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose)：
  安装并设置 [Compose](../../../compose)。
- [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker)：
  安装 Docker Engine。
- [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu)：
  为多平台构建安装 [QEMU](https://github.com/qemu/qemu) 静态二进制文件。
- [Docker Scout](https://github.com/docker/scout-action)：
  分析 Docker 镜像以发现安全漏洞。

使用 Docker 的 action 既提供了易用的接口，同时也保留了自定义构建参数的灵活性。

## Examples

如果你正在寻找如何使用 Docker GitHub Actions 的示例，请参阅以下章节：


- [配置你的 GitHub Actions 构建器](/build/ci/github-actions/configure-builder/)

- [Docker GitHub Builder](/build/ci/github-actions/github-builder/)

- [在 GitHub Actions 中构建可复现的镜像](/build/ci/github-actions/reproducible-builds/)

- [在 GitHub Actions 中使用命名上下文](/build/ci/github-actions/named-contexts/)

- [在 GitHub Actions 的多个作业间共享构建的镜像](/build/ci/github-actions/share-image-jobs/)

- [使用 GitHub Actions 在注册表间复制镜像](/build/ci/github-actions/copy-image-registries/)

- [使用 GitHub Actions 构建多平台镜像](/build/ci/github-actions/multi-platform/)

- [使用 GitHub Actions 导出到 Docker](/build/ci/github-actions/export-docker/)

- [使用 GitHub Actions 推送到多个注册表](/build/ci/github-actions/push-multi-registries/)

- [使用 GitHub Actions 在推送前进行测试](/build/ci/github-actions/test-before-push/)

- [使用 GitHub Actions 更新 Docker Hub 描述](/build/ci/github-actions/update-dockerhub-desc/)

- [配合 GitHub Actions 使用本地注册表](/build/ci/github-actions/local-registry/)

- [在 GitHub Actions 中使用密钥](/build/ci/github-actions/secrets/)

- [GitHub Actions 构建摘要](/build/ci/github-actions/build-summary/)

- [使用 GitHub Actions 验证构建配置](/build/ci/github-actions/checks/)

- [使用 GitHub Actions 管理标签和标记](/build/ci/github-actions/manage-tags-labels/)

- [使用 GitHub Actions 添加镜像注解](/build/ci/github-actions/annotations/)

- [使用 GitHub Actions 管理缓存](/build/ci/github-actions/cache/)

- [使用 GitHub Actions 添加 SBOM 与 provenance 证明](/build/ci/github-actions/attestations/)



## Get started with GitHub Actions

[Introduction to GitHub Actions with Docker](/guides/gha.md) 指南将带你完成为构建 Docker 镜像
以及向 Docker Hub 推送镜像而设置并使用 Docker GitHub Actions 的全过程。

