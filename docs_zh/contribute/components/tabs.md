---
description: Docker 文档中使用的组件和格式示例
title: 标签页 (Tabs)
toc_max: 3
---

标签页组件由两个短代码组成：

- `{{</* tabs */>}}`
- `{{</* tab name="name of the tab" */>}}`

`{{</* tabs */>}}` 短代码是一个父级组件，用于包裹多个 `tab`。
每个 `{{</* tab */>}}` 都使用 `name` 属性来指定名称。

您可以选择为 `tabs` 包装器指定一个 `group` 属性，以指示该标签页部分应属于某个标签页组。请参阅 [组 (Groups)](#groups)。

## 示例

{{< tabs >}}
{{< tab name="JavaScript">}}

```js
console.log("hello world")
```

{{< /tab >}}
{{< tab name="Go">}}

```go
fmt.Println("hello world")
```

{{< /tab >}}
{{< /tabs >}}

## 标记

````markdown
{{</* tabs */>}}
{{</* tab name="JavaScript" */>}}

```js
console.log("hello world")
```

{{</* /tab */>}}
{{</* tab name="Go" */>}}

```go
fmt.Println("hello world")
```

{{</* /tab */>}}
{{</* /tabs */>}}
````

## 组

您可以选择在 `tabs` 短代码上指定一个标签页组。
这样做将同步属于同一组的所有标签页的标签选择。

### 标签页组示例

以下示例显示了属于同一组的两个标签页部分。

{{< tabs group="code" >}}
{{< tab name="JavaScript">}}

```js
console.log("hello world")
```

{{< /tab >}}
{{< tab name="Go">}}

```go
fmt.Println("hello world")
```

{{< /tab >}}
{{< /tabs >}}

{{< tabs group="code" >}}
{{< tab name="JavaScript">}}

```js
const res = await fetch("/users/1")
```

{{< /tab >}}
{{< tab name="Go">}}

```go
resp, err := http.Get("/users/1")
```

{{< /tab >}}
{{< /tabs >}}