# 无 root 模式

无 root 模式允许您以非 root 用户身份运行 Docker 守护进程和容器，从而减轻守护进程和容器运行时中潜在漏洞的影响。

只要满足[先决条件](#先决条件)，无 root 模式甚至在安装 Docker 守护进程时也无需 root 权限。

## 工作原理

无 root 模式在用户命名空间内执行 Docker 守护进程和容器。这类似于 [`userns-remap` 模式](../userns-remap.md)，不同之处在于 `userns-remap` 模式下，守护进程本身是以 root 权限运行的，而在无 root 模式下，守护进程和容器都是在没有 root 权限的情况下运行的。

无 root 模式不使用带有 `SETUID` 位或文件能力的二进制文件，除了 `newuidmap` 和 `newgidmap`，它们是允许在用户命名空间中使用多个 UID/GID 所必需的。

## 先决条件

- 您必须在主机上安装 `newuidmap` 和 `newgidmap`。这些命令在大多数发行版中由 `uidmap` 软件包提供。

- `/etc/subuid` 和 `/etc/subgid` 应包含至少 65,536 个从属 UID/GID 给该用户。在以下示例中，用户 `testuser` 拥有 65,536 个从属 UID/GID (231072-296607)。

```console
$ id -u
1001
$ whoami
testuser
$ grep ^$(whoami): /etc/subuid
testuser:231072:65536
$ grep ^$(whoami): /etc/subgid
testuser:231072:65536
```

`dockerd-rootless-setuptool.sh install` 脚本（见下文）在先决条件不满足时会自动显示帮助信息。

## 安装

> [!NOTE]
>
> 如果系统级的 Docker 守护进程已经在运行，请考虑禁用它：
> ```console
> $ sudo systemctl disable --now docker.service docker.socket
> $ sudo rm /var/run/docker.sock
> ```
> 如果您选择不关闭 `docker` 服务和套接字，则需要在下一节中使用 `--force` 参数。目前没有已知问题，但在您关闭并禁用之前，您仍然在运行有 root 权限的 Docker。








<div
  class="tabs"
  
    x-data="{ selected: '%E4%BD%BF%E7%94%A8%E8%BD%AF%E4%BB%B6%E5%8C%85-RPM/DEB' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BD%BF%E7%94%A8%E8%BD%AF%E4%BB%B6%E5%8C%85-RPM/DEB' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BD%BF%E7%94%A8%E8%BD%AF%E4%BB%B6%E5%8C%85-RPM/DEB'"
        
      >
        使用软件包 (RPM/DEB)
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%B8%8D%E4%BD%BF%E7%94%A8%E8%BD%AF%E4%BB%B6%E5%8C%85' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%B8%8D%E4%BD%BF%E7%94%A8%E8%BD%AF%E4%BB%B6%E5%8C%85'"
        
      >
        不使用软件包
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BD%BF%E7%94%A8%E8%BD%AF%E4%BB%B6%E5%8C%85-RPM/DEB' && 'hidden'"
      >
        <p>如果您使用 
  <a class="link" href="/engine/install">RPM/DEB 软件包</a> 安装了 Docker 20.10 或更高版本，您应该在 <code>/usr/bin</code> 中有 <code>dockerd-rootless-setuptool.sh</code>。</p>
<p>以非 root 用户身份运行 <code>dockerd-rootless-setuptool.sh install</code> 来设置守护进程：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXJkLXJvb3RsZXNzLXNldHVwdG9vbC5zaCBpbnN0YWxsCltJTkZPXSBDcmVhdGluZyAvaG9tZS90ZXN0dXNlci8uY29uZmlnL3N5c3RlbWQvdXNlci9kb2NrZXIuc2VydmljZQouLi4KW0lORk9dIEluc3RhbGxlZCBkb2NrZXIuc2VydmljZSBzdWNjZXNzZnVsbHkuCltJTkZPXSBUbyBjb250cm9sIGRvY2tlci5zZXJ2aWNlLCBydW46IGBzeXN0ZW1jdGwgLS11c2VyIChzdGFydHxzdG9wfHJlc3RhcnQpIGRvY2tlci5zZXJ2aWNlYApbSU5GT10gVG8gcnVuIGRvY2tlci5zZXJ2aWNlIG9uIHN5c3RlbSBzdGFydHVwLCBydW46IGBzdWRvIGxvZ2luY3RsIGVuYWJsZS1saW5nZXIgdGVzdHVzZXJgCgpbSU5GT10gQ3JlYXRpbmcgQ0xJIGNvbnRleHQgInJvb3RsZXNzIgpTdWNjZXNzZnVsbHkgY3JlYXRlZCBjb250ZXh0ICJyb290bGVzcyIKW0lORk9dIFVzaW5nIENMSSBjb250ZXh0ICJyb290bGVzcyIKQ3VycmVudCBjb250ZXh0IGlzIG5vdyAicm9vdGxlc3MiCgpbSU5GT10gTWFrZSBzdXJlIHRoZSBmb2xsb3dpbmcgZW52aXJvbm1lbnQgdmFyaWFibGUocykgYXJlIHNldCAob3IgYWRkIHRoZW0gdG8gfi8uYmFzaHJjKToKZXhwb3J0IFBBVEg9L3Vzci9iaW46JFBBVEgKCltJTkZPXSBTb21lIGFwcGxpY2F0aW9ucyBtYXkgcmVxdWlyZSB0aGUgZm9sbG93aW5nIGVudmlyb25tZW50IHZhcmlhYmxlIHRvbzoKZXhwb3J0IERPQ0tFUl9IT1NUPXVuaXg6Ly8vcnVuL3VzZXIvMTAwMC9kb2NrZXIuc29jaw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> dockerd-rootless-setuptool.sh install
</span></span><span class="line"><span class="cl"><span class="go">[INFO] Creating /home/testuser/.config/systemd/user/docker.service
</span></span></span><span class="line"><span class="cl"><span class="go">...
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] Installed docker.service successfully.
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">[INFO] Creating CLI context &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">Successfully created context &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] Using CLI context &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">Current context is now &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">[INFO] Make sure the following environment variable(s) are set (or add them to ~/.bashrc):
</span></span></span><span class="line"><span class="cl"><span class="go">export PATH=/usr/bin:$PATH
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">[INFO] Some applications may require the following environment variable too:
</span></span></span><span class="line"><span class="cl"><span class="go">export DOCKER_HOST=unix:///run/user/1000/docker.sock
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>如果 <code>dockerd-rootless-setuptool.sh</code> 不存在，您可能需要手动安装 <code>docker-ce-rootless-extras</code> 软件包，例如：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIGFwdC1nZXQgaW5zdGFsbCAteSBkb2NrZXItY2Utcm9vdGxlc3MtZXh0cmFz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo apt-get install -y docker-ce-rootless-extras
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%B8%8D%E4%BD%BF%E7%94%A8%E8%BD%AF%E4%BB%B6%E5%8C%85' && 'hidden'"
      >
        <p>如果您没有权限运行像 <code>apt-get</code> 和 <code>dnf</code> 这样的软件包管理器，请考虑使用 <a class="link" href="https://get.docker.com/rootless" rel="noopener">https://get.docker.com/rootless</a> 提供的安装脚本。
由于 <code>s390x</code> 没有可用的静态软件包，因此不支持 <code>s390x</code>。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBjdXJsIC1mc1NMIGh0dHBzOi8vZ2V0LmRvY2tlci5jb20vcm9vdGxlc3MgfCBzaAouLi4KW0lORk9dIENyZWF0aW5nIC9ob21lL3Rlc3R1c2VyLy5jb25maWcvc3lzdGVtZC91c2VyL2RvY2tlci5zZXJ2aWNlCi4uLgpbSU5GT10gSW5zdGFsbGVkIGRvY2tlci5zZXJ2aWNlIHN1Y2Nlc3NmdWxseS4KW0lORk9dIFRvIGNvbnRyb2wgZG9ja2VyLnNlcnZpY2UsIHJ1bjogYHN5c3RlbWN0bCAtLXVzZXIgKHN0YXJ0fHN0b3B8cmVzdGFydCkgZG9ja2VyLnNlcnZpY2VgCltJTkZPXSBUbyBydW4gZG9ja2VyLnNlcnZpY2Ugb24gc3lzdGVtIHN0YXJ0dXAsIHJ1bjogYHN1ZG8gbG9naW5jdGwgZW5hYmxlLWxpbmdlciB0ZXN0dXNlcmAKCltJTkZPXSBDcmVhdGluZyBDTEkgY29udGV4dCAicm9vdGxlc3MiClN1Y2Nlc3NmdWxseSBjcmVhdGVkIGNvbnRleHQgInJvb3RsZXNzIgpbSU5GT10gVXNpbmcgQ0xJIGNvbnRleHQgInJvb3RsZXNzIgpDdXJyZW50IGNvbnRleHQgaXMgbm93ICJyb290bGVzcyIKCltJTkZPXSBNYWtlIHN1cmUgdGhlIGZvbGxvd2luZyBlbnZpcm9ubWVudCB2YXJpYWJsZShzKSBhcmUgc2V0IChvciBhZGQgdGhlbSB0byB&#43;Ly5iYXNocmMpOgpleHBvcnQgUEFUSD0vaG9tZS90ZXN0dXNlci9iaW46JFBBVEgKCltJTkZPXSBTb21lIGFwcGxpY2F0aW9ucyBtYXkgcmVxdWlyZSB0aGUgZm9sbG93aW5nIGVudmlyb25tZW50IHZhcmlhYmxlIHRvbzoKZXhwb3J0IERPQ0tFUl9IT1NUPXVuaXg6Ly8vcnVuL3VzZXIvMTAwMC9kb2NrZXIuc29jaw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> curl -fsSL https://get.docker.com/rootless <span class="p">|</span> sh
</span></span><span class="line"><span class="cl"><span class="go">...
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] Creating /home/testuser/.config/systemd/user/docker.service
</span></span></span><span class="line"><span class="cl"><span class="go">...
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] Installed docker.service successfully.
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">[INFO] Creating CLI context &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">Successfully created context &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">[INFO] Using CLI context &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">Current context is now &#34;rootless&#34;
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">[INFO] Make sure the following environment variable(s) are set (or add them to ~/.bashrc):
</span></span></span><span class="line"><span class="cl"><span class="go">export PATH=/home/testuser/bin:$PATH
</span></span></span><span class="line"><span class="cl"><span class="go"></span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="go">[INFO] Some applications may require the following environment variable too:
</span></span></span><span class="line"><span class="cl"><span class="go">export DOCKER_HOST=unix:///run/user/1000/docker.sock
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>二进制文件将被安装在 <code>~/bin</code>。</p>

      </div>
    
  </div>
</div>


运行 `docker info` 来确认 `docker` 客户端正在连接到无 root 守护进程：
```console
$ docker info
Client: Docker Engine - Community
 Version:    28.3.3
 Context:    rootless
...
Server:
...
 Security Options:
  seccomp
   Profile: builtin
  rootless
  cgroupns
...
```

如果您遇到错误，请参阅[故障排除](./troubleshoot.md)。

- [使用技巧](/engine/security/rootless/tips/)

- [问题排查](/engine/security/rootless/troubleshoot/)

