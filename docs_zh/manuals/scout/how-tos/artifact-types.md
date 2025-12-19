---
title: 将 Scout 与不同类型的制品配合使用
description: |
  某些 Docker Scout 命令支持镜像引用前缀，
  用于控制要分析的镜像或文件的位置。
keywords: scout, vulnerabilities, analyze, analysis, cli, packages, sbom, cve, security, local, source, code, supply chain
aliases:
  - /scout/image-prefix/
---

某些 Docker Scout CLI 命令支持使用前缀来指定要分析的制品的位置或类型。

默认情况下，`docker scout cves` 命令对 Docker Engine 本地镜像存储中的镜像进行分析。
以下命令始终使用本地镜像（如果存在）：

```console
$ docker scout cves <image>
```

如果镜像在本地不存在，Docker 会在运行分析之前拉取该镜像。
默认情况下，即使标签在注册表中已更改，再次分析同一镜像时仍会使用相同的本地版本。

通过在镜像引用前添加 `registry://` 前缀，
可以强制 Docker Scout 分析镜像的注册表版本：

```console
$ docker scout cves registry://<image>
```

## 支持的前缀

支持的前缀包括：

| 前缀                 | 描述                                                                 |
| -------------------- | -------------------------------------------------------------------- |
| `image://`（默认）   | 使用本地镜像，或回退到注册表查找                                     |
| `local://`           | 使用本地镜像存储中的镜像（不执行注册表查找）                         |
| `registry://`        | 使用注册表中的镜像（不使用本地镜像）                                 |
| `oci-dir://`         | 使用 OCI 布局目录                                                    |
| `archive://`         | 使用 tarball 归档文件（由 `docker save` 创建）                       |
| `fs://`              | 使用本地目录或文件                                                   |

您可以在以下命令中使用前缀：

- `docker scout compare`
- `docker scout cves`
- `docker scout quickview`
- `docker scout recommendations`
- `docker scout sbom`

## 示例

本节包含一些示例，展示如何使用前缀为 `docker scout` 命令指定制品。

### 分析本地项目

`fs://` 前缀允许您直接分析本地源代码，
而无需将其构建为容器镜像。
以下 `docker scout quickview` 命令可为您提供当前工作目录中源代码的漏洞概览：

```console
$ docker scout quickview fs://.
```

要查看本地源代码中发现的漏洞详情，
可以使用 `docker scout cves --details fs://.` 命令。
结合其他标志，可以将结果缩小到您感兴趣的包和漏洞范围。

```console
$ docker scout cves --details --only-severity high fs://.
    ✓ 文件系统读取
    ✓ 已索引 323 个包
    ✗ 检测到 1 个易受攻击的包，包含 1 个漏洞

​## 概览

                    │        分析路径
────────────────────┼──────────────────────────────
  路径              │  /Users/david/demo/scoutfs
    漏洞            │    0C     1H     0M     0L

​## 包和漏洞

   0C     1H     0M     0L  fastify 3.29.0
pkg:npm/fastify@3.29.0

    ✗ 高危 CVE-2022-39288 [OWASP Top Ten 2017 Category A9 - 使用已知漏洞的组件]
      https://scout.docker.com/v/CVE-2022-39288

      fastify 是一个快速且开销较低的 Node.js Web 框架。受影响的 fastify 版本
      存在通过恶意使用 Content-Type 标头导致的拒绝服务漏洞。攻击者可以发送
      无效的 Content-Type 标头，导致应用程序崩溃。此问题已在提交 fbb07e8d 中
      得到解决，并将包含在 4.8.1 版本中。建议用户升级。无法升级的用户可以
      手动过滤掉具有恶意 Content-Type 标头的 HTTP 内容。

      受影响范围：<4.8.1
      修复版本：4.8.1
      CVSS 评分：7.5
      CVSS 向量：CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H

在 1 个包中发现 1 个漏洞
  低危      0
  中危      0
  高危      1
  严重      0
```

### 将本地项目与镜像进行比较

使用 `docker scout compare`，您可以将本地文件系统上源代码的分析结果
与容器镜像的分析结果进行比较。
以下示例将本地源代码 (`fs://.`)
与注册表镜像 `registry://docker/scout-cli:latest` 进行比较。
在这种情况下，比较的基准和目标都使用了前缀。

```console
$ docker scout compare fs://. --to registry://docker/scout-cli:latest --ignore-unchanged
WARN 'docker scout compare' 是实验性功能，其行为将来可能会发生变化
    ✓ 文件系统读取
    ✓ 已索引 268 个包
    ✓ 镜像的 SBOM 已缓存，已索引 234 个包


  ## 概览

                           │              分析的文件系统              │              比较镜像
  ─────────────────────────┼────────────────────────────────────────────────┼─────────────────────────────────────────────
    路径 / 镜像引用        │  /Users/david/src/docker/scout-cli-plugin      │  docker/scout-cli:latest
                           │                                                │  bb0b01303584
      平台                 │                                                │ linux/arm64
      来源                 │ https://github.com/dvdksn/scout-cli-plugin.git │ https://github.com/docker/scout-cli-plugin
                           │  6ea3f7369dbdfec101ac7c0fa9d78ef05ffa6315      │  67cb4ef78bd69545af0e223ba5fb577b27094505
      漏洞                 │    0C     0H     1M     1L                     │    0C     0H     1M     1L
                           │                                                │
      大小                 │ 7.4 MB (-14 MB)                                │ 21 MB
      包                   │ 268 (+34)                                      │ 234
                           │                                                │


  ## 包和漏洞


    +   55 个包已添加
    -   21 个包已移除
       213 个包未更改
```

为简洁起见，前面的示例已被截断。

### 查看镜像 tarball 的 SBOM

以下示例展示如何使用 `archive://` 前缀
获取使用 `docker save` 创建的镜像 tarball 的 SBOM。
此示例中的镜像是 `docker/scout-cli:latest`，
SBOM 以 SPDX 格式导出到文件 `sbom.spdx.json`。

```console
$ docker pull docker/scout-cli:latest
latest: Pulling from docker/scout-cli
257973a141f5: Download complete 
1f2083724dd1: Download complete 
5c8125a73507: Download complete 
Digest: sha256:13318bb059b0f8b0b87b35ac7050782462b5d0ac3f96f9f23d165d8ed68d0894
$ docker save docker/scout-cli:latest -o scout-cli.tar
$ docker scout sbom --format spdx -o sbom.spdx.json archive://scout-cli.tar
```

## 了解更多

在 CLI 参考文档中阅读有关命令和支持的标志：

- [`docker scout quickview`](/reference/cli/docker/scout/quickview.md)
- [`docker scout cves`](/reference/cli/docker/scout/cves.md)
- [`docker scout compare`](/reference/cli/docker/scout/compare.md)