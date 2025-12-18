---
title: "接口: DockerDesktopClient"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/DockerDesktopClient/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/DockerDesktopClient/
---

Docker Desktop API 客户端 v0 和 v1 接口的组合，
出于向后兼容性的原因提供。
除非你正在使用遗留扩展，请改用 v1 类型。

## 属性

### backend

• `只读` **backend**: `undefined` \| [`BackendV0`](BackendV0.md)

`window.ddClient.backend` 对象可用于与扩展元数据的 vm 部分中定义的后端通信。
客户端已连接到后端。

> [!WARNING]
>
> 它将在未来版本中被移除。请改用 [extension](DockerDesktopClient.md#extension)。

#### 继承自

DockerDesktopClientV0.backend

___

### extension

• `只读` **extension**: [`Extension`](Extension.md)

`ddClient.extension` 对象可用于与扩展元数据的 vm 部分中定义的后端通信。
客户端已连接到后端。

#### 继承自

DockerDesktopClientV1.extension

___

### desktopUI

• `只读` **desktopUI**: [`DesktopUI`](DesktopUI.md)

#### 继承自

DockerDesktopClientV1.desktopUI

___

### host

• `只读` **host**: [`Host`](Host.md)

#### 继承自

DockerDesktopClientV1.host

___

### docker

• `只读` **docker**: [`Docker`](Docker.md)

#### 继承自

DockerDesktopClientV1.docker

## 容器方法

### listContainers

▸ **listContainers**(`options`): `Promise`<`unknown`\>

获取运行中容器的列表（等同于 `docker ps`）。

默认情况下，这不会列出已停止的容器。
你可以使用选项 `{"all": true}` 来列出所有运行和停止的容器。

```typescript
const containers = await window.ddClient.listContainers();
```

> [!WARNING]
>
> 它将在未来版本中被移除。请改用 [listContainers](Docker.md#listcontainers)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options` | `never` | （可选）一个 JSON 对象，如 `{ "all": true, "limit": 10, "size": true, "filters": JSON.stringify({ status: ["exited"] }), }` 有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/engine/api/v1.41/#operation/ContainerList)。 |

#### 返回值

`Promise`<`unknown`\>

#### 继承自

DockerDesktopClientV0.listContainers

___

## 镜像方法

### listImages

▸ **listImages**(`options`): `Promise`<`unknown`\>

获取镜像列表

```typescript
const images = await window.ddClient.listImages();
```

> [!WARNING]
>
> 它将在未来版本中被移除。请改用 [listImages](Docker.md#listimages)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options` | `never` | （可选）一个 JSON 对象，如 `{ "all": true, "filters": JSON.stringify({ dangling: ["true"] }), "digests": true }` 有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/engine/api/v1.41/#tag/Image)。 |

#### 返回值

`Promise`<`unknown`\>

#### 继承自

DockerDesktopClientV0.listImages

___

## 导航方法

### navigateToContainers

▸ **navigateToContainers**(): `void`

导航到 Docker Desktop 中的容器窗口。
```typescript
window.ddClient.navigateToContainers();
```

> [!WARNING]
>
> 它将在未来版本中被移除。请改用 [viewContainers](NavigationIntents.md#viewcontainers)。

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.navigateToContainers

___

### navigateToContainer

▸ **navigateToContainer**(`id`): `Promise`<`any`\>

导航到 Docker Desktop 中的容器窗口。
```typescript
await window.ddClient.navigateToContainer(id);
```

> [!WARNING]
>
> 它将在未来版本中被移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。你可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 将失败。

#### 继承自

DockerDesktopClientV0.navigateToContainer

___

### navigateToContainerLogs

▸ **navigateToContainerLogs**(`id`): `Promise`<`any`\>

导航到 Docker Desktop 中的容器日志窗口。
```typescript
await window.ddClient.navigateToContainerLogs(id);
```

> [!WARNING]
>
> 它将在未来版本中被移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。你可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 将失败。

#### 继承自

DockerDesktopClientV0.navigateToContainerLogs

___

### navigateToContainerInspect

▸ **navigateToContainerInspect**(`id`): `Promise`<`any`\>

导航到 Docker Desktop 中的容器检查窗口。
```typescript
await window.ddClient.navigateToContainerInspect(id);
```

> [!WARNING]
>
> 它将在未来版本中被移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。你可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 将失败。

#### 继承自

DockerDesktopClientV0.navigateToContainerInspect

___

### navigateToContainerStats

▸ **navigateToContainerStats**(`id`): `Promise`<`any`\>

导航到容器统计信息，查看 CPU、内存、磁盘读写和网络 I/O 使用情况。

```typescript
await window.ddClient.navigateToContainerStats(id);
```

> [!WARNING]
>
> 它将在未来版本中被移除。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。你可以使用 `docker ps` 命令的 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`any`\>

如果容器不存在，则 Promise 将失败。

#### 继承自

DockerDesktopClientV0.navigateToContainerStats

___

### navigateToImages

▸ **navigateToImages**(): `void`

导航到 Docker Desktop 中的镜像窗口。
```typescript
await window.ddClient.navigateToImages(id);
```

> [!WARNING]
>
> 它将在未来版本中被移除。请改用 [viewImages](NavigationIntents.md#viewimages)。

#### 返回值

`void`

#### 继承自

DockerDesktopClientV0.navigateToImages

___

### navigateToImage

▸ **navigateToImage**(`id`, `tag`): `Promise`<`any`\>

导航到 Docker Desktop 中由 `id` 和 `tag` 引用的特定镜像。
在此导航路径中，你可以找到镜像层、命令、创建时间和大小。

```typescript
await window.ddClient.navigateToImage(id, tag);
```

> [!WARNING]
>
> 它将在未来版本中被移除。请改用 [viewImage](NavigationIntents.md#viewimage)。

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `id` |