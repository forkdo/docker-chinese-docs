---
title: docker mcp server disable
url: /reference/cli/docker/mcp/server/server_disable/
parent:
  title: docker mcp server
  url: /reference/cli/docker/mcp/server/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker mcp
    url: /reference/cli/docker/mcp/
  - title: docker mcp server
    url: /reference/cli/docker/mcp/server/
  - title: docker mcp server disable
    url: /reference/cli/docker/mcp/server/server_disable/
next:
  title: 
  url: /reference/cli/docker/mcp/server/server_inspect/
prev:
  title: docker mcp server enable
  url: /reference/cli/docker/mcp/server/server_enable/
---

**Description:** Disable a server or multiple servers

**Usage:** `docker mcp server disable`

**Aliases:** `docker mcp server remove`, `docker mcp server rm`

<!--
此页面由 Docker 的源代码自动生成。如果您想
建议更改此处显示的文本，请在 GitHub 上的
源代码仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->

<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-mcp-server-disable">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-mcp-server-disable">
    docker mcp server disable
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
        x-data="{ code: 'ZG9ja2VyIG1jcCBzZXJ2ZXIgZGlzYWJsZSBbT1BUSU9OU10gU0VSVkVS', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker mcp server disable <span class="o">[</span>OPTIONS<span class="o">]</span> SERVER</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<!-- MARKDOWN CODE BLOCK: info -->
<!-- MARKDOWN CODE BLOCK: options -->
<!-- MARKDOWN CODE BLOCK: examples -->
<!-- MARKDOWN CODE BLOCK: inherited -->
<!-- MARKDOWN CODE BLOCK: see also -->
<p><strong>说明：</strong></p>
<p>此命令用于禁用已注册的 MCP 服务器。服务器被禁用后，将不再可用于处理工具调用或提示，但其注册信息仍会保留在注册表中，以便将来重新启用。</p>
<p><strong>示例：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDnpoHnlKjlkI3kuLogIm15LXNlcnZlciIg55qE5pyN5Yqh5ZmoCmRvY2tlciBtY3Agc2VydmVyIGRpc2FibGUgbXktc2VydmVyCgojIOemgeeUqOacjeWKoeWZqOW5tuafpeeci&#43;eKtuaAgeWPmOabtApkb2NrZXIgbWNwIHNlcnZlciBkaXNhYmxlIG15LXNlcnZlcgpkb2NrZXIgbWNwIHNlcnZlciBsaXN0', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="c1"># 禁用名为 &#34;my-server&#34; 的服务器</span>
</span></span><span class="line"><span class="cl">docker mcp server disable my-server
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 禁用服务器并查看状态变更</span>
</span></span><span class="line"><span class="cl">docker mcp server disable my-server
</span></span><span class="line"><span class="cl">docker mcp server list</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>相关命令：</strong></p>
<table>
  <thead>
      <tr>
          <th>命令</th>
          <th>描述</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><code>docker mcp server enable</code></td>
          <td>启用已禁用的服务器</td>
      </tr>
      <tr>
          <td><code>docker mcp server list</code></td>
          <td>列出所有服务器及其状态</td>
      </tr>
      <tr>
          <td><code>docker mcp server remove</code></td>
          <td>从注册表中移除服务器</td>
      </tr>
  </tbody>
</table>
<p><strong>使用说明：</strong></p>
<ul>
<li>此命令需要有效的服务器名称作为参数</li>
<li>被禁用的服务器不会从系统中删除</li>
<li>可以随时使用 <code>enable</code> 命令重新启用服务器</li>
<li>禁用操作是即时生效的，无需重启服务</li>
</ul>









## Description

Disable a server or multiple servers







