---
title: 测试和调试
description: 测试和调试你的扩展。
keywords: Docker, Extensions, sdk, preview, update, Chrome DevTools
aliases:
 - /desktop/extensions-sdk/build/test-debug/
 - /desktop/extensions-sdk/dev/test-debug/
weight: 10
---

为了提升开发体验，Docker Desktop 提供了一套工具来帮助你测试和调试扩展。

### 打开 Chrome DevTools

当你选择 **Extensions** 标签时，若要为你的扩展打开 Chrome DevTools，请运行：

```console
$ docker extension dev debug <name-of-your-extensions>
```

之后每次点击扩展标签也会打开 Chrome DevTools。要停止这种行为，请运行：

```console
$ docker extension dev reset <name-of-your-extensions>
```

扩展部署后，也可以通过 UI 扩展部分使用 [Konami Code](https://en.wikipedia.org/wiki/Konami_Code) 的变体来打开 Chrome DevTools。选择 **Extensions** 标签，然后依次按下按键序列 `up, up, down, down, left, right, left, right, p, d, t`。

### 开发 UI 时的热重载

在 UI 开发过程中，使用热重载来测试更改而不必重建整个扩展会很有帮助。为此，你可以配置 Docker Desktop 从开发服务器加载你的 UI，比如 [Vite](https://vitejs.dev/) 在执行 `npm start` 时启动的服务器。

假设你的应用运行在默认端口，启动你的 UI 应用，然后运行：

```console
$ cd ui
$ npm run dev
```

这将启动一个监听 3000 端口的开发服务器。

现在你可以告诉 Docker Desktop 使用这个作为前端源。在另一个终端中运行：

```console
$ docker extension dev ui-source <name-of-your-extensions> http://localhost:3000
```

关闭并重新打开 Docker Desktop 仪表板，然后进入你的扩展。所有前端代码的更改都会立即可见。

完成后，你可以将扩展配置重置为原始设置。这也会重置 Chrome DevTools 的自动打开行为（如果你之前使用过 `docker extension dev debug <name-of-your-extensions>`）：

```console
$ docker extension dev reset <name-of-your-extensions>
```

## 显示扩展容器

如果你的扩展由一个或多个在 Docker Desktop VM 中作为容器运行的服务组成，你可以轻松地从 Docker Desktop 仪表板访问它们。

1. 在 Docker Desktop 中，导航到 **Settings**。
2. 在 **Extensions** 标签下，选择 **Show Docker Desktop Extensions system containers** 选项。现在你可以查看你的扩展容器及其日志。

## 清理

要删除扩展，请运行：

```console
$ docker extension rm <name-of-your-extension>
```

## 下一步

- 构建一个 [高级前端](/manuals/extensions/extensions-sdk/build/frontend-extension-tutorial.md) 扩展。
- 了解有关扩展 [架构](../architecture/_index.md) 的更多信息。
- 探索我们的 [设计原则](../design/design-principles.md)。
- 查看我们的 [UI 样式指南](../design/_index.md)。
- 学习如何为你的扩展 [设置 CI](continuous-integration.md)。