---
title: Docker Scout 中的策略评估入门
linkTitle: 策略评估
weight: 70
keywords: scout, supply chain, vulnerabilities, packages, cves, policy
description: 'Docker Scout 中的策略让您能够为制品定义供应链规则和阈值，

  并跟踪您的制品随时间推移相对于这些要求的表现'
---

在软件供应链管理中，维护制品的安全性和可靠性是重中之重。Docker Scout 中的策略评估在现有分析功能的基础上引入了一层控制。它让您能够为制品定义供应链规则，并帮助您跟踪您的制品随时间推移相对于这些规则和阈值的表现。

了解如何使用策略评估来确保您的制品符合既定的最佳实践。

## 策略评估的工作原理

当您为仓库激活 Docker Scout 时，您推送的镜像会[自动进行分析](/manuals/scout/explore/analysis.md)。该分析让您深入了解镜像的构成，包括它们包含的软件包以及它们面临的漏洞。策略评估建立在镜像分析功能之上，根据策略定义的规则来解读分析结果。

一个策略定义了您的制品应该满足的镜像质量标准。例如，**No AGPL v3 licenses** 策略会标记任何包含根据 AGPL v3 许可证分发的软件包的镜像。如果一个镜像包含这样的软件包，该镜像就被视为不符合此策略。某些策略，如 **No AGPL v3 licenses** 策略，是可配置的。可配置的策略允许您调整标准，以更好地匹配您组织的需求。

在 Docker Scout 中，策略旨在帮助您逐步提升您的安全和供应链状况。其他工具侧重于提供通过或失败状态，而 Docker Scout 策略则可视化微小的增量变化如何影响策略状态，即使您的制品（尚未）满足策略要求。通过跟踪失败差距随时间的变化，您可以更容易地看到您的制品相对于策略是在改进还是在恶化。

策略不一定与应用安全和漏洞相关。您也可以使用策略来衡量和跟踪供应链管理的其他方面，例如开源许可证的使用和基础镜像的最新程度。

## 策略类型

在 Docker Scout 中，*策略* 源自 *策略类型*。策略类型是定义策略核心参数的模板。您可以将策略类型比作面向对象编程中的类，每个策略都是从其对应的策略类型创建的实例。

Docker Scout 支持以下策略类型：

- [基于严重性的漏洞](#基于严重性的漏洞)
- [合规许可证](#合规许可证)
- [最新的基础镜像](#最新的基础镜像)
- [高关注度漏洞](#高关注度漏洞)
- [供应链证明](#供应链证明)
- [默认非 root 用户](#默认非 root 用户)
- [批准的基础镜像](#批准的基础镜像)
- [SonarQube 质量门](#sonarqube-质量门)
- [有效的 Docker 强化镜像 (DHI) 或 DHI 基础镜像](#有效的-docker-强化镜像-dhi-或-dhi-基础镜像)

Docker Scout 会自动为已启用的仓库提供默认策略，但以下策略除外，这些策略是可选的，必须进行配置：

- **SonarQube 质量门** 策略，使用前需要[与 SonarQube 集成](/manuals/scout/integrations/code-quality/sonarqube.md)。
- **有效的 Docker 强化镜像 (DHI) 或 DHI 基础镜像** 策略，如果您想强制使用 Docker 强化镜像，则可以配置此策略。

您可以从任何受支持的策略类型创建自定义策略，或者删除不适用于您项目的默认策略。更多信息，请参阅[配置策略](./configure.md)。

<!-- vale Docker.HeadingSentenceCase = NO -->

### 基于严重性的漏洞

**基于严重性的漏洞** 策略类型检查您的制品是否暴露于已知漏洞。

默认情况下，此策略仅标记存在修复版本的关键和高危漏洞。本质上，这意味着对于未通过此策略的镜像，有一个简单的修复方法可以部署：将易受攻击的软件包升级到包含该漏洞修复的版本。

如果镜像包含一个或多个超出指定策略标准的漏洞，则被视为不符合此策略。

您可以通过创建此策略的自定义版本来配置其参数。以下策略参数可在自定义版本中配置：

- **年龄 (Age)**：漏洞首次发布以来的最少天数

  仅标记达到一定最小存在时间的漏洞的理由是，新发现的漏洞在您有机会解决它们之前，不应导致您的评估失败。

<!-- vale Vale.Spelling = NO -->
- **严重性 (Severities)**：要考虑的严重级别（默认值：`Critical, High`）
<!-- vale Vale.Spelling = YES -->

- **仅限可修复漏洞 (Fixable vulnerabilities only)**：是否仅报告存在修复版本的漏洞（默认启用）。

- **软件包类型 (Package types)**：要考虑的软件包类型列表。

  此选项允许您指定要包含在策略评估中的软件包类型，格式为 [PURL 软件包类型定义](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst)。默认情况下，策略会考虑所有软件包类型。

有关配置策略的更多信息，请参阅[配置策略](./configure.md)。

### 合规许可证

**合规许可证** 策略类型检查您的镜像是否包含在不适当许可证下分发的软件包。如果镜像包含一个或多个具有此类许可证的软件包，则被视为不符合规定。

您可以配置此策略应关注的许可证列表，并通过指定允许列表（以 PURL 形式）来添加例外情况。请参阅[配置策略](./configure.md)。

### 最新的基础镜像

**最新的基础镜像** 策略类型检查您使用的基础镜像是否为最新版本。

如果您用于构建镜像的标签指向的摘要与您使用的摘要不同，则该镜像被视为不符合此策略。如果摘要不匹配，则意味着您使用的基础镜像已过时。

您的镜像需要来源证明 (provenance attestations) 才能成功评估此策略。更多信息，请参阅[无基础镜像数据](#无基础镜像数据)。

### 高关注度漏洞

**高关注度漏洞** 策略类型检查您的镜像是否包含来自 Docker Scout 策划列表的漏洞。该列表会不断更新，包含新披露的、被广泛认为具有风险的漏洞。

该列表包括以下漏洞：

- [CVE-2014-0160 (OpenSSL Heartbleed)](https://scout.docker.com/v/CVE-2014-0160)
- [CVE-2021-44228 (Log4Shell)](https://scout.docker.com/v/CVE-2021-44228)
- [CVE-2023-38545 (cURL SOCKS5 堆缓冲区溢出)](https://scout.docker.com/v/CVE-2023-38545)
- [CVE-2023-44487 (HTTP/2 快速重置)](https://scout.docker.com/v/CVE-2023-44487)
- [CVE-2024-3094 (XZ 后门)](https://scout.docker.com/v/CVE-2024-3094)
- [CVE-2024-47176 (OpenPrinting - `cups-browsed`)](https://scout.docker.com/v/CVE-2024-47176)
- [CVE-2024-47076 (OpenPrinting - `libcupsfilters`)](https://scout.docker.com/v/CVE-2024-47076)
- [CVE-2024-47175 (OpenPrinting - `libppd`)](https://scout.docker.com/v/CVE-2024-47175)
- [CVE-2024-47177 (OpenPrinting - `cups-filters`)](https://scout.docker.com/v/CVE-2024-47177)

您可以自定义此策略，以更改哪些 CVE 被视为高关注度。自定义配置选项包括：

- **排除的 CVE (Excluded CVEs)**：指定您希望此策略忽略的 CVE。

  默认值：`[]`（不忽略任何高关注度 CVE）

- **CISA KEV**：启用对 CISA 已知被利用漏洞 (Known Exploited Vulnerabilities, KEV) 目录中漏洞的跟踪

  [CISA KEV 目录](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) 包含了在野外被积极利用的漏洞。启用后，该策略会标记包含来自 CISA KEV 目录漏洞的镜像。

  默认启用。

有关策略配置的更多信息，请参阅[配置策略](./configure.md)。

### 供应链证明

**供应链证明** 策略类型检查您的镜像是否具有 [SBOM](/manuals/build/metadata/attestations/sbom.md) 和[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。

如果镜像缺少 SBOM 证明或缺少*最大模式*来源证明，则被视为不符合规定。为确保合规，请更新您的构建命令以在构建时附加这些证明：

```console
$ docker buildx build --provenance=true --sbom=true -t <IMAGE> --push .
```

有关使用证明进行构建的更多信息，请参阅[证明](/manuals/build/metadata/attestations/_index.md)。

如果您使用 GitHub Actions 来构建和推送镜像，请了解如何[配置该操作](/manuals/build/ci/github-actions/attestations.md)以应用 SBOM 和来源证明。

### 默认非 root 用户

默认情况下，容器以 `root` 超级用户身份运行，在容器内拥有完整的系统管理权限，除非 Dockerfile 指定了不同的默认用户。以特权用户身份运行容器会削弱其运行时安全性，因为这意味着在容器中运行的任何代码都可以执行管理操作。

**默认非 root 用户** 策略类型检测设置为以默认 `root` 用户身份运行的镜像。要符合此策略，镜像必须在镜像配置中指定一个非 root 用户。如果镜像没有为运行时阶段指定非 root 默认用户，则被视为不符合此策略。

对于不符合规定的镜像，评估结果会显示 `root` 用户是否被显式设置。这有助于您区分由 `root` 用户隐式设置的镜像和故意设置 `root` 的镜像造成的策略违规。

以下 Dockerfile 默认以 `root` 运行，尽管没有显式设置：

```Dockerfile
FROM alpine
RUN echo "Hi"
```

而在以下情况下，`root` 用户是显式设置的：

```Dockerfile
FROM alpine
USER root
RUN echo "Hi"
```

> [!NOTE]
>
> 此策略仅检查镜像的默认用户，该用户在镜像配置数据块中设置。即使您确实指定了非 root 默认用户，仍然可以在运行时覆盖默认用户，例如通过为 `docker run` 命令使用 `--user` 标志。

要使您的镜像符合此策略，请使用 [`USER`](/reference/dockerfile.md#user) Dockerfile 指令为运行时阶段设置一个没有 root 权限的默认用户。

以下 Dockerfile 片段展示了符合规定和不符合规定的镜像之间的区别。

{{< tabs >}}
{{< tab name="不符合规定" >}}

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
ENTRYPOINT ["/app/production"]
```

{{< /tab >}}
{{< tab name="符合规定" >}}

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

**批准的基础镜像** 策略类型确保您在构建中使用的基础镜像是经过维护且安全的。

此策略检查您构建中使用的基础镜像是否与策略配置中指定的任何模式匹配。下表显示了此策略的一些示例模式。

| 用例 | 模式 |
| --------------------------------------------------------------- | -------------------------------- |
| 允许来自 Docker Hub 的所有镜像 | `docker.io/*` |
| 允许所有 Docker 官方镜像 | `docker.io/library/*` |
| 允许来自特定组织的镜像 | `docker.io/orgname/*` |
| 允许特定仓库的标签 | `docker.io/orgname/repository:*` |
| 允许主机名为 `registry.example.com` 的注册中心上的镜像 | `registry.example.com/*` |
| 允许 NodeJS 镜像的 slim 标签 | `docker.io/library/node:*-slim` |

星号 (`*`) 匹配直到后面的字符，或者直到镜像引用的末尾。请注意，需要 `docker.io` 前缀才能匹配 Docker Hub 镜像。这是 Docker Hub 的注册中心主机名。

此策略可通过以下选项进行配置：

- **批准的基础镜像来源 (Approved base image sources)**

  指定您要允许的镜像引用模式。策略会根据这些模式评估基础镜像引用。

  默认值：`[*]`（任何引用都是允许的基础镜像）

- **仅限支持的标签 (Only supported tags)**

  使用 Docker 官方镜像时，仅允许支持的标签。

  启用此选项后，使用官方镜像的不支持标签作为其基础镜像的镜像会触发策略违规。官方镜像的支持标签在 Docker Hub 上的仓库概览的**支持的标签 (Supported tags)** 部分列出。

  默认启用。

- **仅限支持的操作系统发行版 (Only supported OS distributions)**

  仅允许支持的 Linux 发行版版本的 Docker 官方镜像。

  启用此选项后，使用已达到生命周期结束的不支持的 Linux 发行版（如 `ubuntu:18.04`）的镜像会触发策略违规。

  启用此选项可能会导致策略报告无数据，如果无法确定操作系统版本。

  默认启用。

您的镜像需要来源证明才能成功评估此策略。更多信息，请参阅[无基础镜像数据](#无基础镜像数据)。

### SonarQube 质量门

**SonarQube 质量门** 策略类型建立在 [SonarQube 集成](../integrations/code-quality/sonarqube.md) 之上，用于评估您的源代码质量。此策略的工作原理是将 SonarQube 代码分析结果导入 Docker Scout。

您使用 SonarQube 的[质量门](https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/) 定义此策略的标准。SonarQube 根据您在 SonarQube 中定义的质量门评估您的源代码。Docker Scout 将 SonarQube 评估作为 Docker Scout 策略呈现。

Docker Scout 使用[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md) 或 `org.opencontainers.image.revision` OCI 注解将 SonarQube 分析结果与容器镜像关联起来。除了启用 SonarQube 集成外，您还必须确保您的镜像具有证明或标签。

![Git commit SHA 将镜像与 SonarQube 分析链接起来](../images/scout-sq-commit-sha.webp)

一旦您推送镜像并完成策略评估，SonarQube 质量门的结果将作为策略显示在 Docker Scout 仪表板和 CLI 中。

> [!NOTE]
>
> Docker Scout 只能访问启用集成后创建的 SonarQube 分析。Docker Scout 无法访问历史评估。启用集成后，触发 SonarQube 分析和策略评估，以在 Docker Scout 中查看结果。

### 有效的 Docker 强化镜像 (DHI) 或 DHI 基础镜像

**有效的 Docker 强化镜像 (DHI) 或 DHI 基础镜像** 策略类型确保您的镜像是 Docker 强化镜像 (DHI)，或者是使用 DHI 作为基础镜像构建的。

此策略通过检查有效的 Docker 签名验证摘要证明来验证镜像。如果满足以下任一条件，策略即认为镜像符合规定：

- 镜像本身是具有有效 Docker 签名验证摘要证明的 Docker 强化镜像，或者
- 构建中使用的基础镜像（从 SLSA 来源证明中识别）具有有效的 Docker 签名验证摘要证明

如果镜像缺少所需的 Docker 签名验证摘要证明，并且不是从具有此类证明的基础镜像构建的，则该镜像不符合此策略。

此策略没有可配置的参数。

## 无基础镜像数据

在某些情况下，无法确定有关构建中使用的基础镜像的信息。在这种情况下，**最新的基础镜像**和**批准的基础镜像**策略会被标记为**无数据**。

当出现以下情况时，会发生这种“无数据”状态：

- Docker Scout 不知道您使用了哪个基础镜像标签
- 您使用的版本有多个标签，但并非所有标签都已过时

为确保 Docker Scout 始终了解您的基础镜像，您可以在构建时附加[来源证明](/manuals/build/metadata/attestations/slsa-provenance.md)。Docker Scout 使用来源证明来找出基础镜像版本。