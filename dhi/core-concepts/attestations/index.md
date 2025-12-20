# 证明

Docker Hardened Images (DHIs) 和 Helm chart 包含全面的签名安全证明，用于验证镜像的构建过程、内容和安全状况。这些证明是安全软件供应链实践的核心部分，有助于用户验证镜像是否可信且符合策略。

## 什么是证明？

证明是一种签名声明，提供关于镜像或 chart 的可验证信息，例如它是如何构建的、包含什么内容以及通过了哪些安全检查。证明通常使用 Sigstore 工具（如 Cosign）进行签名，使其具有防篡改性和可加密验证性。

证明遵循标准化格式（如 [in-toto](https://in-toto.io/)、[CycloneDX](https://cyclonedx.org/) 和 [SLSA](https://slsa.dev/)），并以符合 OCI 标准的元数据形式附加到镜像或 chart 上。它们可以在镜像构建期间自动生成，也可以手动添加，以记录额外的测试、扫描结果或自定义来源信息。

## 为什么证明很重要？

证明通过以下方式提供对软件供应链的关键可见性：

- 记录镜像中包含的*内容*（例如 SBOM）
- 验证镜像的*构建方式*（例如构建来源）
- 记录镜像*通过或未通过的安全扫描*（例如 CVE 报告、密钥扫描、测试结果）
- 帮助组织执行合规性和安全策略
- 支持运行时信任决策和 CI/CD 策略门控

它们对于满足 SLSA 等行业标准至关重要，并通过使构建和安全数据透明且可验证，帮助团队降低供应链攻击的风险。

## Docker Hardened Images 和 chart 如何使用证明

所有 DHIs 和 chart 均使用 [SLSA Build Level 3](https://slsa.dev/spec/latest/levels) 实践构建，每个镜像变体在发布时都附带一套完整的签名证明。这些证明允许用户：

- 验证镜像或 chart 是否在安全环境中从可信来源构建
- 以多种格式查看 SBOM，以了解组件级详细信息
- 查看扫描结果，检查是否存在漏洞或嵌入的密钥
- 确认每个镜像的构建和部署历史

证明会自动发布并与每个 DHI 和 chart 关联。可以使用 [Docker Scout](../how-to/verify.md) 或 [Cosign](https://docs.sigstore.dev/cosign/overview) 等工具检查这些证明，并可由 CI/CD 工具或安全平台使用。

## 镜像证明

虽然每个 DHI 变体都包含一组证明，但证明可能因镜像变体而异。例如，某些镜像可能包含 STIG 扫描证明。下表列出了所有可能包含在 DHI 中的证明。要查看特定镜像变体的可用证明，可以在 Docker Hub 中[查看镜像变体详细信息](../how-to/explore.md#view-image-variant-details)。

| 证明类型                   | 描述                                                                                                                                                                                                                     | 谓词类型 URI                                 |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| CycloneDX SBOM             | 以 [CycloneDX](https://cyclonedx.org/) 格式提供的软件物料清单，列出组件、库和版本。                                                                                                      | `https://cyclonedx.org/bom/v1.6`                  |
| STIG 扫描                  | STIG 扫描结果，以 HTML 和 XCCDF 格式输出。                                                                                                                           | `https://docker.com/dhi/stig/v0.1`                |
| CVEs (In-Toto 格式)        | 基于包和发行版扫描，列出影响镜像组件的已知漏洞（CVEs）。                                                                           | `https://in-toto.io/attestation/vulns/v0.1`       |
| VEX                        | [Vulnerability Exploitability eXchange (VEX)](https://openvex.dev/) 文档，识别不适用于镜像的漏洞并解释原因（例如不可达或不存在）。                         | `https://openvex.dev/ns/v0.2.0`                   |
| Scout 健康评分             | Docker Scout 提供的签名证明，总结镜像的整体安全性和质量状况。                                                                           | `https://scout.docker.com/health/v0.1`            |
| Scout 来源                 | Docker Scout 生成的来源元数据，包括源 Git 提交、构建参数和环境详细信息。                                                               | `https://scout.docker.com/provenance/v0.1`        |
| Scout SBOM                 | Docker Scout 生成并签名的 SBOM，包含额外的 Docker 特定元数据。                                                                                             | `https://scout.docker.com/sbom/v0.1`              |
| 密钥扫描                   | 扫描意外包含的密钥（如凭据、令牌或私钥）的结果。                                                                                       | `https://scout.docker.com/secrets/v0.1`           |
| 测试                       | 针对镜像运行的自动化测试记录，例如功能检查或验证脚本。                                                                                      | `https://scout.docker.com/tests/v0.1`             |
| 病毒扫描                   | 对镜像层执行的反病毒扫描结果。                                                                                                                                 | `https://scout.docker.com/virus/v0.1`             |
| CVEs (Scout 格式)          | Docker Scout 生成的漏洞报告，列出已知 CVEs 和严重性数据。                                                                                                  | `https://scout.docker.com/vulnerabilities/v0.1`   |
| SLSA 来源                  | 标准 [SLSA](https://slsa.dev/) 来源声明，描述镜像的构建方式，包括构建工具、参数和源。                                               | `https://slsa.dev/provenance/v0.2`                |
| SLSA 验证摘要              | 总结证明，表明镜像符合 SLSA 要求。                                                                                                          | `https://slsa.dev/verification_summary/v1`        |
| SPDX SBOM                  | [SPDX](https://spdx.dev/) 格式的 SBOM，在开源生态系统中广泛采用。                                                                                                   | `https://spdx.dev/Document`                       |
| FIPS 合规性                | 验证镜像使用 FIPS 140 验证的加密模块的证明。                              | `https://docker.com/dhi/fips/v0.1`                |
| DHI 镜像源                 | 指向包含构建镜像所用所有材料的对应源镜像的链接，包括包源代码、git 仓库和本地文件，确保符合开源许可证要求。 | `https://docker.com/dhi/source/v0.1`              |

## Helm chart 证明

Docker Hardened Image (DHI) chart 也包含全面的签名证明，为您的 Kubernetes 部署提供透明度和验证。与 DHI 容器镜像一样，这些 chart 遵循 SLSA Build Level 3 实践构建，并包含广泛的安全元数据。

DHI Helm chart 包含以下证明：

| 证明类型                   | 描述                                                                                                                                                                                                                     | 谓词类型 URI                                 |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
| CycloneDX SBOM             | 以 [CycloneDX](https://cyclonedx.org/) 格式提供的软件物料清单，列出 chart 本身以及 chart 引用的所有容器镜像和工具。                                                              | `https://cyclonedx.org/bom/v1.6`                  |
| CVEs (In-Toto 格式)        | 列出影响 chart 引用的容器镜像和组件的已知漏洞（CVEs）。                                                                                                                   | `https://in-toto.io/attestation/vulns/v0.1`       |
| Scout 健康评分             | Docker Scout 提供的签名证明，总结 chart 及其引用镜像的整体安全性和质量状况。                                                                                        | `https://scout.docker.com/health/v0.1`            |
| Scout 来源                 | Docker Scout 生成的来源元数据，包括 chart 源仓库、使用的构建镜像和构建参数。                                                                                                  | `https://scout.docker.com/provenance/v0.1`        |
| Scout SBOM                 | Docker Scout 生成并签名的 SBOM，包含 chart 及其引用的容器镜像，并带有额外的 Docker 特定元数据。                                                                                | `https://scout.docker.com/sbom/v0.1`              |
| 密钥扫描                   | 扫描 chart 包中意外包含的密钥（如凭据、令牌或私钥）的结果。                                                                                                       | `https://scout.docker.com/secrets/v0.1`           |
| 测试                       | 针对 chart 运行的自动化测试记录，以验证功能性和与引用镜像的兼容性。                                                                                                          | `https://scout.docker.com/tests/v0.1`             |
| 病毒扫描                   | 对 chart 包执行的反病毒扫描结果。                                                                                                                                                                     | `https://scout.docker.com/virus/v0.1`             |
| CVEs (Scout 格式)          | Docker Scout 生成的漏洞报告，列出 chart 引用镜像的已知 CVEs 和严重性数据。                                                                                                      | `https://scout.docker.com/vulnerabilities/v0.1`   |
| SLSA 来源                  | 标准 [SLSA](https://slsa.dev/) 来源声明，描述 chart 的构建方式，包括构建工具、源仓库、引用镜像和构建材料。                                                 | `https://slsa.dev/provenance/v0.2`                |
| SPDX SBOM                  | [SPDX](https://spdx.dev/) 格式的 SBOM，列出 chart 及其引用的所有容器镜像和工具。                                                                                                              | `https://spdx.dev/Document`                       |

有关如何查看和验证 Helm chart 证明的说明，请参阅[验证 Helm chart 证明](../how-to/verify.md#verify-helm-chart-attestations-with-docker-scout)。

## 查看和验证证明

要查看和验证证明，请参阅[验证 Docker Hardened Image](../how-to/verify.md)。

## 添加您自己的证明

除了 Docker Hardened Images 提供的全面证明外，您还可以在构建派生镜像时添加自己的签名证明。如果您在 DHI 之上构建新应用程序，并希望保持软件供应链的透明度、可追溯性和信任，这尤其有用。

通过附加 SBOM、构建来源或自定义元数据等证明，您可以满足合规性要求、通过安全审计，并支持 Docker Scout 等策略评估工具。

这些证明随后可以使用 Cosign 或 Docker Scout 等工具在下游进行验证。

要了解如何在构建过程中附加自定义证明，请参阅[构建证明](/manuals/build/metadata/attestations.md)。
