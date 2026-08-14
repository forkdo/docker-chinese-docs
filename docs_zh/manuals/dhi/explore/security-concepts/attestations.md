---
aliases:
  - /dhi/core-concepts/attestations/
title: Attestations（证明）
description: 查看每个 Docker Hardened Image 附带的一整套已签名证明，例如 SBOM、VEX、构建来源和扫描结果。
keywords: container image attestations, signed sbom, build provenance, slsa compliance, vex document
---

Docker Hardened Images（DHI）和 chart 包含全面、已签名的安全证明，用于验证镜像的构建过程、内容和安全态势。这些证明是安全软件供应链实践的核心部分，帮助用户验证镜像是否可信且符合策略。

## What is an attestation?（什么是证明？）

证明是一份已签名的声明，提供关于镜像或 chart 的可验证信息，例如它是如何构建的、其中包含什么内容，以及它通过了哪些安全检查。证明通常使用 Sigstore 工具（如 Cosign）签名，使其具有防篡改性和加密可验证性。

证明遵循标准化格式（如 [in-toto](https://in-toto.io/)、[CycloneDX](https://cyclonedx.org/) 和 [SLSA](https://slsa.dev/)），并作为符合 OCI 规范的元数据附加到镜像或 chart 上。它们可以在镜像构建期间自动生成，或手动添加以记录额外的测试、扫描结果或自定义来源。

## Why are attestations important?（为何证明很重要？）

证明通过以下方式提供对软件供应链的关键可见性：

- 记录进入镜像的*内容*（例如 SBOM）
- 验证它是*如何*构建的（例如构建来源）
- 捕获它已通过或失败的*安全扫描*（例如 CVE 报告、密钥扫描、测试结果）
- 帮助组织强制执行合规和安全策略
- 支持运行时信任决策和 CI/CD 策略门禁

它们对于满足 SLSA 等行业标准至关重要，并通过使构建和安全数据透明且可验证，帮助团队降低供应链攻击的风险。

## How Docker Hardened Images and charts use attestations（Docker Hardened Images 和 chart 如何使用证明）

所有 DHI 和 chart 都使用 [SLSA Build Level 3](https://slsa.dev/spec/latest/levels) 实践构建，并且每个镜像变体都发布时附带一整套已签名的证明。这些证明允许用户：

- 验证镜像或 chart 是在安全环境中从受信任来源构建的
- 以多种格式查看 SBOM 以了解组件级细节
- 查看扫描结果以检查漏洞或嵌入的密钥
- 确认每个镜像的构建和部署历史

证明会自动发布并与每个 DHI 和 chart 关联。它们可以使用 [Docker Scout](../../how-to/verify.md) 或 [Cosign](https://docs.sigstore.dev/cosign/overview) 等工具检查，并可被 CI/CD 工具或安全平台消费。

## Image attestations（镜像证明）

虽然每个 DHI 变体都包含一组证明，但证明可能因镜像变体而异。例如，某些镜像可能包含 STIG 扫描证明。下表列出了可能随 DHI 一起提供的证明；实际集合因镜像变体而异。要查看特定镜像变体有哪些证明可用（包括具体的 predicate type URI），请使用 Docker Scout：

```console
$ docker scout attest list dhi.io/<image>:<tag>
```

更多详情，请参阅 [Verify image attestations](../../how-to/verify.md#verify-image-attestations)。

| 证明类型           | 描述                                                                                                                                                                                                                     |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CycloneDX SBOM             | [CycloneDX](https://cyclonedx.org/) 格式的软件物料清单，列出组件、库和版本。                                                                                                      |
| STIG scan                  | STIG 扫描结果，输出为 HTML 和 XCCDF 格式。                                                                                                                           |
| CVEs (In-Toto format)      | 基于包和发行版扫描、影响镜像组件的已知漏洞（CVE）列表。                                                                           |
| VEX                        | [Vulnerability Exploitability eXchange (VEX)](https://openvex.dev/) 文档，识别不适用于该镜像的漏洞并解释原因（例如不可达或不存在）。                         |
| Scout provenance           | 由 Docker Scout 生成的来源元数据，包括源 Git commit、构建参数和环境细节。                                                               |
| Scout SBOM                 | 由 Docker Scout 生成并签名的 SBOM，包含额外的 Docker 特定元数据。                                                                                             |
| Secrets scan               | 针对意外包含的密钥（如凭据、令牌或私钥）的扫描结果。                                                                                       |
| Tests                      | 针对镜像运行的自动化测试记录，例如功能检查或验证脚本。                                                                                      |
| Virus scan                 | 对镜像层执行的防病毒扫描结果。详情请参阅 [Malware scanning](../malware-scanning.md)。                                                            |
| CVEs (Scout format)        | 由 Docker Scout 生成的漏洞报告，列出已知 CVE 和严重性数据。                                                                                                  |
| SLSA provenance            | 标准的 [SLSA](https://slsa.dev/) 来源声明，描述镜像的构建方式，包括构建工具、参数和来源。                                               |
| SLSA verification summary  | 表明镜像符合 SLSA 要求的摘要证明。                                                                                                          |
| SPDX SBOM                  | [SPDX](https://spdx.dev/) 格式的 SBOM，在开源生态系统中被广泛采用。                                                                                                   |
| FIPS compliance            | 验证镜像使用经过 FIPS 140 验证的加密模块的证明。                              |
| DHI Changelog              | 跨版本对镜像所做更改的记录。 |
| DHI Image Sources          | 链接到包含构建镜像所用全部材料的相应源镜像，包括包源代码、Git 仓库和本地文件，确保符合开源许可证要求。 |

## Package attestations（包证明）

除了镜像级证明外，Docker 加固包还包含它们自己的证明。这些包级证明为镜像中的各个包提供来源和构建信息，让你可以细粒度地追踪供应链。

包证明包含与镜像证明类似的信息，例如 SLSA 来源，显示每个包是如何构建的以及使用了哪些材料。你可以从镜像的证明中提取包信息，然后递归检索包自身的证明。

有关如何访问和验证包证明的详细说明，请参阅 [Package attestations](../../how-to/hardened-packages.md#package-attestations)。

## Helm chart attestations（Helm chart 证明）

Docker Hardened Image（DHI）chart 还包含全面的已签名证明，为你的 Kubernetes 部署提供透明度和验证。与 DHI 容器镜像一样，这些 chart 遵循 SLSA Build Level 3 实践构建，并包含广泛的安全元数据。

DHI Helm chart 包含以下证明。要查看这些证明的具体 predicate type URI，请使用 Docker Scout：

```console
$ docker scout attest list dhi.io/<chart>:<version>
```

更多详情，请参阅 [Verify Helm chart attestations](../../how-to/verify.md#verify-helm-chart-attestations-with-docker-scout)。

| 证明类型           | 描述                                                                                                                                                                                                                     |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CycloneDX SBOM             | [CycloneDX](https://cyclonedx.org/) 格式的软件物料清单，列出 chart 本身以及 chart 引用的所有容器镜像和工具。                                                              |
| CVEs (In-Toto format)      | 影响 chart 引用的容器镜像和组件的已知漏洞（CVE）列表。                                                                                                                   |
| Scout provenance           | 由 Docker Scout 生成的来源元数据，包括 chart 源仓库、使用的构建镜像和构建参数。                                                                                                  |
| Scout SBOM                 | 由 Docker Scout 生成并签名的 SBOM，包含 chart 及其引用的容器镜像，并带有额外的 Docker 特定元数据。                                                                                |
| Secrets scan               | 对 chart 包中意外包含的密钥（如凭据、令牌或私钥）的扫描结果。                                                                                                       |
| Tests                      | 针对 chart 运行的自动化测试记录，用于验证与所引用镜像的功能和兼容性。                                                                                                          |
| Virus scan                 | 对 chart 包执行的防病毒扫描结果。详情请参阅 [Malware scanning](../malware-scanning.md)。                                                                                                |
| CVEs (Scout format)        | 由 Docker Scout 生成的漏洞报告，列出 chart 引用镜像的已知 CVE 和严重性数据。                                                                                                      |
| SLSA provenance            | 标准的 [SLSA](https://slsa.dev/) 来源声明，描述 chart 的构建方式，包括构建工具、源仓库、引用的镜像和构建材料。                                                 |
| SPDX SBOM                  | [SPDX](https://spdx.dev/) 格式的 SBOM，列出 chart 及其引用的所有容器镜像和工具。                                                                                                              |

## View and verify attestations（查看和验证证明）

要查看和验证证明，请参阅 [Verify a Docker Hardened Image](../../how-to/verify.md)。

## Add your own attestations（添加你自己的证明）

除了 Docker Hardened Images 提供的全面证明外，你还可以在构建派生镜像时添加自己的已签名证明。如果你在 DHI 之上构建新应用程序，并希望在你的软件供应链中保持透明度、可追溯性和信任，这尤其有用。

通过附加 SBOM、构建来源或自定义元数据等证明，你可以满足合规要求、通过安全审计，并支持 Docker Scout 等策略评估工具。

然后可以使用 Cosign 或 Docker Scout 等工具在下游验证这些证明。

要了解如何在构建过程中附加自定义证明，请参阅 [Build attestations](/manuals/build/metadata/attestations.md)。
