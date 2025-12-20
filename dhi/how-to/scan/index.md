# 扫描 Docker Hardened Images

Docker Hardened Images (DHIs) 默认设计为安全，但与任何容器镜像一样，作为漏洞管理流程的一部分，定期扫描它们非常重要。

您可以使用与标准镜像相同的工具（如 Docker Scout、Grype 和 Trivy）来扫描 DHIs。DHIs 遵循相同的格式和标准，以确保与您的安全工具兼容。在扫描镜像之前，必须将镜像同步到 Docker Hub 上的您的组织中。

> [!NOTE]
>
> 当您拥有 Docker Hardened Images Enterprise 订阅时，[Docker Scout](/manuals/scout/_index.md) 会自动启用，无需额外费用，适用于 Docker Hub 上所有同步的 Docker Hardened Image 仓库。您可以在组织的仓库中的 Docker Hub UI 下直接查看扫描结果。

> [!IMPORTANT]
>
> 您必须通过 Docker Hardened Images 注册表 (`dhi.io`) 进行身份验证才能拉取镜像。登录时使用您的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果您没有 Docker 账户，请[免费创建一个](../../accounts/create-account.md)。
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
    v 从证明中获取 SBOM，发现 101 个软件包
    v 从证明中获取来源
    v 从证明中获取 VEX 声明
    v 未检测到易受攻击的软件包
    ...
```

有关更详细的过滤和 JSON 输出，请参阅 [Docker Scout CLI 参考](../../../reference/cli/docker/scout/_index.md)。

### 在 CI/CD 中使用 Docker Scout 自动扫描 DHI

将 Docker Scout 集成到您的 CI/CD 管道中，可以在构建过程中自动验证基于 Docker Hardened Images 构建的镜像是否没有已知漏洞。这种主动方法可确保您的镜像在整个开发生命周期中的安全完整性。

#### GitHub Actions 工作流示例

以下是一个使用 Docker Scout 构建和扫描镜像的 GitHub Actions 工作流示例：

```yaml {collapse="true"}
name: DHI 漏洞扫描

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
      - name: 检出仓库
        uses: actions/checkout@v3

      - name: 设置 Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: 登录到 Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: 构建 Docker 镜像
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }} .

      - name: 运行 Docker Scout CVE 扫描
        uses: docker/scout-action@v1
        with:
          command: cves
          image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.SHA }}
          only-severities: critical,high
          exit-code: true
```

`exit-code: true` 参数确保如果检测到任何严重或高严重性漏洞，工作流将失败，从而防止部署不安全的镜像。

有关在 CI 中使用 Docker Scout 的更多详细信息，请参阅[将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

### 将 Docker Scout 结果与其他扫描器比较

其他扫描器报告的某些漏洞可能不会出现在 Docker Scout 结果中。这可能由以下几个原因造成：

- 特定硬件漏洞：某些漏洞可能仅影响特定硬件架构（例如 Power10 处理器），与 Docker 镜像无关，因此 Docker Scout 不会报告。
- VEX 声明过滤：Docker Scout 自动应用 VEX 声明来记录和抑制不适用于镜像的漏洞。如果您的扫描器不使用 VEX 声明，您可能会看到比 Docker Scout 结果更多的漏洞。
- 临时漏洞标识符：Docker Scout 不会显示临时漏洞标识符（如 Debian 的 `TEMP-xxxxxxx`），因为它们不用于外部引用。

虽然 Docker Scout 会自动处理此过滤，但您可以使用 [Grype 忽略规则](https://github.com/anchore/grype#specifying-matches-to-ignore) 在其配置文件 (`~/.grype.yaml`) 中或 [Trivy 策略例外](https://trivy.dev/v0.19.2/misconfiguration/policy/exceptions/) 使用 REGO 规则手动配置其他扫描器的类似过滤，以按 CVE ID、软件包名称、修复状态或其他条件过滤特定漏洞。您还可以按照 [使用 VEX 过滤已知不可利用的 CVE](#use-vex-to-filter-known-non-exploitable-cves) 中的描述在其他扫描器中使用 VEX 声明。

## Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，用于检查容器镜像是否符合 NVD 和发行版公告等漏洞数据库。

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

您应包含 `--vex` 标志以在扫描期间应用 VEX 声明，从而过滤掉已知不可利用的 CVE。有关更多信息，请参阅 [VEX 部分](#use-vex-to-filter-known-non-exploitable-cves)。

## Trivy

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他工件的开源漏洞扫描器。它检测操作系统软件包和应用程序依赖项中的漏洞。

### 使用 Trivy 扫描 DHI

安装 Trivy 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

```console
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln dhi.io/<image>:<tag>
```

要使用 VEX 声明过滤漏洞，Trivy 支持多种方法。Docker 推荐使用 VEX Hub，它提供了从配置的仓库自动下载和应用 VEX 声明的无缝工作流。

#### 使用 VEX Hub（推荐）

配置 Trivy 从 VEX Hub 下载 Docker Hardened Images 公告仓库。运行以下命令设置 VEX 仓库：

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

设置 VEX Hub 后，您可以使用 VEX 过滤扫描 Docker Hardened Image：

```console
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln --vex repo dhi.io/<image>:<tag>
```

例如，扫描 `dhi.io/python:3.13` 镜像：

```console
$ trivy image --scanners vuln --vex repo dhi.io/python:3.13
```

示例输出：

```plaintext
报告摘要

┌─────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┐
│                                   目标                                      │    类型    │  漏洞          │
├─────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┤
│ dhi.io/python:3.13 (debian 13.2)                                            │   debian   │        0        │
├─────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┤
│ opt/python-3.13.11/lib/python3.13/site-packages/pip-25.3.dist-info/METADATA │ python-pkg │        0        │
└─────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┘
图例：
- '-': 未扫描
- '0': 干净（未检测到安全发现）
```

`--vex repo` 标志在扫描期间应用来自配置仓库的 VEX 声明，从而过滤掉已知不可利用的 CVE。

#### 使用本地 VEX 文件

除了 VEX Hub，Trivy 还支持使用本地 VEX 文件进行漏洞过滤。您可以下载 Docker Hardened Images 提供的 VEX 证明并直接在 Trivy 中使用。

首先，下载镜像的 VEX 证明：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

然后使用本地 VEX 文件扫描镜像：

```console
$ trivy image --scanners vuln --vex vex.json dhi.io/<image>:<tag>
```

## 使用 VEX 过滤已知不可利用的 CVE

Docker Hardened Images 包含签名的 VEX（Vulnerability Exploitability eXchange）证明，用于识别与镜像运行时行为无关的漏洞。

使用 Docker Scout 时，这些 VEX 声明会自动应用，无需手动配置。

> [!NOTE]
>
> 默认情况下，VEX 证明从 `registry.scout.docker.com` 获取。如果您的网络有出站限制，请确保可以访问此注册表。您也可以将证明同步到备用注册表。有关更多详细信息，请参阅[同步到第三方注册表](mirror.md#mirror-to-a-third-party-registry)。

要为支持该功能的工具手动创建 VEX 证明的 JSON 文件：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> [!NOTE]
>
> `docker scout vex get` 命令需要 [Docker Scout CLI](https://github.com/docker/scout-cli/) 1.18.3 或更高版本。
>
> 如果镜像存在于本地设备上，则必须在镜像名称前加上 `registry://`。例如，使用 `registry://docs/dhi-python:3.13` 而不是 `docs/dhi-python:3.13`。

例如：

```console
$ docker scout vex get dhi.io/python:3.13 --output vex.json
```

这将创建一个包含指定镜像 VEX 声明的 `vex.json` 文件。然后，您可以将此文件与支持 VEX 的工具一起使用，以过滤掉已知不可利用的 CVE。

例如，使用 Grype 时，可以使用 `--vex` 标志在扫描期间应用 VEX 声明：

```console
$ grype dhi.io/python:3.13 --vex vex.json
```
