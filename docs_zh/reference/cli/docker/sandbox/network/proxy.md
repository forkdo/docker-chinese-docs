---
datafolder: sandbox-cli
datafile: docker_sandbox_network_proxy
title: docker sandbox network proxy
layout: cli
---

# docker sandbox network proxy

## 概述

`docker sandbox network proxy` 命令用于管理 Docker 沙箱环境中的网络代理配置。

## 语法

```bash
docker sandbox network proxy [OPTIONS] COMMAND [ARG...]
```

## 选项

| 选项 | 描述 |
|------|------|
| `--help` | 显示帮助信息 |

## 子命令

### `create`

创建一个新的沙箱网络代理。

```bash
docker sandbox network proxy create [OPTIONS] NAME
```

#### 选项

| 选项 | 描述 |
|------|------|
| `--driver DRIVER` | 指定代理驱动类型 |
| `--config CONFIG` | 代理配置文件路径 |

### `inspect`

查看沙箱网络代理的详细信息。

```bash
docker sandbox network proxy inspect [OPTIONS] PROXY
```

#### 选项

| 选项 | 描述 |
|------|------|
| `--format FORMAT` | 输出格式（json、table 等） |

### `ls`

列出所有沙箱网络代理。

```bash
docker sandbox network proxy ls [OPTIONS]
```

#### 选项

| 选项 | 描述 |
|------|------|
| `--quiet` | 仅显示代理名称 |

### `rm`

删除一个或多个沙箱网络代理。

```bash
docker sandbox network proxy rm PROXY [PROXY...]
```

## 示例

1. 创建一个名为 `my-proxy` 的沙箱网络代理：

```bash
docker sandbox network proxy create --driver http --config /path/to/config.json my-proxy
```

2. 查看所有沙箱网络代理：

```bash
docker sandbox network proxy ls
```

3. 查看特定代理的详细信息：

```bash
docker sandbox network proxy inspect my-proxy
```

4. 删除沙箱网络代理：

```bash
docker sandbox network proxy rm my-proxy
```