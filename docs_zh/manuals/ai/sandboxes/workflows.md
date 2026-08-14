<!-- FILE: manuals/ai/sandboxes/workflows.md -->

---
title: 工作流模式
linkTitle: 工作流
weight: 30
description: Docker Sandboxes 的工作流模式，涵盖共享 agent 技能、git 策略、本地服务、鉴权工具和 CI 集成。
keywords: docker sandboxes, sbx, workflows, agent skills, shared skills, clone mode, git, branches, commit signing, github cli, local services, ci, headless
---

当你需要为某种特定的沙盒使用方式选择方法时，使用本页。有关命令语法和生命周期基础，请参阅 [用法](usage.md)。

## 共享 agent 技能

共享 agent 技能将宿主上受支持 agent 的技能提供给你的沙盒内部使用。导入会将技能复制到一个持久的存储中，该存储在沙盒删除后仍然存在，并默认与运行受支持 agent 的新沙盒共享。

> [!NOTE]
> 共享 agent 技能是实验性的。

在不复制它们的情况下预览 `sbx` 找到的技能：

```console
$ sbx skills import --dry-run
```

该命令按顺序扫描以下目录，并将每个技能子目录复制到共享存储中。当沙盒启动时，`sbx` 将该存储挂载到 agent 在沙盒内读取的路径。

| Agent       | 宿主来源            | 沙盒挂载目标                |
| ----------- | ------------------- | --------------------------- |
| Claude Code | `~/.claude/skills`  | `/home/agent/.claude/skills`  |
| Codex       | `~/.agents/skills`  | `/home/agent/.agents/skills`  |
| Copilot     | `~/.copilot/skills` | `/home/agent/.copilot/skills` |
| Cursor      | `~/.cursor/skills`  | `/home/agent/.cursor/skills`  |
| Droid       | `~/.factory/skills` | `/home/agent/.factory/skills` |

所有导入的技能都会进入同一个存储，无论其来源如何。如果多个来源包含同名的技能目录，则表中第一个来源中的技能胜出，`sbx` 会就其他来源发出警告。

导入技能：

```console
$ sbx skills import
```

最终输出会报告共享存储路径。默认位置为：

| 平台    | 共享存储路径                                                                     |
| ------- | ------------------------------------------------------------------------------- |
| macOS   | `~/Library/Application Support/com.docker.sandboxes/sandboxes/agent-skills`     |
| Linux   | `~/.local/state/sandboxes/sandboxes/agent-skills`                              |
| Windows | `%LOCALAPPDATA%\DockerSandboxes\sandboxes\state\agent-skills`                  |

在 Linux 上，当设置了 `XDG_STATE_HOME` 时，`sbx` 使用 `$XDG_STATE_HOME/sandboxes/sandboxes/agent-skills`。

当存储中已存在某个技能时，`sbx` 在替换前会提示。使用 `--force` 可在不提示的情况下替换现有技能。导入会替换整个技能目录，而不是合并文件。当你想从宿主复制更新时，再次运行导入命令。运行 `sbx reset` 会清除共享存储。

为受支持 agent 使用 `sbx` 0.37.0 或更高版本创建的沙盒，默认配置为以读写方式挂载该存储。这些沙盒每次启动时都挂载该存储的当前内容，因此你可以在创建它们之前或之后导入技能。要创建一个不带共享存储的沙盒，使用 `--no-share-skills`：

```console
$ sbx run --no-share-skills claude
```

升级 `sbx` 不会为使用早期版本创建的沙盒启用共享技能。升级后请移除并重建这些沙盒。`--no-share-skills` 选项也仅在创建沙盒时适用。要为一个现有沙盒关闭共享技能，请移除并使用该选项重建它。

> [!WARNING]
> 共享技能存储以读写方式挂载。一个沙盒可以修改存储中的任何技能，另一个沙盒稍后可能加载被修改的指令或运行被修改的脚本。该存储是专用的沙盒状态，因此这本身不会在你的宿主上执行被修改的技能。但它确实将所有共享该存储的沙盒置于同一个信任边界中。使用 `--no-share-skills` 使一个沙盒保持在那个边界之外。

一些 agent 在会话启动时会扫描技能。如果导入的技能没有出现在现有会话中，请启动另一个 agent 会话。

## Git 工作流

沙盒支持三种与 Git 仓库协作的方法。正确的选择取决于你是否想要分支隔离，以及你是否计划并行运行任务：

|                           | 直接模式        | 克隆模式（`--clone`）        | 宿主 worktree                  |
| ------------------------- | ---------------- | ---------------------------- | ----------------------------- |
| 分支管理                  | 你，在宿主上     | agent，在克隆内              | 你，在宿主上                 |
| 在宿主上可见的更改        | 立即             | 获取或 agent 推送之后        | 立即                          |
| agent 可以使用 Git        | 是               | 是                           | 否                            |
| 并行性                    | 否               | 多个 agent，一个沙盒         | 每个并行任务一个沙盒          |
| 创建时固定的模式          | 否               | 是                           | —                             |

### 直接模式

最简单的方法。沙盒直接挂载你的宿主工作树——agent 就地编辑文件，更改立即可见。分支由你自己管理。

1. 检出你想要工作的分支：

   ```console
   $ git checkout -b feat/my-feature
   ```

2. 启动沙盒。不需要特殊标志：

   ```console
   $ sbx run claude
   ```

3. agent 编辑你工作树中的文件。像平常一样审查 diff、暂存并提交：

   ```console
   $ git diff
   $ git add -p
   $ git commit
   $ git push -u origin feat/my-feature
   ```

因为沙盒挂载了你的工作树，在宿主上切换分支也会改变 agent 看到的内容。这使得直接模式非常适合聚焦的、单分支的工作，即你与 agent 逐轮协作。

### 克隆模式

在克隆模式下，`sbx` 在沙盒内部创建一个独立的 Git 克隆。agent 编辑这个克隆，而不是你的宿主工作树。它的更改停留在沙盒内部，直到你获取一个分支或 agent 将其推送到远程。你的宿主仓库在 `/run/sandbox/source` 也可用，但只有读访问。沙盒克隆不是链接到你宿主检出的 Git worktree。

一个克隆模式沙盒可以容纳多个分支和 worktree 用于并行任务。`--clone` 标志创建克隆，但它不会将一个任务与另一个任务分开。要保持并行任务隔离，请指示你的 agent 工具为每个任务创建一个独立的分支或 worktree。

> [!NOTE]
> `--clone` 是创建时的标志，无法在现有沙盒上更改。要将沙盒从克隆模式改为直接模式，请移除并重建它。要对同一仓库同时运行两种模式，请使用不同的名称为其创建独立的沙盒。

#### 沙盒远程行为

CLI 将 Git 远程从你的宿主仓库（例如 `origin` 和 `upstream`）复制到沙盒内的克隆中。本地路径远程，例如 `file://` URL 和文件系统路径，不会被复制，因为它们在沙盒内部不可达。

暴露沙盒内克隆的 Git 守护进程作为沙盒的一部分运行。它仅在沙盒运行期间可达：

- `sbx stop` 会关闭该守护进程。在沙盒再次启动之前，`git fetch sandbox-<name>` 会失败。
- 重启沙盒会为守护进程分配另一个临时端口。CLI 会更新你宿主仓库 Git 配置中的 `sandbox-<name>` 远程 URL，因此无需手动重新配置即可继续获取。
- `sbx rm` 会移除沙盒、守护进程、已发布的端口，以及你宿主仓库中的 `sandbox-<name>` 远程条目。

#### 单一任务

1. 启动一个克隆模式沙盒：

   ```console
   $ sbx run --clone claude
   ```

2. 让 agent 在它开始编辑之前创建一个分支：

   > 创建一个分支 `feat/my-feature` 并进行更改。

3. agent 完成后获取它的分支：

   ```console
   $ git fetch sandbox-<name>
   $ git log sandbox-<name>/feat/my-feature
   $ git diff main..sandbox-<name>/feat/my-feature
   ```

4. 将分支拉取到宿主并推送，或者让 agent 直接推送：

   ```console
   # 拉取到宿主，然后推送
   $ git checkout -b feat/my-feature sandbox-<name>/feat/my-feature
   $ git push -u origin feat/my-feature
   $ gh pr create

   # 或者让 agent 来做
   # "将 feat/my-feature 推送到 origin 并打开一个 PR。"
   ```

#### 并行任务

1. 启动一个克隆模式沙盒并打开 [agents 视图](agents/claude-code.md#agents-view)：

   ```console
   $ sbx run --clone claude
   ```

2. 将每个独立的任务分派到一个独立的后台会话。你的 agent 工具可能会使用分支或 worktree 来保持其更改分离。如果没有，请添加一条项目指令，例如：

   ```markdown
   在每次更改之前，始终在自己的 git 分支上开始每个任务。
   ```

3. agent 完成后获取所有分支：

   ```console
   $ git fetch sandbox-<name>
   $ git log sandbox-<name>/feat/task-a
   $ git log sandbox-<name>/feat/task-b
   ```

4. 检出你想保留的分支并像平常一样打开 PR。

### 宿主 worktree

你可以在宿主上创建一个 Git worktree，并将沙盒指向它。agent 直接在 worktree 中编辑文件——但因为沙盒只挂载 worktree 目录（而不是父仓库），它无法解析 `.git` 指针文件，也没有 Git 访问权限。agent 可以读写文件，但不能提交、分支或查看状态。

当你想要分支隔离而不需要克隆模式那样的创建时承诺，并且你乐于在审查更改后自己从宿主提交时，这很有用。

1. 在宿主上创建 worktree：

   ```console
   $ git worktree add -b feat/my-feature ../my-feature-work
   ```

2. 以 worktree 作为工作区启动沙盒：

   ```console
   $ sbx run claude ../my-feature-work
   ```

3. agent 编辑文件。完成后，从宿主提交并推送：

   ```console
   $ cd ../my-feature-work
   $ git diff
   $ git add -p && git commit
   $ git push -u origin feat/my-feature
   $ gh pr create
   ```

## 在沙盒内构建和测试

agent 在沙盒内部拥有 sudo 访问权限，因此它可以安装包、启动数据库、运行测试依赖并准备它所需的环境。已安装的包在沙盒生命周期内持续存在。对于重复的设置，使用 [自定义](customize/) 将环境打包为模板或 kit。

agent 还可以构建 Docker 镜像、运行容器并使用 [Compose](/manuals/compose/_index.md)。一切都运行在沙盒的私有 Docker 守护进程内，因此 agent 启动的容器永远不会出现在你宿主的 `docker ps` 中。当你移除沙盒时，其中的所有镜像、容器和卷都会被删除。

这种模式非常适合 agent 需要运行项目的测试套件或检查它启动的服务的任务。如果你需要从宿主到达该服务，请在创建沙盒时发布端口，或稍后用 `sbx ports` 发布。

## 本地服务

当一个沙盒化的 agent 启动了一个开发服务器，或者 agent 需要调用在你宿主上运行的服务时，使用此工作流。

### 访问沙盒内的服务

沙盒是[网络隔离](security/isolation.md)的——你的浏览器或本地工具默认无法到达在其中运行的服务器。端口映射 `8080:3000` 将沙盒端口 3000 发布到宿主端口 8080。

如果你知道需要哪些端口，在创建沙盒时发布它们：

```console
$ sbx run --publish 8080:3000 --name my-sandbox claude
```

对于现有沙盒，使用 [`sbx ports`](/reference/cli/sbx/ports/) 从宿主转发流量。

常见情况：一个 agent 已经启动了一个开发服务器或 API，你想在浏览器中打开它或针对它运行测试。

```console
$ sbx ports my-sandbox --publish 8080:3000
$ open http://localhost:8080
```

要让操作系统选择一个空闲的宿主端口，而不是自己指定，只指定沙盒端口。然后使用 `sbx ports` 检查分配了哪个宿主端口：

```console
$ sbx ports my-sandbox --publish 3000
$ sbx ports my-sandbox
```

`sbx ls` 在每个沙盒旁边显示活动的端口映射，`sbx ports` 详细列出它们：

```console
$ sbx ls
SANDBOX         AGENT   STATUS   PORTS                    WORKSPACE
my-sandbox      claude  running  127.0.0.1:8080->3000/tcp /home/user/proj
```

要停止转发一个端口：

```console
$ sbx ports my-sandbox --unpublish 8080:3000
```

要使服务可达，它必须在沙盒内部监听所有接口，而不仅是 `127.0.0.1`。将其绑定到 IPv4 的 `0.0.0.0` 或同时支持 IPv4 和 IPv6 的 `[::]`。大多数开发服务器需要一个像 `--host 0.0.0.0` 这样的标志才能做到这一点。在宿主上，`--publish` 监听 `127.0.0.1` 和 `::1`，因此如果沙盒服务只监听 IPv4，解析 `localhost` 的客户端可能选择 IPv6 并因"connection reset by peer"而失败，即使 `http://127.0.0.1:<port>/` 可以工作。要修复这个问题，请将服务绑定到 `[::]`，或使用 `/tcp4` 或 `/tcp6` 将发布的端口固定到某一地址族。

已发布的端口在重启后仍然保留：`sbx` 在沙盒或守护进程重启时重新发布它们。显式的宿主端口会被复用，而使用操作系统分配的宿主端口（例如 `--publish 3000`）在每次启动时会得到不同的宿主端口。使用 `sbx ports my-sandbox` 查找它。如果显式宿主端口在重启时已被占用，CLI 或仪表板会提示你选择另一个。移除沙盒会释放其端口。

当 `sbx run` 重新附加到现有沙盒时，它会忽略 `--publish`。使用 `sbx ports` 在该沙盒上发布端口。要停止转发，`--unpublish 8080:3000` 移除单个映射，`--unpublish 3000` 移除所有映射到沙盒端口 3000 的宿主端口。

### 从沙盒访问宿主服务

使用主机名 `host.docker.internal` 可以从沙盒内部到达在你宿主上运行的服务。请使用它而不是 `127.0.0.1` 或你机器的本地网络 IP 地址，它们在沙盒内部不可达。

沙盒代理在转发请求之前将 `host.docker.internal` 转换为 `localhost`，因此你必须将特定的端口和 `localhost` 地址添加到你的网络策略允许列表：

```console
$ sbx policy allow network localhost:11434
```

然后在任何指向宿主服务的配置或请求中使用 `host.docker.internal`。例如，要从沙盒 shell 验证连通性：

```console
$ curl http://host.docker.internal:11434
```

## 提交签名

沙盒将你的宿主 SSH agent 转发进沙盒，因此 agent 可以在私钥永不离开宿主的情况下使用你的 SSH 密钥签署提交。

1. 在你的宿主上，确保签名密钥已加载到你的 SSH agent 中：

   ```console
   $ ssh-add ~/.ssh/id_ed25519
   $ ssh-add -L  # 确认密钥出现
   ```

2. 在沙盒内部，将 Git 配置为使用 SSH 签名。直接使用转发的密钥，而不是文件路径，因为宿主路径在沙盒内部不存在：

   ```console
   $ git config --global gpg.format ssh
   $ git config --global user.signingkey "key::$(ssh-add -L | head -n 1)"
   ```

3. 像平常一样签署提交：

   ```console
   $ git commit -S -m "feat: my change"
   ```

要将此配置自动应用到每个沙盒，请使用 [`git-ssh-sign`](https://github.com/docker/sbx-kits-contrib/tree/main/git-ssh-sign) 社区 kit，它处理了上述所有设置。如果你希望将它与其他沙盒自定义一起打包，请参阅 [Kits](customize/kits.md)。

有关故障排除，请参阅 [沙盒提交未签名](troubleshooting.md#sandbox-commits-arent-signed)。

## 鉴权 CLI 工具

沙盒代理会自动处理模型提供商的 API 凭据，但 agent 通常还需要 `gh`、`docker` 或密钥管理器等工具的凭据。每种情况中的模式都是相同的：在宿主上配置一次凭据，然后沙盒通过代理或通过 SSH agent 转发将其转发进来。

> [!NOTE]
> 服务凭据默认是全局的，因此所有未来的沙盒都可以使用它们。当你运行 `sbx secret set` 时已经存在的沙盒不会收到更新后的值。要更新一个运行中的沙盒，请直接将该凭据限定到它：`sbx secret set <service> --sandbox <sandbox-name>`。

### GitHub CLI

将你的 GitHub 令牌存储为沙盒凭据。代理将其注入到出站请求中，因此 `gh` 在沙盒内部无需任何额外配置即可工作：

```console
$ echo "$(gh auth token)" | sbx secret set github
```

然后 agent 可以像在你的宿主上一样创建 pull request、开 issue、评论 PR 并与 GitHub API 交互：

```console
# 在沙盒内部
$ gh pr create --title "feat: my feature" --body "..."
$ gh issue list
```

令牌永远不会以明文形式存储在沙盒内部。详情请参阅 [GitHub 令牌](security/credentials.md#github-token)。

### Docker 注册表

使用 Docker Hub 时，鉴权会自动处理；`sbx` 复用你现有的登录会话。对于其他注册表，你需要为 `sbx` 配置凭据，以便它在创建沙盒时可以拉取私有 [模板](customize/templates.md) 和 kit：

```console
$ gh auth token | sbx secret set --all-sandboxes --registry ghcr.io \
    --username <github-username> --password-stdin
$ echo "$ACR_PASSWORD" | sbx secret set --all-sandboxes \
    --registry myregistry.azurecr.io \
    --username myuser --password-stdin
```

当 agent 需要从沙盒内部运行鉴权的 `docker pull` 或 `docker push` 命令时，添加 `-g` 或沙盒名称。宿主侧代理处理注册表登录，而不将凭据写入沙盒。

在沙盒内部构建的镜像和容器运行在沙盒的私有 Docker 守护进程上，而不是你的宿主上。它们在移除沙盒时被删除。

有关注册表凭据与其他凭据的不同之处、每个注册表的用户名要求，以及所有沙盒与每个沙盒范围的详细信息，请参阅 [注册表凭据](security/credentials.md#registry-credentials)。

### 从 1Password 获取凭据

#### 使用 `op read` 填充已存储凭据

使用 `op read` 填充已存储凭据，而无需手动粘贴值。存储一次，它对所有未来的沙盒都可用：

```console
$ op read "op://Work/GitHub/token" | sbx secret set github
$ op read "op://Work/Anthropic/credential" | sbx secret set anthropic
```

真实值保留在你的宿主上；沙盒像往常一样看到代理管理的占位符。

#### 使用 `op run` 每次启动注入

要在每次启动时从你的保险库即时解析凭据，而不通过 `sbx secret set` 存储它们，请使用 `op run`：

```console
$ ANTHROPIC_API_KEY="op://Work/Anthropic/credential" op run -- sbx run claude
$ OPENAI_API_KEY="op://Work/OpenAI/key" op run -- sbx run codex
$ GEMINI_API_KEY="op://Work/Google/key" op run -- sbx run gemini
```

`op run` 在执行 `sbx` 之前解析环境中的每个 `op://` 引用。沙盒在启动时读取[内置服务环境变量](security/credentials.md#built-in-services)，并通过其代理路由它们——凭据永远不会存储在 sbx 的状态中，也永远不会出现在沙盒容器内部。

这仅适用于那些特定的凭据变量。沙盒不会将任意环境变量从宿主转发进沙盒。

要一次处理多个凭据，请将带有 `op://` 引用的 `--env-file` 与文件一起使用：

```console
$ cat .sbx-secrets.env
ANTHROPIC_API_KEY=op://Work/Anthropic/credential
GITHUB_TOKEN=op://Work/GitHub/token

$ op run --env-file=.sbx-secrets.env -- sbx run claude
```

## CI 与无头使用

对于没有浏览器的 CI 环境和脚本，使用 Docker 个人访问令牌（PAT）鉴权：

```console
$ echo "$DOCKER_PAT" | sbx login --username <your-docker-id> --password-stdin
```

至少具有 **Read** 权限地生成 PAT，地址为你的 [Docker 账户设置](https://app.docker.com/settings/personal-access-tokens)。

从那里开始，其余的 `sbx` 工作流与交互式使用相同。使用 `sbx create` 在后台创建沙盒，使用 `sbx exec` 运行 agent 任务，并使用 `sbx rm` 清理：

```console
$ sbx create --name ci-task --clone claude
$ sbx run --name ci-task  # 附加并给出指令，或使用 sbx exec 执行一次性命令
$ git fetch sandbox-ci-task
$ sbx rm ci-task
```

agent 凭据（API 密钥、GitHub 令牌）可以作为全局凭据预先配置，以便 CI 运行器创建的任何沙盒都可用。如果相关环境变量已经在 CI 环境中设置（每个服务读取哪些变量，请参阅 [内置服务表](security/credentials.md#built-in-services)），一次性导入它们：

```console
$ sbx secret import --all
```

要覆盖现有的已存储条目，添加 `--force`。要从 CI 提供商的密钥存储传入一个值，请使用 `-t`。例如，在 GitHub Actions 步骤中：

```yaml
- run: sbx secret set anthropic -t "${{ secrets.ANTHROPIC_API_KEY }}"
```

## 在团队间共享设置

当多个人在同一个项目上使用沙盒时，将可重复的環境设置与策略执行分开。

使用 [自定义模板和 kit](customize/) 进行项目级设置：agent 配置、MCP 服务器、基础镜像、设置脚本和每项目默认值。将 kit spec 和模板定义与项目一起版本化，并将可复用的模板镜像发布到你的注册表。这为每位开发者提供了相同的起始环境。

使用 [组织策略](governance/access-controls/organization.md) 进行组织管理员跨开发者应用的控制，例如网络、文件系统和 MCP 策略。组织策略优先于本地策略，并且需要单独的付费订阅。

你可以两者都用。模板和 kit 描述开发环境；管控定义其运行的边界。
