# 在 Mac 上安装 Docker Desktop

> **Docker Desktop 条款**
>
> 在大型企业中（员工人数超过 250 人或年收入超过 1000 万美元）将 Docker Desktop 用于商业用途需要[付费订阅](https://www.docker.com/pricing/)。

此页面提供了适用于 Mac 的 Docker Desktop 的下载链接、系统要求以及分步安装说明。


<a class="button not-prose" href="https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&amp;utm_medium=webreferral&amp;utm_campaign=docs-driven-download-mac-arm64">适用于 Apple 芯片的 Mac 的 Docker Desktop</a>


<a class="button not-prose" href="https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&amp;utm_medium=webreferral&amp;utm_campaign=docs-driven-download-mac-amd64">适用于 Intel 芯片的 Mac 的 Docker Desktop</a>


*有关校验和，请参阅[发行说明](/manuals/desktop/release-notes.md)。*

## 系统要求








<div
  class="tabs"
  
    x-data="{ selected: '%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac'"
        
      >
        搭载 Intel 芯片的 Mac
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E6%90%AD%E8%BD%BD-Apple-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%90%AD%E8%BD%BD-Apple-%E8%8A%AF%E7%89%87%E7%9A%84-Mac'"
        
      >
        搭载 Apple 芯片的 Mac
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' && 'hidden'"
      >
        <ul>
<li>
<p>受支持的 macOS 版本。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p>[!重要]</p>
<p>Docker Desktop 支持当前版本以及前两个主要的 macOS 版本。随着新的主要 macOS 版本正式发布，Docker 将停止支持最旧的版本，并同时支持最新的 macOS 版本（以及前两个版本）。</p>

  </blockquote>

</li>
<li>
<p>至少 4 GB 内存。</p>
</li>
</ul>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%90%AD%E8%BD%BD-Apple-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' && 'hidden'"
      >
        <ul>
<li>
<p>受支持的 macOS 版本。</p>


  

<blockquote
  
  class="admonition not-prose">
  <p>[!重要]</p>
<p>Docker Desktop 支持当前版本以及前两个主要的 macOS 版本。随着新的主要 macOS 版本正式发布，Docker 将停止支持最旧的版本，并同时支持最新的 macOS 版本（以及前两个版本）。</p>

  </blockquote>

</li>
<li>
<p>至少 4 GB 内存。</p>
</li>
<li>
<p>为了获得最佳体验，建议安装 Rosetta 2。Rosetta 2 不再是严格必需项，但某些可选命令行工具在使用 Darwin/AMD64 时仍需要 Rosetta 2。请参阅
    
  
  <a class="link" href="https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/">已知问题</a>。要从命令行手动安装 Rosetta 2，请运行以下命令：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBzb2Z0d2FyZXVwZGF0ZSAtLWluc3RhbGwtcm9zZXR0YQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> softwareupdate --install-rosetta
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ul>

      </div>
    
  </div>
</div>


> **在安装或更新之前**
>
> - 退出可能在后台调用 Docker 的工具（Visual Studio Code、终端、代理应用）。
>
> - 如果您管理设备群或通过 MDM 安装，请使用[**PKG 安装程序**](/manuals/enterprise/enterprise-deployment/pkg-install-and-configure.md)。
>
> - 在安装完成之前，请保持安装程序卷处于挂载状态。
>
> 如果您遇到“Docker.app 已损坏”对话框，请参阅[修复 macOS 上的“Docker.app 已损坏”](/manuals/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog.md)。

## 在 Mac 上安装和运行 Docker Desktop

> [!提示]
>
> 请参阅[常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md#how-do-I-run-docker-desktop-without-administrator-privileges)，了解如何在不需要管理员权限的情况下安装和运行 Docker Desktop。

### 交互式安装

1. 使用页面顶部的下载按钮或从[发行说明](/manuals/desktop/release-notes.md)下载安装程序。

2. 双击 `Docker.dmg` 打开安装程序，然后将 Docker 图标拖到**应用程序**文件夹中。默认情况下，Docker Desktop 安装在 `/Applications/Docker.app`。

3. 双击**应用程序**文件夹中的 `Docker.app` 启动 Docker。

4. Docker 菜单会显示 Docker 订阅服务协议。

    以下是关键点的摘要：
    - Docker Desktop 对小型企业（员工少于 250 人且年收入低于 1000 万美元）、个人使用、教育以及非商业开源项目免费。
    - 否则，专业用途需要付费订阅。
    - 政府实体也需要付费订阅。
    - Docker Pro、Team 和 Business 订阅包括 Docker Desktop 的商业用途。

5. 选择**接受**以继续。

   请注意，如果您不同意条款，Docker Desktop 将无法运行。您可以选择稍后通过打开 Docker Desktop 来接受条款。

   有关更多信息，请参阅 [Docker Desktop 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)。建议您同时阅读[常见问题解答](https://www.docker.com/pricing/faq)。

6. 在安装窗口中，选择以下任一选项：
   - **使用推荐设置（需要密码）**。这允许 Docker Desktop 自动设置必要的配置设置。
   - **使用高级设置**。然后，您可以将 Docker CLI 工具的位置设置在系统或用户目录中，启用默认 Docker 套接字，并启用特权端口映射。有关更多信息以及如何设置 Docker CLI 工具的位置，请参阅[设置](/manuals/desktop/settings-and-maintenance/settings.md#advanced)。
7. 选择**完成**。如果您在第 6 步中应用了任何需要密码的配置，请输入密码以确认您的选择。

### 从命令行安装

下载 `Docker.dmg` 后（使用页面顶部的下载按钮或从[发行说明](/manuals/desktop/release-notes.md)），在终端中运行以下命令以在**应用程序**文件夹中安装 Docker Desktop：

```console
$ sudo hdiutil attach Docker.dmg
$ sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
$ sudo hdiutil detach /Volumes/Docker
```

默认情况下，Docker Desktop 安装在 `/Applications/Docker.app`。由于 macOS 通常在首次使用应用程序时执行安全检查，因此 `install` 命令可能需要几分钟才能运行。

#### 安装程序标志

`install` 命令接受以下标志：

##### 安装行为

- `--accept-license`：现在接受 [Docker 订阅服务协议](https://www.docker.com/legal/docker-subscription-service-agreement)，而不是在首次运行应用程序时要求接受。
- `--user=<username>`：在安装过程中执行一次特权配置。这消除了用户在首次运行时授予 root 权限的需要。有关更多信息，请参阅[特权帮助程序权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#permission-requirements)。要查找用户名，请在 CLI 中输入 `ls /Users`。

##### 安全和访问

- `--allowed-org=<org name>`：要求用户在运行应用程序时登录并成为指定的 Docker Hub 组织的一部分
- `--user=<username>`：在安装过程中执行一次特权配置。这消除了用户在首次运行时授予 root 权限的需要。有关更多信息，请参阅[特权帮助程序权限要求](/manuals/desktop/setup/install/mac-permission-requirements.md#permission-requirements)。要查找用户名，请在 CLI 中输入 `ls /Users`。
- `--admin-settings`：自动创建一个 `admin-settings.json` 文件，管理员使用该文件来控制其组织内客户端机器上的某些 Docker Desktop 设置。有关更多信息，请参阅[设置管理](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)。
  - 必须与 `--allowed-org=<org name>` 标志一起使用。
  - 例如：`--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`

##### 代理配置

- `--proxy-http-mode=<mode>`：设置 HTTP 代理模式。两种模式为 `system`（默认）或 `manual`。
- `--override-proxy-http=<URL>`：设置用于传出 HTTP 请求的 HTTP 代理的 URL。它要求 `--proxy-http-mode` 为 `manual`。
- `--override-proxy-https=<URL>`：设置用于传出 HTTPS 请求的 HTTP 代理的 URL，要求 `--proxy-http-mode` 为 `manual`
- `--override-proxy-exclude=<hosts/domains>`：为主机和域绕过代理设置。这是一个逗号分隔的列表。
- `--override-proxy-pac=<PAC file URL>`：设置 PAC 文件 URL。此设置仅在使用 `manual` 代理模式时生效。
- `--override-proxy-embedded-pac=<PAC script>`：指定嵌入的 PAC（代理自动配置）脚本。此设置仅在使用 `manual` 代理模式时生效，并且优先于 `--override-proxy-pac` 标志。

###### 指定 PAC 文件示例

```console
$ sudo /Applications/Docker.app/Contents/MacOS/install --user testuser --proxy-http-mode="manual" --override-proxy-pac="http://localhost:8080/myproxy.pac"
```

###### 指定 PAC 脚本示例

```console
$ sudo /Applications/Docker.app/Contents/MacOS/install --user testuser --proxy-http-mode="manual" --override-proxy-embedded-pac="function FindProxyForURL(url, host) { return \"DIRECT\"; }"
```

> [!提示]
>
> 作为 IT 管理员，您可以使用端点管理 (MDM) 软件来识别环境中 Docker Desktop 实例的数量及其版本。这可以提供准确的许可证报告，帮助确保您的机器使用最新版本的 Docker Desktop，并使您能够[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。
> - [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> - [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> - [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> - [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> - [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## 下一步

- 浏览 [Docker 的订阅](https://www.docker.com/pricing/)，了解 Docker 可以为您提供什么。
- [开始使用 Docker](/get-started/introduction/_index.md)。
- [探索 Docker Desktop](/manuals/desktop/use-desktop/_index.md) 及其所有功能。
- [故障排除](/manuals/desktop/troubleshoot-and-support/troubleshoot/_index.md) 描述了常见问题、解决方法、如何运行和提交诊断信息以及提交问题。
- [常见问题解答](/manuals/desktop/troubleshoot-and-support/faqs/general.md) 提供常见问题的答案。
- [发行说明](/manuals/desktop/release-notes.md) 列出了与 Docker Desktop 版本相关的组件更新、新功能和改进。
- [备份和恢复数据](/manuals/desktop/settings-and-maintenance/backup-and-restore.md) 提供了有关备份和恢复与 Docker 相关的数据的说明。
