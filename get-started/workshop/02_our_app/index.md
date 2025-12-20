# 容器化应用程序

在本指南的剩余部分，您将使用一个运行在 Node.js 上的简单待办事项列表管理器。如果您不熟悉 Node.js，也不必担心。本指南不需要任何 JavaScript 前期经验。

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您已安装 [Git 客户端](https://git-scm.com/downloads)。
- 您有一个用于编辑文件的 IDE 或文本编辑器。Docker 推荐使用 [Visual Studio Code](https://code.visualstudio.com/)。

## 获取应用程序

在运行应用程序之前，您需要将应用程序源代码获取到您的机器上。

1. 使用以下命令克隆 [getting-started-app 仓库](https://github.com/docker/getting-started-app/tree/main)：

   ```console
   $ git clone https://github.com/docker/getting-started-app.git
   ```

2. 查看克隆仓库的内容。您应该会看到以下文件和子目录。

   ```text
   ├── getting-started-app/
   │ ├── .dockerignore
   │ ├── package.json
   │ ├── README.md
   │ ├── spec/
   │ ├── src/
   │ └── yarn.lock
   ```

## 构建应用程序的镜像

要构建镜像，您需要使用 Dockerfile。Dockerfile 是一个简单的基于文本的文件，没有文件扩展名，其中包含指令脚本。Docker 使用此脚本来构建容器镜像。

1. 在 `getting-started-app` 目录中，与 `package.json` 文件相同的位置，创建一个名为 `Dockerfile` 的文件，内容如下：

   ```dockerfile
   # syntax=docker/dockerfile:1

   FROM node:lts-alpine
   WORKDIR /app
   COPY . .
   RUN yarn install --production
   CMD ["node", "src/index.js"]
   EXPOSE 3000
   ```

   此 Dockerfile 以 `node:lts-alpine` 基础镜像开始，这是一个轻量级的 Linux 镜像，预装了 Node.js 和 Yarn 包管理器。它将所有源代码复制到镜像中，安装必要的依赖项，并启动应用程序。

2. 使用以下命令构建镜像：

   在终端中，确保您位于 `getting-started-app` 目录中。将 `/path/to/getting-started-app` 替换为您的 `getting-started-app` 目录的路径。

   ```console
   $ cd /path/to/getting-started-app
   ```

   构建镜像。

   ```console
   $ docker build -t getting-started .
   ```

   `docker build` 命令使用 Dockerfile 来构建新镜像。您可能注意到 Docker 下载了很多“层”。这是因为您指示构建器从 `node:lts-alpine` 镜像开始。但是，由于您的机器上没有该镜像，Docker 需要下载它。

   Docker 下载镜像后，Dockerfile 中的指令会复制您的应用程序并使用 `yarn` 安装应用程序的依赖项。`CMD` 指令指定了从此镜像启动容器时要运行的默认命令。

   最后，`-t` 标记为您的镜像打上标签。可以将其视为最终镜像的人类可读名称。由于您将镜像命名为 `getting-started`，因此在运行容器时可以引用该镜像。

   `docker build` 命令末尾的 `.` 告诉 Docker 在当前目录中查找 `Dockerfile`。

## 启动应用程序容器

现在您有了一个镜像，可以使用 `docker run` 命令在容器中运行应用程序。

1. 使用 `docker run` 命令运行您的容器，并指定您刚刚创建的镜像名称：

   ```console
   $ docker run -d -p 127.0.0.1:3000:3000 getting-started
   ```

   `-d` 标志（`--detach` 的缩写）在后台运行容器。
   这意味着 Docker 启动您的容器并将您返回到终端提示符。此外，它不会在终端中显示日志。

   `-p` 标志（`--publish` 的缩写）在主机和容器之间创建端口映射。`-p` 标志采用 `HOST:CONTAINER` 格式的字符串值，其中 `HOST` 是主机上的地址，`CONTAINER` 是容器上的端口。该命令将容器的端口 3000 发布到主机上的 `127.0.0.1:3000` (`localhost:3000`)。如果没有端口映射，您将无法从主机访问应用程序。

2. 几秒钟后，打开您的 Web 浏览器访问 [http://localhost:3000](http://localhost:3000)。
   您应该会看到您的应用程序。

   ![空的待办事项列表](images/todo-list-empty.webp)

3. 添加一两个项目，并查看它是否按预期工作。您可以将项目标记为完成并将其删除。您的前端正在成功地将项目存储在后端。

此时，您拥有一个正在运行的待办事项列表管理器，其中包含几个项目。

如果您快速查看一下您的容器，您应该会看到至少一个正在运行的容器，该容器使用 `getting-started` 镜像并位于端口 `3000` 上。要查看您的容器，您可以使用 CLI 或 Docker Desktop 的图形界面。








<div
  class="tabs"
  
    x-data="{ selected: 'CLI' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'CLI'"
        
      >
        CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Desktop'"
        
      >
        Docker Desktop
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <p>在终端中运行 <code>docker ps</code> 命令以列出您的容器。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcHM=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker ps
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>应该会出现类似以下的输出。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Q09OVEFJTkVSIElEICAgICAgICBJTUFHRSAgICAgICAgICAgICAgIENPTU1BTkQgICAgICAgICAgICAgICAgICBDUkVBVEVEICAgICAgICAgICAgIFNUQVRVUyAgICAgICAgICAgICAgUE9SVFMgICAgICAgICAgICAgICAgICAgICAgTkFNRVMKZGY3ODQ1NDg2NjZkICAgICAgICBnZXR0aW5nLXN0YXJ0ZWQgICAgICJkb2NrZXItZW50cnlwb2ludC5z4oCmIiAgIDIgbWludXRlcyBhZ28gICAgICAgVXAgMiBtaW51dGVzICAgICAgICAxMjcuMC4wLjE6MzAwMC0&#43;MzAwMC90Y3AgICBwcmljZWxlc3NfbWNjbGludG9jaw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
</span></span></span><span class="line"><span class="cl"><span class="go">df784548666d        getting-started     &#34;docker-entrypoint.s…&#34;   2 minutes ago       Up 2 minutes        127.0.0.1:3000-&gt;3000/tcp   priceless_mcclintock
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <p>在 Docker Desktop 中，选择 <strong>Containers</strong> 选项卡以查看您的容器列表。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/get-started/workshop/images/dashboard-two-containers.webp"
    alt="Docker Desktop 正在运行 get-started 容器"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="/get-started/workshop/images/dashboard-two-containers.webp"
        alt="Docker Desktop 正在运行 get-started 容器"
      />
    </div>
  </template>
</figure>

      </div>
    
  </div>
</div>


## 总结

在本节中，您学习了有关创建 Dockerfile 来构建镜像的基础知识。构建镜像后，您启动了一个容器并看到了正在运行的应用程序。

相关信息：

- [Dockerfile 参考](/reference/dockerfile/)
- [docker CLI 参考](/reference/cli/docker/)

## 下一步

接下来，您将对应用程序进行修改，并学习如何使用新镜像更新正在运行的应用程序。在此过程中，您将学习一些其他有用的命令。


<a class="button not-prose" href="/get-started/workshop/03_updating_app/">更新应用程序</a>

