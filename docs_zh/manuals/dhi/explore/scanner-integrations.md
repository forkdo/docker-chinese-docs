---
title: 扫描器集成
description: 了解哪些漏洞扫描器适用于 Docker Hardened Images，以及如何选择合适的扫描器以进行准确的漏洞评估。
keywords: scanner integration, vulnerability scanning, docker scout, trivy, grype, wiz, black duck, aikido, aws inspector, container security scanners
weight: 40
---

Docker Hardened Images (DHI) 可与多种漏洞扫描器配合使用。然而，要获得准确反映这些镜像实际安全状况的结果，您的扫描器需要理解每个镜像附带的 VEX（漏洞可利用性交换）证明。

## 支持 VEX 的扫描器

以下扫描器可以读取并应用 Docker Hardened Images 附带的 VEX 证明：

| 扫描器 | VEX 应用方式 |
|---------|-----------------|
| [Docker Scout](/scout/) | 自动应用，零配置 |
| [Trivy](https://trivy.dev/) | VEX Hub（推荐）或本地 VEX 文件 |
| [Grype](https://github.com/anchore/grype) | 通过 `--vex` 标志配合本地 VEX 文件 |
| [Wiz](https://docs.wiz.io/) | 自动应用，零配置 |
| [Mend.io](https://docs.mend.io/platform/latest/docker-hardened-images) | 自动应用，零配置 |
| [Black Duck](https://documentation.blackduck.com/bundle/bd-hub/page/Reporting/vexReport_global.html) | 自动应用，零配置 |
| [Aikido](https://help.aikido.dev/container-image-scanning/standalone-registries/docker-hub-images) | 自动应用，零配置 |
| [AWS Inspector](https://docs.aws.amazon.com/inspector/latest/user/supported.html) | 自动应用，零配置 |

有关 Docker Scout、Trivy 和 Grype 的分步说明，请参阅[扫描 Docker Hardened Images](/manuals/dhi/how-to/scan.md)。对于 Wiz、Mend.io、Black Duck、Aikido 和 AWS Inspector，请参阅其各自的文档。

## 为 Docker Hardened Images 选择扫描器

在为 Docker Hardened Images 选择扫描器时，是否支持 OpenVEX 等开放标准是关键的区分因素。

Docker Hardened Images 包含遵循 [OpenVEX 标准](https://openvex.dev/)的签名 VEX 证明。OpenVEX 是一种开放标准，满足 CISA（网络安全和基础设施安全局，负责网络安全指导的美国政府机构）定义的 VEX 最低要求。这些证明记录了哪些漏洞不适用于该镜像以及原因，帮助您专注于真正的风险。

要了解 VEX 是什么及其工作原理，请参阅 [VEX 核心概念](/manuals/dhi/explore/security-concepts/vex.md)。

由于 OpenVEX 是获得政府支持的开放标准，它具有强大的行业推动力，任何工具都可以实现它，无需特定于供应商的集成。当您引入使用自有扫描工具的第三方审计人员，或希望在流水线中使用多种安全工具时，这一点很重要。借助 VEX，这些工具都可以直接从您的镜像中读取和验证相同的漏洞数据。

如果没有 VEX 这样的开放标准，供应商会使用专有方法做出可利用性决策，这使得验证声明或跨工具比较结果变得困难。这会使您的安全工具链碎片化，并在不同扫描工具之间产生不一致的漏洞评估。

### 支持 VEX 的扫描器的优势

支持 OpenVEX 等开放标准并能解读 Docker Hardened Images 中 VEX 证明的扫描器提供以下优势：

- **准确的漏洞计数**：自动过滤掉不适用于您特定镜像的漏洞，通常能显著减少误报。
- **透明度和可审计性**：准确验证漏洞被标记或未被标记的原因；安全团队和合规官员可以审查推理过程，而不是信任供应商的黑盒。
- **扫描器灵活性**：在任何支持 VEX 的扫描器（Docker Scout、Trivy、Grype 等）之间切换，而不会丢失漏洞上下文或需要重建排除列表。
- **一致的结果**：支持 VEX 的扫描器以相同的方式解读相同的数据，消除工具之间的差异。
- **更快的工作流程**：专注于真正的风险，而不是研究报告的 CVE 为何实际上不影响您的部署。

### 不支持 VEX 的扫描器

无法读取 VEX 证明的扫描器会报告不适用于 Docker Hardened Images 的漏洞。这会带来运营挑战：

- **需要手动过滤**：您需要维护特定于扫描器的忽略列表，以复制 VEX 声明已经记录的内容。
- **更高的误报率**：预计会看到更多不代表实际风险的报告漏洞。
- **增加调查时间**：安全团队花费时间研究 CVE 为何不适用，而不是处理实际的漏洞。对于 Docker Hardened Images，Docker 的安全专家会为您管理这项调查，在将每个理由添加到 VEX 声明之前进行彻底审查。
- **CI/CD 摩擦**：构建流水线可能因镜像中不可利用的漏洞而失败。

### 基于 VEX 的漏洞处理与专有方法的对比

Docker Hardened Images 使用基于 OpenVEX 开放标准的 VEX 证明来记录漏洞可利用性。OpenVEX 是获得 CISA 等政府机构认可的开放标准。这种开放标准方法与某些其他镜像供应商使用专有方法处理漏洞的方式不同。

#### 使用 VEX 的 Docker Hardened Images

镜像包含签名证明，解释哪些漏洞不适用以及原因。任何支持 VEX 的扫描器都可以读取这些证明，为您提供：

- **工具灵活性**：使用任何支持 OpenVEX 的扫描器（Docker Scout、Trivy、Grype 等）
- **完全透明**：审查每个漏洞评估的确切推理
- **完全可审计**：安全团队和合规官员可以独立验证所有漏洞评估和推理
- **历史可见性**：VEX 声明随镜像保留，因此您始终可以检查漏洞状态，即使是旧版本

#### 专有漏洞处理

某些镜像供应商使用专有咨询源或内部数据库，而不是 VEX。虽然这可能导致报告的漏洞更少，但它带来了重大限制：

- **工具依赖性**：您必须使用供应商首选的扫描工具才能看到他们的漏洞过滤，而标准扫描器仍会报告所有 CVE；扫描器必须实现专有源，而不是使用适用于所有镜像的开放标准
- **缺乏透明度**：专有源充当"黑盒"——漏洞从供应商工具中消失，没有任何解释
- **可验证性有限**：安全团队无法独立验证漏洞被排除的原因或推理是否合理
- **维护挑战**：如果您使用标准工具扫描旧版本的镜像，您无法确定当时实际适用哪些漏洞，这使得长期安全跟踪变得困难
- **生态系统不兼容**：您现有的安全工具（SCA、策略引擎、合规扫描器）无法访问或验证供应商的专有漏洞数据

根本区别：基于 VEX 的方法使用任何工具都可以验证和审计的开放标准来解释漏洞评估。专有方法将漏洞隐藏在供应商特定的系统中，其推理无法被独立验证。

对于 Docker Hardened Images，请使用支持 VEX 的扫描器，以获得在整个安全工具链中都能正常工作的准确结果。

## 不同扫描器的预期结果

使用不同工具扫描 Docker Hardened Images 时，您会看到报告的漏洞数量存在显著差异。

### 支持 VEX 的扫描器自动过滤的内容

使用支持 VEX 的扫描器扫描 Docker Hardened Images 时，它们会自动排除不适用的漏洞：

- **特定于硬件的漏洞**：仅影响特定硬件架构（例如 Power10 处理器）的问题，这些问题与容器化工作负载无关。
- **不可达的代码路径**：存在于包中但在镜像运行时配置中未执行的代码中的 CVE。
- **仅构建时的问题**：构建工具或依赖项中的漏洞，这些工具或依赖项在最终的运行时镜像中不存在。
- **临时标识符**：不用于外部跟踪的占位符漏洞 ID（如 Debian 的 `TEMP-xxxxxxx`）。

### 使用不支持 VEX 的扫描器

如果您的扫描器不支持 VEX，您需要通过扫描器特定的机制（如忽略列表或策略例外）手动排除漏洞。这需要：

- 审查来自 Docker Hardened Images 的 VEX 声明
- 将 VEX 理由转换为您的扫描器格式
- 随着新漏洞的发现维护这些排除项
- 如果您更换扫描器或添加额外的扫描工具，则重复此过程

## 下一步

了解如何使用支持 VEX 的扫描器[扫描 Docker Hardened Images](/manuals/dhi/how-to/scan.md)。
