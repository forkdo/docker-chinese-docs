---
title: 常见漏洞与暴露（CVE）
linktitle: CVE
description: 了解什么是 CVE，Docker 硬化镜像如何减少暴露风险，以及如何使用流行工具扫描镜像中的漏洞。
keywords: docker cve scan, grype vulnerability scanner, trivy image scan, vex attestation, secure container images
---

## 什么是 CVE？

CVE 是软件或硬件中公开披露的网络安全缺陷。每个 CVE 都被分配一个唯一的标识符（例如 CVE-2024-12345），并包含标准化的描述，使组织能够一致地跟踪和解决漏洞。

在 Docker 的上下文中，CVE 通常涉及基础镜像或应用程序依赖项中的问题。这些漏洞可能从轻微的错误到严重的安全风险，例如远程代码执行或权限提升。

## 为什么 CVE 很重要？

定期扫描和更新 Docker 镜像以缓解 CVE 对于维护安全和合规的环境至关重要。忽略 CVE 可能导致严重的安全漏洞，包括：

- 未授权访问：漏洞可能授予攻击者对系统的未授权访问权限。
- 数据泄露：敏感信息可能被暴露或窃取。
- 服务中断：漏洞可能被利用来中断服务或导致停机。
- 合规违规：未能解决已知漏洞可能导致不符合行业法规和标准。

## Docker 硬化镜像如何帮助缓解 CVE

Docker 硬化镜像（DHI）从设计之初就旨在最小化 CVE 风险。通过采用安全优先的方法，DHI 在缓解 CVE 方面提供了多项优势：

- 减少攻击面：DHI 使用无发行版（distroless）方法构建，剥离了不必要的组件和包。这种镜像大小的减少（最多比传统镜像小 95%）限制了潜在漏洞的数量，使得攻击者更难利用不必要的软件。
- 更快的 CVE 修复：由 Docker 企业级 SLA 维护，DHI 持续更新以解决已知漏洞。关键和高严重性的 CVE 会被快速修补，确保您的容器保持安全而无需手动干预。
- 主动的漏洞管理：通过使用 DHI，组织可以主动管理漏洞。镜像附带 CVE 和漏洞暴露（VEX）数据源，使团队能够及时了解潜在威胁并迅速采取必要措施。

## 扫描镜像中的 CVE

定期扫描 Docker 镜像中的 CVE 对于维护安全的容器化环境至关重要。虽然 Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中，但 Grype 和 Trivy 等工具提供了替代的扫描功能。以下是使用每种工具扫描 Docker 镜像中 CVE 的说明。

### Docker Scout

Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中。它提供漏洞洞察、CVE 摘要以及直接链接到修复指导。

#### 使用 Docker Scout 扫描 DHI

要使用 Docker Scout 扫描 Docker 硬化镜像，请运行以下命令：

```console
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

### Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，根据 NVD 和发行版公告等漏洞数据库检查容器镜像。

#### 使用 Grype 扫描 DHI

安装 Grype 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker 硬化镜像。Grype 要求您首先将 VEX 证明导出到文件：

```console
$ docker pull dhi.io/<image>:<tag>
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
$ grype dhi.io/<image>:<tag> --vex vex.json
```

示例输出：

```plaintext
NAME               INSTALLED              FIXED-IN     TYPE  VULNERABILITY     SEVERITY    EPSS%  RISK
libperl5.36        5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl               5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl-base          5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
...
```

### Trivy

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他制品的开源漏洞扫描器。它检测 OS 包和应用程序依赖项中的漏洞。

#### 使用 Trivy 扫描 DHI

安装 Trivy 后，您可以通过拉取镜像并运行扫描命令来扫描 Docker 硬化镜像：

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

## 使用 VEX 过滤已知不可利用的 CVE

Docker 硬化镜像包含签名的 [VEX（漏洞可利用性交换）](./vex.md) 证明，用于标识与镜像运行时行为无关的漏洞。

使用 Docker Scout 或 Trivy 时，通过前面的示例会自动应用这些 VEX 语句，无需手动配置。

要为支持 VEX 的工具手动检索 VEX 证明：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> [!NOTE]
>
> `docker scout vex get` 命令需要 [Docker Scout CLI](https://github.com/docker/scout-cli/) 版本 1.18.3 或更高版本。
>
> 如果镜像存在于您设备的本地，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout vex get dhi.io/python:3.13 --output vex.json
```

这将为指定的镜像创建一个包含 VEX 语句的 `vex.json` 文件。然后您可以将此文件与支持 VEX 的工具一起使用，以过滤掉已知不可利用的 CVE。