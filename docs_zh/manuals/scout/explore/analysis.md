---
title: Docker Scout 镜像分析
description: Docker Scout 镜像分析提供镜像构成及其所含漏洞的详细视图
keywords: scout, scanning, vulnerabilities, supply chain, security, analysis
aliases:
- /scout/advanced-image-analysis/
- /scout/image-analysis/
---

当您为仓库启用镜像分析时，
Docker Scout 会自动分析您推送到该仓库的新镜像。

镜像分析会提取软件物料清单 (SBOM)
及其他镜像元数据，并根据[安全公告](/manuals/scout/deep-dive/advisory-db-sources.md)中的漏洞数据进行评估。

如果您使用 CLI 或 Docker Desktop 作为一次性任务运行镜像分析，
Docker Scout 不会存储关于您镜像的任何数据。但是，如果您为容器镜像仓库启用 Docker Scout，
Docker Scout 会在分析后保存镜像的元数据快照。当新的漏洞数据可用时，Docker Scout 会使用元数据快照重新校准分析，这意味着镜像的安全状态会实时更新。
这种动态评估意味着当新的 CVE 信息被披露时，无需重新分析镜像。

Docker Scout 镜像分析默认适用于 Docker Hub 仓库。
您还可以集成第三方镜像仓库和其他服务。要了解更多信息，
请参阅[将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

## 在仓库上启用 Docker Scout

Docker Personal 套餐包含 1 个启用 Scout 的仓库。如果您需要更多仓库，可以升级您的
Docker 订阅。请参阅[订阅和功能](https://www.docker.com/pricing/)，
了解每个订阅级别包含多少个启用 Scout 的仓库。

在您可以在第三方镜像仓库中的仓库上启用镜像分析之前，
该镜像仓库必须已为您的 Docker 组织集成了 Docker Scout。
Docker Hub 默认已集成。更多信息，请参阅
[容器镜像仓库集成](/manuals/scout/integrations/_index.md#container-registries)。

> [!NOTE]
>
> 您必须在 Docker 组织中拥有 **Editor**（编辑者）或 **Owner**（所有者）角色，
> 才能在仓库上启用镜像分析。

启用镜像分析的步骤：

1. 前往 Docker Scout 仪表板中的 [Repository settings（仓库设置）](https://scout.docker.com/settings/repos)。
2. 选择您要启用的仓库。
3. 选择 **Enable image analysis（启用镜像分析）**。

如果您的仓库已包含镜像，
Docker Scout 会自动拉取并分析最新的镜像。

## 分析镜像仓库中的镜像

要触发镜像仓库中镜像的分析，请将镜像推送到
已与 Docker Scout 集成的镜像仓库，并推送到已启用镜像分析的仓库。

> [!NOTE]
>
> Docker Scout 平台上的镜像分析有 10 GB 的最大镜像文件大小限制，
> 除非镜像带有 SBOM 证明。
> 请参阅[最大镜像大小](#maximum-image-size)。

1. 使用您的 Docker ID 登录，可以使用 `docker login` 命令或 Docker Desktop 中的 **Sign in（登录）**按钮。
2. 构建并推送您要分析的镜像。

   ```console
   $ docker build --push --tag <org>/<image:tag> --provenance=true --sbom=true .
   ```

   使用 `--provenance=true` 和 `--sbom=true` 标志进行构建会将
   [构建证明](/manuals/build/metadata/attestations/_index.md) 附加到镜像。Docker Scout
   使用证明来提供更精细的分析结果。

   > [!NOTE]
   >
   > 默认的 `docker` 驱动程序仅在您使用 [containerd 镜像存储](/manuals/desktop/features/containerd.md) 时支持构建证明。

3. 前往 Docker Scout 仪表板中的 [Images（镜像）页面](https://scout.docker.com/reports/images)。

   镜像在您将其推送到镜像仓库后不久就会出现在列表中。
   分析结果可能需要几分钟才会显示。

## 分析本地镜像

您可以使用 Docker Desktop 或 Docker CLI 的 `docker scout` 命令来分析本地镜像。

### Docker Desktop

> [!NOTE]
>
> Docker Desktop 后台索引支持最大 10 GB 大小的镜像。
> 请参阅[最大镜像大小](#maximum-image-size)。

使用 Docker Desktop GUI 在本地分析镜像：

1. 拉取或构建您要分析的镜像。
2. 前往 Docker 仪表板中的 **Images（镜像）**视图。
3. 在列表中选择一个本地镜像。

   这将打开[镜像详情视图](./image-details-view.md)，显示 Docker Scout 分析为所选镜像发现的软件包和漏洞的细分。

### CLI

`docker scout` CLI 命令提供了一个命令行界面，用于从终端使用 Docker Scout。

- `docker scout quickview`：指定镜像的摘要，参见 [Quickview（快速查看）](#quickview)
- `docker scout cves`：指定镜像的本地分析，参见 [CVEs（CVE）](#cves)
- `docker scout compare`：分析并比较两个镜像

默认情况下，结果会打印到标准输出。
您还可以将结果以结构化格式导出到文件，
例如静态分析结果交换格式 (SARIF)。

#### Quickview

`docker scout quickview` 命令提供给定镜像及其基础镜像中发现的漏洞概览。

```console
$ docker scout quickview traefik:latest
    ✓ SBOM of image already cached, 311 packages indexed

  Your image  traefik:latest  │    0C     2H     8M     1L
  Base image  alpine:3        │    0H     0M     0L     0C
```

如果您的基础镜像已过时，`quickview` 命令还会显示更新基础镜像将如何改变镜像的漏洞暴露情况。

```console
$ docker scout quickview postgres:13.1
    ✓ Pulled
    ✓ Image stored for indexing
    ✓ Indexed 187 packages

  Your image  postgres:13.1                 │   17C    32H    35M    33L
  Base image  debian:buster-slim            │    9C    14H     9M    23L
  Refreshed base image  debian:buster-slim  │    0C     1H     6M    29L
                                            │    -9    -13     -3     +6
  Updated base image  debian:stable-slim    │    0C     0H     0M    17L
                                            │    -9    -14     -9     -6
```

#### CVEs

`docker scout cves` 命令让您全面了解镜像中的所有漏洞。此命令支持多个标志，让您更精确地指定您感兴趣的漏洞，例如，按严重性或软件包类型：

```console
$ docker scout cves --format only-packages --only-vuln-packages \
  --only-severity critical postgres:13.1
    ✓ SBOM of image already cached, 187 packages indexed
    ✗ Detected 10 vulnerable packages with a total of 17 vulnerabilities

     Name            Version         Type        Vulnerabilities
───────────────────────────────────────────────────────────────────────────
  dpkg        1.19.7                 deb      1C     0H     0M     0L
  glibc       2.28-10                deb      4C     0H     0M     0L
  gnutls28    3.6.7-4+deb10u6        deb      2C     0H     0M     0L
  libbsd      0.9.1-2                deb      1C     0H     0M     0L
  libksba     1.3.5-2                deb      2C     0H     0M     0L
  libtasn1-6  4.13-3                 deb      1C     0H     0M     0L
  lz4         1.8.3-1                deb      1C     0H     0M     0L
  openldap    2.4.47+dfsg-3+deb10u5  deb      1C     0H     0M     0L
  openssl     1.1.1d-0+deb10u4       deb      3C     0H     0M     0L
  zlib        1:1.2.11.dfsg-1        deb      1C     0H     0M     0L
```

有关这些命令及其使用方法的更多信息，请参阅 CLI 参考文档：

- [`docker scout quickview`](/reference/cli/docker/scout/quickview.md)
- [`docker scout cves`](/reference/cli/docker/scout/cves.md)

## 漏洞严重性评估

Docker Scout 根据来自[公告来源](/manuals/scout/deep-dive/advisory-db-sources.md)的漏洞数据为漏洞分配严重性评级。
公告的排名和优先级取决于受漏洞影响的软件包类型。例如，如果漏洞影响操作系统软件包，则会优先考虑由发行版维护者分配的严重性级别。

如果首选公告来源为 CVE 分配了严重性评级，但没有 CVSS 分数，Docker Scout 会回退显示来自另一个来源的 CVSS 分数。来自首选公告的严重性评级和来自回退公告的 CVSS 分数会一起显示。这意味着，如果首选公告分配了 `LOW`（低）评级但没有 CVSS 分数，而回退公告分配了 9.8 的 CVSS 分数，则该漏洞的严重性评级可能为 `LOW`，但 CVSS 分数为 9.8。

在任何来源中都未分配 CVSS 分数的漏洞被归类为 **Unspecified**（未指定）(U)。

Docker Scout 不实现专有的漏洞度量系统。所有度量都继承自 Docker Scout 集成的安全公告。公告可能使用不同的阈值来对漏洞进行分类，但大多数都遵循 CVSS v3.0 规范，该规范根据下表将 CVSS 分数映射到严重性评级：

| CVSS 分数 | 严重性评级       |
| ---------- | ---------------- |
| 0.1 – 3.9  | **Low** (L)      |
| 4.0 – 6.9  | **Medium** (M)   |
| 7.0 – 8.9  | **High** (H)     |
| 9.0 – 10.0 | **Critical** (C) |

更多信息，请参阅[漏洞度量 (NIST)](https://nvd.nist.gov/vuln-metrics/cvss)。

请注意，鉴于前面描述的公告优先级和回退机制，Docker Scout 中显示的严重性评级可能与此评级系统有所偏差。

## 最大镜像大小

Docker Scout 平台上的镜像分析，以及由 Docker Desktop 后台索引触发的分析，有 10 GB（解压后）的镜像文件大小限制。
要分析大于此限制的镜像：

- 在构建时附加 [SBOM 证明](/manuals/build/metadata/attestations/sbom.md)。当镜像包含 SBOM 证明时，Docker Scout 会使用它而不是生成一个，因此 10 GB 的限制不适用。
- 或者，您可以使用 [CLI](#cli) 在本地分析镜像。使用 CLI 时，10 GB 的限制不适用。如果镜像包含 SBOM 证明，CLI 会使用它来更快地完成分析。