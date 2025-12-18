---
title: 使用 VEX 创建例外
description: 使用 VEX 文档为镜像中的漏洞创建例外。
keywords: Docker, 漏洞, 例外, 创建, VEX
aliases:
  - /scout/guides/vex/
---

漏洞可利用性交换（Vulnerability Exploitability eXchange，VEX）是一种标准格式，用于记录软件包或产品中漏洞的上下文信息。Docker Scout 支持 VEX 文档，用于为镜像中的漏洞创建 [例外](/manuals/scout/explore/exceptions.md)。

> [!NOTE]
> 您也可以使用 Docker Scout 仪表板或 Docker Desktop 创建例外。GUI 提供了用户友好的界面来创建例外，并且易于管理多个镜像的例外。它还允许您一次性为多个镜像或整个组织创建例外。更多信息，请参阅 [使用 GUI 创建例外](/manuals/scout/how-tos/create-exceptions-gui.md)。

## 前置条件

要使用 OpenVEX 文档创建例外，您需要：

- 最新版本的 Docker Desktop 或 Docker Scout CLI 插件
- [`vexctl`](https://github.com/openvex/vexctl) 命令行工具
- 必须启用 [containerd 镜像存储](/manuals/desktop/features/containerd.md)
- 对存储镜像的注册表仓库具有写入权限

## VEX 简介

VEX 标准由美国网络安全和基础设施安全局（CISA）的一个工作组定义。VEX 的核心是可利用性评估。这些评估描述了给定 CVE 在产品中的状态。VEX 中可能的漏洞状态包括：

- 不受影响：无需针对此漏洞进行修复。
- 受影响：建议采取行动来修复或解决此漏洞。
- 已修复：这些产品版本包含对漏洞的修复。
- 调查中：尚不清楚这些产品版本是否受漏洞影响。将在后续版本中提供更新。

VEX 有多种实现和格式。Docker Scout 支持 [OpenVex](https://github.com/openvex/spec) 实现。无论具体实现如何，核心思想都是相同的：提供一个框架来描述漏洞的影响。VEX 的关键组件包括（与实现无关）：

VEX 文档
: 用于存储 VEX 语句的一种安全公告。文档的格式取决于具体的实现。

VEX 语句
: 描述漏洞在产品中的状态，是否可利用，以及是否有方法来修复问题。

理由和影响
: 根据漏洞状态，语句包括理由或影响说明，解释产品为何受影响或不受影响。

行动说明
: 描述如何修复或缓解漏洞。

## `vexctl` 示例

以下示例命令创建一个 VEX 文档，说明：

- 此 VEX 文档描述的软件产品是 Docker 镜像 `example/app:v1`
- 该镜像包含 npm 包 `express@4.17.1`
- npm 包受已知漏洞 `CVE-2022-24999` 影响
- 由于易受攻击的代码在运行此镜像的容器中永远不会执行，因此该镜像不受此 CVE 影响

```console
$ vexctl create \
  --author="author@example.com" \
  --product="pkg:docker/example/app@v1" \
  --subcomponents="pkg:npm/express@4.17.1" \
  --vuln="CVE-2022-24999" \
  --status="not_affected" \
  --justification="vulnerable_code_not_in_execute_path" \
  --file="CVE-2022-24999.vex.json"
```

以下是此示例中各选项的说明：

`--author`
: VEX 文档作者的电子邮件。

`--product`
: Docker 镜像的软件包 URL（PURL）。PURL 是镜像的标准化格式标识符，定义在 PURL [规范](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#docker)中。

Docker 镜像 PURL 字符串以 `pkg:docker` 类型前缀开头，后跟镜像仓库和版本（镜像标签或 SHA256 摘要）。与镜像标签不同，镜像标签中版本指定为 `example/app:v1`，而在 PURL 中，镜像仓库和版本由 `@` 分隔。

`--subcomponents`
: 镜像中易受攻击包的 PURL。在此示例中，漏洞存在于 npm 包中，因此 `--subcomponents` PURL 是 npm 包名称和版本的标识符（`pkg:npm/express@4.17.1`）。

如果同一漏洞存在于多个包中，`vexctl` 允许您在单个 `create` 命令中多次指定 `--subcomponents` 标志。

您也可以省略 `--subcomponents`，此时 VEX 语句适用于整个镜像。

`--vuln`
: VEX 语句所解决的 CVE ID。

`--status`
: 这是漏洞的状态标签。它描述了软件（`--product`）与 CVE（`--vuln`）之间的关系。OpenVEX 中状态标签的可能值包括：

  - `not_affected`
  - `affected`
  - `fixed`
  - `under_investigation`

在此示例中，VEX 语句断言 Docker 镜像 `not_affected`（不受影响）于该漏洞。`not_affected` 状态是唯一能导致 CVE 抑制的状态，此时 CVE 会从分析结果中过滤掉。其他状态对文档记录很有用，但不能用于创建例外。有关所有可能状态标签的更多信息，请参阅 OpenVEX 规范中的 [状态标签](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#status-labels)。

`--justification`
: 证明 `not_affected` 状态标签的合理性，说明产品为何不受漏洞影响。在此情况下，给出的理由是 `vulnerable_code_not_in_execute_path`，表示漏洞在产品使用中无法执行。

在 OpenVEX 中，状态理由可以有以下五种可能值之一：

  - `component_not_present`
  - `vulnerable_code_not_present`
  - `vulnerable_code_not_in_execute_path`
  - `vulnerable_code_cannot_be_controlled_by_adversary`
  - `inline_mitigations_already_exist`

有关这些值及其定义的更多信息，请参阅 OpenVEX 规范中的 [状态理由](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#status-justifications)。

`--file`
: VEX 文档输出的文件名

## 示例 JSON 文档

以下是此命令生成的 OpenVEX JSON：

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://openvex.dev/docs/public/vex-749f79b50f5f2f0f07747c2de9f1239b37c2bda663579f87a35e5f0fdfc13de5",
  "author": "author@example.com",
  "timestamp": "2024-05-27T13:20:22.395824+02:00",
  "version": 1,
  "statements": [
    {
      "vulnerability": {
        "name": "CVE-2022-24999"
      },
      "timestamp": "2024-05-27T13:20:22.395829+02:00",
      "products": [
        {
          "@id": "pkg:docker/example/app@v1",
          "subcomponents": [
            {
              "@id": "pkg:npm/express@4.17.1"
            }
          ]
        }
      ],
      "status": "not_affected",
      "justification": "vulnerable_code_not_in_execute_path"
    }
  ]
}
```

理解 VEX 文档应该如何构建可能有点复杂。[OpenVEX 规范](https://github.com/openvex/spec) 描述了格式以及文档和语句的所有可能属性。要了解详细信息，请参阅规范以了解可用字段以及如何创建格式正确的 OpenVEX 文档。

要了解 `vexctl` CLI 工具的可用标志、语法以及如何安装它，请参阅 [`vexctl` GitHub 仓库](https://github.com/openvex/vexctl)。

## 验证 VEX 文档

要测试您创建的 VEX 文档是否格式正确并产生预期结果，请使用 `docker scout cves` 命令和 `--vex-location` 标志将 VEX 文档应用于 CLI 的本地镜像分析。

以下命令调用本地镜像分析，该分析包含在指定位置使用 `--vex-location` 标志找到的所有 VEX 文档。在此示例中，CLI 被指示在当前工作目录中查找 VEX 文档。

```console
$ docker scout cves <IMAGE> --vex-location .
```

`docker scout cves` 命令的输出显示结果，其中任何在 `--vex-location` 位置找到的 VEX 语句都已纳入结果。例如，被分配为 `not_affected` 状态的 CVE 会从结果中过滤掉。如果输出似乎未考虑 VEX 语句，这表明 VEX 文档可能在某些方面无效。

需要注意的事项包括：

- Docker 镜像的 PURL 必须以 `pkg:docker/` 开头，后跟镜像名称。
- 在 Docker 镜像 PURL 中，镜像名称和版本由 `@` 分隔。名为 `example/myapp:1.0` 的镜像具有以下 PURL：`pkg:docker/example/myapp@1.0`。
- 记得指定 `author`（它是 OpenVEX 中的强制字段）
- [OpenVEX 规范](https://github.com/openvex/spec) 描述了如何以及何时在 VEX 文档中使用 `justification`、`impact_statement` 和其他字段。以不正确的方式指定这些字段会导致文档无效。确保您的 VEX 文档符合 OpenVEX 规范。

## 将 VEX 文档附加到镜像

创建 VEX 文档后，您可以通过以下方式将其附加到镜像：

- 将文档作为 [证明](#attestation) 附加
- 将文档嵌入 [镜像文件系统](#image-filesystem)

一旦将 VEX 文档添加到镜像，就无法将其移除。对于作为证明附加的文档，您可以创建一个新的 VEX 文档并再次将其附加到镜像。这样做会覆盖之前的 VEX 文档（但不会移除证明）。对于 VEX 文档已嵌入镜像文件系统的镜像，您需要重建镜像以更改 VEX 文档。

### 证明

要将 VEX 文档作为证明附加，您可以使用 `docker scout attestation add` CLI 命令。当使用 VEX 时，将证明作为例外附加到镜像是推荐选项。

您可以将证明附加到已推送到注册表的镜像。您无需再次构建或推送镜像。此外，将例外作为证明附加到镜像意味着消费者可以直接从注册表检查镜像的例外。

要将证明附加到镜像：

1. 构建镜像并将其推送到注册表。

   ```console
   $ docker build --provenance=true --sbom=true --tag <IMAGE> --push .
   ```

2. 将例外作为证明附加到镜像。

   ```console
   $ docker scout attestation add \
     --file <cve-id>.vex.json \
     --predicate-type https://openvex.dev/ns/v0.2.0 \
     <IMAGE>
   ```

此命令的选项包括：

- `--file`：VEX 文档的位置和文件名
- `--predicate-type`：OpenVEX 的 in-toto `predicateType`

### 镜像文件系统

将 VEX 文档直接嵌入镜像文件系统是一个不错的选择，如果您在构建镜像之前就知道例外情况。而且这相对简单；只需在 Dockerfile 中使用 `COPY` 将 VEX 文档复制到镜像中。

这种方法的缺点是您以后无法更改或更新例外。镜像层是不可变的，因此放在镜像文件系统中的任何内容都会永远存在。将文档作为 [证明](#attestation) 附加提供了更好的灵活性。

> [!NOTE]
> 对于具有证明的镜像，不会考虑嵌入镜像文件系统的 VEX 文档。如果您的镜像有 **任何** 证明，Docker Scout 将只在证明中查找例外，而不会在镜像文件系统中查找。
>
> 如果您想使用嵌入镜像文件系统的 VEX 文档，您必须从镜像中移除证明。请注意，证明可能会自动添加到镜像中。为确保不向镜像添加任何证明，您可以在构建镜像时使用 `--provenance=false` 和 `--sbom=false` 标志显式禁用 SBOM 和来源证明。

要将 VEX 文档嵌入镜像文件系统，请在镜像构建期间将文件 `COPY` 到镜像中。以下示例展示了如何将构建上下文中的 `.vex/` 下的所有 VEX 文档复制到镜像中的 `/var/lib/db`。

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine
COPY .vex/* /var/lib/db/
```

VEX 文档的文件名必须匹配 `*.vex.json` 通配符模式。文件存储在镜像文件系统的哪个位置并不重要。

请注意，复制的文件必须是最终镜像文件系统的一部分。对于多阶段构建，文档必须在最终阶段中保留。