# 持久化数据库

如果你没有注意到，每次启动容器时，你的待办事项列表都是空的。为什么会这样？在本部分中，你将深入了解容器的工作原理。

## 容器的文件系统

当容器运行时，它使用镜像中的各个层作为其文件系统。
每个容器还会获得自己的“暂存空间”来创建/更新/删除文件。任何更改都不会在另一个容器中看到，即使它们使用的是同一个镜像。

### 实践演示

为了亲眼看到这一点，你将启动两个容器。在一个容器中，你将创建一个文件。在另一个容器中，你将检查该文件是否存在。

1. 启动一个 Alpine 容器并在其中创建一个新文件。

    ```console
    $ docker run --rm alpine touch greeting.txt
    ```

    > [!TIP]
    > 你在镜像名称（本例中为 `alpine`）之后指定的任何命令都会在容器内执行。在本例中，命令 `touch greeting.txt` 会在容器的文件系统上放置一个名为 `greeting.txt` 的文件。

2. 运行一个新的 Alpine 容器，并使用 `stat` 命令检查文件是否存在。
   
   ```console
   $ docker run --rm alpine stat greeting.txt
   ```

   你应该会看到类似以下的输出，表明该文件在新容器中不存在。

   ```console
   stat: can't stat 'greeting.txt': No such file or directory
   ```

第一个容器创建的 `greeting.txt` 文件在第二个容器中不存在。这是因为每个容器的可写“顶层”是隔离的。即使两个容器共享组成基础镜像的相同底层，可写层对于每个容器也是唯一的。

## 容器卷

通过之前的实验，你看到每个容器在每次启动时都从镜像定义开始。虽然容器可以创建、更新和删除文件，但当你移除容器时，这些更改会丢失，而且 Docker 会将所有更改隔离到该容器中。使用卷，你可以改变这一切。

[卷](/manuals/engine/storage/volumes.md) 提供了将容器的特定文件系统路径连接回主机的能力。如果你在容器中挂载一个目录，该目录中的更改也会在主机上看到。如果你在容器重启时挂载相同的目录，你会看到相同的文件。

主要有两种类型的卷。你最终会使用这两种，但你将从卷挂载开始。

## 持久化待办事项数据

默认情况下，待办事项应用将其数据存储在容器文件系统中 `/etc/todos/todo.db` 的 SQLite 数据库中。如果你不熟悉 SQLite，不用担心！它只是一个关系型数据库，将所有数据存储在单个文件中。虽然这对于大规模应用程序来说不是最佳选择，但对于小型演示来说很有效。稍后你将学习如何将其切换到不同的数据库引擎。

由于数据库是一个单文件，如果你能在主机上持久化该文件并使其对下一个容器可用，它就应该能够从上一个容器停止的地方继续。通过创建一个卷并将其附加（通常称为“挂载”）到你存储数据的目录，你可以持久化数据。当你的容器写入 `todo.db` 文件时，它会将数据持久化到主机上的卷中。

如前所述，你将使用卷挂载。可以将卷挂载视为一个不透明的数据桶。Docker 完全管理卷，包括磁盘上的存储位置。你只需要记住卷的名称。

### 创建卷并启动容器

你可以使用 CLI 或 Docker Desktop 的图形界面来创建卷并启动容器。








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
        <ol>
<li>
<p>使用 <code>docker volume create</code> 命令创建卷。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgdm9sdW1lIGNyZWF0ZSB0b2RvLWRi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker volume create todo-db
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>再次使用 <code>docker rm -f &lt;id&gt;</code> 停止并移除待办事项应用容器，因为它仍在运行且未使用持久卷。</p>
</li>
<li>
<p>启动待办事项应用容器，但添加 <code>--mount</code> 选项以指定卷挂载。给卷一个名称，并将其挂载到容器中的 <code>/etc/todos</code>，这会捕获在该路径下创建的所有文件。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIC0tbW91bnQgdHlwZT12b2x1bWUsc3JjPXRvZG8tZGIsdGFyZ2V0PS9ldGMvdG9kb3MgZ2V0dGluZy1zdGFydGVk', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -dp 127.0.0.1:3000:3000 --mount <span class="nv">type</span><span class="o">=</span>volume,src<span class="o">=</span>todo-db,target<span class="o">=</span>/etc/todos getting-started
</span></span></code></pre></div>
      
    </div>
  </div>
</div>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>如果你使用 Git Bash，必须为此命令使用不同的语法。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIC0tbW91bnQgdHlwZT12b2x1bWUsc3JjPXRvZG8tZGIsdGFyZ2V0PS8vZXRjL3RvZG9zIGdldHRpbmctc3RhcnRlZA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -dp 127.0.0.1:3000:3000 --mount <span class="nv">type</span><span class="o">=</span>volume,src<span class="o">=</span>todo-db,target<span class="o">=</span>//etc/todos getting-started
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>有关 Git Bash 语法差异的更多详细信息，请参阅

  <a class="link" href="/desktop/troubleshoot-and-support/troubleshoot/topics/#docker-commands-failing-in-git-bash">使用 Git Bash</a>。</p>
    </div>
  </blockquote>

</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <p>创建卷：</p>
<ol>
<li>在 Docker Desktop 中选择 <strong>Volumes</strong>。</li>
<li>在 <strong>Volumes</strong> 中，选择 <strong>Create</strong>。</li>
<li>指定 <code>todo-db</code> 作为卷名称，然后选择 <strong>Create</strong>。</li>
</ol>
<p>停止并移除应用容器：</p>
<ol>
<li>在 Docker Desktop 中选择 <strong>Containers</strong>。</li>
<li>在容器的 <strong>Actions</strong> 列中选择 <strong>Delete</strong>。</li>
</ol>
<p>启动挂载了卷的待办事项应用容器：</p>
<ol>
<li>
<p>选择 Docker Desktop 顶部的搜索框。</p>
</li>
<li>
<p>在搜索窗口中，选择 <strong>Images</strong> 选项卡。</p>
</li>
<li>
<p>在搜索框中，指定镜像名称 <code>getting-started</code>。</p>


  

  <blockquote
    
    class="admonition admonition-tip admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_5432_1749" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="4" y="1" width="17" height="22">
<path d="M9.93896 22H14.939M10.439 10H14.439M12.439 10L12.439 16M15.439 15.3264C17.8039 14.2029 19.439 11.7924 19.439 9C19.439 5.13401 16.305 2 12.439 2C8.57297 2 5.43896 5.13401 5.43896 9C5.43896 11.7924 7.07402 14.2029 9.43896 15.3264V16C9.43896 16.9319 9.43896 17.3978 9.59121 17.7654C9.79419 18.2554 10.1835 18.6448 10.6736 18.8478C11.0411 19 11.5071 19 12.439 19C13.3708 19 13.8368 19 14.2043 18.8478C14.6944 18.6448 15.0837 18.2554 15.2867 17.7654C15.439 17.3978 15.439 16.9319 15.439 16V15.3264Z" stroke="#6C7E9D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#mask0_5432_1749)">
<rect width="24" height="24" fill="currentColor" fill-opacity="0.8"/>
</g>
</svg>

      </span>
      <span class="admonition-title">
        Tip
      </span>
    </div>
    <div class="admonition-content">
      <p>使用搜索过滤器过滤镜像，仅显示 <strong>Local images</strong>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择你的镜像，然后选择 <strong>Run</strong>。</p>
</li>
<li>
<p>选择 <strong>Optional settings</strong>。</p>
</li>
<li>
<p>在 <strong>Host port</strong> 中，指定端口，例如 <code>3000</code>。</p>
</li>
<li>
<p>在 <strong>Host path</strong> 中，指定卷的名称 <code>todo-db</code>。</p>
</li>
<li>
<p>在 <strong>Container path</strong> 中，指定 <code>/etc/todos</code>。</p>
</li>
<li>
<p>选择 <strong>Run</strong>。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


### 验证数据是否持久化

1. 容器启动后，打开应用并向你的待办事项列表添加几个项目。

    ![添加到待办事项列表的项目](images/items-added.webp)
    

2. 停止并移除待办事项应用的容器。使用 Docker Desktop 或 `docker ps` 获取 ID，然后使用 `docker rm -f <id>` 移除它。

3. 使用之前的步骤启动一个新容器。

4. 打开应用。你应该会看到你的项目仍在列表中。

5. 检查完列表后，继续移除容器。

你现在已学会如何持久化数据。

## 深入了解卷

很多人经常问“当我使用卷时，Docker 将我的数据存储在哪里？”如果你想了解，可以使用 `docker volume inspect` 命令。

```console
$ docker volume inspect todo-db
```
你应该会看到类似以下的输出：
```console
[
    {
        "CreatedAt": "2019-09-26T02:18:36Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/todo-db/_data",
        "Name": "todo-db",
        "Options": {},
        "Scope": "local"
    }
]
```

`Mountpoint` 是磁盘上数据的实际位置。请注意，在大多数机器上，你需要 root 权限才能从主机访问此目录。

## 总结

在本节中，你学习了如何持久化容器数据。

相关信息：

 - [docker CLI 参考](/reference/cli/docker/)
 - [卷](/manuals/engine/storage/volumes.md)

## 下一步

接下来，你将学习如何使用绑定挂载更高效地开发你的应用。


<a class="button not-prose" href="/get-started/workshop/06_bind_mounts/">使用绑定挂载</a>

