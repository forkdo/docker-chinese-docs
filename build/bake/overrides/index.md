# 覆盖配置（Overriding configurations）


Bake 支持从文件加载构建定义，但有时你需要更大的灵活性来配置这些定义。例如，你可能希望在特定环境中
构建时，或为特定目标覆盖某个属性。

以下属性列表可以被覆盖：

- `args`
- `attest`
- `cache-from`
- `cache-to`
- `context`
- `contexts`
- `dockerfile`
- `entitlements`
- `labels`
- `network`
- `no-cache`
- `output`
- `platform`
- `pull`
- `secrets`
- `ssh`
- `tags`
- `target`

要覆盖这些属性，你可以使用以下方法：

- [文件覆盖](#file-overrides)
- [CLI 覆盖](#command-line)
- [环境变量覆盖](#environment-variables)

## 文件覆盖

你可以加载多个定义目标构建配置的 Bake 文件。当你想将配置分离到不同文件中以便更好地组织，或根据
加载了哪些文件有条件地覆盖配置时，这很有用。

### 默认文件查找

你可以使用 `--file` 或 `-f` 标志指定要加载哪些文件。如果你没有指定任何文件，Bake 将使用以下
查找顺序：

1. `compose.yaml`
2. `compose.yml`
3. `docker-compose.yml`
4. `docker-compose.yaml`
5. `docker-bake.json`
6. `docker-bake.hcl`
7. `docker-bake.override.json`
8. `docker-bake.override.hcl`

如果找到多个 Bake 文件，所有文件都会被加载并合并为一个定义。文件根据查找顺序合并。

```console
$ docker buildx bake --print
[+] Building 0.0s (1/1) FINISHED                                                            
 => [internal] load local bake definitions                                             0.0s
 => => reading compose.yaml 45B / 45B                                                   0.0s
 => => reading docker-bake.hcl 113B / 113B                                              0.0s
 => => reading docker-bake.override.hcl 65B / 65B
```

如果合并的文件包含重复的属性定义，这些定义会根据属性被合并或被最后一次出现覆盖。

Bake 会按照找到的顺序尝试加载所有文件。如果多个文件定义了相同的目标，属性会被合并或覆盖。在覆盖的
情况下，最后加载的优先。

例如，给定以下文件：

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "foo"
}

target "default" {
  tags = ["username/my-app:${TAG}"]
}
```

```hcl {title=docker-bake.override.hcl}
variable "TAG" {
  default = "bar"
}
```

由于 `docker-bake.override.hcl` 在默认查找顺序中最后加载，`TAG` 变量被覆盖为值 `bar`。

```console
$ docker buildx bake --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["username/my-app:bar"]
    }
  }
}
```

### 手动文件覆盖

你可以使用 `--file` 标志显式指定要加载哪些文件，并将其作为一种有条件应用覆盖文件的方式。

例如，你可以创建一个为特定环境定义一组配置的文件，并仅在该环境构建时加载它。以下示例展示了如何
加载一个将 `TAG` 变量设置为 `bar` 的 `override.hcl` 文件。然后 `TAG` 变量被用于 `default` 目标。

```hcl {title=docker-bake.hcl}
variable "TAG" {
  default = "foo"
}

target "default" {
  tags = ["username/my-app:${TAG}"]
}
```

```hcl {title=overrides.hcl}
variable "TAG" {
  default = "bar"
}
```

不使用 `--file` 标志打印构建配置，显示 `TAG` 变量被设置为默认值 `foo`。

```console
$ docker buildx bake --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": [
        "username/my-app:foo"
      ]
    }
  }
}
```

使用 `--file` 标志加载 `overrides.hcl` 文件，将 `TAG` 变量覆盖为值 `bar`。

```console
$ docker buildx bake -f docker-bake.hcl -f overrides.hcl --print
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": [
        "username/my-app:bar"
      ]
    }
  }
}
```

## 命令行

你也可以从命令行使用 [`--set` 标志](/reference/cli/docker/buildx/bake/#set) 覆盖目标配置：

```hcl
# docker-bake.hcl
target "app" {
  args = {
    mybuildarg = "foo"
  }
}
```

```console
$ docker buildx bake --set app.args.mybuildarg=bar --set app.platform=linux/arm64 app --print
```

```json
{
  "group": {
    "default": {
      "targets": ["app"]
    }
  },
  "target": {
    "app": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "mybuildarg": "bar"
      },
      "platforms": ["linux/arm64"]
    }
  }
}
```

> [!NOTE]
>
> `--set` 是一个可重复的标志。对于 `tags` 等数组字段，重复使用 `--set` 以提供多个值，或使用 `+=`
> 运算符在不替换的情况下追加。
> 不支持像 `--set target.tags=[a,b]` 这样的数组字面量语法。

[https://golang.org/pkg/path/#Match](https://golang.org/pkg/path/#Match) 中定义的模式匹配语法也受支持：

```console
$ docker buildx bake --set foo*.args.mybuildarg=value  # overrides build arg for all targets starting with "foo"
$ docker buildx bake --set *.platform=linux/arm64      # overrides platform for all targets
$ docker buildx bake --set foo*.no-cache               # bypass caching only for targets starting with "foo"
```

可以使用 `--set` 覆盖的属性完整列表为：

- `args`
- `attest`
- `cache-from`
- `cache-to`
- `context`
- `contexts`
- `dockerfile`
- `entitlements`
- `labels`
- `network`
- `no-cache`
- `output`
- `platform`
- `pull`
- `secrets`
- `ssh`
- `tags`
- `target`

## 环境变量

你也可以使用环境变量来覆盖配置。

Bake 让你使用环境变量来覆盖 `variable` 块的值。只有 `variable` 块可以通过环境变量覆盖。这意味着你需要在
Bake 文件中定义变量，然后设置同名的环境变量来覆盖它。

以下示例展示了如何在 Bake 文件中定义一个带有默认值的 `TAG` 变量，并使用环境变量覆盖它。

```hcl
variable "TAG" {
  default = "latest"
}

target "default" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

```console
$ export TAG=$(git rev-parse --short HEAD)
$ docker buildx bake --print webapp
```

`TAG` 变量被覆盖为环境变量的值，即 `git rev-parse --short HEAD` 生成的短提交哈希。

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
      "tags": ["docker.io/username/webapp:985e9e9"]
    }
  }
}
```

### 类型强制转换

支持使用环境变量覆盖非字符串变量。作为环境变量传入的值会先被强制转换为合适的类型。

以下示例定义了一个 `PORT` 变量。`backend` 目标原样使用 `PORT` 变量，`frontend` 目标使用 `PORT` 的值
加一。

```hcl
variable "PORT" {
  default = 3000
}

group "default" {
  targets = ["backend", "frontend"]
}

target "backend" {
  args = {
    PORT = PORT
  }
}

target "frontend" {
  args = {
    PORT = add(PORT, 1)
  }
}
```

使用环境变量覆盖 `PORT` 时，会先将该值强制转换为预期类型（整数），然后 `frontend` 目标中的表达式才会运行。

```console
$ PORT=7070 docker buildx bake --print
```

```json
{
  "group": {
    "default": {
      "targets": [
        "backend",
        "frontend"
      ]
    }
  },
  "target": {
    "backend": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "PORT": "7070"
      }
    },
    "frontend": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "PORT": "7071"
      }
    }
  }
}
```

