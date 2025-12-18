---
description: Docker 安全公告
keywords: Docker, CVE, 安全, 通知, Log4J 2, Log4Shell, Text4Shell, 公告
title: Docker 安全公告
linkTitle: 安全公告
outputs: ["HTML", "markdown", "RSS"]
type: "security-announcements"
weight: 80
toc_min: 1
toc_max: 2
---

{{< rss-button feed="/security/security-announcements/index.xml" text="订阅安全 RSS 源" >}}

## Docker Desktop 4.54.0 安全更新：CVE-2025-13743

Docker Desktop 中的一个漏洞已在 12 月 4 日的 [4.54.0](/manuals/desktop/release-notes.md#4540) 版本中修复：

- 修复了 [CVE-2025-13743](https://www.cve.org/cverecord?id=CVE-2025-13743)，Docker Desktop 诊断包因错误对象序列化而在日志输出中包含过期的 Hub PAT。

## Docker Desktop 4.49.0 安全更新：CVE-2025-9164

Windows 版 Docker Desktop 中的一个漏洞已在 10 月 23 日的 [4.49.0](/manuals/desktop/release-notes.md#4490) 版本中修复：

- 修复了 [CVE-2025-9164](https://www.cve.org/cverecord?id=CVE-2025-9164)，Windows 版 Docker Desktop 安装程序因 DLL 搜索顺序不安全而易受 DLL 劫持攻击。安装程序在检查系统目录之前会先搜索用户下载文件夹中的所需 DLL，这可能导致通过恶意 DLL 放置实现本地权限提升。

## Docker Desktop 4.47.0 安全更新：CVE-2025-10657

Docker Desktop 中的一个漏洞已在 9 月 25 日的 [4.47.0](/manuals/desktop/release-notes.md#4470) 版本中修复：

- 修复了 [CVE-2025-10657](https://www.cve.org/CVERecord?id=CVE-2025-10657)，增强容器隔离（Enhanced Container Isolation）的 Docker Socket 命令限制功能在 Docker Desktop 4.46.0 版本中无法正常工作（其配置被忽略）。

## Docker Desktop 4.44.3 安全更新：CVE-2025-9074

_最后更新时间：2025 年 8 月 20 日_

Docker Desktop 中的一个漏洞已在 8 月 20 日的 [4.44.3](/manuals/desktop/release-notes.md#4443) 版本中修复：

- 修复了 [CVE-2025-9074](https://www.cve.org/CVERecord?id=CVE-2025-9074)，恶意容器可能通过 Docker Desktop 访问 Docker Engine 并启动额外容器，无需挂载 Docker Socket。这可能导致对主机系统上用户文件的未授权访问。增强容器隔离（ECI）无法缓解此漏洞。

## Docker Desktop 4.44.0 安全更新：CVE-2025-23266

_最后更新时间：2025 年 7 月 31 日_

我们注意到 [CVE-2025-23266](https://nvd.nist.gov/vuln/detail/CVE-2025-23266)，这是一个影响 NVIDIA Container Toolkit 在 CDI 模式下的严重漏洞，影响版本低于 1.17.7。Docker Desktop 包含版本 1.17.8，不受影响。但是，如果手动启用了 CDI 模式，使用早期工具包版本的旧版 Docker Desktop 可能会受到影响。请升级到 Docker Desktop 4.44 或更高版本，以确保使用已修复的版本。

## Docker Desktop 4.43.0 安全更新：CVE-2025-6587

_最后更新时间：2025 年 7 月 03 日_

Docker Desktop 中的一个漏洞已在 7 月 03 日的 [4.43.0](/manuals/desktop/release-notes.md#4430) 版本中修复：

- 修复了 [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587)，敏感的系统环境变量被包含在 Docker Desktop 诊断日志中，可能导致密钥泄露。

## Docker Desktop 4.41.0 安全更新：CVE-2025-3224、CVE-2025-4095 和 CVE-2025-3911

_最后更新时间：2025 年 5 月 15 日_

Docker Desktop 中的三个漏洞已在 4 月 28 日的 [4.41.0](/manuals/desktop/release-notes.md#4410) 版本中修复：

- 修复了 [CVE-2025-3224](https://www.cve.org/CVERecord?id=CVE-2025-3224)，攻击者在用户机器上可通过 Docker Desktop 更新实现权限提升。
- 修复了 [CVE-2025-4095](https://www.cve.org/CVERecord?id=CVE-2025-4095)，当使用 MacOS 配置文件时，注册表访问管理（RAM）策略未被强制执行，允许用户从未经批准的注册表拉取镜像。
- 修复了 [CVE-2025-3911](https://www.cve.org/CVERecord?id=CVE-2025-3911)，攻击者在获得用户机器的读取权限后，可从 Docker Desktop 日志文件中获取敏感信息，包括为运行容器配置的环境变量。

我们强烈建议您升级到 Docker Desktop [4.41.0](/manuals/desktop/release-notes.md#4410)。

## Docker Desktop 4.34.2 安全更新：CVE-2024-8695 和 CVE-2024-8696

_最后更新时间：2024 年 9 月 13 日_

Cure53 报告了 Docker Desktop 中与 Docker Extensions 相关的两个远程代码执行（RCE）漏洞，已在 9 月 12 日的 [4.34.2](/manuals/desktop/release-notes.md#4342) 版本中修复。

- [CVE-2024-8695](https://www.cve.org/cverecord?id=CVE-2024-8695)：通过精心构造的扩展描述/变更日志可实现远程代码执行（RCE）漏洞，恶意扩展可在 Docker Desktop 4.34.2 之前版本中利用。[严重]
- [CVE-2024-8696](https://www.cve.org/cverecord?id=CVE-2024-8696)：通过精心构造的扩展发布者 URL/附加 URL 可实现远程代码执行（RCE）漏洞，恶意扩展可在 Docker Desktop 4.34.2 之前版本中利用。[高危]

Extensions Marketplace 中未发现利用这些漏洞的现有扩展。Docker 团队将密切监控并仔细审查任何发布新扩展的请求。

我们强烈建议您升级到 Docker Desktop [4.34.2](/manuals/desktop/release-notes.md#4342)。如果您无法及时升级，可以[禁用 Docker Extensions](/manuals/extensions/settings-feedback.md#turn-on-or-turn-off-extensions)作为临时解决方案。

## CLI 密码登录在 SSO 强制执行时的弃用

_最后更新时间：2024 年 7 月_

首次引入[SSO 强制执行](/manuals/enterprise/security/single-sign-on/connect.md)时，Docker 提供了一个宽限期，允许在 Docker CLI 认证到 Docker Hub 时继续使用密码。这是为了让组织能够更轻松地使用 SSO 强制执行。建议配置 SSO 的管理员鼓励使用 CLI 的用户[切换到个人访问令牌（PAT）](/manuals/enterprise/security/single-sign-on/_index.md#prerequisites)，以应对宽限期结束。

2024 年 9 月 16 日宽限期结束后，当 SSO 强制执行时，密码将无法再通过 Docker CLI 认证到 Docker Hub。受影响的用户需要切换到使用 PAT 才能继续登录。

在 Docker，我们希望为开发者和组织提供最安全的体验，这一弃用是朝着这个方向迈出的重要一步。

## SOC 2 Type 2 认证和 ISO 27001 认证

_最后更新时间：2024 年 6 月_

Docker 很高兴地宣布，我们已获得 SOC 2 Type 2 认证和 ISO 27001 认证，无任何例外或重大不符合项。

安全是我们 Docker 运营的基本支柱，它融入到我们的整体使命和公司战略中。Docker 的产品是我们用户社区的核心，我们的 SOC 2 Type 2 认证和 ISO 27001 认证展示了 Docker 对用户群体的持续安全承诺。

更多信息，请参阅[博客公告](https://www.docker.com/blog/docker-announces-soc-2-type-2-attestation-iso-27001-certification/)。

## Docker 安全公告：runc、BuildKit 和 Moby 中的多个漏洞

_最后更新时间：2024 年 2 月 2 日_

我们 Docker 始终将软件安全和完整性以及用户的信任放在首位。Snyk Labs 的安全研究人员发现并报告了容器生态系统中的四个安全漏洞。其中一个漏洞 [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626) 涉及 runc 容器运行时，其他三个影响 BuildKit（[CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651)、[CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652) 和 [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653)）。我们想向社区保证，我们的团队与报告者和开源维护者密切合作，一直在协调并实施必要的修复措施。

我们致力于保持最高的安全标准。我们已在 1 月 31 日发布了修补后的 runc、BuildKit 和 Moby 版本，并在 2 月 1 日发布了 Docker Desktop 更新以解决这些漏洞。此外，我们最新的 BuildKit 和 Moby 版本还修复了由独立研究人员发现的 [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650) 和通过 Docker 内部研究计划发现的 [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557)。

|                        | 受影响的版本         |
|:-----------------------|:--------------------------|
| `runc`                 | <= 1.1.11                 |
| `BuildKit`             | <= 0.12.4                 |
| `Moby (Docker Engine)` | <= 25.0.1 和 <= 24.0.8   |
| `Docker Desktop`       | <= 4.27.0                 |

### 如果您使用的是受影响版本，应该怎么做？

如果您使用的是受影响的 runc、BuildKit、Moby 或 Docker Desktop 版本，请确保升级到最新版本，链接在下表中：

|                        | 修补后的版本          |
|:-----------------------|:--------------------------|
| `runc`                 | >= [1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12)                 |
| `BuildKit`             | >= [0.12.5](https://github.com/moby/buildkit/releases/tag/v0.12.5)                 |
| `Moby (Docker Engine)` | >= [25.0.2](https://github.com/moby/moby/releases/tag/v25.0.2) 和 >= [24.0.9](https://github.com/moby/moby/releases/tag/v24.0.9)   |
| `Docker Desktop`       | >= [4.27.1](/manuals/desktop/release-notes.md#4271)                 |

如果您无法及时升级到不受影响的版本，请遵循以下最佳实践以降低风险：

* 仅使用受信任的 Docker 镜像（例如 [Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images)）。
* 不要从不受信任的源或不受信任的 Dockerfile 构建 Docker 镜像。
* 如果您是使用 Docker Desktop 的 Docker Business 客户且无法升级到 v4.27.1，请确保启用 [Hardened Docker Desktop](/manuals/enterprise/security/hardened-desktop/_index.md) 功能，例如：
  * [增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)，这可以减轻 CVE-2024-21626 在运行恶意镜像容器时的影响。
  * [镜像访问管理](/manuals/enterprise/security/hardened-desktop/image-access-management.md) 和 [注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md)，这些功能让组织能够控制用户可以访问哪些镜像和仓库。
* 对于 CVE-2024-23650、CVE-2024-23651、CVE-2024-23652 和 CVE-2024-23653，避免使用不受信任源的 BuildKit 前端。前端镜像通常在 Dockerfile 的 #syntax 行中指定，或使用 `buildctl build` 命令的 `--frontend` 标志指定。
* 为缓解 CVE-2024-24557，请确保使用 BuildKit 或在构建镜像时禁用缓存。从 CLI 可以通过 `DOCKER_BUILDKIT=1` 环境变量（如果安装了 buildx 插件，Moby >= v23.0 的默认值）或 `--no-cache` 标志完成。如果您直接使用 HTTP API 或通过客户端使用，可以通过为 [/build API 端点](https://docs.docker.com/reference/api/engine/version/v1.44/#tag/Image/operation/ImageBuild) 设置 `nocache` 为 `true` 或 `version` 为 `2` 来实现相同效果。

### 技术细节和影响

#### CVE-2024-21626（高危）

在 runc v1.1.11 及更早版本中，由于某些泄露的文件描述符，攻击者可以通过导致新启动的容器进程（来自 `runc exec`）的工作目录位于主机文件系统命名空间中，或通过诱骗用户运行恶意镜像并允许容器进程通过 `runc run` 访问主机文件系统来获得主机文件系统的访问权限。这些攻击也可以适应覆盖半任意主机二进制文件，从而允许完全的容器逃逸。请注意，当使用高级运行时（如 Docker 或 Kubernetes）时，可以通过运行恶意容器镜像（无需额外配置）或在启动容器时传递特定工作目录选项来利用此漏洞。在 Docker 的情况下，该漏洞也可以从 Dockerfile 内部被利用。

_该问题已在 runc v1.1.12 中修复。_

#### CVE-2024-23651（高危）

在 BuildKit <= v0.12.4 中，两个共享相同缓存挂载且具有子路径的恶意构建步骤并行运行时可能引发竞争条件，导致主机系统文件可被构建容器访问。这只会在用户尝试构建恶意项目的 Dockerfile 时发生。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23652（高危）

在 BuildKit <= v0.12.4 中，恶意 BuildKit 前端或使用 `RUN --mount` 的 Dockerfile 可能会欺骗该功能，该功能会移除为挂载点创建的空文件，从而移除主机系统外部的文件。这只会在用户使用恶意 Dockerfile 时发生。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23653（高危）

除了将容器作为构建步骤运行外，BuildKit 还提供了基于已构建镜像运行交互式容器的 API。在 BuildKit <= v0.12.4 中，可以使用这些 API 请求 BuildKit 运行具有提升权限的容器。通常，只有在 buildkitd 配置中启用了特殊的 `security.insecure` 权限并且初始化构建请求的用户允许时，才允许运行此类容器。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23650（中危）

在 BuildKit <= v0.12.4 中，恶意 BuildKit 客户端或前端可以构造一个请求，导致 BuildKit 守护进程崩溃并引发恐慌。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-24557（中危）

在 M