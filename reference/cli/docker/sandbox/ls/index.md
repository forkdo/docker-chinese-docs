---
title: docker sandbox ls
url: /reference/cli/docker/sandbox/ls/
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
  - title: docker sandbox ls
    url: /reference/cli/docker/sandbox/ls/
next:
  title: docker sandbox inspect
  url: /reference/cli/docker/sandbox/inspect/
prev:
  title: docker sandbox run
  url: /reference/cli/docker/sandbox/run/
---

**Description:** List sandboxes

**Usage:** `docker sandbox ls`

**Aliases:** `docker sandbox list`


<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-sandbox-ls">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-sandbox-ls">
    docker sandbox ls
  </a>
</h1>


<h2 class=" scroll-mt-20 flex items-center gap-2" id="描述">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8f%8f%e8%bf%b0">
    描述
  </a>
</h2>

<p>列出所有可用的沙盒。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="使用">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8">
    使用
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
        x-data="{ code: 'ZG9ja2VyIHNhbmRib3ggbHMgW09QVElPTlNd', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">docker sandbox ls [OPTIONS]</span></span></code></pre></div>
      
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
          <td>--format</td>
          <td>-f</td>
          <td>string</td>
          <td></td>
          <td>使用自定义输出格式打印输出：<br><code>--format '{{.Name}}'</code></td>
      </tr>
      <tr>
          <td>--no-trunc</td>
          <td></td>
          <td>bool</td>
          <td>false</td>
          <td>不截断输出</td>
      </tr>
      <tr>
          <td>--quiet</td>
          <td>-q</td>
          <td>bool</td>
          <td>false</td>
          <td>仅显示沙盒 ID</td>
      </tr>
  </tbody>
</table>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="示例">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%a4%ba%e4%be%8b">
    示例
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="使用自定义格式列出所有沙盒">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8%e8%87%aa%e5%ae%9a%e4%b9%89%e6%a0%bc%e5%bc%8f%e5%88%97%e5%87%ba%e6%89%80%e6%9c%89%e6%b2%99%e7%9b%92">
    使用自定义格式列出所有沙盒
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
        x-data="{ code: 'JCBkb2NrZXIgc2FuZGJveCBscyAtLWZvcm1hdCAne3suTmFtZX19Jw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">$ docker sandbox ls --format &#39;{{.Name}}&#39;</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="列出所有沙盒的-id">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%97%e5%87%ba%e6%89%80%e6%9c%89%e6%b2%99%e7%9b%92%e7%9a%84-id">
    列出所有沙盒的 ID
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
        x-data="{ code: 'JCBkb2NrZXIgc2FuZGJveCBscyAtcQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">$ docker sandbox ls -q</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="列出所有沙盒不截断输出">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%97%e5%87%ba%e6%89%80%e6%9c%89%e6%b2%99%e7%9b%92%e4%b8%8d%e6%88%aa%e6%96%ad%e8%be%93%e5%87%ba">
    列出所有沙盒（不截断输出）
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
        x-data="{ code: 'JCBkb2NrZXIgc2FuZGJveCBscyAtLW5vLXRydW5j', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">$ docker sandbox ls --no-trunc</span></span></code></pre></div>
      
    </div>
  </div>
</div>









## Description

List all sandboxes.

This command lists all sandboxes using the Docker API.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--no-trunc` |  |  Don't truncate output |
| `-q`, `--quiet` |  |  Only display sandbox IDs |



## Examples

### List all sandboxes

```console
$ docker sandbox ls
SANDBOX ID    NAME         WORKSPACE                    CREATED
abc123def     my-project   /home/user/my-project        2 hours ago
def456ghi     ml-work      /home/user/ml-projects       1 day ago
```

### Show only sandbox IDs (--quiet) {#quiet}

```text
--quiet
```

Output only sandbox IDs:

```console
$ docker sandbox ls --quiet
abc123def
def456ghi
```

### Don't truncate output (--no-trunc) {#no-trunc}

```text
--no-trunc
```

By default, long sandbox IDs and workspace paths are truncated for readability. Use `--no-trunc` to display the full values:

```console
$ docker sandbox ls
SANDBOX ID    TEMPLATE  NAME         WORKSPACE                     STATUS   CREATED
abc123def456  ubuntu    my-project   /home/user/.../my-project     running  2 hours ago

$ docker sandbox ls --no-trunc
SANDBOX ID              TEMPLATE  NAME         WORKSPACE                                          STATUS   CREATED
abc123def456ghi789jkl   ubuntu    my-project   /home/user/very/long/path/to/my-project           running  2 hours ago
```



