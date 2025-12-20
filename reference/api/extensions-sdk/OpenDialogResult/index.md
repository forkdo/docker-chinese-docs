# Interface: OpenDialogResult

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
