---
datafolder: sandbox-cli
datafile: docker_sandbox_ls
title: docker sandbox ls
layout: cli
---

# docker sandbox ls

## 用法

```bash
docker sandbox ls [OPTIONS]
```

## 描述

列出所有沙箱。

## 选项

| 选项 | 描述 |
| --- | --- |
| `--filter , -f` | 根据条件过滤输出 |
| `--format` | 使用 Go 模板格式化输出 |
| `--quiet , -q` | 仅显示沙箱 ID |

## 父命令

| 命令 | 描述 |
| --- | --- |
| [docker sandbox](docker_sandbox.md) | 管理沙箱 |