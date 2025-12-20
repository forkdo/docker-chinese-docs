# 软件物料清单

<div id="youtube-player-PbS4y7C7h4A" data-video-id="PbS4y7C7h4A" class="youtube-video aspect-video h-fit w-full py-2">
</div>


物料清单（BOM）是制造产品所需的材料、零件及其数量的列表。例如，计算机的 BOM 可能会列出主板、CPU、RAM、电源、存储设备、机箱和其他组件，以及构建计算机所需的每种组件的数量。

软件物料清单（SBOM）是构成软件的所有组件的列表。这包括开源和第三方组件，以及为该软件编写的任何自定义代码。SBOM 类似于物理产品的 BOM，但适用于软件。

在软件供应链安全的背景下，SBOM 可以帮助识别和减轻软件中的安全和合规风险。通过确切了解软件中使用的组件，您可以快速识别并修补组件中的漏洞，或者确定组件的许可方式是否与您的项目不兼容。

## SBOM 的内容

SBOM 通常包括以下信息：

- SBOM 所描述的软件名称，例如库或框架的名称。
- 软件的版本。
- 软件分发的许可证。
- 该软件依赖的其他组件列表。

## Docker Scout 如何使用 SBOM

Docker Scout 使用 SBOM 来确定 Docker 镜像中使用的组件。当您分析镜像时，Docker Scout 会使用附加到镜像作为证明（attestation）的 SBOM，或者通过分析镜像内容即时生成 SBOM。

SBOM 会与[建议数据库](/manuals/scout/deep-dive/advisory-db-sources.md)进行交叉引用，以确定镜像中的任何组件是否存在已知漏洞。

<div id="scout-lp-survey-anchor"></div>
