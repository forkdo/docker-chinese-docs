---
title: 'Interface: ExecResultV0'
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
- /desktop/extensions-sdk/dev/api/reference/interfaces/ExecResultV0/
- /extensions/extensions-sdk/dev/api/reference/interfaces/ExecResultV0/
---

## 属性

### cmd

• `Optional` `Readonly` **cmd**: `string`

___

### killed

• `Optional` `Readonly` **killed**: `boolean`

___

### signal

• `Optional` `Readonly` **signal**: `string`

___

### code

• `Optional` `Readonly` **code**: `number`

___

### stdout

• `Readonly` **stdout**: `string`

___

### stderr

• `Readonly` **stderr**: `string`

## 方法

### lines

▸ **lines**(): `string`[]

拆分输出行。

#### 返回值

`string`[]

行列表。

___

### parseJsonLines

▸ **parseJsonLines**(): `any`[]

将每行输出解析为 JSON 对象。

#### 返回值

`any`[]

行列表，其中每行都是一个 JSON 对象。

___

### parseJsonObject

▸ **parseJsonObject**(): `any`

解析格式良好的 JSON 输出。

#### 返回值

`any`

JSON 对象。