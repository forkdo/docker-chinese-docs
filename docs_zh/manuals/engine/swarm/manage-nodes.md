---
description: 管理 Swarm 中的现有节点
keywords: 指南, swarm 模式, 节点
title: 管理 Swarm 中的节点
---

作为 Swarm 管理生命周期的一部分，您可能需要：

* [列出 Swarm 中的节点](#list-nodes)
* [检查单个节点](#inspect-an-individual-node)
* [更新节点](#update-a-node)
* [离开 Swarm](#leave-the-swarm)

## 列出节点

要查看 Swarm 中节点的列表，在管理节点上运行 `docker node ls`：

```console
$ docker node ls

ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
46aqrk4e473hjbt745z53cr3t    node-5    Ready   Active        Reachable
61pi3d91s0w3b90ijw3deeb2q    node-4    Ready   Active        Reachable
a5b2m3oghd48m8eu391pefq5u    node-3    Ready   Active
e7p8btxeu3ioshyuj6lxiv6g0    node-2    Ready   Active
ehkv3bcimagdese79dn78otj5 *  node-1    Ready   Active        Leader
```

`AVAILABILITY` 列显示调度器是否可以向节点分配任务：

* `Active` 表示调度器可以向节点分配任务。
* `Pause` 表示调度器不会向节点分配新任务，但现有任务继续运行。
* `Drain` 表示调度器不会向节点分配新任务。调度器会关闭所有现有任务并在可用节点上重新调度它们。

`MANAGER STATUS` 列显示节点在 Raft 共识中的参与情况：

* 无值表示这是一个不参与 Swarm 管理的工作节点。
* `Leader` 表示该节点是主要管理节点，负责 Swarm 的所有管理和编排决策。
* `Reachable` 表示该节点是参与 Raft 共识法定人数的管理节点。如果 Leader 节点不可用，该节点有资格被选举为新 Leader。
* `Unavailable` 表示该节点是无法与其他管理节点通信的管理节点。如果管理节点变为不可用，您应该加入新的管理节点到 Swarm，或者提升工作节点为管理节点。

有关 Swarm 管理的更多信息，请参考 [Swarm 管理指南](admin_guide.md)。

## 检查单个节点

您可以在管理节点上运行 `docker node inspect <NODE-ID>` 来查看单个节点的详细信息。输出默认为 JSON 格式，但您可以使用 `--pretty` 标志以人类可读格式打印结果。例如：

```console
$ docker node inspect self --pretty

ID:                     ehkv3bcimagdese79dn78otj5
Hostname:               node-1
Joined at:              2016-06-16 22:52:44.9910662 +0000 utc
Status:
 State:                 Ready
 Availability:          Active
Manager Status:
 Address:               172.17.0.2:2377
 Raft Status:           Reachable
 Leader:                Yes
Platform:
 Operating System:      linux
 Architecture:          x86_64
Resources:
 CPUs:                  2
 Memory:                1.954 GiB
Plugins:
  Network:              overlay, host, bridge, overlay, null
  Volume:               local
Engine Version:         1.12.0-dev
```

## 更新节点

您可以修改节点属性来：

* [更改节点可用性](#change-node-availability)
* [添加或删除标签元数据](#add-or-remove-label-metadata)
* [更改节点角色](#promote-or-demote-a-node)

### 更改节点可用性

更改节点可用性可以让您：

* 清空管理节点，使其仅执行 Swarm 管理任务，不接受任务分配。
* 清空节点以便进行维护。
* 暂停节点使其无法接收新任务。
* 恢复不可用或暂停节点的可用性状态。

例如，将管理节点更改为 `Drain` 可用性：

```console
$ docker node update --availability drain node-1

node-1
```

有关不同可用性选项的描述，请参见 [列出节点](#list-nodes)。

### 添加或删除标签元数据

节点标签提供了一种灵活的节点组织方法。您也可以在服务约束中使用节点标签。创建服务时应用约束以限制调度器为服务分配任务的节点。

在管理节点上运行 `docker node update --label-add` 向节点添加标签元数据。`--label-add` 标志支持 `<key>` 或 `<key>=<value>` 对。

为每个要添加的节点标签使用一次 `--label-add` 标志：

```console
$ docker node update --label-add foo --label-add bar=baz node-1

node-1
```

使用 `docker node update` 为节点设置的标签仅适用于 Swarm 内的节点实体。不要将它们与 Docker 守护进程的 [dockerd](/manuals/engine/manage-resources/labels.md) 标签混淆。

因此，节点标签可用于限制只有满足特定要求的节点才能调度关键任务。例如，仅在满足特定工作负载要求（如符合 [PCI-SS 合规性](https://www.pcisecuritystandards.org/)）的机器上调度。

受损的工作节点无法更改节点标签，因此无法危及这些特殊工作负载。

然而，引擎标签仍然有用，因为某些不影响容器安全编排的功能可能更适合以分散方式设置。例如，引擎可能有一个标签表示它具有某种类型的磁盘设备，这可能与安全性没有直接关系。这些标签更容易被 Swarm 编排器"信任"。

有关服务约束的更多信息，请参考 `docker service create` [CLI 参考](/reference/cli/docker/service/create.md)。

### 提升或降级节点

您可以将工作节点提升为管理角色。这在管理节点变得不可用或您想将管理节点离线进行维护时很有用。同样，您也可以将管理节点降级为工作角色。

> [!NOTE]
>
> 无论您提升或降级节点的原因是什么，您必须始终保持 Swarm 中管理节点的法定人数。更多信息请参考 [Swarm 管理指南](admin_guide.md)。

要在管理节点上提升节点或节点集，请运行 `docker node promote`：

```console
$ docker node promote node-3 node-2

Node node-3 promoted to a manager in the swarm.
Node node-2 promoted to a manager in the swarm.
```

要在管理节点上降级节点或节点集，请运行 `docker node demote`：

```console
$ docker node demote node-3 node-2

Manager node-3 demoted in the swarm.
Manager node-2 demoted in the swarm.
```

`docker node promote` 和 `docker node demote` 分别是 `docker node update --role manager` 和 `docker node update --role worker` 的便捷命令。

## 在 Swarm 节点上安装插件

如果您的 Swarm 服务依赖一个或多个 [插件](/engine/extend/plugin_api/)，这些插件需要在服务可能部署的每个节点上都可用。您可以手动在每个节点上安装插件，或者编写脚本进行安装。您也可以使用 Docker API 以类似全局服务的方式部署插件，通过指定 `PluginSpec` 而不是 `ContainerSpec`。

> [!NOTE]
>
> 目前无法使用 Docker CLI 或 Docker Compose 将插件部署到 Swarm。此外，也无法从私有仓库安装插件。

`PluginSpec` 由插件开发者定义。要将插件添加到所有 Docker 节点，请使用 [`service/create`](/reference/api/engine/v1.31/#operation/ServiceCreate) API，传递在 `TaskTemplate` 中定义的 `PluginSpec` JSON。

## 离开 Swarm

在节点上运行 `docker swarm leave` 命令以将其从 Swarm 中移除。

例如，在工作节点上离开 Swarm：

```console
$ docker swarm leave

Node left the swarm.
```

当节点离开 Swarm 时，Docker Engine 停止以 Swarm 模式运行。编排器不再向该节点调度任务。

如果节点是管理节点，您会收到有关维护法定人数的警告。要忽略警告，请使用 `--force` 标志。如果最后一个管理节点离开 Swarm，Swarm 将变得不可用，需要您采取灾难恢复措施。

有关维护法定人数和灾难恢复的信息，请参考 [Swarm 管理指南](admin_guide.md)。

节点离开 Swarm 后，您可以在管理节点上运行 `docker node rm` 从节点列表中移除该节点。

例如：

```console
$ docker node rm node-2
```

## 了解更多

* [Swarm 管理指南](admin_guide.md)
* [Docker Engine 命令行参考](/reference/cli/docker/)
* [Swarm 模式教程](swarm-tutorial/_index.md)