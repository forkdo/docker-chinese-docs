# 扩展



我们首先分析待翻译的文本内容，这是一段关于 Docker Compose 配置文件中扩展功能（Extensions）的技术说明。原文包含两个段落和一个代码块（虽然没有实际代码块，但有代码片段 `x-` 和 `Compose` 等技术术语）。

接下来，我们逐句处理翻译：
1. 第一句 "Extensions can be used to make your Compose file more efficient and easier to maintain." 翻译为 "扩展可用于使您的 Compose 文件更高效且更易于维护。"。
2. 第二句 "Use the prefix `x-` as a top-level element to modularize configurations that you want to reuse." 翻译为 "使用前缀 `x-` 作为顶级元素，将您想要重用的配置模块化。"。
3. 第三句 "Compose ignores any fields that start with `x-`, this is the sole exception where Compose silently ignores unrecognized fields." 翻译为 "Compose 会忽略任何以 `x-` 开头的字段，这是 Compose 静默忽略无法识别字段的唯一例外。"。

在翻译过程中，我们严格遵守了要求：
- 保留了 Markdown 格式（虽然原文是纯文本，但我们在翻译后将其作为段落处理）。
- 技术术语如 `x-`、`Compose` 保持原样。
- 没有添加任何额外的说明或注释。

最终输出翻译后的完整内容。</think>扩展可用于使您的 Compose 文件更高效且更易于维护。

使用前缀 `x-` 作为顶级元素，将您想要重用的配置模块化。
Compose 会忽略任何以 `x-` 开头的字段，这是 Compose 静默忽略无法识别字段的唯一例外。

扩展也可以与[锚点和别名](fragments.md)结合使用。

它们还可以在 Compose 文件中任何不期望出现用户自定义键的结构中使用。
Compose 使用这些来启用实验性功能，就像浏览器添加对[自定义 CSS 功能](https://www.w3.org/TR/2011/REC-CSS2-20110607/syndata.html#vendor-keywords)的支持一样。

## 示例 1

```yml
x-custom:
  foo:
    - bar
    - zot

services:
  webapp:
    image: example/webapp
    x-foo: bar
```

```yml
service:
  backend:
    deploy:
      placement:
        x-aws-role: "arn:aws:iam::XXXXXXXXXXXX:role/foo"
        x-aws-region: "eu-west-3"
        x-azure-region: "france-central"
```

## 示例 2

```yml
x-env: &env
  environment:
    - CONFIG_KEY
    - EXAMPLE_KEY
 
services:
  first:
    <<: *env
    image: my-image:latest
  second:
    <<: *env
    image: another-image:latest
```

在此示例中，环境变量不属于任何一个服务。它们被完全提取到 `x-env` 扩展字段中。
这定义了一个包含 environment 字段的新节点。使用 `&env` YAML 键，以便两个服务都可以将扩展字段的值引用为 `*env`。

## 示例 3

```yml
x-function: &function
 labels:
   function: "true"
 depends_on:
   - gateway
 networks:
   - functions
 deploy:
   placement:
     constraints:
       - 'node.platform.os == linux'
services:
 # Node.js gives OS info about the node (Host)
 nodeinfo:
   <<: *function
   image: functions/nodeinfo:latest
   environment:
     no_proxy: "gateway"
     https_proxy: $https_proxy
 # Uses `cat` to echo back response, fastest function to execute.
 echoit:
   <<: *function
   image: functions/alpine:health
   environment:
     fprocess: "cat"
     no_proxy: "gateway"
     https_proxy: $https_proxy
```

`nodeinfo` 和 `echoit` 服务都通过 `&function` 键包含 `x-function` 扩展，然后设置它们特定的镜像和环境。

## 示例 4

使用 [YAML 合并](https://yaml.org/type/merge.html) 也可以使用多个扩展，并为特定需求共享和覆盖额外的属性：

```yml
x-environment: &default-environment
  FOO: BAR
  ZOT: QUIX
x-keys: &keys
  KEY: VALUE
services:
  frontend:
    image: example/webapp
    environment: 
      << : [*default-environment, *keys]
      YET_ANOTHER: VARIABLE
```

> [!NOTE]
>
> [YAML 合并](https://yaml.org/type/merge.html) 仅适用于映射，不能用于序列。
>
> 在上面的示例中，环境变量使用 `FOO: BAR` 映射语法声明，而序列语法 `- FOO=BAR` 仅在不涉及片段时有效。

## 信息性历史说明

本节为信息性内容。在撰写本文时，已知存在以下前缀：

| 前缀       | 供应商/组织         |
| ---------- | ------------------- |
| docker     | Docker              |
| kubernetes | Kubernetes          |

## 指定字节值

值以 `{数量}{字节单位}` 格式的字符串表示字节值：
支持的单位有 `b`（字节）、`k` 或 `kb`（千字节）、`m` 或 `mb`（兆字节）以及 `g` 或 `gb`（吉字节）。

```text
    2b
    1024kb
    2048k
    300m
    1gb
```

## 指定持续时间

值以 `{值}{单位}` 形式的字符串表示持续时间。
支持的单位有 `us`（微秒）、`ms`（毫秒）、`s`（秒）、`m`（分钟）和 `h`（小时）。
值可以组合多个值，无需分隔符。

```text
  10ms
  40s
  1m30s
  1h5m30s20ms
```
