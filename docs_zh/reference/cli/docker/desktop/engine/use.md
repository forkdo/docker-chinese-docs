---
datafolder: desktop-cli
datafile: docker_desktop_engine_use
title: docker desktop engine use
layout: cli
---

# docker desktop engine use

在 Docker Desktop 中使用指定的 Docker 引擎

## 摘要

```
docker desktop engine use [ENGINE_NAME] [flags]
```

## 选项

```
  -h, --help   显示 use 命令的帮助信息
```

## 详细说明

`docker desktop engine use` 命令允许您在 Docker Desktop 中切换到指定的 Docker 引擎。Docker Desktop 将更新 Docker CLI 配置，使其连接到所选的 Docker 引擎。

## 示例

### 使用 Docker 引擎

```
$ docker desktop engine use my-engine
```

### 使用 Docker 引擎并指定 Docker 上下文

```
$ docker desktop engine use my-engine --context my-context
```

## 相关命令

- [docker desktop engine ls](docker_desktop_engine_ls.md) - 列出 Docker Desktop 中可用的 Docker 引擎
- [docker desktop engine inspect](docker_desktop_engine_inspect.md) - 显示 Docker 引擎的详细信息
- [docker context use](docker_context_use.md) - 切换到指定的 Docker 上下文