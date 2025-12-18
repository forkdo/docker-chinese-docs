---
title: 导航
description: Docker 扩展 API
keywords: Docker, 扩展, sdk, API
aliases:
 - /desktop/extensions-sdk/dev/api/dashboard-routes-navigation/
---

`ddClient.desktopUI.navigate` 可以导航到 Docker Desktop 的特定界面，例如容器标签页、镜像标签页，或特定容器的日志。

例如，导航到指定容器的日志：

```typescript
const id = '8c7881e6a107';
try {
  await ddClient.desktopUI.navigate.viewContainerLogs(id);
} catch (e) {
  console.error(e);
  ddClient.desktopUI.toast.error(
    `Failed to navigate to logs for container "${id}".`
  );
}
```

#### 参数

| 名称 | 类型     | 描述                                                                                                                                                                                            |
| :--- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id` | `string` | 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`。你可以在 `docker ps` 命令中使用 `--no-trunc` 标志来显示完整的容器 ID。 |

#### 返回值

`Promise`<`void`\>

如果容器不存在，Promise 将会失败。

有关所有导航方法的详细信息，请参阅 [导航 API 参考](/reference/api/extensions-sdk/NavigationIntents.md)。

> 已弃用的导航方法
>
> 这些方法已被弃用，将在未来的版本中移除。请使用上面指定的新方法。

```typescript
window.ddClient.navigateToContainers();
// id - 完整的容器 ID，例如 `46b57e400d801762e9e115734bf902a2450d89669d85881058a46136520aca28`
window.ddClient.navigateToContainer(id);
window.ddClient.navigateToContainerLogs(id);
window.ddClient.navigateToContainerInspect(id);
window.ddClient.navigateToContainerStats(id);

window.ddClient.navigateToImages();
window.ddClient.navigateToImage(id, tag);

window.ddClient.navigateToVolumes();
window.ddClient.navigateToVolume(volume);

window.ddClient.navigateToDevEnvironments();
```