---
title: 架构
description: Docker Sandboxes 的技术架构；工作区挂载、存储、网络以及沙箱生命周期。
keywords: docker sandboxes, architecture, microVM, workspace mounting, sandbox lifecycle
weight: 70
---

此页面解释了 Docker Sandboxes 在底层是如何工作的。有关架构的安全特性，请参见[沙箱隔离](security/isolation.md)。

## 工作区挂载

你的工作区通过文件系统透传（passthrough）直接挂载到沙箱中。沙箱看到的是你主机上的真实文件，因此双向的更改都是即时生效的，不涉及任何同步过程。

你的工作区以与主机相同的绝对路径挂载到沙箱中。保留绝对路径意味着错误消息、配置文件和构建输出引用的都是在你主机上能找到的路径。代理看到的目录结构与你看到的完全一致，这减少了调试或审查更改时的困惑。

> [!WARNING]
> 不要将网络挂载或远程存储（网络驱动器、SMB/NFS 共享，或云同步文件夹）作为工作区挂载。沙箱通过文件系统透传访问工作区，因此每一次文件读写都会经过网络。这会增加延迟并拖慢代理性能。

## 存储和持久性

当你创建沙箱时，其中的所有内容都会一直保留，直到你移除它：由代理构建或拉取的 Docker 镜像和容器、已安装的软件包、代理状态与历史记录，以及工作区的更改。

每个沙箱都维护自己的 Docker 守护进程状态、镜像缓存和软件包安装。多个沙箱之间不共享镜像或层。[共享代理技能存储](workflows.md#share-agent-skills)是一个例外：受支持的代理会将该主机侧的存储以读写方式挂载，除非你在创建沙箱时选择退出。

每个沙箱都会为它的虚拟机镜像、Docker 镜像、容器层和卷消耗磁盘空间，并且随着你构建镜像和安装软件包而增长。

所有操作系统默认都启用了 Virtiofs 缓存。从沙箱虚拟机发起的文件读取会在主机侧缓存，从而减少经过文件系统透传的往返次数，并提升读密集型工作负载（如 `git status` 或目录扫描）的性能。若要退出，请在创建沙箱时设置 `DOCKER_SANDBOXES_ENABLE_VIRTIOFS_CACHE=0`：

```console
$ DOCKER_SANDBOXES_ENABLE_VIRTIOFS_CACHE=0 sbx run <template>
```

## 网络

来自沙箱的所有出站流量都会经过主机侧的一个 HTTP/HTTPS 代理。代理会自动配置给代理程序使用。该代理执行[网络访问策略](governance/access-controls/network.md)并处理[凭据注入](security/credentials.md)。其工作原理见[网络隔离](security/isolation.md#network-isolation)，开箱即允许的内容见[默认安全态势](security/defaults.md)。

### 上游代理

主机侧代理使用你主机的网络配置和路由来发起出站连接。当某个目标可通过直连路由到达时，流量就走该路由。当到达某个目标需要经过上游代理时，主机侧代理会把请求转发给它。链式连接到上游代理意味着沙箱流量会遵循与你主机上其他应用相同的出口控制。

沙箱守护进程发起这些上游请求，它会读取 `HTTP_PROXY`、`HTTPS_PROXY` 和 `NO_PROXY` 代理环境变量及其对应的小写形式。设置 `NO_PROXY` 可列出应直连而非经过上游代理的主机。

要通过不同的代理路由沙箱流量，请将 `DOCKER_SANDBOXES_PROXY` 设置为代理 URL。它仅作用于沙箱流量，并将 HTTP 和 HTTPS 的上游代理都设置为该 URL。与 `HTTP_PROXY` 和 `HTTPS_PROXY` 不同，它不影响镜像拉取或守护进程自身的请求。

`DOCKER_SANDBOXES_PROXY` 接受 `http://`、`https://`、`socks5://` 和 `socks5h://` 形式的 URL。使用 `socks5://` 时，DNS 在连接交给代理之前于本地解析。使用 `socks5h://` 时，DNS 解析交由代理完成。两种协议都支持在 URL 中携带凭据：`socks5://user:pass@host:port`。

设置 `DOCKER_SANDBOXES_NO_PROXY` 可将特定目标从 `DOCKER_SANDBOXES_PROXY` 中排除，使用标准的逗号分隔 `NO_PROXY` 匹配语义。它只影响经过 `DOCKER_SANDBOXES_PROXY` 路由的流量——用 `NO_PROXY` 来把目标从 `HTTP_PROXY`/`HTTPS_PROXY` 中排除。

在沙箱守护进程启动的环境中设置这些变量。该守护进程在首次需要一个命令时自动启动，因此请在运行 `sbx` 命令之前设置这些变量。如果守护进程已在运行，请运行 `sbx daemon restart` 使更改生效。

有一个限制：

- 不支持代理自动配置文件（如 `proxy.pac`）。请显式设置 `HTTP_PROXY`、`HTTPS_PROXY` 或 `DOCKER_SANDBOXES_PROXY` 环境变量。

## MCP 网关

受支持的代理会连接到一个单一的沙箱 MCP 网关端点。该网关运行在沙箱边界的主机侧，负责代理对注册 MCP 服务器的访问。

注册的 MCP 服务器可以是远程端点，也可以是在主机上启动的本地 stdio 服务器。本地 stdio 服务器不在沙箱虚拟机内运行。如果本地 stdio 服务器被打包为 OCI 镜像，或者你注册了一个显式的 `docker` 命令，它会使用主机上的 Docker。

当 MCP 策略生效时，强制发生在 MCP 网关路径上，与 HTTP/HTTPS 网络代理相互独立。服务器注册会在存储之前接受检查，受治理的 MCP 请求会在工具调用、资源读取、提示词获取或网关元工具执行之前由网关检查。

## 生命周期

`sbx run` 会为指定的代理初始化一个带有工作区的虚拟机并启动代理。你可以停止并重启而无需重新创建虚拟机，从而保留已安装的软件包和 Docker 镜像。

沙箱会一直保留，直到被显式移除。停止代理不会删除虚拟机；环境设置在多次运行之间延续。使用 `sbx rm` 来删除沙箱、其虚拟机以及其中的全部内容。如果沙箱使用了 [`--clone`](usage.md#clone-mode)，那么主机仓库中的 `sandbox-<name>` Git 远程也会被移除。

## 与其他方案的比较

| 方法                                            | 隔离级别            | Docker 访问      | 使用场景           |
| ----------------------------------------------- | ------------------- | ---------------- | ------------------ |
| 沙箱 (microVM)                                  | 完全（虚拟机监控程序） | 隔离的守护进程   | 自主代理           |
| 带套接字挂载的容器                              | 部分（命名空间）    | 共享主机守护进程 | 可信工具           |
| [Docker-in-Docker](https://hub.docker.com/_/docker) | 部分（特权）        | 嵌套守护进程     | CI/CD 流水线       |
| 主机执行                                        | 无                  | 主机守护进程     | 手动开发           |

沙箱以更高的资源开销（一个虚拟机加其自身的守护进程）换取完全的隔离。当你需要轻量级打包但不需要 Docker 访问时，使用容器。当你需要给某个自主实体完整的 Docker 功能但又不能信任它访问你的主机环境时，使用沙箱。
