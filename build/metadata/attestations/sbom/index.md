# SBOM 证明


SBOM 证明通过验证镜像所包含的软件构件以及用于创建镜像的构件，来帮助确保
[软件供应链透明度](/guides/docker-scout/)。包含在 [SBOM](/guides/docker-scout/) 中用于描述软件构件的
元数据可能包括：

- 构件名称
- 版本
- 许可证类型
- 作者
- 唯一的包标识符

在构建过程中为镜像内容建立索引，比扫描最终镜像更有优势。当扫描作为构建的一部分发生时，
你可以检测到用于构建镜像的软件，而这些软件可能不会出现在最终镜像中。

Docker 支持通过基于 BuildKit 和证明的 SLSA 兼容构建流程来生成 SBOM 并生成证明。由
[BuildKit](/manuals/build/buildkit/_index.md) 生成的 SBOM 遵循 SPDX 标准，并使用
[in-toto SPDX predicate](https://github.com/in-toto/attestation/blob/main/spec/predicates/spdx.md)
定义的格式作为 JSON 编码的 SPDX 文档附加到最终镜像上。在本页中，你将学习如何使用 Docker 工具来
创建、管理和验证 SBOM 证明。

## 创建 SBOM 证明

要创建 SBOM 证明，请将 `--attest type=sbom` 选项传递给
`docker buildx build` 命令：

```console
$ docker buildx build --tag <namespace>/<image>:<version> \
    --attest type=sbom --push .
```

或者，你可以使用简写选项 `--sbom=true` 代替 `--attest type=sbom`。

有关如何使用 GitHub Actions 添加 SBOM 证明的示例，请参阅
[使用 GitHub Actions 添加证明](/manuals/build/ci/github-actions/attestations.md)。

## 验证 SBOM 证明

在将镜像推送到镜像仓库之前，务必验证为你的镜像生成的 SBOM。

要验证，你可以使用 `local` 导出器构建镜像。使用 `local` 导出器构建会将构建结果保存到
本地文件系统，而不是创建镜像。证明会被写入导出根目录下的一个 JSON 文件。

```console
$ docker buildx build \
  --sbom=true \
  --output type=local,dest=out .
```

SBOM 文件出现在输出的根目录中，命名为 `sbom.spdx.json`：

```console
$ ls -1 ./out | grep sbom
sbom.spdx.json
```

## 参数

默认情况下，BuildKit 只扫描镜像的最终阶段。生成的 SBOM 不包含在早期阶段安装的
构建时依赖项，也不包含构建上下文中存在的依赖项。这可能导致你忽略这些依赖项中的漏洞，
从而影响最终构建构件的安全性。

例如，你可能会使用 [多阶段构建](/manuals/build/building/multi-stage.md)，
并为最终阶段使用 `FROM scratch` 节来达到更小的镜像体积。

```dockerfile
FROM alpine AS build
# build the software ...

FROM scratch
COPY --from=build /path/to/bin /bin
ENTRYPOINT [ "/bin" ]
```

扫描使用该 Dockerfile 示例构建出的镜像，不会暴露 `build` 阶段中使用的构建时依赖项。

要包含来自 Dockerfile 的构建时依赖项，你可以设置构建参数 `BUILDKIT_SBOM_SCAN_CONTEXT`
和 `BUILDKIT_SBOM_SCAN_STAGE`。这会将扫描范围扩展到包含构建上下文和额外的阶段。

你可以将这些参数设置为全局参数（在声明 Dockerfile 语法指令之后、第一个 `FROM` 命令之前），
或在每个阶段中单独设置。如果全局设置，该值会传播到 Dockerfile 中的每个阶段。

`BUILDKIT_SBOM_SCAN_CONTEXT` 和 `BUILDKIT_SBOM_SCAN_STAGE` 构建参数是特殊值。你不能使用这些参数
进行变量替换，也不能通过 Dockerfile 内的环境变量设置它们。设置这些值的唯一方式是使用
Dockerfile 中显式的 `ARG` 命令。

### 扫描构建上下文

要扫描构建上下文，请将 `BUILDKIT_SBOM_SCAN_CONTEXT` 设置为 `true`。

```dockerfile
# syntax=docker/dockerfile:1
ARG BUILDKIT_SBOM_SCAN_CONTEXT=true
FROM alpine AS build
# ...
```

你可以使用 `--build-arg` CLI 选项来覆盖 Dockerfile 中指定的值。

```console
$ docker buildx build --tag <image>:<version> \
    --attest type=sbom \
    --build-arg BUILDKIT_SBOM_SCAN_CONTEXT=false .
```

请注意，仅作为 CLI 参数传递该选项，而未在 Dockerfile 中使用 `ARG` 声明它，将不会产生任何效果。
你必须在 Dockerfile 中指定 `ARG`，然后才能使用 `--build-arg` 覆盖上下文扫描行为。

### 扫描阶段

要扫描除最终阶段之外的更多阶段，请将 `BUILDKIT_SBOM_SCAN_STAGE` 参数设置为 true，可以是全局设置，
也可以在你想要扫描的特定阶段中设置。下表展示了该参数的不同可能设置。

| 值                                        | 描述                                          |
| ---------------------------------------- | -------------------------------------------- |
| `BUILDKIT_SBOM_SCAN_STAGE=true`          | 启用当前阶段的扫描                           |
| `BUILDKIT_SBOM_SCAN_STAGE=false`         | 禁用当前阶段的扫描                           |
| `BUILDKIT_SBOM_SCAN_STAGE=base,bin`      | 启用对名为 `base` 和 `bin` 的阶段的扫描      |

只有被构建的阶段才会被扫描。不是目标阶段依赖项的阶段不会被构建，也不会被扫描。

以下 Dockerfile 示例使用多阶段构建，通过 [Hugo](https://gohugo.io/) 构建静态网站。

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine as hugo
ARG BUILDKIT_SBOM_SCAN_STAGE=true
WORKDIR /src
COPY <<config.yml ./
title: My Hugo website
config.yml
RUN apk add --upgrade hugo && hugo

FROM scratch
COPY --from=hugo /src/public /
```

在 `hugo` 阶段设置 `ARG BUILDKIT_SBOM_SCAN_STAGE=true`，可确保最终 SBOM 包含
Alpine Linux 和 Hugo 被用于创建该网站的信息。

使用 `local` 导出器构建此镜像会创建两个 JSON 文件：

```console
$ docker buildx build \
  --sbom=true \
  --output type=local,dest=out .
$ ls -1 out | grep sbom
sbom-hugo.spdx.json
sbom.spdx.json
```

## 检查 SBOM

要探索通过 `image` 导出器导出的已创建 SBOM，你可以使用
[`imagetools inspect`](/reference/cli/docker/buildx/imagetools/inspect/)。

使用 `--format` 选项，你可以指定输出的模板。所有与 SBOM 相关的数据都可从
`.SBOM` 属性下获取。例如，要获取 SPDX 格式 SBOM 的原始内容：

```console
$ docker buildx imagetools inspect <namespace>/<image>:<version> \
    --format "{{ json .SBOM.SPDX }}"
{
  "SPDXID": "SPDXRef-DOCUMENT",
  ...
}
```

> [!TIP]
>
> 如果镜像是多平台的，你可以使用 `--format '{{ json (index .SBOM "linux/amd64").SPDX }}'` 检查
> 特定平台索引的 SBOM。

你也可以利用 Go 模板的完整功能构建更复杂的表达式。例如，你可以列出所有已安装的包及其版本标识符：

```console
$ docker buildx imagetools inspect <namespace>/<image>:<version> \
    --format "{{ range .SBOM.SPDX.packages }}{{ .name }}@{{ .versionInfo }}{{ println }}{{ end }}"
adduser@3.118ubuntu2
apt@2.0.9
base-files@11ubuntu5.6
base-passwd@3.5.47
...
```

## SBOM 生成器

BuildKit 使用扫描器插件生成 SBOM。默认情况下，它使用
[BuildKit Syft scanner](https://github.com/docker/buildkit-syft-scanner) 插件。该插件构建于
[Anchore 的 Syft](https://github.com/anchore/syft) 之上，后者是一个用于生成 SBOM 的开源工具。

你可以使用 `generator` 选项选择不同的插件，指定一个实现了
[BuildKit SBOM scanner protocol](https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md)
的镜像。

```console
$ docker buildx build --attest type=sbom,generator=<image> .
```

> [!TIP]
>
> Docker Scout SBOM 生成器可用。请参阅
> [Docker Scout SBOMs](/manuals/scout/how-tos/view-create-sboms.md)。

## SBOM 证明示例

以下 JSON 示例展示了一个 SBOM 证明可能的样子。

```json
{
  "_type": "https://in-toto.io/Statement/v0.1",
  "predicateType": "https://spdx.dev/Document",
  "subject": [
    {
      "name": "pkg:docker/<registry>/<image>@<tag/digest>?platform=<platform>",
      "digest": {
        "sha256": "e8275b2b76280af67e26f068e5d585eb905f8dfd2f1918b3229db98133cb4862"
      }
    }
  ],
  "predicate": {
    "SPDXID": "SPDXRef-DOCUMENT",
    "creationInfo": {
      "created": "2022-12-16T15:27:25.517047753Z",
      "creators": ["Organization: Anchore, Inc", "Tool: syft-v0.60.3"],
      "licenseListVersion": "3.18"
    },
    "dataLicense": "CC0-1.0",
    "documentNamespace": "https://anchore.com/syft/dir/run/src/core/sbom-cba61a72-fa95-4b60-b63f-03169eac25ca",
    "name": "/run/src/core/sbom",
    "packages": [
      {
        "SPDXID": "SPDXRef-b074348b8f56ea64",
        "downloadLocation": "NOASSERTION",
        "externalRefs": [
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:org:repo:\\(devel\\):*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "PACKAGE_MANAGER",
            "referenceLocator": "pkg:golang/github.com/org/repo@(devel)",
            "referenceType": "purl"
          }
        ],
        "filesAnalyzed": false,
        "licenseConcluded": "NONE",
        "licenseDeclared": "NONE",
        "name": "github.com/org/repo",
        "sourceInfo": "acquired package info from go module information: bin/server",
        "versionInfo": "(devel)"
      },
      {
        "SPDXID": "SPDXRef-1b96f57f8fed62d8",
        "checksums": [
          {
            "algorithm": "SHA256",
            "checksumValue": "0c13f1f3c1636491f716c2027c301f21f9dbed7c4a2185461ba94e3e58443408"
          }
        ],
        "downloadLocation": "NOASSERTION",
        "externalRefs": [
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go-chi:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go_chi:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "SECURITY",
            "referenceLocator": "cpe:2.3:a:go:chi\\/v5:v5.0.0:*:*:*:*:*:*:*",
            "referenceType": "cpe23Type"
          },
          {
            "referenceCategory": "PACKAGE_MANAGER",
            "referenceLocator": "pkg:golang/github.com/go-chi/chi/v5@v5.0.0",
            "referenceType": "purl"
          }
        ],
        "filesAnalyzed": false,
        "licenseConcluded": "NONE",
        "licenseDeclared": "NONE",
        "name": "github.com/go-chi/chi/v5",
        "sourceInfo": "acquired package info from go module information: bin/server",
        "versionInfo": "v5.0.0"
      }
    ],
    "relationships": [
      {
        "relatedSpdxElement": "SPDXRef-1b96f57f8fed62d8",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-043f7360d3c66bc31ba45388f16423aa58693289126421b71d884145f8837fe1"
      },
      {
        "relatedSpdxElement": "SPDXRef-b074348b8f56ea64",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-043f7360d3c66bc31ba45388f16423aa58693289126421b71d884145f8837fe1"
      }
    ],
    "spdxVersion": "SPDX-2.2"
  }
}
```

