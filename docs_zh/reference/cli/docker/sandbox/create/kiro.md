---
datafolder: sandbox-cli
datafile: docker_sandbox_create_kiro
title: docker sandbox create kiro
layout: cli
---

```bash
docker sandbox create kiro
```

创建一个名为 `kiro` 的 Docker 沙箱环境。

## 用法

```bash
docker sandbox create kiro [OPTIONS]
```

## 选项

| 选项 | 说明 |
|------|------|
| `--help` | 显示帮助信息 |
| `--version` | 显示版本信息 |

## 示例

创建一个基本的 `kiro` 沙箱：

```bash
docker sandbox create kiro
```

## 相关命令

- [`docker sandbox list`](/docs/cli/docker_sandbox_list) - 列出所有沙箱
- [`docker sandbox start`](/docs/cli/docker_sandbox_start) - 启动沙箱
- [`docker sandbox stop`](/docs/cli/docker_sandbox_stop) - 停止沙箱
- [`docker sandbox delete`](/docs/cli/docker_sandbox_delete) - 删除沙箱