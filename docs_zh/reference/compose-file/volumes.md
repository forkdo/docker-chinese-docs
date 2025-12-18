---
linkTitle: Volumes 
title: 在 Docker Compose 中定义和管理卷
description: 使用顶级 volumes 元素控制卷的声明方式以及服务间的共享。
keywords: compose, compose specification, volumes, compose file reference
aliases: 
 - /compose/compose-file/07-volumes/
weight: 40
---

{{% include "compose/volumes.md" %}}

要在多个服务之间使用卷，必须显式地通过 `services` 顶级元素中的 [volumes](services.md#volumes) 属性为每个服务授予访问权限。`volumes` 属性具有更精细控制的额外语法。

> [!TIP]
>
> 处理大型仓库或单体仓库，或者虚拟文件系统已无法与您的代码库同步扩展？Compose 现在利用 [同步文件共享](/manuals/desktop/features/synchronized-file-sharing.md) 功能，自动为绑定挂载创建文件共享。确保您已使用付费订阅登录 Docker，并在 Docker Desktop 设置中启用 **Access experimental features** 和 **Manage Synchronized file shares with Compose**。

## 示例

以下示例展示了一个双服务设置，其中数据库的数据目录作为卷（名为 `db-data`）与其他服务共享，以便定期备份。

```yml
services:
  backend:
    image: example/database
    volumes:
      - db-data:/etc/data

  backup:
    image: backup-service
    volumes:
      - db-data:/var/lib/backup/data

volumes:
  db-data:
```

`db-data` 卷被挂载到 backup 和 backend 服务的容器路径 `/var/lib/backup/data` 和 `/etc/data`。

运行 `docker compose up` 会创建卷（如果尚不存在）。否则，将使用现有卷，如果在 Compose 外部手动删除，则会重新创建。

## 属性

顶级 `volumes` 部分下的条目可以为空，此时它使用容器引擎创建卷的默认配置。或者，您可以使用以下键配置它：

### `driver`

指定应使用哪个卷驱动。如果驱动不可用，Compose 会返回错误且不部署应用程序。

```yml
volumes:
  db-data:
    driver: foobar
```

### `driver_opts`

`driver_opts` 指定要传递给此卷驱动的选项列表，作为键值对。选项取决于驱动。

```yml
volumes:
  example:
    driver_opts:
      type: "nfs"
      o: "addr=10.40.0.199,nolock,soft,rw"
      device: ":/docker/example"
```

### `external`

如果设置为 `true`：
 - `external` 指定此卷已在平台上存在，其生命周期由应用程序外部管理。Compose 随后不会创建卷，如果卷不存在则返回错误。
 - 除了 `name` 之外的所有其他属性都是无关的。如果 Compose 检测到任何其他属性，它会拒绝 Compose 文件作为无效。

在以下示例中，Compose 不会尝试创建名为 `{project_name}_db-data` 的卷，而是查找一个名为 `db-data` 的现有卷，并将其挂载到 `backend` 服务的容器中。

```yml
services:
  backend:
    image: example/database
    volumes:
      - db-data:/etc/data

volumes:
  db-data:
    external: true
```

### `labels`

`labels` 用于为卷添加元数据。您可以使用数组或字典。

建议使用反向 DNS 表示法，以防止您的标签与其他软件使用的标签冲突。

```yml
volumes:
  db-data:
    labels:
      com.example.description: "Database volume"
      com.example.department: "IT/Ops"
      com.example.label-with-empty-value: ""
```

```yml
volumes:
  db-data:
    labels:
      - "com.example.description=Database volume"
      - "com.example.department=IT/Ops"
      - "com.example.label-with-empty-value"
```

Compose 设置 `com.docker.compose.project` 和 `com.docker.compose.volume` 标签。

> [!NOTE]
>
> 此处定义的标签仅适用于命名卷。它们存储在卷资源上，可通过 `docker volume inspect` 查看。它们不适用于绑定挂载，也不会更改挂载语义。

### `name`

`name` 为卷设置自定义名称。名称字段可用于引用包含特殊字符的卷。名称按原样使用，不会使用栈名称进行作用域限定。

```yml
volumes:
  db-data:
    name: "my-app-data"
```

这使得可以将此查找名称作为 Compose 文件的参数，因此卷的模型 ID 是硬编码的，但平台上的实际卷 ID 在部署期间运行时设置。

例如，如果 `.env` 文件中包含 `DATABASE_VOLUME=my_volume_001`：

```yml
volumes:
  db-data:
    name: ${DATABASE_VOLUME}
```

运行 `docker compose up` 会使用名为 `my_volume_001` 的卷。

它也可以与 `external` 属性结合使用。这意味着用于在平台上查找实际卷的名称与在 Compose 文件中引用卷的名称分开设置：

```yml
volumes:
  db-data:
    external: true
    name: actual-name-of-volume
```