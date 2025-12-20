# 使用策略强制执行 Docker Hardened Image 用法

当您拥有 Docker Hardened Images 企业订阅时，镜像 Docker Hardened Image (DHI) 仓库会自动启用 [Docker Scout](/scout/)，无需额外设置即可开始强制执行镜像的安全性和合规性策略。使用 Docker Scout 策略，您可以定义并应用规则，以确保只有经过批准且安全的镜像（例如基于 DHI 的镜像）在您的环境中使用。

Docker Scout 包含一种专门的 [**Valid Docker Hardened Image (DHI) or DHI base image**](../../scout/policy/_index.md#valid-docker-hardened-image-dhi-or-dhi-base-image) 策略类型，用于验证您的镜像是否为 Docker Hardened Images，或者是否使用 DHI 作为基础镜像构建而成。该策略会检查有效的 Docker 签名的验证摘要声明 (verification summary attestations)。

由于 Docker Scout 内置了策略评估功能，您可以实时监控镜像合规性，将检查集成到 CI/CD 工作流中，并为镜像安全性和来源保持一致的标准。

## 查看现有策略

要查看应用于镜像 DHI 仓库的当前策略：

1. 转到 [Docker Hub](https://hub.docker.com) 中的镜像 DHI 仓库。
2. 选择 **View on Scout**。

   这将打开 [Docker Scout 仪表板](https://scout.docker.com)，您可以在其中查看当前活动的策略以及您的镜像是否满足策略标准。

当推送新镜像时，Docker Scout 会自动评估策略合规性。每条策略都包含一个合规结果以及指向受影响镜像和层的链接。

## 评估镜像的 DHI 策略合规性

为仓库启用 Docker Scout 后，您可以配置 [**Valid Docker Hardened Image (DHI) or DHI base image**](../../scout/policy/_index.md#valid-docker-hardened-image-dhi-or-dhi-base-image) 策略。此可选策略通过检查 Docker 签名的验证摘要声明，来验证您的镜像是 DHI 还是使用 DHI 基础镜像构建的。

以下示例展示了如何使用 DHI 基础镜像构建镜像，并评估其与 DHI 策略的合规性。

### 示例：构建并评估基于 DHI 的镜像

#### 步骤 1：在 Dockerfile 中使用 DHI 基础镜像

创建一个 Dockerfile，使用 Docker Hardened Image 镜像仓库作为基础。例如：

```dockerfile
# Dockerfile
FROM <your-namespace>/dhi-python:3.13-alpine3.21

ENTRYPOINT ["python", "-c", "print('Hello from a DHI-based image')"]
```

#### 步骤 2：构建并推送镜像

打开终端并导航到包含 Dockerfile 的目录。然后，构建镜像并将其推送到您的 Docker Hub 仓库：

```console
$ docker build \
  --push \
  -t <your-namespace>/my-dhi-app:v1 .
```

#### 步骤 3：启用 Docker Scout

要为您的组织和仓库启用 Docker Scout，请在终端中运行以下命令：

```console
$ docker login
$ docker scout enroll <your-namespace>
$ docker scout repo enable --org <your-namespace> <your-namespace>/my-dhi-app
```

#### 步骤 4：配置 DHI 策略

启用 Docker Scout 后，您可以为您的组织配置 **Valid Docker Hardened Image (DHI) or DHI base image** 策略：

1. 转到 [Docker Scout 仪表板](https://scout.docker.com)。
2. 选择您的组织并导航至 **Policies**。
3. 配置 **Valid Docker Hardened Image (DHI) or DHI base image** 策略，以便为您的仓库启用它。

有关配置策略的更多信息，请参阅 [配置策略](../../scout/policy/configure.md)。

#### 步骤 5：查看策略合规性

配置并激活 DHI 策略后，您可以查看合规结果：

1. 转到 [Docker Scout 仪表板](https://scout.docker.com)。
2. 选择您的组织并导航至 **Images**。
3. 找到您的镜像 `<your-namespace>/my-dhi-app:v1`，并在 **Compliance** 列中选择链接。

这将显示您镜像的策略合规结果。**Valid Docker Hardened Image (DHI) or DHI base image** 策略会评估您的镜像是否具有有效的 Docker 签名的验证摘要声明，或者其基础镜像是否具有此类声明。

您现在可以在 [CI 中评估策略合规性](/scout/policy/ci/)。
