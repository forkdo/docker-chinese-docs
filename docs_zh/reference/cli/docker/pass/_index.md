---
datafolder: secrets-engine
datafile: docker_pass
title: Docker Pass
layout: cli
---

{{< summary-bar feature_name="Docker Pass" >}}

# Docker Pass

Docker Pass 是一个 Docker 凭据助手，它使用 Vault 的 Docker 凭据引擎来管理 Docker 注册表的认证信息。

## 工作原理

Docker Pass 通过与 Vault 的 Docker 凭据引擎交互来工作。它会检索用于 Docker 登录的临时认证令牌。

当您运行 `docker login` 时，Docker 会调用凭据助手。凭据助手会向 Vault 请求认证令牌，然后将该令牌返回给 Docker。

## 安装

### 从源码构建

```bash
git clone https://github.com/hashicorp/vault
cd vault
make docker-pass
```

这将在 `bin/` 目录下生成 `docker-pass` 二进制文件。

### 从发布版下载

从 [GitHub 发布页面](https://github.com/hashicorp/vault/releases) 下载适用于您操作系统的预编译二进制文件。

## 配置

### 1. 配置 Docker 凭据引擎

首先，在 Vault 中启用并配置 Docker 凭据引擎：

```bash
# 启用 Docker 凭据引擎
vault secrets enable docker

# 配置 Docker 注册表
vault write docker/registry/my-registry \
    url=https://index.docker.io/v1/ \
    username=myuser \
    password=mypassword
```

### 2. 配置 Docker Pass

创建配置文件 `~/.docker/docker-pass.json`：

```json
{
  "vault_addr": "http://127.0.0.1:8200",
  "vault_token": "s.XXXXXXXXXXXXXXXXXXXXXXXX",
  "registry": "my-registry"
}
```

或者使用环境变量：

```bash
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=s.XXXXXXXXXXXXXXXXXXXXXXXX
export DOCKER_PASS_REGISTRY=my-registry
```

### 3. 配置 Docker

编辑 `~/.docker/config.json` 并添加凭据助手：

```json
{
  "credsStore": "docker-pass"
}
```

或者对于特定注册表：

```json
{
  "credHelpers": {
    "my-registry": "docker-pass"
  }
}
```

## 使用

### 登录 Docker 注册表

```bash
docker login my-registry
```

Docker Pass 会自动从 Vault 获取认证令牌并将其用于登录。

### 拉取镜像

```bash
docker pull my-registry/my-image:latest
```

### 推送镜像

```bash
docker tag my-image:latest my-registry/my-image:latest
docker push my-registry/my-image:latest
```

## 故障排除

### 常见问题

**问题：** `docker login` 失败，提示 "credentials not found"

**解决方案：** 确保 `~/.docker/config.json` 中的 `credsStore` 或 `credHelpers` 配置正确。

**问题：** 无法连接到 Vault

**解决方案：** 检查 `VAULT_ADDR` 和 `VAULT_TOKEN` 环境变量或配置文件是否正确。

**问题：** 权限不足

**解决方案：** 确保您的 Vault token 有权限访问 Docker 凭据引擎。

## API 参考

Docker Pass 使用以下 Vault API 端点：

- `GET /v1/docker/creds/:registry` - 获取指定注册表的认证凭据

## 安全考虑

- 将 Vault token 存储在安全的位置
- 使用具有最小权限的 Vault token
- 定期轮换 Vault token 和 Docker 凭据
- 考虑使用 Vault 的认证方法（如 AppRole、Kubernetes）而不是静态 token

## 选项

| 参数 | 描述 | 环境变量 | 配置文件 |
|------|------|----------|----------|
| `vault_addr` | Vault 服务器地址 | `VAULT_ADDR` | `vault_addr` |
| `vault_token` | Vault 认证令牌 | `VAULT_TOKEN` | `vault_token` |
| `registry` | Docker 注册表名称 | `DOCKER_PASS_REGISTRY` | `registry` |
| `vault_namespace` | Vault 命名空间 | `VAULT_NAMESPACE` | `vault_namespace` |

## 故障排除

如果遇到问题，请检查：

1. Vault 服务是否正在运行
2. Docker 凭据引擎是否已启用
3. 您的 Vault token 是否有效且具有必要的权限
4. 配置文件格式是否正确
5. Docker 是否配置为使用 docker-pass 凭据助手

## 更多信息

- [Vault Docker 凭据引擎文档](https://developer.hashicorp.com/vault/docs/secrets/docker)
- [Docker 凭据助手规范](https://github.com/docker/docker-credential-helpers)
- [GitHub 仓库](https://github.com/hashicorp/vault)