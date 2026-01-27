# docker sandbox create cagent

**Description:** Create a sandbox for cagent

**Usage:** `docker sandbox create cagent WORKSPACE`



<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHNhbmRib3ggY3JlYXRlIGNhZ2VudA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker sandbox create cagent</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>创建一个新的容器代理（Container Agent）沙箱环境。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="参数">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%8f%82%e6%95%b0">
    参数
  </a>
</h3>

<p>无</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="示例">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%a4%ba%e4%be%8b">
    示例
  </a>
</h3>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHNhbmRib3ggY3JlYXRlIGNhZ2VudA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker sandbox create cagent</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>该命令将创建一个新的容器代理沙箱环境，用于运行和管理容器化工作负载。</p>









## Description

Create a sandbox with access to a host workspace for cagent.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host.

Use 'docker sandbox run SANDBOX' to start cagent after creation.







