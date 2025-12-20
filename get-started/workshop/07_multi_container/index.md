# 多容器应用

到目前为止，你一直在使用单容器应用。但是，现在你将向应用程序栈中添加 MySQL。经常会出现这样的问题——“MySQL 应该在哪里运行？是安装在同一个容器中，还是单独运行？”一般来说，每个容器应该只做一件事并把它做好。以下是分开运行容器的几个原因：

- 你很可能需要以不同于数据库的方式来扩展 API 和前端。
- 独立的容器使你可以隔离地进行版本控制和更新。
- 虽然你可能本地使用容器来运行数据库，但在生产环境中你可能希望使用托管数据库服务。那么你就不希望将数据库引擎与你的应用一起打包。
- 运行多个进程将需要一个进程管理器（容器只启动一个进程），这会增加容器启动/关闭的复杂性。

还有更多的原因。因此，如下图所示，最好将你的应用运行在多个容器中。

![连接到 MySQL 容器的 Todo 应用](images/multi-container.webp?w=350h=250)


## 容器网络

请记住，容器默认在隔离状态下运行，它们不知道同一台机器上的其他进程或容器的任何信息。那么，如何让一个容器与另一个容器通信呢？答案是网络。如果你将两个容器放在同一个网络中，它们就可以相互通信。

## 启动 MySQL

有两种方法可以将容器放入网络：
 - 在启动容器时分配网络。
 - 将一个已在运行的容器连接到网络。

在接下来的步骤中，你将首先创建网络，然后在启动时附加 MySQL 容器。

1. 创建网络。

   ```console
   $ docker network create todo-app
   ```

2. 启动一个 MySQL 容器并将其附加到网络。你还将定义一些环境变量，数据库将使用这些变量来初始化数据库。要了解更多关于 MySQL 环境变量的信息，请参阅 [MySQL Docker Hub 页面](https://hub.docker.com/_/mysql/) 中的“环境变量”部分。

   






<div
  class="tabs"
  
    x-data="{ selected: 'Mac-/-Linux-/-Git-Bash' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Mac-/-Linux-/-Git-Bash' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac-/-Linux-/-Git-Bash'"
        
      >
        Mac / Linux / Git Bash
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'PowerShell' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'PowerShell'"
        
      >
        PowerShell
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Command-Prompt' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Command-Prompt'"
        
      >
        Command Prompt
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac-/-Linux-/-Git-Bash' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kIFwKICAgIC0tbmV0d29yayB0b2RvLWFwcCAtLW5ldHdvcmstYWxpYXMgbXlzcWwgXAogICAgLXYgdG9kby1teXNxbC1kYXRhOi92YXIvbGliL215c3FsIFwKICAgIC1lIE1ZU1FMX1JPT1RfUEFTU1dPUkQ9c2VjcmV0IFwKICAgIC1lIE1ZU1FMX0RBVEFCQVNFPXRvZG9zIFwKICAgIG15c3FsOjguMA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -d <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">    --network todo-app --network-alias mysql \
</span></span></span><span class="line"><span class="cl"><span class="go">    -v todo-mysql-data:/var/lib/mysql \
</span></span></span><span class="line"><span class="cl"><span class="go">    -e MYSQL_ROOT_PASSWORD=secret \
</span></span></span><span class="line"><span class="cl"><span class="go">    -e MYSQL_DATABASE=todos \
</span></span></span><span class="line"><span class="cl"><span class="go">    mysql:8.0
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'PowerShell' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kIGAKICAgIC0tbmV0d29yayB0b2RvLWFwcCAtLW5ldHdvcmstYWxpYXMgbXlzcWwgYAogICAgLXYgdG9kby1teXNxbC1kYXRhOi92YXIvbGliL215c3FsIGAKICAgIC1lIE1ZU1FMX1JPT1RfUEFTU1dPUkQ9c2VjcmV0IGAKICAgIC1lIE1ZU1FMX0RBVEFCQVNFPXRvZG9zIGAKICAgIG15c3FsOjguMA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-powershell" data-lang="powershell"><span class="line"><span class="cl"><span class="p">$</span> <span class="n">docker</span> <span class="n">run</span> <span class="n">-d</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">    <span class="p">-</span><span class="n">-network</span> <span class="nb">todo-app</span> <span class="p">-</span><span class="n">-network-alias</span> <span class="n">mysql</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">    <span class="n">-v</span> <span class="nb">todo-mysql</span><span class="n">-data:</span><span class="p">/</span><span class="n">var</span><span class="p">/</span><span class="n">lib</span><span class="p">/</span><span class="n">mysql</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">    <span class="n">-e</span> <span class="n">MYSQL_ROOT_PASSWORD</span><span class="p">=</span><span class="n">secret</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">    <span class="n">-e</span> <span class="n">MYSQL_DATABASE</span><span class="p">=</span><span class="n">todos</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">    <span class="n">mysql</span><span class="err">:</span><span class="mf">8.0</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Command-Prompt' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kIF4KICAgIC0tbmV0d29yayB0b2RvLWFwcCAtLW5ldHdvcmstYWxpYXMgbXlzcWwgXgogICAgLXYgdG9kby1teXNxbC1kYXRhOi92YXIvbGliL215c3FsIF4KICAgIC1lIE1ZU1FMX1JPT1RfUEFTU1dPUkQ9c2VjcmV0IF4KICAgIC1lIE1ZU1FMX0RBVEFCQVNFPXRvZG9zIF4KICAgIG15c3FsOjguMA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -d ^
</span></span><span class="line"><span class="cl"><span class="go">    --network todo-app --network-alias mysql ^
</span></span></span><span class="line"><span class="cl"><span class="go">    -v todo-mysql-data:/var/lib/mysql ^
</span></span></span><span class="line"><span class="cl"><span class="go">    -e MYSQL_ROOT_PASSWORD=secret ^
</span></span></span><span class="line"><span class="cl"><span class="go">    -e MYSQL_DATABASE=todos ^
</span></span></span><span class="line"><span class="cl"><span class="go">    mysql:8.0
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

   
   在上一个命令中，你可以看到 `--network-alias` 标志。在后面的部分，你将了解更多关于这个标志的信息。

   > [!TIP]
   >
   > 你会注意到上一个命令中有一个名为 `todo-mysql-data` 的卷被挂载在 `/var/lib/mysql`，这是 MySQL 存储其数据的位置。但是，你从未运行过 `docker volume create` 命令。Docker 意识到你想要使用一个命名卷，并会自动为你创建一个。

3. 为了确认数据库已启动并正在运行，请连接到数据库并验证它是否连接成功。

   ```console
   $ docker exec -it <mysql-container-id> mysql -u root -p
   ```

   当出现密码提示时，输入 `secret`。在 MySQL shell 中，列出数据库并验证你看到了 `todos` 数据库。

   ```console
   mysql> SHOW DATABASES;
   ```

   你应该会看到如下所示的输出：

   ```plaintext
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | mysql              |
   | performance_schema |
   | sys                |
   | todos              |
   +--------------------+
   5 rows in set (0.00 sec)
   ```

4. 退出 MySQL shell 以返回到你机器上的 shell。

   ```console
   mysql> exit
   ```

   你现在有了一个 `todos` 数据库，它已准备好供你使用。

## 连接到 MySQL

既然你知道 MySQL 已启动并正在运行，你就可以使用它了。但是，如何使用它呢？如果你在同一个网络上运行另一个容器，你如何找到该容器？请记住，每个容器都有自己的 IP 地址。

为了回答上述问题并更好地理解容器网络，你将使用 [nicolaka/netshoot](https://github.com/nicolaka/netshoot) 容器，它附带了许多用于排查或调试网络问题的有用工具。

1. 使用 nicolaka/netshoot 镜像启动一个新容器。确保将其连接到同一个网络。

   ```console
   $ docker run -it --network todo-app nicolaka/netshoot
   ```

2. 在容器内部，你将使用 `dig` 命令，这是一个有用的 DNS 工具。你将查找主机名 `mysql` 的 IP 地址。

   ```console
   $ dig mysql
   ```

   你应该会得到如下所示的输出。

   ```text
   ; <<>> DiG 9.18.8 <<>> mysql
   ;; global options: +cmd
   ;; Got answer:
   ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32162
   ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

   ;; QUESTION SECTION:
   ;mysql.				IN	A

   ;; ANSWER SECTION:
   mysql.			600	IN	A	172.23.0.2

   ;; Query time: 0 msec
   ;; SERVER: 127.0.0.11#53(127.0.0.11)
   ;; WHEN: Tue Oct 01 23:47:24 UTC 2019
   ;; MSG SIZE  rcvd: 44
   ```

   在“ANSWER SECTION”中，你将看到一条 `mysql` 的 `A` 记录，它解析为 `172.23.0.2`（你的 IP 地址很可能有不同的值）。虽然 `mysql` 通常不是一个有效的主机名，但 Docker 能够将其解析为具有该网络别名的容器的 IP 地址。还记得吗，你之前使用了 `--network-alias`。

   这意味着你的应用只需要简单地连接到一个名为 `mysql` 的主机，就可以与数据库通信了。

## 使用 MySQL 运行你的应用

Todo 应用支持设置几个环境变量来指定 MySQL 连接设置。它们是：

- `MYSQL_HOST` - 运行中 MySQL 服务器的主机名
- `MYSQL_USER` - 用于连接的用户名
- `MYSQL_PASSWORD` - 用于连接的密码
- `MYSQL_DB` - 连接后要使用的数据库

> [!NOTE]
>
> 尽管使用环境变量来设置连接设置在开发中通常是可接受的，但在生产环境中运行应用程序时，强烈不鼓励这样做。Docker 前安全负责人 Diogo Monica [写了一篇非常棒的博客文章](https://blog.diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/) 解释了原因。
>
> 一个更安全的机制是使用你的容器编排框架提供的 secret 支持。在大多数情况下，这些 secret 作为文件挂载到正在运行的容器中。你会看到许多应用（包括 MySQL 镜像和 todo 应用）也支持带有 `_FILE` 后缀的环境变量，以指向包含该变量的文件。
>
> 例如，设置 `MYSQL_PASSWORD_FILE` 变量将导致应用使用所引用文件的内容作为连接密码。Docker 不会做任何事情来支持这些环境变量。你的应用需要知道去查找该变量并获取文件内容。

你现在可以启动你的开发容器了。

1. 指定前面的每个环境变量，并将容器连接到你的应用网络。运行此命令时，请确保你位于 `getting-started-app` 目录中。

   






<div
  class="tabs"
  
    x-data="{ selected: 'Mac-/-Linux' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Mac-/-Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac-/-Linux'"
        
      >
        Mac / Linux
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'PowerShell' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'PowerShell'"
        
      >
        PowerShell
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Command-Prompt' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Command-Prompt'"
        
      >
        Command Prompt
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Git-Bash' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Git-Bash'"
        
      >
        Git Bash
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac-/-Linux' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIFwKICAtdyAvYXBwIC12ICIkKHB3ZCk6L2FwcCIgXAogIC0tbmV0d29yayB0b2RvLWFwcCBcCiAgLWUgTVlTUUxfSE9TVD1teXNxbCBcCiAgLWUgTVlTUUxfVVNFUj1yb290IFwKICAtZSBNWVNRTF9QQVNTV09SRD1zZWNyZXQgXAogIC1lIE1ZU1FMX0RCPXRvZG9zIFwKICBub2RlOmx0cy1hbHBpbmUgXAogIHNoIC1jICJ5YXJuIGluc3RhbGwgJiYgeWFybiBydW4gZGV2Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -dp 127.0.0.1:3000:3000 <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -w /app -v &#34;$(pwd):/app&#34; \
</span></span></span><span class="line"><span class="cl"><span class="go">  --network todo-app \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_HOST=mysql \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_USER=root \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_PASSWORD=secret \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_DB=todos \
</span></span></span><span class="line"><span class="cl"><span class="go">  node:lts-alpine \
</span></span></span><span class="line"><span class="cl"><span class="go">  sh -c &#34;yarn install &amp;&amp; yarn run dev&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'PowerShell' && 'hidden'"
      >
        <p>在 Windows 中，请在 PowerShell 中运行此命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIGAKICAtdyAvYXBwIC12ICIkKHB3ZCk6L2FwcCIgYAogIC0tbmV0d29yayB0b2RvLWFwcCBgCiAgLWUgTVlTUUxfSE9TVD1teXNxbCBgCiAgLWUgTVlTUUxfVVNFUj1yb290IGAKICAtZSBNWVNRTF9QQVNTV09SRD1zZWNyZXQgYAogIC1lIE1ZU1FMX0RCPXRvZG9zIGAKICBub2RlOmx0cy1hbHBpbmUgYAogIHNoIC1jICJ5YXJuIGluc3RhbGwgJiYgeWFybiBydW4gZGV2Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-powershell" data-lang="powershell"><span class="line"><span class="cl"><span class="p">$</span> <span class="n">docker</span> <span class="n">run</span> <span class="n">-dp</span> <span class="mf">127.0</span><span class="p">.</span><span class="py">0</span><span class="p">.</span><span class="mf">1</span><span class="err">:</span><span class="mf">3000</span><span class="err">:</span><span class="mf">3000</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="n">-w</span> <span class="p">/</span><span class="n">app</span> <span class="n">-v</span> <span class="s2">&#34;</span><span class="p">$(</span><span class="n">pwd</span><span class="p">)</span><span class="s2">:/app&#34;</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="p">-</span><span class="n">-network</span> <span class="nb">todo-app</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="n">-e</span> <span class="n">MYSQL_HOST</span><span class="p">=</span><span class="n">mysql</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="n">-e</span> <span class="n">MYSQL_USER</span><span class="p">=</span><span class="n">root</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="n">-e</span> <span class="n">MYSQL_PASSWORD</span><span class="p">=</span><span class="n">secret</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="n">-e</span> <span class="n">MYSQL_DB</span><span class="p">=</span><span class="n">todos</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="n">node</span><span class="err">:</span><span class="nb">lts-alpine</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">  <span class="n">sh</span> <span class="n">-c</span> <span class="s2">&#34;yarn install &amp;&amp; yarn run dev&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Command-Prompt' && 'hidden'"
      >
        <p>在 Windows 中，请在命令提示符中运行此命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIF4KICAtdyAvYXBwIC12ICIlY2QlOi9hcHAiIF4KICAtLW5ldHdvcmsgdG9kby1hcHAgXgogIC1lIE1ZU1FMX0hPU1Q9bXlzcWwgXgogIC1lIE1ZU1FMX1VTRVI9cm9vdCBeCiAgLWUgTVlTUUxfUEFTU1dPUkQ9c2VjcmV0IF4KICAtZSBNWVNRTF9EQj10b2RvcyBeCiAgbm9kZTpsdHMtYWxwaW5lIF4KICBzaCAtYyAieWFybiBpbnN0YWxsICYmIHlhcm4gcnVuIGRldiI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -dp 127.0.0.1:3000:3000 ^
</span></span><span class="line"><span class="cl"><span class="go">  -w /app -v &#34;%cd%:/app&#34; ^
</span></span></span><span class="line"><span class="cl"><span class="go">  --network todo-app ^
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_HOST=mysql ^
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_USER=root ^
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_PASSWORD=secret ^
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_DB=todos ^
</span></span></span><span class="line"><span class="cl"><span class="go">  node:lts-alpine ^
</span></span></span><span class="line"><span class="cl"><span class="go">  sh -c &#34;yarn install &amp;&amp; yarn run dev&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Git-Bash' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIFwKICAtdyAvL2FwcCAtdiAiLyQocHdkKTovYXBwIiBcCiAgLS1uZXR3b3JrIHRvZG8tYXBwIFwKICAtZSBNWVNRTF9IT1NUPW15c3FsIFwKICAtZSBNWVNRTF9VU0VSPXJvb3QgXAogIC1lIE1ZU1FMX1BBU1NXT1JEPXNlY3JldCBcCiAgLWUgTVlTUUxfREI9dG9kb3MgXAogIG5vZGU6bHRzLWFscGluZSBcCiAgc2ggLWMgInlhcm4gaW5zdGFsbCAmJiB5YXJuIHJ1biBkZXYi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -dp 127.0.0.1:3000:3000 <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  -w //app -v &#34;/$(pwd):/app&#34; \
</span></span></span><span class="line"><span class="cl"><span class="go">  --network todo-app \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_HOST=mysql \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_USER=root \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_PASSWORD=secret \
</span></span></span><span class="line"><span class="cl"><span class="go">  -e MYSQL_DB=todos \
</span></span></span><span class="line"><span class="cl"><span class="go">  node:lts-alpine \
</span></span></span><span class="line"><span class="cl"><span class="go">  sh -c &#34;yarn install &amp;&amp; yarn run dev&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


2. 如果你查看容器的日志（`docker logs -f <container-id>`），你应该会看到类似以下的消息，这表明它正在使用 mysql 数据库。

   ```console
   $ nodemon src/index.js
   [nodemon] 2.0.20
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching dir(s): *.*
   [nodemon] starting `node src/index.js`
   Connected to mysql db at host mysql
   Listening on port 3000
   ```

3. 在浏览器中打开应用，并向你的待办事项列表中添加几个项目。

4. 连接到 mysql 数据库并证明这些项目正在被写入数据库。记住，密码是 `secret`。

   ```console
   $ docker exec -it <mysql-container-id> mysql -p todos
   ```

   在 mysql shell 中，运行以下命令：

   ```console
   mysql> select * from todo_items;
   +--------------------------------------+--------------------+-----------+
   | id                                   | name               | completed |
   +--------------------------------------+--------------------+-----------+
   | c906ff08-60e6-44e6-8f49-ed56a0853e85 | Do amazing things! |         0 |
   | 2912a79e-8486-4bc3-a4c5-460793a575ab | Be awesome!        |         0 |
   +--------------------------------------+--------------------+-----------+
   ```

   你的表看起来会不一样，因为它包含的是你的项目。但是，你应该能看到它们存储在那里。

## 小结

此时，你拥有一个将其数据存储在运行于独立容器中的外部数据库里的应用程序。你学到了一些关于容器网络和使用 DNS 进行服务发现的知识。

相关信息：
 - [docker CLI 参考](/reference/cli/docker/)
 - [网络概述](/manuals/engine/network/_index.md)

## 后续步骤

你很可能开始觉得要启动这个应用程序需要做的事情有点让人不知所措了。你必须创建网络、启动容器、指定所有环境变量、暴露端口等等。这需要记住很多东西，而且肯定会让将其传递给其他人变得更加困难。

在下一节中，你将学习 Docker Compose。使用 Docker Compose，你可以更轻松地共享你的应用程序栈，并让其他人通过一个简单、单一的命令来启动它们。


<a class="button not-prose" href="/get-started/workshop/08_using_compose/">使用 Docker Compose</a>

