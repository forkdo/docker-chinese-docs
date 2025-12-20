# Compose v2 版本说明

<!-- vale off -->

如需更详细的信息，请参阅 [Compose 仓库的版本说明](https://github.com/docker/compose/releases/)。

## 2.40.3

<em class="text-gray-400 italic dark:text-gray-500">2025-10-30</em>


### 错误修复与增强

- 生命周期钩子现在适用于 `restart` 命令
- 发布 OCI 制品时改进了覆盖支持
- 修复了确保 `run` 命令仅针对目标服务创建镜像的问题
- 添加了默认的 Prompt 实现

## 2.40.2

<em class="text-gray-400 italic dark:text-gray-500">2025-10-22</em>


### 错误修复与增强

- 添加了检查，如果未安装所需的最低 Buildx 版本则构建失败
- 移除了未使用的代码，完全依赖 api.Service
- 通过检查摘要/规范引用（而不仅是标签）改进了镜像检测
- 引入了 `WithPrompt`，为与用户交互添加了可插拔的 UI
- 回滚了 secret/config 的 `uid:gid` 设置修复，以匹配容器的 `USER` 定义

## 2.40.1

<em class="text-gray-400 italic dark:text-gray-500">2025-10-17</em>


### 错误修复与增强

- 修复了使用 bake 构建时的若干问题
- 添加了对使用 `publish` 命令时结合 profiles 的 extends 支持
- 添加了对 `CTRL+Z` 的支持，以便在后台运行 Compose
- 修复了 secret/config 的 `uid:gid` 设置，以匹配容器的 `USER` 定义

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.5.1
- 依赖升级：将 buildx 升级至 v0.29.1
- 依赖升级：将 golang 升级至 v1.24.9

## 2.40.0

<em class="text-gray-400 italic dark:text-gray-500">2025-10-03</em>


### 错误修复与增强

- 添加了将 Compose 应用发布为包含镜像的 `compose.yaml` 的选项
- 修复了使用 bake 构建时基于环境变量的 secrets 支持
- 修复了使用 bake 构建时对转义 '$' 字符的支持

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.5.0

## 2.39.4

<em class="text-gray-400 italic dark:text-gray-500">2025-09-19</em>


### 错误修复与增强

- 在 Compose Develop Specification 定义中添加了 `initial_sync` 属性，用于在启动监视会话后同步文件
- 修复了使用 bake 构建时的 TLS 问题
- 在作为管道命令运行时，禁用了 `run` 的 Tty

### 更新

- 依赖升级：将 compose-go 升级至 v2.9.0

## 2.39.3

<em class="text-gray-400 italic dark:text-gray-500">2025-09-09</em>


### 错误修复与增强

- 为 `--progress` 标志添加了补全支持
- 修复了使用 `bake` 构建时的次要问题
- 修复了发布带有绑定挂载和 `-y` 标志的 Compose 栈时的问题

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.4.0
- 依赖升级：将 compose-go 升级至 v2.8.2
- 依赖升级：将 buildx 升级至 v0.28.0
- 依赖升级：将 buildkit 升级至 v0.24.0
- 依赖升级：将 golang 升级至 v1.24.7

## 2.39.2

<em class="text-gray-400 italic dark:text-gray-500">2025-08-04</em>


### 错误修复与增强

- 修复了构建输出中的多个渲染问题
- 修复了 `pull` 和 `no_cache` 属性在使用 `bake` 时未生效的问题
- 移除了在 `up` 命令中显式未连接服务的日志显示

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.3.3
- 依赖升级：将 golang 升级至 v1.23.12
- 依赖升级：将 containerd 升级至 2.1.4

## 2.39.1

<em class="text-gray-400 italic dark:text-gray-500">2025-07-24</em>


### 错误修复与增强

- 添加了监控 `models` 使用情况的指标

### 更新

- 依赖升级：将 compose-go 升级至 v2.8.1

## 2.39.0

<em class="text-gray-400 italic dark:text-gray-500">2025-07-24</em>


### 错误修复与增强

- 为 `config` 命令添加了 `--models` 标志以列出模型
- 为 `events` 添加了 `--since` 和 `--until` 标志
- 在 `build` 部分引入了 `provenance` 和 `sbom` 属性
- 修复了 Windows 上的 `bridge convert` 问题
- 修复了 `bake` 构建的多个问题

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.3.2
- 依赖升级：将 buildx 升级至 v0.26.1
- 依赖升级：将 compose-go 升级至 v2.8.0

## 2.38.2

<em class="text-gray-400 italic dark:text-gray-500">2025-07-08</em>


### 错误修复与增强

- 为 `config` 命令添加了 `--networks` 标志以列出网络
- 修复了使用 Docker Model Runner 作为提供者服务时 `down` 命令的问题
- 修复了 Docker Model Runner 进度显示问题
- 修复了缺少 secrets 的带 profile 服务的问题

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.3.1
- 依赖升级：将 buildkit 升级至 v0.23.2
- 依赖升级：将 golang 升级至 v1.23.10

## 2.38.1

<em class="text-gray-400 italic dark:text-gray-500">2025-06-30</em>


### 错误修复与增强

- 添加了对服务 `models` 配置中 `model_variable` 的支持

### 更新

- 依赖升级：将 compose-go 升级至 v2.7.1

## 2.38.0

<em class="text-gray-400 italic dark:text-gray-500">2025-06-30</em>


### 错误修复与增强

- 引入了对 LLM 配置中 `models` 的支持
- 添加了 `volumes` 命令
- 移除了对绑定挂载的 `publish` 限制
- 修复了将 docker socket 挂载到不需要它的容器中的问题
- 修复了 bake 输出挂起的问题

### 更新

- 依赖升级：将 compose-go 升级至 v2.7.0
- 依赖升级：将 docker engine 和 cli 升级至 v28.3.0

## 2.37.3

<em class="text-gray-400 italic dark:text-gray-500">2025-06-24</em>


### 错误修复与增强

- 添加了对 Bake 的 `cache_to` 支持
- 修复了 Bake 集成问题
- 修复了影响 `run` 命令的多个问题

### 更新

- 依赖升级：将 buildkit 升级至 v0.23.1

## 2.37.2

<em class="text-gray-400 italic dark:text-gray-500">2025-06-20</em>


### 错误修复与增强

- 引入了 `use_api_socket`
- 修复了 `compose images` JSON 输出格式
- 修复了在没有监视支持的项目上使用 `w` 快捷键时的 panic 问题
- 修复了 Windows 上 bake 元数据文件的权限问题
- 修复了提供者服务启动时的 panic 错误

### 更新

- 依赖升级：将 compose-go 升级至 v2.6.5
- 依赖升级：将 buildx 升级至 v0.25.0
- 依赖升级：将 buildkit 升级至 v0.23.0

## 2.37.1

<em class="text-gray-400 italic dark:text-gray-500">2025-06-12</em>


### 错误修复与增强

- 修复了 Windows 上 bake 元数据文件的权限问题
- 修复了提供者服务启动时的 panic 错误
- 将 `compose images` JSON 输出恢复为数组格式

## 2.37.0

<em class="text-gray-400 italic dark:text-gray-500">2025-06-05</em>


### 错误修复与增强

- 修复了随机端口分配问题
- 修复了在内循环中不必要时重新创建容器的问题
- 修复了 `up --build` 与 `additional_context` 的问题

### 更新

- 依赖升级：将 compose-go 升级至 v2.6.4
- 依赖升级：将 buildx 升级至 v0.24.0
- 依赖升级：将 buildkit 升级至 v0.22.0

## 2.36.2

<em class="text-gray-400 italic dark:text-gray-500">2025-05-23</em>


### 错误修复与增强

- Compose Bridge 功能现已集成到 Compose 中
- 改进了 `docker compose images` 命令的显示
- 将 `bake` 提升为 Compose 的默认构建工具
- 修复了构建流程相关问题
- 修复了 `watch` 重建镜像后依赖服务重启的问题

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.2.2

## 2.36.1

<em class="text-gray-400 italic dark:text-gray-500">2025-05-19</em>


### 错误修复与增强

- 引入了对 `provider` 服务 `options` 属性数组的支持
- 在扩展协议中添加了 `debug` 消息
- 修复了尝试发布包含 `provider` 服务的 Compose 应用时的问题
- 修复了包含 `service.provider` 的 Compose 应用的构建问题
- 为 `config` 命令引入了 `--lock-image-digests`

### 更新

- 依赖升级：将 compose-go 升级至 v2.6.3
- 依赖升级：将 containerd 升级至 2.1.0

## 2.36.0

<em class="text-gray-400 italic dark:text-gray-500">2025-05-07</em>


### 错误修复与增强

- 引入了 `networks.interface_name`
- 添加了对 `COMPOSE_PROGRESS` 环境变量的支持
- 为外部二进制文件添加了 `service.provider`
- 引入了构建 `--check` 标志
- 修复了多个解析 Compose 文件时的 panic 问题

### 更新

- 依赖升级：将 compose-go 升级至 v2.6.2
- 依赖升级：将 docker engine 和 cli 升级至 v28.1.0
- 依赖升级：将 containerd 升级至 2.0.5
- 依赖升级：将 buildkit 升级至 v0.21.1

## 2.35.1

<em class="text-gray-400 italic dark:text-gray-500">2025-04-17</em>


### 错误修复与增强

- 修复了绑定挂载的问题

### 更新

- 依赖升级：将 compose-go 升级至 v2.6.0
- 依赖升级：将 docker engine 和 cli 升级至 v28.0.4
- 依赖升级：将 buildx 升级至 v0.22.0

## 2.35.0

<em class="text-gray-400 italic dark:text-gray-500">2025-04-10</em>


### 错误修复与增强

- 添加了对 [Docker Model Runner](/manuals/ai/model-runner.md) 的支持，可轻松将 AI 模型集成到 Compose 应用中
- 添加了 `build --print` 命令，通过显示等效的 bake 文件来帮助调试复杂构建配置
- 添加了 `volume.type=image` 以提供对容器镜像更灵活的卷管理
- 为 `run` 命令添加了 `--quiet` 选项，以便在运行容器时获得更简洁的输出
- 添加了 `config --no-env-resolution` 选项以查看未经环境变量替换的原始配置
- 修复了 `depends_on` 的行为，防止在依赖项变更时不必要的容器重建
- 修复了使用 `include` 时由环境变量定义的 secrets 支持
- 修复了卷挂载处理，确保绑定挂载在所有场景下正常工作

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.1.0
- 依赖升级：将 buildx 升级至 v0.23.0
- 依赖升级：将 buildkit 升级至 v0.21.0

## 2.34.0

<em class="text-gray-400 italic dark:text-gray-500">2025-03-14</em>


### 错误修复与增强

- 添加了对刷新 `pull_policy` 值 `daily`、`weekly` 和 `every_<duration>` 的支持
- 在 `watch` 定义中引入了 `include` 属性以匹配文件模式
- 为 `docker compose run` 命令引入了 `--env-from-file` 标志
- 将 `publish` 提升为 Compose 的常规命令
- 修复了通过在选择服务后加载 `env_file` 导致的错误

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.0.1
- 依赖升级：将 buildkit 升级至 v0.17.1
- 依赖升级：将 compose-go 升级至 v2.4.9
- 依赖升级：将 buildx 升级至 v0.21.2

## 2.33.1

<em class="text-gray-400 italic dark:text-gray-500">2025-02-21</em>


### 错误修复与增强

- 添加了对 `gw_priority`、`enable_ipv4` 的支持（需要 Docker v28.0）
- 修复了导航菜单的问题
- 改进了在使用只读服务的非文件 secret/config 时的错误消息

### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v28.0.0

## 2.33.0

<em class="text-gray-400 italic dark:text-gray-500">2025-02-13</em>


### 错误修复与增强

- 引入了提示以促进使用 [Bake](/build/bake/)
- 引入了对引用其他服务的 `additional_context` 属性的支持
- 添加了对 `BUILDKIT_PROGRESS` 的支持
- 当发布的 Compose 应用包含环境变量时，Compose 现在会发出警告
- 添加了 `--with-env` 标志以发布包含环境变量的 Compose 应用
- 更新了 `ls --quiet` 的帮助描述
- 修复了多个委托构建给 Bake 的问题
- 更新了 `stats` 命令的帮助信息
- 修复了对 "builtin" seccomp 配置的支持
- 修复了对多服务 `watch` 的支持
- 移除了旧指标系统使用的按错误类型的退出代码
- 修复了 `compatibility` 的测试覆盖率
- 移除了发送给 OpenTelemetry 的原始 os.Args
- 启用了 copyloopvar 检查器
- 修复了二进制文件的 provenance 并生成 SBOM
- 现在使用 docs upstream 验证的主分支
- 添加了 codeowners 文件
- 在测试矩阵中添加了 Docker Engine v28.x

### 更新

- 依赖升级：将 compose-go 升级至 v2.4.8
- 依赖升级：将 buildx 升级至 v0.20.1
- 依赖升级：将 docker 升级至 v27.5.1
- 依赖升级：将 golangci-lint 升级至 v1.63.4
- 依赖升级：将 golang.org/x/sys 从 0.28.0 升级至 0.30.0
- 依赖升级：将 github.com/moby/term 升级至 v0.5.2
- 依赖升级：将 github.com/otiai10/copy 从 1.14.0 升级至 1.14.1
- 依赖升级：将 github.com/jonboulle/clockwork 从 0.4.0 升级至 0.5.0
- 依赖升级：将 github.com/spf13/pflag 从 1.0.5 升级至 1.0.6
- 依赖升级：将 golang.org/x/sync 从 0.10.0 升级至 0.11.0
- 依赖升级：将 gotest.tools/v3 从 3.5.1 升级至 3.5.2

## 2.32.4

<em class="text-gray-400 italic dark:text-gray-500">2025-01-16</em>


### 错误修复与增强

- 修复了使用 `docker compose version` 时 Compose 版本无法正确显示的问题

## 2.32.3

<em class="text-gray-400 italic dark:text-gray-500">2025-01-13</em>


> [!NOTE]
>
> 来自 Compose GitHub 仓库的二进制文件可能无法正确显示版本号。如果在开发或 CI 流程中依赖 `docker compose version`，请升级至 Compose 版本 2.32.4。

### 错误修复与增强

- 修复了 Compose 会用主网络 MAC 地址覆盖服务级 MAC 地址的问题
- 修复了并发构建期间的日志渲染问题

## 2.32.2

<em class="text-gray-400 italic dark:text-gray-500">2025-01-07</em>


### 更新

- 依赖升级：将 compose-go 升级至 v2.4.7
- 依赖升级：将 golang 升级至 v1.22.10

### 错误修复与增强

- 为 `docker compose run` 命令添加了 `--pull` 标志
- 修复了 `watch` 模式的 `restart` 操作不监视绑定挂载的问题
- 修复了使用匿名卷时重新创建容器的问题

## 2.32.1

<em class="text-gray-400 italic dark:text-gray-500">2024-12-16</em>


### 错误修复与增强

- 修复了不必要时重新创建容器的问题

## 2.32.0

<em class="text-gray-400 italic dark:text-gray-500">2024-12-13</em>


### 更新

- 依赖升级：将 docker + buildx 升级至最新版本
- 依赖升级：将 otel 依赖升级至 v1.28.0 和 v0.53.0
- 依赖升级：将 golang.org/x/sys 升级至 0.28.0
- 依赖升级：将 golang.org/x/crypto 升级至 0.31.0
- 依赖升级：将 google.golang.org/grpc 升级至 1.68.1
- 依赖升级：将 golang.org/x/sync 升级至 0.10.0
- 依赖升级：将 xx 升级至 v1.6.1

### 错误修复与增强

- 改进了对使用 [Bake](/manuals/build/bake.md) 构建的支持
- 添加了 `restart` 和 `sync+exec` 监视操作
- 当卷或网络配置变更时，Compose 现在会重新创建容器
- 修复了对 `mac_address` 的支持
- 修复了 `pull --quiet` 仅隐藏进度而非全局状态的问题
- 修复了只有 `rebuild` 监视操作需要构建声明的问题
- 当通过 Compose 菜单启用时，Compose 现在会记录 `watch` 配置错误

## 2.31.0

<em class="text-gray-400 italic dark:text-gray-500">2024-11-28</em>


### 更新

- 依赖升级：将 compose-go 升级至 v2.4.5
- 依赖升级：将 docker engine 和 cli 升级至 v27.4.0-rc.2
- 依赖升级：将 buildx 升级至 v0.18.0
- 依赖升级：将 buildkit 升级至 v0.17.1

### 错误修复与增强

- 添加了使用 Docker Buildx Bake 构建 Docker Compose 服务的功能
- 添加了 `commit` 命令以从运行中的容器创建新镜像
- 修复了网络变更未被检测到的问题
- 修复了容器顺序停止导致重启过程变慢的问题

## 2.30.3

<em class="text-gray-400 italic dark:text-gray-500">2024-11-07</em>


### 更新

- 依赖升级：将 compose-go 升级至 v2.4.4

### 错误修复与增强

- 修复了使用 `--watch` 时不应该重启的服务被重启的问题
- 改进了 Compose 文件中使用相同 YAML 锚点多次的修复

## 2.30.2

<em class="text-gray-400 italic dark:text-gray-500">2024-11-05</em>


### 更新

- 依赖升级：将 compose-go 升级至 v2.4.3

### 错误修复与增强

- 修复了更新服务 profiles 时重新创建服务的问题
- 修复了 Compose 文件中使用相同 YAML 锚点多次的回归问题

## 2.30.1

<em class="text-gray-400 italic dark:text-gray-500">2024-10-30</em>


### 更新

- 依赖升级：将 compose-go 升级至 v2.4.2

### 错误修复与增强

- 修复了使用 stdin 作为 `-f` 标志输入时的回归问题
- 修复了 Compose 文件中使用相同 YAML 锚点多次的回归问题

## 2.30.0

<em class="text-gray-400 italic dark:text-gray-500">2024-10-29</em>


### 更新

- 依赖升级：将 compose-go 升级至 v2.4.1
- 依赖升级：将 docker engine 和 cli 升级至 v27.3.1

### 错误修复与增强

- 引入了服务钩子支持
- 添加了 alpha 版本的 `generate` 命令
- 添加了 `export` 命令
- 添加了对 Compose 文件中使用 `devices` 的 CDI 设备请求的支持
- 大量错误修复

## 2.29.7

<em class="text-gray-400 italic dark:text-gray-500">2024-09-20</em>


### 错误修复与增强

- 修复了使用绑定挂载的 mount API 时的回归问题

## 2.29.6

<em class="text-gray-400 italic dark:text-gray-500">2024-09-19</em>


### 更新

- 依赖升级：将 docker engine 和 cli 升级至 v27.3.0-rc.2

### 错误修复与增强

- 修复了 Windows 容器绑定挂载的问题

## 2.29.5

<em class="text-gray-400 italic dark:text-gray-500">2024-09-17</em>


### 错误修复与增强

- 修复了 WSL2 上的绑定挂载问题

## 2.29.4

<em class="text-gray-400 italic dark:text-gray-500">2024-09-16</em>


### 更新

- 依赖升级：将 buildx 升级至 v0.17.1
- 依赖升级：将 docker engine 和 cli 升级至 v27.3.0-rc.1

### 错误修复与增强

- 修复了重启分叉依赖项时服务未停止的问题
- 修复了 OTEL 客户端潜在的 `nil` 指针错误

## 2.29.3

<em class="text-gray-400 italic dark:text-gray-500">2024-09-12</em>


### 更新

- 依赖升级：将 compose-go 升级至 v2.2.0
- 依赖升级：将 docker engine 和 cli 升级至 v27.2.1

### 错误修复与增强

- 现在允许 `watch` 结合绑定挂载和 `rebuild`
- 修复了使用 `--no-deps` 和 `up` 时重新创建容器的问题
- 修复了重新附加容器时未关闭流的问题
- 恢复了在
