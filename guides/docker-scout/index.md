# 使用 Docker Scout 保护你的软件供应链



当容器镜像不安全时，会产生巨大的风险。约 60% 的组织报告称，在一年内至少经历过一次安全漏洞或漏洞事件，[导致运营中断][CSA]。这些事件常常造成可观的停机时间，44% 的受影响公司每次事件都会经历超过一小时的停机。其财务影响是巨大的，[平均数据泄露成本高达 450 万美元][IBM]。这凸显了维护强有力容器安全措施的极端重要性。

Docker Scout 通过提供自动化的漏洞检测与修复、处理不安全的容器镜像、并确保符合安全标准来增强容器安全性。

[CSA]: https://cloudsecurityalliance.org/blog/2023/09/21/2023-global-cloud-threat-report-cloud-attacks-are-lightning-fast
[IBM]: https://www.ibm.com/reports/data-breach

## 你将学到什么

- 定义安全软件供应链（SSSC）
- 回顾 SBOM 以及如何使用它们
- 检测并监控漏洞

## 工具集成

与 Docker Desktop、GitHub Actions、Jenkins、Kubernetes 以及其他 CI 解决方案配合良好。

## 适用对象

- 需要将自动化安全检查集成到 CI/CD 流水线中，以增强工作流安全性和效率的 DevOps 工程师。
- 希望在开发过程早期使用 Docker Scout 识别并修复漏洞，从而确保生产出安全容器镜像的开发者。
- 必须强制执行安全合规性、开展漏洞评估，并确保容器化应用整体安全的安全专业人员。

<div id="scout-lp-survey-anchor"></div>

## 为何选择 Docker Scout？



组织面临着数据泄露带来的重大挑战，包括财务损失、运营中断，以及对品牌声誉和客户信任的长期损害。Docker Scout 解决的关键问题包括识别不安全的容器镜像、防止安全漏洞，以及降低因漏洞导致运营停机的风险。

Docker Scout 提供了多项好处：

- 安全且可信的内容
- 软件开发生命周期（SDLC）的记录系统
- 持续的安全态势改进

Docker Scout 提供自动化的漏洞检测与修复，帮助组织在开发过程早期识别并修复容器镜像中的安全问题。它还与 Docker Desktop 和 GitHub Actions 等流行开发工具集成，在现有工作流内提供无缝的安全管理与合规检查。

<div id="scout-lp-survey-anchor"></div>

## Docker Scout 演示



Docker Scout 拥有强大的功能，可增强容器化应用的安全性并确保稳健的软件供应链。

- 定义漏洞修复
- 讨论为何修复对于维护容器化应用的安全性和完整性至关重要
- 讨论常见漏洞
- 实施修复技术：更新基础镜像、应用补丁、移除不必要的包
- 使用 Docker Scout 验证修复工作

<div id="scout-lp-survey-anchor"></div>

## 软件供应链安全



“软件供应链”一词指的是从开发到部署和维护的软件交付端到端过程。软件供应链安全，简称 “S3C”，是保护供应链组件和流程的实践。

S3C 是组织对待软件安全方式的根本性转变。在传统软件行业中，安全和合规性大多被视为事后考虑，留到软件交付或发布阶段才处理。而在 S3C 下，安全被集成到整个软件开发生命周期中，从开发与测试的内循环，到交付与监控的外循环。

遵循软件供应链行为的最佳行业实践非常重要，因为它有助于组织保护其软件免受安全威胁、合规风险和其他漏洞的影响。实施软件供应链安全框架，可提升项目在各相关方之间的可见性、协作性和可追溯性。这有助于组织更有效地检测、响应和修复威胁。

### 保护软件供应链

构建安全的软件供应链涉及几个关键步骤，例如：

- 识别你用于构建和运行应用的软件组件与依赖项。
- 在整个软件开发生命周期中自动化安全测试。
- 监控你的软件供应链以发现安全威胁。
- 实施管控软件构建方式及其所包含组件的安全策略。

管理软件供应链是一项复杂的任务，尤其是在当今软件由来自不同来源的多个组件构建而成的情况下。组织需要清楚地了解它们所使用的软件组件，以及与之相关的安全风险。

### Docker Scout 有何不同

Docker Scout 是一个旨在帮助组织保护其软件供应链的平台。它提供用于识别和管理软件资产与策略、以及自动化修复安全威胁的工具和服务。

与那些聚焦于软件开发生命周期中特定阶段、按计划进行某一时点扫描的传统安全工具不同，Docker Scout 采用一种跨越整个软件供应链的现代事件驱动模型。这意味着，当披露一个影响你镜像的新漏洞时，更新后的风险评估会在数秒内可用，并且出现在开发过程的更早期。

Docker Scout 通过分析你的镜像构成来创建软件物料清单（SBOM）。该 SBOM 会与安全公告进行交叉比对，以识别影响你镜像的 CVE。Docker Scout 集成了 [超过 20 个不同的安全公告源](/manuals/scout/deep-dive/advisory-db-sources.md)，并实时更新其漏洞数据库。这确保你的安全态势始终以最新可用信息呈现。

<div id="scout-lp-survey-anchor"></div>

## 软件物料清单



物料清单（BOM）是制造一个产品所需的材料、零件及各自数量的列表。例如，一台计算机的 BOM 可能会列出主板、CPU、内存、电源、存储设备、机箱以及其他组件，以及构建该计算机所需的各自数量。

软件物料清单（SBOM）是构成一段软件的所有组件的列表。这包括开源和第三方组件，以及为该软件编写的任何自定义代码。SBOM 类似于实体产品的 BOM，但针对的是软件。

在软件供应链安全的语境下，SBOM 有助于识别和缓解软件中的安全与合规风险。通过确切了解一段软件中使用了哪些组件，你可以快速识别并修补组件中的漏洞，或者判断某个组件的许可证是否与你的项目不兼容。

### SBOM 的内容

SBOM 通常包含以下信息：

- SBOM 所描述的软件名称，例如某个库或框架的名称。
- 软件的版本。
- 软件分发所依据的许可证。
- 该软件所依赖的其他组件列表。

### Docker Scout 如何使用 SBOM

Docker Scout 使用 SBOM 来确定 Docker 镜像中使用的组件。当你分析一个镜像时，Docker Scout 要么使用作为证明（attestation）附加到镜像上的 SBOM，要么通过分析镜像内容即时生成一个 SBOM。

该 SBOM 会与 [公告数据库](/manuals/scout/deep-dive/advisory-db-sources.md) 进行交叉比对，以确定镜像中是否有任何组件存在已知漏洞。

<div id="scout-lp-survey-anchor"></div>

## 证明



[构建证明（Build attestations）](/manuals/build/metadata/attestations/_index.md) 为你提供关于镜像如何构建及其包含内容的详细信息。这些由 BuildKit 在构建时生成的证明，会作为元数据附加到最终镜像上，使你可以检查镜像以查看其来源、创建者和内容。这些信息有助于你就镜像对你的供应链的安全性和影响做出明智决策。

Docker Scout 利用这些证明来评估镜像的安全性和供应链态势，并为相关问题提供修复建议。如果检测到问题（例如缺失或过时的证明），Docker Scout 可以指导你如何添加或更新它们，从而确保合规性并提升对镜像安全状态的可见性。

证明有两种关键类型：

- SBOM，列出镜像中的软件制品。
- Provenance（来源证明），详述镜像的构建方式。

你可以使用带有 `--provenance` 和 `--sbom` 标志的 `docker buildx build` 来创建证明。证明会附加到镜像索引上，使你可以在不拉取整个镜像的情况下检查它们。Docker Scout 利用这些元数据为你提供更精确的推荐，并更好地控制镜像的安全性。

<div id="scout-lp-survey-anchor"></div>

## 修复



Docker Scout 的 [修复功能](/manuals/scout/policy/dashboard.md) 通过基于策略评估提供量身定制的建议，帮助你解决供应链与安全问题。这些建议指引你改进策略合规性或增强镜像元数据，使 Docker Scout 在未来能够执行更准确的评估。

你可以使用此功能来确保你的基础镜像是最新的，并且你的供应链证明是完整的。当发生违规时，Docker Scout 会提供推荐的修复方案，例如更新基础镜像或添加缺失的证明。如果没有足够的信息来确定合规性，Docker Scout 会建议采取行动以帮助解决问题。

在 Docker Scout 仪表板中，你可以通过查看违规或合规性不确定项来查看这些建议并采取行动。通过 GitHub 等集成，你甚至可以实现更新自动化，直接从仪表板修复问题。

<div id="scout-lp-survey-anchor"></div>

## 常见挑战与问题

<!-- vale Docker.HeadingLength = NO -->

#### Docker Scout 与其他安全工具有何不同？

与第三方安全工具相比，Docker Scout 对容器安全采取了更广义的方法。第三方安全工具即使提供修复指导，其范围也局限于软件供应链内应用安全态势的有限部分，并且在建议修复方案时往往指导有限。这类工具要么在运行时监控方面存在局限，要么根本没有运行时保护。即便它们提供运行时监控，在遵循关键策略方面也很有限。第三方安全工具对 Docker 特定构建的策略评估范围有限。通过聚焦整个软件供应链、提供可操作的指导，并提供具有强力策略执行的全面运行时保护，Docker Scout 超越了对容器漏洞的简单识别。它帮助你从底层开始构建安全的应用。

#### 我可以在 Docker Hub 之外的外部镜像仓库中使用 Docker Scout 吗？

你可以将 Scout 用于 Docker Hub 之外的镜像仓库。将 Docker Scout 与第三方容器镜像仓库集成后，Docker Scout 就可以在这些仓库上运行镜像分析，这样即使这些镜像并非托管在 Docker Hub 上，你也能洞察其构成。

目前提供以下容器镜像仓库集成：

- Artifactory
- Amazon Elastic Container Registry
- Azure Container Registry

在 [将 Docker Scout 与第三方镜像仓库集成](/scout/integrations/#container-registries) 中了解更多关于为你的镜像仓库配置 Scout 的内容。

#### Docker Scout CLI 是否默认随 Docker Desktop 一起提供？

是的，Docker Scout CLI 插件已预装在 Docker Desktop 中。

#### 是否可以在没有 Docker Desktop 的 Linux 系统上运行 `docker scout` 命令？

如果你运行的是没有 Docker Desktop 的 Docker Engine，Docker Scout 不会预装，但你可以 [将其作为独立二进制文件安装](/scout/install/)。

#### Docker Scout 如何使用 SBOM？

SBOM（软件物料清单）是构成软件组件的原料列表。[Docker Scout 使用 SBOM](/scout/concepts/sbom/) 来确定 Docker 镜像中使用的组件。当你分析一个镜像时，Docker Scout 要么使用附加到镜像上的 SBOM（作为证明），要么通过分析镜像内容即时生成一个 SBOM。

该 SBOM 会与公告数据库进行交叉比对，以确定镜像中是否有任何组件存在已知漏洞。

<div id="scout-lp-survey-anchor"></div>

