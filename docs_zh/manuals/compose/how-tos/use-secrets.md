---
title: 在 Docker Compose 中安全管理机密信息
linkTitle: Compose 中的机密信息
weight: 60
description: 了解如何在 Docker Compose 中安全管理运行时和构建时的机密信息。
keywords: secrets, compose, security, environment variables, docker secrets, secure Docker builds, sensitive data in containers
tags:
- Secrets
aliases:
- /compose/use-secrets/
---

机密信息（Secret）是指任何不应通过网络传输或以未加密形式存储在 Dockerfile 或应用程序源代码中的数据片段，例如密码、证书或 API 密钥。

{{% include "compose/secrets.md" %}}

环境变量通常对所有进程都可见，并且难以追踪访问情况。在调试错误时，它们也可能在不知情的情况下被打印到日志中。使用机密信息可以降低这些风险。

## 使用机密信息

机密信息以文件形式挂载到容器内的 `/run/secrets/<secret_name>` 路径下。

将机密信息注入容器需要两个步骤。首先，使用 Compose 文件中的[顶层 secrets 元素](/reference/compose-file/secrets.md)定义机密信息。接着，更新服务定义，使用 [secrets 属性](/reference/compose-file/services.md#secrets)引用它们所需的机密信息。Compose 基于每个服务授予对机密信息的访问权限。

与其他方法不同，这种方式允许通过标准的文件系统权限在服务容器内进行细粒度的访问控制。

## 示例

### 单个服务的机密信息注入

在以下示例中，`frontend` 服务被授予访问 `my_secret` 机密信息的权限。在容器中，`/run/secrets/my_secret` 被设置为文件 `./my_secret.txt` 的内容。

```yaml
services:
  myapp:
    image: myapp:latest
    secrets:
      - my_secret
secrets:
  my_secret:
    file: ./my_secret.txt
```

### 多服务机密信息共享与密码管理

```yaml
services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password


secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:
```
在上述高级示例中：

- 每个服务下的 `secrets` 属性定义了要注入到特定容器中的机密信息。
- 顶层的 `secrets` 部分定义了变量 `db_password` 和 `db_root_password`，并提供了填充其值的 `file`。
- 部署每个容器时，Docker 会在 `/run/secrets/<secret_name>` 下创建一个绑定挂载，其中包含它们的特定值。

> [!NOTE]
>
> 此处演示的 `_FILE` 环境变量是一些镜像（包括 Docker 官方镜像，如 [mysql](https://hub.docker.com/_/mysql) 和 [postgres](https://hub.docker.com/_/postgres)）使用的约定。

### 构建机密信息

在以下示例中，`npm_token` 机密信息在构建时可用。其值取自 `NPM_TOKEN` 环境变量。

```yaml
services:
  myapp:
    build:
      secrets:
        - npm_token
      context: .

secrets:
  npm_token:
    environment: NPM_TOKEN
```

## 资源

- [Secrets 顶层元素](/reference/compose-file/secrets.md)
- [服务顶层元素的 Secrets 属性](/reference/compose-file/services.md#secrets)
- [构建机密信息](https://docs.docker.com/build/building/secrets/)