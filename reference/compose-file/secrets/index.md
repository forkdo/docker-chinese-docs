# Secrets

Secrets 是 [Configs](configs.md) 的一种变体，专注于敏感数据，并针对此用途有特定的约束。

服务只有在被 `services` 顶级元素内的 [`secrets` attribute](services.md#secrets) 显式授予时，才能访问 secrets。

顶级的 `secrets` 声明用于定义或引用授予给 Compose 应用中服务的敏感数据。secret 的来源是 `file` 或 `environment`。

- `file`: secret 通过指定路径的文件内容创建。
- `environment`: secret 通过宿主机上的环境变量的值创建。

## 示例 1

在应用部署时，`server-certificate` secret 通过将 `server.cert` 的内容注册为平台 secret，被创建为 `<project_name>_server-certificate`。

```yml
secrets:
  server-certificate:
    file: ./server.cert
```

## 示例 2

在应用部署时，`token` secret 通过将 `OAUTH_TOKEN` 环境变量的内容注册为平台 secret，被创建为 `<project_name>_token`。

```yml
secrets:
  token:
    environment: "OAUTH_TOKEN"
```

## 其他资源

更多信息，请参阅 [How to use secrets in Compose](/manuals/compose/how-tos/use-secrets.md)。
