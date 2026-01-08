---
datafolder: sandbox-cli
datafile: docker_sandbox_inspect
title: docker sandbox inspect
layout: cli
---

# docker sandbox inspect

## 描述

显示一个或多个沙盒的详细信息

## 使用方法

```shell
docker sandbox inspect [OPTIONS] SANDBOX [SANDBOX...]
```

## 选项

| 名称 | 简写 | 类型 | 默认值 | 描述 |
|------|------|------|--------|------|
| `--format` | `-f` | `string` | | 使用自定义格式打印输出 |
| `--no-trunc` | | `bool` | `false` | 不截断输出 |
| `--size` | | `bool` | `false` | 显示总大小（包括沙盒使用的磁盘空间） |

## 示例

### 查看沙盒的详细信息

```shell
docker sandbox inspect my-sandbox
```

### 使用自定义格式查看沙盒的详细信息

```shell
docker sandbox inspect --format '{{.ID}}' my-sandbox
```

### 查看多个沙盒的详细信息

```shell
docker sandbox inspect my-sandbox-1 my-sandbox-2
```