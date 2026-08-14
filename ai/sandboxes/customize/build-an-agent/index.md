# 构建你自己的 agent kit




> [!NOTE]
> Kits 处于实验阶段。随着功能演进，kit 文件格式、CLI 命令，以及创建、加载和管理
> kit 的体验都可能发生变化。请在 [docker/sbx-releases](https://github.com/docker/sbx-releases)
> 仓库中反馈意见和提交 bug 报告。

本教程将逐步讲解如何为 [Amp](https://ampcode.com/) 编程 agent 构建一个 agent kit。
每一步都会解释 spec 中某一部分背后的决策，以便你将同样的思路应用到其他 agent 上。

关于每个字段的参考，请参阅 [Kit spec 参考](kit-reference.md)。本教程侧重于整个构建过程。

完成后的 kit 也作为一个可运行的示例发布在
[docker/sbx-kits-contrib](https://github.com/docker/sbx-kits-contrib/tree/main/amp) — 
在跟随本教程时可作为参考。

## 选择基础镜像

agent kit 需要一个满足 [基础镜像要求](kit-reference.md#base-image-requirements) 的
容器镜像：UID 为 1000 的非 root `agent` 用户、无需密码的 sudo、`/home/agent/` 家目录，
以及 HTTP 代理环境变量转发。

与其从零构建镜像，不如扩展某个已发布的沙箱模板。三个常见的起点：

- `docker/sandbox-templates:shell`。通用基础镜像，未预装 agent。
- `docker/sandbox-templates:shell-docker`。同上，但在沙箱内置 Docker Engine。
- 特定 agent 的变体（`claude-code`、`codex` 等）。仅在你扩展该特定 agent 时有用。

对于 Amp，选择 `shell-docker`：

- Amp 未预装在任何变体中，因此你需要一个通用基础镜像（`shell`）。
- Docker 支持很方便，因为编程 agent 通常需要运行容器。
- 如果你不需要沙箱内的 Docker，可以使用 `shell` 标签以获得更轻量、非特权的环境。

## 规划认证

Amp 使用 `AMP_API_KEY` 中的 API 密钥进行认证。为了让真实密钥不进入 VM，你将工作
分成两部分：

- kit 的 network 部分将 API 主机映射到一个服务标识符，并告诉代理要注入哪个请求头。
- 你在宿主机上通过 sbx 的密钥存储提供密钥一次。真实值保留在宿主机上；只有占位符
  会进入沙箱。

在沙箱内 `AMP_API_KEY` 被设为该占位符。代理在发往 API 主机的出站请求上替换真实
密钥，因此密钥永远不会进入沙箱。后面的小节会逐步讲解存储密钥的具体命令。

## 编写 sandbox 块

`sandbox:` 块告诉沙箱在用户连接时如何启动 Amp。

```yaml {title="amp/spec.yaml"}
schemaVersion: "1"
kind: sandbox
name: amp
displayName: Amp
description: The frontier coding agent.

sandbox:
  image: "docker/sandbox-templates:shell-docker"
  aiFilename: AGENTS.md
  entrypoint:
    run: [amp, --dangerously-allow-all]
```

- `aiFilename: AGENTS.md` 告诉沙箱在启动时创建 `AGENTS.md`，并将
  [`agentContext`](#prime-amp-with-memory) 块追加到其中。Amp 读取此文件获取指令。
- `entrypoint.run` 在沙箱启动时以"YOLO 模式"运行 `amp`。如果你想在启动时传入不同的
  参数，可以调整。

## 安装 Amp

Amp 通过 curl-to-bash 脚本安装：

```yaml
commands:
  install:
    - command: "curl -fsSL https://ampcode.com/install.sh | bash"
      user: "1000"
      description: Install Amp
```

注意 `user: "1000"`。那就是 agent 用户。安装命令默认以 root（UID 0）运行，而 Amp
的安装程序将二进制文件放在用户的家目录中。以 root 运行会把二进制文件放到 `/root/`
下，agent 无法访问。

## 允许网络访问

network 块做两件事：列出沙箱可以到达的主机（`allowedDomains`），并通过
`serviceDomains` 和 `serviceAuth` 接好 [规划认证](#plan-authentication) 中
认证流程的 kit 一侧。

```yaml
network:
  serviceDomains:
    ampcode.com: amp
  serviceAuth:
    amp:
      headerName: Authorization
      valueFormat: "Bearer %s"
  allowedDomains:
    - "ampcode.com:443"
    - "*.ampcode.com:443"
```

这里的 `allowedDomains` 覆盖了主域名（`ampcode.com`）和安装/CDN 子域名
（`*.ampcode.com`）。把它当作起点；Amp 可能会访问其他域名（模型提供商、分析、更新），
你可以通过在测试时观察 `sbx policy log` 来发现。

kit 还可以声明 `deniedDomains`，用于沙箱不应到达的主机，例如遥测端点。拒绝规则优先于
允许规则，且仅适用于使用该 kit 的沙箱。

对于认证接线的部分，当 agent 向 `ampcode.com` 发出出站请求时，代理在 `serviceDomains`
中查找该主机以找到服务 id `amp`，然后使用 `serviceAuth.amp` 注入一个
`Authorization: Bearer <key>` 请求头。`<key>` 的值来自你将在
[注册你的 API 密钥](#register-your-api-key) 中按主机注册的密钥。服务 id（`amp`）只是
一个将两个块关联起来的标签——可以任取名字。

> [!IMPORTANT]
> 保持 `serviceDomains` 范围狭窄。映射 `*.ampcode.com` 会让代理对所有子域名（包括安装
> 脚本下载二进制文件的 CDN）进入 TLS 拦截模式，从而损坏这些下载。只列出真正需要认证的
> 主机。

## 用记忆初始化 Amp

`agentContext` 字段在创建沙箱时向 `AGENTS.md` 追加 markdown。用它告诉 Amp 沙箱环境，
让它在启动时了解约定。

```yaml
agentContext: |
  ## Sandbox environment

  You are running inside a Docker sandbox. The workspace is mounted at
  its absolute host path. `sudo` is passwordless; use it for package
  installs. Docker is available inside the sandbox; containers you start
  are isolated in the microVM.
```

保持简短且针对沙箱。对于项目说明，请在 workspace 中放置一个常规的 `AGENTS.md`。

## 完整 spec

把它们组合在一起：

```yaml {title="amp/spec.yaml"}
schemaVersion: "1"
kind: sandbox
name: amp
displayName: Amp
description: The frontier coding agent.

sandbox:
  image: "docker/sandbox-templates:shell-docker"
  aiFilename: AGENTS.md
  entrypoint:
    run: [amp, --dangerously-allow-all]

network:
  serviceDomains:
    ampcode.com: amp
  serviceAuth:
    amp:
      headerName: Authorization
      valueFormat: "Bearer %s"
  allowedDomains:
    - "ampcode.com:443"
    - "*.ampcode.com:443"

commands:
  install:
    - command: "curl -fsSL https://ampcode.com/install.sh | bash"
      user: "1000"
      description: Install Amp

agentContext: |
  ## Sandbox environment

  You are running inside a Docker sandbox. The workspace is mounted at
  its absolute host path. `sudo` is passwordless; use it for package
  installs.
```

## 注册你的 API 密钥

在宿主机上使用 `sbx secret set-custom` 注册你的 Amp API 密钥。该值进入宿主机密钥存储，
而一个占位符会在你使用该 kit 启动的每个沙箱中暴露。

Amp 在启动时会校验 `AMP_API_KEY` 的格式，因此占位符需要看起来像一个真实的 Amp 密钥。
选择一个匹配 Amp 期望格式的占位符形态：

```console
$ sbx secret set-custom \
    --host ampcode.com \
    --env AMP_API_KEY \
    --placeholder "sgamp-{rand}" \
    --value "$AMP_API_KEY"
```

`{rand}` 在注册时展开为随机后缀。在沙箱内 `AMP_API_KEY` 被设为该占位符；Amp 接受它
作为语法有效的密钥，代理在发往 `ampcode.com` 的出站请求上替换真实密钥。

> [!TIP]
> 仅因为 Amp 会校验密钥格式才需要 `sbx secret set-custom`。如果你的 agent 读取环境变量
> 时不进行本地格式检查，可以在 kit 中声明 `environment.proxyManaged: [AMP_API_KEY]` 来
> 跳过用户侧的这一步——代理使用一个默认哨兵值（`proxy-managed`），agent 永远不会看到
> 它被拒绝。

> [!NOTE]
> `sbx secret set-custom` 是实验性的，在未来的版本中可能变化。本教程提到它，是因为没有
> 其他途径可以注册自定义格式的占位符。

## 运行它

校验 spec：

```console
$ sbx kit validate ./amp/
```

使用该 kit 启动沙箱，将 kit 的 `name:`（`amp`）作为 agent 参数传入：

```console
$ sbx run --kit ./amp/ amp
```

本 kit 的已发布副本也可以直接从 contrib 仓库运行：

```console
$ sbx run --kit "git+https://github.com/docker/sbx-kits-contrib.git#dir=amp" amp
```

## 迭代

在使用 kit 时，你可能会遇到缺失的域名或安装怪癖。两个循环有帮助：

- 观察网络策略日志（`sbx policy log`）以捕获被阻止的请求，然后将它们的域名添加到
  `allowedDomains`。
- 当 agent 即使被其他策略允许也应保持对某个主机的阻断时，将域名添加到 `deniedDomains`。
- 编辑 spec 并重新运行 `sbx run --kit ./amp/ amp` 以应用更改。先移除沙箱（`sbx rm <name>`）
  以获得干净的开始。

随着你细化 Amp 在沙箱中应有的行为，`agentContext` 块也逐步充实。

## 发布

kit 可用后，将其打包为 ZIP、推送到 OCI 仓库，或提交到 Git 仓库来分享。有关 `sbx kit`
子命令，请参阅 [打包与分发](kits.md#packaging-and-distribution)。

## 适配到其他 agent

这里的多数细节都是 Amp 特有的。要移植该模式，为你的 agent 走一遍相同的决策：

- **基础镜像**：如果需要沙箱内的 Docker 则用 `shell-docker`，否则用 `shell`。如果安装
  较重，也可以用你自己的镜像扩展两者之一。
- **安装**：运行时的 `commands.install` 块，或将 agent 烘焙进自定义镜像。如果是一行脚本
  则选择安装；如果安装很慢或你需要固定版本，则烘焙。
- **网络映射**：在 `serviceDomains` 中只列出 API 主机，而不是通配符。让安装/CDN 路径避开
  TLS 拦截模式。对 agent 不应到达的主机使用 `deniedDomains`。
- **凭据注入**：如果 agent 在本地校验 API 密钥格式，用 `sbx secret set-custom` 注册并选择
  匹配的占位符。如果它原样接受环境变量，则在 kit 中声明 `environment.proxyManaged` 并跳过
  用户侧步骤。

其余部分——agent 上下文块、网络策略迭代、打包——与 agent 无关，都是一样的。

## 移除存储的密钥

要移除早先用 `sbx secret set-custom` 创建的条目，将主机传给 `sbx secret rm`：

```console
$ sbx secret rm --host ampcode.com
```

`--host` 标志是实验性 `set-custom` 接口的一部分，不会出现在 `sbx secret rm --help` 中。

