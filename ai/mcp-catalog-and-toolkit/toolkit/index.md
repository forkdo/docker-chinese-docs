# Docker MCP Toolkit





  
  
  
  


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



Docker MCP Toolkit 是集成在 Docker Desktop 中的管理界面，可让您设置、管理和运行容器化的 MCP 服务器，并将它们连接到 AI 代理。它通过提供安全的默认设置、简便的设置过程以及对不断增长的基于 LLM 的客户端生态系统的支持，消除了工具使用的障碍。这是从 MCP 工具发现到本地执行的最快途径。

## 主要功能

- **跨 LLM 兼容性**：适用于 Claude、Cursor 和其他 MCP 客户端。
- **集成工具发现**：直接在 Docker Desktop 中浏览并启动来自 Docker MCP 目录的 MCP 服务器。
- **零手动设置**：无需依赖管理、运行时配置或设置。
- **兼具 MCP 服务器聚合器和网关功能**：客户端可通过其访问已安装的 MCP 服务器。

> [!TIP]
> MCP Toolkit 包含 [Dynamic MCP](/manuals/ai/mcp-catalog-and-toolkit/dynamic-mcp.md)，
> 它使 AI 代理能够在对话期间按需发现、添加和组合 MCP 服务器，而无需手动配置。当您连接到网关时，您的代理可以搜索目录并根据需要添加工具。

## MCP Toolkit 的工作原理

MCP 引入了两个核心概念：MCP 客户端和 MCP 服务器。

- MCP 客户端通常嵌入在基于 LLM 的应用程序中，例如 Claude Desktop 应用。它们请求资源或操作。
- MCP 服务器由客户端启动，以执行请求的任务，使用任何必要的工具、语言或流程。

Docker 标准化了包括 MCP 服务器在内的应用程序的开发、打包和分发。通过将 MCP 服务器打包为容器，Docker 消除了与隔离和环境差异相关的问题。您可以直接运行容器，而无需管理依赖项或配置运行时。

根据 MCP 服务器的不同，其提供的工具可能在与服务器相同的容器内运行，也可能在专用容器中运行以实现更好的隔离。

## 安全性

Docker MCP Toolkit 结合了被动和主动措施，以减少攻击面并确保安全的运行时行为。

### 被动安全

被动安全是指在构建时（当 MCP 服务器代码被打包到 Docker 镜像中时）实施的措施。

- **镜像签名和证明**：[MCP 目录](catalog.md) 中 `mcp/` 下的所有 MCP 服务器镜像均由 Docker 构建并进行数字签名，以验证其来源和完整性。每个镜像都包含软件物料清单 (SBOM)，以实现完全透明。

### 主动安全

主动安全是指运行时的安全措施，在工具调用前后通过资源和访问限制来执行。

- **CPU 分配**：MCP 工具在它们自己的容器中运行。它们被限制为 1 个 CPU，从而限制了潜在滥用计算资源的影响。
- **内存分配**：MCP 工具的容器限制为 2 GB。
- **文件系统访问**：默认情况下，MCP 服务器无权访问主机文件系统。用户需明确选择将授予文件挂载权限的服务器。
- **工具请求拦截**：包含敏感信息（如密钥）的进出工具请求会被阻止。

### OAuth 身份验证

某些 MCP 服务器需要身份验证才能访问外部服务，如 GitHub、Notion 和 Linear。MCP Toolkit 会自动处理 OAuth 身份验证。您通过浏览器授权访问，Toolkit 会安全地管理凭据。您无需手动创建 API 令牌或为每项服务配置身份验证。

#### 使用 OAuth 授权服务器








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
<li>在 Docker Desktop 中，转到 <strong>MCP Toolkit</strong> 并选择 <strong>Catalog</strong> 选项卡。</li>
<li>找到并添加需要 OAuth 的 MCP 服务器。</li>
<li>在服务器的 <strong>Configuration</strong> 选项卡中，选择 <strong>OAuth</strong> 身份验证方法。按照链接开始 OAuth 授权。</li>
<li>您的浏览器将打开该服务的授权页面。按照屏幕上的说明完成身份验证。</li>
<li>身份验证完成后返回 Docker Desktop。</li>
</ol>
<p>在 <strong>OAuth</strong> 选项卡中查看所有已授权的服务。要撤销访问权限，请选择要断开连接的服务旁边的 <strong>Revoke</strong>。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <p>启用 MCP 服务器：</p>
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
<p>如果服务器需要 OAuth，请授权连接：</p>
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
<p>您的浏览器将打开授权页面。完成身份验证过程，然后返回您的终端。</p>
<p>查看已授权的服务：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbWNwIG9hdXRoIGxz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker mcp oauth ls
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>撤销对某项服务的访问权限：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgbWNwIG9hdXRoIHJldm9rZSBnaXRodWI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker mcp oauth revoke github
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 使用示例

### 示例：将 GitHub Official MCP 服务器与 Ask Gordon 结合使用

为了说明 MCP Toolkit 的工作原理，以下是启用 GitHub Official MCP 服务器并使用 [Ask Gordon](/manuals/ai/gordon/_index.md) 与您的 GitHub 帐户交互的方法：

1. 从 Docker Desktop 的 **MCP Toolkit** 菜单中，选择 **Catalog** 选项卡，找到 **GitHub Official** 服务器并添加它。
2. 在服务器的 **Configuration** 选项卡中，通过 OAuth 进行身份验证。
3. 在 **Clients** 选项卡中，确保 Gordon 已连接。
4. 从 **Ask Gordon** 菜单中，您现在可以根据 GitHub Official 服务器提供的工具发送与 GitHub 帐户相关的请求。要进行测试，请询问 Gordon：

   ```text
   What's my GitHub handle?
   ```

   确保通过在 Gordon 的回答中选择 **Always allow** 来允许 Gordon 与 GitHub 交互。

> [!TIP]
> Gordon 客户端默认启用，这意味着 Gordon 可以自动与您的 MCP 服务器交互。

### 示例：使用 Claude Desktop 作为客户端

假设您安装了 Claude Desktop，并且想使用 GitHub MCP 服务器和 Puppeteer MCP 服务器，您无需在 Claude Desktop 中安装这些服务器。您只需在 MCP Toolkit 中安装这 2 个 MCP 服务器，并将 Claude Desktop 添加为客户端：

1. 从 **MCP Toolkit** 菜单中，选择 **Catalog** 选项卡，找到 **Puppeteer** 服务器并添加它。
2. 对 **GitHub Official** 服务器重复此操作。
3. 从 **Clients** 选项卡中，选择 **Claude Desktop** 旁边的 **Connect**。如果 Claude Desktop 正在运行，请重新启动它，现在它就可以访问 MCP Toolkit 中的所有服务器了。
4. 在 Claude Desktop 中，使用 Sonnet 3.5 模型提交以下提示进行测试：

   ```text
   Take a screenshot of docs.docker.com and then invert the colors
   ```

### 示例：使用 Visual Studio Code 作为客户端

您可以在 Visual Studio Code 中与所有已安装的 MCP 服务器交互：

1. 要启用 MCP Toolkit：

   






<div
  class="tabs"
  
    x-data="{ selected: '%E5%85%A8%E5%B1%80%E5%90%AF%E7%94%A8' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E5%85%A8%E5%B1%80%E5%90%AF%E7%94%A8' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%85%A8%E5%B1%80%E5%90%AF%E7%94%A8'"
        
      >
        全局启用
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%B8%BA%E7%89%B9%E5%AE%9A%E9%A1%B9%E7%9B%AE%E5%90%AF%E7%94%A8' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%B8%BA%E7%89%B9%E5%AE%9A%E9%A1%B9%E7%9B%AE%E5%90%AF%E7%94%A8'"
        
      >
        为特定项目启用
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%85%A8%E5%B1%80%E5%90%AF%E7%94%A8' && 'hidden'"
      >
        <ol>
<li>
<p>在 Visual Studio Code 的用户 <code>mcp.json</code> 中插入以下内容：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Im1jcCI6IHsKICJzZXJ2ZXJzIjogewogICAiTUNQX0RPQ0tFUiI6IHsKICAgICAiY29tbWFuZCI6ICJkb2NrZXIiLAogICAgICJhcmdzIjogWwogICAgICAgIm1jcCIsCiAgICAgICAiZ2F0ZXdheSIsCiAgICAgICAicnVuIgogICAgIF0sCiAgICAgInR5cGUiOiAic3RkaW8iCiAgIH0KIH0KfQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-json" data-lang="json"><span class="line"><span class="cl"><span class="s2">&#34;mcp&#34;</span><span class="err">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl"> <span class="nt">&#34;servers&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">   <span class="nt">&#34;MCP_DOCKER&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">     <span class="nt">&#34;command&#34;</span><span class="p">:</span> <span class="s2">&#34;docker&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">     <span class="nt">&#34;args&#34;</span><span class="p">:</span> <span class="p">[</span>
</span></span><span class="line"><span class="cl">       <span class="s2">&#34;mcp&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="s2">&#34;gateway&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="s2">&#34;run&#34;</span>
</span></span><span class="line"><span class="cl">     <span class="p">],</span>
</span></span><span class="line"><span class="cl">     <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;stdio&#34;</span>
</span></span><span class="line"><span class="cl">   <span class="p">}</span>
</span></span><span class="line"><span class="cl"> <span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%B8%BA%E7%89%B9%E5%AE%9A%E9%A1%B9%E7%9B%AE%E5%90%AF%E7%94%A8' && 'hidden'"
      >
        <ol>
<li>
<p>在您的终端中，导航到您的项目文件夹。</p>
</li>
<li>
<p>运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZG9ja2VyIG1jcCBjbGllbnQgY29ubmVjdCB2c2NvZGU=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">docker mcp client connect vscode</span></span></code></pre></div>
      
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
      <p>此命令在当前目录中创建一个 <code>.vscode/mcp.json</code> 文件。由于这是一个用户特定的文件，请将其添加到您的 <code>.gitignore</code> 文件中，以防止将其提交到仓库。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZWNobyAiLnZzY29kZS9tY3AuanNvbiIgPj4gLmdpdGlnbm9yZQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">echo &#34;.vscode/mcp.json&#34; &gt;&gt; .gitignore
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
    </div>
  </blockquote>

</li>
</ol>

      </div>
    
  </div>
</div>


1. 在 Visual Studio Code 中，打开一个新的聊天并选择 **Agent** 模式：

   ![Copilot mode switching](./images/copilot-mode.png)

1. 您还可以检查可用的 MCP 工具：

   ![Displaying tools in VSCode](./images/tools.png)

有关 Agent 模式的更多信息，请参阅 [Visual Studio Code 文档](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode)。

## 延伸阅读

- [MCP Catalog](/manuals/ai/mcp-catalog-and-toolkit/catalog.md)
- [MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)
