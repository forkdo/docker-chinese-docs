---
description: 详细介绍 Docker Scout 分析背后的咨询数据库和 CVE 到软件包的匹配服务。
keywords: scout, scanning, analysis, vulnerabilities, Hub, supply chain, security, packages, repositories, ecosystem
title: 咨询数据库来源和匹配服务
aliases:
  /scout/advisory-db-sources/
---

可靠的信息来源对于 Docker Scout 准确评估您的软件制品至关重要。鉴于行业中的来源和方法多种多样，漏洞评估结果出现差异是不可避免的。本文档描述了 Docker Scout 咨询数据库及其 CVE 到软件包的匹配方法，以应对这些差异。

## 咨询数据库来源

Docker Scout 从多个来源聚合漏洞数据。数据会持续更新，以确保您的安全状况能够实时反映最新的可用信息。

Docker Scout 使用以下软件包仓库和安全追踪器：

<!-- vale off -->

- [AlmaLinux 安全咨询](https://errata.almalinux.org/)
- [Alpine secdb](https://secdb.alpinelinux.org/)
- [Amazon Linux 安全中心](https://alas.aws.amazon.com/)
- [Bitnami 漏洞数据库](https://github.com/bitnami/vulndb)
- [CISA 已知被利用漏洞目录](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [CISA Vulnrichment](https://github.com/cisagov/vulnrichment)
- [Chainguard 安全源](https://packages.cgr.dev/chainguard/osv/all.json)
- [Debian 安全错误追踪器](https://security-tracker.debian.org/tracker/)
- [Exploit Prediction Scoring System (EPSS)](https://api.first.org/epss/)
- [GitHub 咨询数据库](https://github.com/advisories/)
- [GitLab 咨询数据库](https://gitlab.com/gitlab-org/advisories-community/)
- [Golang VulnDB](https://github.com/golang/vulndb)
- [国家漏洞数据库 (NVD)](https://nvd.nist.gov/)
- [Oracle Linux 安全](https://linux.oracle.com/security/)
- [Photon OS 3.0 安全咨询](https://github.com/vmware/photon/wiki/Security-Updates-3)
- [Python 打包咨询数据库](https://github.com/pypa/advisory-database)
- [RedHat 安全数据](https://www.redhat.com/security/data/metrics/)
- [Rocky Linux 安全咨询](https://errata.rockylinux.org/)
- [RustSec 咨询数据库](https://github.com/rustsec/advisory-db)
- [SUSE 安全 CVRF](http://ftp.suse.com/pub/projects/security/cvrf/)
- [Ubuntu CVE 追踪器](https://people.canonical.com/~ubuntu-security/cve/)
- [Wolfi 安全源](https://packages.wolfi.dev/os/security.json)
- [inTheWild，一个社区驱动的漏洞利用开放数据库](https://github.com/gmatuz/inthewilddb)

<!-- vale on -->

当您为 Docker 组织启用 Docker Scout 时，Docker Scout 平台上会配置一个新的数据库实例。该数据库存储您镜像的软件物料清单 (SBOM) 和其他元数据。当安全咨询对某个漏洞提供新信息时，您的 SBOM 会与 CVE 信息进行交叉引用，以检测其对您的影响。

有关镜像分析工作原理的更多详细信息，请参阅 [镜像分析页面](/manuals/scout/explore/analysis.md)。

## 严重性和评分优先级

Docker Scout 在确定 CVE 的严重性和评分时遵循两个主要原则：

   - 来源优先级
   - CVSS 版本偏好

对于来源优先级，Docker Scout 遵循以下顺序：

  1. 厂商咨询：Scout 始终使用与软件包和版本匹配的来源提供的严重性和评分数据。例如，Debian 软件包使用 Debian 数据。

  2. NIST 评分数据：如果厂商未为某个 CVE 提供评分数据，Scout 会回退到 NIST 评分数据。

对于 CVSS 版本偏好，一旦 Scout 选择了来源，当 CVSS v4 和 v3 都可用时，它优先选择 CVSS v4，因为 v4 是更现代且更精确的评分模型。

## 漏洞匹配

传统工具通常依赖于广泛的 [通用产品枚举 (CPE)](https://en.wikipedia.org/wiki/Common_Platform_Enumeration) 匹配，这可能导致许多误报结果。

Docker Scout 使用 [软件包 URL (PURLs)](https://github.com/package-url/purl-spec) 将软件包与 CVE 进行匹配，从而实现更精确的漏洞识别。PURLs 显著降低了误报的可能性，仅关注真正受影响的软件包。

## 支持的软件包生态系统

Docker Scout 支持以下软件包生态系统：

- .NET
- GitHub 软件包
- Go
- Java
- JavaScript
- PHP
- Python
- RPM
- Ruby
- `alpm` (Arch Linux)
- `apk` (Alpine Linux)
- `deb` (Debian Linux 及其衍生版本)