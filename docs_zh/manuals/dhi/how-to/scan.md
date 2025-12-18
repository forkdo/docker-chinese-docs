---
title: 扫描 Docker Hardened Images
linktitle: 扫描镜像
description: 了解如何使用 Docker Scout、Grype 或 Trivy 扫描 Docker Hardened Images 中的已知漏洞。
keywords: 扫描容器镜像, docker scout cves, grype 扫描器, trivy 容器扫描器, vex 证明
weight: 46
---

Docker Hardened Images (DHIs) 默认设计为安全的，但与任何容器镜像一样，作为漏洞管理流程的一部分，定期扫描它们非常重要。

您可以使用与标准镜像相同的工具（如 Docker Scout、Grype 和 Trivy）扫描 DHIs。DHIs 遵循相同格式和标准，确保与您的安全工具兼容。在扫描镜像之前，必须先将镜像镜像到您在 Docker Hub 上的组织中。

> [!NOTE]
>
> 当您拥有 Docker Hardened Images Enterprise 订阅时，[Docker
> Scout](/manuals/scout/_index.md) 会自动为 Docker Hub 上所有镜像的 Docker Hardened Image 仓库启用，无需额外费用。您可以在 Docker Hub UI 中组织的仓库下直接查看扫描结果。

> [!IMPORTANT]
>
> 您必须对 Docker Hardened Images 仓库（`dhi.io`）进行身份验证才能拉取镜像。使用您的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）登录。如果您没有 Docker 账户，请[创建一个](../../accounts/create-account.md)免费账户。
>
> 运行 `docker login dhi.io` 进行身份验证。

## Docker Scout

Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中。它提供漏洞洞察、CVE 摘要以及直接链接到修复指导。

### 使用 Docker Scout 扫描 DHI

要使用 Docker Scout 扫描 Docker Hardened Image，请运行以下命令：

```console
$ docker scout cves dhi.io/<image>:<tag> --platform <platform>
```

示例输出：

```plaintext
    v SBOM 从证明中获得，发现 101 个包
    v 证明从证明中获得
    v VEX 语句从证明中获得
    v 未检测到易受攻击的包
    ...
```

有关详细过滤和 JSON 输出，请参阅 [Docker Scout CLI 参考](../../../reference/cli/docker/scout/_index.md)。

### 在 CI/CD 中使用 Docker Scout 自动扫描 DHI

将 Docker Scout 集成到您的 CI/CD 管道中，可以自动验证从 Docker Hardened Images 构建的镜像在构建过程中是否没有已知漏洞。这种主动方法确保了在开发周期中持续保持镜像的安全完整性。

#### 示例 GitHub Actions 工作流

以下是构建镜像并使用 Docker Scout 扫描的示例 GitHub Actions 工作流：

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

`exit-code: true` 参数确保如果检测到任何严重或高严重性漏洞，工作流将失败，防止不安全镜像的部署。

有关在 CI 中使用 Docker Scout 的更多详细信息，请参阅 [将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

### 比较 Docker Scout 结果与其他扫描器

其他扫描器报告的某些漏洞可能不会出现在 Docker Scout 结果中。这可能有几个原因：

- 硬件特定漏洞：某些漏洞可能只影响特定硬件架构（例如 Power10 处理器），对 Docker 镜像不相关，因此 Docker Scout 不会报告。
- VEX 语句过滤：Docker Scout 自动应用 VEX 语句来记录和抑制不适用于镜像的漏洞。如果您的扫描器不消费 VEX 语句，您可能会看到比 Docker Scout 结果更多的漏洞报告。
- 临时漏洞标识符：临时漏洞标识符（如 Debian 的 `TEMP-xxxxxxx`）不会被 Docker Scout 显示，因为它们不用于外部引用。

虽然 Docker Scout 自动处理此过滤，但您可以使用 [Grype 忽略规则](https://github.com/anchore/grype#specifying-matches-to-ignore) 在其配置文件（`~/.grype.yaml`）中或使用 [Trivy 策略异常](https://trivy.dev/v0.19.2/misconfiguration/policy/exceptions/) 通过 REGO 规则手动配置其他扫描器的类似过滤，以根据 CVE ID、包名、修复状态或其他标准过滤特定漏洞。您也可以在其他扫描器中使用 VEX 语句，如 [使用 VEX 过滤已知不可利用的 CVE](#use-vex-to-filter-known-non-exploitable-cves) 部分所述。

## Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，根据 NVD 和发行版公告等漏洞数据库检查容器镜像。

### 使用 Grype 扫描 DHI

安装 Grype 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

```console
$ docker pull dhi.io/<image>:<tag>
$ grype dhi.io/<image>:<tag>
```

示例输出：

```plaintext
NAME               INSTALLED              FIXED-IN     TYPE  VULNERABILITY     SEVERITY    EPSS%  RISK
libperl5.36        5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl               5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl-base          5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
...
```

您应包含 `--vex` 标志以在扫描期间应用 VEX 语句，过滤已知不可利用的 CVE。更多信息，请参阅 [VEX 部分](#use-vex-to-filter-known-non-exploitable-cves)。

## Trivy

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他工件的开源漏洞扫描器。它检测 OS 包和应用程序依赖项中的漏洞。

### 使用 Trivy 扫描 DHI

安装 Trivy 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

```console
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln --vex repo dhi.io/<image>:<tag>
```

示例输出：

```plaintext
Report Summary

┌──────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┬─────────┐
│                                    Target                                    │    Type    │ Vulnerabilities │ Secrets │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ dhi.io/<image>:<tag> (debian 12.11)                                          │   debian   │       66        │    -    │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ opt/python-3.13.4/lib/python3.13/site-packages/pip-25.1.1.dist-info/METADATA │ python-pkg │        0        │    -    │
└──────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┴─────────┘
```

您应包含 `--vex` 标志以在扫描期间应用 VEX 语句，过滤已知不可利用的 CVE。

## 使用 VEX 过滤已知不可利用的 CVE

Docker Hardened Images 包含已签名的 VEX（Vulnerability Exploitability Exchange）证明，标识与镜像运行时行为无关的漏洞。

使用 Docker Scout 时，这些 VEX 语句会自动应用，无需手动配置。

> [!NOTE]
>
> 默认情况下，VEX 证明从 `registry.scout.docker.com` 获取。如果您的网络有出站限制，请确保可以访问此注册表。您也可以将证明镜像到其他注册表。更多详细信息，请参阅 [镜像到第三方注册表](mirror.md#mirror-to-a-third-party-registry)。

要为支持的工具手动创建 VEX 证明的 JSON 文件：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> [!NOTE]
>
> `docker scout vex get` 命令需要 [Docker Scout CLI](https://github.com/docker/scout-cli/) 1.18.3 或更高版本。
>
> 如果镜像存在于您设备的本地，您必须在镜像名称前加上 `registry://`。例如，使用 `registry://docs/dhi-python:3.13` 而不是 `docs/dhi-python:3.13`。

例如：

```console
$ docker scout vex get dhi.io/python:3.13 --output vex.json
```

这会为指定镜像创建一个包含 VEX 语句的 `vex.json` 文件。然后您可以将此文件与支持 VEX 的工具一起使用，以过滤已知不可利用的 CVE。

例如，使用 Grype 时，您可以使用 `--vex` 标志在扫描期间应用 VEX 语句：

```console
$ grype dhi.io/python:3.13 --vex vex.json
```