---
title: 在 Docker Scout 中开始使用策略评估
linkTitle: 策略评估
weight: 70
keywords: scout, 供应链, 漏洞, 包, CVE, 策略
description: |
  Docker Scout 中的策略允许您为制品定义供应链规则和阈值，并跟踪您的制品随时间满足这些要求的表现
---

在软件供应链管理中，维护制品的安全性和可靠性是首要任务。Docker Scout 中的策略评估在现有分析功能的基础上，引入了一层额外的控制。它允许您定义制品的图像质量标准，并帮助您跟踪制品相对于规则和阈值的表现随时间的变化。

了解如何使用策略评估来确保您的制品符合既定的最佳实践。

## 策略评估的工作原理

当您为仓库启用 Docker Scout 时，推送的镜像会[自动被分析](/manuals/scout/explore/analysis.md)。分析为您提供有关镜像组成的洞察，包括它们包含哪些包以及它们暴露了哪些漏洞。策略评估建立在镜像分析功能之上，根据策略定义的规则解释分析结果。

策略定义了您的制品应满足的图像质量标准。例如，**禁止 AGPL v3 许可证**策略会标记任何包含以 AGPL v3 许可证分发的包的镜像。如果镜像包含此类包，则该镜像不符合此策略。某些策略（如**禁止 AGPL v3 许可证**策略）是可配置的。可配置的策略允许您调整标准，以更好地匹配您组织的需求。

在 Docker Scout 中，策略旨在帮助您逐步提升安全性和供应链地位。其他工具专注于提供通过或失败状态，而 Docker Scout 策略则可视化小的、渐进式的变化如何影响策略状态，即使您的制品尚未满足策略要求（目前）。通过跟踪失败差距随时间的变化，您可以更容易地看出制品相对于策略是改善还是恶化。

策略不一定与应用程序安全和漏洞相关。您也可以使用策略来衡量和跟踪供应链管理的其他方面，如开源许可证使用和基础镜像的时效性。

## 策略类型

在 Docker Scout 中，*策略* 派生自 *策略类型*。策略类型是定义策略核心参数的模板。您可以将策略类型与面向对象编程中的类进行比较，每个策略作为从其对应策略类型创建的实例。

Docker Scout 支持以下策略类型：

- [基于严重性的漏洞](#基于严重性的漏洞)
- [合规许可证](#合规许可证)
- [最新的基础镜像](#最新的基础镜像)
- [高知名度漏洞](#高知名度漏洞)
- [供应链证明](#供应链证明)
- [默认非 root 用户](#默认非-root用户)
- [批准的基础镜像](#批准的基础镜像)
- [SonarQube 质量门禁](#sonarqube-质量门禁)
- [有效的 Docker Hardened 镜像 (DHI) 或 DHI 基础镜像](#有效的-docker-hardened-镜像-dhi-或-dhi-基础镜像)

Docker Scout 为启用的仓库自动提供默认策略，除了以下策略是可选的，必须手动配置：

- **SonarQube 质量门禁**策略，需要在使用前[与 SonarQube 集成](/manuals/scout/integrations/code-quality/sonarqube.md)。
- **有效的 Docker Hardened 镜像 (DHI) 或 DHI 基础镜像**策略，如果您希望强制使用 Docker Hardened 镜像，可以配置此策略。

您可以从任何支持的策略类型创建自定义策略，或者如果默认策略不适用于您的项目，也可以删除它。更多信息，请参阅[配置策略](./configure.md)。

<!-- vale Docker.HeadingSentenceCase = NO -->

### 基于严重性的漏洞

**基于严重性的漏洞**策略类型检查您的制品是否暴露于已知漏洞。

默认情况下，此策略仅标记存在可用修复版本的严重和高严重性漏洞。本质上，这意味着对于未通过此策略的镜像，有一个简单的修复方法：将易受攻击的包升级到包含漏洞修复的版本。

如果制品包含一个或多个不符合指定策略标准的漏洞，则被视为不符合此策略。

您可以通过创建此策略的自定义版本来配置其参数。自定义版本中可配置的策略参数如下：

- **年龄**：自漏洞首次发布以来的最小天数

  仅标记具有一定最小年龄的漏洞的理由是，新发现的漏洞不应导致您的评估失败，直到您有机会解决它们。

<!-- vale Vale.Spelling = NO -->
- **严重性**：考虑的严重性级别（默认：`Critical, High`）
<!-- vale Vale.Spelling = YES -->

- **仅可修复的漏洞**：是否仅报告有可用修复版本的漏洞（默认启用）。

- **包类型**：要包含的包类型列表。

  此选项允许您指定[作为 PURL 包类型定义](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst)的包类型，这些类型将包含在策略评估中。默认情况下，策略考虑所有包类型。

有关配置策略的更多信息，请参阅[配置策略](./configure.md)。

### 合规许可证

**合规许可证**策略类型检查您的镜像是否包含以不适当许可证分发的包。如果镜像包含一个或多个具有此类许可证的包，则被视为不符合策略。

您可以配置此策略应查找的许可证列表，并通过指定允许列表（以 PURL 形式）添加例外。参见[配置策略](./configure.md)。

### 最新的基础镜像

**最新的基础镜像**策略类型检查您使用的基础镜像是否为最新。

如果用于构建镜像的标签指向的摘要与您使用的不同，则镜像被视为不符合此策略。如果摘要不匹配，意味着您使用的基础镜像已过时。

您的镜像需要证明证明才能成功评估此策略。更多信息，请参阅[无基础镜像数据](#无基础镜像数据)。

### 高知名度漏洞

**高知名度漏洞**策略类型检查您的镜像是否包含 Docker Scout 精选列表中的漏洞。此列表会根据新披露的、被广泛认为有风险的漏洞保持最新。

列表包括以下漏洞：

- [CVE-2014-0160 (OpenSSL Heartbleed)](https://scout.docker.com/v/CVE-2014-0160)
- [CVE-2021-44228 (Log4Shell)](https://scout.docker.com/v/CVE-2021-44228)
- [CVE-2023-38545 (cURL SOCKS5 堆缓冲区溢出)](https://scout.docker.com/v/CVE-2023-38545)
- [CVE-2023-44487 (HTTP/2 Rapid Reset)](https://scout.docker.com/v/CVE-2023-44487)
- [CVE-2024-3094 (XZ 后门)](https://scout.docker.com/v/CVE-2024-3094)
- [CVE-2024-47176 (OpenPrinting - `cups-browsed`)](https://scout.docker.com/v/CVE-2024-47176)
- [CVE-2024-47076 (OpenPrinting - `libcupsfilters`)](https://scout.docker.com/v/CVE-2024-47076)
- [CVE-2024-47175 (OpenPrinting - `libppd`)](https://scout.docker.com/v/CVE-2024-47175)
- [CVE-2024-47177 (OpenPrinting - `cups-filters`)](https://scout.docker.com/v/CVE-2024-47177)

您可以通过配置策略来自定义此策略，以更改哪些 CVE 被视为高知名度。自定义配置选项包括：

- **排除的 CVE**：指定您希望此策略忽略的 CVE。

  默认：`[]`（不忽略任何高知名度 CVE）

- **CISA KEV**：启用对 CISA 已知被利用漏洞 (KEV) 目录中漏洞的跟踪

  [CISA KEV 目录](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
  包含在野外被积极利用的漏洞。启用后，策略会标记包含 CISA KEV 目录中漏洞的镜像。

  默认启用。

有关策略配置的更多信息，请参阅[配置策略](./configure.md)。

### 供应链证明

**供应链证明**策略类型检查您的镜像是否具有[SBOM](/manuals/build/metadata/attestations/sbom.md)和[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)证明。

如果镜像缺少 SBOM 证明或具有 *max mode* 来源的来源证明，则被视为不符合策略。为确保符合策略，请更新您的构建命令，在构建时附加这些证明：

```console
$ docker buildx build --provenance=true --sbom=true -t <IMAGE> --push .
```

有关使用证明构建的更多信息，请参阅
[证明](/manuals/build/metadata/attestations/_index.md)。

如果您使用 GitHub Actions 构建和推送镜像，
请了解如何[配置操作](/manuals/build/ci/github-actions/attestations.md)
以应用 SBOM 和来源证明。

### 默认非 root 用户

默认情况下，容器以 `root` 超级用户身份运行，具有容器内的完全系统管理权限，除非 Dockerfile 指定了其他默认用户。以特权用户身份运行容器会削弱其运行时安全性，因为这意味着在容器中运行的任何代码都可以执行管理操作。

**默认非 root 用户**策略类型检测设置为默认 `root` 用户运行的镜像。要符合此策略，镜像必须在镜像配置中指定非 root 用户。如果镜像未为运行时阶段指定非 root 默认用户，则不符合此策略。

对于不符合策略的镜像，评估结果会显示 `root` 用户是否在镜像中被显式设置。这有助于您区分由 `root` 用户隐式设置的镜像和有意设置 `root` 的镜像。

以下 Dockerfile 默认以 `root` 运行，尽管未被显式设置：

```Dockerfile
FROM alpine
RUN echo "Hi"
```

而在以下情况下，`root` 用户被显式设置：

```Dockerfile
FROM alpine
USER root
RUN echo "Hi"
```

> [!NOTE]
>
> 此策略仅检查镜像配置 blob 中设置的镜像默认用户。即使您确实指定了非 root 默认用户，在运行时仍可能覆盖默认用户，例如使用 `docker run` 命令的 `--user` 标志。

要使您的镜像符合此策略，请使用
[`USER`](/reference/dockerfile.md#user) Dockerfile 指令为运行时阶段设置一个不具有 root 权限的默认用户。

以下 Dockerfile 片段显示了符合和不符合策略的镜像之间的区别。

{{< tabs >}}
{{< tab name="不符合" >}}

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
ENTRYPOINT ["/app/production"]
```

{{< /tab >}}
{{< tab name="符合" >}}

```dockerfile {hl_lines=7}
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
USER nonroot
ENTRYPOINT ["/app/production"]
```

{{< /tab >}}
{{< /tabs >}}

### 批准的基础镜像

**批准的基础镜像**策略类型确保您在构建中使用的基础镜像是维护良好且安全的。

此策略检查您在构建中使用的基础镜像是否与策略配置中指定的任何模式匹配。下表显示了此策略的几个示例模式。

| 用例                                                        | 模式                          |
| --------------------------------------------------------------- | -------------------------------- |
| 允许 Docker Hub 上的所有镜像                                | `docker.io/*`                    |
| 允许所有 Docker 官方镜像                                | `docker.io/library/*`            |
| 允许来自特定组织的镜像                       | `docker.io/orgname/*`            |
| 允许特定仓库的标签                             | `docker.io/orgname/repository:*` |
| 允许主机名为 `registry.example.com` 的注册表上的镜像 | `registry.example.com/*`         |
| 允许 NodeJS 镜像的 slim 标签                                | `docker.io/library/node:*-slim`  |

星号 (`*`) 匹配直到后续字符或镜像引用末尾的内容。注意，Docker Hub 镜像需要 `docker.io` 前缀。这是 Docker Hub 的注册表主机名。

此策略可配置以下选项：

- **批准的基础镜像源**

  指定您要允许的镜像引用模式。策略根据这些模式评估基础镜像引用。

  默认：`[*]`（任何引用都是允许的基础镜像）

- **仅支持的标签**

  使用 Docker 官方镜像时，仅允许支持的标签。

  启用此选项时，使用不支持的官方镜像标签作为基础镜像的镜像会触发策略违规。官方镜像的支持标签列在 Docker Hub 上仓库概览的**支持的标签**部分。

  默认启用。

- **仅支持的操作系统发行版**

  仅允许支持的 Linux 发行版版本的 Docker 官方镜像。

  启用此选项时，使用已达到生命周期结束的不支持 Linux 发行版（如 `ubuntu:18.04`）作为基础镜像的镜像会触发策略违规。

  启用此选项可能会导致策略在无法确定操作系统版本时报告无数据。

  默认启用。

您的镜像需要来源证明才能成功评估此策略。更多信息，请参阅[无基础镜像数据](#无基础镜像数据)。

### SonarQube 质量门禁

**SonarQube 质量门禁**策略类型基于 [SonarQube 集成](../integrations/code-quality/sonarqube.md)来评估源代码质量。此策略通过将 SonarQube 代码分析结果摄取到 Docker Scout 中来工作。

您使用 SonarQube 的 [质量门禁](https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/)定义此策略的标准。SonarQube 根据您在 SonarQube 中定义的质量门禁评估您的源代码。Docker Scout 将 SonarQube 评估作为 Docker Scout 策略展示。

Docker Scout 使用 [来源](/manuals/build/metadata/attestations/slsa-provenance.md)证明或 `org.opencontainers.image.revision` OCI 注释将 SonarQube 分析结果与容器镜像关联。除了启用 SonarQube 集成外，您还必须确保镜像具有证明或标签。

![Git 提交 SHA 将镜像与 SonarQube 分析关联](../images/scout-sq-commit-sha.webp)

推送镜像并完成策略评估后，SonarQube 质量门禁的结果将作为策略显示在 Docker Scout 仪表板和 CLI 中。

> [!NOTE]
>
> Docker Scout 只能访问集成启用后创建的 SonarQube 分析。Docker Scout 无法访问历史评估。启用集成后触发 SonarQube 分析和策略评估，以在 Docker Scout 中查看结果。

### 有效的 Docker Hardened 镜像 (DHI) 或 DHI 基础镜像

**有效的 Docker Hardened 镜像 (DHI) 或 DHI 基础镜像**策略类型确保您的镜像要么是 Docker Hardened 镜像 (DHI)，要么是使用 DHI 作为基础镜像构建的。

此策略通过检查有效的 Docker 签名验证摘要证明来验证镜像。如果以下任一情况成立，镜像被视为符合策略：

- 镜像本身是具有有效 Docker 签名验证摘要证明的 Docker Hardened 镜像，或
- 构建中使用的基础镜像（从 SLSA 来源证明识别）具有有效的 Docker 签名验证摘要证明

如果镜像缺少所需的 Docker 签名验证摘要证明，且未从具有该证明的基础镜像构建，则不符合此策略。

此策略没有可配置的参数。

## 无基础镜像数据

在某些情况下，无法确定构建中使用的基础镜像信息。在这种情况下，**最新的基础镜像**和**批准的基础镜像**策略会被标记为**无数据**。

当以下情况发生时，会出现这种"无数据"状态：

- Docker Scout 不知道您使用的基础镜像标签
- 您使用的基础镜像版本有多个标签，但并非所有标签都过时

为确保 Docker Scout 始终了解您的基础镜像，您可以在构建时附加 [来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。Docker Scout 使用来源证明来找出基础镜像。