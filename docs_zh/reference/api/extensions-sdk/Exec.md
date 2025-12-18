---
title: "接口: Exec"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases: 
 - /desktop/extensions-sdk/dev/api/reference/interfaces/Exec/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/Exec/
---

## 可调用

### Exec

▸ **Exec**(`cmd`, `args`, `options?`): `Promise`<[`ExecResult`](ExecResult.md)\>

执行一个命令。

**`Since`**

0.2.0

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `cmd` | `string` | 要执行的命令。 |
| `args` | `string`[] | 要执行命令的参数。 |
| `options?` | [`ExecOptions`](ExecOptions.md) | 选项列表。 |

#### 返回值

`Promise`<[`ExecResult`](ExecResult.md)\>

命令完成后解析的 Promise。

### Exec

▸ **Exec**(`cmd`, `args`, `options`): [`ExecProcess`](ExecProcess.md)

如果在 `options` 参数中指定了 `stream`，则会流式传输命令的结果。

如果命令的输出过长，或者需要无限期流式传输内容（例如容器日志），请指定 `stream`。

**`Since`**

0.2.2

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `cmd` | `string` | 要执行的命令。 |
| `args` | `string`[] | 要执行命令的参数。 |
| `options` | [`SpawnOptions`](SpawnOptions.md) | 选项列表。 |

#### 返回值

[`ExecProcess`](ExecProcess.md)

生成的进程。