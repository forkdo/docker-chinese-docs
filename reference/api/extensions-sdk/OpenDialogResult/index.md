---
title: Interface: OpenDialogResult
url: /reference/api/extensions-sdk/OpenDialogResult/
parent:
  title: 扩展 API 参考
  url: /reference/api/extensions-sdk/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: 扩展 API 参考
    url: /reference/api/extensions-sdk/
  - title: Interface: OpenDialogResult
    url: /reference/api/extensions-sdk/OpenDialogResult/
next:
  title: Interface: ExtensionHost
  url: /reference/api/extensions-sdk/ExtensionHost/
prev:
  title: Interface: Toast
  url: /reference/api/extensions-sdk/Toast/
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

仅限 macOS。一个与 `filePaths` 数组匹配的、包含安全作用域书签数据的 `base64` 编码字符串数组。必须启用 `securityScopedBookmarks` 才能填充此字段。
