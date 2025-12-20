# 使用 include 模块化 Compose 文件





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Compose 
    
  
  <a class="link" href="https://docs.docker.com/compose/releases/release-notes/#2200">2.20.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



您可以通过包含其他 Compose 文件来重用和模块化 Docker Compose 配置。这在以下情况下很有用：
- 您想要重用其他 Compose 文件。
- 您需要将应用程序模型的一部分提取到单独的 Compose 文件中，以便可以单独管理或与他人共享。
- 团队需要在更大的部署中，为其子域只需声明有限资源的情况下，维护一个具有必要复杂度的 Compose 文件。

`include` 顶级部分用于定义对另一个 Compose 应用程序或子域的依赖。
`include` 部分中列出的每个路径都会作为独立的 Compose 应用程序模型加载，并拥有自己的项目目录，以便解析相对路径。

一旦加载了包含的 Compose 应用程序，所有资源定义都会复制到当前的 Compose 应用程序模型中。如果资源名称冲突，Compose 会显示警告，但不会尝试合并它们。为了强制执行这一点，`include` 在用于定义 Compose 应用程序模型的 Compose 文件被解析和合并之后才进行求值，以便检测 Compose 文件之间的冲突。

`include` 是递归应用的，因此一个声明了自己的 `include` 部分的被包含 Compose 文件也会触发那些其他文件的包含。

任何从被包含的 Compose 文件引入的卷、网络或其他资源都可以被当前的 Compose 应用程序用于跨服务引用。例如：

```yaml
include:
  - my-compose-include.yaml  # 声明了 serviceB
services:
  serviceA:
    build: .
    depends_on:
      - serviceB # 直接使用 serviceB，就像它在这个 Compose 文件中声明的一样
```

Compose 还支持在 `include` 中使用插值变量。建议您[指定必需变量](interpolation.md)。例如：

```text
include:
  -${INCLUDE_PATH:?FOO}/compose.yaml
```

## 短语法

短语法只定义了其他 Compose 文件的路径。该文件以其父文件夹作为项目目录加载，并加载一个可选的 `.env` 文件，通过插值来定义任何变量的默认值。本地项目的环境可以覆盖这些值。

```yaml
include:
  - ../commons/compose.yaml
  - ../another_domain/compose.yaml

services:
  webapp:
    depends_on:
      - included-service # 由 another_domain 定义
```

在之前的示例中，`../commons/compose.yaml` 和 `../another_domain/compose.yaml` 都被作为独立的 Compose 项目加载。被 `include` 引用的 Compose 文件中的相对路径是相对于它们自己的 Compose 文件路径解析的，而不是基于本地项目的目录。变量使用同一文件夹中可选的 `.env` 文件中设置的值进行插值，并会被本地项目的环境覆盖。

## 长语法

长语法提供了对子项目解析的更多控制：

```yaml
include:
   - path: ../commons/compose.yaml
     project_directory: ..
     env_file: ../another/.env
```

### `path`

`path` 是必需的，它定义了要被解析并包含到本地 Compose 模型中的 Compose 文件的位置。

`path` 可以设置为：

- 字符串：当使用单个 Compose 文件时。
- 字符串列表：当需要将多个 Compose 文件[合并在一起](merge.md)来定义本地应用程序的 Compose 模型时。

```yaml
include:
   - path:
       - ../commons/compose.yaml
       - ./commons-override.yaml
```

### `project_directory`

`project_directory` 定义了一个基础路径，用于解析 Compose 文件中设置的相对路径。它默认为被包含的 Compose 文件所在的目录。

### `env_file`

`env_file` 定义了一个或多个环境文件，用于在解析 Compose 文件时定义插值变量的默认值。它默认为被解析的 Compose 文件的 `project_directory` 中的 `.env` 文件。

`env_file` 可以设置为字符串或字符串列表，当需要合并多个环境文件来定义项目环境时。

```yaml
include:
   - path: ../another/compose.yaml
     env_file:
       - ../another/.env
       - ../another/dev.env
```

本地项目的环境优先于 Compose 文件设置的值，因此本地项目可以覆盖这些值进行自定义。

## 其他资源

有关使用 `include` 的更多信息，请参阅[使用多个 Compose 文件](/manuals/compose/how-tos/multiple-compose-files/_index.md)
