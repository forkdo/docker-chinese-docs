# Docker Engine API v1.48 参考文档

<p><a class="link" href="https://github.com/moby/moby/blob/v27.2.0/api/swagger.yaml" rel="noopener">查看源码</a></p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="概述">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a6%82%e8%bf%b0">
    概述
  </a>
</h2>

<p>本文档描述了 Docker Engine API。</p>
<p>Docker Engine API 是与 Docker 守护进程通信的接口。更多关于 Docker 的信息，请访问 <a class="link" href="https://docs.docker.com" rel="noopener">Docker</a>。</p>
<p>默认情况下，Docker 守护进程监听 Unix 套接字，该套接字还提供 Docker Engine API。在使用 Docker 命令行客户端时，客户端默认通过此套接字与 Docker 守护进程通信。您还可以使用 curl 命令与 Docker Engine API 进行交互。</p>
<p>Docker Engine API 是可能变化的未版本化 API。请使用指定版本的 Docker Engine API。</p>
<p>此文档是 Docker Engine API 的参考文档。</p>
<p>Docker Engine API 是 RESTful API，它使用 JSON 通过 Unix 套接字或网络接口进行通信。</p>
<p>Docker Engine API 总是向后兼容的，您无需更改 Docker 客户端即可与较新版本的 Docker 通信。Docker 实现了自己的 API，不使用标准 Dockerfile 格式或 OCI 映像格式，并且不与任何其他库共享代码。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="版本化">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e7%89%88%e6%9c%ac%e5%8c%96">
    版本化
  </a>
</h2>

<p>Docker Engine API 使用 <a class="link" href="https://docs.docker.com/engine/api/version-history/" rel="noopener">API 版本</a> 进行版本控制。API 版本与 Docker Engine 版本不同，不应混为一谈。</p>
<p>请使用指定版本的 Docker Engine API。Docker Engine API 是可能变化的未版本化 API。如果您不使用指定版本的 API，可能会导致互操作性问题。</p>
<p>要查看 Docker 客户端和守护进程支持的 API 版本，请运行 <code>docker version</code> 命令。</p>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="通过-http-使用-docker-engine-api">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%80%9a%e8%bf%87-http-%e4%bd%bf%e7%94%a8-docker-engine-api">
    通过 HTTP 使用 Docker Engine API
  </a>
</h2>

<p>Docker 客户端可以与 Docker 守护进程通信，方法是通过 <code>HTTP 客户端</code> 向 Docker 守护进程监听的 Unix 套接字或端口发出请求，然后读取 HTTP 响应。</p>
<p>Unix 套接字 URL 使用 <code>http+unix</code> 方案。</p>
<p>您可以通过 <code>http+unix</code> 方案 URL 访问 Unix 套接字，该 URL 是 URL 编码的路径到 Unix 套接字文件。例如，<code>/var/run/docker.sock</code> 的 URL 编码是 <code>http%3A%2F%2Fvar%2Frun%2Fdocker.sock</code>。</p>
<p><code>http+unix</code> URL 作为 HTTP 请求的主机标头发送。</p>
<p>例如，要通过 Unix 套接字向 <code>/info</code> 发出 <code>GET http://localhost/info</code> 请求：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'R0VUIC9pbmZvIEhUVFAvMS4xCkhvc3Q6IGh0dHA6Ly92YXIvcnVuL2RvY2tlci5zb2Nr', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">GET /info HTTP/1.1
</span></span><span class="line"><span class="cl">Host: http://var/run/docker.sock</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>或者，如果您配置 Docker 守护进程在主机的 2376 端口上监听：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'R0VUIC9pbmZvIEhUVFAvMS4xCkhvc3Q6IGxvY2FsaG9zdDoyMzc2', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">GET /info HTTP/1.1
</span></span><span class="line"><span class="cl">Host: localhost:2376</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>要以编程方式制作 HTTP 请求，您必须禁用 HTTPS。Docker Engine Go 客户端演示了如何通过 HTTP 与 Docker 守护进程通信。</p>
<p>使用 cURL 时，您必须使用 <code>--unix-socket</code> 标志或禁用 HTTPS 使用 <code>-k</code> 或 <code>--insecure</code> 标志。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>警告</strong></p>
<p>仅在您配置 Docker 守护进程在主机的端口上监听时使用 <code>-k</code> 或 <code>--insecure</code> 标志。Docker 不会阻止您的请求，如果您的主机被劫持，可能会危及您的主机。有关详细信息，请参阅 <a class="link" href="https://docs.docker.com/engine/security/#docker-daemon-attack-surface" rel="noopener">Docker 守护进程攻击面</a>。</p>

  </blockquote>

<p>使用 cURL 通过 Unix 套接字：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBjdXJsIC0tdW5peC1zb2NrZXQgL3Zhci9ydW4vZG9ja2VyLnNvY2sgaHR0cDovL2xvY2FsaG9zdC92ZXJzaW9u', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">$ curl --unix-socket /var/run/docker.sock http://localhost/version</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>使用 cURL 通过端口：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBjdXJsIC1rIGh0dHBzOi8vbG9jYWxob3N0OjIzNzYvdmVyc2lvbg==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">$ curl -k https://localhost:2376/version</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>使用 Go 通过 Unix 套接字：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Y2xpIDo9ICZodHRwLkNsaWVudHsKICAgIFRyYW5zcG9ydDogJmh0dHAuVHJhbnNwb3J0ewogICAgICAgIERpYWxDb250ZXh0OiBmdW5jKF8gY29udGV4dC5Db250ZXh0LCBfLCBfIHN0cmluZykgKG5ldC5Db25uLCBlcnJvcikgewogICAgICAgICAgICByZXR1cm4gbmV0LkRpYWwoInVuaXgiLCAiL3Zhci9ydW4vZG9ja2VyLnNvY2siKQogICAgICAgIH0sCiAgICB9LAp9CgpyZXEsIGVyciA6PSBodHRwLk5ld1JlcXVlc3QoIkdFVCIsICJodHRwOi8vbG9jYWxob3N0L3ZlcnNpb24iLCBuaWwpCmlmIGVyciAhPSBuaWwgewogICAgcGFuaWMoZXJyKQp9CgpyZXNwLCBlcnIgOj0gY2xpLkRvKHJlcSkKaWYgZXJyICE9IG5pbCB7CiAgICBwYW5pYyhlcnIpCn0KCi8vIHJlc3AgY29udGFpbnMgdGhlIHJlc3BvbnNlIGZyb20gdGhlIGRhZW1vbi4=', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-go" data-lang="go"><span class="line"><span class="cl"><span class="nx">cli</span><span class="w"> </span><span class="o">:=</span><span class="w"> </span><span class="o">&amp;</span><span class="nx">http</span><span class="p">.</span><span class="nx">Client</span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nx">Transport</span><span class="p">:</span><span class="w"> </span><span class="o">&amp;</span><span class="nx">http</span><span class="p">.</span><span class="nx">Transport</span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nx">DialContext</span><span class="p">:</span><span class="w"> </span><span class="kd">func</span><span class="p">(</span><span class="nx">_</span><span class="w"> </span><span class="nx">context</span><span class="p">.</span><span class="nx">Context</span><span class="p">,</span><span class="w"> </span><span class="nx">_</span><span class="p">,</span><span class="w"> </span><span class="nx">_</span><span class="w"> </span><span class="kt">string</span><span class="p">)</span><span class="w"> </span><span class="p">(</span><span class="nx">net</span><span class="p">.</span><span class="nx">Conn</span><span class="p">,</span><span class="w"> </span><span class="kt">error</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="nx">net</span><span class="p">.</span><span class="nf">Dial</span><span class="p">(</span><span class="s">&#34;unix&#34;</span><span class="p">,</span><span class="w"> </span><span class="s">&#34;/var/run/docker.sock&#34;</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="p">},</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="p">},</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="p">}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nx">req</span><span class="p">,</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">:=</span><span class="w"> </span><span class="nx">http</span><span class="p">.</span><span class="nf">NewRequest</span><span class="p">(</span><span class="s">&#34;GET&#34;</span><span class="p">,</span><span class="w"> </span><span class="s">&#34;http://localhost/version&#34;</span><span class="p">,</span><span class="w"> </span><span class="kc">nil</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="k">if</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">!=</span><span class="w"> </span><span class="kc">nil</span><span class="w"> </span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="p">}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nx">resp</span><span class="p">,</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">:=</span><span class="w"> </span><span class="nx">cli</span><span class="p">.</span><span class="nf">Do</span><span class="p">(</span><span class="nx">req</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="k">if</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">!=</span><span class="w"> </span><span class="kc">nil</span><span class="w"> </span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="p">}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c1">// resp contains the response from the daemon.</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>使用 Go 通过端口：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Y2xpIDo9ICZodHRwLkNsaWVudHsKICAgIFRyYW5zcG9ydDogJmh0dHAuVHJhbnNwb3J0e30sCn0KCnJlcSwgZXJyIDo9IGh0dHAuTmV3UmVxdWVzdCgiR0VUIiwgImh0dHBzOi8vbG9jYWxob3N0OjIzNzYvdmVyc2lvbiIsIG5pbCkKaWYgZXJyICE9IG5pbCB7CiAgICBwYW5pYyhlcnIpCn0KCnJlc3AsIGVyciA6PSBjbGkuRG8ocmVxKQppZiBlcnIgIT0gbmlsIHsKICAgIHBhbmljKGVycikKfQoKLy8gcmVzcCBjb250YWlucyB0aGUgcmVzcG9uc2UgZnJvbSB0aGUgZGFlbW9uLg==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-go" data-lang="go"><span class="line"><span class="cl"><span class="nx">cli</span><span class="w"> </span><span class="o">:=</span><span class="w"> </span><span class="o">&amp;</span><span class="nx">http</span><span class="p">.</span><span class="nx">Client</span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nx">Transport</span><span class="p">:</span><span class="w"> </span><span class="o">&amp;</span><span class="nx">http</span><span class="p">.</span><span class="nx">Transport</span><span class="p">{},</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="p">}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nx">req</span><span class="p">,</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">:=</span><span class="w"> </span><span class="nx">http</span><span class="p">.</span><span class="nf">NewRequest</span><span class="p">(</span><span class="s">&#34;GET&#34;</span><span class="p">,</span><span class="w"> </span><span class="s">&#34;https://localhost:2376/version&#34;</span><span class="p">,</span><span class="w"> </span><span class="kc">nil</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="k">if</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">!=</span><span class="w"> </span><span class="kc">nil</span><span class="w"> </span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="p">}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nx">resp</span><span class="p">,</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">:=</span><span class="w"> </span><span class="nx">cli</span><span class="p">.</span><span class="nf">Do</span><span class="p">(</span><span class="nx">req</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="k">if</span><span class="w"> </span><span class="nx">err</span><span class="w"> </span><span class="o">!=</span><span class="w"> </span><span class="kc">nil</span><span class="w"> </span><span class="p">{</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nb">panic</span><span class="p">(</span><span class="nx">err</span><span class="p">)</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="p">}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="c1">// resp contains the response from the daemon.</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="dockerfile-指令">
  <a class="text-black dark:text-white no-underline hover:underline" href="#dockerfile-%e6%8c%87%e4%bb%a4">
    Dockerfile 指令
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="dockerfile-指令-1">
  <a class="text-black dark:text-white no-underline hover:underline" href="#dockerfile-%e6%8c%87%e4%bb%a4-1">
    Dockerfile 指令
  </a>
</h3>

<p>返回 Dockerfile 指令列表。</p>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="dockerfile-指令-2">
  <a class="text-black dark:text-white no-underline hover:underline" href="#dockerfile-%e6%8c%87%e4%bb%a4-2">
    Dockerfile 指令
  </a>
</h3>

<p>返回 Dockerfile 指令列表。</p>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="构建">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9e%84%e5%bb%ba">
    构建
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="构建镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9e%84%e5%bb%ba%e9%95%9c%e5%83%8f">
    构建镜像
  </a>
</h3>

<p><code>POST /build</code></p>
<p>构建镜像。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>注意</strong></p>
<p>此端点仅在 API &gt;= 1.31 时可用。它在较旧的 API 版本中使用 <code>/commit</code>。</p>

  </blockquote>

<p><strong>查询参数：</strong></p>
<ul>
<li><strong>t</strong> – 镜像的可选名称。</li>
<li><strong>remote</strong> – 远程 Git 仓库的 URL，如果空字符串则从 STDIN 读取上下文。</li>
<li><strong>q</strong> – 保持安静，仅向客户端发送错误。</li>
<li><strong>nocache</strong> – 不使用缓存。</li>
<li><strong>pull</strong> – 总是尝试拉取所有镜像的较新版本。</li>
<li><strong>rm</strong> – 构建成功后删除中间容器。</li>
<li><strong>forcerm</strong> – 始终删除中间容器，除非构建失败。</li>
<li><strong>memory</strong> – 内存限制</li>
<li><strong>memswap</strong> – 总内存（内存 + swap），设置 <code>-1</code> 以启用无限制交换。</li>
<li><strong>cpushares</strong> – CPU 份额（相对权重）。</li>
<li><strong>cpusetcpus</strong> – 允许执行的 CPU（0-3, 0,1）。</li>
<li><strong>cpusetmems</strong> – 允许执行的内存节点（MEM,0-3, 0,1）。</li>
<li><strong>buildargs</strong> – JSON 映射的字符串对 <code>{&quot;Arg1&quot;: &quot;Value1&quot;, &quot;Arg2&quot;: &quot;Value2&quot; }</code>. 查看 <a class="link" href="https://docs.docker.com/engine/reference/builder/#arg" rel="noopener">使用构建时变量</a> 了解详细信息。</li>
<li><strong>shmsize</strong> – <code>/dev/shm</code> 的大小，以字节为单位。</li>
<li><strong>squash</strong> – 将构建过程中的所有图层压缩成一个图层。</li>
<li><strong>labels</strong> – JSON 映射的字符串对。查看 <a class="link" href="https://docs.docker.com/config/labels-custom-metadata/" rel="noopener">标签</a> 了解详细信息。</li>
<li><strong>networkmode</strong> – 默认为 <code>default</code> 的网络模式。支持的标准值为：<code>bridge</code>、<code>host</code>、<code>none</code>、<code>container:&lt;name|id&gt;</code> 和 <code>default</code>。</li>
<li><strong>platform</strong> – 构建镜像的目标平台。</li>
<li><strong>target</strong> – 构建时目标阶段的名称。</li>
<li><strong>outputs</strong> – 输出配置。格式：<code>type=docker,dest=-</code></li>
</ul>
<p><strong>请求体：</strong></p>
<p>构建上下文 <code>&quot;Content-type:&quot; &quot;application/x-tar&quot;</code></p>
<p>可以通过将 Dockerfile 作为 tar 存档传递给 Docker 守护进程来构建 Docker 镜像。存档应该包含构建 Docker 镜像所需的所有文件。注意：在 Docker 1.0.1 版本之前，构建过程将递归地将所有文件发送到守护进程。</p>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvYnVpbGQgSFRUUC8xLjEKQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXRhcgoKWy4uLnRhciBjb250ZW50cy4uLl0=', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/build HTTP/1.1
</span></span><span class="line"><span class="cl">Content-Type: application/x-tar
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">[...tar contents...]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应体：</strong></p>
<p>流，格式为：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'eyJzdHJlYW0iOiAiU3RlcCAxLzIuLi4ifQp7InN0cmVhbSI6ICIuLi4ifQp7ImVycm9yIjogIkVycm9yLi4uIiwgImVycm9yRGV0YWlsIjogeyJtZXNzYWdlIjogIkVycm9yLi4uIn19Cnsic3RyZWFtIjogIlN1Y2Nlc3NmdWxseSBidWlsdCA1MGYwZTAxZjg4YjJcbiJ9', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Step 1/2...&#34;}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;...&#34;}
</span></span><span class="line"><span class="cl">{&#34;error&#34;: &#34;Error...&#34;, &#34;errorDetail&#34;: {&#34;message&#34;: &#34;Error...&#34;}}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Successfully built 50f0e01f88b2\n&#34;}</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 构建上下文已接受，流已开始。</li>
<li><strong>204</strong> – 构建成功，没有流。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查构建">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e6%9e%84%e5%bb%ba">
    检查构建
  </a>
</h3>

<p><code>POST /build/prune</code></p>
<p>删除未使用的构建缓存。</p>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>keep-storage</strong> – 要保留的构建缓存的字节数。默认全部删除。</li>
<li><strong>filter</strong> – 用于过滤结果的值（例如，<code>'until=24h'</code>）。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查构建-1">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e6%9e%84%e5%bb%ba-1">
    检查构建
  </a>
</h3>

<p><code>GET /build/prune</code></p>
<p>返回要删除的构建缓存的大小。</p>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>filter</strong> – 用于过滤结果的值（例如，<code>'until=24h'</code>）。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>

<h2 class=" scroll-mt-20 flex items-center gap-2" id="镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e9%95%9c%e5%83%8f">
    镜像
  </a>
</h2>


<h3 class=" scroll-mt-20 flex items-center gap-2" id="列出镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%97%e5%87%ba%e9%95%9c%e5%83%8f">
    列出镜像
  </a>
</h3>

<p><code>GET /images/json</code></p>
<p>返回 Docker 守护进程中存储的镜像列表。</p>
<p><strong>查询参数：</strong></p>
<ul>
<li>
<p><strong>all</strong> – 显示所有镜像。仅显示顶层镜像的默认值为 false。</p>
</li>
<li>
<p><strong>filters</strong> – JSON 编码的值映射，用于按条件过滤结果。</p>
<p>可用的过滤器：</p>
<ul>
<li><code>dangling=true</code></li>
<li><code>label=key</code> 或 <code>label=&quot;key=value&quot;</code> 的镜像必须包含标签，或具有指定值的标签。</li>
<li><code>before</code> 接受镜像名称或标签，或短镜像 ID。例如，<code>before=nginx:latest</code>、<code>before=nginx:1.13.0</code> 或 <code>before=a24bb4013296</code>。结果集会扩展为包括在引用镜像之前创建的所有镜像。</li>
<li><code>reference</code> 根据提供的模式过滤镜像。例如，<code>reference=nginx:*</code>。</li>
<li><code>shared-size</code> 接受镜像名称、标签、短镜像 ID 或完整镜像 ID。例如，<code>shared-size=nginx:latest</code>、<code>shared-size=nginx:1.13.0</code>、<code>shared-size=a24bb4013296</code> 或 <code>shared-size=sha256:983488c45c22ec896af1253453fad4404f816023cee5037c8177f8ca2c5d9424</code>。结果集会扩展到包括与引用镜像共享图层的所有镜像。</li>
<li><code>size</code> 接受镜像名称、标签、短镜像 ID 或完整镜像 ID。例如，<code>size=nginx:latest</code>、<code>size=nginx:1.13.0</code>、<code>size=a24bb4013296</code> 或 <code>size=sha256:983488c45c22ec896af1253453fad4404f816023cee5037c8177f8ca2c5d9424</code>。结果集会扩展到包括与引用镜像具有相同大小的所有镜像。</li>
</ul>
</li>
<li>
<p><strong>digests</strong> – 仅在 API &gt;= 1.25 时可用。如果设置为 <code>true</code>，则为每个镜像返回摘要。</p>
</li>
<li>
<p><strong>shared-size</strong> – 仅在 API &gt;= 1.30 时可用。如果设置为 <code>true</code>，则为每个镜像返回共享大小。</p>
</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="构建镜像-1">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9e%84%e5%bb%ba%e9%95%9c%e5%83%8f-1">
    构建镜像
  </a>
</h3>

<p><code>POST /build</code></p>
<p>构建镜像。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>注意</strong></p>
<p>此端点仅在 API &gt;= 1.31 时可用。它在较旧的 API 版本中使用 <code>/commit</code>。</p>

  </blockquote>

<p><strong>查询参数：</strong></p>
<ul>
<li><strong>t</strong> – 镜像的可选名称。</li>
<li><strong>remote</strong> – 远程 Git 仓库的 URL，如果空字符串则从 STDIN 读取上下文。</li>
<li><strong>q</strong> – 保持安静，仅向客户端发送错误。</li>
<li><strong>nocache</strong> – 不使用缓存。</li>
<li><strong>pull</strong> – 总是尝试拉取所有镜像的较新版本。</li>
<li><strong>rm</strong> – 构建成功后删除中间容器。</li>
<li><strong>forcerm</strong> – 始终删除中间容器，除非构建失败。</li>
<li><strong>memory</strong> – 内存限制</li>
<li><strong>memswap</strong> – 总内存（内存 + swap），设置 <code>-1</code> 以启用无限制交换。</li>
<li><strong>cpushares</strong> – CPU 份额（相对权重）。</li>
<li><strong>cpusetcpus</strong> – 允许执行的 CPU（0-3, 0,1）。</li>
<li><strong>cpusetmems</strong> – 允许执行的内存节点（MEM,0-3, 0,1）。</li>
<li><strong>buildargs</strong> – JSON 映射的字符串对 <code>{&quot;Arg1&quot;: &quot;Value1&quot;, &quot;Arg2&quot;: &quot;Value2&quot; }</code>. 查看 <a class="link" href="https://docs.docker.com/engine/reference/builder/#arg" rel="noopener">使用构建时变量</a> 了解详细信息。</li>
<li><strong>shmsize</strong> – <code>/dev/shm</code> 的大小，以字节为单位。</li>
<li><strong>squash</strong> – 将构建过程中的所有图层压缩成一个图层。</li>
<li><strong>labels</strong> – JSON 映射的字符串对。查看 <a class="link" href="https://docs.docker.com/config/labels-custom-metadata/" rel="noopener">标签</a> 了解详细信息。</li>
<li><strong>networkmode</strong> – 默认为 <code>default</code> 的网络模式。支持的标准值为：<code>bridge</code>、<code>host</code>、<code>none</code>、<code>container:&lt;name|id&gt;</code> 和 <code>default</code>。</li>
<li><strong>platform</strong> – 构建镜像的目标平台。</li>
<li><strong>target</strong> – 构建时目标阶段的名称。</li>
<li><strong>outputs</strong> – 输出配置。格式：<code>type=docker,dest=-</code></li>
</ul>
<p><strong>请求体：</strong></p>
<p>构建上下文 <code>&quot;Content-type:&quot; &quot;application/x-tar&quot;</code></p>
<p>可以通过将 Dockerfile 作为 tar 存档传递给 Docker 守护进程来构建 Docker 镜像。存档应该包含构建 Docker 镜像所需的所有文件。注意：在 Docker 1.0.1 版本之前，构建过程将递归地将所有文件发送到守护进程。</p>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvYnVpbGQgSFRUUC8xLjEKQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXRhcgoKWy4uLnRhciBjb250ZW50cy4uLl0=', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/build HTTP/1.1
</span></span><span class="line"><span class="cl">Content-Type: application/x-tar
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">[...tar contents...]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应体：</strong></p>
<p>流，格式为：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'eyJzdHJlYW0iOiAiU3RlcCAxLzIuLi4ifQp7InN0cmVhbSI6ICIuLi4ifQp7ImVycm9yIjogIkVycm9yLi4uIiwgImVycm9yRGV0YWlsIjogeyJtZXNzYWdlIjogIkVycm9yLi4uIn19Cnsic3RyZWFtIjogIlN1Y2Nlc3NmdWxseSBidWlsdCA1MGYwZTAxZjg4YjJcbiJ9', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Step 1/2...&#34;}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;...&#34;}
</span></span><span class="line"><span class="cl">{&#34;error&#34;: &#34;Error...&#34;, &#34;errorDetail&#34;: {&#34;message&#34;: &#34;Error...&#34;}}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Successfully built 50f0e01f88b2\n&#34;}</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 构建上下文已接受，流已开始。</li>
<li><strong>204</strong> – 构建成功，没有流。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="创建镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%9b%e5%bb%ba%e9%95%9c%e5%83%8f">
    创建镜像
  </a>
</h3>

<p><code>POST /images/create</code></p>
<p>从 Docker 守护进程的镜像库中拉取镜像或从 tarball 中导入。</p>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>fromImage</strong> – 使用 <code>image[:tag]</code>、<code>image[@digest]</code> 或 <code>algo:digest</code> 指定要拉取的镜像。当同时指定时，<code>fromImage</code> 优先于 <code>fromSrc</code>。</li>
<li><strong>fromSrc</strong> – 源 tarball 的 ID。可以是从构建 API 返回的 ID、本地文件（<code>fromSrc=image.tar</code>）或远程 URL（<code>fromSrc=-</code> 表示 STDIN）。当同时指定时，<code>fromImage</code> 优先于 <code>fromSrc</code>。</li>
<li><strong>repo</strong> – 镜像的存储库。</li>
<li><strong>tag</strong> – 镜像的标签。</li>
<li><strong>message</strong> – 导入时要包含的消息。</li>
<li><strong>platform</strong> – 如果可以使用多个平台，则用于拉取镜像的平台。</li>
<li><strong>changes</strong> – 应用于从 <code>fromSrc</code> 创建的容器的 <code>Dockerfile</code> 指令列表。</li>
<li><strong>outputMode</strong> – 仅在 API &gt;= 1.47 时可用。如果设置为 <code>auto</code>，则在从 tarball 导入时返回镜像 ID。</li>
</ul>
<p><strong>请求头：</strong></p>
<p>如果从 tarball 导入，<code>Content-Type</code> 应该是 <code>application/x-tar</code>.</p>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvaW1hZ2VzL2NyZWF0ZT9mcm9tSW1hZ2U9YWxwaW5lOmxhdGVzdCBIVFRQLzEuMQ==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/images/create?fromImage=alpine:latest HTTP/1.1</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvaW1hZ2VzL2NyZWF0ZT9mcm9tU3JjPS0mcmVwbz1oZWxsby13b3JsZCBIVFRQLzEuMQpDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL3gtdGFyCgpbLi4udGFyIGNvbnRlbnQuLi5d', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/images/create?fromSrc=-&amp;repo=hello-world HTTP/1.1
</span></span><span class="line"><span class="cl">Content-Type: application/x-tar
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">[...tar content...]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvaW1hZ2VzL2NyZWF0ZT9mcm9tSW1hZ2U9YWxwaW5lOmxhdGVzdCZwbGF0Zm9ybT1hcm0lMkZ2NyBIVFRQLzEuMQ==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/images/create?fromImage=alpine:latest&amp;platform=arm%2Fv7 HTTP/1.1</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应体：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'eyJzdGF0dXMiOiAiUHVsbGluZy4uLiJ9Cnsic3RhdHVzIjogIlB1bGxpbmciLCAicHJvZ3Jlc3MiOiAiMSBCLyAxMDBCIiwgInByb2dyZXNzRGV0YWlsIjogeyJjdXJyZW50IjogMSwgInRvdGFsIjogMTAwfX0KeyJlcnJvciI6ICJJbnZhbGlkLi4uIn0KLi4uCnsic3RhdHVzIjogIlB1bGwgY29tcGxldGUifQ==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">{&#34;status&#34;: &#34;Pulling...&#34;}
</span></span><span class="line"><span class="cl">{&#34;status&#34;: &#34;Pulling&#34;, &#34;progress&#34;: &#34;1 B/ 100B&#34;, &#34;progressDetail&#34;: {&#34;current&#34;: 1, &#34;total&#34;: 100}}
</span></span><span class="line"><span class="cl">{&#34;error&#34;: &#34;Invalid...&#34;}
</span></span><span class="line"><span class="cl">...
</span></span><span class="line"><span class="cl">{&#34;status&#34;: &#34;Pull complete&#34;}</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 没有错误。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e9%95%9c%e5%83%8f">
    检查镜像
  </a>
</h3>

<p><code>GET /images/{name}/json</code></p>
<p>返回关于单个镜像的信息。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>size</strong> – 仅在 API &gt;= 1.29 时可用。如果设置为 <code>true</code>，则在响应中包含镜像的大小。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="获取镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%8e%b7%e5%8f%96%e9%95%9c%e5%83%8f">
    获取镜像
  </a>
</h3>

<p><code>GET /images/{name}/get</code></p>
<p>获取镜像的 tarball，可以是单个镜像或仓库。</p>
<p>如果名称是镜像 ID，则会将镜像的 tarball 作为流返回。</p>
<p>如果名称是镜像名称或名称和标签，则会将仓库的 tarball 作为流返回，其中包含所有具有该名称和标签的所有镜像。</p>
<p>下载多个镜像时，流的格式与 <code>docker save</code> 的输出相同。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检索的镜像或仓库的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>allTags</strong> – 如果存在，则除了镜像 ID 之外，还会下载具有 <code>name</code> 的所有镜像。</li>
</ul>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'R0VUIC92MS40OC9pbWFnZXMvZXhhbXBsZSUyRjIwNDg6bGF0ZXN0L2dldCBIVFRQLzEuMQ==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">GET /v1.48/images/example%2F2048:latest/get HTTP/1.1</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应头：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Q29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXRhcg==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">Content-Type: application/x-tar</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 请求成功，镜像作为 tar 流返回。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/x-tar</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="获取镜像的所有图层">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%8e%b7%e5%8f%96%e9%95%9c%e5%83%8f%e7%9a%84%e6%89%80%e6%9c%89%e5%9b%be%e5%b1%82">
    获取镜像的所有图层
  </a>
</h3>

<p><code>GET /images/get</code></p>
<p>获取一个或多个镜像的所有图层的 tarball。</p>
<p>对于每个镜像，会有一个 tar 包含图层。</p>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>names</strong> – 要检索的镜像的名称或 ID。</li>
</ul>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'R0VUIC92MS40OC9pbWFnZXMvZ2V0P25hbWVzPXNvbWVJbWFnZSZuYW1lcz1leGFtcGxlJTJGMjA0ODpsYXRlc3QmbmFtZXM9YWxwaW5lOjMuNSBIVFRQLzEuMQ==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">GET /v1.48/images/get?names=someImage&amp;names=example%2F2048:latest&amp;names=alpine:3.5 HTTP/1.1</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应头：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Q29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXRhcg==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">Content-Type: application/x-tar</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 请求成功，镜像作为 tar 流返回。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/x-tar</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="加载镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%8a%a0%e8%bd%bd%e9%95%9c%e5%83%8f">
    加载镜像
  </a>
</h3>

<p><code>POST /images/load</code></p>
<p>将镜像加载到 Docker 守护进程中。</p>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>quiet</strong> – 仅在 API &gt;= 1.23 时可用。</li>
<li><strong>stream</strong> – 仅在 API &gt;= 1.47 时可用。如果设置为 <code>true</code>，则在加载 tarball 时将响应作为流返回。</li>
</ul>
<p><strong>请求头：</strong></p>
<p><code>Content-Type</code> 应该是 <code>application/x-tar</code>.</p>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvaW1hZ2VzL2xvYWQ/cXVpZXQ9MCBIVFRQLzEuMQpDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL3gtdGFyCkNvbnRlbnQtTGVuZ3RoOiA5ODU3ClsuLi50YXIgY29udGVudHMuLi5d', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/images/load?quiet=0 HTTP/1.1
</span></span><span class="line"><span class="cl">Content-Type: application/x-tar
</span></span><span class="line"><span class="cl">Content-Length: 9857
</span></span><span class="line"><span class="cl">[...tar contents...]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvaW1hZ2VzL2xvYWQ/c3RyZWFtPXRydWUgSFRUUC8xLjEKQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXRhcgpDb250ZW50LUxlbmd0aDogOTg1NwpbLi4udGFyIGNvbnRlbnRzLi4uXQ==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/images/load?stream=true HTTP/1.1
</span></span><span class="line"><span class="cl">Content-Type: application/x-tar
</span></span><span class="line"><span class="cl">Content-Length: 9857
</span></span><span class="line"><span class="cl">[...tar contents...]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应体：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'eyJzdHJlYW0iOiAiTG9hZGluZyBsYXllciJ9Cnsic3RyZWFtIjogIi4uLiJ9CnsiZXJyb3IiOiAiRXJyb3IuLi4iLCAiZXJyb3JEZXRhaWwiOiB7Im1lc3NhZ2UiOiAiRXJyb3IuLi4ifX0KeyJzdHJlYW0iOiAiTG9hZGluZyBjb21wbGV0ZSJ9', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Loading layer&#34;}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;...&#34;}
</span></span><span class="line"><span class="cl">{&#34;error&#34;: &#34;Error...&#34;, &#34;errorDetail&#34;: {&#34;message&#34;: &#34;Error...&#34;}}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Loading complete&#34;}</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 没有错误。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="删除镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%a0%e9%99%a4%e9%95%9c%e5%83%8f">
    删除镜像
  </a>
</h3>

<p><code>DELETE /images/{name}</code></p>
<p>删除一个或多个镜像。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要删除的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>force</strong> – 强制删除镜像</li>
<li><strong>noprune</strong> – 不删除未标记的父镜像</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 镜像已成功删除。</li>
<li><strong>404</strong> – 镜像未找到</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="搜索-docker-hub">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%90%9c%e7%b4%a2-docker-hub">
    搜索 Docker Hub
  </a>
</h3>

<p><code>GET /images/search</code></p>
<p>搜索 Docker Hub 或守护进程配置的注册表。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>注意</strong></p>
<p>使用此端点搜索注册表 2.0+（如 Docker Hub）仅在守护进程配置为使用注册表 2.0+ 时有效。</p>

  </blockquote>

<p><strong>查询参数：</strong></p>
<ul>
<li>
<p><strong>term</strong> – 要搜索的术语。</p>
</li>
<li>
<p><strong>limit</strong> – 搜索结果的最大数量。</p>
</li>
<li>
<p><strong>filters</strong> – JSON 编码的值映射，用于按条件过滤结果。</p>
<p>可用的过滤器：</p>
<ul>
<li><code>is-automated=true</code></li>
<li><code>is-official=true</code></li>
<li><code>stars=N</code></li>
</ul>
</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 没有错误。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="构建镜像-2">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9e%84%e5%bb%ba%e9%95%9c%e5%83%8f-2">
    构建镜像
  </a>
</h3>

<p><code>POST /build</code></p>
<p>构建镜像。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>注意</strong></p>
<p>此端点仅在 API &gt;= 1.31 时可用。它在较旧的 API 版本中使用 <code>/commit</code>。</p>

  </blockquote>

<p><strong>查询参数：</strong></p>
<ul>
<li><strong>t</strong> – 镜像的可选名称。</li>
<li><strong>remote</strong> – 远程 Git 仓库的 URL，如果空字符串则从 STDIN 读取上下文。</li>
<li><strong>q</strong> – 保持安静，仅向客户端发送错误。</li>
<li><strong>nocache</strong> – 不使用缓存。</li>
<li><strong>pull</strong> – 总是尝试拉取所有镜像的较新版本。</li>
<li><strong>rm</strong> – 构建成功后删除中间容器。</li>
<li><strong>forcerm</strong> – 始终删除中间容器，除非构建失败。</li>
<li><strong>memory</strong> – 内存限制</li>
<li><strong>memswap</strong> – 总内存（内存 + swap），设置 <code>-1</code> 以启用无限制交换。</li>
<li><strong>cpushares</strong> – CPU 份额（相对权重）。</li>
<li><strong>cpusetcpus</strong> – 允许执行的 CPU（0-3, 0,1）。</li>
<li><strong>cpusetmems</strong> – 允许执行的内存节点（MEM,0-3, 0,1）。</li>
<li><strong>buildargs</strong> – JSON 映射的字符串对 <code>{&quot;Arg1&quot;: &quot;Value1&quot;, &quot;Arg2&quot;: &quot;Value2&quot; }</code>. 查看 <a class="link" href="https://docs.docker.com/engine/reference/builder/#arg" rel="noopener">使用构建时变量</a> 了解详细信息。</li>
<li><strong>shmsize</strong> – <code>/dev/shm</code> 的大小，以字节为单位。</li>
<li><strong>squash</strong> – 将构建过程中的所有图层压缩成一个图层。</li>
<li><strong>labels</strong> – JSON 映射的字符串对。查看 <a class="link" href="https://docs.docker.com/config/labels-custom-metadata/" rel="noopener">标签</a> 了解详细信息。</li>
<li><strong>networkmode</strong> – 默认为 <code>default</code> 的网络模式。支持的标准值为：<code>bridge</code>、<code>host</code>、<code>none</code>、<code>container:&lt;name|id&gt;</code> 和 <code>default</code>。</li>
<li><strong>platform</strong> – 构建镜像的目标平台。</li>
<li><strong>target</strong> – 构建时目标阶段的名称。</li>
<li><strong>outputs</strong> – 输出配置。格式：<code>type=docker,dest=-</code></li>
</ul>
<p><strong>请求体：</strong></p>
<p>构建上下文 <code>&quot;Content-type:&quot; &quot;application/x-tar&quot;</code></p>
<p>可以通过将 Dockerfile 作为 tar 存档传递给 Docker 守护进程来构建 Docker 镜像。存档应该包含构建 Docker 镜像所需的所有文件。注意：在 Docker 1.0.1 版本之前，构建过程将递归地将所有文件发送到守护进程。</p>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvYnVpbGQgSFRUUC8xLjEKQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXRhcgoKWy4uLnRhciBjb250ZW50cy4uLl0=', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/build HTTP/1.1
</span></span><span class="line"><span class="cl">Content-Type: application/x-tar
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">[...tar contents...]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应体：</strong></p>
<p>流，格式为：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'eyJzdHJlYW0iOiAiU3RlcCAxLzIuLi4ifQp7InN0cmVhbSI6ICIuLi4ifQp7ImVycm9yIjogIkVycm9yLi4uIiwgImVycm9yRGV0YWlsIjogeyJtZXNzYWdlIjogIkVycm9yLi4uIn19Cnsic3RyZWFtIjogIlN1Y2Nlc3NmdWxseSBidWlsdCA1MGYwZTAxZjg4YjJcbiJ9', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Step 1/2...&#34;}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;...&#34;}
</span></span><span class="line"><span class="cl">{&#34;error&#34;: &#34;Error...&#34;, &#34;errorDetail&#34;: {&#34;message&#34;: &#34;Error...&#34;}}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Successfully built 50f0e01f88b2\n&#34;}</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 构建上下文已接受，流已开始。</li>
<li><strong>204</strong> – 构建成功，没有流。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="构建镜像-3">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%9e%84%e5%bb%ba%e9%95%9c%e5%83%8f-3">
    构建镜像
  </a>
</h3>

<p><code>POST /build</code></p>
<p>构建镜像。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p><strong>注意</strong></p>
<p>此端点仅在 API &gt;= 1.31 时可用。它在较旧的 API 版本中使用 <code>/commit</code>。</p>

  </blockquote>

<p><strong>查询参数：</strong></p>
<ul>
<li><strong>t</strong> – 镜像的可选名称。</li>
<li><strong>remote</strong> – 远程 Git 仓库的 URL，如果空字符串则从 STDIN 读取上下文。</li>
<li><strong>q</strong> – 保持安静，仅向客户端发送错误。</li>
<li><strong>nocache</strong> – 不使用缓存。</li>
<li><strong>pull</strong> – 总是尝试拉取所有镜像的较新版本。</li>
<li><strong>rm</strong> – 构建成功后删除中间容器。</li>
<li><strong>forcerm</strong> – 始终删除中间容器，除非构建失败。</li>
<li><strong>memory</strong> – 内存限制</li>
<li><strong>memswap</strong> – 总内存（内存 + swap），设置 <code>-1</code> 以启用无限制交换。</li>
<li><strong>cpushares</strong> – CPU 份额（相对权重）。</li>
<li><strong>cpusetcpus</strong> – 允许执行的 CPU（0-3, 0,1）。</li>
<li><strong>cpusetmems</strong> – 允许执行的内存节点（MEM,0-3, 0,1）。</li>
<li><strong>buildargs</strong> – JSON 映射的字符串对 <code>{&quot;Arg1&quot;: &quot;Value1&quot;, &quot;Arg2&quot;: &quot;Value2&quot; }</code>. 查看 <a class="link" href="https://docs.docker.com/engine/reference/builder/#arg" rel="noopener">使用构建时变量</a> 了解详细信息。</li>
<li><strong>shmsize</strong> – <code>/dev/shm</code> 的大小，以字节为单位。</li>
<li><strong>squash</strong> – 将构建过程中的所有图层压缩成一个图层。</li>
<li><strong>labels</strong> – JSON 映射的字符串对。查看 <a class="link" href="https://docs.docker.com/config/labels-custom-metadata/" rel="noopener">标签</a> 了解详细信息。</li>
<li><strong>networkmode</strong> – 默认为 <code>default</code> 的网络模式。支持的标准值为：<code>bridge</code>、<code>host</code>、<code>none</code>、<code>container:&lt;name|id&gt;</code> 和 <code>default</code>。</li>
<li><strong>platform</strong> – 构建镜像的目标平台。</li>
<li><strong>target</strong> – 构建时目标阶段的名称。</li>
<li><strong>outputs</strong> – 输出配置。格式：<code>type=docker,dest=-</code></li>
</ul>
<p><strong>请求体：</strong></p>
<p>构建上下文 <code>&quot;Content-type:&quot; &quot;application/x-tar&quot;</code></p>
<p>可以通过将 Dockerfile 作为 tar 存档传递给 Docker 守护进程来构建 Docker 镜像。存档应该包含构建 Docker 镜像所需的所有文件。注意：在 Docker 1.0.1 版本之前，构建过程将递归地将所有文件发送到守护进程。</p>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvYnVpbGQgSFRUUC8xLjEKQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXRhcgoKWy4uLnRhciBjb250ZW50cy4uLl0=', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/build HTTP/1.1
</span></span><span class="line"><span class="cl">Content-Type: application/x-tar
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">[...tar contents...]</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>响应体：</strong></p>
<p>流，格式为：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'eyJzdHJlYW0iOiAiU3RlcCAxLzIuLi4ifQp7InN0cmVhbSI6ICIuLi4ifQp7ImVycm9yIjogIkVycm9yLi4uIiwgImVycm9yRGV0YWlsIjogeyJtZXNzYWdlIjogIkVycm9yLi4uIn19Cnsic3RyZWFtIjogIlN1Y2Nlc3NmdWxseSBidWlsdCA1MGYwZTAxZjg4YjJcbiJ9', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Step 1/2...&#34;}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;...&#34;}
</span></span><span class="line"><span class="cl">{&#34;error&#34;: &#34;Error...&#34;, &#34;errorDetail&#34;: {&#34;message&#34;: &#34;Error...&#34;}}
</span></span><span class="line"><span class="cl">{&#34;stream&#34;: &#34;Successfully built 50f0e01f88b2\n&#34;}</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 构建上下文已接受，流已开始。</li>
<li><strong>204</strong> – 构建成功，没有流。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="标记镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a0%87%e8%ae%b0%e9%95%9c%e5%83%8f">
    标记镜像
  </a>
</h3>

<p><code>POST /images/{name}/tag</code></p>
<p>将镜像标记到仓库中。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要标记的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>repo</strong> – 镜像的存储库。</li>
<li><strong>tag</strong> – 镜像的可选标签。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>201</strong> – 镜像已成功标记。</li>
<li><strong>400</strong> – 错误参数</li>
<li><strong>404</strong> – 镜像未找到</li>
<li><strong>409</strong> – 标签已存在，无错误</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查镜像-1">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e9%95%9c%e5%83%8f-1">
    检查镜像
  </a>
</h3>

<p><code>GET /images/{name}/json</code></p>
<p>返回关于单个镜像的信息。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>size</strong> – 仅在 API &gt;= 1.29 时可用。如果设置为 <code>true</code>，则在响应中包含镜像的大小。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="获取镜像的构建历史">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%8e%b7%e5%8f%96%e9%95%9c%e5%83%8f%e7%9a%84%e6%9e%84%e5%bb%ba%e5%8e%86%e5%8f%b2">
    获取镜像的构建历史
  </a>
</h3>

<p><code>GET /images/{name}/history</code></p>
<p>返回镜像的历史。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="推送镜像">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%8e%a8%e9%80%81%e9%95%9c%e5%83%8f">
    推送镜像
  </a>
</h3>

<p><code>POST /images/{name}/push</code></p>
<p>将镜像推送到仓库。</p>
<p>如果图像名称仅指定图像 ID，Docker 守护进程将返回错误。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要推送的镜像的名称。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>tag</strong> – 要推送的镜像的标签。</li>
</ul>
<p><strong>请求头：</strong></p>
<p>如果图像已经通过身份验证，则应设置 <code>X-Registry-Auth</code>。</p>
<p><strong>示例请求：</strong></p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'UE9TVCAvdjEuNDgvaW1hZ2VzL3Rlc3Q6bGF0ZXN0L3B1c2ggSFRUUC8xLjEKWC1SZWdpc3RyeS1BdXRoOiBleUoxYzJWeWJtRnRaU0k2SW5SbGMzUWlMQ0p3WVhOemQyOXlaQ0k2SW1GelpHWWlMQ0p6WlhKMlpYSWgvND0KQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi9vY3RldC1zdHJlYW0KQ29udGVudC1MZW5ndGg6IDA=', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">POST /v1.48/images/test:latest/push HTTP/1.1
</span></span><span class="line"><span class="cl">X-Registry-Auth: eyJ1c2VybmFtZSI6InRlc3QiLCJwYXNzd29yZCI6ImFzZGYiLCJzZXJ2ZXIh/4=
</span></span><span class="line"><span class="cl">Content-Type: application/octet-stream
</span></span><span class="line"><span class="cl">Content-Length: 0</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 没有错误。</li>
<li><strong>404</strong> – 镜像不存在。</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/octet-stream</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="删除镜像-1">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e5%88%a0%e9%99%a4%e9%95%9c%e5%83%8f-1">
    删除镜像
  </a>
</h3>

<p><code>DELETE /images/{name}</code></p>
<p>删除一个或多个镜像。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要删除的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>force</strong> – 强制删除镜像</li>
<li><strong>noprune</strong> – 不删除未标记的父镜像</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 镜像已成功删除。</li>
<li><strong>404</strong> – 镜像未找到</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查镜像-2">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e9%95%9c%e5%83%8f-2">
    检查镜像
  </a>
</h3>

<p><code>GET /images/{name}/json</code></p>
<p>返回关于单个镜像的信息。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>size</strong> – 仅在 API &gt;= 1.29 时可用。如果设置为 <code>true</code>，则在响应中包含镜像的大小。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查镜像-3">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e9%95%9c%e5%83%8f-3">
    检查镜像
  </a>
</h3>

<p><code>GET /images/{name}/json</code></p>
<p>返回关于单个镜像的信息。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>size</strong> – 仅在 API &gt;= 1.29 时可用。如果设置为 <code>true</code>，则在响应中包含镜像的大小。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="获取镜像的构建历史-1">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%8e%b7%e5%8f%96%e9%95%9c%e5%83%8f%e7%9a%84%e6%9e%84%e5%bb%ba%e5%8e%86%e5%8f%b2-1">
    获取镜像的构建历史
  </a>
</h3>

<p><code>GET /images/{name}/history</code></p>
<p>返回镜像的历史。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查镜像-4">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e9%95%9c%e5%83%8f-4">
    检查镜像
  </a>
</h3>

<p><code>GET /images/{name}/json</code></p>
<p>返回关于单个镜像的信息。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>size</strong> – 仅在 API &gt;= 1.29 时可用。如果设置为 <code>true</code>，则在响应中包含镜像的大小。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="获取镜像的构建历史-2">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e8%8e%b7%e5%8f%96%e9%95%9c%e5%83%8f%e7%9a%84%e6%9e%84%e5%bb%ba%e5%8e%86%e5%8f%b2-2">
    获取镜像的构建历史
  </a>
</h3>

<p><code>GET /images/{name}/history</code></p>
<p>返回镜像的历史。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong> – 服务器错误</li>
</ul>
<p><strong>生产者：</strong></p>
<ul>
<li>application/json</li>
</ul>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="检查镜像-5">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e6%a3%80%e6%9f%a5%e9%95%9c%e5%83%8f-5">
    检查镜像
  </a>
</h3>

<p><code>GET /images/{name}/json</code></p>
<p>返回关于单个镜像的信息。</p>
<p><strong>路径参数：</strong></p>
<ul>
<li><strong>name</strong> – 要检查的镜像的名称或 ID。</li>
</ul>
<p><strong>查询参数：</strong></p>
<ul>
<li><strong>size</strong> – 仅在 API &gt;= 1.29 时可用。如果设置为 <code>true</code>，则在响应中包含镜像的大小。</li>
</ul>
<p><strong>状态码：</strong></p>
<ul>
<li><strong>200</strong> – 成功</li>
<li><strong>404</strong> – 镜像不存在</li>
<li><strong>500</strong></li>
</ul>


**OpenAPI Specification:** [Docker Engine API v1.48 参考文档 API Spec](/reference/api/engine/version/v1.48.yaml)

This page provides interactive API documentation. For the machine-readable OpenAPI specification, see the link above.
