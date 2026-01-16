---
title: 接口：Host
url: /reference/api/extensions-sdk/Host/
parent:
  title: 扩展 API 参考
  url: /reference/api/extensions-sdk/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: 扩展 API 参考
    url: /reference/api/extensions-sdk/
  - title: 接口：Host
    url: /reference/api/extensions-sdk/Host/
next:
  title: 接口：ExtensionCli
  url: /reference/api/extensions-sdk/ExtensionCli/
prev:
  title: 接口：HttpService
  url: /reference/api/extensions-sdk/HttpService/
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
| `url` | `string` | 浏览器将打开的 URL（必须包含 `http` 或 `https` 协议）。 |

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
