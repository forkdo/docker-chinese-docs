# Node.js

本示例演示如何将 Node.js 应用迁移到 Docker Hardened Images。

以下示例展示了迁移到 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- Before (Wolfi)：使用 Wolfi 发行版镜像的 Dockerfile 示例，迁移到 DHI 之前
- Before (DOI)：使用 Docker 官方镜像的 Dockerfile 示例，迁移到 DHI 之前
- After (multi-stage)：迁移到 DHI 后使用多阶段构建的 Dockerfile 示例（推荐用于最小化、安全的镜像）
- After (single-stage)：迁移到 DHI 后使用单阶段构建的 Dockerfile 示例（更简单，但会导致镜像更大，攻击面更广）

> [!NOTE]
>
> 多阶段构建适用于大多数用例。单阶段构建为简化操作而支持，但在镜像大小和安全性方面存在权衡。
>
> 在拉取 Docker Hardened Images 之前，您必须对 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与 Docker Hub 相同的用户名和密码）。如果您没有 Docker 账户，请[免费创建一个](../../../accounts/create-account.md)。
>
> 运行 `docker login dhi.io` 进行身份验证。








<div
  class="tabs"
  
    x-data="{ selected: 'Before-Wolfi' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Before-Wolfi' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Before-Wolfi'"
        
      >
        Before (Wolfi)
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Before-DOI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Before-DOI'"
        
      >
        Before (DOI)
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'After-multi-stage' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'After-multi-stage'"
        
      >
        After (multi-stage)
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'After-single-stage' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'After-single-stage'"
        
      >
        After (single-stage)
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Before-Wolfi' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIGNnci5kZXYvY2hhaW5ndWFyZC9ub2RlOmxhdGVzdC1kZXYKV09SS0RJUiAvdXNyL3NyYy9hcHAKCkNPUFkgcGFja2FnZSouanNvbiAuLwoKIyDlpoLmnpzpnIDopoHvvIzkvb/nlKggYXBrIOWuieijheWFtuS7lui9r&#43;S7tuWMhQojIFJVTiBhcGsgYWRkIC0tbm8tY2FjaGUgcHl0aG9uMyBtYWtlIGcrKwoKUlVOIG5wbSBpbnN0YWxsCgpDT1BZIC4gLgoKQ01EIFsibm9kZSIsICJpbmRleC5qcyJd', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c">#syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">cgr.dev/chainguard/node:latest-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache python3 make g++</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> npm install<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;node&#34;</span><span class="p">,</span> <span class="s2">&#34;index.js&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Before-DOI' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIG5vZGU6bGF0ZXN0CldPUktESVIgL3Vzci9zcmMvYXBwCgpDT1BZIHBhY2thZ2UqLmpzb24gLi8KCiMg5aaC5p6c6ZyA6KaB77yM5L2/55SoIGFwdCDlronoo4Xlhbbku5bova/ku7bljIUKIyBSVU4gYXB0LWdldCB1cGRhdGUgJiYgYXB0LWdldCBpbnN0YWxsIC15IHB5dGhvbjMgbWFrZSBnKysgJiYgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cy8qCgpSVU4gbnBtIGluc3RhbGwKCkNPUFkgLiAuCgpDTUQgWyJub2RlIiwgImluZGV4LmpzIl0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c">#syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">node:latest</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apt 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apt-get update &amp;&amp; apt-get install -y python3 make g++ &amp;&amp; rm -rf /var/lib/apt/lists/*</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> npm install<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;node&#34;</span><span class="p">,</span> <span class="s2">&#34;index.js&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'After-multi-stage' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgojID09PSDmnoTlu7rpmLbmrrXvvJrlronoo4Xkvp3otZblubbmnoTlu7rlupTnlKggPT09CkZST00gZGhpLmlvL25vZGU6MjMtYWxwaW5lMy4yMS1kZXYgQVMgYnVpbGRlcgpXT1JLRElSIC91c3Ivc3JjL2FwcAoKQ09QWSBwYWNrYWdlKi5qc29uIC4vCgojIOWmguaenOmcgOimge&#43;8jOS9v&#43;eUqCBhcGsg5a6J6KOF5YW25LuW6L2v5Lu25YyFCiMgUlVOIGFwayBhZGQgLS1uby1jYWNoZSBweXRob24zIG1ha2UgZysrCgpSVU4gbnBtIGluc3RhbGwKCkNPUFkgLiAuCgojID09PSDmnIDnu4jpmLbmrrXvvJrliJvlu7rmnIDlsI/ljJbov5DooYzml7bplZzlg48gPT09CkZST00gZGhpLmlvL25vZGU6MjMtYWxwaW5lMy4yMQpFTlYgUEFUSD0vYXBwL25vZGVfbW9kdWxlcy8uYmluOiRQQVRICgpDT1BZIC0tZnJvbT1idWlsZGVyIC0tY2hvd249bm9kZTpub2RlIC91c3Ivc3JjL2FwcCAvYXBwCgpXT1JLRElSIC9hcHAKCkNNRCBbImluZGV4LmpzIl0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c">#syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># === 构建阶段：安装依赖并构建应用 ===</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/node:23-alpine3.21-dev</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache python3 make g++</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> npm install<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># === 最终阶段：创建最小化运行时镜像 ===</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/node:23-alpine3.21</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span>/app/node_modules/.bin:<span class="nv">$PATH</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>builder --chown<span class="o">=</span>node:node /usr/src/app /app<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;index.js&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'After-single-stage' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIGRoaS5pby9ub2RlOjIzLWFscGluZTMuMjEtZGV2CldPUktESVIgL3Vzci9zcmMvYXBwCgpDT1BZIHBhY2thZ2UqLmpzb24gLi8KCiMg5aaC5p6c6ZyA6KaB77yM5L2/55SoIGFwayDlronoo4Xlhbbku5bova/ku7bljIUKIyBSVU4gYXBrIGFkZCAtLW5vLWNhY2hlIHB5dGhvbjMgbWFrZSBnKysKClJVTiBucG0gaW5zdGFsbAoKQ09QWSAuIC4KCkNNRCBbIm5vZGUiLCAiaW5kZXguanMiXQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c">#syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/node:23-alpine3.21-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/usr/src/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> package*.json ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache python3 make g++</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> npm install<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> . .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">CMD</span> <span class="p">[</span><span class="s2">&#34;node&#34;</span><span class="p">,</span> <span class="s2">&#34;index.js&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

