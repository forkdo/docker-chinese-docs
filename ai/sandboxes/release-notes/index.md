# 

<!-- FILE: manuals/ai/sandboxes/release-notes.md -->

---
title: Docker Sandboxes 发布说明
linkTitle: 发布说明
description: Docker Sandboxes 中的新功能、错误修复和变更
keywords: docker sandboxes, sbx, release notes, changelog
weight: 120
toc_min: 1
toc_max: 2
tags:
  - Release notes
---

本页列出了 Docker Sandboxes 近期稳定版本的变更。如需查看完整的发布历史（包括预发布版本和下载），请参阅 [GitHub 上的 Docker Sandboxes 发布页](https://github.com/docker/sbx-releases/releases)。

<!-- BEGIN GENERATED RELEASES -->

## 0.38.0

<em class="text-gray-400 italic dark:text-gray-500">2026-08-06</em>


[GitHub 发布](https://github.com/docker/sbx-releases/releases/tag/v0.38.0)

### 亮点

**Kit spec v2。** 提供了新的用于编写 kit 的 schema，其结构在 setup、权限、agent 指令、网络以及凭据方面更加清晰。新 kit 使用 `schemaVersion: "2"`；现有 v1 kit 仍通过旧路径加载。迁移详情请参阅 [kit spec 参考](https://docs.docker.com/ai/sandboxes/customize/kit-reference/#schema-versions)。

**MCP 管理现已成为一等特性。** 使用 `sbx mcp` 一次性注册远程或本地 MCP 服务器，然后在内置的 MCP 网关中跨受支持的 agent 和沙盒复用它们。OAuth 凭据保留在主机上，组织还可使用 Cedar 策略来管控服务器注册与工具调用。请参阅 [MCP 网关文档](https://docs.docker.com/ai/sandboxes/mcp-gateway/)。

### 新增内容

#### CLI

- `sbx create` 和 `sbx run` 在启动过程中会显示结构化的详细进度，包括已加载的环境文件、已预置的资源，以及每个 kit 命令的执行结果；在 `sbx create --kit` 期间，kit 安装进度会实时流式输出。
- 新增 `sbx daemon restart`，用于在后台停止并重启 sandboxd 守护进程。
- `sbx inspect` 现在会显示为某个沙盒配置的自定义凭据。
- `DOCKER_SANDBOXES_CLONED_WORKSPACE_SIZE` 用于配置克隆的工作区卷的大小。
- `sbx setup ssh` 在 PATH 中缺少 `ssh` 时会发出警告，在 Windows 上当缺少 `sh`（Claude Desktop 的 SSH ProxyCommand 所需）时也会发出警告。
- 端口发布失败时现在会标识受影响的宿主机端口，并说明操作系统何时需要额外的守护进程权限。

#### MCP

- 新增 `sbx mcp` 子命令用于管理 MCP 服务器。
- 包含动态 MCP 工具（`mcp-find`、`mcp-add`、`mcp-config-set`），用于将已注册的服务器附加到沙盒。
- 使用 Cedar 策略来管控组织内的 MCP 服务器与工具。

#### 网络与策略

- 在 `sbx run` 和 `sbx create` 上，`--deny-network HOST` 会在创建时记录每个沙盒的网络拒绝规则，并附带层级感知的出站消息。
- 当组织管控覆盖了本地允许时，`sbx policy allow network` 会报告清晰的"由组织管理"错误；失败的删除操作现在会使用单一规则标识符来解释出错原因。
- 登录后会立即刷新运行中的守护进程里的组织策略，而无需等待下一次轮询间隔。
- 被 CIDR 规则拒绝的 IP 字面量目标会以策略消息快速失败，而不是超时。
- 即使客户端中止了 TLS 握手，被拦截的 HTTPS 代理连接也会出现在 `sbx policy log` 中。

#### 凭据与密钥

- 服务和自定义凭据默认是全局的，使用 `--sandbox` 可指定沙盒范围；旧的 positional 形式和 `--global` 形式已被废弃并会发出警告。
- 创建后添加的沙盒级 GitHub 凭据现在无需重建沙盒即可生效。
- 在输入凭据时按 Ctrl+C 会取消命令而不保存该凭据。

#### Agents

- Docker Agent 和 OpenCode 沙盒可以使用由代理管理的 GitHub 凭据来鉴权 GitHub Copilot 请求。
- Codex 沙盒在从 TUI 创建时，优先使用已存储的 OpenAI OAuth 凭据而非 API 密钥；kit 环境变量现在可以到达云端 agent，且 git 不再因提示输入凭据而挂起 Codex 启动过程。
- 共享 agent 技能：技能文件夹下的目录符号链接会被解析并将其内容导入。

#### Kits 与模板

- Kit spec 使用新的 v2 语法。
- 使用 `extends` 的 kit 能够正确继承并覆盖其父级的镜像或构建来源。
- Kit 安装命令可以使用来自 `files/home` 的静态文件，包括二进制文件。

#### 打包

- Homebrew 从带钉书钉（stapled）的 `.dmg` 制品安装，而非 `.tar.gz` 归档，从而改进了 macOS 上的 Gatekeeper 兼容性。
- Windows：在 WinGet/MSI 升级期间会停止运行中的 sandboxd 守护进程，使客户端和服务器最终处于同一版本。

#### 安全性

- Claude Desktop 的 SSH 会话不再在沙盒内部暴露 Desktop OAuth 访问令牌。
- 修复了 `sbx cp` 复制导出（copy-out）时的目标逃逸缺陷（CVE-2026-17106）。
- 守护进程的环回出站代理仅服务于守护进程自身的流量，防止同一多用户主机上的其他本地用户通过该代理到达配置的上游代理。

#### 错误修复

- 修复了 sandboxd 停止响应所有端点、且在崩溃后无法在不使用 SIGKILL 的情况下被停止的挂起问题；致命的守护进程回溯现在会包含在 `sbx diagnose --upload` 的打包文件中。
- 修复了当运行中的守护进程响应健康检查较慢时，sandboxd 启动偶发失败的问题。
- 修复了当有一个空闲的 SSH 会话（例如 Claude Desktop）连接到沙盒时，`sbx daemon stop` 挂起的问题。
- sandboxd 现在会通过重新拉取镜像自动修复损坏的本地镜像缓存，否则会报告清晰的"运行 `sbx daemon reset`"错误。
- 修复了在使用 `sbx kit add` 切换沙盒容器后，守护进程重启导致的重新创建失败（"找不到基础镜像"）；重新创建会从沙盒模板重新组合以自愈。
- 修复了针对容器解析地址的沙盒反向 DNS（PTR）查找返回 NXDOMAIN 的问题。
- 修复了被劫持的 HTTP CONNECT 隧道造成的 goroutine 和网络端点泄漏，该泄漏可能在多次删除/重建循环后最终导致沙盒创建停滞。
- 修复了删除沙盒时其网络端点正在拆除过程中偶发的 500 错误。
- 守护进程在重启时会并行恢复已保存沙盒的网络代理，从而加快多个沙盒时的启动速度，并修复了首次运行策略应用期间潜在的崩溃。
- 修复了在使用 `.gitconfig` 中带有 `includeIf` 指令的仓库创建沙盒时，对宿主 `.git/config` 的损坏问题；沙盒现在仅将 git 身份写入容器的 gitconfig。
- `sbx skills` 现在显示单一的用法形式，并对导入共享 agent 技能提供更清晰的帮助信息。
- 当守护进程注入凭据后，sbx 不再报告已存储的凭据未被注入。

### 实验性功能

#### 企业网络

由设置驱动的 upstream-proxy 配置，具有独立的沙盒和守护进程范围，以及在 Windows 上集成的 NTLM/Kerberos 代理鉴权。

- 使用 `proxy`、`proxy.sandbox`、`proxy.daemon` 以及对应的 `no_proxy` 设置为沙盒和守护进程流量配置独立的代理设置。这些默认使用宿主操作系统的代理设置。守护进程自身的流量（包括镜像拉取和遥测）也使用所配置的代理。
- 在 Windows 上，sbx 可以对需要集成 NTLM 或 Kerberos/Negotiate 鉴权的上游代理进行鉴权。使用 `proxy.integratedAuth` 设置启用此行为。
- 如果 TLS 检测的代理签发带有负序列号的证书，请使用 `sbx settings set tls.allowNegativeSerial true` 启用兼容性，然后重启守护进程。

#### GPU 透传

在 Linux 上使用 `sbx run --gpu` 运行带有 NVIDIA VFIO GPU 透传的沙盒。使用 `sbx settings set feature.sandbox-gpu true` 启用此功能。

#### 本地模型

使用 `sbx run --model <name> claude` 配合本地 GGUF 模型运行 Claude Code。要使用来自现有 Ollama 安装的模型，请在模型名称前加上 `ollama/`。请参阅 [Claude Code > 使用本地模型](https://docs.docker.com/ai/sandboxes/agents/claude-code/#use-a-local-model)。

## 0.37.1

<em class="text-gray-400 italic dark:text-gray-500">2026-07-29</em>


[GitHub 发布](https://github.com/docker/sbx-releases/releases/tag/v0.37.1)

### 亮点

此补丁版本停止了 SSH 会话**默认将凭据环境变量转发进沙盒**的行为。诸如 `ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 和 `GH_TOKEN` 之类的变量不再从客户端发送到沙盒，除非通过 `ssh.acceptEnv` 设置显式允许。

### 新增内容

#### 错误修复

- SSH 会话不再默认将凭据环境变量（`ANTHROPIC_API_KEY`、`OPENAI_API_KEY`、`GH_TOKEN` 等）从客户端转发进沙盒；使用 `ssh.acceptEnv` 设置可以为特定变量重新开启。

## 0.37.0

<em class="text-gray-400 italic dark:text-gray-500">2026-07-24</em>


[GitHub 发布](https://github.com/docker/sbx-releases/releases/tag/v0.37.0)

### 亮点

**到沙盒的 SSH 访问（实验性）。** Docker Sandboxes 现在可以用作 SSH 目标。启用 SSH 访问后，先运行一次 `sbx setup ssh`，然后使用 `ssh my-sandbox.sbx` 按名称连接到现有沙盒。将该连接用于交互式 shell、一次性命令以及基于 SSH 的远程开发。

**共享 agent 技能。** Docker Sandboxes 现在可以将受支持宿主 agent 的技能导入到一个跨沙盒共享的持久化存储中。运行 `sbx skills import` 即可导入。新的沙盒默认以读写方式挂载该存储；使用 `--no-share-skills` 退出。

### 新增内容

#### SSH

- `sbx setup ssh` 会向你的 SSH 配置中添加一个受管理的 `*.sbx` 条目，使现有沙盒在 `<name>.sbx` 处可用。
- 当需要时，SSH 连接会自动启动本地 Docker Sandboxes 守护进程和目标沙盒。
- 使用兼容 OpenSSH 的客户端和远程开发工具（如 VS Code、Cursor、Claude Desktop 和 ChatGPT）进行连接。

#### 共享技能

- `sbx skills import` 会发现并导入来自宿主的技能，并使它们对沙盒中的 agent 可用。使用 `--dry-run` 预览导入，使用 `--force` 替换现有技能。
- 导入的技能在沙盒删除后仍然保留，并被挂载到受支持 agent 的新建沙盒中。
- 创建沙盒时传递 `--no-share-skills` 给 `sbx run` 或 `sbx create` 即可退出。

#### CLI

- `sbx create` 和 `sbx run` 接受 `-p/--publish`，在创建时发布沙盒端口。

#### 网络与策略

- `DOCKER_SANDBOXES_PROXY=system` 通过宿主操作系统的代理配置（macOS/Windows）路由沙盒出站流量，包括任何 PAC 自动配置 URL。
- 管控策略拒绝现在可以显示组织配置的支撑消息（例如联系谁）。

#### 安全与审计

- 审计现在针对网络出站（每次允许的连接有记录）和文件系统挂载（每个允许的路径有记录）发出执行结果记录——成功、延迟和错误类别—— alongside 策略归因的决策记录。
- sandboxd 将自身排除在 Windows 错误报告之外，这样守护进程崩溃转储就无法捕获内存中的凭据。

#### 性能

- 在没有 OS 钥匙串的 Linux 宿主上，`sbx secret ls` 和沙盒启动更快——存储的凭据不再全部解密只是为了列出或解析凭据。

### 错误修复

- 修复了在没有 OS 钥匙串的 Linux 宿主上 sandboxd 无法启动的问题，即磁盘上的密钥存储的密钥派生可能在启动时占满一个 CPU，而 CLI 会杀掉仍在启动中的守护进程。
- 修复了移除运行中的沙盒时偶发的"无法完全删除沙盒"错误，该错误由与引擎端点清理竞争的网络拆除引起。

## 0.35.0

<em class="text-gray-400 italic dark:text-gray-500">2026-07-10</em>


[GitHub 发布](https://github.com/docker/sbx-releases/releases/tag/v0.35.0)

### 注意

由于在此版本发布期间遇到的稳定性问题，v0.35.x 没有 Linux/ARM64 构建。我们计划在下个版本恢复它们。

### 亮点

- **宿主环境变量不再用于鉴权。** 之前的版本会自动检测预定义环境变量（如 `ANTHROPIC_API_KEY`）中的 API 密钥，并将其注入到模型提供商的请求中。从此版本开始，沙盒仅使用你显式存储的凭据，或支持 OAuth 的 agent 使用 OAuth 进行鉴权。如果你依赖环境变量，请运行一次新的 `sbx secret import` 命令将你的密钥迁移到钥匙串中。详情请参阅 [凭据文档](https://docs.docker.com/ai/sandboxes/security/credentials/)。
- 策略命令进行了改版，提供了更简洁的 `sbx policy ls`、新的 `sbx policy inspect`，以及用于在运行前测试当前策略是否允许某个访问请求的 `sbx policy check network` 命令。
- 网络新增了 **SOCKS5 上游代理传输**。

### 新增内容

#### 网络与代理

- 沙盒代理可以通过 `DOCKER_SANDBOXES_PROXY`、`HTTP_PROXY` 或 `HTTPS_PROXY`，使用 SOCKS5 代理（`socks5://` / `socks5h://`，可选带鉴权）链式转发上游出站流量。
- 添加 `DOCKER_SANDBOXES_NO_PROXY`，使用标准的 `NO_PROXY` 匹配语义将目标排除在 `DOCKER_SANDBOXES_PROXY` 之外。
- Droid OAuth 凭据现在由代理管理：真实令牌保留在宿主上，永远不会进入沙盒。
- 更快的沙盒启动：TLS 代理 CA 通过合并进信任包（trust bundle）来安装，而不是运行 `update-ca-certificates`，从而节省几百毫秒。

#### 策略

- 简化 `sbx policy ls` 并添加 `--wide`、`--source` 和 `--decision` 过滤器
- 添加 `sbx policy check` 用于测试当前策略是否允许某个访问请求
- 均衡网络预设现在允许 VS Code 域名、Azure Blob Storage（`*.blob.core.windows.net`）以及通过 HTTP 的 `dhi.io`。

#### Kits

- `sbx kit add` 现在不再在运行时注入，而是使用增强后的 kit 集重建沙盒容器。状态随重建一起保留。
- `sbx kit add` 将所添加 kit 的网络允许/拒绝规则以及组合策略应用到运行中的沙盒。
- 使用来自自定义 `--kit` agent 的沙盒重新连接现在可以使用 `sbx run --name <name>`，而无需重新传递 `--kit`。
- Kit 可以通过服务为 `sbx-login` 的凭据，将用户的 Docker 登录令牌注入到对 docker.com 主机的请求中。

#### CLI

- `sbx rm` 现在除非传递 `--force`，否则不会删除活动会话。
- `sbx inspect` 现在会列出沙盒的 kit、注入的凭据和沙盒信息。
- 新增 `sbx daemon` 命令（`start`、`stop`、`status`、`log-level`）

#### 凭据

- `sbx secret import` 将凭据环境变量导入钥匙串；`sbx secret ls` 标记仅环境变量和 OAuth 遮蔽的条目。宿主环境变量不再在运行时自动注入——请使用 `sbx secret import` 进行迁移。

#### 运行时与镜像

- 在所有操作系统上默认启用 virtiofs 缓存以获得更快的文件系统性能（使用 `DOCKER_SANDBOXES_ENABLE_VIRTIOFS_CACHE=0` 退出）。

### 错误修复

- 修复在已添加 kit 的沙盒上使用 `sbx cp` 复制文件时出现的"找不到容器"错误。
- 在凭据捕获路径上强制执行每个服务一个凭据的规则，这样陈旧的 API 密钥就不会遮蔽新捕获的凭据。
- 修复了 `sbx login` 在重新登录到之前使用过的账户时失败并报"该项已存在于钥匙串中"的问题；注销现在会清除所有已存储的 Docker 凭据。
- 重启的沙盒通过在守护进程重启时重新水合（rehydrate）已存储的 `github` 凭据来保持 GitHub 访问。
- 修复了某个自定义 kit 在重启前清除整个守护进程对 GitHub 的内置代理鉴权头部映射的问题。
- 当上游代理仅支持 CONNECT 时，通过 CONNECT 隧道纯 HTTP 转发流量（例如 `apt`、端口 80）。
- 沙盒通过上游代理的出站流量在 CONNECT 握手上标识为 `sbx-proxy`。
- 修复使用方括号表示法（例如 `[fdcb::1]:22`）的 IPv6 策略允许规则不匹配的问题。
- 修复了在设置了 `DOCKER_HOST` 时 `sbx` 连接到错误 Docker 守护进程的问题。
- 在 CLI 和守护进程之间串行化 Docker Hub 令牌刷新，以免意外丢失登录会话。

### 平台支持

- 阻止在早于 Windows 11（当前唯一受支持的版本）的 Windows 版本上安装。

<!-- END GENERATED RELEASES -->

## 更早的版本

对于较旧的版本，请参阅 [GitHub 上的 Docker Sandboxes 发布页](https://github.com/docker/sbx-releases/releases)。

