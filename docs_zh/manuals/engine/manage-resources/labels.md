---
description: 了解标签，一种用于管理 Docker 对象元数据的工具。
keywords: 标签, 元数据, docker, 注释
title: Docker 对象标签
aliases:
  - /engine/userguide/labels-custom-metadata/
  - /config/labels-custom-metadata/
---

标签是一种为 Docker 对象添加元数据的机制，包括：

- 镜像
- 容器
- 本地守护进程
- 卷
- 网络
- Swarm 节点
- Swarm 服务

您可以使用标签来组织镜像、记录许可证信息、注释容器、卷和网络之间的关系，或以任何对您的业务或应用程序有意义的方式使用。

## 标签键和值

标签是一个键值对，以字符串形式存储。您可以为一个对象指定多个标签，但每个键在对象内必须是唯一的。如果同一个键被赋予多个值，最近写入的值会覆盖所有先前的值。

### 键格式建议

标签键是键值对的左侧部分。键是字母数字字符串，可以包含句点（`.`）、下划线（`_`）、斜杠（`/`）和连字符（`-`）。大多数 Docker 用户使用由其他组织创建的镜像，以下指导原则有助于防止对象间标签的意外重复，特别是如果您计划将标签用作自动化机制时。

- 第三方工具的作者应在每个标签键前加上他们拥有的域名的反向 DNS 表示法，例如 `com.example.some-label`。

- 未经域名所有者许可，不要在标签键中使用该域名。

- `com.docker.*`、`io.docker.*` 和 `org.dockerproject.*` 命名空间由 Docker 保留供内部使用。

- 标签键应以小写字母开头和结尾，且应仅包含小写字母数字字符、句点字符（`.`）和连字符（`-`）。不允许连续的句点或连字符。

- 句点字符（`.`）用于分隔命名空间“字段”。不带命名空间的标签键保留供 CLI 使用，允许 CLI 用户使用较短的、便于输入的字符串交互式地标记 Docker 对象。

这些指导原则目前未被强制执行，特定用例可能需要额外的指导原则。

### 值指导原则

标签值可以包含任何可以表示为字符串的数据类型，包括（但不限于）JSON、XML、CSV 或 YAML。唯一的要求是使用特定于结构类型的机制将值序列化为字符串。例如，要将 JSON 序列化为字符串，您可以使用 `JSON.stringify()` JavaScript 方法。

由于 Docker 不会反序列化值，因此除非您在第三方工具中构建此功能，否则在按标签值查询或过滤时，不能将 JSON 或 XML 文档视为嵌套结构。

## 管理对象上的标签

每种支持标签的对象类型都有添加和管理标签的机制，以及如何使用这些标签的相关说明。这些链接提供了学习如何在 Docker 部署中使用标签的良好起点。

镜像、容器、本地守护进程、卷和网络上的标签在其对象生命周期内是静态的。要更改这些标签，您必须重新创建对象。Swarm 节点和服务上的标签可以动态更新。

- 镜像和容器

  - [为镜像添加标签](/reference/dockerfile.md#label)
  - [在运行时覆盖容器的标签](/reference/cli/docker/container/run.md#label)
  - [检查镜像或容器的标签](/reference/cli/docker/inspect.md)
  - [按标签过滤镜像](/reference/cli/docker/image/ls.md#filter)
  - [按标签过滤容器](/reference/cli/docker/container/ls.md#filter)

- 本地 Docker 守护进程

  - [在运行时为 Docker 守护进程添加标签](/reference/cli/dockerd.md)
  - [检查 Docker 守护进程的标签](/reference/cli/docker/system/info.md)

- 卷

  - [为卷添加标签](/reference/cli/docker/volume/create.md)
  - [检查卷的标签](/reference/cli/docker/volume/inspect.md)
  - [按标签过滤卷](/reference/cli/docker/volume/ls.md#filter)

- 网络

  - [为网络添加标签](/reference/cli/docker/network/create.md)
  - [检查网络的标签](/reference/cli/docker/network/inspect.md)
  - [按标签过滤网络](/reference/cli/docker/network/ls.md#filter)

- Swarm 节点

  - [添加或更新 Swarm 节点的标签](/reference/cli/docker/node/update.md#label-add)
  - [检查 Swarm 节点的标签](/reference/cli/docker/node/inspect.md)
  - [按标签过滤 Swarm 节点](/reference/cli/docker/node/ls.md#filter)

- Swarm 服务
  - [创建 Swarm 服务时添加标签](/reference/cli/docker/service/create.md#label)
  - [更新 Swarm 服务的标签](/reference/cli/docker/service/update.md)
  - [检查 Swarm 服务的标签](/reference/cli/docker/service/inspect.md)
  - [按标签过滤 Swarm 服务](/reference/cli/docker/service/ls.md#filter)