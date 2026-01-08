# Docker 守护进程故障排除

本页面介绍在遇到问题时，如何对守护进程进行故障排除和调试。

您可以开启守护进程的调试功能，以了解守护进程的运行时活动并辅助故障排除。如果守护进程无响应，您还可以通过向 Docker 守护进程发送 `SIGUSR` 信号，[强制记录完整的堆栈跟踪](logs.md#force-a-stack-trace-to-be-logged)（包括所有线程）到守护进程日志中。

## 守护进程 (Daemon)

### 无法连接到 Docker 守护进程

```text
Cannot connect to the Docker daemon. Is 'docker daemon' running on this host?
```

此错误可能表示：

- Docker 守护进程未在您的系统上运行。启动守护进程并尝试再次运行命令。
- 您的 Docker 客户端正尝试连接到另一台主机上的 Docker 守护进程，且该主机不可达。

### 检查 Docker 是否正在运行

检查 Docker 是否正在运行的、与操作系统无关的方法是使用 `docker info` 命令询问 Docker。

您也可以使用操作系统实用程序，例如 `sudo systemctl is-active docker`、`sudo status docker` 或 `sudo service docker status`，或者在 Windows 实用程序中检查服务状态。

最后，您可以使用 `ps` 或 `top` 等命令在进程列表中检查 `dockerd` 进程。

#### 检查客户端连接到的主机

要查看客户端连接到的主机，请检查环境变量 `DOCKER_HOST` 的值。

```console
$ env | grep DOCKER_HOST
```

如果此命令返回一个值，则 Docker 客户端设置为连接到该主机上运行的 Docker 守护进程。如果未设置，则 Docker 客户端设置为连接到本地主机上运行的 Docker 守护进程。如果设置有误，请使用以下命令取消设置：

```console
$ unset DOCKER_HOST
```

您可能需要编辑 `~/.bashrc` 或 `~/.profile` 等文件中的环境设置，以防止错误地设置 `DOCKER_HOST` 变量。

如果 `DOCKER_HOST` 是按预期设置的，请验证 Docker 守护进程是否正在远程主机上运行，以及防火墙或网络中断是否阻止了您的连接。

### 排除 `daemon.json` 和启动脚本之间的冲突

如果您使用 `daemon.json` 文件，同时手动或使用启动脚本向 `dockerd` 命令传递选项，并且这些选项发生冲突，Docker 将无法启动并显示类似以下错误：

```text
unable to configure the Docker daemon with file /etc/docker/daemon.json:
the following directives are specified both as a flag and in the configuration
file: hosts: (from flag: [unix:///var/run/docker.sock], from file: [tcp://127.0.0.1:2376])
```

如果您看到类似于此的错误，并且您正在使用标志手动启动守护进程，则可能需要调整您的标志或 `daemon.json` 以消除冲突。

> [!NOTE]
>
> 如果您看到关于 `hosts` 的此特定错误消息，请继续阅读[下一节](#configure-the-daemon-host-with-systemd)以获取解决方法。

如果您使用操作系统的 init 脚本启动 Docker，则可能需要以特定于操作系统的方式覆盖这些脚本中的默认值。

#### 使用 systemd 配置守护进程主机

一个难以排除的配置冲突的显著例子是，当您想要指定与默认值不同的守护进程地址时。Docker 默认监听套接字。在使用 `systemd` 的 Debian 和 Ubuntu 系统上，这意味着启动 `dockerd` 时始终使用主机标志 `-H`。如果您在 `daemon.json` 中指定 `hosts` 条目，这将导致配置冲突，并导致 Docker 守护进程启动失败。

要解决此问题，请创建一个新文件 `/etc/systemd/system/docker.service.d/docker.conf`，包含以下内容，以移除默认启动守护进程时使用的 `-H` 参数。

```systemd
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd
```

在其他情况下，您可能需要使用 Docker 配置 `systemd`，例如[配置 HTTP 或 HTTPS 代理](./proxy.md)。

> [!NOTE]
>
> 如果您覆盖此选项而未在 `daemon.json` 中指定 `hosts` 条目，或在手动启动 Docker 时未指定 `-H` 标志，Docker 将无法启动。

在尝试启动 Docker 之前运行 `sudo systemctl daemon-reload`。如果 Docker 成功启动，它现在将监听 `daemon.json` 中 `hosts` 键指定的 IP 地址，而不是套接字。

> [!IMPORTANT]
>
> 在 Windows 版 Docker Desktop 或 Mac 版 Docker Desktop 中，不支持在 `daemon.json` 中设置 `hosts`。

### 内存不足问题

如果您的容器尝试使用的内存超过系统可用内存，您可能会遇到内存不足 (OOM) 异常，容器或 Docker 守护进程可能会被内核 OOM 杀手停止。为防止这种情况发生，请确保您的应用程序在具有足够内存的主机上运行，并参阅[了解内存不足的风险](../containers/resource_constraints.md#understand-the-risks-of-running-out-of-memory)。

### 内核兼容性

如果您的内核版本早于 3.10，或者缺少内核模块，Docker 将无法正确运行。要检查内核兼容性，您可以下载并运行 [`check-config.sh`](https://raw.githubusercontent.com/docker/docker/master/contrib/check-config.sh) 脚本。

```console
$ curl https://raw.githubusercontent.com/docker/docker/master/contrib/check-config.sh > check-config.sh

$ bash ./check-config.sh
```

该脚本仅在 Linux 上有效。

### 内核 cgroup 交换限制能力

在 Ubuntu 或 Debian 主机上，处理镜像时可能会看到类似以下的消息：

```text
WARNING: Your kernel does not support swap limit capabilities. Limitation discarded.
```

如果您不需要这些能力，可以忽略此警告。

您可以通过以下说明在 Ubuntu 或 Debian 上开启这些能力。内存和交换记账会产生约总可用内存 1% 的开销，以及整体性能下降 10%，即使 Docker 未运行时也是如此。

1. 以具有 `sudo` 权限的用户身份登录到 Ubuntu 或 Debian 主机。
2. 编辑 `/etc/default/grub` 文件。添加或编辑 `GRUB_CMDLINE_LINUX` 行以添加以下两个键值对：

   ```text
   GRUB_CMDLINE_LINUX="cgroup_enable=memory swapaccount=1"
   ```

   保存并关闭文件。
3. 更新 GRUB 引导加载程序。

   ```console
   $ sudo update-grub
   ```

   如果您的 GRUB 配置文件语法不正确，会发生错误。在这种情况下，重复步骤 2 和 3。

   更改将在您重新启动系统后生效。

## 网络 (Networking)

### IP 转发问题

如果您使用 systemd 版本 219 或更高版本通过 `systemd-network` 手动配置网络，Docker 容器可能无法访问您的网络。从 systemd 版本 220 开始，给定网络的转发设置 (`net.ipv4.conf.<interface>.forwarding`) 默认为关闭。此设置会阻止 IP 转发。它还与 Docker 在容器内启用 `net.ipv4.conf.all.forwarding` 设置的行为冲突。

要在 RHEL、CentOS 或 Fedora 上解决此问题，请在 Docker 主机上编辑 `/usr/lib/systemd/network/` 中的 `<interface>.network` 文件，例如 `/usr/lib/systemd/network/80-container-host0.network`。

在 `[Network]` 部分中添加以下块。

```systemd
[Network]
...
IPForward=kernel
# 或
IPForward=true
```

此配置允许按预期从容器进行 IP 转发。

### DNS 解析器问题

```console
DNS resolver found in resolv.conf and containers can't use it
```

Linux 桌面环境通常运行一个网络管理器程序，该程序使用 `dnsmasq` 通过将其添加到 `/etc/resolv.conf` 来缓存 DNS 请求。`dnsmasq` 实例在环回地址（如 `127.0.0.1` 或 `127.0.1.1`）上运行。它加速 DNS 查找并提供 DHCP 服务。此类配置在 Docker 容器内不起作用。Docker 容器使用自己的网络命名空间，并将环回地址（如 `127.0.0.1`）解析为其自身，并且不太可能在其自己的环回地址上运行 DNS 服务器。

如果 Docker 检测到 `/etc/resolv.conf` 中引用的 DNS 服务器不是功能齐全的 DNS 服务器，则会发生以下警告：

```text
WARNING: Local (127.0.0.1) DNS resolver found in resolv.conf and containers
can't use it. Using default external servers : [8.8.8.8 8.8.4.4]
```

如果您看到此警告，首先检查是否使用了 `dnsmasq`：

```console
$ ps aux | grep dnsmasq
```

如果您的容器需要解析网络内部的主机，则公共名称服务器是不够的。您有两种选择：

- 为 Docker 指定要使用的 DNS 服务器。
- 关闭 `dnsmasq`。

  关闭 `dnsmasq` 会将实际 DNS 名称服务器的 IP 地址添加到 `/etc/resolv.conf`，但您会失去 `dnsmasq` 的优势。

您只需要使用其中一种方法。

### 为 Docker 指定 DNS 服务器

配置文件的默认位置是 `/etc/docker/daemon.json`。您可以使用守护进程标志 `--config-file` 更改配置文件的位置。以下说明假设配置文件的位置是 `/etc/docker/daemon.json`。

1. 创建或编辑 Docker 守护进程配置文件，默认为 `/etc/docker/daemon.json` 文件，该文件控制 Docker 守护进程配置。

   ```console
   $ sudo nano /etc/docker/daemon.json
   ```

2. 添加一个 `dns` 键，其值为一个或多个 DNS 服务器 IP 地址。

   ```json
   {
     "dns": ["8.8.8.8", "8.8.4.4"]
   }
   ```

   如果文件已有内容，您只需添加或编辑 `dns` 行。如果您的内部 DNS 服务器无法解析公共 IP 地址，请至少包含一个可以解析的 DNS 服务器。这样做可以让您连接到 Docker Hub，并让您的容器解析互联网域名。

   保存并关闭文件。

3. 重启 Docker 守护进程。

   ```console
   $ sudo service docker restart
   ```

4. 通过尝试拉取镜像来验证 Docker 是否可以解析外部 IP 地址：

   ```console
   $ docker pull hello-world
   ```

5. 如有必要，通过 ping 内部主机名来验证 Docker 容器是否可以解析它。

   ```console
   $ docker run --rm -it alpine ping -c4 <my_internal_host>

   PING google.com (192.168.1.2): 56 data bytes
   64 bytes from 192.168.1.2: seq=0 ttl=41 time=7.597 ms
   64 bytes from 192.168.1.2: seq=1 ttl=41 time=7.635 ms
   64 bytes from 192.168.1.2: seq=2 ttl=41 time=7.660 ms
   64 bytes from 192.168.1.2: seq=3 ttl=41 time=7.677 ms
   ```

### 关闭 `dnsmasq`








<div
  class="tabs"
  
    x-data="{ selected: 'Ubuntu' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Ubuntu' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Ubuntu'"
        
      >
        Ubuntu
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'RHEL-CentOS-or-Fedora' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'RHEL-CentOS-or-Fedora'"
        
      >
        RHEL, CentOS, or Fedora
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Ubuntu' && 'hidden'"
      >
        <p>如果您不想更改 Docker 守护进程的配置来使用特定 IP 地址，请按照以下说明在 NetworkManager 中关闭 <code>dnsmasq</code>。</p>
<ol>
<li>
<p>编辑 <code>/etc/NetworkManager/NetworkManager.conf</code> 文件。</p>
</li>
<li>
<p>通过在行首添加 <code>#</code> 字符来注释掉 <code>dns=dnsmasq</code> 行。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBkbnM9ZG5zbWFzcQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl"># dns=dnsmasq</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>保存并关闭文件。</p>
</li>
<li>
<p>重启 NetworkManager 和 Docker。或者，您可以重新启动系统。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCByZXN0YXJ0IG5ldHdvcmstbWFuYWdlcgokIHN1ZG8gc3lzdGVtY3RsIHJlc3RhcnQgZG9ja2Vy', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl restart network-manager
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl restart docker
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'RHEL-CentOS-or-Fedora' && 'hidden'"
      >
        <p>要在 RHEL、CentOS 或 Fedora 上关闭 <code>dnsmasq</code>：</p>
<ol>
<li>
<p>关闭 <code>dnsmasq</code> 服务：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCBzdG9wIGRuc21hc3EKJCBzdWRvIHN5c3RlbWN0bCBkaXNhYmxlIGRuc21hc3E=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl stop dnsmasq
</span></span><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl disable dnsmasq
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>使用 <a class="link" href="https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/configuring_and_managing_networking/configuring-the-order-of-dns-servers_configuring-and-managing-networking" rel="noopener">Red Hat 文档</a> 手动配置 DNS 服务器。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


### Docker 网络消失

如果 Docker 网络（例如 `docker0` 网桥或自定义网络）随机消失或以其他方式显示为工作不正常，可能是因为另一个服务正在干扰或修改 Docker 接口。已知管理主机上网络接口的工具有时也会不适当地修改 Docker 接口。

请参阅以下部分，了解如何根据主机上存在的网络管理工具配置您的网络管理器以将 Docker 接口设置为非托管状态：

- 如果安装了 `netscript`，请考虑[卸载它](#uninstall-netscript)
- 配置网络管理器以[将 Docker 接口视为非托管](#un-manage-docker-interfaces)
- 如果您使用 Netplan，您可能需要[应用自定义 Netplan 配置](#prevent-netplan-from-overriding-network-configuration)

#### 卸载 `netscript`

如果您的系统上安装了 `netscript`，您可以通过卸载它来解决此问题。例如，在基于 Debian 的系统上：

```console
$ sudo apt-get remove netscript-2.4
```

#### 将 Docker 接口设为非托管

在某些情况下，网络管理器默认会尝试管理 Docker 接口。您可以通过编辑系统的网络配置设置，尝试明确将 Docker 网络标记为非托管。








<div
  class="tabs"
  
    x-data="{ selected: 'NetworkManager' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'NetworkManager' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'NetworkManager'"
        
      >
        NetworkManager
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'systemd-networkd' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'systemd-networkd'"
        
      >
        systemd-networkd
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'NetworkManager' && 'hidden'"
      >
        <p>如果您使用的是 <code>NetworkManager</code>，请在 <code>/etc/network/interfaces</code> 下编辑您的系统网络配置。</p>
<ol>
<li>
<p>在 <code>/etc/network/interfaces.d/20-docker0</code> 创建一个包含以下内容的文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aWZhY2UgZG9ja2VyMCBpbmV0IG1hbnVhbA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-text" data-lang="text"><span class="line"><span class="cl">iface docker0 inet manual</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>请注意，此示例配置仅将默认的 <code>docker0</code> 网桥“非托管”，不包括自定义网络。</p>
</li>
<li>
<p>重启 <code>NetworkManager</code> 以使配置更改生效。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzeXN0ZW1jdGwgcmVzdGFydCBOZXR3b3JrTWFuYWdlcg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> systemctl restart NetworkManager
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>验证 <code>docker0</code> 接口是否处于 <code>unmanaged</code> 状态。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBubWNsaSBkZXZpY2U=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> nmcli device
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'systemd-networkd' && 'hidden'"
      >
        <p>如果您在使用 <code>systemd-networkd</code> 作为网络守护进程的系统上运行 Docker，请通过在 <code>/etc/systemd/network</code> 下创建配置文件将 Docker 接口配置为非托管：</p>
<ol>
<li>
<p>创建 <code>/etc/systemd/network/docker.network</code>，内容如下：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyDnoa7kv50gRG9ja2VyIOaOpeWPo&#43;aYr&#43;mdnuaJmOeuoeeahAoKW01hdGNoXQpOYW1lPWRvY2tlcjAgYnItKiB2ZXRoKgoKW0xpbmtdClVubWFuYWdlZD15ZXM=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-ini" data-lang="ini"><span class="line"><span class="cl"><span class="c1"># 确保 Docker 接口是非托管的</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">[Match]</span>
</span></span><span class="line"><span class="cl"><span class="na">Name</span><span class="o">=</span><span class="s">docker0 br-* veth*</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">[Link]</span>
</span></span><span class="line"><span class="cl"><span class="na">Unmanaged</span><span class="o">=</span><span class="s">yes</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>重新加载配置。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCByZXN0YXJ0IHN5c3RlbWQtbmV0d29ya2Q=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl restart systemd-networkd
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>重启 Docker 守护进程。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIHN5c3RlbWN0bCByZXN0YXJ0IGRvY2tlcg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo systemctl restart docker
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>验证 Docker 接口是否处于 <code>unmanaged</code> 状态。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBuZXR3b3JrY3Rs', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> networkctl
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
  </div>
</div>


### 防止 Netplan 覆盖网络配置

在使用 [Netplan](https://netplan.io/) 通过 [`cloud-init`](https://cloudinit.readthedocs.io/en/latest/index.html) 的系统上，您可能需要应用自定义配置以防止 `netplan` 覆盖网络管理器配置：

1. 按照[将 Docker 接口设为非托管](#un-manage-docker-interfaces)中的步骤创建网络管理器配置。
2. 在 `/etc/netplan/50-cloud-init.yml` 下创建一个 `netplan` 配置文件。

   以下示例配置文件是一个起点。请根据您想要非托管的接口进行调整。不正确的配置可能导致网络连接问题。

   ```yaml {title="/etc/netplan/50-cloud-init.yml"}
   network:
     ethernets:
       all:
         dhcp4: true
         dhcp6: true
         match:
           # 编辑此过滤器以匹配对您的系统有意义的任何内容
           name: en*
     renderer: networkd
     version: 2
   ```

3. 应用新的 Netplan 配置。

   ```console
   $ sudo netplan apply
   ```

4. 重启 Docker 守护进程：

   ```console
   $ sudo systemctl restart docker
   ```

5. 验证 Docker 接口是否处于 `unmanaged` 状态。

   ```console
   $ networkctl
   ```

## 卷 (Volumes)

### 无法删除文件系统

```text
Error: Unable to remove filesystem
```

一些基于容器的实用程序，例如 [Google cAdvisor](https://github.com/google/cadvisor)，会将 Docker 系统目录（如 `/var/lib/docker/`）挂载到容器中。例如，`cadvisor` 的文档指示您按如下方式运行 `cadvisor` 容器：

```console
$ sudo docker run \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  --name=cadvisor \
  google/cadvisor:latest
```

当您绑定挂载 `/var/lib/docker/` 时，这实际上会将所有其他正在运行的容器的所有资源作为文件系统挂载到挂载了 `/var/lib/docker/` 的容器内。当您尝试删除这些容器中的任何一个时，删除尝试可能会失败，并显示类似以下的错误：

```text
Error: Unable to remove filesystem for
74bef250361c7817bee19349c93139621b272bc8f654ae112dd4eb9652af9515:
remove /var/lib/docker/containers/74bef250361c7817bee19349c93139621b272bc8f654ae112dd4eb9652af9515/shm:
Device or resource busy
```

如果绑定挂载 `/var/lib/docker/` 的容器对 `/var/lib/docker/` 内的文件系统句柄使用 `statfs` 或 `fstatfs` 并且没有关闭它们，就会发生此问题。

通常，我们建议不要以这种方式绑定挂载 `/var/lib/docker`。但是，`cAdvisor` 需要此绑定挂载才能实现核心功能。

如果您不确定是哪个进程导致错误中提到的路径繁忙并阻止其被删除，可以使用 `lsof` 命令查找其进程。例如，对于上面的错误：

```console
$ sudo lsof /var/lib/docker/containers/74bef250361c7817bee19349c93139621b272bc8f654ae112dd4eb9652af9515/shm
```

要解决此问题，请停止绑定挂载 `/var/lib/docker` 的容器，然后再次尝试删除其他容器。
