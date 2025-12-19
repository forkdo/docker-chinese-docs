---
title: 测试与调试
description: 测试与调试您的扩展。
keywords: Docker, Extensions, sdk, preview, update, Chrome DevTools
aliases:
 - /desktop/extensions-sdk/build/test-debug/
 - /desktop/extensions-sdk/dev/test-debug/
weight: 10
---

为了改善开发者体验，Docker Desktop 提供了一系列工具来帮助您测试和调试您的扩展。

### 打开 Chrome DevTools

当您选择 **Extensions** 标签页时，若要为您的扩展打开 Chrome DevTools，请运行：

```console
$ docker extension dev debug <name-of-your-extensions>
```

之后每次点击扩展标签页也会打开 Chrome DevTools。要停止此行为，请运行：

```console
$ docker extension dev reset <name-of-your-extensions>
```

扩展部署后，也可以通过 [Konami Code](https://en.wikipedia.org/wiki/Konami_Code) 的一种变体从扩展 UI 部分打开 Chrome DevTools。选择 **Extensions** 标签页，然后依次按下 `up, up, down, down, left, right, left, right, p, d, t` 键序列。

### 在 UI 开发中进行热重载

在 UI 开发过程中，使用 hot reloading 来测试更改而无需重新构建整个扩展会很有帮助。为此，您可以将 Docker Desktop 配置为从开发服务器加载您的 UI，例如使用 `npm start` 命令启动 [Vite](https://vitejs.dev/) 时所创建的服务器。

假设您的应用运行在默认端口，请启动您的 UI 应用，然后运行：

```console
$ cd ui
$ npm run dev
```

这会启动一个监听 3000 端口的开发服务器。

现在，您可以告知 Docker Desktop 使用此地址作为 frontend source。在另一个终端中运行：

```console
$ docker extension dev ui-source <name-of-your-extensions> http://localhost:3000
```

关闭并重新打开 Docker Desktop 仪表板，然后进入您的扩展。前端代码的所有更改将立即可见。

完成后，您可以将扩展配置重置为原始设置。如果您之前使用了 `docker extension dev debug <name-of-your-extensions>`，这也会重置打开 Chrome DevTools 的行为：

```console
$ docker extension dev reset <name-of-your-extensions>
```

## 显示扩展容器

如果您的扩展由一个或多个作为容器运行在 Docker Desktop VM 中的服务组成，您可以从 Docker Desktop 的仪表板中轻松访问它们。

1.  在 Docker Desktop 中，导航到 **Settings**。
2.  在 **Extensions** 标签页下，选择 **Show Docker Desktop Extensions system containers** 选项。您现在可以查看您的扩展容器及其 logs。

## 清理

要移除扩展，请运行：

```console
$ docker extension rm <name-of-your-extension>
```

## 后续步骤

- 构建一个[高级前端](/manuals/extensions/extensions-sdk/build/frontend-extension-tutorial.md)扩展。
- 了解更多关于扩展[架构](../architecture/_index.md)的信息。
- 探索我们的[设计原则](../design/design-principles.md)。
- 查看我们的 [UI 样式指南](../design/_index.md)。
- 了解如何为您的扩展[设置 CI](continuous-integration.md)。