# Bake


Bake 是 Docker Buildx 的一项功能，让你使用声明式文件来定义构建配置，而不是指定复杂的 CLI 表达式。
它还让你可以使用单次调用并发运行多个构建。

Bake 文件可以用 HCL 或 JSON 格式编写。Bake 还可以直接从 [Docker Compose 文件](./compose-file.md)
构建。下面是一个 HCL 格式的 Bake 文件示例：

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["frontend", "backend"]
}

target "frontend" {
  context = "./frontend"
  dockerfile = "frontend.Dockerfile"
  args = {
    NODE_VERSION = "22"
  }
  tags = ["myapp/frontend:latest"]
}

target "backend" {
  context = "./backend"
  dockerfile = "backend.Dockerfile"
  args = {
    GO_VERSION = "1.26"
  }
  tags = ["myapp/backend:latest"]
}
```

`group` 块定义了一组可以并发构建的目标。每个 `target` 块定义一个带有自身配置的构建目标，
例如构建上下文、Dockerfile 和 tags。

要使用上述 Bake 文件调用构建，你可以运行：

```console
$ docker buildx bake
```

这会执行 `default` 组，该组并发构建 `frontend` 和 `backend` 目标。

## 开始使用

要了解如何开始使用 Bake，请前往 [Bake 简介](./introduction.md)。

