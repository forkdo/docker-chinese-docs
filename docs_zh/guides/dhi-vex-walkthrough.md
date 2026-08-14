---
title: 在 Docker Hardened Images 中探索 VEX 声明
description: |
  在启用和禁用 VEX 的情况下分别扫描 Docker Hardened Image，并审计每一条
  CVE 抑制及其理由。
summary: >
  在启用和禁用 VEX 的情况下分别扫描 Docker Hardened Image，并审计每一条抑制
  及其理由。
keywords: vex, openvex, not_affected, under_investigation, affected, cve, docker scout, dhi, vulnerability
weight: 1
params:
  tags: [security]
  featured: true
  proficiencyLevel: Intermediate
  time: 25 minutes
---

标准漏洞扫描器会针对镜像中存在的包报告 CVE。对于 Docker Hardened Images，这些包的存在是设计使然，但每一个被报告的 CVE 都附有一条 VEX 声明，说明在该特定产品配置下它是否可利用。本指南将带你逐步扫描启用和禁用 VEX 的 Docker Hardened Image，并审计每条抑制背后的理由。

## 先决条件

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)，已认证到 `dhi.io`。使用 `docker login dhi.io` 登录。Docker Desktop 内置了 Docker Scout，它会获取 VEX 证明（attestation）。
- 一个漏洞扫描器。本指南展示了 Docker Scout、[Trivy](https://trivy.dev/) 和 [Grype](https://github.com/anchore/grype) 的示例。Trivy 和 Grype 也可以作为 Docker 容器运行，无需安装。
- `jq`（可选），用于过滤 VEX 文件。

## 为 Windows 用户开放守护进程

本指南中容器化扫描器命令所使用的 `-v /var/run/docker.sock:/var/run/docker.sock` 套接字挂载，在 Docker Desktop for Windows 上无法工作。要在 Windows 上使用容器化扫描器，请在 Docker Desktop 中进入 **Settings > General**（设置 > 通用），并开启 **Expose daemon on tcp://localhost:2375 without TLS**（在 TCP 上开放守护进程，不使用 TLS）。然后在每条容器化扫描器命令中，将 `-v /var/run/docker.sock:/var/run/docker.sock` 替换为 `-e DOCKER_HOST=tcp://host.docker.internal:2375`。

> [!WARNING]
>
> 在 TCP 上以不使用 TLS 的方式开放守护进程，会使你的系统面临远程代码执行攻击。测试完成后请关闭该设置。

## 步骤 1：不启用 VEX 进行扫描

登录到 Docker Hardened Images 镜像仓库：

```console
$ docker login dhi.io
```

然后拉取镜像：

```console
$ docker pull dhi.io/python:3.13
```

然后在不启用 VEX 的情况下进行扫描，以查看原始 CVE 数量。Docker Scout 会自动对 Docker Hardened Images 应用 VEX。要查看未经过滤的 CVE 基线，请使用 Trivy 或 Grype。

{{< tabs >}}
{{< tab name="Trivy" >}}

```console
$ trivy image --scanners vuln dhi.io/python:3.13
```

如果未安装 Trivy，可在容器中运行它：

```console
$ docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image --scanners vuln dhi.io/python:3.13
```

示例输出：

```plaintext
Total: 30 (UNKNOWN: 0, LOW: 15, MEDIUM: 11, HIGH: 4, CRITICAL: 0)
```

{{< /tab >}}
{{< tab name="Grype" >}}

```console
$ grype dhi.io/python:3.13
```

如果未安装 Grype，可在容器中运行它：

```console
$ docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  anchore/grype:latest docker:dhi.io/python:3.13
```

示例输出：

```plaintext
NAME          INSTALLED              FIXED IN     TYPE  VULNERABILITY       SEVERITY
libc6         2.41-12+deb13u2                     deb   CVE-2018-20796      Negligible
libc6         2.41-12+deb13u2        (won't fix)  deb   CVE-2026-4437       High
libc6         2.41-12+deb13u2        (won't fix)  deb   CVE-2026-5450       Critical
...
```

{{< /tab >}}
{{< /tabs >}}

输出列出了 `libc6`、`libncursesw6`、`libsqlite3-0`、`libuuid1`、`zlib1g` 等包中的 CVE，它们全都是 Python 运行所需的运行时依赖。这些包的存在是设计使然。

像这样的扫描结果并不意味着每一个被报告的 CVE 都需要打补丁。它只意味着这些 CVE 是针对镜像中存在的包被报告的。至于这些 CVE 中有哪些在此配置下实际可被利用，则是另一个独立的问题——而这恰恰是 VEX 所要回答的。

## 步骤 2：获取 VEX 证明

将 VEX 证明导出到本地文件：

```console
$ docker scout vex get registry://dhi.io/python:3.13 --output python-vex.json
```

`registry://` 前缀告诉 Scout 从镜像仓库（而非本地镜像存储）获取证明。由于你在步骤 1 中已经拉取了该镜像，它已存在于本地；如果不加此前缀，Scout 在本地找不到任何证明。

这会从 `registry.scout.docker.com`（Docker 为所有 Docker Hardened Images 提供的供应链元数据镜像仓库）获取一份已签名的 OpenVEX 文档。该文档记录了 Docker 对镜像 SBOM 中发现的每个 CVE 的可利用性评估。

> [!NOTE]
>
> Docker Scout 在扫描时会自动获取并应用此文件。你只需为那些未原生集成它的扫描器，或者为运行步骤 5 和步骤 6 中的 `jq` 查询而显式下载它。

## 步骤 3：在应用 VEX 的情况下进行扫描

{{< tabs >}}
{{< tab name="Docker Scout" >}}

Docker Scout 自动获取并应用 VEX 证明，无需本地文件：

```console
$ docker scout cves dhi.io/python:3.13
```

示例输出：

```plaintext
    ✓ SBOM obtained from attestation, 47 packages indexed
    ✓ Provenance obtained from attestation
    ✓ VEX statements obtained from attestation
    ✓ No vulnerable package detected
```

{{< /tab >}}
{{< tab name="Trivy" >}}

使用 `--vex` 标志传入 VEX 文件：

```console
$ trivy image --scanners vuln --vex python-vex.json dhi.io/python:3.13
```

如果未安装 Trivy，可在容器中运行它：

```console
$ docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)/python-vex.json:/tmp/vex.json" \
  aquasec/trivy:latest image --scanners vuln --vex /tmp/vex.json dhi.io/python:3.13
```

示例输出：

```plaintext
Total: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)

Some vulnerabilities have been ignored/suppressed. Use the '--show-suppressed' flag to display them.
```

{{< /tab >}}
{{< tab name="Grype" >}}

使用 `--vex` 标志传入 VEX 文件：

```console
$ grype dhi.io/python:3.13 --vex python-vex.json
```

如果未安装 Grype，可在容器中运行它：

```console
$ docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)/python-vex.json:/tmp/vex.json" \
  anchore/grype:latest docker:dhi.io/python:3.13 --vex /tmp/vex.json
```

示例输出：

```plaintext
No vulnerabilities found
```

{{< /tab >}}
{{< /tabs >}}

相同的镜像，相同的包，相同的 CVE 数据库。唯一的区别在于上下文。扫描器将每个 CVE 与 VEX 文件进行匹配，并抑制了 Docker 评估为不可利用的每一条。

这些包仍然存在。检查 SBOM，你会看到 `libc6`、`libsqlite3-0` 以及步骤 1 中的其他每个包。零 CVE 并不意味着这些包被移除了。它意味着每个被报告的 CVE 都有一份记录在案的、说明其为何不适用于此产品配置的理由。

VEX 是一个开放标准：证明随镜像一同传递，任何兼容的扫描器都会读取相同的推理逻辑。

## 步骤 4：检查每一条抑制及其理由

Docker Scout 和 Grype 会抑制与 VEX 匹配的 CVE，但不会在其输出中展示理由代码。请使用 Trivy 的 `--show-suppressed` 标志，以查看每条被抑制的 CVE 及其对应的每条 CVE 理由代码。

```console
$ trivy image --scanners vuln --vex python-vex.json --show-suppressed dhi.io/python:3.13
```

如果未安装 Trivy，可在容器中运行它：

```console
$ docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)/python-vex.json:/tmp/vex.json" \
  aquasec/trivy:latest image --scanners vuln --vex /tmp/vex.json --show-suppressed dhi.io/python:3.13
```

示例输出：

```plaintext
Suppressed Vulnerabilities (Total: 28)
======================================
┌──────────────┬──────────────────┬──────────┬──────────────┬───────────────────────────────────────────────────┐
│   Library    │  Vulnerability   │ Severity │    Status    │                     Statement                     │
├──────────────┼──────────────────┼──────────┼──────────────┼───────────────────────────────────────────────────┤
│ libc6        │ CVE-2010-4756    │ LOW      │ not_affected │ vulnerable_code_cannot_be_controlled_by_adversary │
│ libsqlite3-0 │ CVE-2025-70873   │ LOW      │ not_affected │ vulnerable_code_not_present                       │
│ ...          │ ...              │ ...      │ ...          │ ...                                               │
└──────────────┴──────────────────┴──────────┴──────────────┴───────────────────────────────────────────────────┘
```

`Statement` 列显示了来自 VEX 文件的、机器可读的理由代码。

这些理由代码具有精确的含义：

- `vulnerable_code_cannot_be_controlled_by_adversary`：该包中存在存在漏洞的代码路径，但在此配置下攻击者无法触发它。
- `vulnerable_code_not_present`：存在漏洞的代码未被编译进此构建版本，或以其他方式缺失。
- `inline_mitigations_already_exist`：Docker 已应用一个向后移植的补丁或修复，以解决此镜像中的该 CVE。

完整的理由代码列表，请参阅 [VEX 状态参考](/manuals/dhi/explore/security-concepts/vex.md#not_affected-justification-codes)。

每一条抑制都是被记录、可审计、并可使用任何支持 VEX 的扫描器进行验证的。

## 步骤 5：阅读 Docker 对特定 CVE 的推理

理由代码是机器可读的；VEX 文件中的 `status_notes` 字段包含了 Docker 以人类可读语言写出的推理。使用 `jq` 来查找特定的 CVE：

```console
$ jq '.statements[] | select(.vulnerability.name == "CVE-2010-4756") | {status, justification, status_notes}' python-vex.json
```

示例输出：

```json
{
  "status": "not_affected",
  "justification": "vulnerable_code_cannot_be_controlled_by_adversary",
  "status_notes": "Standard POSIX behavior in glibc. Applications using glob need to impose limits themselves. Requires authenticated access and is considered unimportant by Debian."
}
```

`status_notes` 字段以通俗语言解释了 Docker 的推理逻辑。对于 CVE-2010-4756，该 CVE 所描述的 glob 行为是标准的 POSIX 行为，需要已认证的访问权限，并且被 Debian 安全团队归类为不重要。

每条声明还会以 Package URL（PURL）的形式列出受影响的产品，例如 `pkg:deb/debian/glibc@2.41-12%2Bdeb13u2?os_distro=trixie&os_name=debian&os_version=13`。Trivy 通过将这个 PURL 与 SBOM 中记录的包进行比对，将该声明匹配到了镜像 SBOM 中的 `libc6`。

> [!IMPORTANT]
>
> PURL 匹配是严格的。扫描器必须使用完整的 PURL 字符串（包括 `os_name`、`os_version` 和 `os_distro` 限定符）来将 VEX 声明匹配到包。仅依据包名进行匹配，可能会把针对某一 OS 版本的抑制错误地应用到另一个*确实*可利用该 CVE 的版本上。

## 步骤 6：按状态过滤 VEX 声明

一旦你拥有了 `python-vex.json`，就可以直接使用 `jq` 查询它。

按状态统计声明数量：

```console
$ jq '[.statements[].status] | group_by(.) | map({status: .[0], count: length})' python-vex.json
```

列出所有正在调查中的 CVE：

```console
$ jq '[.statements[] | select(.status == "under_investigation") | {cve: .vulnerability.name, products: [.products[]."@id"]}]' python-vex.json
```

列出任何处于 `affected` 状态的 CVE：

```console
$ jq '[.statements[] | select(.status == "affected") | {cve: .vulnerability.name, action: .action_statement}]' python-vex.json
```

对于当前的 `dhi.io/python:3.13` 镜像，`affected` 查询返回一个空数组，这对于一个被积极维护的标签而言是预期结果。要查看所有 DHI Python 版本中的 `affected` 条目，请查询完整的 VEX 数据源：

```console
$ curl -s https://raw.githubusercontent.com/docker-hardened-images/advisories/main/vex/python/dhi-python.vex.json \
  | jq '[.statements[] | select(.status == "affected") | {cve: .vulnerability.name, action: .action_statement}]'
```

有关状态定义和理由代码，请参阅 [VEX 状态参考](/manuals/dhi/explore/security-concepts/vex.md#vex-status-reference)。

## 后续步骤

- 使用其他工具扫描：了解如何在 [扫描 Docker Hardened Images](/manuals/dhi/how-to/scan.md) 中使用 Trivy（VEX Hub）和 Grype 应用 DHI VEX 声明。
- 为子镜像编写你自己的 VEX：如果你在 DHI 基础上构建，并希望抑制你所添加包中的 CVE，请参阅 [使用 VEX 创建例外](/manuals/scout/how-tos/create-exceptions-vex.md)。
- VEX 状态参考：有关状态定义、理由代码，以及 DHI 为何不使用 `fixed` 的原因，请参阅 [漏洞可利用性交换（VEX）](/manuals/dhi/explore/security-concepts/vex.md#vex-status-reference)。
- 直接浏览 VEX 数据源：原始 VEX 数据发布于 [github.com/docker-hardened-images/advisories](https://github.com/docker-hardened-images/advisories/tree/main/vex)，按镜像名称组织。
