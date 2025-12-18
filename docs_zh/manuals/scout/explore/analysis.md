---
title: Docker Scout 镜像分析
description:
  Docker Scout 镜像分析提供镜像构成的详细视图以及其中包含的漏洞信息
keywords: scout, 扫描, 漏洞, 供应链, 安全, 分析
aliases:
  - /scout/advanced-image-analysis/
  - /scout/image-analysis/
---

当你为仓库启用镜像分析时，Docker Scout 会自动分析你推送到该仓库的新镜像。

镜像分析会提取软件物料清单（SBOM）和其他镜像元数据，并使用来自[安全公告](/manuals/scout/deep-dive/advisory-db-sources.md)的漏洞数据进行评估。

如果你使用 CLI 或 Docker Desktop 执行一次性的镜像分析任务，Docker Scout 不会存储任何关于你镜像的数据。但如果你为容器镜像仓库启用 Docker Scout，Docker Scout 会在分析后保存镜像的元数据快照。随着新漏洞数据的出现，Docker Scout 会使用元数据快照重新校准分析，这意味着镜像的安全状态会实时更新。这种动态评估意味着当披露新的 CVE 信息时，无需重新分析镜像。

Docker Scout 镜像分析默认对 Docker Hub 仓库可用。你也可以集成第三方注册表和其他服务。欲了解更多信息，请参阅[将 Docker Scout 与其他系统集成](/manuals/scout/integrations/_index.md)。

## 在仓库中启用 Docker Scout

Docker Personal 提供 1 个 Scout 启用的仓库。如果你需要更多仓库，可以升级 Docker 订阅。参阅[订阅和功能](../../subscription/details.md)了解每个订阅层级包含多少 Scout 启用的仓库。

> [!NOTE]
>
> 在第三方注册表的仓库中启用镜像分析之前，该注册表必须与你的 Docker 组织的 Docker Scout 集成。Docker Hub 默认已集成。更多信息请参阅[容器注册表集成](/manuals/scout/integrations/_index.md#container-registries)。

> [!NOTE]
>
> 你必须在 Docker 组织中具有 **Editor** 或 **Owner** 角色才能在仓库中启用镜像分析。

启用镜像分析的方法：

1. 转到 Docker Scout 仪表板中的[仓库设置](https://scout.docker.com/settings/repos)。
2. 选择你想要启用的仓库。
3. 选择 **Enable image analysis**（启用镜像分析）。

如果你的仓库已包含镜像，Docker Scout 会自动拉取并分析最新镜像。

## 分析注册表镜像

要在注册表中触发镜像分析，请将镜像推送到与 Docker Scout 集成的注册表中，并且该仓库已启用镜像分析。

> [!NOTE]
>
> Docker Scout 平台上的镜像分析最大镜像文件大小限制为 10 GB，除非镜像有 SBOM 证明。参见[最大镜像大小](#最大镜像大小)。

1. 使用你的 Docker ID 登录，可以通过 `docker login` 命令或 Docker Desktop 中的 **Sign in**（登录）按钮。
2. 构建并推送你想要分析的镜像。

   ```console
   $ docker build --push --tag <org>/<image:tag> --provenance=true --sbom=true .
   ```

   使用 `--provenance=true` 和 `--sbom=true` 标志构建会为镜像附加[构建证明](/manuals/build/metadata/attestations/_index.md)。Docker Scout 使用证明提供更细粒度的分析结果。

   > [!NOTE]
   >
   > 默认 `docker` 驱动仅在使用[containerd 镜像存储](/manuals/desktop/features/containerd.md)时支持构建证明。

3. 转到 Docker Scout 仪表板中的[镜像页面](https://scout.docker.com/reports/images)。

   推送镜像到注册表后不久，镜像会出现在列表中。分析结果可能需要几分钟才能显示。

## 本地分析镜像

你可以使用 Docker Desktop 或 Docker CLI 的 `docker scout` 命令在本地分析镜像。

### Docker Desktop

> [!NOTE]
>
> Docker Desktop 后台索引支持最大 10 GB 的镜像。参见[最大镜像大小](#最大镜像大小)。

使用 Docker Desktop GUI 在本地分析镜像：

1. 拉取或构建你想要分析的镜像。
2. 转到 Docker Dashboard 中的 **Images**（镜像）视图。
3. 在列表中选择你的一个本地镜像。

   这会打开[镜像详情视图](./image-details-view.md)，显示 Docker Scout 分析发现的所选镜像的包和漏洞的详细信息。

### CLI

`docker scout` CLI 命令提供从终端使用 Docker Scout 的命令行界面。

- `docker scout quickview`：指定镜像的摘要，参见[快速查看](#快速查看)
- `docker scout cves`：指定镜像的本地分析，参见[CVEs](#cves)
- `docker scout compare`：分析并比较两个镜像

默认情况下，结果会打印到标准输出。你也可以将结果导出到文件，格式为结构化格式，例如静态分析结果交换格式（SARIF）。

#### 快速查看

`docker scout quickview` 命令提供给定镜像及其基础镜像中发现漏洞的概览。

```console
$ docker scout quickview traefik:latest
    ✓ SBOM of image already cached, 311 packages indexed

  Your image  traefik:latest  │    0C     2H     8M     1L
  Base image  alpine:3        │    0C     0H     0M     0L
```

如果你的基础镜像已过时，`quickview` 命令还会显示更新基础镜像如何改变镜像的漏洞暴露情况。

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

`docker scout cves` 命令提供镜像中所有漏洞的完整视图。此命令支持多个标志，让你可以更精确地指定感兴趣的漏洞，例如按严重性或包类型：

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

Docker Scout 根据来自[公告源](/manuals/scout/deep-dive/advisory-db-sources.md)的漏洞数据为漏洞分配严重性评级。公告根据受影响包的类型进行排名和优先级排序。例如，如果漏洞影响操作系统包，Docker Scout 会优先考虑发行版维护者分配的严重性级别。

如果首选公告源为 CVE 分配了严重性评级但没有 CVSS 分数，Docker Scout 会回退到显示来自其他源的 CVSS 分数。首选公告的严重性评级和回退公告的 CVSS 分数会一起显示。这意味着漏洞可能有 `LOW` 的严重性评级和 9.8 的 CVSS 分数，如果首选公告分配了 `LOW` 评级但没有 CVSS 分数，而回退公告分配了 9.8 的 CVSS 分数。

在任何源中未分配 CVSS 分数的漏洞被归类为**未指定**（U）。

Docker Scout 不实现专有的漏洞指标系统。所有指标都继承自 Docker Scout 集成的安全公告。公告可能使用不同的阈值对漏洞进行分类，但大多数遵循 CVSS v3.0 规范，该规范根据下表将 CVSS 分数映射到严重性评级：

| CVSS 分数 | 严重性评级  |
| ---------- | ---------------- |
| 0.1 – 3.9  | **Low** (L)      |
| 4.0 – 6.9  | **Medium** (M)   |
| 7.0 – 8.9  | **High** (H)     |
| 9.0 – 10.0 | **Critical** (C) |

更多信息请参阅 [Vulnerability Metrics (NIST)](https://nvd.nist.gov/vuln-metrics/cvss)。

注意，鉴于前面描述的公告优先级和回退机制，Docker Scout 中显示的严重性评级可能偏离此评级系统。

## 最大镜像大小

Docker Scout 平台上的镜像分析，以及 Docker Desktop 后台索引触发的分析，镜像文件大小限制为 10 GB（未压缩）。要分析更大的镜像：

- 在构建时附加[SBOM 证明](/manuals/build/metadata/attestations/sbom.md)。当镜像包含 SBOM 证明时，Docker Scout 使用它而不是生成一个，因此 10 GB 限制不适用。
- 或者，你可以使用[CLI](#cli)在本地分析镜像。使用 CLI 时 10 GB 限制不适用。如果镜像包含 SBOM 证明，CLI 会使用它来更快地完成分析。