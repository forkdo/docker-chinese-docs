# 在 CentOS 上安装 Docker Engine

要在 CentOS 上开始使用 Docker Engine，请确保您[满足先决条件](#prerequisites)，然后按照[安装步骤](#installation-methods)进行操作。

## 先决条件

### 操作系统要求

要安装 Docker Engine，您需要以下 CentOS 维护版本之一：

- CentOS Stream 10
- CentOS Stream 9

必须启用 `centos-extras` 存储库。此存储库默认是启用的。如果您禁用了它，则需要重新启用它。

### 卸载旧版本

在安装 Docker Engine 之前，您需要卸载任何冲突的包。

您的 Linux 发行版可能提供非官方的 Docker 包，这些包可能与 Docker 提供的官方包冲突。在安装官方版本的 Docker Engine 之前，您必须卸载这些包。

```console
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

`dnf` 可能会报告您没有安装这些包中的任何一个。

存储在 `/var/lib/docker/` 中的镜像、容器、卷和网络在卸载 Docker 时不会自动删除。

## 安装方法

您可以根据需要以不同方式安装 Docker Engine：

- 您可以[设置 Docker 的存储库](#install-using-the-repository)并从中安装，以便于安装和升级任务。这是推荐的方法。

- 您可以下载 RPM 包，[手动安装](#install-from-a-package)，并完全手动管理升级。这在无法访问互联网的隔离系统上安装 Docker 等情况下非常有用。

- 在测试和开发环境中，您可以使用自动化的[便捷脚本](#install-using-the-convenience-script)来安装 Docker。



Apache License, Version 2.0. 请参阅 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) 获取完整许可证。

### 使用 rpm 存储库安装 {#install-using-the-repository}

在新主机上首次安装 Docker Engine 之前，您需要设置 Docker 存储库。之后，您可以从存储库安装和更新 Docker。

#### 设置存储库

安装 `dnf-plugins-core` 包（提供管理 DNF 存储库的命令）并设置存储库。

```console
$ sudo dnf -y install dnf-plugins-core
$ sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

#### 安装 Docker Engine

1. 安装 Docker 包。

   






<div
  class="tabs"
  
    x-data="{ selected: '%E6%9C%80%E6%96%B0%E7%89%88' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E6%9C%80%E6%96%B0%E7%89%88' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%9C%80%E6%96%B0%E7%89%88'"
        
      >
        最新版
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E7%89%B9%E5%AE%9A%E7%89%88%E6%9C%AC' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E7%89%B9%E5%AE%9A%E7%89%88%E6%9C%AC'"
        
      >
        特定版本
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%9C%80%E6%96%B0%E7%89%88' && 'hidden'"
      >
        <p>要安装最新版本，请运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIGRuZiBpbnN0YWxsIGRvY2tlci1jZSBkb2NrZXItY2UtY2xpIGNvbnRhaW5lcmQuaW8gZG9ja2VyLWJ1aWxkeC1wbHVnaW4gZG9ja2VyLWNvbXBvc2UtcGx1Z2lu', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>如果提示接受 GPG 密钥，请验证指纹是否匹配 <code>060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35</code>，如果匹配，请接受它。</p>
<p>此命令安装 Docker，但不会启动 Docker。它还会创建一个 <code>docker</code> 组，但默认情况下不会向该组添加任何用户。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E7%89%B9%E5%AE%9A%E7%89%88%E6%9C%AC' && 'hidden'"
      >
        <p>要安装特定版本，请先列出存储库中可用的版本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkbmYgbGlzdCBkb2NrZXItY2UgLS1zaG93ZHVwbGljYXRlcyB8IHNvcnQgLXIKCmRvY2tlci1jZS54ODZfNjQgICAgMzoyOS4xLjMtMS5lbDkgICAgZG9ja2VyLWNlLXN0YWJsZQpkb2NrZXItY2UueDg2XzY0ICAgIDM6MjkuMS4yLTEuZWw5ICAgIGRvY2tlci1jZS1zdGFibGUKPC4uLj4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> dnf list docker-ce --showduplicates <span class="p">|</span> sort -r
</span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="go">docker-ce.x86_64    3:29.1.3-1.el9    docker-ce-stable
</span></span></span><span class="line"><span class="cl"><span class="go">docker-ce.x86_64    3:29.1.2-1.el9    docker-ce-stable
</span></span></span><span class="line"><span class="cl"><span class="go">&lt;...&gt;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>返回的列表取决于启用了哪些存储库，并且特定于您的 CentOS 版本（在此示例中由 <code>.el9</code> 后缀表示）。</p>
<p>通过其完全限定的包名安装特定版本，即包名 (<code>docker-ce</code>) 加上版本字符串（第 2 列），用连字符 (<code>-</code>) 分隔。例如，<code>docker-ce-3:29.1.3-1.el9</code>。</p>
<p>将 <code>&lt;VERSION_STRING&gt;</code> 替换为所需的版本，然后运行以下命令进行安装：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzdWRvIGRuZiBpbnN0YWxsIGRvY2tlci1jZS08VkVSU0lPTl9TVFJJTkc&#43;IGRvY2tlci1jZS1jbGktPFZFUlNJT05fU1RSSU5HPiBjb250YWluZXJkLmlvIGRvY2tlci1idWlsZHgtcGx1Z2luIGRvY2tlci1jb21wb3NlLXBsdWdpbg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> sudo dnf install docker-ce-&lt;VERSION_STRING&gt; docker-ce-cli-&lt;VERSION_STRING&gt; containerd.io docker-buildx-plugin docker-compose-plugin
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>此命令安装 Docker，但不会启动 Docker。它还会创建一个 <code>docker</code> 组，但默认情况下不会向该组添加任何用户。</p>

      </div>
    
  </div>
</div>


2. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这会将 Docker systemd 服务配置为在系统启动时自动启动。如果您不希望 Docker 自动启动，请改用 `sudo systemctl start docker`。

3. 通过运行 `hello-world` 镜像来验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行。容器运行时，会打印确认消息并退出。

您现已成功安装并启动了 Docker Engine。



> [!TIP]
> 
> 尝试以非 root 用户身份运行时遇到错误？
>
> `docker` 用户组存在但不包含任何用户，这就是为什么您需要使用 `sudo` 来运行 Docker 命令。请继续阅读 [Linux 安装后配置](/engine/install/linux-postinstall)，了解如何允许非特权用户运行 Docker 命令以及其他可选配置步骤。

#### 升级 Docker Engine

要升级 Docker Engine，请按照[安装说明](#install-using-the-repository)进行操作，选择您要安装的新版本。

### 从软件包安装

如果您无法使用 Docker 的 `rpm` 存储库来安装 Docker Engine，则可以下载适用于您发行版的 `.rpm` 文件并手动安装。每次要升级 Docker Engine 时，您都需要下载一个新文件。

<!-- markdownlint-disable-next-line -->
1. 转到 [https://download.docker.com/linux/centos/](https://download.docker.com/linux/centos/) 并选择您的 CentOS 版本。然后浏览到 `x86_64/stable/Packages/` 并下载您要安装的 Docker 版本的 `.rpm` 文件。

2. 安装 Docker Engine，将以下路径更改为您下载 Docker 包的路径。

   ```console
   $ sudo dnf install /path/to/package.rpm
   ```

   Docker 已安装但未启动。创建了 `docker` 组，但没有用户被添加到该组。

3. 启动 Docker Engine。

   ```console
   $ sudo systemctl enable --now docker
   ```

   这会将 Docker systemd 服务配置为在系统启动时自动启动。如果您不希望 Docker 自动启动，请改用 `sudo systemctl start docker`。

4. 通过运行 `hello-world` 镜像来验证安装是否成功：

   ```console
   $ sudo docker run hello-world
   ```

   此命令下载测试镜像并在容器中运行。容器运行时，会打印确认消息并退出。

您现已成功安装并启动了 Docker Engine。



> [!TIP]
> 
> 尝试以非 root 用户身份运行时遇到错误？
>
> `docker` 用户组存在但不包含任何用户，这就是为什么您需要使用 `sudo` 来运行 Docker 命令。请继续阅读 [Linux 安装后配置](/engine/install/linux-postinstall)，了解如何允许非特权用户运行 Docker 命令以及其他可选配置步骤。

#### 升级 Docker Engine

要升级 Docker Engine，请下载较新的软件包文件，并重复[安装过程](#install-from-a-package)，使用 `dnf upgrade` 代替 `dnf install`，并指向新文件。



### 使用便捷脚本安装

Docker 提供了一个便捷脚本，位于 [https://get.docker.com/](https://get.docker.com/)，用于以非交互方式将 Docker 安装到开发环境中。该便捷脚本不推荐用于生产环境，但对于创建符合您需求的配置脚本很有用。另请参阅[使用仓库安装](#install-using-the-repository)步骤，了解使用软件包仓库进行安装的相关步骤。该脚本的源代码是开源的，您可以在 GitHub 上的 [`docker-install` 仓库](https://github.com/docker/docker-install) 中找到它。

<!-- prettier-ignore -->
在本地运行从互联网下载的脚本之前，请务必仔细检查。在安装之前，请熟悉便捷脚本的潜在风险和限制：

- 该脚本需要 `root` 或 `sudo` 权限才能运行。
- 该脚本会尝试检测您的 Linux 发行版和版本，并为您配置包管理系统。
- 该脚本不允许您自定义大多数安装参数。
- 该脚本会安装依赖项和推荐包，而不会要求确认。根据主机机器的当前配置，这可能会安装大量软件包。
- 默认情况下，该脚本会安装 Docker、containerd 和 runc 的最新稳定版本。使用此脚本配置机器时，可能会导致 Docker 意外地进行主要版本升级。在将升级部署到生产系统之前，请务必在测试环境中测试升级。
- 该脚本并非用于升级现有的 Docker 安装。使用该脚本更新现有安装时，依赖项可能不会更新到预期版本，从而导致版本过时。

> [!TIP]
>
> 在运行脚本之前预览脚本步骤。您可以使用 `--dry-run` 选项运行脚本，以了解脚本被调用时将运行的步骤：
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

此示例从 [https://get.docker.com/](https://get.docker.com/) 下载脚本并运行它，以在 Linux 上安装 Docker 的最新稳定版本：

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

现在，您已成功安装并启动了 Docker 引擎。基于 Debian 的发行版会自动启动 `docker` 服务。在基于 `RPM` 的发行版（如 CentOS、Fedora 或 RHEL）上，您需要使用适当的 `systemctl` 或 `service` 命令手动启动它。如消息所示，默认情况下，非 root 用户无法运行 Docker 命令。

> **以非特权用户使用 Docker，或以无根模式安装？**
>
> 安装脚本需要 `root` 或 `sudo` 权限才能安装和使用 Docker。如果您想授予非 root 用户访问 Docker 的权限，请参阅 [Linux 安装后步骤](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)。您也可以在没有 `root` 权限的情况下安装 Docker，或配置为以无根模式运行。有关以无根模式运行 Docker 的说明，请参阅[以非 root 用户身份运行 Docker 守护进程（无根模式）](/engine/security/rootless/)。

#### 安装预发布版本

Docker 还在 [https://test.docker.com/](https://test.docker.com/) 提供了一个便捷脚本，用于在 Linux 上安装 Docker 的预发布版本。该脚本与 `get.docker.com` 上的脚本相同，但会将您的包管理器配置为使用 Docker 软件包仓库的测试通道。测试通道包括 Docker 的稳定版本和预发布版本（测试版本、候选发布版本）。使用此脚本可以提前获取新版本，并在它们作为稳定版本发布之前在测试环境中对其进行评估。

要在 Linux 上从测试通道安装 Docker 的最新版本，请运行：

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### 使用便捷脚本后升级 Docker

如果您使用便捷脚本安装了 Docker，则应直接使用包管理器升级 Docker。重新运行便捷脚本没有任何优势。如果它尝试重新安装主机上已存在的仓库，重新运行它可能会导致问题。

## 卸载 Docker Engine

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 包：

   ```console
   $ sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的镜像、容器、卷或自定义配置文件不会自动删除。要删除所有镜像、容器和卷：

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

您必须手动删除任何编辑过的配置文件。

## 后续步骤

- 继续阅读 [Linux 安装后步骤](linux-postinstall.md)。
