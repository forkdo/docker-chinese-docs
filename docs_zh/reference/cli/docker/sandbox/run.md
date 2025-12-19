```markdown
---
datafolder: sandbox-cli
datafile: docker_sandbox_run
title: docker sandbox run
layout: cli
---
# docker sandbox run

## 说明

在 Docker 容器中启动一个临时的 sandbox 环境。

该命令会创建一个新的 Docker 容器，其中包含预配置的开发工具和依赖项，非常适合用于安全的代码测试、实验或调试。

## 使用示例

```bash
# 使用默认配置启动 sandbox
docker sandbox run

# 指定自定义镜像启动 sandbox
docker sandbox run --image my-custom-sandbox:latest

# 启动 sandbox 并挂载当前目录
docker sandbox run --volume "$(pwd):/workspace"

# 启动 sandbox 并设置环境变量
docker sandbox run --env "API_KEY=secret" --env "DEBUG=true"

# 指定容器名称
docker sandbox run --name my-dev-env

# 启动 sandbox 并自动移除容器（一次性使用）
docker sandbox run --rm

# 使用特定资源限制启动 sandbox
docker sandbox run --cpus 2 --memory 2g

# 启动 sandbox 并暴露端口
docker sandbox run --publish 8080:8080

# 使用自定义工作目录启动 sandbox
docker sandbox run --workdir /app
```

## 参数

| 参数 | 长格式 | 类型 | 必需 | 默认值 | 描述 |
|------|--------|------|------|--------|------|
| `--image` | `--image` | string | 否 | `sandbox-base:latest` | 要使用的 Docker 镜像 |
| `--volume` | `--volume` | stringArray | 否 | - | 挂载卷，格式：`host_path:container_path` |
| `--env` | `--env` | stringArray | 否 | - | 设置环境变量，格式：`KEY=VALUE` |
| `--name` | `--name` | string | 否 | 自动生成 | 容器名称 |
| `--rm` | `--rm` | boolean | 否 | `false` | 运行后自动移除容器 |
| `--cpus` | `--cpus` | float | 否 | `1.0` | 分配给容器的 CPU 核心数 |
| `--memory` | `--memory` | string | 否 | `512m` | 分配给容器的内存，支持单位：b, k, m, g |
| `--publish` | `--publish` | stringArray | 否 | - | 端口映射，格式：`host_port:container_port` |
| `--workdir` | `--workdir` | string | 否 | `/workspace` | 容器内的工作目录 |
| `--detach` | `--detach` | boolean | 否 | `false` | 后台运行容器 |
| `--help` | `--help` | boolean | 否 | `false` | 显示帮助信息 |

## 环境变量

| 变量 | 默认值 | 描述 |
|------|--------|------|
| `SANDBOX_TIMEOUT` | `3600` | sandbox 自动关闭的超时时间（秒） |
| `SANDBOX_WORKSPACE` | `/workspace` | 默认工作目录 |
| `SANDBOX_TOOLS` | `git,vim,nano` | 预装工具列表 |

## 返回值

| 代码 | 描述 |
|------|------|
| `0` | 成功启动 sandbox |
| `1` | 参数错误或配置无效 |
| `2` | Docker 守护进程连接失败 |
| `3` | 镜像拉取失败 |
| `4` | 容器启动失败 |

## 另请参阅

*   [sandbox stop](sandbox_stop) - 停止运行中的 sandbox
*   [sandbox list](sandbox_list) - 列出所有 sandbox
*   [sandbox rm](sandbox_rm) - 移除 sandbox
*   [sandbox logs](sandbox_logs) - 查看 sandbox 日志

## 示例输出

### 成功启动

```bash
$ docker sandbox run --name my-test --rm
Creating sandbox container 'my-test'...
✓ Image pulled: sandbox-base:latest
✓ Container created: my-test
✓ Environment configured
✓ Workspace mounted: /workspace

Sandbox is ready! Access it with:
  docker exec -it my-test bash

To stop: docker sandbox stop my-test
To view logs: docker sandbox logs my-test
```

### 后台运行

```bash
$ docker sandbox run --name my-bg-sandbox --detach
Sandbox 'my-bg-sandbox' started in background
Container ID: a1b2c3d4e5f6
```

### 错误示例

```bash
$ docker sandbox run --cpus 0.5
Error: Invalid CPU allocation. Minimum required: 1.0 core
```

## 注意事项

1.  **Docker 要求**：需要安装并运行 Docker 守护进程
2.  **权限**：可能需要 `sudo` 或适当的用户权限
3.  **网络**：默认使用 bridge 网络模式
4.  **持久化**：使用 `--volume` 挂载卷以保存工作成果
5.  **资源限制**：合理设置 CPU 和内存限制以避免影响宿主机性能
6.  **安全性**：sandbox 容器默认具有受限权限，但仍需谨慎处理敏感数据

## 常见问题

**Q: 如何保存 sandbox 中的工作？**
A: 使用 `--volume` 参数挂载本地目录，或在退出前将文件复制到挂载的卷中。

**Q: sandbox 启动失败怎么办？**
A: 检查 Docker 是否运行，使用 `docker sandbox logs` 查看详细日志。

**Q: 可以同时运行多个 sandbox 吗？**
A: 可以，只需为每个 sandbox 指定不同的名称即可。

**Q: 如何访问运行中的 sandbox？**
A: 使用 `docker exec -it <container_name> bash` 进入容器，或使用 `docker sandbox logs` 查看日志。
```