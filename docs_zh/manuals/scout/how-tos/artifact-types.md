---
title: 将 Scout 与不同类型的制品配合使用
description: |
  Docker Scout 的一些命令支持使用镜像引用前缀，
  以控制要分析的镜像或文件的位置。
keywords: scout, 漏洞, 分析, 前瞻性分析, cli, 包, sbom, cve, 安全, 本地, 源代码, 供应链
aliases:
  - /scout/image-prefix/
---

Docker Scout CLI 的一些命令支持使用前缀来指定
要分析的制品的位置或类型。

默认情况下，使用 `docker scout cves` 命令进行镜像分析时，
会以 Docker Engine 的本地镜像存储中的镜像为目标。
以下命令始终会使用本地镜像（如果存在）：

```console
$ docker scout cves <image>
```

如果镜像在本地不存在，Docker 会先拉取镜像，然后执行分析。
再次分析同一镜像时会默认使用相同的本地版本，
即使该标签在注册表中已更新也是如此。

通过在镜像引用前添加 `registry://` 前缀，
你可以强制 Docker Scout 分析注册表中的镜像版本：

```console
$ docker scout cves registry://<image>
```

## 支持的前缀

支持的前缀如下：

| 前缀               | 描述                                                           |
| ------------------ | -------------------------------------------------------------- |
| `image://`（默认） | 使用本地镜像，或回退到注册表查找                                 |
| `local://`         | 使用本地镜像存储中的镜像（不进行注册表查找）                     |
| `registry://`      | 使用注册表中的镜像（不使用本地镜像）                             |
| `oci-dir://`       | 使用 OCI 布局目录                                                |
| `archive://`       | 使用 tarball 归档文件（由 `docker save` 创建）                   |
| `fs://`            | 使用本地目录或文件                                               |

你可以在以下命令中使用前缀：

- `docker scout compare`
- `docker scout cves`
- `docker scout quickview`
- `docker scout recommendations`
- `docker scout sbom`

## 示例

本节包含一些示例，展示如何使用前缀
为 `docker scout` 命令指定制品。

### 分析本地项目

`fs://` 前缀允许你直接分析本地源代码，
无需将其构建成容器镜像。
以下 `docker scout quickview` 命令会为你提供当前工作目录中源代码的
漏洞概览摘要：

```console
$ docker scout quickview fs://.
```

要查看本地源代码中漏洞的详细信息，你可以使用
`docker scout cves --details fs://.` 命令。结合使用其他标志，
可以将结果缩小到你感兴趣的包和漏洞。

```console
$ docker scout cves --details --only-severity high fs://.
    ✓ File system read
    ✓ Indexed 323 packages
    ✗ Detected 1 vulnerable package with 1 vulnerability

​## 概览

                    │        Analyzed path
────────────────────┼──────────────────────────────
  Path              │  /Users/david/demo/scoutfs
    vulnerabilities │    0C     1H     0M     0L

​## 包和漏洞

   0C     1H     0M     0L  fastify 3.29.0
pkg:npm/fastify@3.29.0

    ✗ HIGH CVE-2022-39288 [OWASP Top Ten 2017 Category A9 - 使用已知漏洞的组件]
      https://scout.docker.com/v/CVE-2022-39288

      fastify 是一个快速且低开销的 Node.js Web 框架。受影响的 fastify 版本
      存在通过恶意使用 Content-Type 头导致拒绝服务的漏洞。攻击者可以发送
      无效的 Content-Type 头，导致应用程序崩溃。此问题已在提交 fbb07e8d 中修复，
      并将包含在 4.8.1 版本中。建议用户升级。无法升级的用户可以手动过滤
      包含恶意 Content-Type 头的 HTTP 内容。

      受影响范围 : <4.8.1
      修复版本   : 4.8.1
      CVSS 评分  : 7.5
      CVSS 向量  : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H

1 个漏洞在 1 个包中被发现
  低       0
  中       0
  高       1
  严重     0
```

### 将本地项目与镜像进行比较

使用 `docker scout compare`，你可以将本地文件系统上的源代码分析
与容器镜像的分析进行比较。
以下示例将本地源代码（`fs://.`）与注册表镜像
`registry://docker/scout-cli:latest` 进行比较。
在本例中，比较的基准和目标都使用了前缀。

```console
$ docker scout compare fs://. --to registry://docker/scout-cli:latest --ignore-unchanged
WARN 'docker scout compare' is experimental and its behaviour might change in the future
    ✓ File system read
    ✓ Indexed 268 packages
    ✓ SBOM of image already cached, 234 packages indexed


  ## 概览

                           │              Analyzed File System              │              Comparison Image
  ─────────────────────────┼────────────────────────────────────────────────┼─────────────────────────────────────────────
    Path / Image reference │  /Users/david/src/docker/scout-cli-plugin      │  docker/scout-cli:latest
                           │                                                │  bb0b01303584
      platform             │                                                │ linux/arm64
      provenance           │ https://github.com/dvdksn/scout-cli-plugin.git │ https://github.com/docker/scout-cli-plugin
                           │  6ea3f7369dbdfec101ac7c0fa9d78ef05ffa6315      │  67cb4ef78bd69545af0e223ba5fb577b27094505
      vulnerabilities      │    0C     0H     1M     1L                     │    0C     0H     1M     1L
                           │                                                │
      size                 │ 7.4 MB (-14 MB)                                │ 21 MB
      packages             │ 268 (+34)                                      │ 234
                           │                                                │


  ## 包和漏洞


    +   55 个包被添加
    -   21 个包被移除
       213 个包未改变
```

前面的示例为简洁起见已截断。

### 查看镜像 tarball 的 SBOM

以下示例展示了如何使用 `archive://` 前缀
获取使用 `docker save` 创建的镜像 tarball 的 SBOM。
在本例中，镜像是 `docker/scout-cli:latest`，
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

请阅读 CLI 参考文档中关于命令和支持标志的说明：

- [`docker scout quickview`](/reference/cli/docker/scout/quickview.md)
- [`docker scout cves`](/reference/cli/docker/scout/cves.md)
- [`docker scout compare`](/reference/cli/docker/scout/compare.md)
