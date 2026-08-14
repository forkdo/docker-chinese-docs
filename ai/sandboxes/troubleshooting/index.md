# 

<!-- FILE: manuals/ai/sandboxes/troubleshooting.md -->

---
title: 故障排除
weight: 100
description: 解决使用 Docker Sandboxes 时的常见问题。
keywords: docker sandboxes, sbx, troubleshooting, diagnostics, reset, network policy, git, ssh
---

## 运行诊断

在深入某个具体问题之前，运行 [`sbx diagnose`](/reference/cli/sbx/diagnose/) 来检查你的安装中的常见问题，例如缺少 CLI 二进制文件、守护进程可达性问题、CLI/守护进程版本不匹配、缺少存储目录或被破坏的鉴权。

```console
$ sbx diagnose
```

该命令会打印一份检查摘要，显示通过、警告或失败的检查，并附带建议的修复方法。使用 `--output json` 获取机器可读的输出，或使用 `--output github-issue` 生成适合粘贴到 GitHub issue 中的 Markdown 片段。

## 重启沙盒守护进程

如果沙盒命令挂起、无法连接到守护进程，或不断返回守护进程错误，请在执行重置沙盒状态之前重启沙盒守护进程：

```console
$ sbx daemon restart
```

然后重试失败的命令。重启守护进程不会删除沙盒数据。如果问题持续存在或状态已损坏，请使用 [`sbx reset`](/reference/cli/sbx/reset/)。

## 重置沙盒

如果你遇到持续的问题或状态损坏，请运行 [`sbx reset`](/reference/cli/sbx/reset/) 以停止所有 VM 并删除所有沙盒数据。之后创建全新的沙盒。

## agent 无法安装包或访问 API

沙盒使用[网络访问规则](governance/access-controls/network.md)来控制出站流量。如果 agent 无法安装包或调用外部 API，目标域很可能不在允许列表中。检查哪些请求被阻止：

```console
$ sbx policy log
```

然后允许你的工作流需要的域：

```console
$ sbx policy allow network "*.npmjs.org,*.pypi.org,files.pythonhosted.org"
```

要允许所有出站流量，改为：

```console
$ sbx policy allow network "**"
```

如果 `sbx policy allow` 仍无法解除请求阻塞，你的组织可能集中管理了沙盒策略，并优先于本地规则。请参阅 [组织策略](governance/access-controls/organization.md)。

## kit 安装失败：来源不在允许列表中

如果加载一个 kit 失败，并出现类似其来源不在你的允许列表中的消息：

```console
$ sbx run claude --kit "git+https://github.com/docker/sbx-kits-contrib.git#dir=vale"
ERROR: resolve kits: kit "git+https://github.com/docker/sbx-kits-contrib.git#dir=vale" cannot be installed — its source is not in your allowlist.
```

`sbx` 将 kit 安装限制在来源允许列表中，该列表默认仅为 Docker Hub（`docker.io/`）。将 kit 的发布者添加到 `kit.allowedSources` 设置中，保留你想保留的条目：

```console
$ sbx settings set kit.allowedSources '["docker.io/","github.com/docker/"]'
```

然后再次运行该命令。有关详细信息，包括如何允许本地 kit 或任何远程来源，请参阅 [限制 kit 来源](customize/kits.md#restrict-kit-sources)。

## SSH 和其他非 HTTP 连接失败

像 SSH 这样的非 HTTP TCP 连接可以通过为目标 IP 地址和端口添加策略规则来允许。例如，允许到特定主机的 SSH：

```console
$ sbx policy allow network "10.1.2.3:22"
```

基于主机名的规则（例如 `myhost:22`）对非 HTTP 连接不起作用，因为在此上下文中代理无法将主机名解析为 IP 地址。请直接使用 IP 地址。

UDP 和 ICMP 流量在网络层被阻止，无法通过策略规则解除阻塞。

对于通过 SSH 进行的 Git 操作，你可以为 Git 服务器的 IP 地址添加允许规则，或者改用 HTTPS URL：

```console
$ git clone https://github.com/owner/repo.git
```

## 无法到达宿主上运行的服务

如果从沙盒内部对 `127.0.0.1` 或本地网络 IP 的请求返回"connection refused"，则该地址在沙盒 VM 内部不可达。请参阅 [从沙盒访问宿主服务](workflows.md#accessing-host-services-from-a-sandbox)。

## Docker 鉴权失败

如果你看到类似 `You are not authenticated to Docker` 的消息，说明你的登录会话已过期。在交互式终端中，CLI 会提示你重新登录。在非交互式环境（如脚本或 CI）中，运行 `sbx login` 重新鉴权。

## agent 鉴权失败

如果 agent 无法到达其模型提供商，或者你看到 API 密钥错误，密钥很可能无效、已过期或未配置。验证它已设置在你的 shell 配置文件中，并且你已 source 它或打开了新终端。

对于使用[凭据代理](security/credentials.md)的 agent，请确保你没有在沙盒内部将 API 密钥设置为无效值——代理会在出站请求时自动注入凭据。

如果凭据配置正确但 API 调用仍然失败，请检查 `sbx policy log` 并查看 **PROXY** 列。通过 `transparent` 代理路由的请求不会获得凭据注入。这可能发生在沙盒内部的客户端（例如 Docker 容器中的进程）未配置为使用前向代理时。详情请参阅 [监控网络活动](governance/monitor-and-enforce/monitoring.md)。

## API 调用因证书错误失败

如果你的组织使用了检测 HTTPS 流量的代理，agent 请求可能因证书错误而失败，例如 `SSL certificate problem: self-signed certificate in certificate chain`。在沙盒内部安装你组织的内部根 CA，以便 agent 及其 SDK 信任由代理签名的证书。证书错误会在凭据代理注入凭据之前就阻止请求。

对于可重复的设置，创建一个在沙盒创建时安装 CA 的 [沙盒 kit](customize/kits.md)。有关示例 kit，请参阅 [安装内部 CA 证书](customize/kit-examples.md#install-an-internal-ca-certificate)。

使用具有 `.crt` 扩展名的 PEM 编码证书。如果流量可能被多个内部代理签名，请在运行 `update-ca-certificates` 之前安装每个代理的根 CA。

使用 kit 创建沙盒：

```console
$ sbx run claude --kit ./internal-ca/
```

要更新现有沙盒，请将证书复制到沙盒并更新信任存储：

```console
$ sbx cp ./internal-ca.crt <sandbox-name>:/tmp/internal-ca.crt
$ sbx exec <sandbox-name> -- sudo install -m 0644 /tmp/internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt
$ sbx exec <sandbox-name> -- sudo update-ca-certificates
```

> [!IMPORTANT]
> 如上所示，使用 `update-ca-certificates` 将 CA 安装到系统信任存储中。不要覆盖沙盒的 TLS 信任变量（例如 `SSL_CERT_FILE`）使其仅指向你的内部 CA。这样做会替换系统包，并破坏凭据代理所依赖的信任，从而导致 `forward` 出站路径上的请求失败。

如果在安装 CA 后 API 调用仍然失败，请运行 `sbx policy log` 并检查 **PROXY** 列中的出站路径：

- `forward`：凭据代理终止 TLS 并呈现自己的证书，沙盒已经信任该证书。此路径上的请求不需要内部 CA，而覆盖沙盒的信任变量会像上面描述的那样破坏它们。
- `forward-bypass` 和 `transparent`：代理将数据包转发到上游代理而不终止 TLS，因此沙盒直接看到你组织的证书。这些路径正是安装内部 CA 适用的地方。它们之间的唯一区别是客户端是否知道它正在与代理对话。

## 沙盒磁盘空间不足

沙盒根文件系统（`/`）默认为 20 GB。要在创建沙盒之前增大它，请设置 `DOCKER_SANDBOXES_ROOT_SIZE`：

```console
$ DOCKER_SANDBOXES_ROOT_SIZE=40g sbx run claude
```

`DOCKER_SANDBOXES_ROOT_SIZE` 控制根文件系统大小。`DOCKER_SANDBOXES_DOCKER_SIZE` 控制 Docker 数据盘（`/var/lib/docker`）大小。两者相互独立——如果需要，可以同时设置两者。

对于[克隆模式沙盒](usage.md#clone-mode)，在创建沙盒之前设置 `DOCKER_SANDBOXES_CLONED_WORKSPACE_SIZE` 以配置克隆的工作区卷容量。该变量接受人类可读的大小字符串，例如 `100g`：

```console
$ DOCKER_SANDBOXES_CLONED_WORKSPACE_SIZE=100g sbx run --clone claude
```

## 大型仓库中文件系统操作缓慢

当沙盒工作区以直接模式挂载时（没有 `--clone` 的工作区默认如此），`git status`、`git log` 或目录扫描等文件系统操作会明显变慢。Virtiofs 缓存可以加速这些工作负载。克隆模式沙盒始终启用它，因此此调优仅适用于直接模式。

Virtiofs 缓存在所有操作系统上默认启用。如果你遇到 Git 索引损坏或意外的文件内容，请使用终止开关禁用缓存并重建沙盒：

```console
$ DOCKER_SANDBOXES_ENABLE_VIRTIOFS_CACHE=0 sbx run <template>
```

## 克隆模式在 WSL 上报告"不在 Git 仓库中"

在 Windows 上，针对位于 WSL 文件系统（`\\wsl.localhost\...` 路径）上的仓库运行 [`sbx run --clone`](usage.md#clone-mode) 可能会失败，即使该目录是一个有效的 Git 仓库：

```console
> sbx run --clone claude \\wsl.localhost\Ubuntu\home\you\repo
ERROR: --clone requires a Git repository, but \\wsl.localhost\Ubuntu\home\you\repo is not in a Git repository
```

原因是 Git 的可疑所有权检查。当 Windows 上的 Git 访问由 WSL 边界另一侧的不同用户拥有的仓库时，它会拒绝操作，因此底层的仓库检测失败：

```console
> git -C \\wsl.localhost\Ubuntu\home\you\repo rev-parse --show-toplevel
fatal: detected dubious ownership in repository at '//wsl.localhost/Ubuntu/home/you/repo'
```

将仓库添加到 Git 的 `safe.directory` 列表以允许访问，然后再次运行该命令：

```console
> git config --global --add safe.directory '%(prefix)///wsl.localhost/Ubuntu/home/you/repo'
> sbx run --clone claude \\wsl.localhost\Ubuntu\home\you\repo
✓ Git repository detected: \\wsl.localhost\Ubuntu\home\you\repo
```

## 沙盒提交未签名

Docker Sandboxes 可以使用你宿主 agent 的 SSH 密钥签署 Git 提交。设置步骤请参阅 [提交签名](workflows.md#commit-signing)。

如果 `ssh-add -L` 打印 `The agent has no identities.`，说明沙盒可以到达转发的 agent，但宿主 agent 没有加载的密钥。将签名密钥加载到你的宿主 SSH agent：

```console
$ ssh-add ~/.ssh/id_ed25519
```

如果提交签名在宿主上有效但在沙盒中失败，请检查 Git 是否配置为使用宿主文件路径（例如 `/Users/me/.ssh/id_ed25519.pub`）进行签名。沙盒使用的是转发的 SSH agent，而不是宿主密钥文件路径。请改用内联公钥形式：

```console
$ git config --global gpg.format ssh
$ git config --global user.signingkey "key::$(ssh-add -L | head -n 1)"
```

如果 Git 报告需要配置 `ssh-keygen` 缺失，请使用包含 OpenSSH 客户端工具的沙盒模板。

如果 `git log --show-signature` 报告需要配置 `gpg.ssh.allowedSignersFile`，说明 Git 无法在本地验证 SSH 签名。此验证配置对于创建签名提交不是必需的。GitHub 使用你 GitHub 账户中配置的 SSH 签名密钥来验证提交。

GPG 和 S/MIME 签名密钥在沙盒内部不可用。如果你的仓库或组织要求 GPG 或 S/MIME 签名，或者未配置 SSH 签名，请使用以下解决方法之一：

- 在沙盒之外提交。让 agent 在不提交的情况下进行更改，然后从你的宿主终端提交并签名。
- 事后签名。让 agent 在沙盒内提交，然后在宿主上重新签署提交：

  ```console
  $ git rebase --exec 'git commit --amend --no-edit -S' origin/main
  ```

  这会在分支上重放每个提交，并用你的本地签名密钥重新签署它。

## 降级后守护进程无法启动

如果你将 `sbx` 降级到比最后管理你本地状态的版本更旧的版本，守护进程可能会因数据库版本不匹配而启动失败：

```text
ERROR: failed to start backend in-process: start backend: creating containerd
server: ... database is at major version 6, but this binary only supports up
to major version 1
```

较新版本的 `sbx` 将本地数据库升级到了旧二进制文件无法理解的 schema。要恢复，请重置所有沙盒状态：

```console
$ sbx reset --preserve-secrets
```

这会停止所有 VM 并删除所有沙盒数据。之后你需要创建新的沙盒。 `--preserve-secrets` 标志会保留你设置的任何凭据，因此你无需重新配置它们。

## 移除所有状态

作为最后的手段，如果 `sbx reset` 无法解决你的问题，你可以完全移除 `sbx` 状态目录。这会删除所有沙盒数据、配置和缓存的镜像。请先用 `sbx reset` 停止所有运行中的沙盒。

**macOS**



```console
$ rm -rf ~/Library/Application\ Support/com.docker.sandboxes/
```

**Windows**



```powershell
> Remove-Item -Recurse -Force "$env:LOCALAPPDATA\DockerSandboxes"
```

**Linux**



Linux 上的沙盒状态遵循 XDG Base Directory 规范，分布在三个目录中：

```console
$ rm -rf ~/.local/state/sandboxes/
$ rm -rf ~/.cache/sandboxes/
$ rm -rf ~/.config/sandboxes/
```

如果你设置了自定义的 `XDG_STATE_HOME`、`XDG_CACHE_HOME` 或 `XDG_CONFIG_HOME` 环境变量，请将 `~/.local/state`、`~/.cache` 和 `~/.config` 替换为相应的值。



## 报告问题

如果你已穷尽上述步骤但问题仍然存在，请在 [github.com/docker/sbx-releases/issues](https://github.com/docker/sbx-releases/issues) 提交一个 GitHub issue。

为了帮助 Docker 调查，请生成一份诊断包，并在报告问题时分享它：

```console
$ sbx diagnose --upload
```

该包包含守护进程日志、诊断检查结果和基本系统信息。当确认 `--upload` 时，该包会被上传到 Docker 支持，并且命令会打印一个诊断 ID。在你的 issue 中包含此 ID，以便团队能将其与上传的包关联起来。

