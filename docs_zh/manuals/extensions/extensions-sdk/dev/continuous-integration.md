---
title: 持续集成 (CI)
description: 自动测试和验证您的扩展。
keywords: Docker, Extensions, sdk, CI, test, regression
aliases:
- /desktop/extensions-sdk/dev/continuous-integration/
weight: 20
---

为了帮助验证您的扩展并确保其功能正常，扩展 SDK 提供了工具来帮助您为扩展设置持续集成。

> [!重要]
>
> [Docker Desktop Action](https://github.com/docker/desktop-action) 和 [extension-test-helper 库](https://www.npmjs.com/package/@docker/extension-test-helper) 目前均为[实验性功能](https://docs.docker.com/release-lifecycle/#experimental)。

## 使用 GitHub Actions 设置 CI 环境

您需要 Docker Desktop 才能安装和验证扩展。
可以通过在工作流文件中添加以下内容，使用 [Docker Desktop Action](https://github.com/docker/desktop-action) 在 GitHub Actions 中启动 Docker Desktop：

```yaml
steps:
  - id: start_desktop
    uses: docker/desktop-action/start@v0.1.0
```

> [!注意]
>
> 此操作目前仅支持 GitHub Actions 的 macOS 运行器。您需要在端到端测试中指定 `runs-on: macOS-latest`。

执行该步骤后，后续步骤将使用 Docker Desktop 和 Docker CLI 来安装和测试扩展。

## 使用 Puppeteer 验证扩展

在 CI 中启动 Docker Desktop 后，您可以使用 Jest 和 Puppeteer 构建、安装和验证扩展。

首先，从测试中构建并安装扩展：

```ts
import { DesktopUI } from "@docker/extension-test-helper";
import { exec as originalExec } from "child_process";
import * as util from "util";

export const exec = util.promisify(originalExec);

// 保留应用句柄以便在测试结束时停止它
let dashboard: DesktopUI;

beforeAll(async () => {
  await exec(`docker build -t my/extension:latest .`, {
    cwd: "my-extension-src-root",
  });

  await exec(`docker extension install -f my/extension:latest`);
});
```

然后打开 Docker Desktop 仪表板并在扩展的 UI 中运行一些测试：

```ts
describe("测试我的扩展", () => {
  test("应该能够正常工作", async () => {
    dashboard = await DesktopUI.start();

    const eFrame = await dashboard.navigateToExtension("my/extension");

    // 使用 puppeteer API 操作 UI，点击按钮，检查视觉显示并验证扩展
    await eFrame.waitForSelector("#someElementId");
  });
});
```

最后，关闭 Docker Desktop 仪表板并卸载扩展：

```ts
afterAll(async () => {
  dashboard?.stop();
  await exec(`docker extension uninstall my/extension`);
});
```

## 下一步

- 构建一个[高级前端](/manuals/extensions/extensions-sdk/build/frontend-extension-tutorial.md)扩展。
- 了解更多关于扩展[架构](../architecture/_index.md)的信息。
- 了解如何[发布您的扩展](../extensions/_index.md)。