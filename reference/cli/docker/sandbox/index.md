# Docker 沙箱

**Description:** Docker Sandbox

**Usage:** `docker sandbox`




<h1 class=" scroll-mt-20 flex items-center gap-2" id="docker-沙箱">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-%e6%b2%99%e7%ae%b1">
    Docker 沙箱
  </a>
</h1>

<p>Docker 沙箱是一个隔离的环境，用于在容器中运行代码，而不会影响主机系统。这对于测试、开发和安全实验非常有用。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="前置条件">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%89%8d%e7%bd%ae%e6%9d%a1%e4%bb%b6">
    前置条件
  </a>
</h2>

<ul>
<li>Docker 已安装并运行</li>
<li>基本的 Docker 知识</li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="快速开始">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%bf%ab%e9%80%9f%e5%bc%80%e5%a7%8b">
    快速开始
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="1-创建沙箱">
  <a class="text-black dark:text-white no-underline hover:underline" href="#1-%e5%88%9b%e5%bb%ba%e6%b2%99%e7%ae%b1">
    1. 创建沙箱
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
        x-data="{ code: 'IyDliJvlu7rkuIDkuKrmlrDnmoQgRG9ja2VyIOaymeeusQpkb2NrZXIgcnVuIC1kIC0tbmFtZSBteS1zYW5kYm94IFwKICAtdiAvcGF0aC90by95b3VyL2NvZGU6L3dvcmtzcGFjZSBcCiAgLXAgODA4MDo4MDgwIFwKICAtLXJlc3RhcnQgdW5sZXNzLXN0b3BwZWQgXAogIHVidW50dTpsYXRlc3QgdGFpbCAtZiAvZGV2L251bGwKCiMg6L&#43;b5YWl5rKZ566xCmRvY2tlciBleGVjIC1pdCBteS1zYW5kYm94IGJhc2g=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="c1"># 创建一个新的 Docker 沙箱</span>
</span></span><span class="line"><span class="cl">docker run -d --name my-sandbox <span class="se">\
</span></span></span><span class="line"><span class="cl">  -v /path/to/your/code:/workspace <span class="se">\
</span></span></span><span class="line"><span class="cl">  -p 8080:8080 <span class="se">\
</span></span></span><span class="line"><span class="cl">  --restart unless-stopped <span class="se">\
</span></span></span><span class="line"><span class="cl">  ubuntu:latest tail -f /dev/null
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 进入沙箱</span>
</span></span><span class="line"><span class="cl">docker <span class="nb">exec</span> -it my-sandbox bash</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="2-使用沙箱">
  <a class="text-black dark:text-white no-underline hover:underline" href="#2-%e4%bd%bf%e7%94%a8%e6%b2%99%e7%ae%b1">
    2. 使用沙箱
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
        x-data="{ code: 'IyDlnKjmspnnrrHkuK3lronoo4Xova/ku7YKYXB0LWdldCB1cGRhdGUgJiYgYXB0LWdldCBpbnN0YWxsIC15IHB5dGhvbjMgcHl0aG9uMy1waXAKCiMg6L&#43;Q6KGM5L2g55qE5Luj56CBCnB5dGhvbjMgL3dvcmtzcGFjZS9hcHAucHk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="c1"># 在沙箱中安装软件</span>
</span></span><span class="line"><span class="cl">apt-get update <span class="o">&amp;&amp;</span> apt-get install -y python3 python3-pip
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 运行你的代码</span>
</span></span><span class="line"><span class="cl">python3 /workspace/app.py</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="常用命令">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%b8%b8%e7%94%a8%e5%91%bd%e4%bb%a4">
    常用命令
  </a>
</h2>

<table>
  <thead>
      <tr>
          <th>命令</th>
          <th>描述</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><code>docker ps</code></td>
          <td>查看运行中的沙箱</td>
      </tr>
      <tr>
          <td><code>docker stop &lt;name&gt;</code></td>
          <td>停止沙箱</td>
      </tr>
      <tr>
          <td><code>docker start &lt;name&gt;</code></td>
          <td>启动沙箱</td>
      </tr>
      <tr>
          <td><code>docker rm &lt;name&gt;</code></td>
          <td>删除沙箱</td>
      </tr>
      <tr>
          <td><code>docker logs &lt;name&gt;</code></td>
          <td>查看沙箱日志</td>
      </tr>
  </tbody>
</table>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="配置示例">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%85%8d%e7%bd%ae%e7%a4%ba%e4%be%8b">
    配置示例
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="docker-composeyml">
  <a class="text-black dark:text-white no-underline hover:underline" href="#docker-composeyml">
    docker-compose.yml
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
        x-data="{ code: 'dmVyc2lvbjogJzMuOCcKc2VydmljZXM6CiAgc2FuZGJveDoKICAgIGltYWdlOiB1YnVudHU6bGF0ZXN0CiAgICBjb250YWluZXJfbmFtZTogbXktc2FuZGJveAogICAgdm9sdW1lczoKICAgICAgLSAuL2NvZGU6L3dvcmtzcGFjZQogICAgcG9ydHM6CiAgICAgIC0gIjgwODA6ODA4MCIKICAgIHJlc3RhcnQ6IHVubGVzcy1zdG9wcGVkCiAgICBjb21tYW5kOiB0YWlsIC1mIC9kZXYvbnVsbA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="s1">&#39;3.8&#39;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">services</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">sandbox</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu:latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">container_name</span><span class="p">:</span><span class="w"> </span><span class="l">my-sandbox</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">volumes</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="l">./code:/workspace</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">ports</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="s2">&#34;8080:8080&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">restart</span><span class="p">:</span><span class="w"> </span><span class="l">unless-stopped</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">command</span><span class="p">:</span><span class="w"> </span><span class="l">tail -f /dev/null</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="最佳实践">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9c%80%e4%bd%b3%e5%ae%9e%e8%b7%b5">
    最佳实践
  </a>
</h2>

<ol>
<li><strong>使用非 root 用户</strong>：在容器中创建专用用户</li>
<li><strong>限制资源</strong>：使用 <code>--cpus</code> 和 <code>--memory</code> 参数</li>
<li><strong>只读挂载</strong>：对于不需要写入的目录使用只读挂载</li>
<li><strong>清理</strong>：定期删除不再使用的沙箱</li>
</ol>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="故障排除">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%95%85%e9%9a%9c%e6%8e%92%e9%99%a4">
    故障排除
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="问题沙箱无法启动">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%97%ae%e9%a2%98%e6%b2%99%e7%ae%b1%e6%97%a0%e6%b3%95%e5%90%af%e5%8a%a8">
    问题：沙箱无法启动
  </a>
</h3>

<p><strong>解决方案</strong>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDmo4Dmn6UgRG9ja2VyIOeKtuaAgQpzeXN0ZW1jdGwgc3RhdHVzIGRvY2tlcgoKIyDmo4Dmn6Xnq6/lj6PlhrLnqoEKbmV0c3RhdCAtdHVscG4gfCBncmVwIDgwODA=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="c1"># 检查 Docker 状态</span>
</span></span><span class="line"><span class="cl">systemctl status docker
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 检查端口冲突</span>
</span></span><span class="line"><span class="cl">netstat -tulpn <span class="p">|</span> grep <span class="m">8080</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="问题无法访问沙箱中的文件">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%97%ae%e9%a2%98%e6%97%a0%e6%b3%95%e8%ae%bf%e9%97%ae%e6%b2%99%e7%ae%b1%e4%b8%ad%e7%9a%84%e6%96%87%e4%bb%b6">
    问题：无法访问沙箱中的文件
  </a>
</h3>

<p><strong>解决方案</strong>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDmo4Dmn6XmjILovb3ngrkKZG9ja2VyIGluc3BlY3QgbXktc2FuZGJveCB8IGdyZXAgTW91bnRzIC1BIDEwCgojIOmqjOivgeadg&#43;mZkApscyAtbGEgL3BhdGgvdG8veW91ci9jb2Rl', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="c1"># 检查挂载点</span>
</span></span><span class="line"><span class="cl">docker inspect my-sandbox <span class="p">|</span> grep Mounts -A <span class="m">10</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 验证权限</span>
</span></span><span class="line"><span class="cl">ls -la /path/to/your/code</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="安全提示">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%ae%89%e5%85%a8%e6%8f%90%e7%a4%ba">
    安全提示
  </a>
</h2>

<ul>
<li>不要在沙箱中存储敏感信息</li>
<li>使用网络隔离（<code>--network none</code>）</li>
<li>定期更新基础镜像</li>
<li>监控容器资源使用情况</li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="相关链接">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%9b%b8%e5%85%b3%e9%93%be%e6%8e%a5">
    相关链接
  </a>
</h2>

<ul>
<li><a class="link" href="https://docs.docker.com/" rel="noopener">Docker 官方文档</a></li>
<li><a class="link" href="https://docs.docker.com/engine/reference/commandline/docker/" rel="noopener">Docker CLI 参考</a></li>
<li><a class="link" href="https://docs.docker.com/develop/develop-images/dockerfile_best-practices/" rel="noopener">最佳实践指南</a></li>
</ul>









## Description

Local sandbox environments for AI agents, using Docker.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-D`, `--debug` |  |  Enable debug logging |





## Subcommands

| Command | Description |
|---------|-------------|
| [`docker sandbox create`](/reference/cli/docker/sandbox/create/) | Create a sandbox for an agent |
| [`docker sandbox create cagent`](/reference/cli/docker/sandbox/create/cagent/) | Create a sandbox for cagent |
| [`docker sandbox create codex`](/reference/cli/docker/sandbox/create/codex/) | Create a sandbox for codex |
| [`docker sandbox create gemini`](/reference/cli/docker/sandbox/create/gemini/) | Create a sandbox for gemini |
| [`docker sandbox create kiro`](/reference/cli/docker/sandbox/create/kiro/) | Create a sandbox for kiro |
| [`docker sandbox exec`](/reference/cli/docker/sandbox/exec/) | Execute a command inside a sandbox |
| [`docker sandbox inspect`](/reference/cli/docker/sandbox/inspect/) | Display detailed information on one or more sandboxes |
| [`docker sandbox ls`](/reference/cli/docker/sandbox/ls/) | List VMs |
| [`docker sandbox reset`](/reference/cli/docker/sandbox/reset/) | Reset all VM sandboxes and clean up state |
| [`docker sandbox run`](/reference/cli/docker/sandbox/run/) | Run an agent in a sandbox |
| [`docker sandbox stop`](/reference/cli/docker/sandbox/stop/) | Stop one or more sandboxes without removing them |
| [`docker sandbox 删除`](/reference/cli/docker/sandbox/rm/) | Remove one or more sandboxes |
| [`Docker 沙箱网络`](/reference/cli/docker/sandbox/network/) | Manage sandbox networking |


