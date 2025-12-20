# Docker 安全公告



<button
  onclick="window.open('\/security\/security-announcements\/index.xml', '_blank')"
  data-heap-id="rss-subscribe-button"
  class="inline-flex items-center gap-2 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-900 py-2 px-3 text-sm transition-colors"
>
  <span class="icon-svg text-base leading-none">
    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M195-120q-31 0-53-22t-22-53q0-31 22-53t53-22q31 0 53 22t22 53q0 31-22 53t-53 22Zm560 0q-20 0-32.5-14T708-168q-9-109-54-203T537-537q-72-72-166-117t-203-54q-20-2-34-14.5T120-755q0-20 15-32.5t35-10.5q127 9 236.5 60.5T601-601q85 85 136.5 194.5T798-170q2 20-10.5 35T755-120Zm-258 0q-19 0-32.5-13.5T449-167q-8-57-32-106t-62-87q-38-38-85.5-63.5T166-457q-19-3-32.5-16T120-505q0-19 13.5-32t31.5-11q75 8 139.5 40.5T419-424q50 51 81.5 117.5T540-165q2 19-11 32t-32 13Z"/></svg>
  </span>
  <div class="leading-tight">
    <div class="text-base">订阅安全 RSS 源</div>
  </div>
</button>

## Docker Desktop 4.54.0 安全更新：CVE-2025-13743

Docker Desktop 中的一个漏洞已于 12 月 4 日在 [4.54.0](/manuals/desktop/release-notes.md#4540) 版本中修复：

- 修复了 [CVE-2025-13743](https://www.cve.org/cverecord?id=CVE-2025-13743)，该漏洞导致 Docker Desktop 诊断包因错误对象序列化而在日志输出中包含过期的 Hub PAT。

## Docker Desktop 4.49.0 安全更新：CVE-2025-9164

Windows 版 Docker Desktop 中的一个漏洞已于 10 月 23 日在 [4.49.0](/manuals/desktop/release-notes.md#4490) 版本中修复：

- 修复了 [CVE-2025-9164](https://www.cve.org/cverecord?id=CVE-2025-9164)，该漏洞导致 Windows 版 Docker Desktop 安装程序因 DLL 搜索顺序不安全而易受 DLL 劫持攻击。安装程序在检查系统目录之前会先在用户的 Downloads 文件夹中搜索所需的 DLL，这可能导致通过恶意 DLL 放置实现本地权限提升。

## Docker Desktop 4.47.0 安全更新：CVE-2025-10657

Docker Desktop 中的一个漏洞已于 9 月 25 日在 [4.47.0](/manuals/desktop/release-notes.md#4470) 版本中修复：

- 修复了 [CVE-2025-10657](https://www.cve.org/CVERecord?id=CVE-2025-10657)，该漏洞导致增强容器隔离（Enhanced Container Isolation）的 [Docker Socket 命令限制](../enterprise/security/hardened-desktop/enhanced-container-isolation/config.md#command-restrictions) 功能在仅 Docker Desktop 4.46.0 版本中无法正常工作（其配置被忽略）。

## Docker Desktop 4.44.3 安全更新：CVE-2025-9074

_最后更新时间：2025 年 8 月 20 日_

Docker Desktop 中的一个漏洞已于 8 月 20 日在 [4.44.3](/manuals/desktop/release-notes.md#4443) 版本中修复：

- 修复了 [CVE-2025-9074](https://www.cve.org/CVERecord?id=CVE-2025-9074)，该漏洞导致在 Docker Desktop 上运行的恶意容器可以在不需要挂载 Docker socket 的情况下访问 Docker Engine 并启动其他容器。这可能导致对主机系统上用户文件的未授权访问。增强容器隔离（ECI）无法缓解此漏洞。

## Docker Desktop 4.44.0 安全更新：CVE-2025-23266

_最后更新时间：2025 年 7 月 31 日_

我们注意到 [CVE-2025-23266](https://nvd.nist.gov/vuln/detail/CVE-2025-23266)，这是一个影响 CDI 模式下 NVIDIA Container Toolkit 1.17.7 及更早版本的严重漏洞。Docker Desktop 包含 1.17.8 版本，不受影响。但是，如果手动启用了 CDI 模式，捆绑了早期工具包版本的旧版 Docker Desktop 可能会受到影响。请升级到 Docker Desktop 4.44 或更高版本，以确保使用的是已修复的版本。

## Docker Desktop 4.43.0 安全更新：CVE-2025-6587

_最后更新时间：2025 年 7 月 03 日_

Docker Desktop 中的一个漏洞已于 7 月 03 日在 [4.43.0](/manuals/desktop/release-notes.md#4430) 版本中修复：

- 修复了 [CVE-2025-6587](https://www.cve.org/CVERecord?id=CVE-2025-6587)，该漏洞导致敏感的系统环境变量被包含在 Docker Desktop 诊断日志中，可能导致密钥泄露。

## Docker Desktop 4.41.0 安全更新：CVE-2025-3224、CVE-2025-4095 和 CVE-2025-3911

_最后更新时间：2025 年 5 月 15 日_

Docker Desktop 中的三个漏洞已于 4 月 28 日在 [4.41.0](/manuals/desktop/release-notes.md#4410) 版本中修复。

- 修复了 [CVE-2025-3224](https://www.cve.org/CVERecord?id=CVE-2025-3224)，该漏洞允许攻击者在 Docker Desktop 更新时通过访问用户机器来提升权限。
- 修复了 [CVE-2025-4095](https://www.cve.org/CVERecord?id=CVE-2025-4095)，该漏洞导致在使用 MacOS 配置文件时，注册表访问管理（RAM）策略未被强制执行，允许用户从未经批准的注册表拉取镜像。
- 修复了 [CVE-2025-3911](https://www.cve.org/CVERecord?id=CVE-2025-3911)，该漏洞允许具有用户机器读取权限的攻击者从 Docker Desktop 日志文件中获取敏感信息，包括为运行容器配置的环境变量。

我们强烈建议您升级到 Docker Desktop [4.41.0](/manuals/desktop/release-notes.md#4410)。

## Docker Desktop 4.34.2 安全更新：CVE-2024-8695 和 CVE-2024-8696

_最后更新时间：2024 年 9 月 13 日_

Cure53 报告了 Docker Desktop 中与 Docker Extensions 相关的两个远程代码执行（RCE）漏洞，并已于 9 月 12 日在 [4.34.2](/manuals/desktop/release-notes.md#4342) 版本中修复。

- [CVE-2024-8695](https://www.cve.org/cverecord?id=CVE-2024-8695)：通过精心制作的扩展描述/变更日志可能导致远程代码执行（RCE）的漏洞，可能被 Docker Desktop 4.34.2 之前的恶意扩展滥用。[严重]
- [CVE-2024-8696](https://www.cve.org/cverecord?id=CVE-2024-8696)：通过精心制作的扩展发布者 URL/附加 URL 可能导致远程代码执行（RCE）的漏洞，可能被 Docker Desktop 4.34.2 之前的恶意扩展滥用。[高]

Extensions Marketplace 中未发现利用这些漏洞的现有扩展。Docker 团队将密切监控并仔细审查任何发布新扩展的请求。

我们强烈建议您升级到 Docker Desktop [4.34.2](/manuals/desktop/release-notes.md#4342)。如果您无法及时升级，可以[禁用 Docker Extensions](/manuals/extensions/settings-feedback.md#turn-on-or-turn-off-extensions) 作为临时解决方案。

## CLI 密码登录在 SSO 强制时的弃用

_最后更新时间：2024 年 7 月_

首次引入 [SSO 强制](/manuals/enterprise/security/single-sign-on/connect.md) 时，Docker 提供了一个宽限期，允许在 Docker CLI 认证到 Docker Hub 时继续使用密码。这是为了方便组织更轻松地使用 SSO 强制。建议配置 SSO 的管理员鼓励使用 CLI 的用户[切换到个人访问令牌（PAT）](/manuals/enterprise/security/single-sign-on/_index.md#prerequisites)，以应对宽限期结束。

2024 年 9 月 16 日，宽限期将结束，当 SSO 强制时，密码将无法再通过 Docker CLI 认证到 Docker Hub。受影响的用户需要切换到使用 PAT 才能继续登录。

在 Docker，我们希望为开发者和组织提供最安全的体验，这一弃用是我们朝着这个方向迈出的关键一步。

## SOC 2 Type 2 认证和 ISO 27001 认证

_最后更新时间：2024 年 6 月_

Docker 很高兴地宣布，我们已获得 SOC 2 Type 2 认证和 ISO 27001 认证，无任何例外或重大不符合项。

安全是我们运营的基本支柱，它融入到我们的整体使命和公司战略中。Docker 的产品是用户社区的核心，我们的 SOC 2 Type 2 认证和 ISO 27001 认证展示了 Docker 对用户群体持续的安全承诺。

更多信息，请参阅 [博客公告](https://www.docker.com/blog/docker-announces-soc-2-type-2-attestation-iso-27001-certification/)。

## Docker 安全公告：runc、BuildKit 和 Moby 中的多个漏洞

_最后更新时间：2024 年 2 月 2 日_

我们 Docker 团队高度重视软件的安全性和完整性，以及用户的信任。Snyk Labs 的安全研究人员发现并报告了容器生态系统中的四个安全漏洞。其中一个漏洞 [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626) 涉及 runc 容器运行时，其他三个影响 BuildKit（[CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651)、[CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652) 和 [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653)）。我们想向社区保证，我们的团队与报告者和开源维护者密切合作，一直在努力协调和实施必要的修复措施。

我们致力于维护最高安全标准。我们已在 1 月 31 日发布了修复版本的 runc、BuildKit 和 Moby，并在 2 月 1 日发布了 Docker Desktop 的更新，以解决这些漏洞。此外，我们最新的 BuildKit 和 Moby 版本还包括对 [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650) 和 [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557) 的修复，分别由独立研究人员和通过 Docker 的内部研究计划发现。

|                        | 受影响的版本         |
|:-----------------------|:--------------------------|
| `runc`                 | <= 1.1.11                 |
| `BuildKit`             | <= 0.12.4                 |
| `Moby (Docker Engine)` | <= 25.0.1 和 <= 24.0.8   |
| `Docker Desktop`       | <= 4.27.0                 |

### 如果您使用的是受影响的版本，应该怎么做？

如果您使用的是受影响的 runc、BuildKit、Moby 或 Docker Desktop 版本，请确保升级到最新版本，链接在下表中：

|                        | 已修复的版本          |
|:-----------------------|:--------------------------|
| `runc`                 | >= [1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12)                 |
| `BuildKit`             | >= [0.12.5](https://github.com/moby/buildkit/releases/tag/v0.12.5)                 |
| `Moby (Docker Engine)` | >= [25.0.2](https://github.com/moby/moby/releases/tag/v25.0.2) 和 >= [24.0.9](https://github.com/moby/moby/releases/tag/v24.0.9)   |
| `Docker Desktop`       | >= [4.27.1](/manuals/desktop/release-notes.md#4271)                 |

如果您无法及时升级到不受影响的版本，请遵循以下最佳实践以降低风险：

* 仅使用受信任的 Docker 镜像（例如 [Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images)）。
* 不要从不受信任的来源或不受信任的 Dockerfile 构建 Docker 镜像。
* 如果您是使用 Docker Desktop 的 Docker Business 客户且无法升级到 v4.27.1，请确保启用 [Hardened Docker Desktop](/manuals/enterprise/security/hardened-desktop/_index.md) 功能，例如：
  * [增强容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/_index.md)，这可以减轻在运行恶意镜像容器时 CVE-2024-21626 的影响。
  * [镜像访问管理](/manuals/enterprise/security/hardened-desktop/image-access-management.md) 和 [注册表访问管理](/manuals/enterprise/security/hardened-desktop/registry-access-management.md)，这些功能让组织能够控制用户可以访问哪些镜像和仓库。
* 对于 CVE-2024-23650、CVE-2024-23651、CVE-2024-23652 和 CVE-2024-23653，避免使用来自不受信任来源的 BuildKit 前端。前端镜像通常在 Dockerfile 的 #syntax 行中指定，或在使用 `buildctl build` 命令时使用 `--frontend` 标志指定。
* 为了缓解 CVE-2024-24557，请确保使用 BuildKit 或在构建镜像时禁用缓存。从 CLI 可以通过 `DOCKER_BUILDKIT=1` 环境变量（如果安装了 buildx 插件，Moby >= v23.0 的默认值）或 `--no-cache` 标志完成。如果您直接使用 HTTP API 或通过客户端使用，可以通过将 [/build API 端点](https://docs.docker.com/reference/api/engine/version/v1.44/#tag/Image/operation/ImageBuild) 的 `nocache` 设置为 `true` 或将 `version` 设置为 `2` 来实现相同的效果。

### 技术细节和影响

#### CVE-2024-21626（高）

在 runc v1.1.11 及更早版本中，由于某些泄露的文件描述符，攻击者可以通过导致新启动的容器进程（来自 `runc exec`）在其工作目录位于主机文件系统命名空间中，或通过诱骗用户运行恶意镜像并允许容器进程通过 `runc run` 访问主机文件系统来获得对主机文件系统的访问权限。这些攻击也可以适应以覆盖半任意主机二进制文件，从而允许完全的容器逃逸。注意，当使用高级运行时（如 Docker 或 Kubernetes）时，此漏洞可以通过运行恶意容器镜像（无需额外配置）或在启动容器时传递特定工作目录选项来利用。在 Docker 的情况下，也可以通过 Dockerfile 适应这种攻击。

_该问题已在 runc v1.1.12 中修复。_

#### CVE-2024-23651（高）

在 BuildKit <= v0.12.4 中，两个恶意构建步骤并行运行，共享带有子路径的缓存挂载，可能导致竞争条件，导致主机系统文件可被构建容器访问。这只会在用户尝试构建恶意项目的 Dockerfile 时发生。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23652（高）

在 BuildKit <= v0.12.4 中，恶意 BuildKit 前端或使用 `RUN --mount` 的 Dockerfile 可以欺骗功能，该功能会移除为空挂载点创建的空文件，从而移除主机系统外部的文件。这只会在用户使用恶意 Dockerfile 时发生。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23653（高）

除了将容器作为构建步骤运行外，BuildKit 还提供了基于已构建镜像运行交互式容器的 API。在 BuildKit <= v0.12.4 中，可以使用这些 API 请求 BuildKit 运行具有提升权限的容器。通常，只有在 buildkitd 配置中启用特殊 `security.insecure` 权限并由初始化构建请求的用户允许时，才允许运行此类容器。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-23650（中）

在 BuildKit <= v0.12.4 中，恶意 BuildKit 客户端或前端可以构造一个请求，导致 BuildKit 守护进程崩溃并引发 panic。

_该问题已在 BuildKit v0.12.5 中修复。_

#### CVE-2024-24557（中）

在 Moby <= v25.0.1 和 <= v24.0.8 中，经典构建器缓存系统容易受到缓存投毒，如果镜像从 scratch 构建。此外，某些指令（最重要的是 `HEALTHCHECK` 和 `ONBUILD`）的更改不会导致缓存未命中。攻击者如果知道某人使用的 Dockerfile，可以通过制作一个特别的镜像来毒化其缓存，该镜像将被视为某些构建步骤的有效缓存候选。

_该问题已在 Moby >= v25.0.2 和 >= v24.0.9 中修复。_

### Docker 产品如何受影响？

#### Docker Desktop

Docker Desktop v4.27.0 及更早版本受影响。Docker Desktop v4.27.1 于 2 月 1 日发布，包含已修补的 runc、BuildKit 和 dockerd 二进制文件。除了升级到此新版本外，我们还鼓励所有 Docker 用户仔细使用 Docker 镜像和 Dockerfile，并确保仅在构建中使用受信任的内容。

一如既往，在更新之前，请检查 Docker Desktop 系统要求，以确保与您的操作系统（[Windows](/manuals/desktop/setup/install/windows-install.md#system-requirements)、[Linux](/manuals/desktop/setup/install/linux/_index.md#general-system-requirements)、[Mac](/manuals/desktop/setup/install/mac-install.md#system-requirements)）完全兼容。

#### Docker Build Cloud

任何新的 Docker Build Cloud 构建器实例都将使用最新的 Docker Engine 和 BuildKit 版本进行配置，因此不会受到这些 CVE 的影响。更新也已部署到现有的 Docker Build Cloud 构建器。

_没有其他 Docker 产品受这些漏洞影响。_

### 公告链接

* Runc
  * [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
* BuildKit
  * [CVE-2024-23650](https://github.com/moby/buildkit/security/advisories/GHSA-9p26-698r-w4hx)
  * [CVE-2024-23651](https://github.com/moby/buildkit/security/advisories/GHSA-m3r6-h7wv-7xxv)
  * [CVE-2024-23652](https://github.com/moby/buildkit/security/advisories/GHSA-4v98-7qmw-rqr8)
  * [CVE-2024-23653](https://github.com/moby/buildkit/security/advisories/GHSA-wr6v-9f75-vh2g)
* Moby
  * [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

## Text4Shell CVE-2022-42889

_最后更新时间：2022 年 10 月_

在流行的 Apache Commons Text 库中发现了 [CVE-2022-42889](https://nvd.nist.gov/vuln/detail/CVE-2022-42889)。此漏洞影响 1.10.0 之前的所有版本。

我们强烈建议您将 [Apache Commons Text](https://commons.apache.org/proper/commons-text/download_text.cgi) 升级到最新版本。

### 扫描 Docker Hub 上的镜像

2021 年 10 月 21 日 1200 UTC 之后触发的 Docker Hub 安全扫描现在可以正确识别 Text4Shell CVE。在此之前触发的扫描目前不反映此漏洞的状态。因此，我们建议您通过向 Docker Hub 推送新镜像来触发扫描，以查看 Text4Shell CVE 在漏洞报告中的状态。详细说明，请参阅 [扫描 Docker Hub 上的镜像](../docker-hub/repos/manage/vulnerability-scanning.md)。

### 受 CVE-2022-42889 影响的 Docker 官方镜像

[Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images) 中的多个镜像包含易受攻击的 Apache Commons Text 版本。以下列出了可能包含易受攻击的 Apache Commons Text 版本的 Docker 官方镜像：

- [bonita](https://hub.docker.com/_/bonita)
- [Couchbase](https://hub.docker.com/_/couchbase)
- [Geonetwork](https://hub.docker.com/_/geonetwork)
- [neo4j](https://hub.docker.com/_/neo4j)
- [sliverpeas](https://hub.docker.com/_/sliverpeas)
- [solr](https://hub.docker.com/_/solr)
- [xwiki](https://hub.docker.com/_/xwiki)

我们已在这些镜像中将 Apache Commons Text 更新到最新版本。其中一些镜像可能因其他原因而不易受攻击。我们建议您也查看上游网站上发布的指南。

## Log4j 2 CVE-2021-44228

_最后更新时间：2021 年 12 月_

[Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 漏洞存在于 Log4j 2 中，这是一个非常常见的 Java 日志库，允许远程代码执行，通常从攻击者容易获得的上下文中获得。例如，它在 Minecraft 服务器中被发现，允许在聊天日志中键入命令，因为这些命令随后被发送到日志记录器。这使其成为一个非常严重的漏洞，因为日志记录库被如此广泛使用，并且可能很容易被利用。许多开源维护者正在努力修复和更新软件生态系统。

Log4j 2 的易受攻击版本是从 2.0 到 2.14.1（包含）。第一个修复版本是 2.15.0。我们强烈建议您升级到 [最新版本](https://logging.apache.org/log4j/2.x/download.html)，如果可以的话。如果您使用的是 2.0 之前的版本，您也不会受到攻击。

如果您的配置已经缓解了此问题，或者您记录的内容不包含任何用户输入，您可能不会受到攻击。但是，如果没有详细了解可能记录的所有代码路径以及它们可能从何处获取输入，这可能很难验证。因此，您可能希望升级所有使用易受攻击版本的代码。

> CVE-2021-45046
>
> 作为对
> [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228) 的更新，2.15.0 版本中的修复是不完整的。已识别出其他问题，并使用
> [CVE-2021-45046](https://nvd.nist.gov/vuln/detail/CVE-2021-45046) 和
> [CVE-2021-45105](https://nvd.nist.gov/vuln/detail/CVE-2021-45105) 进行跟踪。
> 为了更完整地修复此漏洞，我们建议您尽可能升级到 2.17.0 版本。

### 扫描 Docker Hub 上的镜像

2021 年 12 月 13 日 1700 UTC 之后触发的 Docker Hub 安全扫描现在可以正确识别 Log4j 2 CVE。在此之前触发的扫描目前不反映此漏洞的状态。因此，我们建议您通过向 Docker Hub 推送新镜像来触发扫描，以查看 Log4j 2 CVE 在漏洞报告中的状态。详细说明，请参阅 [扫描 Docker Hub 上的镜像](../docker-hub/repos/manage/vulnerability-scanning.md)。

## 受 Log4j 2 CVE 影响的 Docker 官方镜像

_最后更新时间：2021 年 12 月_

[Docker 官方镜像](../docker-hub/image-library/trusted-content.md#docker-official-images) 中的多个镜像包含易受攻击的 Log4j 2 CVE-2021-44228 版本。下表列出了可能包含易受攻击的 Log4j 2 版本的 Docker 官方镜像。我们已将这些镜像中的 Log4j 2 更新到最新版本。其中一些镜像可能因其他原因而不易受攻击。我们建议您也查看上游网站上发布的指南。

| 仓库                | 已修复版本         | 附加文档       |
|:------------------------|:-----------------------|:-----------------------|
| [couchbase](https://hub.docker.com/_/couchbase)    | 7.0.3 | [Couchbase 博客](https://blog.couchbase.com/what-to-know-about-the-log4j-vulnerability-cve-2021-44228/) |
| [Elasticsearch](https://hub.docker.com/_/elasticsearch)    | 6.8.22, 7.16.2 | [Elasticsearch 公告](https://www.elastic.co/blog/new-elasticsearch-and-logstash-releases-upgrade-apache-log4j2) |
| [Flink](https://hub.docker.com/_/flink)    | 1.11.6, 1.12.7, 1.13.5, 1.14.2  | [Flink 对 Log4j CVE 的建议](https://flink.apache.org/2021/12/10/log4j-cve.html) |
| [Geonetwork](https://hub.docker.com/_/geonetwork)    | 3.10.10 | [Geonetwork GitHub 讨论](https://github.com/geonetwork/core-geonetwork/issues/6076) |
| [lightstreamer](https://hub.docker.com/_/lightstreamer)     | 等待信息 | 等待信息  |
| [logstash](https://hub.docker.com/_/logstash)    | 6.8.22, 7.16.2 | [Elasticsearch 公告](https://www.elastic.co/blog/new-elasticsearch-and-logstash-releases-upgrade-apache-log4j2) |
| [neo4j](https://hub.docker.com/_/neo4j)     | 4.4.2 | [Neo4j 公告](https://community.neo4j.com/t/log4j-cve-mitigation-for-neo4j/48856) |
| [solr](https://hub.docker.com/_/solr)    | 8.11.1 | [Solr 安全新闻](https://solr.apache.org/security.html#apache-solr-affected-by-apache-log4j-cve-2021-44228) |
| [sonarqube](https://hub.docker.com/_/sonarqube)    | 8.9.5, 9.2.2 | [SonarQube 公告](https://community.sonarsource.com/t/sonarqube-sonarcloud-and-the-log4j-vulnerability/54721) |
| [storm](https://hub.docker.com/_/storm)    | 等待信息 | 等待信息 |

> [!NOTE]
>
> 尽管 [xwiki](https://hub.docker.com/_/xwiki) 镜像可能被某些扫描器检测为易受攻击，但作者认为这些镜像不受 Log4j 2 CVE 攻击，因为 API jar 不包含该漏洞。
> [Nuxeo](https://hub.docker.com/_/nuxeo) 镜像已弃用，将不会更新。
