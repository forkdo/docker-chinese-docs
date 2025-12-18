---
title: Secrets
description: 探索 secrets 顶级元素可以拥有的所有属性。
keywords: compose, compose specification, secrets, compose 文件参考
aliases:
 - /compose/compose-file/09-secrets/
weight: 60
---

Secrets 是 [Configs](configs.md) 的一种变体，专注于敏感数据，针对此用途具有特定约束。

服务只有在 `services` 顶级元素中的 [`secrets` 属性](services.md#secrets) 明确授予时，才能访问 secrets。

顶级 `secrets` 声明定义或引用您的 Compose 应用程序中的服务被授予的敏感数据。secret 的来源可以是 `file` 或 `environment`。

- `file`：通过在指定路径处的文件内容创建 secret。
- `environment`：通过主机上环境变量的值创建 secret。

## 示例 1

当应用程序部署时，通过将 `server.cert` 的内容注册为平台 secret，创建 `server-certificate` secret 为 `<project_name>_server-certificate`。

```yml
secrets:
  server-certificate:
    file: ./server.cert
```

## 示例 2

当应用程序部署时，通过将 `OAUTH_TOKEN` 环境变量的内容注册为平台 secret，创建 `token` secret 为 `<project_name>_token`。

```yml
secrets:
  token:
    environment: "OAUTH_TOKEN"
```

## 额外资源

更多信息，请参阅 [如何在 Compose 中使用 secrets](/manuals/compose/how-tos/use-secrets.md)。