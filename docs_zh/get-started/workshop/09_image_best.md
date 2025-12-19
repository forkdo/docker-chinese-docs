---
title: 镜像构建最佳实践
weight: 90
linkTitle: "第 8 部分：镜像构建最佳实践"
keywords: 入门，设置，概述，快速开始，简介，概念，容器，
  Docker Desktop
description: 为您的应用程序构建镜像的技巧
aliases:
 - /get-started/09_image_best/
 - /guides/workshop/09_image_best/
---

## 镜像分层

使用 `docker image history` 命令，您可以查看镜像中每个层的创建命令。

1. 使用 `docker image history` 命令查看您创建的 `getting-started` 镜像的各层。

    ```console
    $ docker image history getting-started
    ```

    您应该会看到类似以下的输出。

    ```plaintext
    IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
    a78a40cbf866        18 seconds ago      /bin/sh -c #(nop)  CMD ["node" "src/index.j…    0B                  
    f1d1808565d6        19 seconds ago      /bin/sh -c yarn install --production            85.4MB              
    a2c054d14948        36 seconds ago      /bin/sh -c #(nop) COPY dir:5dc710ad87c789593…   198kB               
    9577ae713121        37 seconds ago      /bin/sh -c #(nop) WORKDIR /app                  0B                  
    b95baba1cfdb        13 days ago         /bin/sh -c #(nop)  CMD ["node"]                 0B                  
    <missing>           13 days ago         /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B                  
    <missing>           13 days ago         /bin/sh -c #(nop) COPY file:238737301d473041…   116B                
    <missing>           13 days ago         /bin/sh -c apk add --no-cache --virtual .bui…   5.35MB              
    <missing>           13 days ago         /bin/sh -c #(nop)  ENV YARN_VERSION=1.21.1      0B                  
    <missing>           13 days ago         /bin/sh -c addgroup -g 1000 node     && addu…   74.3MB              
    <missing>           13 days ago         /bin/sh -c #(nop)  ENV NODE_VERSION=12.14.1     0B                  
    <missing>           13 days ago         /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B                  
    <missing>           13 days ago         /bin/sh -c #(nop) ADD file:e69d441d729412d24…   5.59MB   
    ```

    每一行代表镜像中的一个层。这里的显示是底部为基础层，顶部为最新层。通过这个输出，您还可以快速查看每个层的大小，帮助诊断大型镜像。

2. 您会注意到几行被截断了。如果添加 `--no-trunc` 标志，您将获得完整的输出。

    ```console
    $ docker image history --no-trunc getting-started
    ```

## 层缓存

现在您已经看到了分层的实际效果，接下来有一个重要的知识点，可以帮助减少容器镜像的构建时间。一旦某一层发生变化，所有下游层都必须重新创建。

回顾一下您为入门应用创建的以下 Dockerfile。

```dockerfile
# syntax=docker/dockerfile:1
FROM node:lts-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
```

回到镜像历史输出，您会看到 Dockerfile 中的每条命令都变成了镜像中的一个新层。您可能还记得，当您修改镜像时，yarn 依赖项必须重新安装。每次构建都携带相同的依赖项并没有太大意义。

要解决这个问题，您需要重新调整 Dockerfile 的结构，以支持依赖项的缓存。对于基于 Node 的应用，这些依赖项在 `package.json` 文件中定义。您可以先复制该文件，安装依赖项，然后再复制其他所有内容。这样，只有当 `package.json` 发生更改时，才会重新创建 yarn 依赖项。

1. 更新 Dockerfile，先复制 `package.json`，安装依赖项，然后再复制其他所有内容。

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM node:lts-alpine
   WORKDIR /app
   COPY package.json yarn.lock ./
   RUN yarn install --production
   COPY . .
   CMD ["node", "src/index.js"]
   ```

2. 使用 `docker build` 构建新镜像。

    ```console
    $ docker build -t getting-started .
    ```

    您应该会看到类似以下的输出。

    ```plaintext
    [+] Building 16.1s (10/10) FINISHED
    => [internal] load build definition from Dockerfile
    => => transferring dockerfile: 175B
    => [internal] load .dockerignore
    => => transferring context: 2B
    => [internal] load metadata for docker.io/library/node:lts-alpine
    => [internal] load build context
    => => transferring context: 53.37MB
    => [1/5] FROM docker.io/library/node:lts-alpine
    => CACHED [2/5] WORKDIR /app
    => [3/5] COPY package.json yarn.lock ./
    => [4/5] RUN yarn install --production
    => [5/5] COPY . .
    => exporting to image
    => => exporting layers
    => => writing image     sha256:d6f819013566c54c50124ed94d5e66c452325327217f4f04399b45f94e37d25
    => => naming to docker.io/library/getting-started
    ```

3. 现在，修改 `src/static/index.html` 文件。例如，将 `<title>` 改为 "The Awesome Todo App"。

4. 再次使用 `docker build -t getting-started .` 构建 Docker 镜像。这次，您的输出应该略有不同。

    ```plaintext
    [+] Building 1.2s (10/10) FINISHED
    => [internal] load build definition from Dockerfile
    => => transferring dockerfile: 37B
    => [internal] load .dockerignore
    => => transferring context: 2B
    => [internal] load metadata for docker.io/library/node:lts-alpine
    => [internal] load build context
    => => transferring context: 450.43kB
    => [1/5] FROM docker.io/library/node:lts-alpine
    => CACHED [2/5] WORKDIR /app
    => CACHED [3/5] COPY package.json yarn.lock ./
    => CACHED [4/5] RUN yarn install --production
    => [5/5] COPY . .
    => exporting to image
    => => exporting layers
    => => writing image     sha256:91790c87bcb096a83c2bd4eb512bc8b134c757cda0bdee4038187f98148e2eda
    => => naming to docker.io/library/getting-started
    ```

    首先，您应该注意到构建速度快了很多。而且，您会看到几个步骤使用了之前缓存的层。推送和拉取此镜像及其更新也会更快。

## 多阶段构建

多阶段构建是一种非常强大的工具，它使用多个阶段来创建镜像。它有几个优点：

- 将构建时依赖项与运行时依赖项分离
- 通过仅发送应用运行所需的文件来减少整体镜像大小

### Maven/Tomcat 示例

构建基于 Java 的应用时，您需要 JDK 将源代码编译为 Java 字节码。但是，JDK 在生产环境中并不需要。此外，您可能使用 Maven 或 Gradle 等工具来帮助构建应用。这些工具在最终镜像中也不需要。多阶段构建可以解决这个问题。

```dockerfile
# syntax=docker/dockerfile:1
FROM maven AS build
WORKDIR /app
COPY . .
RUN mvn package

FROM tomcat
COPY --from=build /app/target/file.war /usr/local/tomcat/webapps 
```

在这个示例中，您使用一个阶段（称为 `build`）来使用 Maven 执行实际的 Java 构建。在第二阶段（从 `FROM tomcat` 开始），您从 `build` 阶段复制文件。最终镜像只是正在创建的最后一个阶段，可以使用 `--target` 标志覆盖。

### React 示例

构建 React 应用时，您需要 Node 环境将 JS 代码（通常是 JSX）、SASS 样式表等编译为静态 HTML、JS 和 CSS。如果您不进行服务器端渲染，甚至不需要 Node 环境来运行生产构建。您可以将静态资源发送到静态 nginx 容器中。

```dockerfile
# syntax=docker/dockerfile:1
FROM node:lts AS build
WORKDIR /app
COPY package* yarn.lock ./
RUN yarn install
COPY public ./public
COPY src ./src
RUN yarn run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

在前面的 Dockerfile 示例中，它使用 `node:lts` 镜像执行构建（最大化层缓存），然后将输出复制到 nginx 容器中。

## 总结

在本节中，您学习了一些镜像构建最佳实践，包括层缓存和多阶段构建。

相关信息：
 - [Dockerfile 参考](/reference/dockerfile/)
 - [Dockerfile 最佳实践](/manuals/build/building/best-practices.md)

## 下一步

在下一节中，您将学习可以用来继续学习容器的其他资源。

{{< button text="下一步" url="10_what_next.md" >}}