---
datafolder: sandbox-cli
datafile: docker_sandbox_run
title: docker sandbox run
layout: cli
---

# docker sandbox run

在沙箱容器中运行指定的 Docker Compose 文件

## 用法

```
docker sandbox run [OPTIONS] [COMPOSE_FILE] [flags]
```

## 描述

在沙箱容器中运行指定的 Docker Compose 文件。如果未指定 Compose 文件，将使用当前目录中的 `docker-compose.yaml` 或 `docker-compose.yml`。

## 示例

在沙箱容器中运行 Docker Compose 文件：

```
docker sandbox run
```

在沙箱容器中运行指定的 Docker Compose 文件：

```
docker sandbox run docker-compose.yaml
```

## 选项

### --detach, -d

在后台运行服务容器

### --env-file

指定包含环境变量的文件

### --file, -f

指定一个备用 compose 文件（默认值：docker-compose.yaml）

### --help, -h

显示帮助信息

### --no-build

不自动构建镜像，即使它们缺失

### --no-deps

不启动链接的服务

### --no-recreate

如果容器已存在，则不重新创建

### --no-start

不自动启动容器

### --profile

为匹配的服务启用配置文件

### --quiet, -q

仅显示容器 ID

### --remove-orphans

删除未在 compose 文件中定义的服务

### --scale

为服务设置服务规模（重复以指定多个服务）

### --timeout, -t

停止容器前等待的秒数（默认值为 10）

### --wait

等待容器进入"运行中"状态，然后退出

### --wait-timeout

等待容器启动的秒数（默认值为 600）