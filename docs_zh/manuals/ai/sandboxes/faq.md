---
title: FAQ
weight: 110
description: 关于 Docker Sandboxes 的常见问题。
keywords: docker sandboxes, sbx, faq, sign in, telemetry, clipboard, image paste, pricing, commercial use, allowlist, firewall, domains, proxy
---

## Docker Sandboxes 免费吗？可以商用吗？

两者都是肯定的。`sbx` CLI 可免费使用，包括用于商业和专业工作，没有按席位收费。安装它，用
免费的 Docker 账户登录，即可免费运行沙箱。

唯一付费的组成部分是组织治理：集中管理的网络、文件系统和 MCP 策略、
[登录强制](governance/monitor-and-enforce/sign-in-enforcement.md)，以及
[审计日志](governance/audit/)。这些
[组织治理功能](governance/) 需要单独的付费订阅——
[联系 Docker 销售](https://www.docker.com/products/ai-governance/#contact-sales) 以开始使用。
其他一切，包括在隔离沙箱中运行 agent，都是免费的。

## 为什么我需要登录？

Docker Sandboxes 围绕"你和你的 agent 是一个团队"的理念构建。登录为每个沙箱提供一个经过
验证的身份，这让 Docker 能够：

- **将沙箱绑定到真实的人。** 当 agent 可以构建容器、安装包和推送代码时，治理就很重要。你的
  Docker 身份是锚点。
- **启用团队功能。** 团队级功能如 [组织治理](governance/)、共享环境和审计日志需要一个"谁"
  的概念，而以后再加上对所有人来说都会更糟。
- **对 Docker 基础设施进行认证。** 沙箱拉取镜像、运行守护进程并与 Docker 服务通信。Docker
  账户认证这些请求。

你的 Docker 账户邮箱仅用于认证，不用于营销。

## 我可以在整个组织内强制实施沙箱策略吗？

可以。管理员可以集中管理网络、文件系统和 MCP 策略。这些控制适用于组织中的每个沙箱。当
组织治理处于激活状态时，只有组织允许规则授予访问权限：用 `sbx policy` 设置的本地允许规则
不再被评估，而本地拒绝规则仍然叠加生效。

请参阅 [组织策略](governance/access-controls/organization.md)。此功能需要单独的付费订阅——
[联系 Docker 销售](https://www.docker.com/products/ai-governance/#contact-sales) 以开始使用。

## 要让 Docker Sandboxes 工作，我需要允许哪些域名？

如果你的组织用防火墙或代理限制出站网络访问，请将以下域名添加到你的允许列表，以便 `sbx`
能够认证、拉取镜像并上报诊断信息。

| Domain                                             | Description             |
| -------------------------------------------------- | ----------------------- |
| https://login.docker.com                           | Authentication          |
| https://hub.docker.com                             | Docker Hub              |
| https://api.docker.com                             | Docker API              |
| https://marlin-2.docker.com                        | Telemetry               |
| https://marlin-api.docker.com                      | Telemetry               |
| https://registry-1.docker.io                       | Docker pull/push        |
| https://auth.docker.io                             | Registry authentication |
| https://dhi.io                                     | Docker Hardened Images  |
| https://sbx-diagnostics.s3.us-east-1.amazonaws.com | Diagnostics upload      |

## CLI 会收集遥测数据吗？

`sbx` CLI 收集有关 CLI 调用的基本使用数据：

- 你运行了哪个命令
- 它是成功还是失败
- 花了多长时间
- 如果你已登录，会包含你的 Docker 用户名

Docker Sandboxes 不监控会话、不读取你的提示、也不访问你的代码。你的代码保留在沙箱和你的
宿主机上。

要退出所有分析，请设置 `SBX_NO_TELEMETRY` 环境变量：

```console
$ export SBX_NO_TELEMETRY=1
```

## 如何在沙箱内设置自定义环境变量？

[`sbx secret`](/reference/cli/sbx/secret/) 命令只支持固定的一组
[服务](security/credentials.md#built-in-services)（Anthropic、OpenAI、GitHub 等）。如果你的
agent 需要绑定到受支持服务之外的环境变量，例如 `BRAVE_API_KEY` 或自定义的内部 token，请将其
写入沙箱内的 `/etc/sandbox-persistent.sh`。此文件在每次 shell 登录时被 source，因此该变量在
沙箱生命周期内跨 agent 会话持久保留。

使用 `sbx exec` 追加导出：

```console
$ sbx exec -d <sandbox-name> bash -c "echo 'export BRAVE_API_KEY=your_key' >> /etc/sandbox-persistent.sh"
```

需要 `bash -c` 包装器，以便 `>>` 重定向在沙箱内运行，而不是在你的宿主机上。

> [!NOTE]
> 与 `sbx secret` 不同（后者通过宿主侧代理注入凭据，不向 agent 暴露它们），此方法将值存储在
> 沙箱内。agent 进程可以直接读取它。仅对无法使用基于代理注入的凭据使用此方法。

`/etc/sandbox-persistent.sh` 中的变量在 bash 在沙箱内运行时自动被 source，包括交互式会话和
用 `sbx run` 启动的 agent。如果你直接用 `sbx exec <name> <command>` 运行命令，该命令在没有
shell 的情况下运行，因此不会 source 持久环境文件。将命令包裹在 `bash -c` 中以加载环境：

```console
$ sbx exec <sandbox-name> bash -c "your-command"
```

要验证变量是否已设置，在沙箱中打开一个 shell：

```console
$ sbx exec -it <sandbox-name> bash
$ echo $BRAVE_API_KEY
```

## 为什么 agent 在没有审批提示的情况下运行？

沙箱本身就是安全边界。由于 agent 在隔离的 microVM 内运行，具有
[网络策略](governance/access-controls/network.md)、[凭据隔离](security/credentials.md)，且
除显式共享的路径外无法访问你的宿主系统，通常需要审批提示的原因（防止破坏性命令、网络访问、
文件修改）由沙箱隔离层处理，而非由 agent 处理。

如果你希望重新启用审批提示，请在会话内更改权限模式。多数 agent 允许你在启动后切换权限模式。
在 Claude Code 中，使用 `/permissions` 命令交互式更改模式。

要让审批提示成为每个会话的默认行为，请定义一个自定义 sandbox kit，覆盖 agent 的入口点以
去掉跳过权限的标志。例如，一个不带 `--dangerously-skip-permissions` 启动 Claude Code 的 kit：

```yaml {title="claude-safe/spec.yaml"}
schemaVersion: "1"
kind: sandbox
name: claude-safe
sandbox:
  image: "docker/sandbox-templates:claude-code-docker"
  entrypoint:
    run: [claude]
```

用 `sbx run claude-safe --kit ./claude-safe/` 运行它。完整的模式请参阅
[Sandbox kits](customize/kits.md#sandbox-kits)。

## 我如何知道我的 agent 是否在沙箱中运行？

问 agent。agent 可以看到它是否在沙箱内运行。在 Claude Code 中，使用 `/btw` 斜杠命令在不
打断进行中任务的情况下提问：

```text
/btw are you running in a sandbox?
```

## 为什么沙箱不使用我的用户级 agent 配置？

沙箱不会导入你完整的用户级 agent 配置。钩子、设置，以及 `~/.claude` 等目录下的其他文件保留在
宿主机上。工作目录中的项目级配置在沙箱内仍然可用。

共享的 agent skills 是例外。运行 `sbx skills import` 将 skills 从受支持的宿主目录复制到与
沙箱共享的持久存储。有关受支持的目录、挂载行为和每个沙箱的退出选择，请参阅
[共享 agent skills](workflows.md#share-agent-skills)。

将项目特定的 skills 和其他 agent 配置保留在项目本身中。这使配置与代码一起版本化。不要使用
指向宿主路径的符号链接，因为沙箱内的 agent 无法在沙箱外跟进它们。

## 我可以向 agent 粘贴图片吗？

可以，但默认关闭。文本粘贴已经可用，因为终端直接发送它。用 `Ctrl+V` 粘贴图片或截图则不同：
agent 从你的宿主剪贴板读取它，而沙箱会阻止该访问，除非你选择加入。

用本地设置打开它：

```console
$ sbx settings set clipboard.imagePaste true
```

然后 `Ctrl+V` 将宿主图片粘贴到读取剪贴板的 agent 中，包括 Claude Code 和 Codex。该设置会在
几秒内生效，即使对运行中的沙箱也是如此。

这是选择加入的，因为它放宽了沙箱的隔离：启用时，沙箱内的进程可以通过宿主侧代理读取你的宿主
剪贴板。暴露面很窄——读取只在粘贴时发生，只返回图片数据（`image/png`），且剪贴板内容从不
缓存或记录——但它仍然是宿主数据进入沙箱，因此在你打开它之前保持关闭。

要重新关闭它：

```console
$ sbx settings set clipboard.imagePaste false
```

## 我可以在无界面的 Linux 上使用 Docker Sandboxes 吗？

可以。在 Linux 上，`sbx` 将秘密存储在你的桌面密钥环暴露的 Secret Service 中，例如 GNOME
Keyring 或 KDE Wallet。无界面服务器和某些 WSL 设置没有运行中的 Secret Service，因此 `sbx`
回退到 `$XDG_CONFIG_HOME/com.docker.sandboxes` 下的加密文件，当 `$XDG_CONFIG_HOME` 未设置时
默认为 `~/.config/com.docker.sandboxes`。无需设置。当你在这样的宿主上存储秘密时，`sbx` 会
打印一条通知：

```text
No keychain detected - this secret will be stored in an encrypted file on disk
```

该文件在静态时加密，并受 `0700` 目录权限保护，与 `~/.docker/config.json` 相同的姿态。它比
OS 密钥环弱，后者还按应用调解访问。

要将秘密保留在密钥环中，请在存储它们之前在宿主上运行 Secret Service：安装 `gnome-keyring`
并启动 `dbus-run-session`，或在解锁它的登录会话下运行密钥环守护进程。一旦有可用的 Secret
Service 在运行，`sbx` 会再次将新秘密存储在密钥环中。有关每个平台保存秘密的位置，请参阅
[秘密存储在哪里](security/credentials.md#where-secrets-are-stored)。
