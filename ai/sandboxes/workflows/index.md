# 有效使用沙盒




本指南介绍使用隔离代理的实用模式。

## 基本工作流

为你的项目创建一个沙盒：

```console
$ cd ~/my-project
$ docker sandbox run claude .
```

沙盒具有持久性。停止并重新启动时不会丢失已安装的包或配置：

```console
$ docker sandbox run <sandbox-name>  # 后续重新连接
```

## 安装依赖

让代理安装所需内容：

```plaintext
你： "安装 pytest 和 black"
Claude： [通过 pip 安装包]

你： "安装 build-essential"
Claude： [通过 apt 安装]
```

代理具有 sudo 权限。已安装的包在其生命周期内持续存在。这适用于系统包、语言包和开发工具。

对于团队或重复设置，请使用 [自定义模板](templates.md) 预先安装工具。

## 沙盒内的 Docker

代理可以构建镜像、运行容器并使用 Docker Compose。所有操作都在沙盒的私有 Docker 守护进程中运行。

### 测试容器化应用

```plaintext
你： "构建 Docker 镜像并运行测试"

Claude： *执行*
  docker build -t myapp:test .
  docker run myapp:test npm test
```

代理启动的容器运行在沙盒内部，而非你的主机上。它们不会出现在你主机的 `docker ps` 中。

### 多容器架构

```plaintext
你： "使用 docker-compose 启动应用并运行集成测试"

Claude： *执行*
  docker-compose up -d
  docker-compose exec api pytest tests/integration
  docker-compose down
```

删除沙盒后，所有镜像、容器和卷都会被清除。

## 什么会持续存在

沙盒存在期间：

- 已安装的包（apt、pip、npm 等）
- 沙盒内的 Docker 镜像和容器
- 配置更改
- 命令历史

删除沙盒时：

- 内部所有内容都会被删除
- 你的工作区文件保留在主机上（已同步回来）

若要保留已配置的环境，请创建一个 [自定义模板](templates.md)。

## 安全注意事项

代理可以创建和修改你挂载工作区中的任何文件，包括脚本、配置文件和隐藏文件。

在代理操作过工作区后，在主机上执行可能运行代码的操作前，请先审查更改：

- 提交更改（会执行 Git hooks）
- 在 IDE 中打开工作区（可能自动运行脚本或插件）
- 运行代理创建或修改过的脚本或可执行文件

审查变更内容：

```console
$ git status                        # 查看已修改和新增的文件
$ git diff                          # 查看已跟踪文件的变更
```

检查未跟踪的文件，并注意 `.git/hooks/` 中的 Git hooks 等变更不会出现在标准 diff 中。

这与 Visual Studio Code 等编辑器使用的信任模型相同，后者在打开新工作区时也会发出警告。

## 命名沙盒

为可重复使用的沙盒使用有意义的名称：

```console
$ docker sandbox run --name myproject claude ~/project
```

为同一工作区创建多个沙盒：

```console
$ docker sandbox create --name dev claude ~/project
$ docker sandbox create --name staging claude ~/project
$ docker sandbox run dev
```

每个沙盒保持独立的包、Docker 镜像和状态，但共享工作区文件。

## 调试

通过交互式 shell 直接访问沙盒：

```console
$ docker sandbox exec -it <sandbox-name> bash
```

在 shell 内部，你可以检查环境、手动安装包或查看 Docker 容器：

```console
agent@sandbox:~$ docker ps
agent@sandbox:~$ docker images
```

列出所有沙盒：

```console
$ docker sandbox ls
```

## 管理多个项目

为不同项目创建沙盒：

```console
$ docker sandbox create claude ~/project-a
$ docker sandbox create claude ~/project-b
$ docker sandbox create claude ~/work/client-project
```

每个沙盒完全隔离。通过运行相应名称切换沙盒。

删除未使用的沙盒以释放磁盘空间：

```console
$ docker sandbox rm <sandbox-name>
```

## 下一步

- [自定义模板](templates.md)
- [架构](architecture.md)
- [网络策略](network-policies.md)
---
