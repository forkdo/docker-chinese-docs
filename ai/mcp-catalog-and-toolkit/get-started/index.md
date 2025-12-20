# Docker MCP Toolkit 入门指南





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Beta
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M360-360H217q-18 0-26.5-16t2.5-31l338-488q8-11 20-15t24 1q12 5 19 16t5 24l-39 309h176q19 0 27 17t-4 32L388-66q-8 10-20.5 13T344-55q-11-5-17.5-16T322-95l38-265Z"/></svg></span>
            
          
            
          
            
          
            
          
            
          
        </span>
      </div>
    

    

    
  </div>



Docker MCP Toolkit 可以轻松设置、管理和运行容器化的 Model Context Protocol (MCP) 服务器，并将其连接到 AI 代理。它提供了安全的默认配置，并支持不断增长的基于 LLM 的客户端生态系统。本页面将向您展示如何快速开始使用 Docker MCP Toolkit。

## 设置

在开始之前，请确保您满足以下要求以开始使用 Docker MCP Toolkit。

1. 下载并安装最新版本的 [Docker Desktop](/get-started/get-docker/)。
2. 打开 Docker Desktop 设置，然后选择 **Beta features**。
3. 选择 **Enable Docker MCP Toolkit**。
4. 选择 **Apply**。

Docker Desktop 中的 **Learning center** 提供了教程和资源，帮助您开始使用 Docker 产品和功能。在 **MCP Toolkit** 页面上，**Get started** 教程将指导您安装 MCP 服务器、连接客户端并测试您的设置。

或者，请按照本页的分步说明来：

- [安装 MCP 服务器](#install-mcp-servers)
- [连接客户端](#connect-clients)
- [验证连接](#verify-connections)

## 安装 MCP 服务器








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Desktop' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Desktop'"
        
      >
        Docker Desktop
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'CLI'"
        
      >
        CLI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <ol>
<li>
<p>在 Docker Desktop 中，选择 <strong>MCP Toolkit</strong>，然后选择 <strong>Catalog</strong> 选项卡。</p>
</li>
<li>
<p>在目录中搜索 <strong>GitHub Official</strong> 服务器，然后选择加号图标将其添加。</p>
</li>
<li>
<p>在 <strong>GitHub Official</strong> 服务器页面，选择 <strong>Configuration</strong> 选项卡，然后选择 <strong>OAuth</strong>。</p>


  

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
      <p>所需的配置类型取决于您选择的服务器。对于 GitHub Official 服务器，您必须使用 OAuth 进行身份验证。</p>
    </div>
  </blockquote>

<p>您的浏览器将打开 GitHub 授权页面。请按照屏幕上的说明 
    
  
  <a class="link" href="/ai/mcp-catalog-and-toolkit/toolkit/#authenticate-via-oauth">通过 OAuth 进行身份验证</a>。</p>
</li>
<li>
<p>身份验证完成后返回 Docker Desktop。</p>
</li>
<li>
<p>在目录中搜索 <strong>Playwright</strong> 服务器并添加它。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <ol>
<li>
<p>添加 GitHub Official MCP 服务器。运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbWNwIHNlcnZlciBlbmFibGUgZ2l0aHViLW9mZmljaWFs', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker mcp server <span class="nb">enable</span> github-official
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>通过运行以下命令对服务器进行身份验证：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbWNwIG9hdXRoIGF1dGhvcml6ZSBnaXRodWI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker mcp oauth authorize github
</span></span></code></pre></div>
      
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
      <p>所需的配置类型取决于您选择的服务器。对于 GitHub Official 服务器，您必须使用 OAuth 进行身份验证。</p>
    </div>
  </blockquote>

<p>您的浏览器将打开 GitHub 授权页面。请按照屏幕上的说明 
    
  
  <a class="link" href="/ai/mcp-catalog-and-toolkit/toolkit/#authenticate-via-oauth">通过 OAuth 进行身份验证</a>。</p>
</li>
<li>
<p>添加 <strong>Playwright</strong> 服务器。运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbWNwIHNlcnZlciBlbmFibGUgcGxheXdyaWdodA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker mcp server <span class="nb">enable</span> playwright
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
  </div>
</div>


您已成功添加 MCP 服务器。接下来，连接 MCP 客户端以在 AI 应用程序中使用 MCP Toolkit。

## 连接客户端

要将客户端连接到 MCP Toolkit：

1. 在 Docker Desktop 中，选择 **MCP Toolkit**，然后选择 **Clients** 选项卡。
2. 在列表中找到您的应用程序。
3. 选择 **Connect** 以配置客户端。

如果您的客户端未列出，您可以通过 `stdio` 手动连接 MCP Toolkit，方法是配置您的客户端运行以下命令：

```plaintext
docker mcp gateway run
```

例如，如果您的客户端使用 JSON 文件来配置 MCP 服务器，您可以添加如下条目：

```json {title="Example configuration"
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"],
      "type": "stdio"
    }
  }
}
```

请查阅您正在使用的应用程序的文档，了解如何手动设置 MCP 服务器的说明。

## 验证连接

请参考相关部分，了解如何验证您的设置是否正常工作：

- [Claude Code](#claude-code)
- [Claude Desktop](#claude-desktop)
- [OpenAI Codex](#codex)
- [Continue](#continue)
- [Cursor](#cursor)
- [Gemini](#gemini)
- [Goose](#goose)
- [Gordon](#gordon)
- [LM Studio](#lm-studio)
- [OpenCode](#opencode)
- [Sema4.ai](#sema4)
- [Visual Studio Code](#vscode)
- [Zed](#zed)

### Claude Code

如果您为特定项目配置了 MCP Toolkit，请导航到相关的项目目录。然后运行 `claude mcp list`。输出应显示 `MCP_DOCKER`，状态为 "connected"：

```console
$ claude mcp list
Checking MCP server health...

MCP_DOCKER: docker mcp gateway run - ✓ Connected
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ claude "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Claude Desktop

重启 Claude Desktop 并检查聊天输入中的 **Search and tools** 菜单。您应该看到 `MCP_DOCKER` 服务器已列出并启用：

![Claude Desktop](images/claude-desktop.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Codex

运行 `codex mcp list` 以查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 服务器应出现在列表中，状态为 "enabled"：

```console
$ codex mcp list
Name        Command  Args             Env  Cwd  Status   Auth
MCP_DOCKER  docker   mcp gateway run  -    -    enabled  Unsupported
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ codex "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Continue

通过运行 `cn` 启动 Continue 终端 UI。使用 `/mcp` 命令查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 服务器应出现在列表中，状态为 "connected"：

```plaintext
   MCP Servers

   ➤ 🟢 MCP_DOCKER (🔧75 📝3)
     🔄 Restart all servers
     ⏹️ Stop all servers
     🔍 Explore MCP Servers
     Back

   ↑/↓ to navigate, Enter to select, Esc to go back
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ cn "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Cursor

打开 Cursor。如果您为特定项目配置了 MCP Toolkit，请打开相关的项目目录。然后导航到 **Cursor Settings > Tools & MCP**。您应该在 **Installed MCP Servers** 下看到 `MCP_DOCKER`：

![Cursor](images/cursor.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Gemini

运行 `gemini mcp list` 以查看活动的 MCP 服务器及其状态。`MCP_DOCKER` 应出现在列表中，状态为 "connected"。

```console
$ gemini mcp list
Configured MCP servers:

✓ MCP_DOCKER: docker mcp gateway run (stdio) - Connected
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ gemini "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Goose








<div
  class="tabs"
  
    x-data="{ selected: 'Desktop-app' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Desktop-app' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Desktop-app'"
        
      >
        Desktop app
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'CLI'"
        
      >
        CLI
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Desktop-app' && 'hidden'"
      >
        <p>打开 Goose 桌面应用程序，然后在侧边栏中选择 <strong>Extensions</strong>。在 <strong>Enabled Extensions</strong> 下，您应该看到一个名为 <code>Mcpdocker</code> 的扩展：</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/ai/mcp-catalog-and-toolkit/images/goose.avif"
    alt="Goose desktop app"
    
    
    class="mx-auto rounded-sm"
  />
  
  <template x-teleport="body">
    <div
      x-show="zoom"
      @click="zoom = false"
      x-transition.opacity.duration.250ms
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/100 p-6"
    >
      <button class="icon-svg fixed top-6 right-8 z-30 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-438 270-228q-9 9-21 9t-21-9q-9-9-9-21t9-21l210-210-210-210q-9-9-9-21t9-21q9-9 21-9t21 9l210 210 210-210q9-9 21-9t21 9q9 9 9 21t-9 21L522-480l210 210q9 9 9 21t-9 21q-9 9-21 9t-21-9L480-438Z"/></svg>
      </button>
      <img
        loading="lazy"
        class="max-h-full max-w-full rounded-sm"
        src="/ai/mcp-catalog-and-toolkit/images/goose.avif"
        alt="Goose desktop app"
      />
    </div>
  </template>
</figure>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <p>运行 <code>goose info -v</code> 并在 extensions 下查找名为 <code>mcpdocker</code> 的条目。状态应显示为 <code>enabled: true</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBnb29zZSBpbmZvIC12CuKApgogICAgbWNwZG9ja2VyOgogICAgICBhcmdzOgogICAgICAtIG1jcAogICAgICAtIGdhdGV3YXkKICAgICAgLSBydW4KICAgICAgYXZhaWxhYmxlX3Rvb2xzOiBbXQogICAgICBidW5kbGVkOiBudWxsCiAgICAgIGNtZDogZG9ja2VyCiAgICAgIGRlc2NyaXB0aW9uOiBUaGUgRG9ja2VyIE1DUCBUb29sa2l0IGFsbG93cyBmb3IgZWFzeSBjb25maWd1cmF0aW9uIGFuZCBjb25zdW1wdGlvbiBvZiBNQ1Agc2VydmVycyBmcm9tIHRoZSBEb2NrZXIgTUNQIENhdGFsb2cKICAgICAgZW5hYmxlZDogdHJ1ZQogICAgICBlbnZfa2V5czogW10KICAgICAgZW52czoge30KICAgICAgbmFtZTogbWNwZG9ja2VyCiAgICAgIHRpbWVvdXQ6IDMwMAogICAgICB0eXBlOiBzdGRpbw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> goose info -v
</span></span><span class="line"><span class="cl"><span class="go">…
</span></span></span><span class="line"><span class="cl"><span class="go">    mcpdocker:
</span></span></span><span class="line"><span class="cl"><span class="go">      args:
</span></span></span><span class="line"><span class="cl"><span class="go">      - mcp
</span></span></span><span class="line"><span class="cl"><span class="go">      - gateway
</span></span></span><span class="line"><span class="cl"><span class="go">      - run
</span></span></span><span class="line"><span class="cl"><span class="go">      available_tools: []
</span></span></span><span class="line"><span class="cl"><span class="go">      bundled: null
</span></span></span><span class="line"><span class="cl"><span class="go">      cmd: docker
</span></span></span><span class="line"><span class="cl"><span class="go">      description: The Docker MCP Toolkit allows for easy configuration and consumption of MCP servers from the Docker MCP Catalog
</span></span></span><span class="line"><span class="cl"><span class="go">      enabled: true
</span></span></span><span class="line"><span class="cl"><span class="go">      env_keys: []
</span></span></span><span class="line"><span class="cl"><span class="go">      envs: {}
</span></span></span><span class="line"><span class="cl"><span class="go">      name: mcpdocker
</span></span></span><span class="line"><span class="cl"><span class="go">      timeout: 300
</span></span></span><span class="line"><span class="cl"><span class="go">      type: stdio
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Gordon

在 Docker Desktop 中打开 **Ask Gordon** 视图，然后选择聊天输入区域中的工具箱图标。**MCP Toolkit** 选项卡显示 MCP Toolkit 是否已启用，并显示所有提供的工具：

![MCP Toolkit in the Ask Gordon UI](images/ask-gordon.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接，可以直接在 Docker Desktop 中或使用 CLI：

```console
$ docker ai "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### LM Studio

重启 LM Studio 并开始新的聊天。打开集成菜单并查找名为 `mcp/mcp-docker` 的条目。使用切换按钮启用服务器：

![LM Studio](images/lm-studio.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### OpenCode

OpenCode 配置文件（默认位于 `~/.config/opencode/opencode.json`）包含 MCP Toolkit 的设置：

```json
{
  "mcp": {
    "MCP_DOCKER": {
      "type": "local",
      "command": ["docker", "mcp", "gateway", "run"],
      "enabled": true
    }
  },
  "$schema": "https://opencode.ai/config.json"
}
```

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```console
$ opencode "使用 GitHub MCP 服务器向我展示我的开放拉取请求"
```

### Sema4.ai Studio {#sema4}

在 Sema4.ai Studio 中，在侧边栏中选择 **Actions**，然后选择 **MCP Servers** 选项卡。您应该在列表中看到 Docker MCP Toolkit：

![Docker MCP Toolkit in Sema4.ai Studio](./images/sema4-mcp-list.avif)

要在 Sema4.ai 中使用 MCP Toolkit，请将其添加为代理操作。找到您想要连接到 MCP Toolkit 的代理并打开代理编辑器。选择 **Add Action**，在列表中启用 Docker MCP Toolkit，然后保存您的代理：

![Editing an agent in Sema4.ai Studio](images/sema4-edit-agent.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Visual Studio Code {#vscode}

打开 Visual Studio Code。如果您为特定项目配置了 MCP Toolkit，请打开相关的项目目录。然后打开 **Extensions** 面板。您应该看到 `MCP_DOCKER` 服务器已列出在已安装的 MCP 服务器下。

![MCP_DOCKER installed in Visual Studio Code](images/vscode-extensions.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

### Zed

启动 Zed 并打开代理设置：

![Opening Zed agent settings from command palette](images/zed-cmd-palette.avif)

确保 `MCP_DOCKER` 在 MCP Servers 部分已列出并启用：

![MCP_DOCKER in Zed's agent settings](images/zed-agent-settings.avif)

通过提交一个调用您已安装的 MCP 服务器的提示来测试连接：

```plaintext
使用 GitHub MCP 服务器向我展示我的开放拉取请求
```

## 进一步阅读

- [MCP Toolkit](/manuals/ai/mcp-catalog-and-toolkit/toolkit.md)
- [MCP Catalog](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)
