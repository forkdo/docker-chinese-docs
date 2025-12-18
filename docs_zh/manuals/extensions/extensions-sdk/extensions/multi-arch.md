---
title: 构建多架构扩展
description: 创建扩展的第三步。
keywords: Docker, Extensions, sdk, build, multi-arch
aliases: 
 - /desktop/extensions-sdk/extensions/multi-arch/
---

强烈建议，至少为以下架构提供扩展支持：

- `linux/amd64`
- `linux/arm64`

Docker Desktop 会根据用户的系统架构检索扩展镜像。如果扩展未提供匹配用户系统架构的镜像，Docker Desktop 将无法安装该扩展。因此，用户无法在 Docker Desktop 中运行该扩展。

## 为多架构构建并推送

如果您通过 `docker extension init` 命令创建扩展，目录根部的 `Makefile` 包含一个名为 `push-extension` 的目标。

运行 `make push-extension` 可以针对 `linux/amd64` 和 `linux/arm64` 两个平台构建扩展，并推送到 Docker Hub。

例如：

```console
$ make push-extension
```

或者，如果您从空目录开始，可使用以下命令为多架构构建扩展：

```console
$ docker buildx build --push --platform=linux/amd64,linux/arm64 --tag=username/my-extension:0.0.1 .
```

然后，您可以使用 [`docker buildx imagetools` 命令](/reference/cli/docker/buildx/imagetools/_index.md) 检查镜像清单，确认镜像是否支持两种架构：

```console
$ docker buildx imagetools inspect username/my-extension:0.0.1
Name:      docker.io/username/my-extension:0.0.1
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:f3b552e65508d9203b46db507bb121f1b644e53a22f851185d8e53d873417c48

Manifests:
  Name:      docker.io/username/my-extension:0.0.1@sha256:71d7ecf3cd12d9a99e73ef448bf63ae12751fe3a436a007cb0969f0dc4184c8c
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/amd64

  Name:      docker.io/username/my-extension:0.0.1@sha256:5ba4ceea65579fdd1181dfa103cc437d8e19d87239683cf5040e633211387ccf
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm64
```

> [!TIP]
>
> 如果推送镜像时遇到问题，请确保您已登录 Docker Hub。否则，请运行 `docker login` 进行身份验证。

更多信息，请参阅 [多平台镜像](/manuals/build/building/multi-platform.md) 页面。

## 添加多架构二进制文件

如果您的扩展包含部署到主机的二进制文件，那么在为多架构构建扩展时，确保这些二进制文件也具有正确的架构非常重要。

目前，Docker 未在 `metadata.json` 文件中提供显式指定每个架构多个二进制文件的方法。但是，您可以在扩展的 `Dockerfile` 中根据 `TARGETARCH` 添加特定架构的二进制文件。

以下示例展示了一个扩展，它在操作中使用二进制文件，且需要在 Mac 和 Windows 的 Docker Desktop 中运行。

在 `Dockerfile` 中，根据目标架构下载二进制文件：

```Dockerfile
#syntax=docker/dockerfile:1.3-labs

FROM alpine AS dl
WORKDIR /tmp
RUN apk add --no-cache curl tar
ARG TARGETARCH
RUN <<EOT ash
    mkdir -p /out/darwin
    curl -fSsLo /out/darwin/kubectl "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/darwin/${TARGETARCH}/kubectl"
    chmod a+x /out/darwin/kubectl
EOT
RUN <<EOT ash
    if [ "amd64" = "$TARGETARCH" ]; then
        mkdir -p /out/windows
        curl -fSsLo /out/windows/kubectl.exe "https://dl.k8s.io/release/$(curl -Ls https://dl.k8s.io/release/stable.txt)/bin/windows/amd64/kubectl.exe"
    fi
EOT

FROM alpine
LABEL org.opencontainers.image.title="example-extension" \
    org.opencontainers.image.description="My Example Extension" \
    org.opencontainers.image.vendor="Docker Inc." \
    com.docker.desktop.extension.api.version=">= 0.3.3"

COPY --from=dl /out /
```

在 `metadata.json` 文件中，为每个平台指定每个二进制文件的路径：

```json
{
  "icon": "docker.svg",
  "ui": {
    "dashboard-tab": {
      "title": "Example Extension",
      "src": "index.html",
      "root": "ui"
    }
  },
  "host": {
    "binaries": [
      {
        "darwin": [
          {
            "path": "/darwin/kubectl"
          }
        ],
        "windows": [
          {
            "path": "/windows/kubectl.exe"
          }
        ]
      }
    ]
  }
}
```

结果是，当 `TARGETARCH` 等于：

- `arm64` 时，获取的 `kubectl` 二进制文件对应 `arm64` 架构，并复制到最终阶段的 `/darwin/kubectl`。
- `amd64` 时，获取两个 `kubectl` 二进制文件，一个用于 Darwin，另一个用于 Windows。它们分别复制到最终阶段的 `/darwin/kubectl` 和 `/windows/kubectl.exe`。

> [!NOTE]
>
> 在这两种情况下，Darwin 的二进制文件目标路径都是 `darwin/kubectl`。唯一的变化是下载的架构特定二进制文件。

当安装扩展时，扩展框架会将二进制文件从扩展镜像中的 `/darwin/kubectl`（Darwin）或 `/windows/kubectl.exe`（Windows）复制到用户主机文件系统的特定位置。

## 我能否开发运行 Windows 容器的扩展？

虽然 Docker Extensions 支持 Windows、Mac 和 Linux 的 Docker Desktop，但扩展框架仅支持 Linux 容器。因此，构建扩展镜像时必须将 `linux` 作为目标操作系统。