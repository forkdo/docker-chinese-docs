# 使用 bind mounts

在[第 4 部分](./05_persisting_data.md)中，您使用了卷挂载来持久化数据库中的数据。当您需要一个持久化的位置来存储应用程序数据时，卷挂载是一个很好的选择。

bind mount 是另一种挂载类型，它允许您将主机文件系统中的目录共享到容器中。在开发应用程序时，您可以使用 bind mount 将源代码挂载到容器中。容器会立即看到您对代码所做的更改，一旦您保存文件。这意味着您可以在容器中运行监视文件系统更改并对其做出响应的进程。

在本章中，您将看到如何使用 bind mounts 和一个名为 [nodemon](https://npmjs.com/package/nodemon) 的工具来监视文件更改，然后自动重启应用程序。大多数其他语言和框架都有类似工具。

## 快速卷类型比较

以下是使用 `--mount` 的命名卷和 bind mount 的示例：

- 命名卷：`type=volume,src=my-volume,target=/usr/local/data`
- Bind mount：`type=bind,src=/path/to/data,target=/usr/local/data`

下表概述了卷挂载和 bind mount 之间的主要区别。

|                                              | 命名卷                                          | Bind mounts                                      |
| -------------------------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| 主机位置                                     | Docker 选择                                      | 您决定                                           |
| 使用容器内容填充新卷                         | 是                                               | 否                                               |
| 支持卷驱动                                   | 是                                               | 否                                               |

## 尝试使用 bind mounts

在了解如何使用 bind mounts 开发应用程序之前，您可以运行一个快速实验，以实际了解 bind mounts 的工作原理。

1. 验证您的 `getting-started-app` 目录是否位于 Docker Desktop 文件共享设置中定义的目录中。此设置定义了您可以与容器共享的文件系统的哪些部分。有关访问该设置的详细信息，请参阅 [文件共享](/manuals/desktop/settings-and-maintenance/settings.md#file-sharing)。

    > [!NOTE]
    > **文件共享**选项卡仅在 Hyper-V 模式下可用，因为在 WSL 2 模式和 Windows 容器模式下文件会自动共享。

2. 打开终端并切换到 `getting-started-app` 目录。

3. 运行以下命令，使用 bind mount 在 `ubuntu` 容器中启动 `bash`。

   






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
    
      <button
        class="tab-item"
        :class="selected === 'PowerShell' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'PowerShell'"
        
      >
        PowerShell
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
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1pdCAtLW1vdW50IHR5cGU9YmluZCxzcmM9IiQocHdkKSIsdGFyZ2V0PS9zcmMgdWJ1bnR1IGJhc2g=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -it --mount <span class="nv">type</span><span class="o">=</span>bind,src<span class="o">=</span><span class="s2">&#34;</span><span class="k">$(</span><span class="nb">pwd</span><span class="k">)</span><span class="s2">&#34;</span>,target<span class="o">=</span>/src ubuntu bash
</span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1pdCAtLW1vdW50ICJ0eXBlPWJpbmQsc3JjPSVjZCUsdGFyZ2V0PS9zcmMiIHVidW50dSBiYXNo', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -it --mount <span class="s2">&#34;type=bind,src=%cd%,target=/src&#34;</span> ubuntu bash
</span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1pdCAtLW1vdW50IHR5cGU9YmluZCxzcmM9Ii8kKHB3ZCkiLHRhcmdldD0vc3JjIHVidW50dSBiYXNo', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -it --mount <span class="nv">type</span><span class="o">=</span>bind,src<span class="o">=</span><span class="s2">&#34;/</span><span class="k">$(</span><span class="nb">pwd</span><span class="k">)</span><span class="s2">&#34;</span>,target<span class="o">=</span>/src ubuntu bash
</span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1pdCAtLW1vdW50ICJ0eXBlPWJpbmQsc3JjPSQoJHB3ZCksdGFyZ2V0PS9zcmMiIHVidW50dSBiYXNo', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -it --mount <span class="s2">&#34;type=bind,src=</span><span class="k">$(</span><span class="nv">$pwd</span><span class="k">)</span><span class="s2">,target=/src&#34;</span> ubuntu bash
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

   
   `--mount type=bind` 选项告诉 Docker 创建 bind mount，其中 `src` 是主机上的当前工作目录（`getting-started-app`），而 `target` 是该目录在容器内应出现的位置（`/src`）。

4. 运行命令后，Docker 在容器的文件系统根目录中启动交互式 `bash` 会话。

   ```console
   root@ac1237fad8db:/# pwd
   /
   root@ac1237fad8db:/# ls
   bin   dev  home  media  opt   root  sbin  srv  tmp  var
   boot  etc  lib   mnt    proc  run   src   sys  usr
   ```

5. 切换到 `src` 目录。

   这是启动容器时挂载的目录。列出此目录的内容将显示与主机上 `getting-started-app` 目录中相同的文件。

   ```console
   root@ac1237fad8db:/# cd src
   root@ac1237fad8db:/src# ls
   Dockerfile  node_modules  package.json  spec  src  yarn.lock
   ```

6. 创建一个名为 `myfile.txt` 的新文件。

   ```console
   root@ac1237fad8db:/src# touch myfile.txt
   root@ac1237fad8db:/src# ls
   Dockerfile  myfile.txt  node_modules  package.json  spec  src  yarn.lock
   ```

7. 在主机上打开 `getting-started-app` 目录，并观察 `myfile.txt` 文件是否在目录中。

   ```text
   ├── getting-started-app/
   │ ├── Dockerfile
   │ ├── myfile.txt
   │ ├── node_modules/
   │ ├── package.json
   │ ├── spec/
   │ ├── src/
   │ └── yarn.lock
   ```

8. 从主机上删除 `myfile.txt` 文件。
9. 在容器中，再次列出 `app` 目录的内容。观察该文件现在已消失。

   ```console
   root@ac1237fad8db:/src# ls
   Dockerfile  node_modules  package.json  spec  src  yarn.lock
   ```

10. 使用 `Ctrl` + `D` 停止交互式容器会话。

这就是对 bind mounts 的简要介绍。此过程演示了文件如何在主机和容器之间共享，以及如何立即在两侧反映更改。现在您可以使用 bind mounts 来开发软件。

## 开发容器

使用 bind mounts 对于本地开发设置很常见。其优点是开发机器不需要安装所有构建工具和开发环境。只需一条 docker run 命令，Docker 就会拉取依赖项和工具。

### 在开发容器中运行您的应用

以下步骤描述了如何使用 bind mount 运行开发容器，该容器将执行以下操作：

- 将源代码挂载到容器中
- 安装所有依赖项
- 启动 `nodemon` 以监视文件系统更改

您可以使用 CLI 或 Docker Desktop 通过 bind mount 运行容器。








<div
  class="tabs"
  
    x-data="{ selected: 'Mac-/-Linux-CLI' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Mac-/-Linux-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac-/-Linux-CLI'"
        
      >
        Mac / Linux CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'PowerShell-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'PowerShell-CLI'"
        
      >
        PowerShell CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Command-Prompt-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Command-Prompt-CLI'"
        
      >
        Command Prompt CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Git-Bash-CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Git-Bash-CLI'"
        
      >
        Git Bash CLI
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
        :class="selected !== 'Mac-/-Linux-CLI' && 'hidden'"
      >
        <ol>
<li>
<p>确保当前没有运行任何 <code>getting-started</code> 容器。</p>
</li>
<li>
<p>从 <code>getting-started-app</code> 目录运行以下命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIFwKICAgIC13IC9hcHAgLS1tb3VudCB0eXBlPWJpbmQsc3JjPSIkKHB3ZCkiLHRhcmdldD0vYXBwIFwKICAgIG5vZGU6bHRzLWFscGluZSBcCiAgICBzaCAtYyAieWFybiBpbnN0YWxsICYmIHlhcm4gcnVuIGRldiI=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="go">    -w /app --mount type=bind,src=&#34;$(pwd)&#34;,target=/app \
</span></span></span><span class="line"><span class="cl"><span class="go">    node:lts-alpine \
</span></span></span><span class="line"><span class="cl"><span class="go">    sh -c &#34;yarn install &amp;&amp; yarn run dev&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>以下是命令的详细说明：</p>
<ul>
<li><code>-dp 127.0.0.1:3000:3000</code> - 与之前相同。在分离（后台）模式下运行并创建端口映射</li>
<li><code>-w /app</code> - 设置“工作目录”或命令将运行的当前目录</li>
<li><code>--mount type=bind,src=&quot;$(pwd)&quot;,target=/app</code> - 将主机的当前目录 bind mount 到容器中的 <code>/app</code> 目录</li>
<li><code>node:lts-alpine</code> - 要使用的镜像。请注意，这是 Dockerfile 中应用的基础镜像</li>
<li><code>sh -c &quot;yarn install &amp;&amp; yarn run dev&quot;</code> - 命令。您使用 <code>sh</code>（alpine 没有 <code>bash</code>）启动一个 shell，运行 <code>yarn install</code> 安装包，然后运行 <code>yarn run dev</code> 启动开发服务器。如果您查看 <code>package.json</code>，您会看到 <code>dev</code> 脚本启动了 <code>nodemon</code>。</li>
</ul>
</li>
<li>
<p>您可以使用 <code>docker logs &lt;container-id&gt;</code> 查看日志。当您看到以下内容时，表示已准备就绪：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbG9ncyAtZiA8Y29udGFpbmVyLWlkPgpub2RlbW9uIC1MIHNyYy9pbmRleC5qcwpbbm9kZW1vbl0gMi4wLjIwCltub2RlbW9uXSB0byByZXN0YXJ0IGF0IGFueSB0aW1lLCBlbnRlciBgcnNgCltub2RlbW9uXSB3YXRjaGluZyBwYXRoKHMpOiAqLioKW25vZGVtb25dIHdhdGNoaW5nIGV4dGVuc2lvbnM6IGpzLG1qcyxqc29uCltub2RlbW9uXSBzdGFydGluZyBgbm9kZSBzcmMvaW5kZXguanNgClVzaW5nIHNxbGl0ZSBkYXRhYmFzZSBhdCAvZXRjL3RvZG9zL3RvZG8uZGIKTGlzdGVuaW5nIG9uIHBvcnQgMzAwMA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker logs -f &lt;container-id&gt;
</span></span><span class="line"><span class="cl"><span class="go">nodemon -L src/index.js
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] 2.0.20
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] to restart at any time, enter `rs`
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching path(s): *.*
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching extensions: js,mjs,json
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] starting `node src/index.js`
</span></span></span><span class="line"><span class="cl"><span class="go">Using sqlite database at /etc/todos/todo.db
</span></span></span><span class="line"><span class="cl"><span class="go">Listening on port 3000
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>查看完日志后，按 <code>Ctrl</code>+<code>C</code> 退出。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'PowerShell-CLI' && 'hidden'"
      >
        <ol>
<li>
<p>确保当前没有运行任何 <code>getting-started</code> 容器。</p>
</li>
<li>
<p>从 <code>getting-started-app</code> 目录运行以下命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIGAKICAgIC13IC9hcHAgLS1tb3VudCAidHlwZT1iaW5kLHNyYz0kcHdkLHRhcmdldD0vYXBwIiBgCiAgICBub2RlOmx0cy1hbHBpbmUgYAogICAgc2ggLWMgInlhcm4gaW5zdGFsbCAmJiB5YXJuIHJ1biBkZXYi', copying: false }"
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
</span></span><span class="line"><span class="cl">    <span class="n">-w</span> <span class="p">/</span><span class="n">app</span> <span class="p">-</span><span class="n">-mount</span> <span class="s2">&#34;type=bind,src=</span><span class="nv">$pwd</span><span class="s2">,target=/app&#34;</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">    <span class="n">node</span><span class="err">:</span><span class="nb">lts-alpine</span> <span class="p">`</span>
</span></span><span class="line"><span class="cl">    <span class="n">sh</span> <span class="n">-c</span> <span class="s2">&#34;yarn install &amp;&amp; yarn run dev&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>以下是命令的详细说明：</p>
<ul>
<li><code>-dp 127.0.0.1:3000:3000</code> - 与之前相同。在分离（后台）模式下运行并创建端口映射</li>
<li><code>-w /app</code> - 设置“工作目录”或命令将运行的当前目录</li>
<li><code>--mount &quot;type=bind,src=$pwd,target=/app&quot;</code> - 将主机的当前目录 bind mount 到容器中的 <code>/app</code> 目录</li>
<li><code>node:lts-alpine</code> - 要使用的镜像。请注意，这是 Dockerfile 中应用的基础镜像</li>
<li><code>sh -c &quot;yarn install &amp;&amp; yarn run dev&quot;</code> - 命令。您使用 <code>sh</code>（alpine 没有 <code>bash</code>）启动一个 shell，运行 <code>yarn install</code> 安装包，然后运行 <code>yarn run dev</code> 启动开发服务器。如果您查看 <code>package.json</code>，您会看到 <code>dev</code> 脚本启动了 <code>nodemon</code>。</li>
</ul>
</li>
<li>
<p>您可以使用 <code>docker logs &lt;container-id&gt;</code> 查看日志。当您看到以下内容时，表示已准备就绪：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbG9ncyAtZiA8Y29udGFpbmVyLWlkPgpub2RlbW9uIC1MIHNyYy9pbmRleC5qcwpbbm9kZW1vbl0gMi4wLjIwCltub2RlbW9uXSB0byByZXN0YXJ0IGF0IGFueSB0aW1lLCBlbnRlciBgcnNgCltub2RlbW9uXSB3YXRjaGluZyBwYXRoKHMpOiAqLioKW25vZGVtb25dIHdhdGNoaW5nIGV4dGVuc2lvbnM6IGpzLG1qcyxqc29uCltub2RlbW9uXSBzdGFydGluZyBgbm9kZSBzcmMvaW5kZXguanNgClVzaW5nIHNxbGl0ZSBkYXRhYmFzZSBhdCAvZXRjL3RvZG9zL3RvZG8uZGIKTGlzdGVuaW5nIG9uIHBvcnQgMzAwMA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker logs -f &lt;container-id&gt;
</span></span><span class="line"><span class="cl"><span class="go">nodemon -L src/index.js
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] 2.0.20
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] to restart at any time, enter `rs`
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching path(s): *.*
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching extensions: js,mjs,json
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] starting `node src/index.js`
</span></span></span><span class="line"><span class="cl"><span class="go">Using sqlite database at /etc/todos/todo.db
</span></span></span><span class="line"><span class="cl"><span class="go">Listening on port 3000
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>查看完日志后，按 <code>Ctrl</code>+<code>C</code> 退出。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Command-Prompt-CLI' && 'hidden'"
      >
        <ol>
<li>
<p>确保当前没有运行任何 <code>getting-started</code> 容器。</p>
</li>
<li>
<p>从 <code>getting-started-app</code> 目录运行以下命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIF4KICAgIC13IC9hcHAgLS1tb3VudCAidHlwZT1iaW5kLHNyYz0lY2QlLHRhcmdldD0vYXBwIiBeCiAgICBub2RlOmx0cy1hbHBpbmUgXgogICAgc2ggLWMgInlhcm4gaW5zdGFsbCAmJiB5YXJuIHJ1biBkZXYi', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="go">    -w /app --mount &#34;type=bind,src=%cd%,target=/app&#34; ^
</span></span></span><span class="line"><span class="cl"><span class="go">    node:lts-alpine ^
</span></span></span><span class="line"><span class="cl"><span class="go">    sh -c &#34;yarn install &amp;&amp; yarn run dev&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>以下是命令的详细说明：</p>
<ul>
<li><code>-dp 127.0.0.1:3000:3000</code> - 与之前相同。在分离（后台）模式下运行并创建端口映射</li>
<li><code>-w /app</code> - 设置“工作目录”或命令将运行的当前目录</li>
<li><code>--mount &quot;type=bind,src=%cd%,target=/app&quot;</code> - 将主机的当前目录 bind mount 到容器中的 <code>/app</code> 目录</li>
<li><code>node:lts-alpine</code> - 要使用的镜像。请注意，这是 Dockerfile 中应用的基础镜像</li>
<li><code>sh -c &quot;yarn install &amp;&amp; yarn run dev&quot;</code> - 命令。您使用 <code>sh</code>（alpine 没有 <code>bash</code>）启动一个 shell，运行 <code>yarn install</code> 安装包，然后运行 <code>yarn run dev</code> 启动开发服务器。如果您查看 <code>package.json</code>，您会看到 <code>dev</code> 脚本启动了 <code>nodemon</code>。</li>
</ul>
</li>
<li>
<p>您可以使用 <code>docker logs &lt;container-id&gt;</code> 查看日志。当您看到以下内容时，表示已准备就绪：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbG9ncyAtZiA8Y29udGFpbmVyLWlkPgpub2RlbW9uIC1MIHNyYy9pbmRleC5qcwpbbm9kZW1vbl0gMi4wLjIwCltub2RlbW9uXSB0byByZXN0YXJ0IGF0IGFueSB0aW1lLCBlbnRlciBgcnNgCltub2RlbW9uXSB3YXRjaGluZyBwYXRoKHMpOiAqLioKW25vZGVtb25dIHdhdGNoaW5nIGV4dGVuc2lvbnM6IGpzLG1qcyxqc29uCltub2RlbW9uXSBzdGFydGluZyBgbm9kZSBzcmMvaW5kZXguanNgClVzaW5nIHNxbGl0ZSBkYXRhYmFzZSBhdCAvZXRjL3RvZG9zL3RvZG8uZGIKTGlzdGVuaW5nIG9uIHBvcnQgMzAwMA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker logs -f &lt;container-id&gt;
</span></span><span class="line"><span class="cl"><span class="go">nodemon -L src/index.js
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] 2.0.20
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] to restart at any time, enter `rs`
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching path(s): *.*
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching extensions: js,mjs,json
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] starting `node src/index.js`
</span></span></span><span class="line"><span class="cl"><span class="go">Using sqlite database at /etc/todos/todo.db
</span></span></span><span class="line"><span class="cl"><span class="go">Listening on port 3000
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>查看完日志后，按 <code>Ctrl</code>+<code>C</code> 退出。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Git-Bash-CLI' && 'hidden'"
      >
        <ol>
<li>
<p>确保当前没有运行任何 <code>getting-started</code> 容器。</p>
</li>
<li>
<p>从 <code>getting-started-app</code> 目录运行以下命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1kcCAxMjcuMC4wLjE6MzAwMDozMDAwIFwKICAgIC13IC8vYXBwIC0tbW91bnQgdHlwZT1iaW5kLHNyYz0iLyQocHdkKSIsdGFyZ2V0PS9hcHAgXAogICAgbm9kZTpsdHMtYWxwaW5lIFwKICAgIHNoIC1jICJ5YXJuIGluc3RhbGwgJiYgeWFybiBydW4gZGV2Ig==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="go">    -w //app --mount type=bind,src=&#34;/$(pwd)&#34;,target=/app \
</span></span></span><span class="line"><span class="cl"><span class="go">    node:lts-alpine \
</span></span></span><span class="line"><span class="cl"><span class="go">    sh -c &#34;yarn install &amp;&amp; yarn run dev&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>以下是命令的详细说明：</p>
<ul>
<li><code>-dp 127.0.0.1:3000:3000</code> - 与之前相同。在分离（后台）模式下运行并创建端口映射</li>
<li><code>-w //app</code> - 设置“工作目录”或命令将运行的当前目录</li>
<li><code>--mount type=bind,src=&quot;/$(pwd)&quot;,target=/app</code> - 将主机的当前目录 bind mount 到容器中的 <code>/app</code> 目录</li>
<li><code>node:lts-alpine</code> - 要使用的镜像。请注意，这是 Dockerfile 中应用的基础镜像</li>
<li><code>sh -c &quot;yarn install &amp;&amp; yarn run dev&quot;</code> - 命令。您使用 <code>sh</code>（alpine 没有 <code>bash</code>）启动一个 shell，运行 <code>yarn install</code> 安装包，然后运行 <code>yarn run dev</code> 启动开发服务器。如果您查看 <code>package.json</code>，您会看到 <code>dev</code> 脚本启动了 <code>nodemon</code>。</li>
</ul>
</li>
<li>
<p>您可以使用 <code>docker logs &lt;container-id&gt;</code> 查看日志。当您看到以下内容时，表示已准备就绪：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbG9ncyAtZiA8Y29udGFpbmVyLWlkPgpub2RlbW9uIC1MIHNyYy9pbmRleC5qcwpbbm9kZW1vbl0gMi4wLjIwCltub2RlbW9uXSB0byByZXN0YXJ0IGF0IGFueSB0aW1lLCBlbnRlciBgcnNgCltub2RlbW9uXSB3YXRjaGluZyBwYXRoKHMpOiAqLioKW25vZGVtb25dIHdhdGNoaW5nIGV4dGVuc2lvbnM6IGpzLG1qcyxqc29uCltub2RlbW9uXSBzdGFydGluZyBgbm9kZSBzcmMvaW5kZXguanNgClVzaW5nIHNxbGl0ZSBkYXRhYmFzZSBhdCAvZXRjL3RvZG9zL3RvZG8uZGIKTGlzdGVuaW5nIG9uIHBvcnQgMzAwMA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker logs -f &lt;container-id&gt;
</span></span><span class="line"><span class="cl"><span class="go">nodemon -L src/index.js
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] 2.0.20
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] to restart at any time, enter `rs`
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching path(s): *.*
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching extensions: js,mjs,json
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] starting `node src/index.js`
</span></span></span><span class="line"><span class="cl"><span class="go">Using sqlite database at /etc/todos/todo.db
</span></span></span><span class="line"><span class="cl"><span class="go">Listening on port 3000
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>查看完日志后，按 <code>Ctrl</code>+<code>C</code> 退出。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <p>确保当前没有运行任何 <code>getting-started</code> 容器。</p>
<p>使用 bind mount 运行镜像。</p>
<ol>
<li>
<p>选择 Docker Desktop 顶部的搜索框。</p>
</li>
<li>
<p>在搜索窗口中，选择 <strong>Images</strong> 选项卡。</p>
</li>
<li>
<p>在搜索框中，指定容器名称 <code>getting-started</code>。</p>


  

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
      <p>使用搜索过滤器过滤镜像，仅显示 <strong>本地镜像</strong>。</p>
    </div>
  </blockquote>

</li>
<li>
<p>选择您的镜像，然后选择 <strong>Run</strong>。</p>
</li>
<li>
<p>选择 <strong>Optional settings</strong>。</p>
</li>
<li>
<p>在 <strong>Host path</strong> 中，指定主机上 <code>getting-started-app</code> 目录的路径。</p>
</li>
<li>
<p>在 <strong>Container path</strong> 中，指定 <code>/app</code>。</p>
</li>
<li>
<p>选择 <strong>Run</strong>。</p>
</li>
</ol>
<p>您可以使用 Docker Desktop 查看容器日志。</p>
<ol>
<li>在 Docker Desktop 中选择 <strong>Containers</strong>。</li>
<li>选择您的容器名称。</li>
</ol>
<p>当您看到以下内容时，表示已准备就绪：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bm9kZW1vbiAtTCBzcmMvaW5kZXguanMKW25vZGVtb25dIDIuMC4yMApbbm9kZW1vbl0gdG8gcmVzdGFydCBhdCBhbnkgdGltZSwgZW50ZXIgYHJzYApbbm9kZW1vbl0gd2F0Y2hpbmcgcGF0aChzKTogKi4qCltub2RlbW9uXSB3YXRjaGluZyBleHRlbnNpb25zOiBqcyxtanMsanNvbgpbbm9kZW1vbl0gc3RhcnRpbmcgYG5vZGUgc3JjL2luZGV4LmpzYApVc2luZyBzcWxpdGUgZGF0YWJhc2UgYXQgL2V0Yy90b2Rvcy90b2RvLmRiCkxpc3RlbmluZyBvbiBwb3J0IDMwMDA=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">nodemon -L src/index.js
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] 2.0.20
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] to restart at any time, enter `rs`
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching path(s): *.*
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] watching extensions: js,mjs,json
</span></span></span><span class="line"><span class="cl"><span class="go">[nodemon] starting `node src/index.js`
</span></span></span><span class="line"><span class="cl"><span class="go">Using sqlite database at /etc/todos/todo.db
</span></span></span><span class="line"><span class="cl"><span class="go">Listening on port 3000
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


### 使用开发容器开发您的应用

在主机上更新您的应用，并查看容器中反映的更改。

1. 在 `src/static/js/app.js` 文件的第 109 行，将“Add Item”按钮更改为仅显示“Add”：

   ```diff
   - {submitting ? 'Adding...' : 'Add Item'}
   + {submitting ? 'Adding...' : 'Add'}
   ```

   保存文件。

2. 刷新网页浏览器中的页面，您应该几乎立即看到更改，因为 bind mount。Nodemon 检测到更改并重启服务器。Node 服务器重启可能需要几秒钟。如果遇到错误，请等待几秒后重试刷新。

   ![更新后的“Add”按钮标签截图](images/updated-add-button.webp)

3. 您可以随意进行其他所需的更改。每次进行更改并保存文件时，由于 bind mount，更改都会反映在容器中。当 Nodemon 检测到更改时，它会自动在容器内重启应用。完成后，停止容器并使用以下命令构建新镜像：

   ```console
   $ docker build -t getting-started .
   ```

## 总结

至此，您可以持久化数据库，并在开发过程中看到应用的更改，而无需重建镜像。

除了卷挂载和 bind mounts 之外，Docker 还支持其他挂载类型和存储驱动，以处理更复杂和特殊的使用场景。

相关信息：

 - [docker CLI 参考](/reference/cli/docker/)
 - [管理 Docker 中的数据](https://docs.docker.com/storage/)

## 下一步

为了准备将您的应用部署到生产环境，您需要将数据库从 SQLite 迁移到可以更好扩展的数据库。为简化起见，您将继续使用关系型数据库，并将应用切换为使用 MySQL。但是，您应该如何运行 MySQL？如何允许容器相互通信？您将在下一节中了解这些内容。


<a class="button not-prose" href="/get-started/workshop/07_multi_container/">多容器应用</a>

