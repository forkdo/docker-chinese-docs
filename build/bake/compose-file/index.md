# 从 Compose 文件使用 Bake 构建


Bake 支持 [Compose 文件格式](/reference/compose-file/_index.md)，
可解析 Compose 文件并将每个服务转换为一个 [目标](reference.md#target)。

```yaml
# compose.yaml
services:
  webapp-dev:
    build: &build-dev
      dockerfile: Dockerfile.webapp
      tags:
        - docker.io/username/webapp:latest
      cache_from:
        - docker.io/username/webapp:cache
      cache_to:
        - docker.io/username/webapp:cache

  webapp-release:
    build:
      <<: *build-dev
      x-bake:
        platforms:
          - linux/amd64
          - linux/arm64

  db:
    image: docker.io/username/db
    build:
      dockerfile: Dockerfile.db
```

```console
$ docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": ["db", "webapp-dev", "webapp-release"]
    }
  },
  "target": {
    "db": {
      "context": ".",
      "dockerfile": "Dockerfile.db",
      "tags": ["docker.io/username/db"]
    },
    "webapp-dev": {
      "context": ".",
      "dockerfile": "Dockerfile.webapp",
      "tags": ["docker.io/username/webapp:latest"],
      "cache-from": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ],
      "cache-to": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ]
    },
    "webapp-release": {
      "context": ".",
      "dockerfile": "Dockerfile.webapp",
      "tags": ["docker.io/username/webapp:latest"],
      "cache-from": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ],
      "cache-to": [
        {
          "ref": "docker.io/username/webapp:cache",
          "type": "registry"
        }
      ],
      "platforms": ["linux/amd64", "linux/arm64"]
    }
  }
}
```

与 HCL 格式相比，Compose 格式有一些限制：

- 不支持指定变量或全局作用域属性
- 不支持 `inherits` 服务字段，但你可以使用 [YAML anchors](/reference/compose-file/fragments.md)
  引用其他服务，如前面使用 `&build-dev` 的示例所示。

## `.env` 文件

你可以在名为 `.env` 的环境文件中声明默认环境变量。该文件将从执行命令的当前工作目录加载，
并应用到通过 `-f` 传递的 Compose 定义中。

```yaml
# compose.yaml
services:
  webapp:
    image: docker.io/username/webapp:${TAG:-v1.0.0}
    build:
      dockerfile: Dockerfile
```

```sh
# .env
TAG=v1.1.0
```

```console
$ docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["docker.io/username/webapp:v1.1.0"]
    }
  }
}
```

> [!NOTE]
>
> 系统环境变量优先于 `.env` 文件中的环境变量。

## 使用 `x-bake` 的扩展字段

在 Compose 规范中某些字段不可用时，你可以使用 [特殊扩展](/reference/compose-file/extension.md) 字段
`x-bake` 在你的 Compose 文件中来求值额外的字段：

```yaml
# compose.yaml
services:
  addon:
    image: ct-addon:bar
    build:
      context: .
      dockerfile: ./Dockerfile
      args:
        CT_ECR: foo
        CT_TAG: bar
      x-bake:
        tags:
          - ct-addon:foo
          - ct-addon:alp
        platforms:
          - linux/amd64
          - linux/arm64
        cache-from:
          - user/app:cache
          - type=local,src=path/to/cache
        cache-to:
          - type=local,dest=path/to/cache
        pull: true

  aws:
    image: ct-fake-aws:bar
    build:
      dockerfile: ./aws.Dockerfile
      args:
        CT_ECR: foo
        CT_TAG: bar
      x-bake:
        secret:
          - id=mysecret,src=./secret
          - id=mysecret2,src=./secret2
        platforms: linux/arm64
        output: type=docker
        no-cache: true
```

```console
$ docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": ["addon", "aws"]
    }
  },
  "target": {
    "addon": {
      "context": ".",
      "dockerfile": "./Dockerfile",
      "args": {
        "CT_ECR": "foo",
        "CT_TAG": "bar"
      },
      "tags": ["ct-addon:foo", "ct-addon:alp"],
      "cache-from": [
        {
          "ref": "user/app:cache",
          "type": "registry"
        },
        {
          "src": "path/to/cache",
          "type": "local"
        }
      ],
      "cache-to": [
        {
          "dest": "path/to/cache",
          "type": "local"
        }
      ],
      "platforms": ["linux/amd64", "linux/arm64"],
      "pull": true
    },
    "aws": {
      "context": ".",
      "dockerfile": "./aws.Dockerfile",
      "args": {
        "CT_ECR": "foo",
        "CT_TAG": "bar"
      },
      "tags": ["ct-fake-aws:bar"],
      "secret": [
        {
          "id": "mysecret",
          "src": "./secret"
        },
        {
          "id": "mysecret2",
          "src": "./secret2"
        }
      ],
      "platforms": ["linux/arm64"],
      "output": [
        {
          "type": "docker"
        }
      ],
      "no-cache": true
    }
  }
}
```

`x-bake` 的有效字段完整列表：

- `cache-from`
- `cache-to`
- `contexts`
- `no-cache`
- `no-cache-filter`
- `output`
- `platforms`
- `pull`
- `secret`
- `ssh`
- `tags`

