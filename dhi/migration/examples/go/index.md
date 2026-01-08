# Go

本示例展示了如何将 Go 应用程序迁移到 Docker Hardened Images。

以下示例展示了迁移到 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- Before (Wolfi)：使用 Wolfi 发行版镜像的 Dockerfile 示例，迁移到 DHI 之前
- Before (DOI)：使用 Docker 官方镜像的 Dockerfile 示例，迁移到 DHI 之前
- After (multi-stage)：迁移到 DHI 后使用多阶段构建的 Dockerfile 示例（推荐用于最小化、安全的镜像）
- After (single-stage)：迁移到 DHI 后使用单阶段构建的 Dockerfile 示例（更简单，但会导致镜像更大，攻击面更广）

> [!NOTE]
>
> 对于大多数用例，推荐使用多阶段构建。单阶段构建为了简化而支持，但在大小和安全性方面有所权衡。
>
> 在拉取 Docker Hardened Images 之前，您必须对 `dhi.io` 进行身份验证。
> 使用您的 Docker ID 凭据（与用于 Docker Hub 的用户名和密码相同）。如果您没有 Docker 账户，可以免费[创建一个](../../../accounts/create-account.md)。
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIGNnci5kZXYvY2hhaW5ndWFyZC9nbzpsYXRlc3QtZGV2CgpXT1JLRElSIC9hcHAKQUREIC4gLi8KCiMg5aaC5p6c6ZyA6KaB77yM5L2/55SoIGFwayDlronoo4Xlhbbku5bova/ku7bljIUKIyBSVU4gYXBrIGFkZCAtLW5vLWNhY2hlIGdpdAoKUlVOIENHT19FTkFCTEVEPTAgR09PUz1saW51eCBnbyBidWlsZCAtYSAtbGRmbGFncz0iLXMgLXciIC0taW5zdGFsbHN1ZmZpeCBjZ28gLW8gbWFpbiAuCgpFTlRSWVBPSU5UIFsiL2FwcC9tYWluIl0=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">cgr.dev/chainguard/go:latest-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ADD</span> . ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache git</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">CGO_ENABLED</span><span class="o">=</span><span class="m">0</span> <span class="nv">GOOS</span><span class="o">=</span>linux go build -a -ldflags<span class="o">=</span><span class="s2">&#34;-s -w&#34;</span> --installsuffix cgo -o main .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/app/main&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIGdvbGFuZzpsYXRlc3QKCldPUktESVIgL2FwcApBREQgLiAuLwoKIyDlpoLmnpzpnIDopoHvvIzkvb/nlKggYXB0IOWuieijheWFtuS7lui9r&#43;S7tuWMhQojIFJVTiBhcHQtZ2V0IHVwZGF0ZSAmJiBhcHQtZ2V0IGluc3RhbGwgLXkgZ2l0ICYmIHJtIC1yZiAvdmFyL2xpYi9hcHQvbGlzdHMvKgoKUlVOIENHT19FTkFCTEVEPTAgR09PUz1saW51eCBnbyBidWlsZCAtYSAtbGRmbGFncz0iLXMgLXciIC0taW5zdGFsbHN1ZmZpeCBjZ28gLW8gbWFpbiAuCgpFTlRSWVBPSU5UIFsiL2FwcC9tYWluIl0=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">golang:latest</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ADD</span> . ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apt 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apt-get update &amp;&amp; apt-get install -y git &amp;&amp; rm -rf /var/lib/apt/lists/*</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">CGO_ENABLED</span><span class="o">=</span><span class="m">0</span> <span class="nv">GOOS</span><span class="o">=</span>linux go build -a -ldflags<span class="o">=</span><span class="s2">&#34;-s -w&#34;</span> --installsuffix cgo -o main .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/app/main&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgojID09PSDmnoTlu7rpmLbmrrXvvJrnvJbor5EgR28g5bqU55So56iL5bqPID09PQpGUk9NIGRoaS5pby9nb2xhbmc6MS1hbHBpbmUzLjIxLWRldiBBUyBidWlsZGVyCgpXT1JLRElSIC9hcHAKQUREIC4gLi8KCiMg5aaC5p6c6ZyA6KaB77yM5L2/55SoIGFwayDlronoo4Xlhbbku5bova/ku7bljIUKIyBSVU4gYXBrIGFkZCAtLW5vLWNhY2hlIGdpdAoKUlVOIENHT19FTkFCTEVEPTAgR09PUz1saW51eCBnbyBidWlsZCAtYSAtbGRmbGFncz0iLXMgLXciIC0taW5zdGFsbHN1ZmZpeCBjZ28gLW8gbWFpbiAuCgojID09PSDmnIDnu4jpmLbmrrXvvJrliJvlu7rmnIDlsI/ov5DooYzml7bplZzlg48gPT09CkZST00gZGhpLmlvL2dvbGFuZzoxLWFscGluZTMuMjEKCldPUktESVIgL2FwcApDT1BZIC0tZnJvbT1idWlsZGVyIC9hcHAvbWFpbiAgL2FwcC9tYWluCgpFTlRSWVBPSU5UIFsiL2FwcC9tYWluIl0=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># === 构建阶段：编译 Go 应用程序 ===</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/golang:1-alpine3.21-dev</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ADD</span> . ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache git</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">CGO_ENABLED</span><span class="o">=</span><span class="m">0</span> <span class="nv">GOOS</span><span class="o">=</span>linux go build -a -ldflags<span class="o">=</span><span class="s2">&#34;-s -w&#34;</span> --installsuffix cgo -o main .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># === 最终阶段：创建最小运行时镜像 ===</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/golang:1-alpine3.21</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>builder /app/main  /app/main<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/app/main&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIGRoaS5pby9nb2xhbmc6MS1hbHBpbmUzLjIxLWRldgoKV09SS0RJUiAvYXBwCkFERCAuIC4vCgojIOWmguaenOmcgOimge&#43;8jOS9v&#43;eUqCBhcGsg5a6J6KOF5YW25LuW6L2v5Lu25YyFCiMgUlVOIGFwayBhZGQgLS1uby1jYWNoZSBnaXQKClJVTiBDR09fRU5BQkxFRD0wIEdPT1M9bGludXggZ28gYnVpbGQgLWEgLWxkZmxhZ3M9Ii1zIC13IiAtLWluc3RhbGxzdWZmaXggY2dvIC1vIG1haW4gLgoKRU5UUllQT0lOVCBbIi9hcHAvbWFpbiJd', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/golang:1-alpine3.21-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ADD</span> . ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装其他软件包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache git</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> <span class="nv">CGO_ENABLED</span><span class="o">=</span><span class="m">0</span> <span class="nv">GOOS</span><span class="o">=</span>linux go build -a -ldflags<span class="o">=</span><span class="s2">&#34;-s -w&#34;</span> --installsuffix cgo -o main .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/app/main&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

