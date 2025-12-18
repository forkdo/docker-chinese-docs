---
title: 使用策略强制使用 Docker Hardened 镜像
linktitle: 强制使用镜像
description: 了解如何使用 Docker Scout 的 Docker Hardened 镜像策略。
weight: 50
keywords: docker scout policies, enforce image compliance, container security policy, image provenance, vulnerability policy check
---

当您拥有 Docker Hardened Images Enterprise 订阅时，镜像 Docker Hardened Image (DHI) 仓库会自动启用 [Docker Scout](/scout/)，使您无需额外配置即可开始对镜像强制执行安全和合规策略。使用 Docker Scout 策略，您可以定义和应用规则，确保跨环境仅使用经过批准且安全的镜像，例如基于 DHI 的镜像。

Docker Scout 包含专门的 [**有效的 Docker Hardened Image (DHI) 或 DHI 基础镜像**](../../scout/policy/_index.md#valid-docker-hardened-image-dhi-or-dhi-base-image) 策略类型，用于验证您的镜像是否为 Docker Hardened Images，或是否使用 DHI 作为基础镜像构建。此策略会检查有效的 Docker 签名验证摘要证明。

通过 Docker Scout 内置的策略评估功能，您可以实时监控镜像合规性，将检查集成到 CI/CD 工作流中，并保持镜像安全性和来源的一致标准。

## 查看现有策略

要查看应用于镜像 DHI 仓库的当前策略：

1. 转到 [Docker Hub](https://hub.docker.com) 中的镜像 DHI 仓库。
2. 选择 **View on Scout**。

   这将打开 [Docker Scout 仪表板](https://scout.docker.com)，您可以在其中看到当前激活的策略以及您的镜像是否满足策略条件。

Docker Scout 会在推送新镜像时自动评估策略合规性。每个策略都包含合规结果以及受影响镜像和层的链接。

## 评估镜像的 DHI 策略合规性

启用 Docker Scout 后，您可以配置 [**有效的 Docker Hardened Image (DHI) 或 DHI 基础镜像**](../../scout/policy/_index.md#valid-docker-hardened-image-dhi-or-dhi-base-image) 策略。此可选策略通过检查 Docker 签名验证摘要证明，验证您的镜像是否为 DHI 或使用 DHI 作为基础镜像构建。

以下示例展示了如何使用 DHI 基础镜像构建镜像并评估其与 DHI 策略的合规性。

### 示例：构建并评估基于 DHI 的镜像

#### 步骤 1：在 Dockerfile 中使用 DHI 基础镜像

创建一个使用镜像 Docker Hardened Image 仓库作为基础的 Dockerfile。例如：

```dockerfile
# Dockerfile
FROM <your-namespace>/dhi-python:3.13-alpine3.21

ENTRYPOINT ["python", "-c", "print('Hello from a DHI-based image')"]
```

#### 步骤 2：构建并推送镜像

打开终端并导航到包含 Dockerfile 的目录。然后，构建并推送镜像到您的 Docker Hub 仓库：

```console
$ docker build \
  --push \
  -t <your-namespace>/my-dhi-app:v1 .
```

#### 步骤 3：启用 Docker Scout

要在您的组织和仓库中启用 Docker Scout，请在终端中运行以下命令：

```console
$ docker login
$ docker scout enroll <your-namespace>
$ docker scout repo enable --org <your-namespace> <your-namespace>/my-dhi-app
```

#### 步骤 4：配置 DHI 策略

启用 Docker Scout 后，您可以为组织配置 **有效的 Docker Hardened Image (DHI) 或 DHI 基础镜像** 策略：

1. 转到 [Docker Scout 仪表板](https://scout.docker.com)。
2. 选择您的组织并导航到 **Policies**。
3. 启用 **有效的 Docker Hardened Image (DHI) 或 DHI 基础镜像** 策略以应用于您的仓库。

有关配置策略的更多信息，请参阅 [配置策略](../../scout/policy/configure.md)。

#### 步骤 5：查看策略合规性

配置并激活 DHI 策略后，您可以查看合规性结果：

1. 转到 [Docker Scout 仪表板](https://scout.docker.com)。
2. 选择您的组织并导航到 **Images**。
3. 找到您的镜像 `<your-namespace>/my-dhi-app:v1`，并选择 **Compliance** 列中的链接。

这将显示您镜像的策略合规性结果。**有效的 Docker Hardened Image (DHI) 或 DHI 基础镜像** 策略会评估您的镜像是否具有有效的 Docker 签名验证摘要证明，或其基础镜像是否具有此类证明。

现在您可以 [在 CI 中评估策略合规性](/scout/policy/ci/)。