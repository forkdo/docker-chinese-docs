---
title: 扫描 Docker 安全加固镜像
linktitle: 扫描镜像
description: 了解如何使用 Docker Scout、Grype、Trivy 或 Wiz 扫描 Docker 安全加固镜像中的已知漏洞。
keywords: scan container image, docker scout cves, grype scanner, trivy container scanner, vex attestation
weight: 46
---

Docker 安全加固镜像（Docker Hardened Images，简称 DHI）在设计上默认就是安全的，但与任何容器镜像一样，作为漏洞管理流程的一部分，定期扫描它们非常重要。

## 使用兼容 OpenVEX 的扫描器

为了获得准确的漏洞评估，请使用支持 [VEX](/manuals/dhi/core-concepts/vex.md) 证明的扫描器。以下扫描器可以读取并应用 Docker 安全加固镜像中包含的 VEX 声明：

- [Docker Scout](#docker-scout)：自动应用 VEX 声明，无需配置
- [Trivy](#trivy)：通过 VEX Hub 或本地 VEX 文件支持 VEX
- [Grype](#grype)：通过 `--vex` 标志支持 VEX
- [Wiz](#wiz)：自动应用 VEX 声明，无需配置

有关如何选择合适的扫描器以及了解支持 VEX 的扫描器与不支持 VEX 的扫描器之间的差异，请参阅[扫描器集成](/manuals/dhi/explore/scanner-integrations.md)。

## Docker Scout

Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中。它提供漏洞洞察、CVE 摘要以及指向修复指南的直接链接。

### 使用 Docker Scout 扫描 DHI

要使用 Docker Scout 扫描 Docker 安全加固镜像，请运行以下命令：

```console
$ docker login dhi.io
$ docker scout cves dhi.io/<image>:<tag> --platform <platform>
```

示例输出：

```plaintext
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v VEX statements obtained from attestation
    v No vulnerable package detected
    ...
```

有关更详细的过滤和 JSON 输出，请参阅 [Docker Scout CLI 参考](../../../reference/cli/docker/scout/_index.md)。

### 在 CI/CD 中使用 Docker Scout 自动扫描 DHI

将 Docker Scout 集成到 CI/CD 流水线中，使您能够在构建过程中自动验证从 Docker 安全加固镜像构建的镜像是否仍然没有已知漏洞。这种主动方法可确保在整个开发生命周期中镜像的持续安全完整性。

#### GitHub Actions 工作流示例

以下是一个示例 GitHub Actions 工作流，它构建镜像并使用 Docker Scout 扫描它：

```yaml {collapse="true"}
name: DHI Vulnerability Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ "**" ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build Docker image
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }} .

      - name: Run Docker Scout CVE scan
        uses: docker/scout-action@v1
        with:
          command: cves
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }}
          only-severities: critical,high
          exit-code: true
```

`exit-code: true` 参数确保如果检测到任何严重或高危漏洞，工作流将失败，从而防止部署不安全的镜像。

有关在 CI 中使用 Docker Scout 的更多详细信息，请参阅[将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

## Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，用于根据 NVD 和发行版公告等漏洞数据库检查容器镜像。

### 使用 Grype 扫描 DHI

要使用 Grype 扫描带有 VEX 过滤的 Docker 安全加固镜像，请先导出 VEX 证明，然后使用 `--vex` 标志进行扫描：

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
$ grype dhi.io/<image>:<tag> --vex vex.json
```

`--vex` 标志在扫描期间应用 VEX 声明，过滤掉已知的不可利用 CVE，以获得准确的结果。

有关导出 VEX 证明的更多信息，请参阅[导出 VEX 证明](#export-vex-attestations)。

## Trivy

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他工件的开源漏洞扫描器。它可以检测操作系统包和应用程序依赖项中的漏洞。

### 使用 Trivy 扫描 DHI

安装 Trivy 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker 安全加固镜像：

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln dhi.io/<image>:<tag>
```

要使用 VEX 声明过滤漏洞，Trivy 支持多种方法。Docker 推荐使用 VEX Hub，它提供了一个无缝的工作流，用于自动下载并应用来自配置仓库的 VEX 声明。

#### 使用 VEX Hub（推荐）

配置 Trivy 从 VEX Hub 下载 Docker 安全加固镜像公告仓库。运行以下命令来设置 VEX 仓库：

```console
$ trivy vex repo init
$ cat << REPO > ~/.trivy/vex/repository.yaml
repositories:
  - name: default
    url: https://github.com/aquasecurity/vexhub
    enabled: true
    username: ""
    password: ""
    token: ""
  - name: dhi-vex
    url: https://github.com/docker-hardened-images/advisories
    enabled: true
REPO
$ trivy vex repo list
$ trivy vex repo download
```

设置 VEX Hub 后，您可以使用 VEX 过滤扫描 Docker 安全加固镜像：

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln --vex repo dhi.io/<image>:<tag>
```

例如，扫描 `dhi.io/python:3.13` 镜像：

```console
$ trivy image --scanners vuln --vex repo dhi.io/python:3.13
```

示例输出：

```plaintext
Report Summary

┌─────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┐
│                                   Target                                    │    Type    │ Vulnerabilities │
├─────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┤
│ dhi.io/python:3.13 (debian 13.2)                                            │   debian   │        0        │
├─────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┤
│ opt/python-3.13.11/lib/python3.13/site-packages/pip-25.3.dist-info/METADATA │ python-pkg │        0        │
└─────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┘
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)
```

`--vex repo` 标志会在扫描期间应用来自已配置仓库的 VEX 声明，
从而过滤掉已知的不可利用 CVE。

#### 使用本地 VEX 文件

除了 VEX Hub，Trivy 还支持使用本地 VEX 文件进行漏洞过滤。
您可以下载 Docker Hardened Images 提供的 VEX 证明，并直接将其与 Trivy 配合使用。

首先，为您的镜像下载 VEX 证明：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

然后使用本地 VEX 文件扫描镜像：

```console
$ trivy image --scanners vuln --vex vex.json dhi.io/<image>:<tag>
```

## Wiz

[Wiz](https://www.wiz.io/) 是一个云安全平台，包含容器镜像扫描功能，并支持 DHI VEX 证明。
Wiz CLI 会自动从 Docker Hardened Images 获取 VEX 声明，以提供准确的漏洞评估。

### 使用 Wiz CLI 扫描 DHI

获取 Wiz 订阅并安装 Wiz CLI 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

```console
$ docker login dhi.io
$ docker pull dhi.io/<image>:<tag>
$ wiz docker scan --image dhi.io/<image>:<tag>
```

## 导出 VEX 证明

对于需要本地 VEX 文件的扫描器（如 Grype 或带本地文件的 Trivy），
您可以从 Docker Hardened Images 导出 VEX 证明。

> [!NOTE]
>
> 默认情况下，VEX 证明会从 `registry.scout.docker.com` 获取。如果您的网络有出站限制，请确保可以访问此注册表。
> 您也可以将证明镜像到备用注册表。有关更多详细信息，请参阅[镜像到第三方注册表](mirror.md#mirror-to-a-third-party-registry)。

将 VEX 证明导出到 JSON 文件：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> [!NOTE]
>
> `docker scout vex get` 命令需要 [Docker Scout CLI](https://github.com/docker/scout-cli/) 1.18.3 或更高版本。
>
> 如果镜像在您的设备上本地存在，您必须在镜像名称前加上 `registry://` 前缀。例如，使用
> `registry://docs/dhi-python:3.13` 而不是 `docs/dhi-python:3.13`。