# 接口：Docker

**`自版本`**

0.2.0

## 属性 (Properties)

### cli

• `Readonly` **cli**: [`DockerCommand`](DockerCommand.md)

您也可以直接执行 Docker 二进制文件。

```typescript
const output = await ddClient.docker.cli.exec("volume", [
  "ls",
  "--filter",
  "dangling=true"
]);
```

输出：

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

为方便起见，命令结果对象还包含根据输出格式轻松解析的方法。请参阅 [ExecResult](ExecResult.md)。

---

流式传输执行 Docker 命令的输出结果。
当命令输出过长，或者您需要以流的形式获取输出时，此方法非常有用。

```typescript
await ddClient.docker.cli.exec("logs", ["-f", "..."], {
  stream: {
    onOutput(data): void {
        // 由于可能同时接收到 `stdout` 和 `stderr`，我们将它们包装在 JSON 对象中
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

## 方法 (Methods)

### listContainers

▸ **listContainers**(`options?`): `Promise`<`unknown`\>

获取正在运行的容器列表（与 `docker ps` 相同）。

默认情况下，此方法不会列出已停止的容器。
您可以使用选项 `{"all": true}` 来列出所有正在运行和已停止的容器。

```typescript
const containers = await ddClient.docker.listContainers();
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options?` | `any` | （可选）。一个类似 `{ "all": true, "limit": 10, "size": true, "filters": JSON.stringify({ status: ["exited"] }), }` 的 JSON 对象。有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/reference/api/engine/version/v1.52/#operation/ContainerList)。 |

#### 返回值

`Promise`<`unknown`\>

---

### listImages

▸ **listImages**(`options?`): `Promise`<`unknown`\>

获取本地容器镜像列表

```typescript
const images = await ddClient.docker.listImages();
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `options?` | `any` | （可选）。一个类似 `{ "all": true, "filters": JSON.stringify({ dangling: ["true"] }), "digests": true * }` 的 JSON 对象。有关不同属性的更多信息，请参阅 [Docker API 端点文档](https://docs.docker.com/reference/api/engine/version/v1.52/#tag/Image)。 |

#### 返回值

`Promise`<`unknown`\>
