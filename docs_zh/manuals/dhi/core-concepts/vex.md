---
title: 漏洞可利用性交换 (VEX)
linktitle: VEX
description: 了解 VEX 如何通过识别 Docker Hardened Images 中哪些漏洞实际可被利用，帮助您优先处理真实风险。
keywords: vex 容器安全, 漏洞可利用性, 过滤误报, docker scout vex, cve 优先级排序
---

## 什么是 VEX？

漏洞可利用性交换 (Vulnerability Exploitability eXchange, VEX) 是由美国网络安全和基础设施安全局 (CISA) 开发的一种标准化框架，用于记录软件组件中漏洞的可利用性。与传统的 CVE（通用漏洞披露）数据库不同，VEX 提供了上下文相关的评估，指明特定环境中的漏洞是否可被利用。这种方法通过区分可利用的漏洞和与特定用例无关的漏洞，帮助组织优先进行修复工作。

## 为什么 VEX 很重要？

VEX 通过以下方式增强了传统的漏洞管理：

- 减少误报：通过提供特定于上下文的评估，VEX 有助于过滤掉在特定环境中不构成威胁的漏洞。

- 优先进行修复：组织可以集中资源解决在特定上下文中可被利用的漏洞，提高漏洞管理的效率。

- 增强合规性：VEX 报告提供详细信息，有助于满足监管要求和内部安全标准。

这种方法在存在众多组件和配置的复杂环境中特别有益，传统的基于 CVE 的评估可能导致不必要的修复工作。

## Docker Hardened Images 如何集成 VEX

为了增强漏洞管理，Docker Hardened Images (DHI) 集成了 VEX 报告，提供对已知漏洞的特定上下文评估。

此集成允许您：

- 评估可利用性：确定镜像组件中已知漏洞在特定环境中是否可被利用。

- 优先处理操作：集中修复资源解决实际构成风险的漏洞，优化资源分配。

- 简化审计：利用 VEX 报告提供的详细信息，简化合规审计和报告。

通过将 DHI 的安全特性与 VEX 的上下文洞察相结合，组织可以实现更有效和高效的漏洞管理方法。

## 使用 VEX 过滤已知不可利用的 CVE

使用 Docker Scout 或 Trivy 时，VEX 语句会自动应用，如 [常见漏洞和暴露 (CVEs)](./cves.md) 中的示例所示。

对于 Grype，您需要先将 VEX 证明导出到文件，然后再进行扫描，如 [Grype 扫描示例](./cves.md#scan-a-dhi-using-grype) 所示。

> [!NOTE]
>
> 默认情况下，VEX 证明从 `registry.scout.docker.com` 获取。如果您的网络有出站限制，请确保可以访问此注册表。您也可以将证明镜像到其他注册表。更多详细信息，请参阅 [将 Docker Hardened Image 仓库镜像到其他注册表](../how-to/mirror.md#mirror-from-docker-hub-to-another-registry)。

要手动检索支持 VEX 工具的 VEX 证明：

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> [!NOTE]
>
> `docker scout vex get` 命令需要 [Docker Scout CLI](https://github.com/docker/scout-cli/) 版本 1.18.3 或更高版本。
>
> 如果镜像存在于您的本地设备上，您必须在镜像名称前加上 `registry://` 前缀。例如，使用 `registry://dhi.io/python:3.13` 而不是 `dhi.io/python:3.13`。

例如：

```console
$ docker scout vex get dhi.io/python:3.13 --output vex.json
```

这将为指定的镜像创建一个包含 VEX 语句的 `vex.json` 文件。然后您可以将此文件与支持 VEX 的工具一起使用，以过滤掉已知不可利用的 CVE。