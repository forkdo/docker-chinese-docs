---
title: 将 Docker Hardened Image 策略应用到您的镜像
linktitle: 应用镜像策略
description: 了解如何使用 Docker Scout CLI 让您自己的镜像达到 Docker Hardened Image 的安全和合规标准。
weight: 50
keywords: docker scout policies, image security policy, container compliance, dhi policies, vulnerability policy check
---

Docker 发布了 Docker Hardened Images (DHI) 构建所遵循的一套安全和合规策略，因此您可以让自己的镜像达到相同的标准。您可以使用 [`docker scout policy`](../../scout/policy/local.md) 命令根据这些策略评估镜像。

这些策略编码了以下要求：以非 root 用户运行、不存在可修复的严重和高危漏洞、不包含嵌入的恶意软件或密钥、并提供签名的供应链证明。它们不会验证某个镜像是否是 DHI 或基于 DHI 基础镜像构建；它们检查的是镜像是否达到了 DHI 所遵循的同一标准。

与内置的 Docker Scout 策略不同，DHI 策略并不内嵌在 CLI 中。它们以 Rego 源代码的形式维护在 [`docker-hardened-images/policies`](https://github.com/docker-hardened-images/policies) 仓库中，并作为 OCI 策略包发布在 [`dhi/policies`](https://hub.docker.com/repository/docker/dhi/policies/general)。您在评估时使用 `--policy-bundle` 标志拉取该包，因此您可以在本地、CI 或两者中应用 DHI 标准，而无需将任何数据发送到 Docker Scout 服务。

## DHI 包中的策略

`dhi/policies` 包包含以下策略：

| 策略 | 策略名称 | 检查内容 |
| --- | --- | --- |
| 非 dev 镜像不得使用默认 root 用户 | `dhi-default-non-root-user` | 镜像配置为以非 root 用户运行。 |
| 超过修复 SLA 的可修复漏洞 | `fixable-vulnerabilities` | 超过修复 SLA（严重和高危为 7 天，其他为 30 天）后不再有未处理的可修复 CVE。 |
| 无高知名度漏洞 | `high-profile-vulnerabilities` | 镜像不含一份精选的知名 CVE 列表，可选择包含 CISA KEV 目录。 |
| 无嵌入的恶意软件 | `dhi-no-embedded-malware` | 存在且通过了恶意软件扫描证明。 |
| 无嵌入的密钥 | `dhi-no-embedded-secrets` | 存在且通过了密钥扫描证明。 |
| 无失败测试 | `dhi-no-failing-tests` | 存在且通过了测试证明。 |
| 签名的供应链证明 | `dhi-signed-supply-chain-attestations` | SBOM 和溯源证明已附加并签名。 |
| 非预期的 shell 或包管理器 | `dhi-unintentional-shell-or-package-manager` | 镜像中不存在未声明的 shell 或包管理器。 |
| STIG 扫描 | `dhi-stig-scan-score` | 对于兼容 FIPS 的镜像，STIG 扫描达到要求的分数。 |

**策略名称** 是您在 `--policy-config` 文件中引用以启用、禁用或调整策略的稳定 ID。

有关权威列表以及每个策略的 Rego 源代码，请参阅 [`docker-hardened-images/policies`](https://github.com/docker-hardened-images/policies) 仓库。

## 先决条件

- [Docker Scout CLI 插件](/manuals/scout/install.md)。它随 Docker Desktop 一起提供。
- 具有从 Docker Hub 拉取 `dhi/policies` 包的访问权限。身份验证使用您现有的 Docker 注册表凭据，因此请先登录：

  ```console
  $ docker login
  ```

## 根据 DHI 策略评估镜像

要根据 DHI 策略包评估镜像，请使用 `--policy-bundle` 标志将包引用传递给 `docker scout policy`：

```console
$ docker scout policy <image> --policy-bundle dhi/policies:latest
```

CLI 会拉取包、将镜像索引为 SBOM、用 CVE 和 VEX 数据对其进行丰富，并根据该数据评估包中的每个策略。包按摘要缓存，因此针对同一包重新运行不会重新下载它。

### 示例：构建并评估基于 DHI 的镜像

以下示例从 DHI 基础镜像构建镜像，并根据 DHI 策略包对其进行评估。

#### 步骤 1：在 Dockerfile 中使用 DHI 基础镜像

创建一个 Dockerfile，使用 DHI 目录中的 Docker Hardened Image 作为基础。例如：

```dockerfile
# Dockerfile
FROM dhi.io/python:3.13

ENTRYPOINT ["python", "-c", "print('Hello from a DHI-based image')"]
```

#### 步骤 2：构建镜像

打开终端并导航到包含 Dockerfile 的目录。然后，构建镜像并将其加载到本地镜像存储中：

```console
$ docker build --load -t my-dhi-app:v1 .
```

#### 步骤 3：根据 DHI 策略评估镜像

登录并根据 DHI 策略包评估本地镜像：

```console
$ docker login
$ docker scout policy my-dhi-app:v1 \
  --policy-bundle dhi/policies:latest
```

该命令会打印包中每个策略的合规结果，以及任何违规的详细信息。

## 自定义 DHI 策略

您可以使用 `--policy-config` 文件调整运行哪些策略及其阈值。[`docker-hardened-images/policies`](https://github.com/docker-hardened-images/policies) 仓库包含一个示例 `config.json`，您可以以此为基础开始。

```console
$ docker scout policy my-dhi-app:v1 \
  --policy-bundle dhi/policies:latest \
  --policy-config ./config.json
```

配置文件按[DHI 包中的策略](#policies-in-the-dhi-bundle)中列出的**策略名称**匹配策略，并允许您禁用单个策略或调整其设置。例如，以下配置禁用了 STIG 扫描策略，并选择退出高知名度漏洞策略中的 CISA KEV 检查：

```json
{
  "policies": [
    {
      "name": "dhi-stig-scan-score",
      "enabled": false
    },
    {
      "name": "high-profile-vulnerabilities",
      "config": {
        "include_cisa_kev": false
      }
    }
  ]
}
```

有关完整的配置文件格式，请参阅[配置内置策略](../../scout/policy/local.md#configure-built-in-policies)。

您还可以将 DHI 包与内置的 Docker Scout 策略、额外的包或您自己的自定义 Rego 文件组合使用。`--policy-bundle`、`--policy-file` 和 `--policy-dir` 均可重复指定：

```console
$ docker scout policy my-dhi-app:v1 \
  --policy-bundle dhi/policies:latest \
  --policy-file ./custom.rego
```

有关编写自定义策略以及组合策略来源的更多信息，请参阅[评估策略](../../scout/policy/local.md)。

## 在 CI 中强制执行策略合规

使用 [Docker Scout GitHub Action](https://github.com/docker/scout-action) 在每次推送时评估 DHI 策略，并在镜像不满足要求时使工作流失败。以下工作流构建镜像，然后根据 DHI 策略包对其进行评估：

```yaml
name: DHI policy check

on:
  push:

env:
  IMAGE_NAME: my-dhi-app:${{ github.sha }}

jobs:
  policy:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      - name: Build the image
        uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: ${{ env.IMAGE_NAME }}

      - name: Evaluate DHI policies
        uses: docker/scout-action@v1.23.1
        with:
          command: policy
          image: ${{ env.IMAGE_NAME }}
          policy-bundle: dhi/policies:latest
          exit-code: true
```

`docker/login-action` 步骤使用 Docker Hub 进行身份验证，以便运行器可以拉取 DHI 基础镜像和 `dhi/policies` 包。将您的 Docker Hub 用户名和[个人访问令牌](/manuals/security/access-tokens.md)存储为 `DOCKER_USER` 和 `DOCKER_PAT` 仓库密钥。

设置 `exit-code: true` 以便在任何策略未满足时使该步骤失败。`policy-bundle` 输入接受逗号分隔的包列表，并且您可以将其与 `policy-file`、`policy-dir` 和 `policy-config` 输入组合使用，与 CLI 标志相同。

有关在 CI 中运行策略评估的更多信息，请参阅[评估策略](../../scout/policy/local.md#use-in-ci)。
