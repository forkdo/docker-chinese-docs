---
datafolder: sandbox-cli
datafile: docker_sandbox
title: docker sandbox
layout: cli
---

# docker sandbox

Docker 沙箱命令

## 用法

```
docker sandbox [COMMAND]
```

## 全局选项

| 选项 | 默认值 | 描述 |
|------|--------|------|
| `--config` | `~/.docker` | 客户端配置文件所在目录（默认值为 "~/.docker"） |
| `-c`, `--context` |  | 要使用的上下文 |
| `-D`, `--debug` |  | 启用调试模式 |
| `-H`, `--host` |  | Docker 服务器套接字的地址 |
| `--insecure-registry` |  | 将注册表标记为不安全的注册表 |
| `--log-level` |  | 日志级别 ("debug"|"info"|"warn"|"error"|"fatal")（默认值为 "info"） |
| `--tls` |  | 使用 TLS；由客户端自动启用 |
| `--tlscacert` | `~/.docker/ca.pem` | 信任的 CA 证书的路径 |
| `--tlscert` | `~/.docker/cert.pem` | TLS 证书文件的路径 |
| `--tlskey` | `~/.docker/key.pem` | TLS 密钥文件的路径 |
| `--tlsverify` |  | 使用 TLS 并验证远程 |
| `-v`, `--version` |  | 打印版本信息并退出 |

## 选项

| 选项 | 默认值 | 描述 |
|------|--------|------|
| `-h`, `--help` |  | 显示帮助信息 |

## 父命令

| 命令 | 描述 |
|------|------|
| [docker](../docker/) | Docker CLI 命令行接口 |

## 子命令

| 命令 | 描述 |
|------|------|
| [docker sandbox create](./create/) | 创建一个沙箱 |
| [docker sandbox delete](./delete/) | 删除一个沙箱 |
| [docker sandbox exec](./exec/) | 在沙箱中执行命令 |
| [docker sandbox inspect](./inspect/) | 显示一个或多个沙箱的详细信息 |
| [docker sandbox list](./list/) | 列出沙箱 |
| [docker sandbox pause](./pause/) | 暂停沙箱 |
| [docker sandbox resume](./resume/) | 恢复沙箱 |
| [docker sandbox run](./run/) | 运行一个沙箱 |
| [docker sandbox start](./start/) | 启动沙箱 |
| [docker sandbox stop](./stop/) | 停止沙箱 |
| [docker sandbox update](./update/) | 更新沙箱 |
| [docker sandbox wait](./wait/) | 等待沙箱 |
| [docker sandbox wait-for-ready](./wait-for-ready/) | 等待沙箱就绪 |