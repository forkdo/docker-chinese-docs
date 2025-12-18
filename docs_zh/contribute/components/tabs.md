---
description: Docker 文档中使用的组件和格式化示例
title: 标签页（Tabs）
toc_max: 3
---

标签页（tabs）组件由两个短代码组成：

- `{{</* tabs */>}}`
- `{{</* tab name="标签页名称" */>}}`

`{{</* tabs */>}}` 短代码是一个父级组件，用于包装多个 `tabs`。
每个 `{{</* tab */>}}` 通过 `name` 属性指定一个名称。

您还可以选择性地为 `tabs` 包装器指定一个 `group` 属性，以表明标签页部分应属于一组标签页。参见 [分组（Groups）](#分组)。

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

## 标记语法

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

## 分组

您可以在 `tabs` 短代码上选择性地指定一个标签页组。
这样做会同步属于同一组的所有标签页的选中状态。

### 标签页分组示例

以下示例展示了属于同一组的两个标签页部分。

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