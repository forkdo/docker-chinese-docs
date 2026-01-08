---
title: '接口: ExtensionVM'
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
- /desktop/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
- /extensions/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
---

**`Since`**

0.2.0

## 属性 (Properties)

### cli

• `Readonly` **cli**: [`ExtensionCli`](ExtensionCli.md)

在后端容器中执行命令。

示例：在后端容器中执行命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec(
  "ls",
  ["-l"]
);
```

流式传输在后端容器中执行命令的输出。

当扩展定义了自己的 `compose.yaml` 文件并包含多个容器时，该命令将在定义的第一个容器上执行。
更改容器的定义顺序，以便在另一个容器上执行命令。

示例：在后端容器中生成命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
           stream: {
             onOutput(data): void {
                 // 由于我们可能同时接收到 `stdout` 和 `stderr`，因此将它们包装在 JSON 对象中
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

**`Param`**

要执行的命令。

**`Param`**

要执行的命令的参数。

**`Param`**

用于监听命令输出数据和错误的回调函数。

___

### service

• `Optional` `Readonly` **service**: [`HttpService`](HttpService.md)