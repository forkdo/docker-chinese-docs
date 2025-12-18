---
title: Docker Scout SBOM
description: 使用 Docker Scout 提取项目的 SBOM。
keywords: scout, 供应链, sbom, 软件物料清单, spdx, cli, 证明, 文件
aliases:
- /engine/sbom/
- /scout/sbom/
---

[镜像分析](/manuals/scout/explore/analysis.md) 使用镜像 SBOM 来了解镜像包含哪些包和版本。
Docker Scout 优先使用镜像上可用的 SBOM 证明（推荐）。
如果镜像上没有 SBOM 证明，Docker Scout 会通过索引镜像内容来创建一个。

## 从 CLI 查看

要查看 Docker Scout 生成的 SBOM 内容，可以使用 `docker scout sbom` 命令。

```console
$ docker scout sbom [IMAGE]
```

默认情况下，这会将 SBOM 以 JSON 格式打印到标准输出。
`docker scout sbom` 生成的默认 JSON 格式不是 SPDX-JSON。
要输出 SPDX，请使用 `--format spdx` 标志：

```console
$ docker scout sbom --format spdx [IMAGE]
```

要生成人类可读的列表，请使用 `--format list` 标志：

```console
$ docker scout sbom --format list alpine

           Name             Version    Type
───────────────────────────────────────────────
  alpine-baselayout       3.4.3-r1     apk
  alpine-baselayout-data  3.4.3-r1     apk
  alpine-keys             2.4-r1       apk
  apk-tools               2.14.0-r2    apk
  busybox                 1.36.1-r2    apk
  busybox-binsh           1.36.1-r2    apk
  ca-certificates         20230506-r0  apk
  ca-certificates-bundle  20230506-r0  apk
  libc-dev                0.7.2-r5     apk
  libc-utils              0.7.2-r5     apk
  libcrypto3              3.1.2-r0     apk
  libssl3                 3.1.2-r0     apk
  musl                    1.2.4-r1     apk
  musl-utils              1.2.4-r1     apk
  openssl                 3.1.2-r0     apk
  pax-utils               1.3.7-r1     apk
  scanelf                 1.3.7-r1     apk
  ssl_client              1.36.1-r2    apk
  zlib                    1.2.13-r1    apk
```

有关 `docker scout sbom` 命令的更多信息，请参考 [CLI 参考](/reference/cli/docker/scout/sbom.md)。

## 作为构建证明附加 {#attest}

您可以在构建时生成 SBOM 并将其作为[证明](/manuals/build/metadata/attestations/_index.md)附加到镜像上。
BuildKit 提供了一个默认的 SBOM 生成器，它与 Docker Scout 使用的不同。
您可以使用 `docker build` 命令的 `--attest` 标志来配置 BuildKit 使用 Docker Scout SBOM 生成器。
Docker Scout SBOM 索引器提供更丰富的结果，并确保与 Docker Scout 镜像分析更好的兼容性。

```console
$ docker build --tag <org>/<image> \
  --attest type=sbom,generator=docker/scout-sbom-indexer:latest \
  --push .
```

要构建带有 SBOM 证明的镜像，您必须使用 [containerd 镜像存储](/manuals/desktop/features/containerd.md) 功能，或者将 `docker-container` 构建器与 `--push` 标志一起使用，直接将镜像（含证明）推送到注册表。
经典的镜像存储不支持清单列表或镜像索引，而这些是向镜像添加证明所必需的。

## 提取到文件

将镜像的 SBOM 提取并保存到 SPDX JSON 文件的命令，取决于镜像是否已推送到注册表还是本地镜像。

### 远程镜像

要提取镜像的 SBOM 并保存到文件，可以使用 `docker buildx imagetools inspect` 命令。
此命令仅对注册表中的镜像有效。

```console
$ docker buildx imagetools inspect <image> --format "{{ json .SBOM }}" > sbom.spdx.json
```

### 本地镜像

要提取本地镜像的 SPDX 文件，请使用 `local` 导出器构建镜像，并使用 `scout-sbom-indexer` SBOM 生成器插件。

以下命令将 SBOM 保存到 `build/sbom.spdx.json` 文件。

```console
$ docker build --attest type=sbom,generator=docker/scout-sbom-indexer:latest \
  --output build .
```