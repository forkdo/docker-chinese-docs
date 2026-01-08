---
title: Compose 开发规范
description: 了解 Compose 开发规范
keywords: compose, compose specification, compose file reference, compose develop specification
aliases:
- /compose/compose-file/develop/
weight: 150
---

> [!NOTE] 
>
> Develop 是 Compose 规范的一个可选部分。它在 Docker Compose 2.22.0 及更高版本中可用。

{{% include "compose/develop.md" %}}

本文档定义了 Compose 的行为方式，以高效地为您提供帮助，并定义了 Compose 设置的开发约束和工作流。只有 Compose 文件服务的一个子集可能需要 `develop` 小节。

## 示例说明

```yaml
services:
  frontend:
    image: example/webapp
    build: ./webapp
    develop:
      watch: 
        # 同步静态内容
        - path: ./webapp/html
          action: sync
          target: /var/www
          ignore:
            - node_modules/

  backend:
    image: example/backend
    build: ./backend
    develop:
      watch: 
        # 重建镜像并重新创建服务
        - path: ./backend/src
          action: rebuild
```

## 属性

`develop` 小节定义了 Compose 应用的配置选项，旨在通过优化的工作流在开发过程中为您提供协助。

### `watch`

`watch` 属性定义了一个规则列表，用于根据本地文件变化控制自动服务更新。`watch` 是一个序列，序列中的每个项目都定义了一条规则，Compose 将应用这些规则来监视源代码的更改。更多信息，请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

#### `action`

`action` 定义检测到更改时要采取的操作。如果 `action` 设置为：

- `rebuild`：Compose 根据 `build` 部分重建服务镜像，并使用更新后的镜像重新创建服务。
- `restart`：Compose 重新启动服务容器。在 Docker Compose 2.32.0 及更高版本中可用。
- `sync`：Compose 保持现有服务容器运行，但根据 `target` 属性将源文件与容器内容同步。
- `sync+restart`：Compose 根据 `target` 属性将源文件与容器内容同步，然后重新启动容器。在 Docker Compose 2.23.0 及更高版本中可用。
- `sync+exec`：Compose 根据 `target` 属性将源文件与容器内容同步，然后在容器内执行命令。在 Docker Compose 2.32.0 及更高版本中可用。

#### `exec`

{{< summary-bar feature_name="Compose exec" >}}

`exec` 仅在 `action` 设置为 `sync+exec` 时相关。与 [服务钩子](services.md#post_start) 类似，`exec` 用于定义容器启动后要在容器内运行的命令。

- `command`：指定容器启动后要运行的命令。此属性是必需的，您可以选择使用 shell 形式或 exec 形式。
- `user`：运行命令的用户。如果未设置，命令将以与主服务命令相同的用户运行。
- `privileged`：允许命令以特权访问运行。
- `working_dir`：运行命令的工作目录。如果未设置，则在与主服务命令相同的工作目录中运行。
- `environment`：设置运行命令的环境变量。虽然该命令继承了为服务主命令定义的环境变量，但此部分允许您添加新变量或覆盖现有变量。

```yaml
services:
  frontend:
    image: ...
    develop:
      watch: 
        # 同步内容，然后运行命令以无中断地重新加载服务
        - path: ./etc/config
          action: sync+exec
          target: /etc/config/
          exec:
            command: app reload
```

#### `ignore`

`ignore` 属性用于定义要忽略的路径模式列表。任何匹配模式或属于匹配模式的文件夹的更新文件都不会触发服务的重新创建。语法与 `.dockerignore` 文件相同：

- `*` 匹配文件名中的 0 个或多个字符。
- `?` 匹配文件名中的单个字符。
- `*/*` 匹配两个具有任意名称的嵌套文件夹。
- `**` 匹配任意数量的嵌套文件夹。

如果构建上下文包含 `.dockerignore` 文件，则该文件中的模式将作为 `ignores` 文件的隐式内容加载，并附加 Compose 模型中设置的值。

#### `include`

有时，选择要监视的文件比使用 `ignore` 声明不应监视的文件更容易。

`include` 属性用于定义一个模式或模式列表，用于指定要考虑监视的路径。只有匹配这些模式的文件才会在应用监视规则时被考虑。语法与 `ignore` 相同。

```yaml
services:
  backend:
    image: example/backend
    develop:
      watch: 
        # 重建镜像并重新创建服务
        - path: ./src
          include: "*.go"  
          action: rebuild
```

> [!NOTE]
> 
> 在许多情况下，`include` 模式以通配符 (`*`) 字符开头。这在 YAML 语法中具有特殊含义，用于定义 [别名节点](https://yaml.org/spec/1.2.2/#alias-nodes)，因此您必须用引号包裹模式表达式。

#### `initial_sync`

使用 `sync+x` 操作时，确保在新的监视会话开始时容器内的文件是最新的会很有用。

`initial_sync` 属性指示 Compose 运行时，如果服务的容器已存在，则检查 `path` 属性中的文件是否已在服务容器中同步。

#### `path`

`path` 属性定义要监视更改的源代码路径（相对于项目目录）。对路径内任何文件的更新（如果不符合任何 `ignore` 规则）都会触发配置的操作。

#### `target`

`target` 属性仅在 `action` 配置为 `sync` 时适用。`path` 中发生更改的文件会与容器的文件系统同步，以便后者始终使用最新的内容运行。