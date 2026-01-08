---
title: 扩展 UI API
description: Docker 扩展开发概述
keywords: Docker, extensions, sdk, development
aliases:
- /desktop/extensions-sdk/dev/api/overview/
---

扩展 UI 运行在沙盒环境中，无法访问任何
electron 或 nodejs API。

扩展 UI API 为前端提供了一种执行不同操作的方式，
并与 Docker Desktop 仪表板或底层系统进行通信。

支持 Typescript 的 JavaScript API 库可用于将全部 API 定义引入到您的扩展代码中。

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

`ddClient` 对象提供对各种 API 的访问：

- [扩展后端](backend.md)
- [Docker](docker.md)
- [仪表板](dashboard.md)
- [导航](dashboard-routes-navigation.md)

另请参阅 [扩展 API 参考](reference/api/extensions-sdk/_index.md)。