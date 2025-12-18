---
title: 使用构建缓存
keywords: 概念, 构建, 镜像, 容器, Docker Desktop
description: 本概念页面将向您介绍构建缓存、哪些更改会令缓存失效以及如何高效使用构建缓存。
summary: |
  高效使用构建缓存可以让您通过重用之前构建的结果并跳过不必要的步骤来实现更快的构建。为了最大化缓存使用率并避免资源密集且耗时的重建，了解缓存失效的工作原理至关重要。在本指南中，您将学习如何高效使用 Docker 构建缓存，以简化 Docker 镜像开发和持续集成工作流。
weight: 4
aliases: 
 - /guides/docker-concepts/building-images/using-the-build-cache/
---

{{< youtube-embed Ri6jMknjprY >}}

## 说明

考虑一下您为 [入门](./writing-a-dockerfile/) 应用创建的以下 Dockerfile。

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "./src/index.js"]
```

当您运行 `docker build` 命令创建新镜像时，Docker 会执行 Dockerfile 中的每条指令，为每条命令按顺序创建一个层。对于每条指令，Docker 会检查是否可以重用之前构建中的指令。如果发现您之前已经执行过类似的指令，Docker 就不需要重新执行，而是会使用缓存的结果。这样，您的构建过程会更快、更高效，为您节省宝贵的时间和资源。

高效使用构建缓存可以让您通过重用之前构建的结果并跳过不必要的工作来实现更快的构建。为了最大化缓存使用率并避免资源密集且耗时的重建，了解缓存失效的工作原理非常重要。以下是一些可能导致缓存失效的情况示例：

- `RUN` 指令的任何命令更改都会使该层失效。Docker 检测到更改，如果 Dockerfile 中的 `RUN` 命令有任何修改，Docker 会使其缓存失效。

- 使用 `COPY` 或 `ADD` 指令复制到镜像中的文件的任何更改。Docker 会密切关注项目目录中文件的任何更改。无论是内容还是权限等属性的更改，Docker 都会将这些修改视为触发缓存失效的因素。

- 一旦某一层失效，其后的所有层也会失效。如果任何先前的层（包括基础镜像或中间层）因更改而失效，Docker 会确保依赖它的后续层也被失效。这保持了构建过程的同步，防止了不一致性。

当您编写或编辑 Dockerfile 时，请注意避免不必要的缓存未命中，以确保构建尽可能快速高效地运行。

## 动手尝试

在本实践指南中，您将学习如何为 Node.js 应用高效使用 Docker 构建缓存。

### 构建应用

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 打开终端并 [克隆此示例应用](https://github.com/dockersamples/todo-list-app)。

    ```console
    $ git clone https://github.com/dockersamples/todo-list-app
    ```

3. 导航到 `todo-list-app` 目录：

    ```console
    $ cd todo-list-app
    ```

    在此目录中，您会找到一个名为 `Dockerfile` 的文件，内容如下：

    ```dockerfile
    FROM node:22-alpine
    WORKDIR /app
    COPY . .
    RUN yarn install --production
    EXPOSE 3000
    CMD ["node", "./src/index.js"]
    ```

4. 执行以下命令构建 Docker 镜像：

    ```console
    $ docker build .
    ```

    这是构建过程的结果：

    ```console
    [+] Building 20.0s (10/10) FINISHED
    ```

    第一行表示整个构建过程耗时 *20.0 秒*。首次构建可能需要一些时间，因为它会安装依赖项。

5. 不做更改重新构建。

   现在，在不更改源代码或 Dockerfile 的情况下重新运行 `docker build` 命令，如下所示：

    ```console
    $ docker build .
    ```

   只要命令和上下文保持不变，后续构建就会比初始构建更快，这是由于缓存机制。Docker 会缓存构建过程中生成的中间层。当您在不更改 Dockerfile 或源代码的情况下重新构建镜像时，Docker 可以重用缓存层，显著加快构建过程。

    ```console
    [+] Building 1.0s (9/9) FINISHED                                                                            docker:desktop-linux
     => [internal] load build definition from Dockerfile                                                                        0.0s
     => => transferring dockerfile: 187B                                                                                        0.0s
     ...
     => [internal] load build context                                                                                           0.0s
     => => transferring context: 8.16kB                                                                                         0.0s
     => CACHED [2/4] WORKDIR /app                                                                                               0.0s
     => CACHED [3/4] COPY . .                                                                                                   0.0s
     => CACHED [4/4] RUN yarn install --production                                                                              0.0s
     => exporting to image                                                                                                      0.0s
     => => exporting layers                                                                                                     0.0s
     => => exporting manifest
   ```

   后续构建仅用 1.0 秒就完成了，利用了缓存层。无需重复依赖项安装等耗时步骤。

    <table>
      <thead>
        <tr>
          <th>步骤
          </th>
          <th>描述
          </th>
          <th>首次耗时
          </th>
          <th>第二次耗时
          </th>
        </tr>
      </thead>
      <tbody>
      <tr>
       <td>1
       </td>
       <td><code>从 Dockerfile 加载构建定义</code>
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>2
       </td>
       <td><code>加载 docker.io/library/node:22-alpine 的元数据</code>
       </td>
       <td>2.7 秒
       </td>
       <td>0.9 秒
       </td>
      </tr>
      <tr>
       <td>3
       </td>
       <td><code>加载 .dockerignore</code>
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>4
       </td>
       <td><code>加载构建上下文</code>
    <p>
    (上下文大小: 4.60MB)
       </td>
       <td>0.1 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>5
       </td>
       <td><code>设置工作目录 (WORKDIR)</code>
       </td>
       <td>0.1 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>6
       </td>
       <td><code>将本地代码复制到容器中</code>
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>7
       </td>
       <td><code>运行 yarn install --production</code>
       </td>
       <td>10.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>8
       </td>
       <td><code>导出层</code>
       </td>
       <td>2.2 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>9
       </td>
       <td><code>导出最终镜像</code>
       </td>
       <td>3.0 秒
       </td>
       <td>0.0 秒
       </td>
     </tr>
     </tbody>
    </table>

    回到 `docker image history` 输出，您会看到 Dockerfile 中的每条命令都成为镜像中的新层。您可能记得，当您对镜像进行更改时，yarn 依赖项必须重新安装。有办法解决这个问题吗？每次构建都重新安装相同的依赖项似乎没什么意义，对吧？

    要解决这个问题，请重新构建您的 Dockerfile，使依赖缓存保持有效，除非确实需要使其失效。对于基于 Node 的应用，依赖项在 `package.json` 文件中定义。如果该文件更改，您希望重新安装依赖项；如果文件未更改，则使用缓存的依赖项。因此，首先复制该文件，然后安装依赖项，最后复制其他所有内容。这样，只有当 `package.json` 文件更改时，您才需要重新创建 yarn 依赖项。

6. 更新 Dockerfile，首先复制 `package.json` 文件，安装依赖项，然后复制其他所有内容。

     ```dockerfile
     FROM node:22-alpine
     WORKDIR /app
     COPY package.json yarn.lock ./
     RUN yarn install --production 
     COPY . . 
     EXPOSE 3000
     CMD ["node", "src/index.js"]
     ```

7. 在与 Dockerfile 相同的文件夹中创建一个名为 `.dockerignore` 的文件，内容如下。

     ```plaintext
     node_modules
     ```

8. 构建新镜像：

    ```console
    $ docker build .
    ```

    然后您会看到类似以下的输出：

    ```console
    [+] Building 16.1s (10/10) FINISHED
    => [internal] load build definition from Dockerfile                                               0.0s
    => => transferring dockerfile: 175B                                                               0.0s
    => [internal] load .dockerignore                                                                  0.0s
    => => transferring context: 2B                                                                    0.0s
    => [internal] load metadata for docker.io/library/node:22-alpine                                  0.0s
    => [internal] load build context                                                                  0.8s
    => => transferring context: 53.37MB                                                               0.8s
    => [1/5] FROM docker.io/library/node:22-alpine                                                    0.0s
    => CACHED [2/5] WORKDIR /app                                                                      0.0s
    => [3/5] COPY package.json yarn.lock ./                                                           0.2s
    => [4/5] RUN yarn install --production                                                           14.0s
    => [5/5] COPY . .                                                                                 0.5s
    => exporting to image                                                                             0.6s
    => => exporting layers                                                                            0.6s
    => => writing image     
    sha256:d6f819013566c54c50124ed94d5e66c452325327217f4f04399b45f94e37d25        0.0s
    => => naming to docker.io/library/node-app:2.0                                                 0.0s
    ```

    您会看到所有层都被重建了。这很好，因为您对 Dockerfile 进行了相当大的更改。

9. 现在，对 `src/static/index.html` 文件进行更改（比如将标题更改为 "The Awesome Todo App"）。

10. 构建 Docker 镜像。这次，您的输出应该略有不同。

    ```console
    $ docker build -t node-app:3.0 .
    ```

    然后您会看到类似以下的输出：

    ```console
    [+] Building 1.2s (10/10) FINISHED 
    => [internal] load build definition from Dockerfile                                               0.0s
    => => transferring dockerfile: 37B                                                                0.0s
    => [internal] load .dockerignore                                                                  0.0s
    => => transferring context: 2B                                                                    0.0s
    => [internal] load metadata for docker.io/library/node:22-alpine                                  0.0s 
    => [internal] load build context                                                                  0.2s
    => => transferring context: 450.43kB                                                              0.2s
    => [1/5] FROM docker.io/library/node:22-alpine                                                    0.0s
    => CACHED [2/5] WORKDIR /app                                                                      0.0s
    => CACHED [3/5] COPY package.json yarn.lock ./                                                    0.0s
    => CACHED [4/5] RUN yarn install --production                                                     0.0s
    => [5/5] COPY . .                                                                                 0.5s 
    => exporting to image                                                                             0.3s
    => => exporting layers                                                                            0.3s
    => => writing image     
    sha256:91790c87bcb096a83c2bd4eb512bc8b134c757cda0bdee4038187f98148e2eda       0.0s
    => => naming to docker.io/library/node-app:3.0                                                 0.0s
    ```

    首先，您应该注意到构建快了很多。您会看到几个步骤正在使用之前缓存的层。这很好；您正在使用构建缓存。推送和拉取此镜像及其更新也会更快。

通过遵循这些优化技术，您可以使 Docker 构建更快、更高效，从而实现更快的迭代周期并提高开发效率。

## 额外资源

* [使用缓存管理优化构建](/build/cache/)
* [缓存存储后端](/build/cache/backends/)
* [构建缓存失效](/build/cache/invalidation/)

## 下一步

现在您已经了解了如何高效使用 Docker 构建缓存，您已准备好学习多阶段构建。

{{< button text="多阶段构建" url="multi-stage-builds" >}}