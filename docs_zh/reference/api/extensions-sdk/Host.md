---
title: "接口: Host"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases: 
 - /desktop/extensions-sdk/dev/api/reference/interfaces/Host/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/Host/
---

**`Since`**

0.2.0

## 方法

### openExternal

▸ **openExternal**(`url`): `void`

使用系统默认浏览器打开外部 URL。

**`Since`**

0.2.0

```typescript
ddClient.host.openExternal("https://docker.com");
```

#### 参数

| 名称 | 类型 | 描述 |
| :------ | :------ | :------ |
| `url` | `string` | 浏览器将打开的 URL（必须包含协议 `http` 或 `https`）。 |

#### 返回值

`void`

## 属性

### platform

• **platform**: `string`

返回标识操作系统平台的字符串。参见 https://nodejs.org/api/os.html#osplatform

**`Since`**

0.2.2

___

### arch

• **arch**: `string`

返回操作系统 CPU 架构。参见 https://nodejs.org/api/os.html#osarch

**`Since`**

0.2.2

___

### hostname

• **hostname**: `string`

返回操作系统的主机名。参见 https://nodejs.org/api/os.html#oshostname

**`Since`**

0.2.2