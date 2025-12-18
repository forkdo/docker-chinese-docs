---
title: Docker
description: Docker 扩展 API
keywords: Docker, extensions, sdk, API
aliases: 
 - /desktop/extensions-sdk/dev/api/docker/
---

## Docker 对象

▸ **listContainers**(`options?`): `Promise`<`unknown`\>

获取容器列表：

```typescript
const containers = await ddClient.docker.listContainers();
```

▸ **listImages**(`options?`): `Promise`<`unknown`\>

获取本地容器镜像列表：

```typescript
const images = await ddClient.docker.listImages();
```

详细信息请参阅 [Docker API 参考文档](/reference/api/extensions-sdk/Docker.md)。

> 已弃用的 Docker 对象访问方式
>
> 以下方法已弃用，将在未来版本中移除。请使用上面指定的方法。

```typescript
const containers = await window.ddClient.listContainers();

const images = await window.ddClient.listImages();
```

## Docker 命令

扩展也可以直接执行 `docker` 命令行。

▸ **exec**(`cmd`, `args`): `Promise`<[`ExecResult`](/reference/api/extensions-sdk/ExecResult.md)\>

```typescript
const result = await ddClient.docker.cli.exec("info", [
  "--format",
  '"{{ json . }}"',
]);
```

结果包含执行命令的标准输出和标准错误：

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

在本例中，命令输出是 JSON。
为方便起见，命令结果对象还提供了以下方法来轻松解析结果：

- `result.lines(): string[]` 分割输出行。
- `result.parseJsonObject(): any` 解析格式良好的 JSON 输出。
- `result.parseJsonLines(): any[]` 将每行输出解析为 JSON 对象。

▸ **exec**(`cmd`, `args`, `options`): `void`

上面的命令将输出作为 Docker 命令执行的结果以流的形式返回。
如果你需要将输出作为流获取，或者命令输出太长，这会很有用。

```typescript
await ddClient.docker.cli.exec("logs", ["-f", "..."], {
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
    splitOutputLines: true,
  },
});
```

扩展创建的子进程会在你关闭 Docker Desktop 中的仪表板或退出扩展 UI 时自动被终止（`SIGTERM`）。
如有需要，你也可以使用 `exec(streamOptions)` 调用的结果来终止（`SIGTERM`）该进程。

```typescript
const logListener = await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    // ...
  },
});

// 监听日志结束后或开始新监听前，终止进程
logListener.close();
```

这种 `exec(streamOptions)` API 也可用于监听 docker 事件：

```typescript
await ddClient.docker.cli.exec(
  "events",
  ["--format", "{{ json . }}", "--filter", "container=my-container"],
  {
    stream: {
      onOutput(data) {
        if (data.stdout) {
          const event = JSON.parse(data.stdout);
          console.log(event);
        } else {
          console.log(data.stderr);
        }
      },
      onClose(exitCode) {
        console.log("onClose with exit code " + exitCode);
      },
      splitOutputLines: true,
    },
  }
);
```

> [!NOTE]
>
> 你不能使用此 API 在单个 `exec()` 调用中链接命令（比如 `docker kill $(docker ps -q)` 或在命令间使用管道）。
>
> 你需要为每个命令单独调用 `exec()`，并解析结果以将参数传递给下一个命令（如果需要）。

详细信息请参阅 [Exec API 参考文档](/reference/api/extensions-sdk/Exec.md)。

> 已弃用的 Docker 命令执行方式
>
> 此方法已弃用，将在未来版本中移除。请使用上面指定的方法。

```typescript
const output = await window.ddClient.execDockerCmd(
  "info",
  "--format",
  '"{{ json . }}"'
);

window.ddClient.spawnDockerCmd("logs", ["-f", "..."], (data, error) => {
  console.log(data.stdout);
});
```