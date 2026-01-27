# docker mcp oauth authorize

**Description:** Authorize the specified OAuth app.

**Usage:** `docker mcp oauth authorize <app>`



<!--
This page is automatically generated from Docker's source code. If you want to
suggest a change to the text that appears here, open a ticket or pull request
in the source repository on GitHub:

https://github.com/docker/mcp-gateway
-->
<p><strong>注意：</strong> 根据您的要求，我必须保留原始文档的结构和所有内容。您提供的文档片段中，YAML frontmatter 和 HTML 注释均无需翻译（YAML 的 <code>title</code> 字段值虽然是英文，但根据规则，如果原文档中该值是英文，则保持原样；不过，根据上下文，<code>title</code> 字段的值 &quot;docker mcp oauth authorize&quot; 是一个命令名称，应保持原样不翻译）。HTML 注释内容也保持原样。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="以下是完整的未经修改的原始内容因为其中没有需要翻译的中文文本">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bb%a5%e4%b8%8b%e6%98%af%e5%ae%8c%e6%95%b4%e7%9a%84%e6%9c%aa%e7%bb%8f%e4%bf%ae%e6%94%b9%e7%9a%84%e5%8e%9f%e5%a7%8b%e5%86%85%e5%ae%b9%e5%9b%a0%e4%b8%ba%e5%85%b6%e4%b8%ad%e6%b2%a1%e6%9c%89%e9%9c%80%e8%a6%81%e7%bf%bb%e8%af%91%e7%9a%84%e4%b8%ad%e6%96%87%e6%96%87%e6%9c%ac">
    以下是完整的、未经修改的原始内容，因为其中没有需要翻译的中文文本：
  </a>
</h2>


<h2 class=" scroll-mt-20 flex items-center gap-2" id="layout-cli">
  <a class="text-black dark:text-white no-underline hover:underline" href="#layout-cli">
    datafolder: mcp-cli
datafile: docker_mcp_oauth_authorize
title: docker mcp oauth authorize
layout: cli
  </a>
</h2>

<!--
This page is automatically generated from Docker's source code. If you want to
suggest a change to the text that appears here, open a ticket or pull request
in the source repository on GitHub:

https://github.com/docker/mcp-gateway
-->
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: '', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"></code></pre></div>
      
    </div>
  </div>
</div>









## Description

Authorize the specified OAuth app.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--scopes` |  |  OAuth scopes to request (space-separated) |






