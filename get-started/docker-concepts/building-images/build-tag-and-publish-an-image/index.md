# 构建、标记和发布镜像

<div id="youtube-player-chiiGLlYRlY" data-video-id="chiiGLlYRlY" class="youtube-video aspect-video h-fit w-full py-2">
</div>


## 解释

在本指南中，您将学习以下内容：

- **构建镜像**：基于 `Dockerfile` 构建镜像的过程
- **标记镜像**：为镜像命名的过程，这同时也决定了镜像的分发位置
- **发布镜像**：使用容器注册中心分发或共享新创建镜像的过程

### 构建镜像

大多数情况下，镜像是使用 Dockerfile 构建的。最基本的 `docker build` 命令可能如下所示：

```bash
docker build .
```

命令末尾的 `.` 提供了[构建上下文](https://docs.docker.com/build/concepts/context/#what-is-a-build-context)的路径或 URL。构建器将在该位置查找 `Dockerfile` 和其他引用的文件。

运行构建时，构建器会在需要时拉取基础镜像，然后运行 Dockerfile 中指定的指令。

使用前面的命令，镜像将没有名称，但输出会提供镜像的 ID。例如，前面的命令可能会产生以下输出：

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED                                              docker:desktop-linux
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 308B                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.12                                  0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [1/6] FROM docker.io/library/python:3.12                                                    0.0s
 => [internal] load build context                                                               0.0s
 => => transferring context: 123B                                                               0.0s
 => [2/6] WORKDIR /usr/local/app                                                                0.0s
 => [3/6] RUN useradd app                                                                       0.1s
 => [4/6] COPY ./requirements.txt ./requirements.txt                                            0.0s
 => [5/6] RUN pip install --no-cache-dir --upgrade -r requirements.txt                          3.2s
 => [6/6] COPY ./app ./app                                                                      0.0s
 => exporting to image                                                                          0.1s
 => => exporting layers                                                                         0.1s
 => => writing image sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00    0.0s
```

根据前面的输出，您可以使用引用的镜像启动容器：

```console
docker run sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00
```

这个名字当然不容易记住，这就是标记发挥作用的地方。

### 标记镜像

标记镜像是为镜像提供一个容易记住的名称的方法。但是，镜像名称有其结构。完整的镜像名称具有以下结构：

```text
[HOST[:PORT_NUMBER]/]PATH[:TAG]
```

- `HOST`：镜像所在的注册中心主机名（可选）。如果未指定主机，则默认使用 Docker 在 `docker.io` 的公共注册中心。
- `PORT_NUMBER`：如果提供了主机名，则为注册中心的端口号
- `PATH`：镜像的路径，由斜杠分隔的组件组成。对于 Docker Hub，格式遵循 `[NAMESPACE/]REPOSITORY`，其中命名空间是用户或组织的名称。如果未指定命名空间，则使用 `library`，这是 Docker 官方镜像的命名空间。
- `TAG`：自定义的、人类可读的标识符，通常用于识别镜像的不同版本或变体。如果未指定标签，则默认使用 `latest`。

镜像名称的一些示例包括：

- `nginx`，等同于 `docker.io/library/nginx:latest`：这会从 `docker.io` 注册中心的 `library` 命名空间、`nginx` 镜像仓库和 `latest` 标签拉取镜像。
- `docker/welcome-to-docker`，等同于 `docker.io/docker/welcome-to-docker:latest`：这会从 `docker.io` 注册中心的 `docker` 命名空间、`welcome-to-docker` 镜像仓库和 `latest` 标签拉取镜像。
- `ghcr.io/dockersamples/example-voting-app-vote:pr-311`：这会从 GitHub Container Registry 的 `dockersamples` 命名空间、`example-voting-app-vote` 镜像仓库和 `pr-311` 标签拉取镜像。

要在构建期间标记镜像，请添加 `-t` 或 `--tag` 标志：

```console
docker build -t my-username/my-image .
```

如果您已经构建了镜像，可以使用 [`docker image tag`](https://docs.docker.com/engine/reference/commandline/image_tag/) 命令为镜像添加另一个标签：

```console
docker image tag my-username/my-image another-username/another-image:v1
```

### 发布镜像

一旦您构建并标记了镜像，就可以将其推送到注册中心。为此，请使用 [`docker push`](https://docs.docker.com/engine/reference/commandline/image_push/) 命令：

```console
docker push my-username/my-image
```

几秒钟内，镜像的所有层都将被推送到注册中心。

> **需要身份验证**
>
> 在将镜像推送到仓库之前，您需要进行身份验证。
> 为此，只需使用 [docker login](https://docs.docker.com/engine/reference/commandline/login/) 命令。
{ .information }

## 动手尝试

在本实践指南中，您将使用提供的 Dockerfile 构建一个简单的镜像，并将其推送到 Docker Hub。

### 设置

1. 获取示例应用程序。

   如果您有 Git，可以克隆示例应用程序的仓库。否则，您可以下载示例应用程序。选择以下选项之一。

   






<div
  class="tabs"
  
    x-data="{ selected: '%E4%BD%BF%E7%94%A8-git-%E5%85%8B%E9%9A%86' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8-git-%E5%85%8B%E9%9A%86' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8-git-%E5%85%8B%E9%9A%86'"
        
      >
        使用 git 克隆
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%B8%8B%E8%BD%BD' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%B8%8B%E8%BD%BD'"
        
      >
        下载
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8-git-%E5%85%8B%E9%9A%86' && 'hidden'"
      >
        <p>在终端中使用以下命令克隆示例应用程序仓库。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBnaXQgY2xvbmUgaHR0cHM6Ly9naXRodWIuY29tL2RvY2tlci9nZXR0aW5nLXN0YXJ0ZWQtdG9kby1hcHA=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> git clone https://github.com/docker/getting-started-todo-app
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%B8%8B%E8%BD%BD' && 'hidden'"
      >
        <p>下载源代码并解压。</p>
<p><a class="button not-prose" href="https://github.com/docker/getting-started-todo-app/raw/cd61f824da7a614a8298db503eed6630eeee33a3/app.zip">下载源代码</a></p>

      </div>
    
  </div>
</div>



2. [下载并安装](https://www.docker.com/products/docker-desktop/) Docker Desktop。

3. 如果您还没有 Docker 账户，请[立即创建一个](https://hub.docker.com/)。完成后，使用该账户登录 Docker Desktop。


### 构建镜像

现在您已经在 Docker Hub 上拥有了一个仓库，是时候构建一个镜像并将其推送到该仓库了。

1. 在示例应用仓库的根目录下使用终端，运行以下命令。将 `YOUR_DOCKER_USERNAME` 替换为您的 Docker Hub 用户名：

    ```console
    $ docker build -t <YOUR_DOCKER_USERNAME>/concepts-build-image-demo .
    ```

    例如，如果您的用户名是 `mobywhale`，您将运行以下命令：

    ```console
    $ docker build -t mobywhale/concepts-build-image-demo .
    ```

2. 构建完成后，您可以使用以下命令查看镜像：

    ```console
    $ docker image ls
    ```

    该命令将产生类似于以下内容的输出：

    ```plaintext
    REPOSITORY                             TAG       IMAGE ID       CREATED          SIZE
    mobywhale/concepts-build-image-demo    latest    746c7e06537f   24 seconds ago   354MB
    ```

3. 您实际上可以使用 [docker image history](/reference/cli/docker/image/history/) 命令查看历史记录（或镜像的创建方式）：

    ```console
    $ docker image history mobywhale/concepts-build-image-demo
    ```

    然后您将看到类似于以下内容的输出：

    ```plaintext
    IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
    f279389d5f01   8 seconds ago   CMD ["node" "./src/index.js"]                   0B        buildkit.dockerfile.v0
    <missing>      8 seconds ago   EXPOSE map[3000/tcp:{}]                         0B        buildkit.dockerfile.v0 
    <missing>      8 seconds ago   WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
    <missing>      4 days ago      /bin/sh -c #(nop)  CMD ["node"]                 0B
    <missing>      4 days ago      /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B
    <missing>      4 days ago      /bin/sh -c #(nop) COPY file:4d192565a7220e13…   20.5kB
    <missing>      4 days ago      /bin/sh -c apk add --no-cache --virtual .bui…   7.92MB
    <missing>      4 days ago      /bin/sh -c #(nop)  ENV YARN_VERSION=1.22.19     0B
    <missing>      4 days ago      /bin/sh -c addgroup -g 1000 node     && addu…   126MB
    <missing>      4 days ago      /bin/sh -c #(nop)  ENV NODE_VERSION=20.12.0     0B
    <missing>      2 months ago    /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
    <missing>      2 months ago    /bin/sh -c #(nop) ADD file:d0764a717d1e9d0af…   8.42MB
    ```

    此输出显示了镜像的各个层，突出显示了您添加的层以及从基础镜像继承的层。

### 推送镜像

现在您已经构建了镜像，是时候将其推送到注册中心了。

1. 使用 [docker push](/reference/cli/docker/image/push/) 命令推送镜像：

    ```console
    $ docker push <YOUR_DOCKER_USERNAME>/concepts-build-image-demo
    ```

    如果您收到 `requested access to the resource is denied`（请求访问资源被拒绝），请确保您已登录并且镜像标签中的 Docker 用户名正确。

    稍等片刻，您的镜像就会被推送到 Docker Hub。

## 其他资源

要了解有关构建、标记和发布镜像的更多信息，请访问以下资源：

* [什么是构建上下文？](/build/concepts/context/#what-is-a-build-context)
* [docker build 参考](/engine/reference/commandline/image_build/)
* [docker image tag 参考](/engine/reference/commandline/image_tag/)
* [docker push 参考](/engine/reference/commandline/image_push/)
* [什么是注册中心？](/get-started/docker-concepts/the-basics/what-is-a-registry/)

## 下一步

现在您已经了解了如何构建和发布镜像，是时候学习如何使用 Docker 构建缓存来加速构建过程了。


<a class="button not-prose" href="https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/">使用构建缓存</a>

