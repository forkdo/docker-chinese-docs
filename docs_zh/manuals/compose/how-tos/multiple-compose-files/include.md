---
description: 如何使用 Docker Compose 的 include 顶级元素
keywords: compose, docker, include, compose file
title: Include
aliases:
- /compose/multiple-compose-files/include/
---

{{< summary-bar feature_name="Compose include" >}}

{{% include "compose/include.md" %}}

[`include` 顶级元素](/reference/compose-file/include.md) 有助于将负责代码的工程团队直接反映在配置文件的组织结构中。它还解决了 [`extends`](extends.md) 和 [merge](merge.md) 所带来的相对路径问题。

`include` 列表中的每个路径都会作为独立的 Compose 应用模型加载，拥有自己的项目目录，以便解析相对路径。

一旦包含的 Compose 应用加载完成，所有资源都会被复制到当前的 Compose 应用模型中。

> [!NOTE]
>
> `include` 会递归应用，因此如果一个包含的 Compose 文件声明了自己的 `include` 部分，那些文件也会被包含进来。

## 示例

```yaml
include:
  - my-compose-include.yaml  # 声明了 serviceB
services:
  serviceA:
    build: .
    depends_on:
      - serviceB # 直接使用 serviceB，就像它在当前 Compose 文件中声明一样
```

`my-compose-include.yaml` 管理着 `serviceB`，其中包含一些副本、用于检查数据的 Web UI、隔离的网络、用于数据持久化的卷等。依赖 `serviceB` 的应用不需要了解这些基础设施细节，而是将 Compose 文件作为可依赖的构建块来使用。

这意味着管理 `serviceB` 的团队可以重构自己的数据库组件，引入额外的服务，而不会影响任何依赖团队。这也意味着依赖团队不需要在每次运行 Compose 命令时都添加额外的标志。

```yaml
include:
  - oci://docker.io/username/my-compose-app:latest # 使用存储为 OCI 工件的 Compose 文件
services:
  serviceA:
    build: .
    depends_on:
      - serviceB 
```
`include` 允许你从远程源（如 OCI 工件或 Git 仓库）引用 Compose 文件。  
这里 `serviceB` 是在 Docker Hub 上存储的 Compose 文件中定义的。

## 在包含的 Compose 文件中使用覆盖

如果 `include` 中的任何资源与包含的 Compose 文件中的资源冲突，Compose 会报告错误。此规则防止与包含的 Compose 文件作者定义的资源发生意外冲突。但是，在某些情况下，你可能希望自定义包含的模型。这可以通过在 include 指令中添加覆盖文件来实现：

```yaml
include:
  - path : 
      - third-party/compose.yaml
      - override.yaml  # 第三方模型的本地覆盖
```

这种方法的主要限制是，你需要为每个 include 维护一个专用的覆盖文件。对于具有多个 include 的复杂项目，这会导致许多 Compose 文件。

另一种选择是使用 `compose.override.yaml` 文件。虽然当同一资源被声明时，使用 `include` 的文件会拒绝冲突，但全局 Compose 覆盖文件可以覆盖最终合并的模型，如下例所示：

主 `compose.yaml` 文件：
```yaml
include:
  - team-1/compose.yaml # 声明 service-1
  - team-2/compose.yaml # 声明 service-2
```

覆盖 `compose.override.yaml` 文件：
```yaml
services:
  service-1:
    # 覆盖包含的 service-1 以启用调试端口
    ports:
      - 2345:2345

  service-2:
    # 覆盖包含的 service-2 以使用包含测试数据的本地数据文件夹
    volumes:
      - ./data:/data
```

结合使用，这允许你受益于第三方可重用组件，并根据需要调整 Compose 模型。

## 参考信息

[`include` top-level element](/reference/compose-file/include.md)