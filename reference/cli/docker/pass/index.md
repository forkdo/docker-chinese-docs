# Docker Pass





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Beta
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M360-360H217q-18 0-26.5-16t2.5-31l338-488q8-11 20-15t24 1q12 5 19 16t5 24l-39 309h176q19 0 27 17t-4 32L388-66q-8 10-20.5 13T344-55q-11-5-17.5-16T322-95l38-265Z"/></svg></span>
            
          
            
          
            
          
            
          
            
          
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 4.54 and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



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

- [docker pass get](https://docs.docker.com/reference/cli/docker/pass/get/)

- [docker pass ls](https://docs.docker.com/reference/cli/docker/pass/ls/)

- [docker pass rm](https://docs.docker.com/reference/cli/docker/pass/rm/)

- [docker pass set](https://docs.docker.com/reference/cli/docker/pass/set/)

