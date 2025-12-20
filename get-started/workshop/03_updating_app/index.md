# 更新应用程序

在[第1部分](./02_our_app.md)中，你已经将一个待办事项应用程序容器化。在本部分中，你将更新应用程序和镜像。你还将学习如何停止和删除容器。

## 更新源代码

在接下来的步骤中，你将把没有待办事项列表项时的“空文本”更改为“你还没有待办事项！在上面添加一个！”

1. 在 `src/static/js/app.js` 文件中，更新第56行以使用新的空文本。

   ```diff
   - <p className="text-center">No items yet! Add one above!</p>
   + <p className="text-center">You have no todo items yet! Add one above!</p>
   ```

2. 使用 `docker build` 命令构建更新版本的镜像。

   ```console
   $ docker build -t getting-started .
   ```

3. 使用更新后的代码启动一个新容器。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

你可能会看到如下错误：

```console
docker: Error response from daemon: driver failed programming external connectivity on endpoint laughing_burnell 
(bb242b2ca4d67eba76e79474fb36bb5125708ebdabd7f45c8eaf16caaabde9dd): Bind for 127.0.0.1:3000 failed: port is already allocated.
```

该错误发生是因为在旧容器仍在运行时，你无法启动新容器。原因是旧容器已经使用了主机的3000端口，而一台机器上（包括容器）只能有一个进程监听特定端口。要解决此问题，你需要删除旧容器。

## 删除旧容器

要删除容器，首先需要停止它。一旦停止，你就可以将其删除。你可以使用CLI或Docker Desktop的图形界面删除旧容器。选择你最习惯的方式。








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
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="使用cli删除容器">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8cli%e5%88%a0%e9%99%a4%e5%ae%b9%e5%99%a8">
    使用CLI删除容器
  </a>
</h3>

<ol>
<li>
<p>使用 <code>docker ps</code> 命令获取容器的ID。</p>
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
</li>
<li>
<p>使用 <code>docker stop</code> 命令停止容器。将 <code>&lt;the-container-id&gt;</code> 替换为 <code>docker ps</code> 中的ID。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgc3RvcCA8dGhlLWNvbnRhaW5lci1pZD4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker stop &lt;the-container-id&gt;
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>容器停止后，使用 <code>docker rm</code> 命令将其删除。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcm0gPHRoZS1jb250YWluZXItaWQ&#43;', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker rm &lt;the-container-id&gt;
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>


  

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
      <p>你可以通过在 <code>docker rm</code> 命令中添加 <code>force</code> 标志来一次性停止并删除容器。例如：<code>docker rm -f &lt;the-container-id&gt;</code></p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="使用docker-desktop删除容器">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8docker-desktop%e5%88%a0%e9%99%a4%e5%ae%b9%e5%99%a8">
    使用Docker Desktop删除容器
  </a>
</h3>

<ol>
<li>打开Docker Desktop，进入<strong>Containers</strong>视图。</li>
<li>在<strong>Actions</strong>列中，选择要删除容器的垃圾桶图标。</li>
<li>在确认对话框中，选择<strong>Delete forever</strong>。</li>
</ol>

      </div>
    
  </div>
</div>


### 启动更新后的应用程序容器

1. 现在，使用 `docker run` 命令启动更新后的应用程序。

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

2. 刷新浏览器中的 [http://localhost:3000](http://localhost:3000)，你应该会看到更新后的帮助文本。

## 总结

在本节中，你学习了如何更新和重建镜像，以及如何停止和删除容器。

相关信息：
 - [docker CLI参考文档](/reference/cli/docker/)

## 下一步

接下来，你将学习如何与他人共享镜像。


<a class="button not-prose" href="/get-started/workshop/04_sharing_app/">共享应用程序</a>

