---
title: Compose 开发规范
description: 了解 Compose 开发规范
keywords: compose, compose 规范, compose 文件参考, compose develop 规范
aliases:
 - /compose/compose-file/develop/
weight: 150
---

> [!NOTE] 
>
> Develop 是 Compose 规范的可选部分。Docker Compose 2.22.0 及更高版本支持。

{{% include "compose/develop.md" %}}

本文档定义了 Compose 如何高效地辅助您开发，并说明了 Compose 设定的开发约束和工作流。只有部分 Compose 服务需要 `develop` 子节。

## 示例

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

`develop` 子节定义了 Compose 在开发过程中应用的配置选项，以优化工作流并辅助您高效开发服务。只有部分 Compose 服务需要 `develop` 子节。

### `watch`

`watch` 属性定义了一组规则，用于控制当本地文件发生更改时自动更新服务的行为。`watch` 是一个序列，序列中的每个条目都定义了一条规则，Compose 将根据这些规则监控源代码的变更。更多信息请参阅 [使用 Compose Watch](/manuals/compose/how-tos/file-watch.md)。

#### `action`

`action` 定义了检测到变更时要执行的操作。当 `action` 设置为：

- `rebuild`：Compose 基于 `build` 部分重建服务镜像，并使用更新后的镜像重新创建服务。
- `restart`：Compose 重启服务容器。Docker Compose 2.32.0 及更高版本支持。
- `sync`：Compose 保持现有服务容器运行，但根据 `target` 属性将源文件与容器内容同步。
- `sync+restart`：Compose 根据 `target` 属性将源文件与容器内容同步，然后重启容器。Docker Compose 2.23.0 及更高版本支持。
- `sync+exec`：Compose 根据 `target` 属性将源文件与容器内容同步，然后在容器内执行命令。Docker Compose 2.32.0 及更高版本支持。

#### `exec`

{{< summary-bar feature_name="Compose exec" >}}

`exec` 仅在 `action` 设置为 `sync+exec` 时生效。与 [服务钩子](services.md#post_start) 类似，`exec` 用于定义容器启动后要运行的命令。

- `command`：指定容器启动后要运行的命令。此属性为必需项，您可以使用 shell 形式或 exec 形式。
- `user`：运行命令的用户。如未设置，命令将以与主服务命令相同的用户身份运行。
- `privileged`：允许命令以特权模式运行。
- `working_dir`：运行命令的工作目录。如未设置，命令将在与主服务命令相同的工作目录中运行。
- `environment`：设置运行命令所需的环境变量。虽然命令会继承为服务主命令定义的环境变量，但此部分允许您添加新变量或覆盖现有变量。

```yaml
services:
  frontend:
    image: ...
    develop:
      watch: 
        # 同步内容后执行命令以重新加载服务，不中断服务
        - path: ./etc/config
          action: sync+exec
          target: /etc/config/
          exec:
            command: app reload
```

#### `ignore`

`ignore` 属性用于定义一组路径模式，这些路径将被忽略。任何与模式匹配的更新文件，或属于与模式匹配的文件夹的文件，都不会触发服务重新创建。语法与 `.dockerignore` 文件相同：

- `*` 匹配文件名中的 0 个或多个字符。
- `?` 匹配文件名中的单个字符。
- `*/*` 匹配两个嵌套文件夹，文件夹名任意。
- `**` 匹配任意数量的嵌套文件夹。

如果构建上下文包含 `.dockerignore` 文件，该文件中的模式将作为 `ignores` 文件的隐式内容加载，Compose 模型中设置的值将被追加。

#### `include`

在某些情况下，选择要监视的文件比使用 `ignore` 声明不应监视的文件更容易。

`include` 属性用于定义一个或一组路径模式，这些路径将被考虑用于监视。只有匹配这些模式的文件才会在应用监视规则时被考虑。语法与 `ignore` 相同。

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
> 在许多情况下，`include` 模式以通配符 (`*`) 字符开头。这在 YAML 语法中有特殊含义，用于定义 [别名节点](https://yaml.org/spec/1.2.2/#alias-nodes)，因此您必须用引号包装模式表达式。

#### `initial_sync`

使用 `sync+x` 操作时，确保在新的监视会话开始时容器内的文件是最新的可能会很有用。

`initial_sync` 属性指示 Compose 运行时，如果服务的容器已存在，则检查 `path` 属性中的文件是否与服务容器内的文件同步。

#### `path`

`path` 属性定义了要监视的源代码路径（相对于项目目录），以监控变更。路径内任何文件的更新（不匹配任何 `ignore` 规则）都会触发配置的操作。

#### `target`

`target` 属性仅在 `action` 配置为 `sync` 时适用。当 `path` 中的文件发生变更时，这些文件将与容器文件系统同步，以确保后者始终运行最新内容。