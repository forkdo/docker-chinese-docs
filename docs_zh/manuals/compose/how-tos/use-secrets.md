---
title: 在 Docker Compose 中安全地管理密钥
linkTitle: Compose 中的密钥
weight: 60
description: 了解如何在 Docker Compose 中安全地管理运行时和构建时密钥。
keywords: 密钥, compose, 安全, 环境变量, docker 密钥, 安全的 Docker 构建, 容器中的敏感数据
tags: [Secrets]
aliases:
- /compose/use-secrets/
---

密钥是任何不应通过网络传输或在 Dockerfile 或应用程序源代码中未加密存储的数据，例如密码、证书或 API 密钥。

{{% include "compose/secrets.md" %}}

环境变量通常对所有进程都可用，跟踪访问权限可能很困难。在调试错误时，它们也可能被打印到日志中，而您并不知情。使用密钥可以减轻这些风险。

## 使用密钥

密钥作为文件挂载在容器内的 `/run/secrets/<secret_name>` 路径下。

将密钥注入容器是一个两步过程。首先，使用 [Compose 文件中的顶级 secrets 元素](/reference/compose-file/secrets.md) 定义密钥。然后，更新您的服务定义，使用 [secrets 属性](/reference/compose-file/services.md#secrets) 引用所需密钥。Compose 按服务授予密钥访问权限。

与其他方法不同，此方法允许通过标准文件系统权限在服务容器内进行细粒度访问控制。

## 示例

### 单服务密钥注入

在以下示例中，前端服务被授予访问 `my_secret` 密钥的权限。在容器中，`/run/secrets/my_secret` 被设置为文件 `./my_secret.txt` 的内容。

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

### 多服务密钥共享和密码管理

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
在上面的高级示例中：

- 每个服务下的 `secrets` 属性定义了您要注入到特定容器中的密钥。
- 顶级 `secrets` 部分定义了变量 `db_password` 和 `db_root_password`，并提供了填充其值的 `file`。
- 每个容器的部署意味着 Docker 在 `/run/secrets/<secret_name>` 下创建一个绑定挂载，包含其特定值。

> [!NOTE]
>
> 此处演示的 `_FILE` 环境变量是某些镜像（包括 Docker 官方镜像，如 [mysql](https://hub.docker.com/_/mysql) 和 [postgres](https://hub.docker.com/_/postgres)）使用的约定。

### 构建密钥

在以下示例中，`npm_token` 密钥在构建时可用。其值来自 `NPM_TOKEN` 环境变量。

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

- [Secrets 顶级元素](/reference/compose-file/secrets.md)
- [服务顶级元素的 secrets 属性](/reference/compose-file/services.md#secrets)
- [构建密钥](https://docs.docker.com/build/building/secrets/)