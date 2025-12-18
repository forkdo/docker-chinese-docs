---
title: "Interface: OpenDialogResult"
description: Docker 扩展 API 参考
keywords: Docker, 扩展, sdk, API, 参考
aliases:
 - /desktop/extensions-sdk/dev/api/reference/interfaces/OpenDialogResult/
 - /extensions/extensions-sdk/dev/api/reference/interfaces/OpenDialogResult/
---

**`Since`**

0.2.3

## 属性

### canceled

• `Readonly` **canceled**: `boolean`

对话框是否被取消。

___

### filePaths

• `Readonly` **filePaths**: `string`[]

用户选择的文件路径数组。如果对话框被取消，这将是一个空数组。

___

### bookmarks

• `Optional` `Readonly` **bookmarks**: `string`[]

仅限 macOS。一个与 `filePaths` 数组对应的数组，包含经过 base64 编码的安全作用域书签数据字符串。必须启用 `securityScopedBookmarks` 才会填充此数组。