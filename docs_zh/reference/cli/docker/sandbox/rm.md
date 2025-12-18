---
datafolder: sandbox-cli
datafile: docker_sandbox_rm
title: docker sandbox rm
layout: cli
---

# docker sandbox rm

从 Docker Desktop 中删除沙箱

## 用法

```
docker sandbox rm [OPTIONS] SANDBOX_NAME
```

## 描述

从 Docker Desktop 中删除沙箱。

## 选项

| 选项 | 描述 |
| --- | --- |
| `-f, --force` | 强制删除沙箱，即使它正在运行 |

## 示例

### 删除沙箱

```
$ docker sandbox rm my-sandbox
```

### 强制删除正在运行的沙箱

```
$ docker sandbox rm --force my-sandbox
```

## 另请参阅

- [`docker sandbox create`](docker_sandbox_create.html)
- [`docker sandbox ls`](docker_sandbox_ls.html)
- [`docker sandbox start`](docker_sandbox_start.html)
- [`docker sandbox stop`](docker_sandbox_stop.html)