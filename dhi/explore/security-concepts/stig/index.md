# STIG




## What is STIG?（什么是 STIG？）

[Security Technical Implementation Guides（STIGs，安全技术实施指南）](https://public.cyber.mil/stigs/) 是由美国国防信息系统局（DISA）发布的配置标准。它们为美国国防部（DoD）环境中使用的操作系统、应用程序、数据库和其他技术定义了安全要求。

STIG 有助于确保系统以安全且一致的方式配置，从而减少漏洞。它们通常基于更广泛的要求，如 DoD 的通用操作系统安全需求指南（GPOS SRG）。

## Why STIG guidance matters（为何 STIG 指南很重要）

遵循 STIG 指南对于与美国政府系统合作或提供支持的组织至关重要。它表明与 DoD 安全标准的对齐，并有助于：

- 加速 DoD 系统的运行授权（ATO）流程
- 降低错误配置和可被利用弱点的风险
- 通过标准化基线简化审计和报告

即使在联邦环境之外，安全意识强的组织也将 STIG 用作加固系统配置的基准。

STIG 源自更广泛的 NIST 指南，特别是 [NIST Special Publication 800-53](https://csrc.nist.gov/publications/sp800)，该出版物定义了联邦系统的安全和隐私控制目录。追求符合 800-53 或相关框架（如 FedRAMP）的组织可以使用 STIG 作为实施指南，帮助满足适用的控制要求。

## How Docker Hardened Images help apply STIG guidance（Docker Hardened Images 如何帮助应用 STIG 指南）

Docker Hardened Images（DHI）包含 STIG 变体，这些变体针对自定义的基于 STIG 的配置文件进行扫描，并包含已签名的 STIG 扫描证明。这些证明可用于审计和合规报告。

虽然 Docker Hardened Images 面向所有人开放，但 STIG 变体需要 Docker 订阅。

Docker 基于 GPOS SRG 和 DoD 容器加固流程指南为镜像创建自定义的基于 STIG 的配置文件。由于 DISA 尚未发布专门针对容器的 STIG，这些配置文件有助于以一致、可审查的方式将类 STIG 指南应用于容器环境，并旨在减少容器镜像中常见的误报。

## Identify images that include STIG scan results（识别包含 STIG 扫描结果的镜像）

包含 STIG 扫描结果的 Docker Hardened Images 在 Docker Hardened Images 目录中标记为 **STIG**。

要查找带有 STIG 镜像变体的 DHI 仓库，请[浏览镜像](../../tools/hub.md#images-page)并：

- 使用目录页面上的 **STIG** 筛选器
- 在单个镜像列表中查找 **STIG** 标签

要在仓库中查找 STIG 镜像变体，请转到仓库中的 **Tags** 选项卡，并在 **Compliance** 列中查找标记为 **STIG** 的镜像。

## Use a STIG variant（使用 STIG 变体）

要使用 STIG 变体，你必须先[镜像](../../how-to/mirror.md)该仓库，然后从你镜像的仓库中拉取 STIG 镜像。

## View and verify STIG scan results（查看和验证 STIG 扫描结果）

Docker 为每个 STIG 就绪镜像提供已签名的 [STIG 扫描证明](attestations.md)。这些证明包括：

- 扫描结果摘要，包括通过、失败和不适用的检查数量
- 所用 STIG 配置文件的名称和版本
- HTML 和 XCCDF（XML）两种格式的完整输出

### View STIG scan attestations（查看 STIG 扫描证明）

你可以使用 Docker Scout CLI 检索并检查 STIG 扫描证明：

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  dhi.io/<image>:<tag>
```

### Extract HTML report（提取 HTML 报告）

要提取并查看人类可读的 HTML 报告：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "html").content | @base64d' > stig_report.html
```

### Extract XCCDF report（提取 XCCDF 报告）

要提取 XML（XCCDF）报告以与其他工具集成：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0].output[] | select(.format == "xccdf").content | @base64d' > stig_report.xml
```

### View STIG scan summary（查看 STIG 扫描摘要）

要仅查看扫描摘要而不查看完整报告：

```console
$ docker scout attest get dhi.io/<image>:<tag> \
  --predicate-type https://docker.com/dhi/stig/v0.1 \
  --verify \
  --predicate \
  | jq -r '.[0] | del(.output)'
```

