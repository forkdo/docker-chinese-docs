# 扩展后端

`ddClient.extension.vm` 对象可用于与扩展元数据中 [vm 部分](../../architecture/metadata.md#vm-section) 定义的后端进行通信。

## get

▸ **get**(`url`): `Promise`<`unknown`\>

向后端服务发起 HTTP GET 请求。

```typescript
ddClient.extension.vm.service
 .get("/some/service")
 .then((value: any) => console.log(value)
```

有关其他方法（如 POST、UPDATE 和 DELETE），请参阅 [Service API 参考](/reference/api/extensions-sdk/HttpService.md)。

> 已弃用的扩展后端通信
>
> 以下使用 `window.ddClient.backend` 的方法已被弃用，并将在未来版本中移除。请使用上面指定的方法。

`window.ddClient.backend` 对象可用于与扩展元数据中 [vm 部分](../../architecture/metadata.md#vm-section) 定义的后端进行通信。客户端已连接到后端。

用法示例：

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

例如，在后端容器中执行命令 `ls -l`：

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"]);
```

流式传输在后端容器中执行的命令输出。例如，在后端容器中生成命令 `ls -l`：

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

更多详情，请参阅 [Extension VM API 参考](/reference/api/extensions-sdk/ExtensionVM.md)

> 已弃用的扩展后端命令执行
>
> 此方法已被弃用，并将在未来版本中移除。请使用上面指定的方法。

如果你的扩展附带了需要在后端容器中运行的额外二进制文件，可以使用 `execInVMExtension` 函数：

```typescript
const output = await window.ddClient.backend.execInVMExtension(
  `cliShippedInTheVm xxx`
);
console.log(output);
```

## 在主机上调用扩展二进制文件

在主机上调用二进制文件。该二进制文件通常使用扩展元数据中的 [host 部分](../../architecture/metadata.md#host-section) 随扩展一起提供。请注意，扩展以用户访问权限运行，此 API 不受扩展元数据中 [host 部分](../../architecture/metadata.md#host-section) 所列二进制文件的限制（某些扩展可能在用户交互期间安装软件，并调用新安装的二进制文件，即使这些二进制文件未在扩展元数据中列出）。

例如，在主机中执行随附的二进制文件 `kubectl -h` 命令：

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

只要 `kubectl` 二进制文件作为扩展的一部分提供，你就可以在主机中生成 `kubectl -h` 命令并获取输出流：

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

你可以流式传输在后端容器或主机中执行的命令输出。

更多详情，请参阅 [Extension Host API 参考](/reference/api/extensions-sdk/ExtensionHost.md)

> 已弃用的扩展二进制文件调用
>
> 此方法已被弃用，并将在未来版本中移除。请使用上面指定的方法。

在主机中执行命令：

```typescript
window.ddClient.execHostCmd(`cliShippedOnHost xxx`).then((cmdResult: any) => {
  console.log(cmdResult);
});
```

流式传输在后端容器或主机中执行的命令输出：

```typescript
window.ddClient.spawnHostCmd(
  `cliShippedOnHost`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // 命令退出后，我们会获得状态码
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> [!NOTE]
> 
> 你不能使用此方法在单个 `exec()` 调用中链接命令（例如 `cmd1 $(cmd2)` 或在命令之间使用管道）。
>
> 如果需要将参数传递给下一个命令，你需要为每个命令调用 `exec()` 并解析结果。
