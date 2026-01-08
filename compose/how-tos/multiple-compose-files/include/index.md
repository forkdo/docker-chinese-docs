# Include





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose <a class="link" href="https://github.com/docker/compose/releases/tag/v2.20.3" rel="noopener">2.20.3</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>





使用 `include`，您可以将单独的 `compose.yaml` 文件直接合并到当前的 `compose.yaml` 文件中。这样可以轻松地将复杂应用程序模块化到子 Compose 文件中，从而使应用程序配置变得更简单、更明确。

[`include` 顶级元素](/reference/compose-file/include.md) 有助于将负责代码的工程团队直接反映在配置文件的组织结构中。它还解决了 [`extends`](extends.md) 和 [merge](merge.md) 所带来的相对路径问题。

`include` 列表中的每个路径都会作为独立的 Compose 应用模型加载，拥有自己的项目目录，以便解析相对路径。

一旦包含的 Compose 应用加载完成，所有资源都会被复制到当前 Compose 应用模型中。

> [!NOTE]
>
> `include` 会递归应用，因此如果一个包含的 Compose 文件声明了自己的 `include` 部分，这些文件也会被包含进来。

## 示例

```yaml
include:
  - my-compose-include.yaml  # 包含 serviceB 的声明
services:
  serviceA:
    build: .
    depends_on:
      - serviceB # 直接使用 serviceB，就像它在当前 Compose 文件中声明一样
```

`my-compose-include.yaml` 管理着 `serviceB`，其中包含一些副本、用于检查数据的 Web UI、隔离的网络、用于数据持久化的卷等。依赖 `serviceB` 的应用程序不需要了解这些基础设施细节，而是将 Compose 文件作为可依赖的构建块来使用。

这意味着管理 `serviceB` 的团队可以重构自己的数据库组件，引入额外的服务，而不会影响任何依赖团队。这也意味着依赖团队在运行每个 Compose 命令时不需要添加额外的标志。

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

如果 `include` 中的任何资源与包含的 Compose 文件中的资源冲突，Compose 会报告错误。此规则可防止与包含的 Compose 文件作者定义的资源发生意外冲突。但是，在某些情况下，你可能希望自定义包含的模型。这可以通过在 include 指令中添加覆盖文件来实现：

```yaml
include:
  - path : 
      - third-party/compose.yaml
      - override.yaml  # 对第三方模型的本地覆盖
```

此方法的主要限制是，你需要为每个 include 维护一个专用的覆盖文件。对于具有多个 include 的复杂项目，这会导致许多 Compose 文件。

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

结合使用，这使你能够受益于第三方可重用组件，并根据需要调整 Compose 模型。

## 参考信息

[`include` top-level element](/reference/compose-file/include.md)
