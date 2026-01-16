---
title: docker sandbox inspect
url: /reference/cli/docker/sandbox/inspect/
parent:
  title: Docker 沙箱
  url: /reference/cli/docker/sandbox/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: Docker 沙箱
    url: /reference/cli/docker/sandbox/
  - title: docker sandbox inspect
    url: /reference/cli/docker/sandbox/inspect/
next:
  title: 
  url: /reference/cli/docker/sandbox/version/
prev:
  title: docker sandbox ls
  url: /reference/cli/docker/sandbox/ls/
---

**Description:** Display detailed information on one or more sandboxes

**Usage:** `docker sandbox inspect [OPTIONS] SANDBOX [SANDBOX...]`




<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-sandbox-inspect">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-sandbox-inspect">
    docker sandbox inspect
  </a>
</h1>


<h2 class=" scroll-mt-20 flex items-center gap-2" id="描述">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8f%8f%e8%bf%b0">
    描述
  </a>
</h2>

<p>显示一个或多个沙盒的详细信息</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="使用方法">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8%e6%96%b9%e6%b3%95">
    使用方法
  </a>
</h2>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIHNhbmRib3ggaW5zcGVjdCBbT1BUSU9OU10gU0FOREJPWCBbU0FOREJPWC4uLl0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-shell" data-lang="shell"><span class="line"><span class="cl">docker sandbox inspect <span class="o">[</span>OPTIONS<span class="o">]</span> SANDBOX <span class="o">[</span>SANDBOX...<span class="o">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="选项">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%80%89%e9%a1%b9">
    选项
  </a>
</h2>

<table>
  <thead>
      <tr>
          <th>名称</th>
          <th>简写</th>
          <th>类型</th>
          <th>默认值</th>
          <th>描述</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><code>--format</code></td>
          <td><code>-f</code></td>
          <td><code>string</code></td>
          <td></td>
          <td>使用自定义格式打印输出</td>
      </tr>
      <tr>
          <td><code>--no-trunc</code></td>
          <td></td>
          <td><code>bool</code></td>
          <td><code>false</code></td>
          <td>不截断输出</td>
      </tr>
      <tr>
          <td><code>--size</code></td>
          <td></td>
          <td><code>bool</code></td>
          <td><code>false</code></td>
          <td>显示总大小（包括沙盒使用的磁盘空间）</td>
      </tr>
  </tbody>
</table>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="示例">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%a4%ba%e4%be%8b">
    示例
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="查看沙盒的详细信息">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9f%a5%e7%9c%8b%e6%b2%99%e7%9b%92%e7%9a%84%e8%af%a6%e7%bb%86%e4%bf%a1%e6%81%af">
    查看沙盒的详细信息
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
        x-data="{ code: 'ZG9ja2VyIHNhbmRib3ggaW5zcGVjdCBteS1zYW5kYm94', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-shell" data-lang="shell"><span class="line"><span class="cl">docker sandbox inspect my-sandbox</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="使用自定义格式查看沙盒的详细信息">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8%e8%87%aa%e5%ae%9a%e4%b9%89%e6%a0%bc%e5%bc%8f%e6%9f%a5%e7%9c%8b%e6%b2%99%e7%9b%92%e7%9a%84%e8%af%a6%e7%bb%86%e4%bf%a1%e6%81%af">
    使用自定义格式查看沙盒的详细信息
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
        x-data="{ code: 'ZG9ja2VyIHNhbmRib3ggaW5zcGVjdCAtLWZvcm1hdCAne3suSUR9fScgbXktc2FuZGJveA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-shell" data-lang="shell"><span class="line"><span class="cl">docker sandbox inspect --format <span class="s1">&#39;{{.ID}}&#39;</span> my-sandbox</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="查看多个沙盒的详细信息">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9f%a5%e7%9c%8b%e5%a4%9a%e4%b8%aa%e6%b2%99%e7%9b%92%e7%9a%84%e8%af%a6%e7%bb%86%e4%bf%a1%e6%81%af">
    查看多个沙盒的详细信息
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
        x-data="{ code: 'ZG9ja2VyIHNhbmRib3ggaW5zcGVjdCBteS1zYW5kYm94LTEgbXktc2FuZGJveC0y', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-shell" data-lang="shell"><span class="line"><span class="cl">docker sandbox inspect my-sandbox-1 my-sandbox-2</span></span></code></pre></div>
      
    </div>
  </div>
</div>









## Description

Display detailed information on one or more sandboxes.

This command retrieves and displays detailed information about the specified
sandboxes using the Docker API. Each sandbox is identified by its unique ID or name.




## Examples

### Inspect a sandbox

```console
$ docker sandbox inspect abc123def
[
  {
    "id": "abc123def69b16c5c0dab4cf699e26f8d01e1ace3aeee06254e0999492e11647",
    "name": "claude-sandbox-2025-11-04-170333",
    "created_at": "2025-11-04T16:03:33.910642347Z",
    "status": "running",
    "template": "docker/sandbox-templates:claude-code",
    "labels": {
      "com.docker.sandbox.agent": "claude",
      "com.docker.sandbox.workingDirectory": "/Users/moby/code/docker/sandboxes",
      "com.docker.sandbox.workingDirectoryInode": "3041007",
      "com.docker.sandboxes": "templates",
      "com.docker.sandboxes.base": "ubuntu:questing",
      "com.docker.sandboxes.flavor": "claude-code",
      "com.docker.sdk": "true",
      "com.docker.sdk.client": "0.1.0-alpha011",
      "com.docker.sdk.container": "0.1.0-alpha012",
      "com.docker.sdk.lang": "go",
      "docker/sandbox": "true",
      "org.opencontainers.image.ref.name": "ubuntu",
      "org.opencontainers.image.version": "25.10"
    }
  }
]
```



