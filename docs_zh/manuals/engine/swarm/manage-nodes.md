---
description: 管理 swarm 中的现有节点
keywords: guide, swarm mode, node
title: 管理 swarm 中的节点
---

作为 swarm 管理生命周期的一部分，您可能需要：

* [列出 swarm 中的节点](#list-nodes)
* [检查单个节点](#inspect-an-individual-node)
* [更新节点](#update-a-node)
* [离开 swarm](#leave-the-swarm)

## 列出节点

要从管理节点查看 swarm 中的节点列表，请运行 `docker node ls`：

```console
$ docker node ls

ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
46aqrk4e473hjbt745z53cr3t    node-5    Ready   Active        Reachable
61pi3d91s0w3b90ijw3deeb2q    node-4    Ready   Active        Reachable
a5b2m3oghd48m8eu391pefq5u    node-3    Ready   Active
e7p8btxeu3ioshyuj6lxiv6g0    node-2    Ready   Active
ehkv3bcimagdese79dn78otj5 *  node-1    Ready   Active        Leader
```

`AVAILABILITY` 列显示调度器是否可以向该节点分配任务：

* `Active` 表示调度器可以向该节点分配任务。
* `Pause` 表示调度器不会向该节点分配新任务，但现有任务将继续运行。
* `Drain` 表示调度器不会向该节点分配新任务。调度器将关闭所有现有任务，并将其调度到可用的节点上。

`MANAGER STATUS` 列显示节点在 Raft 共识中的参与情况：

* 无值表示该节点是 worker 节点，不参与 swarm 管理。
* `Leader` 表示该节点是主管理节点，负责为 swarm 做出所有管理和编排决策。
* `Reachable` 表示该节点是参与 Raft 共识仲裁的管理节点。如果主节点不可用，则该节点有资格被选为新主节点。
* `Unavailable` 表示该节点是管理节点，但无法与其他管理节点通信。如果管理节点变得不可用，您应该将新的管理节点加入 swarm，或将 worker 节点提升为管理节点。

有关 swarm 管理的更多信息，请参阅 [Swarm 管理指南](admin_guide.md)。

## 检查单个节点

您可以在管理节点上运行 `docker node inspect <NODE-ID>` 来查看单个节点的详细信息。输出默认为 JSON 格式，但您可以传递 `--pretty` 标志以人类可读的格式打印结果。例如：

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

您可以修改节点属性以：

* [更改节点可用性](#change-node-availability)
* [添加或删除标签元数据](#add-or-remove-label-metadata)
* [更改节点角色](#promote-or-demote-a-node)

### 更改节点可用性

更改节点可用性可让您：

* 将管理节点设置为 `Drain`，使其仅执行 swarm 管理任务，不可用于任务分配。
* 将节点设置为 `Drain`，以便您可以将其关闭进行维护。
* 暂停节点，使其无法接收新任务。
* 恢复不可用或暂停节点的可用性状态。

例如，要将管理节点的可用性更改为 `Drain`：

```console
$ docker node update --availability drain node-1

node-1
```

有关不同可用性选项的描述，请参阅[列出节点](#list-nodes)。

### 添加或删除标签元数据

节点标签提供了一种灵活的节点组织方法。您还可以在服务约束中使用节点标签。在创建服务时应用约束，以限制调度器为该服务分配任务的节点。

在管理节点上运行 `docker node update --label-add` 以向节点添加标签元数据。`--label-add` 标志支持 `<key>` 或 `<key>=<value>` 对。

为要添加的每个节点标签传递一次 `--label-add` 标志：

```console
$ docker node update --label-add foo --label-add bar=baz node-1

node-1
```

您使用 `docker node update` 为节点设置的标签仅适用于 swarm 中的节点实体。不要将它们与 [dockerd](/manuals/engine/manage-resources/labels.md) 的 Docker 守护进程标签混淆。

因此，节点标签可用于将关键任务限制在满足特定要求的节点上。例如，仅在应运行特殊工作负载的机器上调度，例如满足 [PCI-SS 合规性](https://www.pcisecuritystandards.org/)的机器。

被入侵的 worker 节点无法更改节点标签，因此无法破坏这些特殊工作负载。

然而，引擎标签仍然有用，因为某些不影响容器安全编排的功能可能更适合以分散的方式设置。例如，引擎可以有一个标签来指示它具有某种类型的磁盘设备，这可能与安全性无直接关系。这些标签更容易被 swarm 编排器“信任”。

有关服务约束的更多信息，请参阅 `docker service create` [CLI 参考](/reference/cli/docker/service/create.md)。

### 提升或降级节点

您可以将 worker 节点提升为管理角色。这在管理节点变得不可用或您希望将管理节点脱机进行维护时非常有用。同样，您也可以将管理节点降级为 worker 节点。

> [!NOTE]
>
> 无论您提升或降级节点的原因是什么，您都必须始终在 swarm 中保持管理节点的仲裁。有关更多信息，请参阅 [Swarm 管理指南](admin_guide.md)。

要提升一个或多个节点，请在管理节点上运行 `docker node promote`：

```console
$ docker node promote node-3 node-2

Node node-3 promoted to a manager in the swarm.
Node node-2 promoted to a manager in the swarm.
```

要降级一个或多个节点，请在管理节点上运行 `docker node demote`：

```console
$ docker node demote node-3 node-2

Manager node-3 demoted in the swarm.
Manager node-2 demoted in the swarm.
```

`docker node promote` 和 `docker node demote` 分别是 `docker node update --role manager` 和 `docker node update --role worker` 的便捷命令。

## 在 swarm 节点上安装插件

如果您的 swarm 服务依赖于一个或多个[插件](/engine/extend/plugin_api/)，则这些插件需要在服务可能部署到的每个节点上都可用。您可以手动在每个节点上安装插件，也可以编写安装脚本。您还可以使用 Docker API 以类似于全局服务的方式部署插件，方法是指定 `PluginSpec` 而不是 `ContainerSpec`。

> [!NOTE]
>
> 目前无法使用 Docker CLI 或 Docker Compose 将插件部署到 swarm。此外，无法从私有存储库安装插件。

[`PluginSpec`](/engine/extend/plugin_api/#json-specification) 由插件开发人员定义。要将插件添加到所有 Docker 节点，请使用 [`service/create`](/reference/api/engine/v1.31/#operation/ServiceCreate) API，传递在 `TaskTemplate` 中定义的 `PluginSpec` JSON。

## 离开 swarm

在节点上运行 `docker swarm leave` 命令以将其从 swarm 中移除。

例如，要在 worker 节点上离开 swarm：

```console
$ docker swarm leave

Node left the swarm.
```

当节点离开 swarm 时，Docker Engine 将停止在 Swarm 模式下运行。编排器不再向该节点调度任务。

如果该节点是管理节点，您将收到有关维护仲裁的警告。要覆盖警告，请传递 `--force` 标志。如果最后一个管理节点离开 swarm，则 swarm 将变得不可用，需要您采取灾难恢复措施。

有关维护仲裁和灾难恢复的信息，请参阅 [Swarm 管理指南](admin_guide.md)。

节点离开 swarm 后，您可以在管理节点上运行 `docker node rm` 以从节点列表中移除该节点。

例如：

```console
$ docker node rm node-2
```

## 了解更多

* [Swarm 管理指南](admin_guide.md)
* [Docker Engine 命令行参考](/reference/cli/docker/)
* [Swarm 模式教程](swarm-tutorial/_index.md)