---
title: "接口: RawExecResult"
description: Docker 扩展 API 参考
keywords: Docker, extensions, sdk, API, reference
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/RawExecResult/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/RawExecResult/
---

**`自版本`**

0.2.0

## 继承关系

- **`RawExecResult`**

  ↳ [`ExecResult`](ExecResult.md)

## 属性

### cmd

• `可选` `只读` **cmd**: `string`

___

### killed

• `可选` `只读` **killed**: `boolean`

___

### signal

• `可选` `只读` **signal**: `string`

___

### code

• `可选` `只读` **code**: `number`

___

### stdout

• `只读` **stdout**: `string`

___

### stderr

• `只读` **stderr**: `string`