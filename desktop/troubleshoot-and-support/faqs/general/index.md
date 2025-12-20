# Docker Desktop 通用常见问题解答

### 我可以在离线状态下使用 Docker Desktop 吗？

可以，您可以在离线状态下使用 Docker Desktop。但是，您将无法访问需要互联网连接的功能。此外，任何需要登录的功能在离线或使用隔离网络环境时都无法使用。这包括：

- [学习中心](/manuals/desktop/use-desktop/_index.md)中的资源
- 从 Docker Hub 拉取或推送镜像
- [镜像访问管理](/manuals/security/access-tokens.md)
- [静态漏洞扫描](/manuals/docker-hub/repos/manage/vulnerability-scanning.md)
- 在 Docker 仪表板中查看远程镜像
- 使用 [BuildKit](/manuals/build/buildkit/_index.md#getting-started) 时的 Docker Build。您可以通过禁用 BuildKit 来解决此问题。运行 `DOCKER_BUILDKIT=0 docker build .` 可禁用 BuildKit。
- [Kubernetes](/manuals/desktop/use-desktop/kubernetes.md)（首次启用 Kubernetes 时会下载镜像）
- 检查更新
- [应用内诊断](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-app)（包括[自诊断工具](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md#diagnose-from-the-app)）
- 发送使用情况统计信息
- 当 `networkMode` 设置为 `mirrored` 时

### 如何连接到远程 Docker Engine API？

要连接到远程 Engine API，您可能需要为 Docker 客户端和开发工具提供 Engine API 的位置。

Mac 和 Windows WSL 2 用户可以通过 Unix 套接字连接到 Docker Engine：`unix:///var/run/docker.sock`。

如果您使用的是 [Apache Maven](https://maven.apache.org/) 等应用程序，这些程序需要设置 `DOCKER_HOST` 和 `DOCKER_CERT_PATH` 环境变量，请指定这些变量以通过 Unix 套接字连接到 Docker 实例。

例如：

```console
$ export DOCKER_HOST=unix:///var/run/docker.sock
```

Docker Desktop Windows 用户可以通过**命名管道**连接到 Docker Engine：`npipe:////./pipe/docker_engine`，或通过此 URL 的 **TCP 套接字**：`tcp://localhost:2375`。

详细信息请参阅 [Docker Engine API](/reference/api/engine/_index.md)。

### 如何从容器连接到主机上的服务？

主机的 IP 地址是变化的，或者如果您没有网络访问权限，则可能没有 IP 地址。建议连接到特殊的 DNS 名称 `host.docker.internal`，该名称解析为主机使用的内部 IP 地址。

更多信息和示例，请参阅[如何从容器连接到主机上的服务](/manuals/desktop/features/networking.md#connect-a-container-to-a-service-on-the-host)。

### 我能否将 USB 设备直接传递给容器？

Docker Desktop 不支持直接传递 USB 设备。但是，您可以使用 USB over IP 将常用 USB 设备连接到 Docker Desktop 虚拟机，然后转发到容器。更多详情，请参阅[在 Docker Desktop 中使用 USB/IP](/manuals/desktop/features/usbip.md)。

### 如何验证 Docker Desktop 是否正在使用代理服务器？

要验证，请查看 `httpproxy.log` 中记录的最新事件。该文件位于 macOS 的 `~/Library/Containers/com.docker.docker/Data/log/host` 或 Windows 的 `%LOCALAPPDATA%/Docker/log/host/` 目录中。

以下是您可以看到的一些示例：

- Docker Desktop 使用应用级设置（代理模式：手动）作为代理：

   ```console
   host will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
   Linux will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
   ```

- Docker Desktop 使用系统级设置（代理模式：系统）作为代理：

   ```console
   host will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
   Linux will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
   ```

- Docker Desktop 未配置为使用代理服务器：

   ```console
   host will use proxy: disabled
   Linux will use proxy: disabled
   ```

- Docker Desktop 配置为使用应用级设置（代理模式：手动）并使用 PAC 文件：

   ```console
   using a proxy PAC file: http://127.0.0.1:8081/proxy.pac
   host will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
   Linux will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
   ```

- 使用配置的代理服务器进行连接请求：

   ```console
   CONNECT desktop.docker.com:443: host connecting via static system HTTPS proxy http://172.211.16.3:3128
   ```

### 我能否在不具备管理员权限的情况下运行 Docker Desktop？

Docker Desktop 仅在安装时需要管理员权限。安装完成后，运行它不需要管理员权限。但是，要让非管理员用户运行 Docker Desktop，必须使用特定的安装程序标志进行安装，并满足某些先决条件，这些条件因平台而异。








<div
  class="tabs"
  
    x-data="{ selected: 'Mac' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac'"
        
      >
        Mac
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows'"
        
      >
        Windows
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac' && 'hidden'"
      >
        <p>要在 Mac 上无需管理员权限运行 Docker Desktop，请通过命令行安装并传递 <code>—user=&lt;userid&gt;</code> 安装程序标志：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAvQXBwbGljYXRpb25zL0RvY2tlci5hcHAvQ29udGVudHMvTWFjT1MvaW5zdGFsbCAtLXVzZXI9PHVzZXJpZD4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> /Applications/Docker.app/Contents/MacOS/install --user<span class="o">=</span>&lt;userid&gt;
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>然后，您可以使用指定的用户 ID 登录到您的计算机并启动 Docker Desktop。</p>


  

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
      <p>在启动 Docker Desktop 之前，如果 <code>~/Library/Group Containers/group.com.docker/</code> 目录中已存在 <code>settings-store.json</code> 文件（对于 Docker Desktop 4.34 及更早版本为 <code>settings.json</code>），当您选择<strong>完成</strong>时，会出现一个<strong>完成 Docker Desktop 设置</strong>窗口，提示需要管理员权限。为避免这种情况，请确保在启动应用程序之前删除之前安装遗留下来的 <code>settings-store.json</code> 文件（对于 Docker Desktop 4.34 及更早版本为 <code>settings.json</code>）。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows' && 'hidden'"
      >
        

  

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
      <p>如果您使用的是 WSL 2 后端，请首先确保您满足 WSL 2 的
    
  
  <a class="link" href="https://docs.docker.com/desktop/features/wsl/best-practices/">最低版本要求</a>。否则，请先更新 WSL 2。</p>
    </div>
  </blockquote>

<p>要在 Windows 上无需管理员权限运行 Docker Desktop，请通过命令行安装并传递 <code>—always-run-service</code> 安装程序标志。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAiRG9ja2VyIERlc2t0b3AgSW5zdGFsbGVyLmV4ZSIgaW5zdGFsbCDigJRhbHdheXMtcnVuLXNlcnZpY2U=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="s2">&#34;Docker Desktop Installer.exe&#34;</span> install —always-run-service
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

