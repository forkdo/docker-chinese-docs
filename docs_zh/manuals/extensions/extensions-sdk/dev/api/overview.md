---
title: 扩展 UI API
description: Docker 扩展开发概述
keywords: Docker, extensions, sdk, development
aliases:
 - /desktop/extensions-sdk/dev/api/overview/
---

扩展的 UI 运行在一个沙盒环境中，无法访问任何 electron 或 nodejs API。

扩展 UI API 为前端提供了一种方式，可以执行不同的操作并与 Docker Desktop 仪表板或底层系统进行通信。

我们提供了带有 Typescript 支持的 JavaScript API 库，以便在扩展代码中获取所有 API 定义。

- [@docker/extension-api-client](https://www.npmjs.com/package/@docker/extension-api-client) 提供对扩展 API 入口点 `DockerDesktopClient` 的访问。
- [@docker/extension-api-client-types](https://www.npmjs.com/package/@docker/extension-api-client-types) 可作为开发依赖项添加，以便在 IDE 中获得类型自动补全功能。

```Typescript
import { createDockerDesktopClient } from '@docker/extension-api-client';

export function App() {
  // 获取 Docker Desktop 客户端
  const ddClient = createDockerDesktopClient();
  // 使用 ddClient 执行扩展操作
}
```

`ddClient` 对象提供了对各种 API 的访问：

- [扩展后端](backend.md)
- [Docker](docker.md)
- [仪表板](dashboard.md)
- [导航](dashboard-routes-navigation.md)

另请参阅 [扩展 API 参考文档](reference/api/extensions-sdk/_index.md)。