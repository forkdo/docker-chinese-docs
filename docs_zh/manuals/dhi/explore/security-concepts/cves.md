---
aliases:
  - /dhi/core-concepts/cves/
title: Common Vulnerabilities and Exposures (CVEs)
linktitle: CVEs
description: 了解什么是 CVE，Docker Hardened Images 如何降低暴露风险，以及如何使用常用工具扫描镜像中的漏洞。
keywords: docker cve scan, grype vulnerability scanner, trivy image scan, vex attestation, secure container images
---

## 什么是 CVE？（What are CVEs?）

CVE 是软件或硬件中公开披露的网络安全缺陷。每个 CVE 都会被分配一个唯一标识符（例如 CVE-2024-12345），并包含标准化的描述，使组织能够一致地跟踪和处理漏洞。

在 Docker 的语境下，CVE 通常涉及基础镜像或应用依赖中的问题。这些漏洞的范围从小错误到严重的安全风险不等，例如远程代码执行或权限提升。

## 为什么 CVE 很重要？（Why are CVEs important?）

定期扫描并更新 Docker 镜像以缓解 CVE，对于维护一个安全且合规的环境至关重要。忽视 CVE 可能导致严重的安全事件，包括：

- 未授权访问：漏洞利用可让攻击者获得对系统的未授权访问。
- 数据泄露：敏感信息可能被暴露或窃取。
- 服务中断：漏洞可被利用来破坏服务或导致停机。
- 合规违规：未能处理已知漏洞可能导致不符合行业法规和标准。

## Docker Hardened Images 如何帮助缓解 CVE

Docker Hardened Images（DHIs，Docker 加固镜像）从一开始就被设计用来最大程度降低 CVE 风险。通过采用安全优先的方法，DHI 在缓解 CVE 方面具有多项优势：

- 缩小攻击面：DHI 采用 distroless（无发行版）方法构建，剥离了不必要的组件和软件包。镜像体积因此最多可比传统镜像小 95%，从而减少了潜在漏洞的数量，使攻击者更难利用那些不需要的软件。
- 更快的 CVE 修复：由 Docker 以 [企业级 SLA](https://docs.docker.com/go/dhi-sla/) 维护，DHI 会持续更新以解决已知漏洞。关键和高严重性的 CVE 会快速被打上补丁，确保你的容器在没有人工干预的情况下保持安全。
- 主动的漏洞管理：通过使用 DHI，组织可以主动管理漏洞。这些镜像附带 CVE 和漏洞暴露（VEX）订阅源，使团队能够随时了解潜在威胁并及时采取必要措施。

## 扫描镜像中的 CVE

定期扫描 Docker 镜像中的 CVE 对于维护安全的容器化环境至关重要。虽然 Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中，但像 Grype 和 Trivy 这样的工具也提供了替代性的扫描能力。以下分别介绍了使用每种工具扫描 Docker 镜像中 CVE 的方法。

### Docker Scout

Docker Scout 已集成到 Docker Desktop 和 Docker CLI 中。它提供漏洞洞察、CVE 概要，以及指向修复指南的直接链接。

#### 使用 Docker Scout 扫描 DHI

要使用 Docker Scout 扫描 Docker Hardened Image，运行以下命令：

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

有关更详细的过滤和 JSON 输出，请参阅 [Docker Scout CLI reference](/reference/cli/docker/scout/)。

### Grype

[Grype](https://github.com/anchore/grype) 是一个开源扫描器，它会将容器镜像与 NVD 和发行版公告等漏洞数据库进行比对。

#### 使用 Grype 扫描 DHI

安装 Grype 之后，你可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image。Grype 要求你先将 VEX 证明（attestation）导出到文件中：

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

[Trivy](https://github.com/aquasecurity/trivy) 是一个用于容器和其他制品的开源漏洞扫描器。它可以检测操作系统软件包和应用依赖中的漏洞。

#### 使用 Trivy 扫描 DHI

安装 Trivy 之后，你可以通过拉取镜像并运行扫描命令来扫描 Docker Hardened Image：

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

Docker Hardened Images 包含已签名的 [VEX（Vulnerability Exploitability eXchange，漏洞可利用性交换）](./vex.md) 证明（attestation），用于标识与镜像运行时行为无关的漏洞。

在使用 Docker Scout 或 Trivy 时，这些 VEX 声明会通过上述示例自动应用，无需任何手动配置。

要手动获取支持 VEX 的工具所需的 VEX 证明：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> [!NOTE]
>
> 如果镜像存在于你设备的本地，你必须在镜像名称前加上 `registry://` 前缀。例如，使用
> `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout vex get dhi.io/python:3.13 --output vex.json
```

这将创建一个包含指定镜像 VEX 声明的 `vex.json` 文件。随后你可以将此文件用于支持 VEX 的工具，以过滤掉已知不可利用的 CVE。
