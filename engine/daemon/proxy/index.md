# 守护进程代理配置

<a name="httphttps-proxy"><!-- included for deep-links to old section --></a>

如果您的组织使用代理服务器连接互联网，您可能需要配置 Docker 守护进程以使用代理服务器。守护进程使用代理服务器访问存储在 Docker Hub 和其他注册表中的镜像，以及连接 Docker 集群中的其他节点。

本文档介绍如何为 Docker 守护进程配置代理。有关为 Docker CLI 配置代理设置的说明，请参阅 [配置 Docker CLI 使用代理服务器](/manuals/engine/cli/proxy.md)。

> [!IMPORTANT]
> `daemon.json` 中指定的代理配置会被 Docker Desktop 忽略。如果您使用 Docker Desktop，可以使用 [Docker Desktop 设置](/manuals/desktop/settings-and-maintenance/settings.md#proxies) 配置代理。

有两种方式可以配置这些设置：

- 通过配置文件或 CLI 标志 [配置守护进程](#daemon-configuration)
- 在系统上设置 [环境变量](#environment-variables)

直接配置守护进程优先于环境变量。

## 守护进程配置

您可以在 `daemon.json` 文件中配置守护进程的代理行为，或者使用 `dockerd` 命令的 `--http-proxy` 或 `--https-proxy` 标志。建议使用 `daemon.json` 进行配置。

```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:3128",
    "https-proxy": "https://proxy.example.com:3129",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
  }
}
```

更改配置文件后，重启守护进程以使代理配置生效：

```console
$ sudo systemctl restart docker
```

## 环境变量

Docker 守护进程在启动环境中检查以下环境变量，以配置 HTTP 或 HTTPS 代理行为：

- `HTTP_PROXY`
- `http_proxy`
- `HTTPS_PROXY`
- `https_proxy`
- `NO_PROXY`
- `no_proxy`

### systemd 单元文件

如果您将 Docker 守护进程作为 systemd 服务运行，可以创建一个 systemd drop-in 文件，为 `docker` 服务设置变量。

> **Rootless 模式注意事项**
>
> 在 [rootless 模式](/manuals/engine/security/rootless.md) 下运行 Docker 时，systemd 配置文件的位置不同。在 rootless 模式下运行时，Docker 作为用户模式的 systemd 服务启动，使用存储在每个用户主目录中的文件，位于 `~/.config/systemd/<user>/docker.service.d/`。此外，`systemctl` 必须在不使用 `sudo` 的情况下执行，并使用 `--user` 标志。如果您以 rootless 模式运行 Docker，请选择 "Rootless 模式" 选项卡。








<div
  class="tabs"
  
    x-data="{ selected: '%E5%B8%B8%E8%A7%84%E5%AE%89%E8%A3%85' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E5%B8%B8%E8%A7%84%E5%AE%89%E8%A3%85' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%B8%B8%E8%A7%84%E5%AE%89%E8%A3%85'"
        
      >
        常规安装
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Rootless-%E6%A8%A1%E5%BC%8F' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Rootless-%E6%A8%A1%E5%BC%8F'"
        
      >
        Rootless 模式
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%B8%B8%E8%A7%84%E5%AE%89%E8%A3%85' && 'hidden'"
      >
        <ol>
<li>
<p>为 <code>docker</code> 服务创建一个 systemd drop-in 目录：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIG1rZGlyIC1wIC9ldGMvc3lzdGVtZC9zeXN0ZW0vZG9ja2VyLnNlcnZpY2UuZA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo mkdir -p /etc/systemd/system/docker.service.d
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>创建一个名为 <code>/etc/systemd/system/docker.service.d/http-proxy.conf</code> 的文件，添加 <code>HTTP_PROXY</code> 环境变量：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI4Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://proxy.example.com:3128&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>如果您使用 HTTPS 代理服务器，请设置 <code>HTTPS_PROXY</code> 环境变量：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQU19QUk9YWT1odHRwczovL3Byb3h5LmV4YW1wbGUuY29tOjMxMjki', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTPS_PROXY=https://proxy.example.com:3129&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>可以设置多个环境变量；要同时设置非 HTTPS 和 HTTPS 代理：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI4IgpFbnZpcm9ubWVudD0iSFRUUFNfUFJPWFk9aHR0cHM6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI5Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://proxy.example.com:3128&#34;</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTPS_PROXY=https://proxy.example.com:3129&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>代理值中的特殊字符，如 <code>#?!()[]{}</code>，必须使用 <code>%%</code> 进行双重转义。例如：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9kb21haW4lJTVDdXNlcjpjb21wbGV4JSUyM3Bhc3NAcHJveHkuZXhhbXBsZS5jb206MzEyOC8i', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
    </div>
  </blockquote>

</li>
<li>
<p>如果您有需要直接联系的内部 Docker 注册表，不通过代理，可以通过 <code>NO_PROXY</code> 环境变量指定它们。</p>
<p><code>NO_PROXY</code> 变量指定一个包含逗号分隔值的字符串，用于指定应排除在代理之外的主机。您可以指定以下选项来排除主机：</p>
<ul>
<li>IP 地址前缀（<code>1.2.3.4</code>）</li>
<li>域名，或特殊 DNS 标签（<code>*</code>）</li>
<li>域名匹配该名称及其所有子域名。以 &quot;.&quot; 开头的域名仅匹配子域名。例如，给定域名 <code>foo.example.com</code> 和 <code>example.com</code>：
<ul>
<li><code>example.com</code> 匹配 <code>example.com</code> 和 <code>foo.example.com</code></li>
<li><code>.example.com</code> 仅匹配 <code>foo.example.com</code></li>
</ul>
</li>
<li>单个星号（<code>*</code>）表示不应进行代理</li>
<li>IP 地址前缀（<code>1.2.3.4:80</code>）和域名（<code>foo.example.com:80</code>）接受字面端口号</li>
</ul>
<p>示例：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI4IgpFbnZpcm9ubWVudD0iSFRUUFNfUFJPWFk9aHR0cHM6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI5IgpFbnZpcm9ubWVudD0iTk9fUFJPWFk9bG9jYWxob3N0LDEyNy4wLjAuMSxkb2NrZXItcmVnaXN0cnkuZXhhbXBsZS5jb20sLmNvcnAi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://proxy.example.com:3128&#34;</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTPS_PROXY=https://proxy.example.com:3129&#34;</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>刷新更改并重启 Docker</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCBkYWVtb24tcmVsb2FkCiQgc3VkbyBzeXN0ZW1jdGwgcmVzdGFydCBkb2NrZXI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl daemon-reload
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl restart docker
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>验证配置已加载且与您所做的更改匹配，例如：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCBzaG93IC0tcHJvcGVydHk9RW52aXJvbm1lbnQgZG9ja2VyCgpFbnZpcm9ubWVudD1IVFRQX1BST1hZPWh0dHA6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI4IEhUVFBTX1BST1hZPWh0dHBzOi8vcHJveHkuZXhhbXBsZS5jb206MzEyOSBOT19QUk9YWT1sb2NhbGhvc3QsMTI3LjAuMC4xLGRvY2tlci1yZWdpc3RyeS5leGFtcGxlLmNvbSwuY29ycA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl show --property<span class="o">=</span>Environment docker
</span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=https://proxy.example.com:3129 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Rootless-%E6%A8%A1%E5%BC%8F' && 'hidden'"
      >
        <ol>
<li>
<p>为 <code>docker</code> 服务创建一个 systemd drop-in 目录：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBta2RpciAtcCB&#43;Ly5jb25maWcvc3lzdGVtZC91c2VyL2RvY2tlci5zZXJ2aWNlLmQ=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> mkdir -p ~/.config/systemd/user/docker.service.d
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>创建一个名为 <code>~/.config/systemd/user/docker.service.d/http-proxy.conf</code> 的文件，添加 <code>HTTP_PROXY</code> 环境变量：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI4Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://proxy.example.com:3128&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>如果您使用 HTTPS 代理服务器，请设置 <code>HTTPS_PROXY</code> 环境变量：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQU19QUk9YWT1odHRwczovL3Byb3h5LmV4YW1wbGUuY29tOjMxMjki', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTPS_PROXY=https://proxy.example.com:3129&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>可以设置多个环境变量；要同时设置非 HTTPS 和 HTTPS 代理：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI4IgpFbnZpcm9ubWVudD0iSFRUUFNfUFJPWFk9aHR0cHM6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI5Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://proxy.example.com:3128&#34;</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTPS_PROXY=https://proxy.example.com:3129&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>代理值中的特殊字符，如 <code>#?!()[]{}</code>，必须使用 <code>%%</code> 进行双重转义。例如：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9kb21haW4lJTVDdXNlcjpjb21wbGV4JSUyM3Bhc3NAcHJveHkuZXhhbXBsZS5jb206MzEyOC8i', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
    </div>
  </blockquote>

</li>
<li>
<p>如果您有需要直接联系的内部 Docker 注册表，不通过代理，可以通过 <code>NO_PROXY</code> 环境变量指定它们。</p>
<p><code>NO_PROXY</code> 变量指定一个包含逗号分隔值的字符串，用于指定应排除在代理之外的主机。您可以指定以下选项来排除主机：</p>
<ul>
<li>IP 地址前缀（<code>1.2.3.4</code>）</li>
<li>域名，或特殊 DNS 标签（<code>*</code>）</li>
<li>域名匹配该名称及其所有子域名。以 &quot;.&quot; 开头的域名仅匹配子域名。例如，给定域名 <code>foo.example.com</code> 和 <code>example.com</code>：
<ul>
<li><code>example.com</code> 匹配 <code>example.com</code> 和 <code>foo.example.com</code></li>
<li><code>.example.com</code> 仅匹配 <code>foo.example.com</code></li>
</ul>
</li>
<li>单个星号（<code>*</code>）表示不应进行代理</li>
<li>IP 地址前缀（<code>1.2.3.4:80</code>）和域名（<code>foo.example.com:80</code>）接受字面端口号</li>
</ul>
<p>示例：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'W1NlcnZpY2VdCkVudmlyb25tZW50PSJIVFRQX1BST1hZPWh0dHA6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI4IgpFbnZpcm9ubWVudD0iSFRUUFNfUFJPWFk9aHR0cHM6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI5IgpFbnZpcm9ubWVudD0iTk9fUFJPWFk9bG9jYWxob3N0LDEyNy4wLjAuMSxkb2NrZXItcmVnaXN0cnkuZXhhbXBsZS5jb20sLmNvcnAi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-systemd" data-lang="systemd"><span class="line"><span class="cl"><span class="k">[Service]</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTP_PROXY=http://proxy.example.com:3128&#34;</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;HTTPS_PROXY=https://proxy.example.com:3129&#34;</span>
</span></span><span class="line"><span class="cl"><span class="na">Environment</span><span class="o">=</span><span class="s">&#34;NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>刷新更改并重启 Docker</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzeXN0ZW1jdGwgLS11c2VyIGRhZW1vbi1yZWxvYWQKJCBzeXN0ZW1jdGwgLS11c2VyIHJlc3RhcnQgZG9ja2Vy', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> systemctl --user daemon-reload
</span></span><span class="line"><span class="cl"><span class="gp">$</span> systemctl --user restart docker
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>验证配置已加载且与您所做的更改匹配，例如：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzeXN0ZW1jdGwgLS11c2VyIHNob3cgLS1wcm9wZXJ0eT1FbnZpcm9ubWVudCBkb2NrZXIKCkVudmlyb25tZW50PUhUVFBfUFJPWFk9aHR0cDovL3Byb3h5LmV4YW1wbGUuY29tOjMxMjggSFRUUFNfUFJPWFk9aHR0cHM6Ly9wcm94eS5leGFtcGxlLmNvbTozMTI5IE5PX1BST1hZPWxvY2FsaG9zdCwxMjcuMC4wLjEsZG9ja2VyLXJlZ2lzdHJ5LmV4YW1wbGUuY29tLC5jb3Jw', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> systemctl --user show --property<span class="o">=</span>Environment docker
</span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=https://proxy.example.com:3129 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
  </div>
</div>

