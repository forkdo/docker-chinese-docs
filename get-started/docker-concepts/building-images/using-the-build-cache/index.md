# 使用构建缓存

<div id="youtube-player-Ri6jMknjprY" data-video-id="Ri6jMknjprY" class="youtube-video aspect-video h-fit w-full py-2">
</div>


## 解释

考虑您为 [getting-started](./writing-a-dockerfile/) 应用创建的以下 Dockerfile。

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "./src/index.js"]
```

当您运行 `docker build` 命令来创建新镜像时，Docker 会按指定顺序执行 Dockerfile 中的每个指令，为每个命令创建一个层。对于每个指令，Docker 会检查是否可以重用先前构建中的指令。如果发现之前已经执行过类似的指令，Docker 就不需要重新执行，而是使用缓存的结果。这样，您的构建过程变得更快、更高效，为您节省宝贵的时间和资源。

有效使用构建缓存可以通过重用先前构建的结果并跳过不必要的工作来实现更快的构建。
为了最大化缓存使用率并避免资源密集型和耗时的重新构建，理解缓存失效的工作原理非常重要。
以下是一些可能导致缓存失效的情况示例：

- 对 `RUN` 指令命令的任何更改都会使该层失效。如果您的 Dockerfile 中对 `RUN` 命令有任何修改，Docker 会检测到该更改并使构建缓存失效。

- 对使用 `COPY` 或 `ADD` 指令复制到镜像中的文件的任何更改。Docker 会监视项目目录内文件的任何更改。无论是内容更改还是权限等属性更改，Docker 都会将这些修改视为触发缓存失效的因素。

- 一旦某一层失效，所有后续层也会失效。如果任何先前的层（包括基础镜像或中间层）因更改而失效，Docker 会确保依赖于它的后续层也失效。这可以保持构建过程同步并防止不一致。

在编写或编辑 Dockerfile 时，请注意避免不必要的缓存未命中，以确保构建尽可能快速高效地运行。

## 动手实践

在本实践指南中，您将学习如何为 Node.js 应用有效使用 Docker 构建缓存。

### 构建应用程序

1. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

2. 打开终端并[克隆此示例应用程序](https://github.com/dockersamples/todo-list-app)。

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

    构建过程的结果如下：

    ```console
    [+] Building 20.0s (10/10) FINISHED
    ```

    第一行表示整个构建过程耗时 *20.0 秒*。首次构建可能需要一些时间，因为它需要安装依赖项。

5. 不做任何更改重新构建。

   现在，在不对源代码或 Dockerfile 进行任何更改的情况下重新运行 `docker build` 命令，如下所示：

    ```console
    $ docker build .
    ```

   只要命令和上下文保持不变，初始构建之后的后续构建会更快，这得益于缓存机制。Docker 会缓存构建过程中生成的中间层。当您在不更改 Dockerfile 或源代码的情况下重新构建镜像时，Docker 可以重用缓存的层，从而显著加快构建过程。

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

   后续构建仅耗时 1.0 秒，这是通过利用缓存层实现的。无需重复执行安装依赖项等耗时步骤。

    <table>
      <thead>
        <tr>
          <th>步骤
          </th>
          <th>描述
          </th>
          <th>耗时（首次运行）
          </th>
          <th>耗时（第二次运行）
          </th>
        </tr>
      </thead>
      <tbody>
      <tr>
       <td>1
       </td>
       <td><code>Load build definition from Dockerfile</code>
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>2
       </td>
       <td><code>Load metadata for docker.io/library/node:22-alpine</code>
       </td>
       <td>2.7 秒
       </td>
       <td>0.9 秒
       </td>
      </tr>
      <tr>
       <td>3
       </td>
       <td><code>Load .dockerignore</code>
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>4
       </td>
       <td><code>Load build context</code>
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
       <td><code>Set the working directory (WORKDIR)</code>
       </td>
       <td>0.1 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>6
       </td>
       <td><code>Copy the local code into the container</code>
       </td>
       <td>0.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>7
       </td>
       <td><code>Run yarn install --production</code>
       </td>
       <td>10.0 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>8
       </td>
       <td><code>Exporting layers</code>
       </td>
       <td>2.2 秒
       </td>
       <td>0.0 秒
       </td>
      </tr>
      <tr>
       <td>9
       </td>
       <td><code>Exporting the final image</code>
       </td>
       <td>3.0 秒
       </td>
       <td>0.0 秒
       </td>
     </tr>
     </tbody>
    </table>

    回到 `docker image history` 的输出，您会看到 Dockerfile 中的每个命令都成为镜像中的一个新层。您可能还记得，当您对镜像进行更改时，`yarn` 依赖项必须重新安装。有什么方法可以解决这个问题吗？每次构建都重新安装相同的依赖项没有太大意义，对吧？

    为了解决这个问题，请重构您的 Dockerfile，以便依赖项缓存保持有效，除非确实需要使其失效。对于基于 Node 的应用程序，依赖项在 `package.json` 文件中定义。如果该文件发生更改，您需要重新安装依赖项；但如果文件未更改，则使用缓存的依赖项。因此，首先只复制该文件，然后安装依赖项，最后复制其他所有内容。这样，只有在 `package.json` 文件发生更改时，才需要重新创建 yarn 依赖项。

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

    然后您将看到类似以下的输出：

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

    您会看到所有层都已重新构建。这完全没问题，因为您对 Dockerfile 做了相当大的更改。

9. 现在，对 `src/static/index.html` 文件进行更改（例如将标题更改为 "The Awesome Todo App"）。

10. 构建 Docker 镜像。这次，您的输出应该看起来有点不同。

    ```console
    $ docker build -t node-app:3.0 .
    ```

    然后您将看到类似以下的输出：

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

    首先，您应该注意到构建速度更快了。您会看到有几个步骤正在使用先前缓存的层。这是个好消息；您正在使用构建缓存。推送和拉取此镜像及其更新也会快得多。

通过遵循这些优化技术，您可以使 Docker 构建更快、更高效，从而实现更快的迭代周期并提高开发效率。

## 其他资源

* [使用缓存管理优化构建](/build/cache/)
* [缓存存储后端](/build/cache/backends/)
* [构建缓存失效](/build/cache/invalidation/)


## 下一步

现在您已经了解了如何有效使用 Docker 构建缓存，您可以开始学习多阶段构建。


<a class="button not-prose" href="/get-started/docker-concepts/building-images/multi-stage-builds/">多阶段构建</a>

