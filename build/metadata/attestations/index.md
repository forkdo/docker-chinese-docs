# 构建证明（Build attestations）




构建证明描述了一个镜像是如何构建的，以及它包含什么。这些证明在构建时由 BuildKit
创建，并作为元数据附加到最终镜像上。

证明的目的是让你能够检查一个镜像，了解它来自何处、由谁以及如何创建，以及它包含什么。
这使你能够就一个镜像如何影响应用程序的软件供应链安全性做出明智的决策。它还支持使用
策略引擎根据你定义的策略规则来验证镜像。

有两种类型的构建证明可用：

- 软件物料清单（SBOM）：一个镜像所包含、或用于构建该镜像的软件构件列表。
- 来源（Provenance）：一个镜像是如何构建的。

## 证明的目的

如今，使用开源和第三方软件包比以往任何时候都更加普遍。开发者共享和重用代码，因为这有助于
提高生产力，使团队能够更快、更好地创造产品。

在未经审查的情况下导入和使用别处创建的代码，会引入严重的安全风险。即使你审查了所消费的软件，
新的零日漏洞也经常被披露，要求开发团队采取行动予以修复。

构建证明让查看镜像的内容及其来源变得更加容易。使用证明来分析并决定是否使用一个镜像，或查看
你正在使用的镜像是否暴露于漏洞之中。

## 创建证明

BuildKit 在构建镜像时生成证明。默认情况下，`mode=min` 级别的来源证明会被添加到镜像中。
证明记录被封装在 in-toto JSON 格式中，并作为最终镜像的清单附加到镜像索引（image index）上。

你可以使用 `--provenance` 和 `--sbom` 标志自定义证明行为：

```bash
# Opt in to SBOM attestations:
docker buildx build --sbom=true .
# Opt in to max-level provenance attestations:
docker buildx build --provenance=mode=max .
# Opt out of provenance attestations:
docker buildx build --provenance=false .
```

你也可以通过设置
[`BUILDX_NO_DEFAULT_ATTESTATIONS`](/manuals/build/building/variables.md#buildx_no_default_attestations)
环境变量来禁用默认的来源证明。有关来源模式和选项的更多详细信息，请参阅
[来源证明](./slsa-provenance.md)。

### 驱动与镜像存储支持

证明附加到镜像索引上。经典镜像存储不支持镜像索引，因此它无法保存带有证明的镜像。

默认的 `docker` 驱动使用捆绑在 Docker 守护进程中的 BuildKit 库进行构建，并将结果写入守护进程的
镜像存储。如果守护进程仍使用经典镜像存储，构建将失败：

```text
ERROR: failed to build: Attestation is not supported for the docker driver.
Switch to a different driver, or turn on the containerd image store, and try again.
```

要使用 `docker` 驱动构建证明，请打开 containerd 镜像存储。请参阅
[Docker Desktop 中的 containerd 镜像存储](/manuals/desktop/features/containerd.md)
或 [Docker Engine 中的 containerd 镜像存储](/manuals/engine/storage/containerd.md)。

| 驱动                         | 证明支持                            |
| :-------------------------- | :---------------------------------- |
| `docker`                    | 需要 containerd 镜像存储            |
| `docker-container`          | 支持                                |
| `kubernetes` 和 `remote`    | 支持                                |

`docker-container`、`kubernetes` 和 `remote` 驱动在 Docker 守护进程之外运行 BuildKit，
因此它们无论守护进程使用哪种镜像存储都会构建证明。使用 `--push` 将结果推送到镜像仓库会保留
证明。如果你改用 `--load` 将结果加载到守护进程中，则同样的镜像存储要求仍然适用。

如果你不想切换镜像存储或驱动，请使用 `--provenance=false --sbom=false` 退出证明。

## 存储

BuildKit 以 [in-toto 格式](https://github.com/in-toto/attestation) 生成证明，
该格式由 [in-toto 框架](https://in-toto.io/) 定义，这是一个由 Linux Foundation 支持的标准。

证明作为镜像索引中的一个清单附加到镜像上。证明的数据记录以 JSON blob 的形式存储。

由于证明作为清单附加到镜像上，这意味着你可以在不拉取整个镜像的情况下检查镜像仓库中
任意镜像的证明。

所有 BuildKit 导出器都支持证明。`local` 和 `tar` 无法将证明保存到镜像清单中，因为它们输出的是
文件目录或 tarball，而不是镜像。相反，这些导出器会将证明写入导出根目录下的一个或多个 JSON 文件。

## 示例

以下示例展示了一个截断的 SBOM 证明的 in-toto JSON 表示形式。

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
      "created": "2022-12-15T11:47:54.546747383Z",
      "creators": ["Organization: Anchore, Inc", "Tool: syft-v0.60.3"],
      "licenseListVersion": "3.18"
    },
    "dataLicense": "CC0-1.0",
    "documentNamespace": "https://anchore.com/syft/dir/run/src/core-da0f600b-7f0a-4de0-8432-f83703e6bc4f",
    "name": "/run/src/core",
    // list of files that the image contains, e.g.:
    "files": [
      {
        "SPDXID": "SPDXRef-1ac501c94e2f9f81",
        "comment": "layerID: sha256:9b18e9b68314027565b90ff6189d65942c0f7986da80df008b8431276885218e",
        "fileName": "/bin/busybox",
        "licenseConcluded": "NOASSERTION"
      }
    ],
    // list of packages that were identified for this image:
    "packages": [
      {
        "name": "busybox",
        "originator": "Person: Sören Tempel <soeren+alpine@soeren-tempel.net>",
        "sourceInfo": "acquired package info from APK DB: lib/apk/db/installed",
        "versionInfo": "1.35.0-r17",
        "SPDXID": "SPDXRef-980737451f148c56",
        "description": "Size optimized toolbox of many common UNIX utilities",
        "downloadLocation": "https://busybox.net/",
        "licenseConcluded": "GPL-2.0-only",
        "licenseDeclared": "GPL-2.0-only"
        // ...
      }
    ],
    // files-packages relationship
    "relationships": [
      {
        "relatedSpdxElement": "SPDXRef-1ac501c94e2f9f81",
        "relationshipType": "CONTAINS",
        "spdxElementId": "SPDXRef-980737451f148c56"
      },
      ...
    ],
    "spdxVersion": "SPDX-2.2"
  }
}
```

要深入了解证明如何存储的具体细节，请参阅
[Image Attestation Storage (BuildKit)](attestation-storage.md)。

## 证明清单格式

证明作为清单存储，由镜像的索引引用。每个_证明清单_（attestation manifest）指向一个_镜像清单_
（image manifest，即镜像的一个平台变体）。证明清单包含单个层，即证明的"值"。

以下示例展示了证明清单的结构：

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "size": 167,
    "digest": "sha256:916d7437a36dd0e258e64d9c5a373ca5c9618eeb1555e79bd82066e593f9afae"
  },
  "layers": [
    {
      "mediaType": "application/vnd.in-toto+json",
      "size": 1833349,
      "digest": "sha256:3138024b98ed5aa8e3008285a458cd25a987202f2500ce1a9d07d8e1420f5491",
      "annotations": {
        "in-toto.io/predicate-type": "https://spdx.dev/Document"
      }
    }
  ]
}
```

### 作为 OCI 制品的证明

你可以使用 `image` 和 `registry` 导出器的
[`oci-artifact` option](/manuals/build/exporters/image-registry.md#synopsis)
来配置证明清单的格式。如果设置为 `true`，证明清单的结构会如下改变：

- 一个 `artifactType` 字段被添加到证明清单，值为 `application/vnd.docker.attestation.manifest.v1+json`。
- `config` 字段是一个[空描述符]（empty descriptor），而不是一个"虚拟" config。
- 还会添加一个 `subject` 字段，指向该证明所引用的镜像清单。

[empty descriptor]: https://github.com/opencontainers/image-spec/blob/main/manifest.md#guidance-for-an-empty-descriptor

以下示例展示了一个采用 OCI 制品格式的证明：

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "artifactType": "application/vnd.docker.attestation.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.empty.v1+json",
    "size": 2,
    "digest": "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    "data": "e30="
  },
  "layers": [
    {
      "mediaType": "application/vnd.in-toto+json",
      "size": 2208,
      "digest": "sha256:6d2f2c714a6bee3cf9e4d3cb9a966b629efea2dd8556ed81f19bd597b3325286",
      "annotations": {
        "in-toto.io/predicate-type": "https://slsa.dev/provenance/v0.2"
      }
    }
  ],
  "subject": {
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "size": 1054,
    "digest": "sha256:bc2046336420a2852ecf915786c20f73c4c1b50d7803aae1fd30c971a7d1cead",
    "platform": {
      "architecture": "amd64",
      "os": "linux"
    }
  }
}
```

## 下一步

进一步了解可用的证明类型以及如何使用它们：

- [来源（Provenance）](slsa-provenance.md)
- [SBOM](sbom.md)

