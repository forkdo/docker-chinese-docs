# docker desktop restart

**Description:** Restart Docker Desktop

**Usage:** `docker desktop restart`




<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-desktop-restart">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-desktop-restart">
    docker desktop restart
  </a>
</h1>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: '55So5rOV77yaZG9ja2VyIGRlc2t0b3AgcmVzdGFydCBb6YCJ6aG5XQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">用法：docker desktop restart [选项]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>重新启动 Docker Desktop。</p>
<p><strong>注意</strong>：此命令仅在 Docker Desktop 的 CLI 模式下可用。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="选项">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%80%89%e9%a1%b9">
    选项
  </a>
</h3>

<table>
  <thead>
      <tr>
          <th>选项</th>
          <th>类型</th>
          <th>默认值</th>
          <th>描述</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><code>--wait</code></td>
          <td>bool</td>
          <td><code>false</code></td>
          <td>等待 Docker Desktop 完全启动后再返回</td>
      </tr>
  </tbody>
</table>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="示例">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%a4%ba%e4%be%8b">
    示例
  </a>
</h3>


<h4 class=" scroll-mt-20 flex items-center gap-2" id="重新启动-docker-desktop">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%87%8d%e6%96%b0%e5%90%af%e5%8a%a8-docker-desktop">
    重新启动 Docker Desktop
  </a>
</h4>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIGRlc2t0b3AgcmVzdGFydA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker desktop restart</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h4 class=" scroll-mt-20 flex items-center gap-2" id="重新启动-docker-desktop-并等待其完全启动">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%87%8d%e6%96%b0%e5%90%af%e5%8a%a8-docker-desktop-%e5%b9%b6%e7%ad%89%e5%be%85%e5%85%b6%e5%ae%8c%e5%85%a8%e5%90%af%e5%8a%a8">
    重新启动 Docker Desktop 并等待其完全启动
  </a>
</h4>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIGRlc2t0b3AgcmVzdGFydCAtLXdhaXQ=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker desktop restart --wait</span></span></code></pre></div>
      
    </div>
  </div>
</div>











## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--detach` |  |  Do not synchronously wait for the requested operation to complete. |
| `--timeout` |  |  Terminate the running command after the specified timeout with a non-zero exit code. A value of zero (the default) or -1 means no timeout.<br> |






