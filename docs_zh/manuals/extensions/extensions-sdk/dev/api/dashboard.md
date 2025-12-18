---
title: 仪表板
description: Docker 扩展 API
keywords: Docker, 扩展, sdk, API
aliases:
 - /desktop/extensions-sdk/dev/api/dashboard/
---

## 用户通知

Toasts 会向用户提供简短的通知。它们会临时显示，不应中断用户体验，也不需要用户输入即可消失。

### success

▸ **success**(`msg`): `void`

用于显示成功类型的消息提示。

```typescript
ddClient.desktopUI.toast.success("message");
```

### warning

▸ **warning**(`msg`): `void`

用于显示警告类型的消息提示。

```typescript
ddClient.desktopUI.toast.warning("message");
```

### error

▸ **error**(`msg`): `void`

用于显示错误类型的消息提示。

```typescript
ddClient.desktopUI.toast.error("message");
```

有关可用方法参数和返回类型的更多详细信息，请参阅 [Toast API 参考](/reference/api/extensions-sdk/Toast.md)。

> 已弃用的用户通知
>
> 这些方法已弃用，将在未来版本中移除。请使用上面指定的方法。

```typescript
window.ddClient.toastSuccess("message");
window.ddClient.toastWarning("message");
window.ddClient.toastError("message");
```

## 打开文件选择对话框

此函数会打开一个文件选择对话框，要求用户选择文件或文件夹。

▸ **showOpenDialog**(`dialogProperties`): `Promise`<[`OpenDialogResult`](/reference/api/extensions-sdk/OpenDialogResult.md)\>:

`dialogProperties` 参数是一个传递给 Electron 的标志列表，用于自定义对话框的行为。例如，可以传递 `multiSelections` 以允许用户选择多个文件。请参阅 [Electron 文档](https://www.electronjs.org/docs/latest/api/dialog) 了解完整列表。

```typescript
const result = await ddClient.desktopUI.dialog.showOpenDialog({
  properties: ["openDirectory"],
});
if (!result.canceled) {
  console.log(result.paths);
}
```

## 打开 URL

此函数使用系统默认浏览器打开外部 URL。

▸ **openExternal**(`url`): `void`

```typescript
ddClient.host.openExternal("https://docker.com");
```

> URL 必须使用 `http` 或 `https` 协议。

有关可用方法参数和返回类型的更多详细信息，请参阅 [Desktop host API 参考](/reference/api/extensions-sdk/Host.md)。

> 已弃用的用户通知
>
> 此方法已弃用，将在未来版本中移除。请使用上面指定的方法。

```typescript
window.ddClient.openExternal("https://docker.com");
```

## 导航到仪表板路由

从您的扩展中，您还可以 [导航](dashboard-routes-navigation.md) 到 Docker Desktop 仪表板的其他部分。