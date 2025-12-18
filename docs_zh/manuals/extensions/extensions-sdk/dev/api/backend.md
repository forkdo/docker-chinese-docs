---
title: 扩展后端
description: Docker 扩展 API
keywords: Docker, extensions, sdk, API
aliases: 
 - /desktop/extensions-sdk/dev/api/backend/
---

`ddClient.extension.vm` 对象可用于与扩展元数据中 [vm 部分](../../architecture/metadata.md#vm-section) 定义的后端通信。

## get

▸ **get**(`url`): `Promise`<`unknown`\>

向后端服务发送 HTTP GET 请求。

```typescript
ddClient.extension.vm.service
 .get("/some/service")
 .then((value: any) => console.log(value)
```

其他方法（如 POST、UPDATE 和 DELETE）请参阅 [服务 API 参考](/reference/api/extensions-sdk/HttpService.md)。

> 已弃用的扩展后端通信
>
> 下面使用 `window.ddClient.backend` 的方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

`window.ddClient.backend` 对象可用于与扩展元数据中 [vm 部分](../../architecture/metadata.md#vm-section) 定义的后端通信。客户端已连接到后端。

示例用法：

```typescript
window.ddClient.backend
  .get("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .post("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .put("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .patch("/some/service", { ... })
  .then((value: any) => console.log(value));

window.ddClient.backend
  .delete("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .head("/some/service")
  .then((value: any) => console.log(value));

window.ddClient.backend
  .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
  .then((value: any) => console.log(value));
```

## 在扩展后端容器中运行命令

例如，在后端容器内执行 `ls -l` 命令：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"]);
```

流式传输在后端容器中执行的命令输出。例如，在后端容器内启动 `ls -l` 命令：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
  stream: {
    onOutput(data) {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
    },
    onError(error) {
      console.error(error);
    },
    onClose(exitCode) {
      console.log("onClose with exit code " + exitCode);
    },
  },
});
```

更多详情，请参阅 [扩展 VM API 参考](/reference/api/extensions-sdk/ExtensionVM.md)

> 已弃用的扩展后端命令执行
>
> 此方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

如果您的扩展包含应在后端容器中运行的额外二进制文件，可以使用 `execInVMExtension` 函数：

```typescript
const output = await window.ddClient.backend.execInVMExtension(
  `cliShippedInTheVm xxx`
);
console.log(output);
```

## 在主机上调用扩展二进制文件

在主机上调用二进制文件。该二进制文件通常通过扩展元数据中的 [host 部分](../../architecture/metadata.md#host-section) 随您的扩展一起分发。请注意，扩展以用户权限运行，此 API 不限制于扩展元数据 [host 部分](../../architecture/metadata.md#host-section) 中列出的二进制文件（某些扩展可能在用户交互期间安装软件，并调用新安装的二进制文件，即使未在扩展元数据中列出）。

例如，在主机上执行分发的二进制文件 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

只要 `kubectl` 二进制文件作为您扩展的一部分分发，您就可以在主机上启动 `kubectl -h` 命令并获取输出流：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
  stream: {
    onOutput(data: { stdout: string } | { stderr: string }): void {
      if (data.stdout) {
        console.error(data.stdout);
      } else {
        console.log(data.stderr);
      }
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

您可以在后端容器或主机上流式传输执行命令的输出。

更多详情，请参阅 [扩展主机 API 参考](/reference/api/extensions-sdk/ExtensionHost.md)

> 已弃用的扩展二进制文件调用
>
> 此方法已被弃用，将在未来版本中移除。请使用上面指定的方法。

在主机上执行命令：

```typescript
window.ddClient.execHostCmd(`cliShippedOnHost xxx`).then((cmdResult: any) => {
  console.log(cmdResult);
});
```

在后端容器或主机上流式传输执行命令的输出：

```typescript
window.ddClient.spawnHostCmd(
  `cliShippedOnHost`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // 命令退出后，我们获得状态码
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> [!NOTE]
> 
> 您不能在单个 `exec()` 调用中链接命令（例如 `cmd1 $(cmd2)` 或在命令间使用管道）。
>
> 您需要为每个命令调用 `exec()`，并解析结果以在需要时将参数传递给下一个命令。