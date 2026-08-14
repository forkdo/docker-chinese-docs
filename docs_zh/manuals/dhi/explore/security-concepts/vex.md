---
aliases:
  - /dhi/core-concepts/vex/
title: 漏洞可利用性交换（VEX）
linktitle: VEX
description: 了解 VEX 如何通过识别 Docker Hardened Images 中哪些漏洞实际可被利用，帮助您优先处理真实风险。
keywords: vex container security, vulnerability exploitability, filter false positives, docker scout vex, cve prioritization
---

## 什么是 VEX？

漏洞可利用性交换（Vulnerability Exploitability eXchange，VEX）是一种用于记录软件组件中漏洞可利用性状态的规范。VEX 主要通过 CSAF（OASIS）和 CycloneDX VEX 等行业标准定义，美国网络安全和基础设施安全局（CISA）也在推动其采用。VEX 通过添加由生产者声明的状态信息来补充 CVE（通用漏洞披露）标识符，指明某个漏洞在交付的产品中是否可被利用。这有助于组织识别不影响其特定产品配置的漏洞，从而对修复工作进行优先排序。

有关 VEX 如何影响漏洞计数和扫描器选择，请参阅[扫描器集成](/manuals/dhi/explore/scanner-integrations.md)。要使用支持 VEX 的方式扫描 DHI，请参阅[扫描 Docker Hardened Images](/manuals/dhi/how-to/scan.md)。

## VEX 状态参考

每条 VEX 声明都包含一个 `status` 字段，记录 Docker 对特定 CVE 和镜像的可利用性评估。OpenVEX 定义了四种状态值，DHI 使用其中三种：

| 状态 | 含义 |
|---|---|
| `not_affected` | 该 CVE 是针对镜像中的某个软件包报告的，但 Docker 评估认为在交付状态下不可被利用 |
| `under_investigation` | Docker 已知晓该 CVE，并正在积极评估它是否影响该镜像 |
| `affected` | Docker 已确认该 CVE 在该镜像中可被利用，且修复尚不可用 |
| `fixed` | 该漏洞已在此版本中修复。DHI 不使用此状态（见下文）。 |

您可以使用 Docker Scout 查看任何 DHI 的 VEX 声明。请参阅[扫描 Docker Hardened Images](/manuals/dhi/how-to/scan.md)。

### `not_affected` 理由代码

`not_affected` 声明包含一个机器可读的 `justification` 字段，用于说明该漏洞为何不适用：

| 理由 | 含义 |
|---|---|
| `component_not_present` | 该镜像中不存在存在漏洞的组件；该 CVE 是按名称匹配到了另一个软件包 |
| `vulnerable_code_not_present` | 存在漏洞的代码路径未被编译进此次构建 |
| `vulnerable_code_not_in_execute_path` | 存在漏洞的代码存在于软件包中，但在该镜像的运行时配置下不会被调用 |
| `vulnerable_code_cannot_be_controlled_by_adversary` | 存在漏洞的代码存在，但攻击者在此配置下无法触发它 |
| `inline_mitigations_already_exist` | Docker 已应用可解决该 CVE 的向后移植补丁或补丁 |

### 为什么 DHI 不使用 `fixed`

DHI 不使用 `fixed`。支持 VEX 的扫描器对 `fixed` 的处理方式可能不一致，因此当 Docker 向后移植上游补丁、而仅凭版本号无法反映该修复时，会改用 `not_affected` 并附带 `inline_mitigations_already_exist` 理由。
