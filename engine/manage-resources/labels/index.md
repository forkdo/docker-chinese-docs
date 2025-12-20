# Docker 对象标签

标签（Labels）是一种向 Docker 对象应用元数据的机制，这些对象包括：

- 镜像（Images）
- 容器（Containers）
- 本地守护进程（Local daemons）
- 卷（Volumes）
- 网络（Networks）
- Swarm 节点（Swarm nodes）
- Swarm 服务（Swarm services）

您可以使用标签来组织镜像、记录许可信息、注释容器、卷和网络之间的关系，或者以任何对您的业务或应用程序有意义的方式进行使用。

## 标签键和值

标签是一个键值对，存储为字符串。您可以为一个对象指定多个标签，但每个键在对象内必须是唯一的。如果同一个键被赋予了多个值，最近写入的值将覆盖所有先前的值。

### 键格式建议

标签键是键值对的左侧部分。键是字母数字字符串，可以包含句点（`.`）、下划线（`_`）、斜杠（`/`）和连字符（`-`）。大多数 Docker 用户使用其他组织创建的镜像，以下指南有助于防止跨对象无意中复制标签，特别是如果您计划将标签用作自动化机制。

- 第三方工具的作者应使用他们拥有的域名的反向 DNS 表示法作为每个标签键的前缀，例如 `com.example.some-label`。

- 未经域名所有者许可，不要在标签键中使用该域名。

- `com.docker.*`、`io.docker.*` 和 `org.dockerproject.*` 命名空间由 Docker 保留供内部使用。

- 标签键应以小写字母开头和结尾，并且只能包含小写字母数字字符、句点字符（`.`）和连字符（`-`）。不允许连续的句点或连字符。

- 句点字符（`.`）分隔命名空间“字段”。没有命名空间的标签键保留给 CLI 使用，允许 CLI 用户使用更短、更易于输入的字符串以交互方式标记 Docker 对象。

目前这些指南尚未强制执行，并且特定用例可能会适用额外的指南。

### 值指南

标签值可以包含任何可以表示为字符串的数据类型，包括（但不限于）JSON、XML、CSV 或 YAML。唯一的要求是值必须首先使用特定于结构类型的机制序列化为字符串。例如，要将 JSON 序列化为字符串，您可以使用 `JSON.stringify()` JavaScript 方法。

由于 Docker 不会反序列化值，因此在按标签值查询或过滤时，您不能将 JSON 或 XML 文档视为嵌套结构，除非您将此功能构建到第三方工具中。

## 管理对象上的标签

每种支持标签的对象类型都有添加和管理标签的机制，并根据该对象类型使用它们。这些链接是了解如何在 Docker 部署中使用标签的良好起点。

镜像、容器、本地守护进程、卷和网络上的标签在对象的生命周期内是静态的。要更改这些标签，必须重新创建对象。Swarm 节点和服务上的标签可以动态更新。

- 镜像和容器

  - [向镜像添加标签](/reference/dockerfile.md#label)
  - [在运行时覆盖容器的标签](/reference/cli/docker/container/run.md#label)
  - [检查镜像或容器上的标签](/reference/cli/docker/inspect.md)
  - [按标签过滤镜像](/reference/cli/docker/image/ls.md#filter)
  - [按标签过滤容器](/reference/cli/docker/container/ls.md#filter)

- 本地 Docker 守护进程

  - [在运行时向 Docker 守护进程添加标签](/reference/cli/dockerd.md)
  - [检查 Docker 守护进程的标签](/reference/cli/docker/system/info.md)

- 卷

  - [向卷添加标签](/reference/cli/docker/volume/create.md)
  - [检查卷的标签](/reference/cli/docker/volume/inspect.md)
  - [按标签过滤卷](/reference/cli/docker/volume/ls.md#filter)

- 网络

  - [向网络添加标签](/reference/cli/docker/network/create.md)
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
