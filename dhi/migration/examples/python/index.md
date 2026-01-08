# Python

本示例展示如何将 Python 应用程序迁移到 Docker Hardened Images。

以下示例展示了迁移到 Docker Hardened Images 前后的 Dockerfile。每个示例包含四种变体：

- 迁移前 (Wolfi)：使用 Wolfi 发行版镜像的示例 Dockerfile，迁移到 DHI 之前
- 迁移前 (DOI)：使用 Docker Official Images 的示例 Dockerfile，迁移到 DHI 之前
- 迁移后 (多阶段)：迁移到 DHI 后使用多阶段构建的示例 Dockerfile（推荐用于最小化、安全的镜像）
- 迁移后 (单阶段)：迁移到 DHI 后使用单阶段构建的示例 Dockerfile（更简单，但会生成更大的镜像，攻击面更广）

> [!NOTE]
>
> 大多数用例推荐使用多阶段构建。为简化操作也支持单阶段构建，但在镜像大小和安全性方面需要权衡。
>
> 在拉取 Docker Hardened Images 之前，必须先向 `dhi.io` 进行身份验证。
> 运行 `docker login dhi.io` 进行身份验证。








<div
  class="tabs"
  
    x-data="{ selected: '%E8%BF%81%E7%A7%BB%E5%89%8D-Wolfi' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E8%BF%81%E7%A7%BB%E5%89%8D-Wolfi' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E8%BF%81%E7%A7%BB%E5%89%8D-Wolfi'"
        
      >
        迁移前 (Wolfi)
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E8%BF%81%E7%A7%BB%E5%89%8D-DOI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E8%BF%81%E7%A7%BB%E5%89%8D-DOI'"
        
      >
        迁移前 (DOI)
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E8%BF%81%E7%A7%BB%E5%90%8E-%E5%A4%9A%E9%98%B6%E6%AE%B5' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E8%BF%81%E7%A7%BB%E5%90%8E-%E5%A4%9A%E9%98%B6%E6%AE%B5'"
        
      >
        迁移后 (多阶段)
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E8%BF%81%E7%A7%BB%E5%90%8E-%E5%8D%95%E9%98%B6%E6%AE%B5' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E8%BF%81%E7%A7%BB%E5%90%8E-%E5%8D%95%E9%98%B6%E6%AE%B5'"
        
      >
        迁移后 (单阶段)
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E8%BF%81%E7%A7%BB%E5%89%8D-Wolfi' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIGNnci5kZXYvY2hhaW5ndWFyZC9weXRob246bGF0ZXN0LWRldiBBUyBidWlsZGVyCgpFTlYgTEFORz1DLlVURi04CkVOViBQWVRIT05ET05UV1JJVEVCWVRFQ09ERT0xCkVOViBQWVRIT05VTkJVRkZFUkVEPTEKRU5WIFBBVEg9Ii9hcHAvdmVudi9iaW46JFBBVEgiCgpXT1JLRElSIC9hcHAKClJVTiBweXRob24gLW0gdmVudiAvYXBwL3ZlbnYKQ09QWSByZXF1aXJlbWVudHMudHh0IC4KCiMg5aaC5p6c6ZyA6KaB77yM5L2/55SoIGFwayDlronoo4Xku7vkvZXpop3lpJbnmoTljIUKIyBSVU4gYXBrIGFkZCAtLW5vLWNhY2hlIGdjYyBtdXNsLWRldgoKUlVOIHBpcCBpbnN0YWxsIC0tbm8tY2FjaGUtZGlyIC1yIHJlcXVpcmVtZW50cy50eHQKCkZST00gY2dyLmRldi9jaGFpbmd1YXJkL3B5dGhvbjpsYXRlc3QKCldPUktESVIgL2FwcAoKRU5WIFBZVEhPTlVOQlVGRkVSRUQ9MQpFTlYgUEFUSD0iL2FwcC92ZW52L2JpbjokUEFUSCIKCkNPUFkgYXBwLnB5IC4vCkNPUFkgLS1mcm9tPWJ1aWxkZXIgL2FwcC92ZW52IC9hcHAvdmVudgoKRU5UUllQT0lOVCBbICJweXRob24iLCAiL2FwcC9hcHAucHkiIF0=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">cgr.dev/chainguard/python:latest-dev</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">LANG</span><span class="o">=</span>C.UTF-8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONDONTWRITEBYTECODE</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span><span class="s2">&#34;/app/venv/bin:</span><span class="nv">$PATH</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> python -m venv /app/venv<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> requirements.txt .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装任何额外的包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache gcc musl-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> pip install --no-cache-dir -r requirements.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">cgr.dev/chainguard/python:latest</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span><span class="s2">&#34;/app/venv/bin:</span><span class="nv">$PATH</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> app.py ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>builder /app/venv /app/venv<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span> <span class="s2">&#34;python&#34;</span><span class="p">,</span> <span class="s2">&#34;/app/app.py&#34;</span> <span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E8%BF%81%E7%A7%BB%E5%89%8D-DOI' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIHB5dGhvbjpsYXRlc3QgQVMgYnVpbGRlcgoKRU5WIExBTkc9Qy5VVEYtOApFTlYgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9MQpFTlYgUFlUSE9OVU5CVUZGRVJFRD0xCkVOViBQQVRIPSIvYXBwL3ZlbnYvYmluOiRQQVRIIgoKV09SS0RJUiAvYXBwCgpSVU4gcHl0aG9uIC1tIHZlbnYgL2FwcC92ZW52CkNPUFkgcmVxdWlyZW1lbnRzLnR4dCAuCgojIOWmguaenOmcgOimge&#43;8jOS9v&#43;eUqCBhcHQg5a6J6KOF5Lu75L2V6aKd5aSW55qE5YyFCiMgUlVOIGFwdC1nZXQgdXBkYXRlICYmIGFwdC1nZXQgaW5zdGFsbCAteSBnY2MgJiYgcm0gLXJmIC92YXIvbGliL2FwdC9saXN0cy8qCgpSVU4gcGlwIGluc3RhbGwgLS1uby1jYWNoZS1kaXIgLXIgcmVxdWlyZW1lbnRzLnR4dAoKRlJPTSBweXRob246bGF0ZXN0CgpXT1JLRElSIC9hcHAKCkVOViBQWVRIT05VTkJVRkZFUkVEPTEKRU5WIFBBVEg9Ii9hcHAvdmVudi9iaW46JFBBVEgiCgpDT1BZIGFwcC5weSAuLwpDT1BZIC0tZnJvbT1idWlsZGVyIC9hcHAvdmVudiAvYXBwL3ZlbnYKCkVOVFJZUE9JTlQgWyAicHl0aG9uIiwgIi9hcHAvYXBwLnB5IiBd', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">python:latest</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">LANG</span><span class="o">=</span>C.UTF-8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONDONTWRITEBYTECODE</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span><span class="s2">&#34;/app/venv/bin:</span><span class="nv">$PATH</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> python -m venv /app/venv<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> requirements.txt .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apt 安装任何额外的包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apt-get update &amp;&amp; apt-get install -y gcc &amp;&amp; rm -rf /var/lib/apt/lists/*</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> pip install --no-cache-dir -r requirements.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">python:latest</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span><span class="s2">&#34;/app/venv/bin:</span><span class="nv">$PATH</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> app.py ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>builder /app/venv /app/venv<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span> <span class="s2">&#34;python&#34;</span><span class="p">,</span> <span class="s2">&#34;/app/app.py&#34;</span> <span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E8%BF%81%E7%A7%BB%E5%90%8E-%E5%A4%9A%E9%98%B6%E6%AE%B5' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgojID09PSDmnoTlu7rpmLbmrrXvvJrlronoo4Xkvp3otZblubbliJvlu7romZrmi5/njq/looMgPT09CkZST00gZGhpLmlvL3B5dGhvbjozLjEzLWFscGluZTMuMjEtZGV2IEFTIGJ1aWxkZXIKCkVOViBMQU5HPUMuVVRGLTgKRU5WIFBZVEhPTkRPTlRXUklURUJZVEVDT0RFPTEKRU5WIFBZVEhPTlVOQlVGRkVSRUQ9MQpFTlYgUEFUSD0iL2FwcC92ZW52L2JpbjokUEFUSCIKCldPUktESVIgL2FwcAoKUlVOIHB5dGhvbiAtbSB2ZW52IC9hcHAvdmVudgpDT1BZIHJlcXVpcmVtZW50cy50eHQgLgoKIyDlpoLmnpzpnIDopoHvvIzkvb/nlKggYXBrIOWuieijheS7u&#43;S9lemineWklueahOWMhQojIFJVTiBhcGsgYWRkIC0tbm8tY2FjaGUgZ2NjIG11c2wtZGV2CgpSVU4gcGlwIGluc3RhbGwgLS1uby1jYWNoZS1kaXIgLXIgcmVxdWlyZW1lbnRzLnR4dAoKIyA9PT0g5pyA57uI6Zi25q6177ya5Yib5bu65pyA5bCP6L&#43;Q6KGM5pe26ZWc5YOPID09PQpGUk9NIGRoaS5pby9weXRob246My4xMy1hbHBpbmUzLjIxCgpXT1JLRElSIC9hcHAKCkVOViBQWVRIT05VTkJVRkZFUkVEPTEKRU5WIFBBVEg9Ii9hcHAvdmVudi9iaW46JFBBVEgiCgpDT1BZIGFwcC5weSAuLwpDT1BZIC0tZnJvbT1idWlsZGVyIC9hcHAvdmVudiAvYXBwL3ZlbnYKCkVOVFJZUE9JTlQgWyAicHl0aG9uIiwgIi9hcHAvYXBwLnB5IiBd', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="c"># === 构建阶段：安装依赖并创建虚拟环境 ===</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/python:3.13-alpine3.21-dev</span><span class="w"> </span><span class="k">AS</span><span class="w"> </span><span class="s">builder</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">LANG</span><span class="o">=</span>C.UTF-8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONDONTWRITEBYTECODE</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span><span class="s2">&#34;/app/venv/bin:</span><span class="nv">$PATH</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> python -m venv /app/venv<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> requirements.txt .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装任何额外的包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache gcc musl-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> pip install --no-cache-dir -r requirements.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># === 最终阶段：创建最小运行时镜像 ===</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/python:3.13-alpine3.21</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span><span class="s2">&#34;/app/venv/bin:</span><span class="nv">$PATH</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> app.py ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> --from<span class="o">=</span>builder /app/venv /app/venv<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span> <span class="s2">&#34;python&#34;</span><span class="p">,</span> <span class="s2">&#34;/app/app.py&#34;</span> <span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E8%BF%81%E7%A7%BB%E5%90%8E-%E5%8D%95%E9%98%B6%E6%AE%B5' && 'hidden'"
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
        x-data="{ code: 'I3N5bnRheD1kb2NrZXIvZG9ja2VyZmlsZToxCgpGUk9NIGRoaS5pby9weXRob246My4xMy1hbHBpbmUzLjIxLWRldgoKRU5WIExBTkc9Qy5VVEYtOApFTlYgUFlUSE9ORE9OVFdSSVRFQllURUNPREU9MQpFTlYgUFlUSE9OVU5CVUZGRVJFRD0xCkVOViBQQVRIPSIvYXBwL3ZlbnYvYmluOiRQQVRIIgoKV09SS0RJUiAvYXBwCgpSVU4gcHl0aG9uIC1tIHZlbnYgL2FwcC92ZW52CkNPUFkgcmVxdWlyZW1lbnRzLnR4dCAuCgojIOWmguaenOmcgOimge&#43;8jOS9v&#43;eUqCBhcGsg5a6J6KOF5Lu75L2V6aKd5aSW55qE5YyFCiMgUlVOIGFwayBhZGQgLS1uby1jYWNoZSBnY2MgbXVzbC1kZXYKClJVTiBwaXAgaW5zdGFsbCAtLW5vLWNhY2hlLWRpciAtciByZXF1aXJlbWVudHMudHh0CgpDT1BZIGFwcC5weSAuLwoKRU5UUllQT0lOVCBbICJweXRob24iLCAiL2FwcC9hcHAucHkiIF0=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="k">FROM</span><span class="w"> </span><span class="s">dhi.io/python:3.13-alpine3.21-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">LANG</span><span class="o">=</span>C.UTF-8<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONDONTWRITEBYTECODE</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PYTHONUNBUFFERED</span><span class="o">=</span><span class="m">1</span>
</span></span><span class="line"><span class="cl"><span class="k">ENV</span> <span class="nv">PATH</span><span class="o">=</span><span class="s2">&#34;/app/venv/bin:</span><span class="nv">$PATH</span><span class="s2">&#34;</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">WORKDIR</span><span class="w"> </span><span class="s">/app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> python -m venv /app/venv<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> requirements.txt .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># 如果需要，使用 apk 安装任何额外的包</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="c"># RUN apk add --no-cache gcc musl-dev</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">RUN</span> pip install --no-cache-dir -r requirements.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">COPY</span> app.py ./<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="k">ENTRYPOINT</span> <span class="p">[</span> <span class="s2">&#34;python&#34;</span><span class="p">,</span> <span class="s2">&#34;/app/app.py&#34;</span> <span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

