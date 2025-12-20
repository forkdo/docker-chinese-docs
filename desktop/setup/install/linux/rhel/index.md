# 在 RHEL 上安装 Docker Desktop

> **Docker Desktop 条款**
>
> 在大型企业（超过 250 名员工或年收入超过 1000 万美元）中商业使用 Docker Desktop 需要[付费订阅](https://www.docker.com/pricing/)。

本页包含有关如何在 Red Hat Enterprise Linux (RHEL) 发行版上安装、启动和升级 Docker Desktop 的信息。

## 先决条件

要成功安装 Docker Desktop，您必须：

- 满足[通用系统要求](_index.md#general-system-requirements)。
- 拥有 RHEL 8 或 RHEL 9 的 64 位版本。

- 如果 `pass` 未安装，或者无法安装，则必须启用 [CodeReady Linux Builder (CRB) 仓库](https://access.redhat.com/articles/4348511) 和 [Extra Packages for Enterprise Linux (EPEL)](https://docs.fedoraproject.org/en-US/epel/)。

   






<div
  class="tabs"
  
    
      x-data="{ selected: 'RHEL-9' }"
    
    @tab-select.window="$event.detail.group === 'os_version' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'RHEL-9' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os_version', name:
          'RHEL-9'})"
        
      >
        RHEL 9
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'RHEL-8' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os_version', name:
          'RHEL-8'})"
        
      >
        RHEL 8
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'RHEL-9' && 'hidden'"
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
        x-data="{ code: 'JCBzdWRvIHN1YnNjcmlwdGlvbi1tYW5hZ2VyIHJlcG9zIC0tZW5hYmxlIGNvZGVyZWFkeS1idWlsZGVyLWZvci1yaGVsLTktJChhcmNoKS1ycG1zCiQgc3VkbyBkbmYgaW5zdGFsbCBodHRwczovL2RsLmZlZG9yYXByb2plY3Qub3JnL3B1Yi9lcGVsL2VwZWwtcmVsZWFzZS1sYXRlc3QtOS5ub2FyY2gucnBtCiQgc3VkbyBkbmYgaW5zdGFsbCBwYXNz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo subscription-manager repos --enable codeready-builder-for-rhel-9-<span class="k">$(</span>arch<span class="k">)</span>-rpms
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install pass
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'RHEL-8' && 'hidden'"
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
        x-data="{ code: 'JCBzdWRvIHN1YnNjcmlwdGlvbi1tYW5hZ2VyIHJlcG9zIC0tZW5hYmxlIGNvZGVyZWFkeS1idWlsZGVyLWZvci1yaGVsLTgtJChhcmNoKS1ycG1zCiQgc3VkbyBkbmYgaW5zdGFsbCBodHRwczovL2RsLmZlZG9yYXByb2plY3Qub3JnL3B1Yi9lcGVsL2VwZWwtcmVsZWFzZS1sYXRlc3QtOC5ub2FyY2gucnBtCiQgc3VkbyBkbmYgaW5zdGFsbCBwYXNz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo subscription-manager repos --enable codeready-builder-for-rhel-8-<span class="k">$(</span>arch<span class="k">)</span>-rpms
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install pass
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


- 对于 GNOME 桌面环境，您必须安装 AppIndicator 和 KStatusNotifierItem [GNOME 扩展](https://extensions.gnome.org/extension/615/appindicator-support/)。您还必须启用 EPEL。

   






<div
  class="tabs"
  
    
      x-data="{ selected: 'RHEL-9' }"
    
    @tab-select.window="$event.detail.group === 'os_version' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'RHEL-9' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os_version', name:
          'RHEL-9'})"
        
      >
        RHEL 9
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'RHEL-8' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os_version', name:
          'RHEL-8'})"
        
      >
        RHEL 8
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'RHEL-9' && 'hidden'"
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
        x-data="{ code: 'JCAjIOWmguS4iuaJgOi/sOWQr&#43;eUqCBFUEVMCiQgc3VkbyBkbmYgaW5zdGFsbCBnbm9tZS1zaGVsbC1leHRlbnNpb24tYXBwaW5kaWNhdG9yCiQgc3VkbyBnbm9tZS1leHRlbnNpb25zIGVuYWJsZSBhcHBpbmRpY2F0b3JzdXBwb3J0QHJnY2pvbmFzLmdtYWlsLmNvbQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="c1"># 如上所述启用 EPEL</span>
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install gnome-shell-extension-appindicator
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo gnome-extensions <span class="nb">enable</span> appindicatorsupport@rgcjonas.gmail.com
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'RHEL-8' && 'hidden'"
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
        x-data="{ code: 'JCAjIOWmguS4iuaJgOi/sOWQr&#43;eUqCBFUEVMCiQgc3VkbyBkbmYgaW5zdGFsbCBnbm9tZS1zaGVsbC1leHRlbnNpb24tYXBwaW5kaWNhdG9yCiQgc3VkbyBkbmYgaW5zdGFsbCBnbm9tZS1zaGVsbC1leHRlbnNpb24tZGVza3RvcC1pY29ucwokIHN1ZG8gZ25vbWUtc2hlbGwtZXh0ZW5zaW9uLXRvb2wgLWUgYXBwaW5kaWNhdG9yc3VwcG9ydEByZ2Nqb25hcy5nbWFpbC5jb20=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="c1"># 如上所述启用 EPEL</span>
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install gnome-shell-extension-appindicator
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install gnome-shell-extension-desktop-icons
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo gnome-shell-extension-tool -e appindicatorsupport@rgcjonas.gmail.com
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


- 如果您不使用 GNOME，则必须安装 `gnome-terminal` 以启用从 Docker Desktop 访问终端：

   ```console
   $ sudo dnf install gnome-terminal
   ```

## 安装 Docker Desktop

要在 RHEL 上安装 Docker Desktop：

1. 按如下方式设置 Docker 的软件包仓库：

   ```console
   $ sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   ```

2. 下载最新的 [RPM 软件包](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64-rhel.rpm?utm_source=docker&utm_medium=webreferral&utm_campaign=docs-driven-download-linux-amd64)。

3. 使用 dnf 安装软件包，如下所示：

   ```console
   $ sudo dnf install ./docker-desktop-x86_64-rhel.rpm
   ```

RPM 软件包包含一个安装后脚本，该脚本会自动完成其他设置步骤。

安装后脚本：

- 在 Docker Desktop 二进制文件上设置 capabilities，以映射特权端口和设置资源限制。
- 为 Kubernetes 添加一个 DNS 名称到 `/etc/hosts`。
- 创建一个从 `/usr/local/bin/com.docker.cli` 到 `/usr/bin/docker` 的符号链接。
  这是因为经典 Docker CLI 安装在 `/usr/bin/docker`。Docker Desktop 安装程序还会安装一个包含云集成功能的 Docker CLI 二进制文件，它本质上是 Compose CLI 的包装器，位于 `/usr/local/bin/com.docker.cli`。该符号链接确保包装器可以访问经典 Docker CLI。
- 创建一个从 `/usr/libexec/qemu-kvm` 到 `/usr/local/bin/qemu-system-x86_64` 的符号链接。

## 启动 Docker Desktop



要启动 Docker Desktop for Linux：

1.  在您的 Gnome/KDE 桌面中找到 Docker Desktop 应用程序。
2.  选择 **Docker Desktop** 以启动 Docker。

    此时将显示 Docker 订阅服务协议。

3.  选择 **接受** 继续。接受条款后，Docker Desktop 将会启动。

    请注意，如果您不同意该条款，Docker Desktop 将无法运行。您可以通过稍后打开 Docker Desktop 来选择接受条款。

    更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议您同时阅读 [常见问题解答](https://www/docker.com/pricing/faq)。

或者，打开终端并运行：

```console
$ systemctl --user start docker-desktop
```

当 Docker Desktop 启动时，它会创建一个专用的 [上下文](/engine/context/working-with-contexts)，供 Docker CLI 作为目标使用，并将其设置为当前正在使用的上下文。这样做是为了避免与可能在 Linux 主机上运行并使用默认上下文的本地 Docker Engine 发生冲突。关闭时，Docker Desktop 会将当前上下文重置为之前的上下文。

Docker Desktop 安装程序会更新主机上的 Docker Compose 和 Docker CLI 二进制文件。它会安装 Docker Compose V2，并允许用户通过设置面板选择将其链接为 docker-compose。Docker Desktop 会在 `/usr/local/bin/com.docker.cli` 安装包含云集成功能的新版 Docker CLI 二进制文件，并在 `/usr/local/bin` 创建指向经典 Docker CLI 的符号链接。

成功安装 Docker Desktop 后，您可以通过运行以下命令来检查这些二进制文件的版本：

```console
$ docker compose version
Docker Compose version v2.39.4

$ docker --version
Docker version 28.4.0, build d8eb465

$ docker version
Client:
 Version:           28.4.0
 API version:       1.51
 Go version:        go1.24.7
<...>
```

要让 Docker Desktop 在登录时自动启动，请从 Docker 菜单中选择 **设置** > **常规** > **登录计算机时启动 Docker Desktop**。

或者，打开终端并运行：

```console
$ systemctl --user enable docker-desktop
```

要停止 Docker Desktop，请选择 Docker 菜单图标以打开 Docker 菜单，然后选择 **退出 Docker Desktop**。

或者，打开终端并运行：

```console
$ systemctl --user stop docker-desktop
```

> [!TIP]
>
> 要将 Red Hat 订阅数据附加到容器，请参阅 [Red Hat 验证的解决方案](https://access.redhat.com/solutions/5870841)。
>
> 例如：
> ```console
> $ docker run --rm -it -v "/etc/pki/entitlement:/etc/pki/entitlement" -v "/etc/rhsm:/etc/rhsm-host" -v "/etc/yum.repos.d/redhat.repo:/etc/yum.repos.d/redhat.repo" registry.access.redhat.com/ubi9
> ```

## 升级 Docker Desktop

一旦发布了 Docker Desktop 的新版本，Docker UI 会显示通知。
每次要升级 Docker Desktop 时，您需要先卸载旧版本，然后下载新软件包。运行：

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-<arch>-rhel.rpm
```

## 后续步骤

- 查看 [Docker 的订阅](https://www.docker.com/pricing/)，了解 Docker 可以为您提供什么。
- 浏览 [Docker 研讨会](/get-started/workshop/_index.md)，了解如何构建镜像并将其作为容器化应用程序运行。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、解决方法、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供了常见问题的解答。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 版本相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和恢复 Docker 相关数据的说明。
