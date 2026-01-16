---
title: Interface: ExtensionHost
url: /reference/api/extensions-sdk/ExtensionHost/
parent:
  title: 扩展 API 参考
  url: /reference/api/extensions-sdk/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: 扩展 API 参考
    url: /reference/api/extensions-sdk/
  - title: Interface: ExtensionHost
    url: /reference/api/extensions-sdk/ExtensionHost/
next:
  title: Interface: ExecResultV0
  url: /reference/api/extensions-sdk/ExecResultV0/
prev:
  title: Interface: OpenDialogResult
  url: /reference/api/extensions-sdk/OpenDialogResult/
---


**`Since`**

0.2.0

## 属性

### cli

• `Readonly` **cli**: [`ExtensionCli`](ExtensionCli.md)

在宿主机上执行命令。

例如，在宿主机上执行已打包的二进制文件 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

---

流式传输在后端容器或宿主机上执行的命令输出。

假设 `kubectl` 二进制文件作为扩展的一部分打包，你可以在宿主机上启动 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
           stream: {
             onOutput(data): void {
                 // 由于可能同时接收到 `stdout` 和 `stderr`，我们将其包装在 JSON 对象中
                 JSON.stringify(
                   {
                     stdout: data.stdout,
                     stderr: data.stderr,
                   },
                   null,
                   "  "
                 );
             },
             onError(error: any): void {
               console.error(error);
             },
             onClose(exitCode: number): void {
               console.log("onClose with exit code " + exitCode);
             },
           },
         });
```
