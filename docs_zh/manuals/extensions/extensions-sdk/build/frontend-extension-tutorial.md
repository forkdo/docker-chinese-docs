---
title: 创建高级前端扩展
description: 高级前端扩展教程
keywords: Docker, extensions, sdk, build
aliases:
 - /desktop/extensions-sdk/tutorials/react-extension/
 - /desktop/extensions-sdk/build/set-up/react-extension/
 - /desktop/extensions-sdk/build/set-up/minimal-frontend-using-docker-cli/
 - /desktop/extensions-sdk/build/set-up/frontend-extension-tutorial/
 - /desktop/extensions-sdk/build/frontend-extension-tutorial/
weight: 20
---

要开始创建你的扩展，你首先需要一个包含若干文件的目录，这些文件从扩展的源代码到扩展所需的特定文件都有。本页提供
关于如何搭建一个具有更高级前端的扩展的信息。

在开始之前，请确保你已经安装了最新版本的 [Docker Desktop](/manuals/desktop/release-notes.md)。

## 扩展文件夹结构（Extension folder structure）

创建新扩展最快的方式是像 [快速入门](../quickstart.md) 中那样运行 `docker extension init my-extension`。这会创建一个
包含完整功能扩展的新目录 `my-extension`。

> [!TIP]
>
> `docker extension init` 生成的是基于 React 的扩展。但你仍可以将其作为你自己扩展的起点，并使用任何其他前端框架，
> 如 Vue、Angular、Svelte 等，甚至坚持使用原生 JavaScript（vanilla Javascript）。

虽然你可以从空目录或 `react-extension` [示例文件夹](https://github.com/docker/extensions-sdk/tree/main/samples) 开始，但
强烈建议你从 `docker extension init` 命令开始，并更改为满足你的需求。

```bash
.
├── Dockerfile # (1)
├── ui # (2)
│   ├── public # (3)
│   │   └── index.html
│   ├── src # (4)
│   │   ├── App.tsx
│   │   ├── index.tsx
│   ├── package.json
│   └── package-lock.lock
│   ├── tsconfig.json
├── docker.svg # (5)
└── metadata.json # (6)
```

1. 包含构建扩展并在 Docker Desktop 中运行它所需的一切。
2. 包含你前端应用源代码的高层文件夹。
3. 未被编译或动态生成的资源存储在此处。这些可以是静态资源，如 logo 或 robots.txt 文件。
4. src 或源文件夹包含所有的 React 组件、外部 CSS 文件，以及引入到组件文件中的动态资源。
5. 显示在 Docker Desktop 仪表盘左侧菜单中的图标。
6. 提供有关扩展信息（如名称、描述和版本）的文件。

## 调整 Dockerfile（Adapting the Dockerfile）

> [!NOTE]
>
> 使用 `docker extension init` 时，它会创建一个已经包含 React 扩展所需内容的 `Dockerfile`。

创建扩展后，你需要配置 `Dockerfile` 来构建扩展，并配置用于在 Marketplace 中填充扩展卡片的标签。以下是一个
React 扩展的 `Dockerfile` 示例：

{{< tabs group="framework" >}}
{{< tab name="React" >}}

```Dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM node:18.9-alpine3.15 AS client-builder
WORKDIR /ui
# cache packages in layer
COPY ui/package.json /ui/package.json
COPY ui/package-lock.json /ui/package-lock.json
RUN --mount=type=cache,target=/usr/src/app/.npm \
    npm set cache /usr/src/app/.npm && \
    npm ci
# install
COPY ui /ui
RUN npm run build

FROM alpine
LABEL org.opencontainers.image.title="My extension" \
    org.opencontainers.image.description="Your Desktop Extension Description" \
    org.opencontainers.image.vendor="Awesome Inc." \
    com.docker.desktop.extension.api.version="0.3.3" \
    com.docker.desktop.extension.icon="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" \
    com.docker.extension.screenshots="" \
    com.docker.extension.detailed-description="" \
    com.docker.extension.publisher-url="" \
    com.docker.extension.additional-urls="" \
    com.docker.extension.changelog=""

COPY metadata.json .
COPY docker.svg .
COPY --from=client-builder /ui/build ui

```
> Note
>
> 在示例 Dockerfile 中，你可以看到镜像标签 `com.docker.desktop.extension.icon` 被设置为一个图标 URL。Extensions
> Marketplace 会在不安装扩展的情况下显示此图标。Dockerfile 还包含 `COPY docker.svg .` 来在镜像内复制一个图标文件。
> 这个第二个图标文件用于在扩展安装后在仪表盘中显示扩展 UI。

{{< /tab >}}
{{< tab name="Vue" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Vue 的可运行 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> 让我们知道你是否想要 Vue 的 Dockerfile。

{{< /tab >}}
{{< tab name="Angular" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Angular 的可运行 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> 让我们知道你是否想要 Angular 的 Dockerfile。

{{< /tab >}}
{{< tab name="Svelte" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Svelte 的可运行 Dockerfile。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> 让我们知道你是否想要 Svelte 的 Dockerfile。

{{< /tab >}}
{{< /tabs >}}

## 配置元数据文件（Configure the metadata file）

要在 Docker Desktop 中为你的扩展添加标签页，你必须在扩展目录根目录的 `metadata.json` 文件中配置它。

```json
{
  "icon": "docker.svg",
  "ui": {
    "dashboard-tab": {
      "title": "UI Extension",
      "root": "/ui",
      "src": "index.html"
    }
  }
}
```

`title` 属性是显示在 Docker Desktop 仪表盘左侧菜单中的扩展名称。`root` 属性是扩展容器文件系统中前端应用程序的路径，
系统用它来在主机上部署。`src` 属性是 `root` 文件夹内前端应用程序 HTML 入口点的路径。

有关 `metadata.json` 的 `ui` 段落的更多信息，请参阅 [元数据](../architecture/metadata.md#ui-section)。

## 构建扩展并安装（Build the extension and install it）

现在你已经配置好了扩展，需要构建 Docker Desktop 将用于安装它的扩展镜像。

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

这会构建一个标记为 `awesome-inc/my-extension:latest` 的镜像，你可以运行 `docker inspect
awesome-inc/my-extension:latest` 查看更多细节。

最后，你可以安装扩展并在 Docker Desktop 仪表盘中看到它出现。

```bash
docker extension install awesome-inc/my-extension:latest
```

## 使用扩展 API 客户端（Use the Extension APIs client）

要使用扩展 API 并通过 Docker Desktop 执行操作，扩展必须首先导入 `@docker/extension-api-client` 库。要安装它，
运行以下命令：

```bash
npm install @docker/extension-api-client
```

然后调用 `createDockerDesktopClient` 函数创建一个客户端对象来调用扩展 API。

```js
import { createDockerDesktopClient } from '@docker/extension-api-client';

const ddClient = createDockerDesktopClient();
```

使用 Typescript 时，你也可以将 `@docker/extension-api-client-types` 作为 dev 依赖安装。这会为你提供扩展 API 的
类型定义，并在 IDE 中提供自动补全。

```bash
npm install @docker/extension-api-client-types --save-dev
```

![IDE 中的自动补全](images/types-autocomplete.png)

例如，你可以使用 `docker.cli.exec` 函数通过 `docker ps --all` 命令获取所有容器的列表，并将结果显示在表格中。

{{< tabs group="framework" >}}
{{< tab name="React" >}}

用以下代码替换 `ui/src/App.tsx` 文件：

```tsx

// ui/src/App.tsx
import React, { useEffect } from 'react';
import {
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography
} from "@mui/material";
import { createDockerDesktopClient } from "@docker/extension-api-client";

//obtain docker desktop extension client
const ddClient = createDockerDesktopClient();

export function App() {
  const [containers, setContainers] = React.useState<any[]>([]);

  useEffect(() => {
    // List all containers
    ddClient.docker.cli.exec('ps', ['--all', '--format', '"{{json .}}"']).then((result) => {
      // result.parseJsonLines() parses the output of the command into an array of objects
      setContainers(result.parseJsonLines());
    });
  }, []);

  return (
    <Stack>
      <Typography data-testid="heading" variant="h3" role="title">
        Container list
      </Typography>
      <Typography
      data-testid="subheading"
      variant="body1"
      color="text.secondary"
      sx={{ mt: 2 }}
    >
      Simple list of containers using Docker Extensions SDK.
      </Typography>
      <TableContainer sx={{mt:2}}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Container id</TableCell>
              <TableCell>Image</TableCell>
              <TableCell>Command</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {containers.map((container) => (
              <TableRow
                key={container.ID}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
              >
                <TableCell>{container.ID}</TableCell>
                <TableCell>{container.Image}</TableCell>
                <TableCell>{container.Command}</TableCell>
                <TableCell>{container.CreatedAt}</TableCell>
                <TableCell>{container.Status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Stack>
  );
}

```

![容器列表示例截图。](images/react-extension.png)

{{< /tab >}}
{{< tab name="Vue" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Vue 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> 让我们知道你是否想要 Vue 的示例。

{{< /tab >}}
{{< tab name="Angular" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Angular 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> 让我们知道你是否想要 Angular 的示例。

{{< /tab >}}
{{< tab name="Svelte" >}}

> [!IMPORTANT]
>
> 我们目前还没有 Svelte 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> 让我们知道你是否想要 Svelte 的示例。

{{< /tab >}}
{{< /tabs >}}

## 前端代码强制执行的策略（Policies enforced for the front-end code）

扩展 UI 代码在独立的 electron 会话中渲染，没有初始化 node.js 环境，也无法直接访问 electron API。

这是为了限制可能对整个 Docker 仪表盘产生的意外副作用。

扩展 UI 代码不能执行特权任务，例如更改系统或生成子进程，除非通过使用扩展框架提供的 SDK API。扩展 UI 代码也
只能通过扩展 SDK API 执行与 Docker Desktop 的交互，例如导航到仪表盘中的各个位置。

扩展 UI 部分彼此隔离，每个扩展的 UI 代码运行在它自己的会话中。扩展无法访问其他扩展的会话数据。

`localStorage` 是浏览器 Web 存储的机制之一。它允许用户将数据以键值对的形式保存在浏览器中以供以后使用。当浏览器
（扩展面板）关闭时，`localStorage` 不会清除数据。这使其非常适合在离开扩展导航到 Docker Desktop 其他部分时持久化
数据。

如果你的扩展使用 `localStorage` 存储数据，运行在 Docker Desktop 中的其他扩展无法访问你的扩展的本地存储。扩展的
本地存储在 Docker Desktop 停止或重启后仍然持久化。当扩展升级时，其本地存储会持久化；而当其被卸载时，本地存储会被
完全移除。

## 重新构建扩展并更新它（Re-build the extension and update it）

由于你已修改了扩展的代码，必须重新构建扩展。

```console
$ docker build --tag=awesome-inc/my-extension:latest .
```

构建完成后，你需要更新它。

```console
$ docker extension update awesome-inc/my-extension:latest
```

现在你可以在 Docker Desktop 仪表盘的容器标签页中看到后端服务正在运行，并在需要调试时查看日志。

> [!TIP]
>
> 你可以开启 [热重载](../dev/test-debug.md#hot-reloading-whilst-developing-the-ui) 以避免每次更改都需要重新构建扩展。

## 接下来？（What's next?）

- 为你的扩展添加 [后端](backend-extension-tutorial.md)。
- 了解如何 [测试和调试](../dev/test-debug.md) 你的扩展。
- 了解如何为你的扩展 [设置 CI](../dev/continuous-integration.md)。
- 了解更多关于扩展 [架构](../architecture/_index.md)。
- 有关构建 UI 的更多信息和指南，请参阅 [设计与 UI 样式部分](../design/design-guidelines.md)。
- 如果你想为扩展设置用户认证，请参阅 [认证](../guides/oauth2-flow.md)。
