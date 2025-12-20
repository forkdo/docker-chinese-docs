# 使用容器化数据库

使用本地容器化数据库提供了灵活性和易设置性，让您能够密切镜像生产环境，而无需传统数据库安装的开销。Docker 简化了这一过程，只需几个命令即可在隔离的容器中部署、管理和扩展数据库。

在本指南中，您将学习如何：

- 运行本地容器化数据库
- 访问容器化数据库的 Shell
- 从主机连接到容器化数据库
- 从另一个容器连接到容器化数据库
- 在卷中持久化数据库数据
- 构建自定义数据库镜像
- 使用 Docker Compose 运行数据库

本指南使用 MySQL 镜像作为示例，但这些概念可应用于其他数据库镜像。

## 先决条件

要学习本指南，您必须安装 Docker。要安装 Docker，请参阅 [获取 Docker](/get-started/get-docker.md)。

## 运行本地容器化数据库

大多数流行的数据库系统，包括 MySQL、PostgreSQL 和 MongoDB，都在 Docker Hub 上提供了 Docker 官方镜像。这些镜像是遵循最佳实践精心策划的集合，确保您可以访问最新的功能和安全更新。要开始使用，请访问 [Docker Hub](https://hub.docker.com) 并搜索您感兴趣的数据库。每个镜像的页面都提供了有关如何运行容器、自定义设置以及根据您的需求配置数据库的详细说明。有关本指南中使用的 MySQL 镜像的更多信息，请参阅 Docker Hub [MySQL 镜像](https://hub.docker.com/_/mysql) 页面。

要运行数据库容器，您可以使用 Docker Desktop GUI 或 CLI。








<div
  class="tabs"
  
    
      x-data="{ selected: 'CLI' }"
    
    @tab-select.window="$event.detail.group === 'ui' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'CLI'})"
        
      >
        CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'GUI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'GUI'})"
        
      >
        GUI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <p>要使用 CLI 运行容器，请在终端中运行以下命令：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC0tbmFtZSBteS1teXNxbCAtZSBNWVNRTF9ST09UX1BBU1NXT1JEPW15LXNlY3JldC1wdyAtZSBNWVNRTF9EQVRBQkFTRT1teWRiIC1kIG15c3FsOmxhdGVzdA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run --name my-mysql -e <span class="nv">MYSQL_ROOT_PASSWORD</span><span class="o">=</span>my-secret-pw -e <span class="nv">MYSQL_DATABASE</span><span class="o">=</span>mydb -d mysql:latest
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>在此命令中：</p>
<ul>
<li><code>--name my-mysql</code> 将名称 my-mysql 分配给您的容器，以便于引用。</li>
<li><code>-e MYSQL_ROOT_PASSWORD=my-secret-pw</code> 将 MySQL 的 root 密码设置为 my-secret-pw。将 my-secret-pw 替换为您选择的安全密码。</li>
<li><code>-e MYSQL_DATABASE=mydb</code> 可选地创建一个名为 mydb 的数据库。您可以将 mydb 更改为您所需的数据库名称。</li>
<li><code>-d</code> 以分离模式运行容器，意味着它在后台运行。</li>
<li><code>mysql:latest</code> 指定您要使用最新版本的 MySQL 镜像。</li>
</ul>
<p>要验证您的容器是否正在运行，请在终端中运行 <code>docker ps</code></p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'GUI' && 'hidden'"
      >
        <p>要使用 GUI 运行容器：</p>
<ol>
<li>
<p>在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。</p>
</li>
<li>
<p>在搜索框中指定 <code>mysql</code>，如果尚未选择，请选择 <code>Images</code> 选项卡。</p>
</li>
<li>
<p>将鼠标悬停在 <code>mysql</code> 镜像上并选择 <code>Run</code>。
出现 <strong>Run a new container</strong> 模态框。</p>
</li>
<li>
<p>展开 <strong>Optional settings</strong>。</p>
</li>
<li>
<p>在可选设置中，指定以下内容：</p>
<ul>
<li><strong>Container name</strong>: <code>my-mysql</code></li>
<li><strong>Environment variables</strong>:
<ul>
<li><code>MYSQL_ROOT_PASSWORD</code>:<code>my-secret-pw</code></li>
<li><code>MYSQL_DATABASE</code>:<code>mydb</code></li>
</ul>
</li>
</ul>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/guides/images/databases-1.webp"
    alt="指定了选项的可选设置屏幕。"
    
    
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
        src="/guides/images/databases-1.webp"
        alt="指定了选项的可选设置屏幕。"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>选择 <code>Run</code>。</p>
</li>
<li>
<p>打开 Docker Desktop 仪表板中的 <strong>Container</strong> 视图以验证您的容器是否正在运行。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


## 访问容器化数据库的 Shell

当数据库在 Docker 容器中运行时，您可能需要访问其 shell 来管理数据库、执行命令或执行管理任务。Docker 提供了一种使用 `docker exec` 命令的直接方法。此外，如果您更喜欢图形界面，可以使用 Docker Desktop 的 GUI。

如果您还没有运行的数据库容器，请参阅 [运行本地容器化数据库](#run-a-local-containerized-database)。








<div
  class="tabs"
  
    
      x-data="{ selected: 'CLI' }"
    
    @tab-select.window="$event.detail.group === 'ui' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'CLI'})"
        
      >
        CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'GUI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'GUI'})"
        
      >
        GUI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <p>要使用 CLI 访问 MySQL 容器的终端，您可以使用以下 <code>docker exec</code> 命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgZXhlYyAtaXQgbXktbXlzcWwgYmFzaA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker <span class="nb">exec</span> -it my-mysql bash
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>在此命令中：</p>
<ul>
<li><code>docker exec</code> 告诉 Docker 您想在正在运行的容器中执行命令。</li>
<li><code>-it</code> 确保您访问的终端是交互式的，因此您可以向其键入命令。</li>
<li><code>my-mysql</code> 是您的 MySQL 容器的名称。如果您在运行容器时使用了不同的名称，请使用该名称。</li>
<li><code>bash</code> 是您要在容器内运行的命令。它会打开一个 bash shell，让您可以与容器的文件系统和已安装的应用程序进行交互。</li>
</ul>
<p>执行此命令后，您将获得对 MySQL 容器内部 bash shell 的访问权限，您可以直接从那里管理 MySQL 服务器。您可以运行 <code>exit</code> 返回到您的终端。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'GUI' && 'hidden'"
      >
        <ol>
<li>打开 Docker Desktop 仪表板并选择 <strong>Containers</strong> 视图。</li>
<li>在容器的 <strong>Actions</strong> 列中，选择 <strong>Show container actions</strong>，然后选择 <strong>Open in terminal</strong>。</li>
</ol>
<p>在此终端中，您可以访问 MySQL 容器内部的 shell，您可以直接从那里管理 MySQL 服务器。</p>

      </div>
    
  </div>
</div>


访问容器的终端后，您可以在该容器中运行任何可用的工具。以下示例展示了如何在容器中使用 `mysql` 来列出数据库。

```console
# mysql -u root -p
Enter password: my-secret-pw

mysql> SHOW DATABASES;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

## 从主机连接到容器化数据库

从主机连接到容器化数据库涉及将容器内的端口映射到主机上的端口。此过程确保可以通过主机的网络访问容器内的数据库。对于 MySQL，默认端口是 3306。通过公开此端口，您可以使用主机上的各种数据库管理工具或应用程序与您的 MySQL 数据库进行交互。

在开始之前，您必须删除之前为本指南运行的任何容器。要停止并删除容器，可以：

- 在终端中，运行 `docker rm --force my-mysql` 以删除名为 `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **Containers** 视图中选择容器旁边的 **Delete** 图标。

接下来，您可以使用 Docker Desktop GUI 或 CLI 来运行映射了端口的容器。








<div
  class="tabs"
  
    
      x-data="{ selected: 'CLI' }"
    
    @tab-select.window="$event.detail.group === 'ui' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'CLI'})"
        
      >
        CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'GUI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'GUI'})"
        
      >
        GUI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <p>在终端中运行以下命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1wIDMzMDc6MzMwNiAtLW5hbWUgbXktbXlzcWwgLWUgTVlTUUxfUk9PVF9QQVNTV09SRD1teS1zZWNyZXQtcHcgLWUgTVlTUUxfREFUQUJBU0U9bXlkYiAtZCBteXNxbDpsYXRlc3Q=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -p 3307:3306 --name my-mysql -e <span class="nv">MYSQL_ROOT_PASSWORD</span><span class="o">=</span>my-secret-pw -e <span class="nv">MYSQL_DATABASE</span><span class="o">=</span>mydb -d mysql:latest
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>在此命令中，<code>-p 3307:3306</code> 将主机上的端口 3307 映射到容器中的端口 3306。</p>
<p>要验证端口是否已映射，请运行以下命令。</p>
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
<p>您应该看到类似以下的输出。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Q09OVEFJTkVSIElEICAgSU1BR0UgICAgICAgICAgQ09NTUFORCAgICAgICAgICAgICAgICAgIENSRUFURUQgICAgICAgICAgU1RBVFVTICAgICAgICAgIFBPUlRTICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIE5BTUVTCjZlYjc3NmNmZDczYyAgIG15c3FsOmxhdGVzdCAgICJkb2NrZXItZW50cnlwb2ludC5z4oCmIiAgIDE3IG1pbnV0ZXMgYWdvICAgVXAgMTcgbWludXRlcyAgIDMzMDYwL3RjcCwgMC4wLjAuMDozMzA3LT4zMzA2L3RjcCAgIG15LW15c3Fs', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                               NAMES
</span></span></span><span class="line"><span class="cl"><span class="go">6eb776cfd73c   mysql:latest   &#34;docker-entrypoint.s…&#34;   17 minutes ago   Up 17 minutes   33060/tcp, 0.0.0.0:3307-&gt;3306/tcp   my-mysql
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'GUI' && 'hidden'"
      >
        <p>要使用 GUI 运行容器：</p>
<ol>
<li>
<p>在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。</p>
</li>
<li>
<p>在搜索框中指定 <code>mysql</code>，如果尚未选择，请选择 <code>Images</code> 选项卡。</p>
</li>
<li>
<p>将鼠标悬停在 <code>mysql</code> 镜像上并选择 <code>Run</code>。
出现 <strong>Run a new container</strong> 模态框。</p>
</li>
<li>
<p>展开 <strong>Optional settings</strong>。</p>
</li>
<li>
<p>在可选设置中，指定以下内容：</p>
<ul>
<li><strong>Container name</strong>: <code>my-mysql</code></li>
<li><strong>Host port</strong> for the <strong>3306/tcp</strong> port: <code>3307</code></li>
<li><strong>Environment variables</strong>:
<ul>
<li><code>MYSQL_ROOT_PASSWORD</code>:<code>my-secret-pw</code></li>
<li><code>MYSQL_DATABASE</code>:<code>mydb</code></li>
</ul>
</li>
</ul>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/guides/images/databases-2.webp"
    alt="指定了选项的可选设置屏幕。"
    
    
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
        src="/guides/images/databases-2.webp"
        alt="指定了选项的可选设置屏幕。"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>选择 <code>Run</code>。</p>
</li>
<li>
<p>在 <strong>Containers</strong> 视图中，验证 <strong>Port(s)</strong> 列下是否映射了端口。您应该看到 <strong>my-mysql</strong> 容器的 <strong>3307:3306</strong>。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


此时，主机上运行的任何应用程序都可以通过 `localhost:3307` 访问容器中的 MySQL 服务。

## 从另一个容器连接到容器化数据库

从另一个容器连接到容器化数据库是微服务架构和开发过程中的常见场景。Docker 的网络功能可以轻松建立此连接，而无需将数据库暴露给主机网络。这是通过将数据库容器和需要访问它的容器放在同一个 Docker 网络上来实现的。

在开始之前，您必须删除之前为本指南运行的任何容器。要停止并删除容器，可以：

- 在终端中，运行 `docker rm --force my-mysql` 以删除名为 `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **Containers** 视图中选择容器旁边的 **Delete** 图标。

要创建网络并在其上运行容器：

1. 运行以下命令以创建名为 my-network 的 Docker 网络。

   ```console
   $ docker network create my-network
   ```

2. 运行您的数据库容器，并使用 `--network` 选项指定网络。这将在 my-network 网络上运行容器。

   ```console
   $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb --network my-network -d mysql:latest
   ```

3. 运行您的其他容器，并使用 `--network` 选项指定网络。在此示例中，您将运行一个可以连接到您的数据库的 phpMyAdmin 容器。

   1. 运行一个 phpMyAdmin 容器。使用 `--network` 选项指定网络，使用 `-p` 选项让您可以从主机访问容器，并使用 `-e` 选项为此镜像指定必需的环境变量。

      ```console
      $ docker run --name my-phpmyadmin -d --network my-network -p 8080:80 -e PMA_HOST=my-mysql phpmyadmin
      ```

4. 验证容器是否可以通信。在此示例中，您将访问 phpMyAdmin 并验证它是否连接到数据库。

   1. 打开 [http://localhost:8080](http://localhost:8080) 访问您的 phpMyAdmin 容器。
   2. 使用 `root` 作为用户名和 `my-secret-pw` 作为密码登录。
      您应该连接到 MySQL 服务器并看到您的数据库列出。

此时，运行在您的 `my-network` 容器网络上的任何应用程序都可以通过 `my-mysql:3306` 访问容器中的 MySQL 服务。

## 在卷中持久化数据库数据

在 Docker 卷中持久化数据库数据对于确保您的数据在容器重启和移除后得以保存是必要的。Docker 卷让您可以将数据库文件存储在容器的可写层之外，从而可以在不丢失数据的情况下升级容器、切换基础镜像和共享数据。以下是如何使用 Docker CLI 或 Docker Desktop GUI 将卷附加到您的数据库容器。

在开始之前，您必须删除之前为本指南运行的任何容器。要停止并删除容器，可以：

- 在终端中，运行 `docker rm --force my-mysql` 以删除名为 `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **Containers** 视图中选择容器旁边的 **Delete** 图标。

接下来，您可以使用 Docker Desktop GUI 或 CLI 来运行带有卷的容器。








<div
  class="tabs"
  
    
      x-data="{ selected: 'CLI' }"
    
    @tab-select.window="$event.detail.group === 'ui' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'CLI'})"
        
      >
        CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'GUI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'ui', name:
          'GUI'})"
        
      >
        GUI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <p>要运行附加了卷的数据库容器，请在 <code>docker run</code> 命令中包含 <code>-v</code> 选项，指定卷名和数据库在容器内存储其数据的路径。如果卷不存在，Docker 会自动为您创建它。</p>
<p>要运行附加了卷的数据库容器，然后验证数据是否持久化：</p>
<ol>
<li>
<p>运行容器并附加卷。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC0tbmFtZSBteS1teXNxbCAtZSBNWVNRTF9ST09UX1BBU1NXT1JEPW15LXNlY3JldC1wdyAtZSBNWVNRTF9EQVRBQkFTRT1teWRiIC12IG15LWRiLXZvbHVtZTovdmFyL2xpYi9teXNxbCAtZCBteXNxbDpsYXRlc3Q=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run --name my-mysql -e <span class="nv">MYSQL_ROOT_PASSWORD</span><span class="o">=</span>my-secret-pw -e <span class="nv">MYSQL_DATABASE</span><span class="o">=</span>mydb -v my-db-volume:/var/lib/mysql -d mysql:latest
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此命令将名为 <code>my-db-volume</code> 的卷挂载到容器中的 <code>/var/lib/mysql</code> 目录。</p>
</li>
<li>
<p>在数据库中创建一些数据。使用 <code>docker exec</code> 命令在容器内运行 <code>mysql</code> 并创建一个表。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgZXhlYyBteS1teXNxbCBteXNxbCAtdSByb290IC1wbXktc2VjcmV0LXB3IC1lICJDUkVBVEUgVEFCTEUgSUYgTk9UIEVYSVNUUyBteWRiLm15dGFibGUgKGNvbHVtbl9uYW1lIFZBUkNIQVIoMjU1KSk7IElOU0VSVCBJTlRPIG15ZGIubXl0YWJsZSAoY29sdW1uX25hbWUpIFZBTFVFUyAoJ3ZhbHVlJyk7Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker <span class="nb">exec</span> my-mysql mysql -u root -pmy-secret-pw -e <span class="s2">&#34;CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES (&#39;value&#39;);&#34;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此命令使用容器中的 <code>mysql</code> 工具创建一个名为 <code>mytable</code> 的表，其中包含一个名为 <code>column_name</code> 的列，最后插入一个值 <code>value</code>。</p>
</li>
<li>
<p>停止并删除容器。如果没有卷，您创建的表将在删除容器时丢失。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcm0gLS1mb3JjZSBteS1teXNxbA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker rm --force my-mysql
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>启动一个附加了卷的新容器。这次，您不需要指定任何环境变量，因为配置已保存在卷中。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC0tbmFtZSBteS1teXNxbCAtdiBteS1kYi12b2x1bWU6L3Zhci9saWIvbXlzcWwgLWQgbXlzcWw6bGF0ZXN0', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run --name my-mysql -v my-db-volume:/var/lib/mysql -d mysql:latest
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>验证您创建的表是否仍然存在。再次使用 <code>docker exec</code> 命令在容器内运行 <code>mysql</code>。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgZXhlYyBteS1teXNxbCBteXNxbCAtdSByb290IC1wbXktc2VjcmV0LXB3IC1lICJTRUxFQ1QgKiBGUk9NIG15ZGIubXl0YWJsZTsi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker <span class="nb">exec</span> my-mysql mysql -u root -pmy-secret-pw -e <span class="s2">&#34;SELECT * FROM mydb.mytable;&#34;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此命令使用容器中的 <code>mysql</code> 工具从 <code>mytable</code> 表中选择所有记录。</p>
<p>您应该看到类似以下的输出。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Y29sdW1uX25hbWUKdmFsdWU=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">column_name
</span></span></span><span class="line"><span class="cl"><span class="go">value
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'GUI' && 'hidden'"
      >
        <p>要运行附加了卷的数据库容器，然后验证数据是否持久化：</p>
<ol>
<li>
<p>运行附加了卷的容器。</p>
<ol>
<li>
<p>在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。</p>
</li>
<li>
<p>在搜索框中指定 <code>mysql</code>，如果尚未选择，请选择 <strong>Images</strong> 选项卡。</p>
</li>
<li>
<p>将鼠标悬停在 <strong>mysql</strong> 镜像上并选择 <strong>Run</strong>。
出现 <strong>Run a new container</strong> 模态框。</p>
</li>
<li>
<p>展开 <strong>Optional settings</strong>。</p>
</li>
<li>
<p>在可选设置中，指定以下内容：</p>
<ul>
<li><strong>Container name</strong>: <code>my-mysql</code></li>
<li><strong>Environment variables</strong>:
<ul>
<li><code>MYSQL_ROOT_PASSWORD</code>:<code>my-secret-pw</code></li>
<li><code>MYSQL_DATABASE</code>:<code>mydb</code></li>
</ul>
</li>
<li><strong>Volumes</strong>:
<ul>
<li><code>my-db-volume</code>:<code>/var/lib/mysql</code></li>
</ul>
</li>
</ul>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/guides/images/databases-3.webp"
    alt="指定了选项的可选设置屏幕。"
    
    
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
        src="/guides/images/databases-3.webp"
        alt="指定了选项的可选设置屏幕。"
      />
    </div>
  </template>
</figure>
<p>这里，卷的名称是 <code>my-db-volume</code>，它挂载在容器的 <code>/var/lib/mysql</code> 中。</p>
</li>
<li>
<p>选择 <code>Run</code>。</p>
</li>
</ol>
</li>
<li>
<p>在数据库中创建一些数据。</p>
<ol>
<li>
<p>在 <strong>Containers</strong> 视图中，在容器旁边选择 <strong>Show container actions</strong> 图标，然后选择 <strong>Open in terminal</strong>。</p>
</li>
<li>
<p>在容器的终端中运行以下命令以添加一个表。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBteXNxbCAtdSByb290IC1wbXktc2VjcmV0LXB3IC1lICJDUkVBVEUgVEFCTEUgSUYgTk9UIEVYSVNUUyBteWRiLm15dGFibGUgKGNvbHVtbl9uYW1lIFZBUkNIQVIoMjU1KSk7IElOU0VSVCBJTlRPIG15ZGIubXl0YWJsZSAoY29sdW1uX25hbWUpIFZBTFVFUyAoJ3ZhbHVlJyk7Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">#</span> mysql -u root -pmy-secret-pw -e <span class="s2">&#34;CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES (&#39;value&#39;);&#34;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此命令使用容器中的 <code>mysql</code> 工具创建一个名为 <code>mytable</code> 的表，其中包含一个名为 <code>column_name</code> 的列，最后插入一个值 value`。</p>
</li>
</ol>
</li>
<li>
<p>在 <strong>Containers</strong> 视图中，选择容器旁边的 <strong>Delete</strong> 图标，然后选择 <strong>Delete forever</strong>。如果没有卷，您创建的表将在删除容器时丢失。</p>
</li>
<li>
<p>运行附加了卷的容器。</p>
<ol>
<li>
<p>在 Docker Desktop 仪表板中，选择窗口顶部的全局搜索。</p>
</li>
<li>
<p>在搜索框中指定 <code>mysql</code>，如果尚未选择，请选择 <strong>Images</strong> 选项卡。</p>
</li>
<li>
<p>将鼠标悬停在 <strong>mysql</strong> 镜像上并选择 <strong>Run</strong>。
出现 <strong>Run a new container</strong> 模态框。</p>
</li>
<li>
<p>展开 <strong>Optional settings</strong>。</p>
</li>
<li>
<p>在可选设置中，指定以下内容：</p>
<ul>
<li><strong>Container name</strong>: <code>my-mysql</code></li>
<li><strong>Environment variables</strong>:
<ul>
<li><code>MYSQL_ROOT_PASSWORD</code>:<code>my-secret-pw</code></li>
<li><code>MYSQL_DATABASE</code>:<code>mydb</code></li>
</ul>
</li>
<li><strong>Volumes</strong>:
<ul>
<li><code>my-db-volume</code>:<code>/var/lib/mysql</code></li>
</ul>
</li>
</ul>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/guides/images/databases-3.webp"
    alt="指定了选项的可选设置屏幕。"
    
    
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
        src="/guides/images/databases-3.webp"
        alt="指定了选项的可选设置屏幕。"
      />
    </div>
  </template>
</figure>
</li>
<li>
<p>选择 <code>Run</code>。</p>
</li>
</ol>
</li>
<li>
<p>验证您创建的表是否仍然存在。</p>
<ol>
<li>
<p>在 <strong>Containers</strong> 视图中，在容器旁边选择 <strong>Show container actions</strong> 图标，然后选择 <strong>Open in terminal</strong>。</p>
</li>
<li>
<p>在容器的终端中运行以下命令以验证您创建的表是否仍然存在。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBteXNxbCAtdSByb290IC1wbXktc2VjcmV0LXB3IC1lICJTRUxFQ1QgKiBGUk9NIG15ZGIubXl0YWJsZTsi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">#</span> mysql -u root -pmy-secret-pw -e <span class="s2">&#34;SELECT * FROM mydb.mytable;&#34;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此命令使用容器中的 <code>mysql</code> 工具从 <code>mytable</code> 表中选择所有记录。</p>
<p>您应该看到类似以下的输出。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Y29sdW1uX25hbWUKdmFsdWU=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">column_name
</span></span></span><span class="line"><span class="cl"><span class="go">value
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>
</li>
</ol>

      </div>
    
  </div>
</div>


此时，任何挂载 `my-db-volume` 的 MySQL 容器都将能够访问和保存持久化的数据。

## 构建自定义数据库镜像

自定义您的数据库镜像可以让您在基础数据库服务器之外包含额外的配置、脚本或工具。这对于创建符合您特定开发或生产环境需求的 Docker 镜像特别有用。以下示例概述了如何构建和运行包含表初始化脚本的自定义 MySQL 镜像。

在开始之前，您必须删除之前为本指南运行的任何容器。要停止并删除容器，可以：

- 在终端中，运行 `docker rm --force my-mysql` 以删除名为 `my-mysql` 的容器。
- 或者，在 Docker Desktop 仪表板中，在 **Containers** 视图中选择容器旁边的 **Delete** 图标。

要构建和运行您的自定义镜像：

1. 创建一个 Dockerfile。

   1. 在您的项目目录中创建一个名为 `Dockerfile` 的文件。对于此示例，您可以在您选择的空目录中创建 `Dockerfile`。此文件将定义如何构建您的自定义 MySQL 镜像。
   2. 将以下内容添加到 `Dockerfile`。

      ```dockerfile
      # syntax=docker/dockerfile:1

      # 使用基础镜像 mysql:latest
      FROM mysql:latest

      # 设置环境变量
      ENV MYSQL_DATABASE mydb

      # 将自定义脚本或配置文件从主机复制到容器
      COPY ./scripts/ /docker-entrypoint-initdb.d/
      ```

      在此 Dockerfile 中，您设置了 MySQL 数据库名称的环境变量。您还可以使用 `COPY` 指令将自定义配置文件或脚本添加到容器中。在此示例中，主机 `./scripts/` 目录中的文件被复制到容器的 `/docker-entrypoint-initdb.d/` 目录中。在此目录中，`.sh`、`.sql` 和 `.sql.gz` 脚本在容器首次启动时执行。有关 Dockerfile 的更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

   3. 创建一个脚本文件以在数据库中初始化一个表。在您的 `Dockerfile` 所在的目录中，创建一个名为 `scripts` 的子目录，然后创建一个名为 `create_table.sql` 的文件，内容如下。

   ```text
   CREATE TABLE IF NOT EXISTS mydb.myothertable (
     column_name VARCHAR(255)
   );

   INSERT INTO mydb.myothertable (column_name) VALUES ('other_value');
   ```

   您现在应该具有以下目录结构。

   ```text
   ├── your-project-directory/
   │ ├── scripts/
   │ │ └── create_table.sql
   │ └── Dockerfile
   ```

2. 构建您的镜像。

   1. 在终端中，切换到您的 `Dockerfile` 所在的目录。
   2. 运行以下命令以构建镜像。

      ```console
      $ docker build -t my-custom-mysql .
      ```

      在此命令中，`-t my-custom-mysql` 将您的新镜像标记（命名）为 `my-custom-mysql`。命令末尾的句点 (.) 指定当前目录作为构建的上下文，Docker 在其中查找 Dockerfile 和构建所需的任何其他文件。

3. 像在 [运行本地容器化数据库](#run-a-local-containerized-database) 中那样运行您的镜像。这次，指定您的镜像名称而不是 `mysql:latest`。此外，您不再需要指定 `MYSQL_DATABASE` 环境变量，因为它现在由您的 Dockerfile 定义。

   ```console
   $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d my-custom-mysql
   ```

4. 使用以下命令验证您的容器是否正在运行。

   ```console
   $ docker ps
   ```

   您应该看到类似以下的输出。

   ```console
   CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS          PORTS                 NAMES
   f74dcfdb0e59   my-custom-mysql   "docker-entrypoint.s…"    2 hours ago    Up 51 minutes   3306/tcp, 33060/tcp   my-mysql
   ```

5. 验证您的初始化脚本是否已运行。在终端中运行以下命令以显示 `myothertable` 表的内容。

   ```console
   $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.myothertable;"
   ```

   您应该看到类似以下的输出。

   ```console
   column_name
   other_value
   ```

任何使用您的 `my-custom-mysql` 镜像运行的容器都将在首次启动时初始化表。

## 使用 Docker Compose 运行数据库

Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。只需一个命令，您就可以配置应用程序的所有服务（如数据库、Web 应用程序等）并管理它们。在此示例中，您将创建一个 Compose 文件并使用它来运行 MySQL 数据库容器和 phpMyAdmin 容器。

要使用 Docker Compose 运行您的容器：

1. 创建一个 Docker Compose 文件。

   1. 在您的项目目录中创建一个名为 `compose.yaml` 的文件。此文件将定义服务、网络和卷。
   2. 将以下内容添加到 `compose.yaml` 文件。

      ```yaml
      services:
        db:
          image: mysql:latest
          environment:
            MYSQL_ROOT_PASSWORD: my-secret-pw
            MYSQL_DATABASE: mydb
          ports:
            - 3307:3306
          volumes:
            - my-db-volume:/var/lib/mysql

        phpmyadmin:
          image: phpmyadmin/phpmyadmin:latest
          environment:
            PMA_HOST: db
            PMA_PORT: 3306
            MYSQL_ROOT_PASSWORD: my-secret-pw
          ports:
            - 8080:80
          depends_on:
            - db

      volumes:
        my-db-volume:
      ```

      对于数据库服务：

      - `db` 是服务的名称。
      - `image: mysql:latest` 指定该服务使用来自 Docker Hub 的最新 MySQL 镜像。
      - `environment` 列出了 MySQL 用于初始化数据库的环境变量，例如 root 密码和数据库名称。
      - `ports` 将主机上的端口 3307 映射到容器中的端口 3306，允许您从主机连接到数据库。
      - `volumes` 将 `my-db-volume` 挂载到容器内的 `/var/lib/mysql` 以持久化数据库数据。

      除了数据库服务之外，还有一个 phpMyAdmin 服务。默认情况下，Compose 为您的应用程序设置一个网络。每个服务的容器都加入默认网络，并且既可由该网络上的其他容器访问，又可通过服务名称被发现。因此，在 `PMA_HOST` 环境变量中，您可以指定服务名称 `db` 以连接到数据库服务。有关 Compose 的更多详细信息，请参阅 [Compose 文件参考](/reference/compose-file/)。

2. 运行 Docker Compose。

   1. 打开终端并切换到您的 `compose.yaml` 文件所在的目录。
   2. 使用以下命令运行 Docker Compose。

      ```console
      $ docker compose up
      ```

      您现在可以访问 [http://localhost:8080](http://localhost:8080) 上的 phpMyAdmin，并使用 `root` 作为用户名和 `my-secret-pw` 作为密码连接到您的数据库。

   3. 要停止容器，请在终端中按 `ctrl`+`c`。

现在，使用 Docker Compose，您可以启动数据库和应用程序、挂载卷、配置网络等等，所有这些都只需一个命令。

## 总结

本指南向您介绍了使用容器化数据库的基础知识，特别关注 MySQL，以增强灵活性、易设置性以及开发环境之间的一致性。本指南涵盖的用例不仅简化了您的开发工作流程，还为您应对更高级的数据库管理和部署场景做好准备，确保您的数据驱动应用程序保持健壮和可扩展。

相关信息：

- [Docker Hub 数据库镜像](https://hub.docker.com/search?q=database&type=image)
- [Dockerfile 参考](/reference/dockerfile/)
- [Compose 文件参考](/reference/compose-file/)
- [CLI 参考](/reference/cli/docker/)
- [数据库示例](../../reference/samples/_index.md#databases)
