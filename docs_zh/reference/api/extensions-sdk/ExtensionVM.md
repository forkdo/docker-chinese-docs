---
title: "接口: ExtensionVM"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/ExtensionVM/
---

**`Since`**

0.2.0

## 属性

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

流式传输在后端容器中执行的命令输出。

当扩展定义了自己的 `compose.yaml` 文件且包含多个容器时，
命令将在定义的第一个容器中执行。
如需在其他容器中执行命令，请调整容器的定义顺序。

示例：在后端容器中启动命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
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

**`Param`**

要执行的命令。

**`Param`**

命令的参数。

**`Param`**

用于监听命令输出数据和错误的回调函数。

___

### service

• `Optional` `Readonly` **service**: [`HttpService`](HttpService.md)