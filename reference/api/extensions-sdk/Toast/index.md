# Interface: Toast

Toasts 提供对用户的简短通知。
它们会临时显示，不应中断用户体验。
同时，它们的消失也不需要用户输入。

**`Since`**

0.2.0

## 方法

### success

▸ **success**(`msg`): `void`

显示成功类型的消息提示。

```typescript
ddClient.desktopUI.toast.success("message");
```

#### 参数

| 名称 | 类型 | 说明 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在提示中显示的消息。 |

#### 返回值

`void`

___

### warning

▸ **warning**(`msg`): `void`

显示警告类型的消息提示。

```typescript
ddClient.desktopUI.toast.warning("message");
```

#### 参数

| 名称 | 类型 | 说明 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在警告中显示的消息。 |

#### 返回值

`void`

___

### error

▸ **error**(`msg`): `void`

显示错误类型的消息提示。

```typescript
ddClient.desktopUI.toast.error("message");
```

#### 参数

| 名称 | 类型 | 说明 |
| :------ | :------ | :------ |
| `msg` | `string` | 要在提示中显示的消息。 |

#### 返回值

`void`
