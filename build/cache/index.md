# Docker 构建缓存


当你多次构建同一个 Docker 镜像时，懂得如何优化构建缓存是确保构建快速运行的重要工具。

## 构建缓存的工作原理（How the build cache works）

理解 Docker 的构建缓存有助于你编写出更好的 Dockerfile，从而带来更快的构建。

以下示例展示了一个用于 C 语言程序的小型 Dockerfile。

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

这个 Dockerfile 中的每条指令都会转换为最终镜像中的一个层。你可以把镜像层想象成一摞堆叠，每一层都在它之前的层之上添加更多内容：

![Image layer diagram](../images/cache-stack.png)

每当某一层发生变化，该层就需要重新构建。例如，假设你修改了 `main.c` 文件中的程序。修改之后，`COPY` 命令必须再次运行，这些更改才能出现在镜像中。换句话说，Docker 会使该层的缓存失效。

如果某一层发生变化，所有位于它之后的层也会受到影响。当带有 `COPY` 命令的层失效时，其后的所有层也需要重新运行：

![Image layer diagram, showing cache invalidation](../images/cache-stack-invalidated.png)

这就是 Docker 构建缓存的概要。一旦某一层发生变化，所有下游层也必须随之重新构建。即便它们本不会产生任何不同的构建结果，它们仍然需要重新运行。

## 其他资源（Other resources）

有关使用缓存进行高效构建的更多信息，请参阅：

- [缓存失效](invalidation.md)
- [优化构建缓存](optimization.md)
- [垃圾回收](garbage-collection.md)
- [缓存存储后端](./backends/_index.md)

