---
title: 'STIG <span class="not-prose bg-blue-500 dark:bg-blue-400 rounded-sm px-1 text-xs text-white whitespace-nowrap">DHI Enterprise</span>'
linkTitle: STIG
description: 了解 Docker Hardened Images 如何为政府和企业合规需求提供即用型 STIG 容器镜像，以及可验证的安全扫描证明。
keywords: docker stig, stig-ready images, stig guidance, openscap docker, secure container images
---

{{< summary-bar feature_name="Docker Hardened Images" >}}

## 什么是 STIG？

[安全技术实施指南（STIG）](https://public.cyber.mil/stigs/) 是由美国国防信息系统局（DISA）发布的配置标准。它们定义了美国国防部（DoD）环境中使用的操作系统、应用程序、数据库和其他技术的安全要求。

STIG 有助于确保系统以安全且一致的方式配置，以减少漏洞。它们通常基于更广泛的 DoD 通用操作系统安全需求指南（GPOS SRG）等要求。

## 为什么 STIG 指导很重要

遵循 STIG 指导对于与美国政府系统合作或为其提供支持的组织至关重要。它展示了与 DoD 安全标准的一致性，并有助于：

- 加速 DoD 系统的授权运行（ATO）流程
- 降低配置错误和可利用漏洞的风险
- 通过标准化基线简化审计和报告

即使在联邦环境之外，安全意识强的组织也使用 STIG 作为加固系统配置的基准。

STIG 源自更广泛的 NIST 指导，特别是 [NIST 特别出版物 800-53](https://csrc.nist.gov/publications/sp800)，该出版物定义了联邦系统的安全和隐私控制目录。追求 800-53 或相关框架（如 FedRAMP）合规性的组织可以使用 STIG 作为实施指南，以帮助满足适用的控制要求。

## Docker Hardened Images 如何帮助应用 STIG 指导

Docker Hardened Images（DHI）包含 STIG 变体，这些变体针对基于 STIG 的自定义配置文件进行扫描，并包含已签名的 STIG 扫描证明。这些证明可以支持审计和合规报告。

虽然 Docker Hardened Images 向所有用户开放，但 STIG 变体需要 Docker 订阅。

Docker 基于 GPOS SRG 和 DoD 容器加固流程指南为镜像创建自定义的 STIG 配置文件。由于 DISA 尚未发布专门针对容器的 STIG，这些配置文件有助于以一致、可审查的方式将类似 STIG 的指导应用于容器环境，并旨在减少容器镜像中常见的误报。

## 识别包含 STIG 扫描结果的镜像

在 Docker Hardened Images 目录中，包含 STIG 扫描结果的镜像被标记为 **STIG**。

要查找具有 STIG 镜像变体的 DHI 仓库，[浏览镜像](../how-to/explore.md) 并：

- 在目录页面上使用 **STIG** 筛选器
- 在单个镜像列表上查找 **STIG** 标签

要在仓库中查找 STIG 镜像变体，请转到仓库的 **Tags** 标签页，在 **Compliance** 列中找到标记为 **STIG** 的镜像。

## 使用 STIG 变体

要使用 STIG 变体，您必须 [镜像](../how-to/mirror.md) 仓库，然后从您的镜像仓库中拉取 STIG 镜像。

## 查看和验证 STIG 扫描结果

Docker 为每个 STIG 就绪镜像提供已签名的 [STIG 扫描证明](../core-concepts/attestations.md)。这些证明包括：

- 扫描结果摘要，包括通过、失败和不适用检查的数量
- 所用 STIG 配置文件的名称和版本
- HTML 和 XCCDF（XML）格式的完整输出

### 查看 STIG 扫描证明

您可以使用 Docker Scout CLI 检索和检查 STIG 扫描证明：

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  dhi.io/<image>:<tag>
```

### 提取 HTML 报告

要提取并查看可读的 HTML 报告：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "html").content | @base64d' > stig_report.html
```

### 提取 XCCDF 报告

要提取 XML（XCCDF）报告以集成到其他工具中：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "xccdf").content | @base64d' > stig_report.xml
```

### 查看 STIG 扫描摘要

要仅查看扫描摘要而不包含完整报告：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0] | del(.output)'
```