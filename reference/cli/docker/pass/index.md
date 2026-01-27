# Docker Pass

**Description:** Manage your local OS keychain secrets.

**Usage:** `docker pass set|get|ls|rm`





<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-pass">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-pass">
    Docker Pass
  </a>
</h1>

<p>Docker Pass 是一个 Docker 凭据助手，它使用 Vault 的 Docker 凭据引擎来管理 Docker 注册表的认证信息。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="工作原理">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%b7%a5%e4%bd%9c%e5%8e%9f%e7%90%86">
    工作原理
  </a>
</h2>

<p>Docker Pass 通过与 Vault 的 Docker 凭据引擎交互来工作。它会检索用于 Docker 登录的临时认证令牌。</p>
<p>当您运行 <code>docker login</code> 时，Docker 会调用凭据助手。凭据助手会向 Vault 请求认证令牌，然后将该令牌返回给 Docker。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="安装">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%ae%89%e8%a3%85">
    安装
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="从源码构建">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bb%8e%e6%ba%90%e7%a0%81%e6%9e%84%e5%bb%ba">
    从源码构建
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
        x-data="{ code: 'Z2l0IGNsb25lIGh0dHBzOi8vZ2l0aHViLmNvbS9oYXNoaWNvcnAvdmF1bHQKY2QgdmF1bHQKbWFrZSBkb2NrZXItcGFzcw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">git clone https://github.com/hashicorp/vault
</span></span><span class="line"><span class="cl"><span class="nb">cd</span> vault
</span></span><span class="line"><span class="cl">make docker-pass</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>这将在 <code>bin/</code> 目录下生成 <code>docker-pass</code> 二进制文件。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="从发布版下载">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bb%8e%e5%8f%91%e5%b8%83%e7%89%88%e4%b8%8b%e8%bd%bd">
    从发布版下载
  </a>
</h3>

<p>从 <a class="link" href="https://github.com/hashicorp/vault/releases" rel="noopener">GitHub 发布页面</a> 下载适用于您操作系统的预编译二进制文件。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="配置">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%85%8d%e7%bd%ae">
    配置
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="1-配置-docker-凭据引擎">
  <a class="text-black dark:text-white no-underline hover:underline" href="#1-%e9%85%8d%e7%bd%ae-docker-%e5%87%ad%e6%8d%ae%e5%bc%95%e6%93%8e">
    1. 配置 Docker 凭据引擎
  </a>
</h3>

<p>首先，在 Vault 中启用并配置 Docker 凭据引擎：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDlkK/nlKggRG9ja2VyIOWHreaNruW8leaTjgp2YXVsdCBzZWNyZXRzIGVuYWJsZSBkb2NrZXIKCiMg6YWN572uIERvY2tlciDms6jlhozooagKdmF1bHQgd3JpdGUgZG9ja2VyL3JlZ2lzdHJ5L215LXJlZ2lzdHJ5IFwKICAgIHVybD1odHRwczovL2luZGV4LmRvY2tlci5pby92MS8gXAogICAgdXNlcm5hbWU9bXl1c2VyIFwKICAgIHBhc3N3b3JkPW15cGFzc3dvcmQ=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="c1"># 启用 Docker 凭据引擎</span>
</span></span><span class="line"><span class="cl">vault secrets <span class="nb">enable</span> docker
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 配置 Docker 注册表</span>
</span></span><span class="line"><span class="cl">vault write docker/registry/my-registry <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">url</span><span class="o">=</span>https://index.docker.io/v1/ <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">username</span><span class="o">=</span>myuser <span class="se">\
</span></span></span><span class="line"><span class="cl">    <span class="nv">password</span><span class="o">=</span>mypassword</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="2-配置-docker-pass">
  <a class="text-black dark:text-white no-underline hover:underline" href="#2-%e9%85%8d%e7%bd%ae-docker-pass">
    2. 配置 Docker Pass
  </a>
</h3>

<p>创建配置文件 <code>~/.docker/docker-pass.json</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICJ2YXVsdF9hZGRyIjogImh0dHA6Ly8xMjcuMC4wLjE6ODIwMCIsCiAgInZhdWx0X3Rva2VuIjogInMuWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYIiwKICAicmVnaXN0cnkiOiAibXktcmVnaXN0cnkiCn0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-json" data-lang="json"><span class="line"><span class="cl"><span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;vault_addr&#34;</span><span class="p">:</span> <span class="s2">&#34;http://127.0.0.1:8200&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;vault_token&#34;</span><span class="p">:</span> <span class="s2">&#34;s.XXXXXXXXXXXXXXXXXXXXXXXX&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;registry&#34;</span><span class="p">:</span> <span class="s2">&#34;my-registry&#34;</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>或者使用环境变量：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZXhwb3J0IFZBVUxUX0FERFI9aHR0cDovLzEyNy4wLjAuMTo4MjAwCmV4cG9ydCBWQVVMVF9UT0tFTj1zLlhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWApleHBvcnQgRE9DS0VSX1BBU1NfUkVHSVNUUlk9bXktcmVnaXN0cnk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="nb">export</span> <span class="nv">VAULT_ADDR</span><span class="o">=</span>http://127.0.0.1:8200
</span></span><span class="line"><span class="cl"><span class="nb">export</span> <span class="nv">VAULT_TOKEN</span><span class="o">=</span>s.XXXXXXXXXXXXXXXXXXXXXXXX
</span></span><span class="line"><span class="cl"><span class="nb">export</span> <span class="nv">DOCKER_PASS_REGISTRY</span><span class="o">=</span>my-registry</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="3-配置-docker">
  <a class="text-black dark:text-white no-underline hover:underline" href="#3-%e9%85%8d%e7%bd%ae-docker">
    3. 配置 Docker
  </a>
</h3>

<p>编辑 <code>~/.docker/config.json</code> 并添加凭据助手：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICJjcmVkc1N0b3JlIjogImRvY2tlci1wYXNzIgp9', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-json" data-lang="json"><span class="line"><span class="cl"><span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;credsStore&#34;</span><span class="p">:</span> <span class="s2">&#34;docker-pass&#34;</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>或者对于特定注册表：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICJjcmVkSGVscGVycyI6IHsKICAgICJteS1yZWdpc3RyeSI6ICJkb2NrZXItcGFzcyIKICB9Cn0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-json" data-lang="json"><span class="line"><span class="cl"><span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;credHelpers&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nt">&#34;my-registry&#34;</span><span class="p">:</span> <span class="s2">&#34;docker-pass&#34;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="使用">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bd%bf%e7%94%a8">
    使用
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="登录-docker-注册表">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%99%bb%e5%bd%95-docker-%e6%b3%a8%e5%86%8c%e8%a1%a8">
    登录 Docker 注册表
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
        x-data="{ code: 'ZG9ja2VyIGxvZ2luIG15LXJlZ2lzdHJ5', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker login my-registry</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>Docker Pass 会自动从 Vault 获取认证令牌并将其用于登录。</p>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="拉取镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8b%89%e5%8f%96%e9%95%9c%e5%83%8f">
    拉取镜像
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
        x-data="{ code: 'ZG9ja2VyIHB1bGwgbXktcmVnaXN0cnkvbXktaW1hZ2U6bGF0ZXN0', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker pull my-registry/my-image:latest</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="推送镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8e%a8%e9%80%81%e9%95%9c%e5%83%8f">
    推送镜像
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
        x-data="{ code: 'ZG9ja2VyIHRhZyBteS1pbWFnZTpsYXRlc3QgbXktcmVnaXN0cnkvbXktaW1hZ2U6bGF0ZXN0CmRvY2tlciBwdXNoIG15LXJlZ2lzdHJ5L215LWltYWdlOmxhdGVzdA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker tag my-image:latest my-registry/my-image:latest
</span></span><span class="line"><span class="cl">docker push my-registry/my-image:latest</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="故障排除">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%95%85%e9%9a%9c%e6%8e%92%e9%99%a4">
    故障排除
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="常见问题">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%b8%b8%e8%a7%81%e9%97%ae%e9%a2%98">
    常见问题
  </a>
</h3>

<p><strong>问题：</strong> <code>docker login</code> 失败，提示 &quot;credentials not found&quot;</p>
<p><strong>解决方案：</strong> 确保 <code>~/.docker/config.json</code> 中的 <code>credsStore</code> 或 <code>credHelpers</code> 配置正确。</p>
<p><strong>问题：</strong> 无法连接到 Vault</p>
<p><strong>解决方案：</strong> 检查 <code>VAULT_ADDR</code> 和 <code>VAULT_TOKEN</code> 环境变量或配置文件是否正确。</p>
<p><strong>问题：</strong> 权限不足</p>
<p><strong>解决方案：</strong> 确保您的 Vault token 有权限访问 Docker 凭据引擎。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="api-参考">
  <a class="text-black dark:text-white no-underline hover:underline" href="#api-%e5%8f%82%e8%80%83">
    API 参考
  </a>
</h2>

<p>Docker Pass 使用以下 Vault API 端点：</p>
<ul>
<li><code>GET /v1/docker/creds/:registry</code> - 获取指定注册表的认证凭据</li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="安全考虑">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%ae%89%e5%85%a8%e8%80%83%e8%99%91">
    安全考虑
  </a>
</h2>

<ul>
<li>将 Vault token 存储在安全的位置</li>
<li>使用具有最小权限的 Vault token</li>
<li>定期轮换 Vault token 和 Docker 凭据</li>
<li>考虑使用 Vault 的认证方法（如 AppRole、Kubernetes）而不是静态 token</li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="选项">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%80%89%e9%a1%b9">
    选项
  </a>
</h2>

<table>
  <thead>
      <tr>
          <th>参数</th>
          <th>描述</th>
          <th>环境变量</th>
          <th>配置文件</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><code>vault_addr</code></td>
          <td>Vault 服务器地址</td>
          <td><code>VAULT_ADDR</code></td>
          <td><code>vault_addr</code></td>
      </tr>
      <tr>
          <td><code>vault_token</code></td>
          <td>Vault 认证令牌</td>
          <td><code>VAULT_TOKEN</code></td>
          <td><code>vault_token</code></td>
      </tr>
      <tr>
          <td><code>registry</code></td>
          <td>Docker 注册表名称</td>
          <td><code>DOCKER_PASS_REGISTRY</code></td>
          <td><code>registry</code></td>
      </tr>
      <tr>
          <td><code>vault_namespace</code></td>
          <td>Vault 命名空间</td>
          <td><code>VAULT_NAMESPACE</code></td>
          <td><code>vault_namespace</code></td>
      </tr>
  </tbody>
</table>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="故障排除-1">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%95%85%e9%9a%9c%e6%8e%92%e9%99%a4-1">
    故障排除
  </a>
</h2>

<p>如果遇到问题，请检查：</p>
<ol>
<li>Vault 服务是否正在运行</li>
<li>Docker 凭据引擎是否已启用</li>
<li>您的 Vault token 是否有效且具有必要的权限</li>
<li>配置文件格式是否正确</li>
<li>Docker 是否配置为使用 docker-pass 凭据助手</li>
</ol>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="更多信息">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9b%b4%e5%a4%9a%e4%bf%a1%e6%81%af">
    更多信息
  </a>
</h2>

<ul>
<li><a class="link" href="https://developer.hashicorp.com/vault/docs/secrets/docker" rel="noopener">Vault Docker 凭据引擎文档</a></li>
<li><a class="link" href="https://github.com/docker/docker-credential-helpers" rel="noopener">Docker 凭据助手规范</a></li>
<li><a class="link" href="https://github.com/hashicorp/vault" rel="noopener">GitHub 仓库</a></li>
</ul>




> [!NOTE]
> **Experimental**
>
> This command is experimental. Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.





## Description

Docker Pass is a helper that allows you to store secrets securely in your
local OS keychain and inject them into containers later.

On Windows: Uses the Windows Credential Manager API.

On macOS: Uses macOS Keychain services API.

On Linux: `org.freedesktop.secrets` API (requires DBus and `gnome-keyring` or
`kdewallet` to be installed).




## Examples

### Using keychain secrets in containers

Create a secret:

```console
$ docker pass set GH_TOKEN=123456789
```

Creating a secret from STDIN:

```console
echo 123456789 > token.txt
cat token.txt | docker pass set GH_TOKEN
```

Run a container that uses the secret:

```console
$ docker run -e GH_TOKEN= -dt --name demo busybox
```

Inspect your secret from inside the container

```console
$ docker exec demo sh -c 'echo $GH_TOKEN'
123456789
```

Explicitly assigning a secret to another environment variable:

```console
$ docker run -e GITHUB_TOKEN=se://GH_TOKEN -dt --name demo busybox
```


## Subcommands

| Command | Description |
|---------|-------------|
| [`docker pass get`](/reference/cli/docker/pass/get/) | Get a secret |
| [`docker pass ls`](/reference/cli/docker/pass/ls/) | List secrets |
| [`docker pass rm`](/reference/cli/docker/pass/rm/) | Remove a secret |
| [`docker pass set`](/reference/cli/docker/pass/set/) | Set a secret |


