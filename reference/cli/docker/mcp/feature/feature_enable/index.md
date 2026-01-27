# docker mcp feature enable

**Description:** Enable an experimental feature

**Usage:** `docker mcp feature enable <feature-name>`



<!--
此页面内容自动从 Docker 的源代码生成。如果您想建议修改此处显示的文本，请在 GitHub 上的源代码仓库中提交工单或拉取请求：

https://github.com/docker/mcp-gateway
-->

<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-mcp-feature-enable">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-mcp-feature-enable">
    docker mcp feature enable
  </a>
</h1>

<!-- MARKDOWN-ANCHOR: docker mcp feature enable -->
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIG1jcCBmZWF0dXJlIGVuYWJsZSBbT1BUSU9OU10gRkVBVFVSRQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">docker mcp feature enable [OPTIONS] FEATURE</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>启用指定的 MCP 功能。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="选项">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%80%89%e9%a1%b9">
    选项
  </a>
</h3>

<!-- MARKDOWN-ANCHOR: Options -->
<table>
  <thead>
      <tr>
          <th>名称</th>
          <th>简写</th>
          <th>默认值</th>
          <th>描述</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><code>--format</code></td>
          <td></td>
          <td><code>pretty</code></td>
          <td>格式化输出<br>支持的值：<code>pretty</code>、<code>json</code>、<code>jsona</code></td>
      </tr>
      <tr>
          <td><code>--help</code></td>
          <td><code>-h</code></td>
          <td></td>
          <td>显示帮助信息</td>
      </tr>
  </tbody>
</table>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="描述">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8f%8f%e8%bf%b0">
    描述
  </a>
</h3>

<p>启用指定的 MCP 功能。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="示例">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%a4%ba%e4%be%8b">
    示例
  </a>
</h3>

<!-- MARKDOWN-ANCHOR: Examples -->
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDlkK/nlKggZG9ja2VyLm1jcCDlip/og70KZG9ja2VyIG1jcCBmZWF0dXJlIGVuYWJsZSBkb2NrZXIubWNwCgojIOS7pSBKU09OIOagvOW8j&#43;i&#43;k&#43;WHugpkb2NrZXIgbWNwIGZlYXR1cmUgZW5hYmxlIGRvY2tlci5tY3AgLS1mb3JtYXQganNvbg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="c1"># 启用 docker.mcp 功能</span>
</span></span><span class="line"><span class="cl">docker mcp feature <span class="nb">enable</span> docker.mcp
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 以 JSON 格式输出</span>
</span></span><span class="line"><span class="cl">docker mcp feature <span class="nb">enable</span> docker.mcp --format json</span></span></code></pre></div>
      
    </div>
  </div>
</div>









## Description

Enable an experimental feature.

Available features:
  oauth-interceptor      Enable GitHub OAuth flow interception for automatic authentication
  mcp-oauth-dcr          Enable Dynamic Client Registration (DCR) for automatic OAuth client setup
  dynamic-tools          Enable internal MCP management tools (mcp-find, mcp-add, mcp-remove)







