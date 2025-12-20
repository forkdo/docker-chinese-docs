# 构建代码质量检查工作流

在本节中，您将逐步构建一个完整的代码质量自动化工作流。您将从创建一个包含 GitHub 和 SonarQube MCP 服务器的 E2B 沙箱开始，然后逐步添加功能，直到拥有一个可投入生产的、能够分析代码质量并创建拉取请求的工作流。

通过按顺序完成每个步骤，您将学习 MCP 服务器的工作原理、如何通过 Claude 与它们交互，以及如何将操作串联起来以构建强大的自动化工作流。

## 先决条件

在开始之前，请确保您拥有：

- 具有 [API 访问权限](https://e2b.dev/docs/api-key) 的 E2B 账户
- [Anthropic API 密钥](https://docs.claude.com/en/api/admin-api/apikeys/get-api-key)

  > [!NOTE]
  >
  > 此示例使用 Claude CLI，它已预装在 E2B 沙箱中，但您可以调整示例以使用您选择的其他 AI 助手。有关替代连接方法，请参阅 [E2B 的 MCP 文档](https://e2b.dev/docs/mcp/quickstart)。

- GitHub 账户，包含：
  - 一个包含待分析代码的仓库
  - 具有 `repo` 范围的 [个人访问令牌](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- SonarCloud 账户，包含：
  - 已创建的 [组织](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/resources-structure/organization)
  - 为您的仓库 [配置的项目](https://docs.sonarsource.com/sonarqube-community-build/project-administration/creating-and-importing-projects)
  - 已生成的 [用户令牌](https://docs.sonarsource.com/sonarqube-server/instance-administration/security/administering-tokens)
- 已安装的语言运行时：
  - TypeScript: [Node.js 18+](https://nodejs.org/en/download)
  - Python: [Python 3.8+](https://www.python.org/downloads/)

> [!NOTE]
>
> 本指南使用 Claude 的 `--dangerously-skip-permissions` 标志来启用 E2B 沙箱中的自动化命令执行。此标志会绕过权限提示，这适用于像 E2B 这样的隔离容器环境，因为沙箱是临时性的，并且与您的本地机器分开。
>
> 但是，请注意 Claude 可以在沙箱内执行任何命令，包括访问该环境中的文件和凭证。仅将此方法用于受信任的代码和工作流。更多信息，请参阅 [Anthropic 关于容器安全的指南](https://docs.anthropic.com/en/docs/claude-code/devcontainer)。

## 设置您的项目








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
      >
        <ol>
<li>
<p>为您的工作流创建一个新目录并初始化 Node.js：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bWtkaXIgZ2l0aHViLXNvbmFycXViZS13b3JrZmxvdwpjZCBnaXRodWItc29uYXJxdWJlLXdvcmtmbG93Cm5wbSBpbml0IC15', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">mkdir github-sonarqube-workflow
</span></span><span class="line"><span class="cl"><span class="nb">cd</span> github-sonarqube-workflow
</span></span><span class="line"><span class="cl">npm init -y</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>打开 <code>package.json</code> 并将其配置为 ES 模块：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICJuYW1lIjogImdpdGh1Yi1zb25hcnF1YmUtd29ya2Zsb3ciLAogICJ2ZXJzaW9uIjogIjEuMC4wIiwKICAiZGVzY3JpcHRpb24iOiAi5L2/55SoIEUyQuOAgUdpdEh1YiDlkowgU29uYXJRdWJlIOeahOiHquWKqOWMluS7o&#43;eggei0qOmHj&#43;W3peS9nOa1gSIsCiAgInR5cGUiOiAibW9kdWxlIiwKICAibWFpbiI6ICJxdWFsaXR5LXdvcmtmbG93LnRzIiwKICAic2NyaXB0cyI6IHsKICAgICJzdGFydCI6ICJ0c3ggcXVhbGl0eS13b3JrZmxvdy50cyIKICB9LAogICJrZXl3b3JkcyI6IFsiZTJiIiwgImdpdGh1YiIsICJzb25hcnF1YmUiLCAibWNwIiwgImNvZGUtcXVhbGl0eSJdLAogICJhdXRob3IiOiAiIiwKICAibGljZW5zZSI6ICJNSVQiCn0=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-json" data-lang="json"><span class="line"><span class="cl"><span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;name&#34;</span><span class="p">:</span> <span class="s2">&#34;github-sonarqube-workflow&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;version&#34;</span><span class="p">:</span> <span class="s2">&#34;1.0.0&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;description&#34;</span><span class="p">:</span> <span class="s2">&#34;使用 E2B、GitHub 和 SonarQube 的自动化代码质量工作流&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;module&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;main&#34;</span><span class="p">:</span> <span class="s2">&#34;quality-workflow.ts&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;scripts&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nt">&#34;start&#34;</span><span class="p">:</span> <span class="s2">&#34;tsx quality-workflow.ts&#34;</span>
</span></span><span class="line"><span class="cl">  <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;keywords&#34;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&#34;e2b&#34;</span><span class="p">,</span> <span class="s2">&#34;github&#34;</span><span class="p">,</span> <span class="s2">&#34;sonarqube&#34;</span><span class="p">,</span> <span class="s2">&#34;mcp&#34;</span><span class="p">,</span> <span class="s2">&#34;code-quality&#34;</span><span class="p">],</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;author&#34;</span><span class="p">:</span> <span class="s2">&#34;&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;license&#34;</span><span class="p">:</span> <span class="s2">&#34;MIT&#34;</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>安装所需的依赖项：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bnBtIGluc3RhbGwgZTJiIGRvdGVudgpucG0gaW5zdGFsbCAtRCB0eXBlc2NyaXB0IHRzeCBAdHlwZXMvbm9kZQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">npm install e2b dotenv
</span></span><span class="line"><span class="cl">npm install -D typescript tsx @types/node</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>在项目根目录创建一个 <code>.env</code> 文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'dG91Y2ggLmVudg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">touch .env</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>添加您的 API 密钥和配置，将占位符替换为您的实际凭证：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'RTJCX0FQSV9LRVk9eW91cl9lMmJfYXBpX2tleV9oZXJlCkFOVEhST1BJQ19BUElfS0VZPXlvdXJfYW50aHJvcGljX2FwaV9rZXlfaGVyZQpHSVRIVUJfVE9LRU49Z2hwX3lvdXJfcGVyc29uYWxfYWNjZXNzX3Rva2VuX2hlcmUKR0lUSFVCX09XTkVSPXlvdXJfZ2l0aHViX3VzZXJuYW1lCkdJVEhVQl9SRVBPPXlvdXJfcmVwb3NpdG9yeV9uYW1lClNPTkFSUVVCRV9PUkc9eW91cl9zb25hcmNsb3VkX29yZ19rZXkKU09OQVJRVUJFX1RPS0VOPXlvdXJfc29uYXJxdWJlX3VzZXJfdG9rZW4KU09OQVJRVUJFX1VSTD1odHRwczovL3NvbmFyY2xvdWQuaW8=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-plaintext" data-lang="plaintext"><span class="line"><span class="cl">E2B_API_KEY=your_e2b_api_key_here
</span></span><span class="line"><span class="cl">ANTHROPIC_API_KEY=your_anthropic_api_key_here
</span></span><span class="line"><span class="cl">GITHUB_TOKEN=ghp_your_personal_access_token_here
</span></span><span class="line"><span class="cl">GITHUB_OWNER=your_github_username
</span></span><span class="line"><span class="cl">GITHUB_REPO=your_repository_name
</span></span><span class="line"><span class="cl">SONARQUBE_ORG=your_sonarcloud_org_key
</span></span><span class="line"><span class="cl">SONARQUBE_TOKEN=your_sonarqube_user_token
</span></span><span class="line"><span class="cl">SONARQUBE_URL=https://sonarcloud.io</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>通过将 <code>.env</code> 添加到 <code>.gitignore</code> 来保护您的凭证：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZWNobyAiLmVudiIgPj4gLmdpdGlnbm9yZQplY2hvICJub2RlX21vZHVsZXMvIiA&#43;PiAuZ2l0aWdub3Jl', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="nb">echo</span> <span class="s2">&#34;.env&#34;</span> &gt;&gt; .gitignore
</span></span><span class="line"><span class="cl"><span class="nb">echo</span> <span class="s2">&#34;node_modules/&#34;</span> &gt;&gt; .gitignore</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <ol>
<li>
<p>为您的工作流创建一个新目录：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bWtkaXIgZ2l0aHViLXNvbmFycXViZS13b3JrZmxvdwpjZCBnaXRodWItc29uYXJxdWJlLXdvcmtmbG93', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">mkdir github-sonarqube-workflow
</span></span><span class="line"><span class="cl"><span class="nb">cd</span> github-sonarqube-workflow</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>创建虚拟环境并激活它：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cHl0aG9uMyAtbSB2ZW52IHZlbnYKc291cmNlIHZlbnYvYmluL2FjdGl2YXRlICAjIOWcqCBXaW5kb3dzIOS4ijogdmVudlxTY3JpcHRzXGFjdGl2YXRl', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">python3 -m venv venv
</span></span><span class="line"><span class="cl"><span class="nb">source</span> venv/bin/activate  <span class="c1"># 在 Windows 上: venv\Scripts\activate</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>安装所需的依赖项：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cGlwIGluc3RhbGwgZTJiIHB5dGhvbi1kb3RlbnY=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">pip install e2b python-dotenv</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>在项目根目录创建一个 <code>.env</code> 文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'dG91Y2ggLmVudg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">touch .env</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>添加您的 API 密钥和配置，将占位符替换为您的实际凭证：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'RTJCX0FQSV9LRVk9eW91cl9lMmJfYXBpX2tleV9oZXJlCkFOVEhST1BJQ19BUElfS0VZPXlvdXJfYW50aHJvcGljX2FwaV9rZXlfaGVyZQpHSVRIVUJfVE9LRU49Z2hwX3lvdXJfcGVyc29uYWxfYWNjZXNzX3Rva2VuX2hlcmUKR0lUSFVCX09XTkVSPXlvdXJfZ2l0aHViX3VzZXJuYW1lCkdJVEhVQl9SRVBPPXlvdXJfcmVwb3NpdG9yeV9uYW1lClNPTkFSUVVCRV9PUkc9eW91cl9zb25hcmNsb3VkX29yZ19rZXkKU09OQVJRVUJFX1RPS0VOPXlvdXJfc29uYXJxdWJlX3VzZXJfdG9rZW4KU09OQVJRVUJFX1VSTD1odHRwczovL3NvbmFyY2xvdWQuaW8=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-plaintext" data-lang="plaintext"><span class="line"><span class="cl">E2B_API_KEY=your_e2b_api_key_here
</span></span><span class="line"><span class="cl">ANTHROPIC_API_KEY=your_anthropic_api_key_here
</span></span><span class="line"><span class="cl">GITHUB_TOKEN=ghp_your_personal_access_token_here
</span></span><span class="line"><span class="cl">GITHUB_OWNER=your_github_username
</span></span><span class="line"><span class="cl">GITHUB_REPO=your_repository_name
</span></span><span class="line"><span class="cl">SONARQUBE_ORG=your_sonarcloud_org_key
</span></span><span class="line"><span class="cl">SONARQUBE_TOKEN=your_sonarqube_user_token
</span></span><span class="line"><span class="cl">SONARQUBE_URL=https://sonarcloud.io</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>通过将 <code>.env</code> 添加到 <code>.gitignore</code> 来保护您的凭证：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZWNobyAiLmVudiIgPj4gLmdpdGlnbm9yZQplY2hvICJ2ZW52LyIgPj4gLmdpdGlnbm9yZQplY2hvICJfX3B5Y2FjaGVfXy8iID4&#43;IC5naXRpZ25vcmU=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="nb">echo</span> <span class="s2">&#34;.env&#34;</span> &gt;&gt; .gitignore
</span></span><span class="line"><span class="cl"><span class="nb">echo</span> <span class="s2">&#34;venv/&#34;</span> &gt;&gt; .gitignore
</span></span><span class="line"><span class="cl"><span class="nb">echo</span> <span class="s2">&#34;__pycache__/&#34;</span> &gt;&gt; .gitignore</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
  </div>
</div>


## 步骤 1：创建您的第一个沙箱

让我们从创建一个沙箱开始，并验证 MCP 服务器是否已正确配置。








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
      >
        <p>在项目根目录创建一个名为 <code>01-test-connection.ts</code> 的文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiB0ZXN0Q29ubmVjdGlvbigpIHsKICBjb25zb2xlLmxvZygKICAgICJDcmVhdGluZyBFMkIgc2FuZGJveCB3aXRoIEdpdEh1YiBhbmQgU29uYXJRdWJlIE1DUCBzZXJ2ZXJzLi4uXG4iLAogICk7CgogIGNvbnN0IHNieCA9IGF3YWl0IFNhbmRib3guYmV0YUNyZWF0ZSh7CiAgICBlbnZzOiB7CiAgICAgIEFOVEhST1BJQ19BUElfS0VZOiBwcm9jZXNzLmVudi5BTlRIUk9QSUNfQVBJX0tFWSEsCiAgICAgIEdJVEhVQl9UT0tFTjogcHJvY2Vzcy5lbnYuR0lUSFVCX1RPS0VOISwKICAgICAgU09OQVJRVUJFX1RPS0VOOiBwcm9jZXNzLmVudi5TT05BUlFVQkVfVE9LRU4hLAogICAgfSwKICAgIG1jcDogewogICAgICBnaXRodWJPZmZpY2lhbDogewogICAgICAgIGdpdGh1YlBlcnNvbmFsQWNjZXNzVG9rZW46IHByb2Nlc3MuZW52LkdJVEhVQl9UT0tFTiEsCiAgICAgIH0sCiAgICAgIHNvbmFycXViZTogewogICAgICAgIG9yZzogcHJvY2Vzcy5lbnYuU09OQVJRVUJFX09SRyEsCiAgICAgICAgdG9rZW46IHByb2Nlc3MuZW52LlNPTkFSUVVCRV9UT0tFTiEsCiAgICAgICAgdXJsOiAiaHR0cHM6Ly9zb25hcmNsb3VkLmlvIiwKICAgICAgfSwKICAgIH0sCiAgfSk7CgogIGNvbnN0IG1jcFVybCA9IHNieC5iZXRhR2V0TWNwVXJsKCk7CiAgY29uc3QgbWNwVG9rZW4gPSBhd2FpdCBzYnguYmV0YUdldE1jcFRva2VuKCk7CgogIGNvbnNvbGUubG9nKCIgU2FuZGJveCBjcmVhdGVkIHN1Y2Nlc3NmdWxseSEiKTsKICBjb25zb2xlLmxvZyhgTUNQIEdhdGV3YXkgVVJMOiAke21jcFVybH1cbmApOwoKICAvLyDnrYnlvoUgTUNQIOWIneWni&#43;WMlgogIGF3YWl0IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiBzZXRUaW1lb3V0KHJlc29sdmUsIDEwMDApKTsKCiAgLy8g6YWN572uIENsYXVkZSDkvb/nlKggTUNQIOe9keWFswogIGNvbnNvbGUubG9nKCJDb25uZWN0aW5nIENsYXVkZSBDTEkgdG8gTUNQIGdhdGV3YXkuLi4iKTsKICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgYGNsYXVkZSBtY3AgYWRkIC0tdHJhbnNwb3J0IGh0dHAgZTJiLW1jcC1nYXRld2F5ICR7bWNwVXJsfSAtLWhlYWRlciAiQXV0aG9yaXphdGlvbjogQmVhcmVyICR7bWNwVG9rZW59ImAsCiAgICB7CiAgICAgIHRpbWVvdXRNczogMCwKICAgICAgb25TdGRvdXQ6IGNvbnNvbGUubG9nLAogICAgICBvblN0ZGVycjogY29uc29sZS5sb2csCiAgICB9LAogICk7CgogIGNvbnNvbGUubG9nKCJcbsKcQ29ubmVjdGlvbiBzdWNjZXNzZnVsISBDbGVhbmluZyB1cC4uLiIpOwogIGF3YWl0IHNieC5raWxsKCk7Cn0KCnRlc3RDb25uZWN0aW9uKCkuY2F0Y2goY29uc29sZS5lcnJvcik7', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">import</span> <span class="s2">&#34;dotenv/config&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">Sandbox</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;e2b&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">testConnection() {</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="s2">&#34;Creating E2B sandbox with GitHub and SonarQube MCP servers...\n&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">GITHUB_TOKEN</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">SONARQUBE_TOKEN</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nx">sonarqube</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">org</span>: <span class="kt">process.env.SONARQUBE_ORG</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">token</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">url</span><span class="o">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34; Sandbox created successfully!&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="sb">`MCP Gateway URL: </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="err">\</span><span class="sb">n`</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="c1">// 等待 MCP 初始化
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">1000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="c1">// 配置 Claude 使用 MCP 网关
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Connecting Claude CLI to MCP gateway...&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nConnection successful! Cleaning up...&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">testConnection</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行此脚本以验证您的设置：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bnB4IHRzeCAwMS10ZXN0LWNvbm5lY3Rpb24udHM=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">npx tsx 01-test-connection.ts</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>在项目根目录创建一个名为 <code>01_test_connection.py</code> 的文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmZyb20gZG90ZW52IGltcG9ydCBsb2FkX2RvdGVudgpmcm9tIGUyYiBpbXBvcnQgQXN5bmNTYW5kYm94Cgpsb2FkX2RvdGVudigpCgphc3luYyBkZWYgdGVzdF9jb25uZWN0aW9uKCk6CiAgICBwcmludCgiQ3JlYXRpbmcgRTJCIHNhbmRib3ggd2l0aCBHaXRIdWIgYW5kIFNvbmFyUXViZSBNQ1Agc2VydmVycy4uLlxuIikKCiAgICBzYnggPSBhd2FpdCBBc3luY1NhbmRib3guYmV0YV9jcmVhdGUoCiAgICAgICAgZW52cz17CiAgICAgICAgICAgICJBTlRIUk9QSUNfQVBJX0tFWSI6IG9zLmdldGVudigiQU5USFJPUElDX0FQSV9LRVkiKSwKICAgICAgICAgICAgIkdJVEhVQl9UT0tFTiI6IG9zLmdldGVudigiR0lUSFVCX1RPS0VOIiksCiAgICAgICAgICAgICJTT05BUlFVQkVfVE9LRU4iOiBvcy5nZXRlbnYoIlNPTkFSUVVCRV9UT0tFTiIpLAogICAgICAgIH0sCiAgICAgICAgbWNwPXsKICAgICAgICAgICAgImdpdGh1Yk9mZmljaWFsIjogewogICAgICAgICAgICAgICAgImdpdGh1YlBlcnNvbmFsQWNjZXNzVG9rZW4iOiBvcy5nZXRlbnYoIkdJVEhVQl9UT0tFTiIpLAogICAgICAgICAgICB9LAogICAgICAgICAgICAic29uYXJxdWJlIjogewogICAgICAgICAgICAgICAgIm9yZyI6IG9zLmdldGVudigiU09OQVJRVUJFX09SRyIpLAogICAgICAgICAgICAgICAgInRva2VuIjogb3MuZ2V0ZW52KCJTT05BUlFVQkVfVE9LRU4iKSwKICAgICAgICAgICAgICAgICJ1cmwiOiAiaHR0cHM6Ly9zb25hcmNsb3VkLmlvIiwKICAgICAgICAgICAgfSwKICAgICAgICB9LAogICAgKQoKICAgIG1jcF91cmwgPSBzYnguYmV0YV9nZXRfbWNwX3VybCgpCiAgICBtY3BfdG9rZW4gPSBhd2FpdCBzYnguYmV0YV9nZXRfbWNwX3Rva2VuKCkKCiAgICBwcmludCgiIFNhbmRib3ggY3JlYXRlZCBzdWNjZXNzZnVsbHkhIikKICAgIHByaW50KGYiTUNQIEdhdGV3YXkgVVJMOiB7bWNwX3VybH1cbiIpCgogICAgIyDnrYnlvoUgTUNQIOWIneWni&#43;WMlgogICAgYXdhaXQgYXN5bmNpby5zbGVlcCgxKQoKICAgICMg6YWN572uIENsYXVkZSDkvb/nlKggTUNQIOe9keWFswogICAgcHJpbnQoIkNvbm5lY3RpbmcgQ2xhdWRlIENMSSB0byBNQ1AgZ2F0ZXdheS4uLiIpCiAgICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgICAgIGYnY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkge21jcF91cmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIge21jcF90b2tlbn0iJywKICAgICAgICB0aW1lb3V0PTAsCiAgICAgICAgb25fc3Rkb3V0PXByaW50LAogICAgICAgIG9uX3N0ZGVycj1wcmludCwKICAgICkKCiAgICBwcmludCgiXG4gQ29ubmVjdGlvbiBzdWNjZXNzZnVsISBDbGVhbmluZyB1cC4uLiIpCiAgICBhd2FpdCBzYngua2lsbCgpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgYXN5bmNpby5ydW4odGVzdF9jb25uZWN0aW9uKCkp', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">os</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">asyncio</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">AsyncSandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">test_connection</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating E2B sandbox with GitHub and SonarQube MCP servers...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;sonarqube&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;org&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_ORG&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;token&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;url&#34;</span><span class="p">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34; Sandbox created successfully!&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;MCP Gateway URL: </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1"># 等待 MCP 初始化</span>
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1"># 配置 Claude 使用 MCP 网关</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Connecting Claude CLI to MCP gateway...&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2"> Connection successful! Cleaning up...&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">    <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">test_connection</span><span class="p">())</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行此脚本以验证您的设置：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cHl0aG9uIDAxX3Rlc3RfY29ubmVjdGlvbi5weQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">python 01_test_connection.py</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


您的输出应类似于以下示例：

```console {collapse=true}
Creating E2B sandbox with GitHub and SonarQube MCP servers...

✓ Sandbox created successfully!
MCP Gateway URL: https://50005-xxxxx.e2b.app/mcp

Connecting Claude CLI to MCP gateway...
Added HTTP MCP server e2b-mcp-gateway with URL: https://50005-xxxxx.e2b.app/mcp to local config
Headers: {
  "Authorization": "Bearer xxxxx-xxxx-xxxx"
}
File modified: /home/user/.claude.json [project: /home/user]

✓ Connection successful! Cleaning up...
```

您刚刚学习了如何创建一个配置了多个 MCP 服务器的 E2B 沙箱。`betaCreate` 方法初始化了一个包含 Claude CLI 和您指定的 MCP 服务器的云环境。

## 步骤 2：发现可用的 MCP 工具

MCP 服务器公开了 Claude 可以调用的工具。GitHub MCP 服务器提供仓库管理工具，而 SonarQube 提供代码分析工具。通过列出它们的工具，您可以知道可以执行哪些操作。

要尝试列出 MCP 工具：








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
      >
        <p>创建 <code>02-list-tools.ts</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiBsaXN0VG9vbHMoKSB7CiAgY29uc29sZS5sb2coIkNyZWF0aW5nIHNhbmRib3guLi5cbiIpOwoKICBjb25zdCBzYnggPSBhd2FpdCBTYW5kYm94LmJldGFDcmVhdGUoewogICAgZW52czogewogICAgICBBTlRIUk9QSUNfQVBJX0tFWTogcHJvY2Vzcy5lbnYuQU5USFJPUElDX0FQSV9LRVkhLAogICAgICBHSVRIVUJfVE9LRU46IHByb2Nlc3MuZW52LkdJVEhVQl9UT0tFTiEsCiAgICAgIFNPTkFSUVVCRV9UT0tFTjogcHJvY2Vzcy5lbnYuU09OQVJRVUJFX1RPS0VOISwKICAgIH0sCiAgICBtY3A6IHsKICAgICAgZ2l0aHViT2ZmaWNpYWw6IHsKICAgICAgICBnaXRodWJQZXJzb25hbEFjY2Vzc1Rva2VuOiBwcm9jZXNzLmVudi5HSVRIVUJfVE9LRU4hLAogICAgICB9LAogICAgICBzb25hcnF1YmU6IHsKICAgICAgICBvcmc6IHByb2Nlc3MuZW52LlNPTkFSUVVCRV9PUkchLAogICAgICAgIHRva2VuOiBwcm9jZXNzLmVudi5TT05BUlFVQkVfVE9LRU4hLAogICAgICAgIHVybDogImh0dHBzOi8vc29uYXJjbG91ZC5pbyIsCiAgICAgIH0sCiAgICB9LAogIH0pOwoKICBjb25zdCBtY3BVcmwgPSBzYnguYmV0YUdldE1jcFVybCgpOwogIGNvbnN0IG1jcFRva2VuID0gYXdhaXQgc2J4LmJldGFHZXRNY3BUb2tlbigpOwoKICAvLyDnrYnlvoUgTUNQIOWIneWni&#43;WMlgogIGF3YWl0IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiBzZXRUaW1lb3V0KHJlc29sdmUsIDEwMDApKTsKCiAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgIGBjbGF1ZGUgbWNwIGFkZCAtLXRyYW5zcG9ydCBodHRwIGUyYi1tY3AtZ2F0ZXdheSAke21jcFVybH0gLS1oZWFkZXIgIkF1dGhvcml6YXRpb246IEJlYXJlciAke21jcFRva2VufSJgLAogICAgeyB0aW1lb3V0TXM6IDAsIG9uU3Rkb3V0OiBjb25zb2xlLmxvZywgb25TdGRlcnI6IGNvbnNvbGUubG9nIH0sCiAgKTsKCiAgY29uc29sZS5sb2coIlxuRGlzY292ZXJpbmcgYXZhaWxhYmxlIE1DUCB0b29scy4uLlxuIik7CgogIGNvbnN0IHByb21wdCA9CiAgICAiTGlzdCBhbGwgTUNQIHRvb2xzIHlvdSBoYXZlIGFjY2VzcyB0by4gRm9yIGVhY2ggdG9vbCwgc2hvdyBpdHMgZXhhY3QgbmFtZSBhbmQgYSBicmllZiBkZXNjcmlwdGlvbi4iOwoKICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgYGVjaG8gJyR7cHJvbXB0fScgfCBjbGF1ZGUgLXAgLS1kYW5nZXJvdXNseS1za2lwLXBlcm1pc3Npb25zYCwKICAgIHsgdGltZW91dE1zOiAwLCBvblN0ZG91dDogY29uc29sZS5sb2csIG9uU3RkZXJyOiBjb25zb2xlLmxvZyB9LAogICk7CgogIGF3YWl0IHNieC5raWxsKCk7Cn0KCmxpc3RUb29scygpLmNhdGNoKGNvbnNvbGUuZXJyb3IpOw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">import</span> <span class="s2">&#34;dotenv/config&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">Sandbox</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;e2b&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">listTools() {</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">GITHUB_TOKEN</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">SONARQUBE_TOKEN</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nx">sonarqube</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">org</span>: <span class="kt">process.env.SONARQUBE_ORG</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">token</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">url</span><span class="o">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="c1">// 等待 MCP 初始化
</span></span></span><span class="line"><span class="cl"><span class="c1"></span>  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">1000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span> <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span> <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span> <span class="nx">onStderr</span>: <span class="kt">console.log</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nDiscovering available MCP tools...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span>
</span></span><span class="line"><span class="cl">    <span class="s2">&#34;List all MCP tools you have access to. For each tool, show its exact name and a brief description.&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`echo &#39;</span><span class="si">${</span><span class="nx">prompt</span><span class="si">}</span><span class="sb">&#39; | claude -p --dangerously-skip-permissions`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span> <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span> <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span> <span class="nx">onStderr</span>: <span class="kt">console.log</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">listTools</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bnB4IHRzeCAwMi1saXN0LXRvb2xzLnRz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">npx tsx 02-list-tools.ts</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>创建 <code>02_list_tools.py</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmZyb20gZG90ZW52IGltcG9ydCBsb2FkX2RvdGVudgpmcm9tIGUyYiBpbXBvcnQgQXN5bmNTYW5kYm94Cgpsb2FkX2RvdGVudigpCgphc3luYyBkZWYgbGlzdF90b29scygpOgogICAgcHJpbnQoIkNyZWF0aW5nIHNhbmRib3guLi5cbiIpCgogICAgc2J4ID0gYXdhaXQgQXN5bmNTYW5kYm94LmJldGFfY3JlYXRlKAogICAgICAgIGVudnM9ewogICAgICAgICAgICAiQU5USFJPUElDX0FQSV9LRVkiOiBvcy5nZXRlbnYoIkFOVEhST1BJQ19BUElfS0VZIiksCiAgICAgICAgICAgICJHSVRIVUJfVE9LRU4iOiBvcy5nZXRlbnYoIkdJVEhVQl9UT0tFTiIpLAogICAgICAgICAgICAiU09OQVJRVUJFX1RPS0VOIjogb3MuZ2V0ZW52KCJTT05BUlFVQkVfVE9LRU4iKSwKICAgICAgICB9LAogICAgICAgIG1jcD17CiAgICAgICAgICAgICJnaXRodWJPZmZpY2lhbCI6IHsKICAgICAgICAgICAgICAgICJnaXRodWJQZXJzb25hbEFjY2Vzc1Rva2VuIjogb3MuZ2V0ZW52KCJHSVRIVUJfVE9LRU4iKSwKICAgICAgICAgICAgfSwKICAgICAgICAgICAgInNvbmFycXViZSI6IHsKICAgICAgICAgICAgICAgICJvcmciOiBvcy5nZXRlbnYoIlNPTkFSUVVCRV9PUkciKSwKICAgICAgICAgICAgICAgICJ0b2tlbiI6IG9zLmdldGVudigiU09OQVJRVUJFX1RPS0VOIiksCiAgICAgICAgICAgICAgICAidXJsIjogImh0dHBzOi8vc29uYXJjbG91ZC5pbyIsCiAgICAgICAgICAgIH0sCiAgICAgICAgfSwKICAgICkKCiAgICBtY3BfdXJsID0gc2J4LmJldGFfZ2V0X21jcF91cmwoKQogICAgbWNwX3Rva2VuID0gYXdhaXQgc2J4LmJldGFfZ2V0X21jcF90b2tlbigpCgogICAgIyDnrYnlvoUgTUNQIOWIneWni&#43;WMlgogICAgYXdhaXQgYXN5bmNpby5zbGVlcCgxKQoKICAgIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICAgICAgZidjbGF1ZGUgbWNwIGFkZCAtLXRyYW5zcG9ydCBodHRwIGUyYi1tY3AtZ2F0ZXdheSB7bWNwX3VybH0gLS1oZWFkZXIgIkF1dGhvcml6YXRpb246IEJlYXJlciB7bWNwX3Rva2VufSInLAogICAgICAgIHRpbWVvdXQ9MCwKICAgICAgICBvbl9zdGRvdXQ9cHJpbnQsCiAgICAgICAgb25fc3RkZXJyPXByaW50LAogICAgKQoKICAgIHByaW50KCJcbkRpc2NvdmVyaW5nIGF2YWlsYWJsZSBNQ1AgdG9vbHMuLi5cbiIpCgogICAgcHJvbXB0ID0gIkxpc3QgYWxsIE1DUCB0b29scyB5b3UgaGF2ZSBhY2Nlc3MgdG8uIEZvciBlYWNoIHRvb2wsIHNob3cgaXRzIGV4YWN0IG5hbWUgYW5kIGEgYnJpZWYgZGVzY3JpcHRpb24uIgoKICAgIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICAgICAgZiJlY2hvICd7cHJvbXB0fScgfCBjbGF1ZGUgLXAgLS1kYW5nZXJvdXNseS1za2lwLXBlcm1pc3Npb25zIiwKICAgICAgICB0aW1lb3V0PTAsCiAgICAgICAgb25fc3Rkb3V0PXByaW50LAogICAgICAgIG9uX3N0ZGVycj1wcmludCwKICAgICkKCiAgICBhd2FpdCBzYngua2lsbCgpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgYXN5bmNpby5ydW4obGlzdF90b29scygpKQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">os</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">asyncio</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">AsyncSandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">list_tools</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;sonarqube&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;org&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_ORG&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;token&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;url&#34;</span><span class="p">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1"># 等待 MCP 初始化</span>
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Discovering available MCP tools...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">prompt</span> <span class="o">=</span> <span class="s2">&#34;List all MCP tools you have access to. For each tool, show its exact name and a brief description.&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s2">&#34;echo &#39;</span><span class="si">{</span><span class="n">prompt</span><span class="si">}</span><span class="s2">&#39; | claude -p --dangerously-skip-permissions&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">    <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">list_tools</span><span class="p">())</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cHl0aG9uIDAyX2xpc3RfdG9vbHMucHk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">python 02_list_tools.py</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


在控制台中，您应该会看到一个 MCP 工具列表：

```console {collapse=true}
Creating sandbox...

Sandbox created
Connecting to MCP gateway...

Discovering available MCP tools...

I have access to the following MCP tools:

**GitHub Tools:**
1. mcp__create_repository - Create a new GitHub repository
2. mcp__list_issues - List issues in a repository
3. mcp__create_issue - Create a new issue
4. mcp__get_file_contents - Get file contents from a repository
5. mcp__create_or_update_file - Create or update files in a repository
6. mcp__create_pull_request - Create a pull request
7. mcp__create_branch - Create a new branch
8. mcp__push_files - Push multiple files in a single commit
... (30+ more GitHub tools)

**SonarQube Tools:**
1. mcp__get_projects - List projects in organization
2. mcp__get_quality_gate_status - Get quality gate status for a project
3. mcp__list_project_issues - List quality issues in a project
4. mcp__search_issues - Search for specific quality issues
... (SonarQube analysis tools)
```

## 步骤 3：测试 GitHub MCP 工具

让我们尝试使用 MCP 工具测试 GitHub。从列出仓库问题开始。








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
      >
        <p>创建 <code>03-test-github.ts</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiB0ZXN0R2l0SHViKCkgewogIGNvbnNvbGUubG9nKCJDcmVhdGluZyBzYW5kYm94Li4uXG4iKTsKCiAgY29uc3Qgc2J4ID0gYXdhaXQgU2FuZGJveC5iZXRhQ3JlYXRlKHsKICAgIGVudnM6IHsKICAgICAgQU5USFJPUElDX0FQSV9LRVk6IHByb2Nlc3MuZW52LkFOVEhST1BJQ19BUElfS0VZISwKICAgICAgR0lUSFVCX1RPS0VOOiBwcm9jZXNzLmVudi5HSVRIVUJfVE9LRU4hLAogICAgfSwKICAgIG1jcDogewogICAgICBnaXRodWJPZmZpY2lhbDogewogICAgICAgIGdpdGh1YlBlcnNvbmFsQWNjZXNzVG9rZW46IHByb2Nlc3MuZW52LkdJVEhVQl9UT0tFTiEsCiAgICAgIH0sCiAgICB9LAogIH0pOwoKICBjb25zdCBtY3BVcmwgPSBzYnguYmV0YUdldE1jcFVybCgpOwogIGNvbnN0IG1jcFRva2VuID0gYXdhaXQgc2J4LmJldGFHZXRNY3BUb2tlbigpOwoKICBhd2FpdCBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4gc2V0VGltZW91dChyZXNvbHZlLCAxMDAwKSk7CgogIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICBgY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkgJHttY3BVcmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIgJHttY3BUb2tlbn0iYCwKICAgIHsgdGltZW91dE1zOiAwLCBvblN0ZG91dDogY29uc29sZS5sb2csIG9uU3RkZXJyOiBjb25zb2xlLmxvZyB9LAogICk7CgogIGNvbnN0IHJlcG9QYXRoID0gYCR7cHJvY2Vzcy5lbnYuR0lUSFVCX09XTkVSfS8ke3Byb2Nlc3MuZW52LkdJVEhVQl9SRVBPfWA7CgogIGNvbnNvbGUubG9nKGBcbkxpc3RpbmcgaXNzdWVzIGluICR7cmVwb1BhdGh9Li4uXG5gKTsKCiAgY29uc3QgcHJvbXB0ID0gYFVzaW5nIHRoZSBHaXRIdWIgTUNQIHRvb2xzLCBsaXN0IGFsbCBvcGVuIGlzc3VlcyBpbiB0aGUgcmVwb3NpdG9yeSAiJHtyZXBvUGF0aH0iLiBTaG93IHRoZSBpc3N1ZSBudW1iZXIsIHRpdGxlLCBhbmQgYXV0aG9yIGZvciBlYWNoLmA7CgogIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICBgZWNobyAnJHtwcm9tcHQucmVwbGFjZSgvJy9nLCAiJ1xcJyciKX0nIHwgY2xhdWRlIC1wIC0tZGFuZ2Vyb3VzbHktc2tpcC1wZXJtaXNzaW9uc2AsCiAgICB7CiAgICAgIHRpbWVvdXRNczogMCwKICAgICAgb25TdGRvdXQ6IGNvbnNvbGUubG9nLAogICAgICBvblN0ZGVycjogY29uc29sZS5sb2csCiAgICB9LAogICk7CgogIGF3YWl0IHNieC5raWxsKCk7Cn0KCnRlc3RHaXRIdWIoKS5jYXRjaChjb25zb2xlLmVycm9yKTs=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">import</span> <span class="s2">&#34;dotenv/config&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">Sandbox</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;e2b&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">testGitHub() {</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">GITHUB_TOKEN</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">1000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span> <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span> <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span> <span class="nx">onStderr</span>: <span class="kt">console.log</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">repoPath</span> <span class="o">=</span> <span class="sb">`</span><span class="si">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">GITHUB_OWNER</span><span class="si">}</span><span class="sb">/</span><span class="si">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">GITHUB_REPO</span><span class="si">}</span><span class="sb">`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="sb">`</span><span class="err">\</span><span class="sb">nListing issues in </span><span class="si">${</span><span class="nx">repoPath</span><span class="si">}</span><span class="sb">...</span><span class="err">\</span><span class="sb">n`</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span> <span class="sb">`Using the GitHub MCP tools, list all open issues in the repository &#34;</span><span class="si">${</span><span class="nx">repoPath</span><span class="si">}</span><span class="sb">&#34;. Show the issue number, title, and author for each.`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`echo &#39;</span><span class="si">${</span><span class="nx">prompt</span><span class="p">.</span><span class="nx">replace</span><span class="p">(</span><span class="sr">/&#39;/g</span><span class="p">,</span> <span class="s2">&#34;&#39;\\&#39;&#39;&#34;</span><span class="p">)</span><span class="si">}</span><span class="sb">&#39; | claude -p --dangerously-skip-permissions`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">testGitHub</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bnB4IHRzeCAwMy10ZXN0LWdpdGh1Yi50cw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">npx tsx 03-test-github.ts</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>创建 <code>03_test_github.py</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmZyb20gZG90ZW52IGltcG9ydCBsb2FkX2RvdGVudgpmcm9tIGUyYiBpbXBvcnQgQXN5bmNTYW5kYm94Cgpsb2FkX2RvdGVudigpCgphc3luYyBkZWYgdGVzdF9naXRodWIoKToKICAgIHByaW50KCJDcmVhdGluZyBzYW5kYm94Li4uXG4iKQoKICAgIHNieCA9IGF3YWl0IEFzeW5jU2FuZGJveC5iZXRhX2NyZWF0ZSgKICAgICAgICBlbnZzPXsKICAgICAgICAgICAgIkFOVEhST1BJQ19BUElfS0VZIjogb3MuZ2V0ZW52KCJBTlRIUk9QSUNfQVBJX0tFWSIpLAogICAgICAgICAgICAiR0lUSFVCX1RPS0VOIjogb3MuZ2V0ZW52KCJHSVRIVUJfVE9LRU4iKSwKICAgICAgICB9LAogICAgICAgIG1jcD17CiAgICAgICAgICAgICJnaXRodWJPZmZpY2lhbCI6IHsKICAgICAgICAgICAgICAgICJnaXRodWJQZXJzb25hbEFjY2Vzc1Rva2VuIjogb3MuZ2V0ZW52KCJHSVRIVUJfVE9LRU4iKSwKICAgICAgICAgICAgfSwKICAgICAgICB9LAogICAgKQoKICAgIG1jcF91cmwgPSBzYnguYmV0YV9nZXRfbWNwX3VybCgpCiAgICBtY3BfdG9rZW4gPSBhd2FpdCBzYnguYmV0YV9nZXRfbWNwX3Rva2VuKCkKCiAgICBhd2FpdCBhc3luY2lvLnNsZWVwKDEpCgogICAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgICAgICBmJ2NsYXVkZSBtY3AgYWRkIC0tdHJhbnNwb3J0IGh0dHAgZTJiLW1jcC1nYXRld2F5IHttY3BfdXJsfSAtLWhlYWRlciAiQXV0aG9yaXphdGlvbjogQmVhcmVyIHttY3BfdG9rZW59IicsCiAgICAgICAgdGltZW91dD0wLAogICAgICAgIG9uX3N0ZG91dD1wcmludCwKICAgICAgICBvbl9zdGRlcnI9cHJpbnQsCiAgICApCgogICAgcmVwb19wYXRoID0gZiJ7b3MuZ2V0ZW52KCdHSVRIVUJfT1dORVInKX0ve29zLmdldGVudignR0lUSFVCX1JFUE8nKX0iCgogICAgcHJpbnQoZiJcbkxpc3RpbmcgaXNzdWVzIGluIHtyZXBvX3BhdGh9Li4uXG4iKQoKICAgIHByb21wdCA9IGYnVXNpbmcgdGhlIEdpdEh1YiBNQ1AgdG9vbHMsIGxpc3QgYWxsIG9wZW4gaXNzdWVzIGluIHRoZSByZXBvc2l0b3J5ICJ7cmVwb19wYXRofSIuIFNob3cgdGhlIGlzc3VlIG51bWJlciwgdGl0bGUsIGFuZCBhdXRob3IgZm9yIGVhY2guJwoKICAgIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICAgICAgZiJlY2hvICd7cHJvbXB0fScgfCBjbGF1ZGUgLXAgLS1kYW5nZXJvdXNseS1za2lwLXBlcm1pc3Npb25zIiwKICAgICAgICB0aW1lb3V0PTAsCiAgICAgICAgb25fc3Rkb3V0PXByaW50LAogICAgICAgIG9uX3N0ZGVycj1wcmludCwKICAgICkKCiAgICBhd2FpdCBzYngua2lsbCgpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgYXN5bmNpby5ydW4odGVzdF9naXRodWIoKSk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">os</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">asyncio</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">AsyncSandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">test_github</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">repo_path</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;</span><span class="si">{</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">&#39;GITHUB_OWNER&#39;</span><span class="p">)</span><span class="si">}</span><span class="s2">/</span><span class="si">{</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">&#39;GITHUB_REPO&#39;</span><span class="p">)</span><span class="si">}</span><span class="s2">&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Listing issues in </span><span class="si">{</span><span class="n">repo_path</span><span class="si">}</span><span class="s2">...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">prompt</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">&#39;Using the GitHub MCP tools, list all open issues in the repository &#34;</span><span class="si">{</span><span class="n">repo_path</span><span class="si">}</span><span class="s1">&#34;. Show the issue number, title, and author for each.&#39;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s2">&#34;echo &#39;</span><span class="si">{</span><span class="n">prompt</span><span class="si">}</span><span class="s2">&#39; | claude -p --dangerously-skip-permissions&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">    <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">test_github</span><span class="p">())</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cHl0aG9uIDAzX3Rlc3RfZ2l0aHViLnB5', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">python 03_test_github.py</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


您应该会看到 Claude 使用 GitHub MCP 工具列出您仓库的问题：

```console {collapse=true}
Creating sandbox...
Connecting to MCP gateway...

Listing issues in <your-repo>...

Here are the first 10 open issues in the <your-repo> repository:

1. **Issue #23577**: Update README (author: user1)
2. **Issue #23575**: release-notes for Compose v2.40.1 version (author: user2)
3. **Issue #23570**: engine-cli: fix `docker volume prune` output (author: user3)
4. **Issue #23568**: Engdocs update (author: user4)
5. **Issue #23565**: add new section (author: user5)
... (continues with more issues)
```

您现在可以向 Claude 发送提示，并通过自然语言与 GitHub 交互。Claude 根据您的提示决定调用什么工具。

## 步骤 4：测试 SonarQube MCP 工具

让我们使用 SonarQube MCP 工具分析代码质量。








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
      >
        <p>创建 <code>04-test-sonarqube.ts</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiB0ZXN0U29uYXJRdWJlKCkgewogIGNvbnNvbGUubG9nKCJDcmVhdGluZyBzYW5kYm94Li4uXG4iKTsKCiAgY29uc3Qgc2J4ID0gYXdhaXQgU2FuZGJveC5iZXRhQ3JlYXRlKHsKICAgIGVudnM6IHsKICAgICAgQU5USFJPUElDX0FQSV9LRVk6IHByb2Nlc3MuZW52LkFOVEhST1BJQ19BUElfS0VZISwKICAgICAgR0lUSFVCX1RPS0VOOiBwcm9jZXNzLmVudi5HSVRIVUJfVE9LRU4hLAogICAgICBTT05BUlFVQkVfVE9LRU46IHByb2Nlc3MuZW52LlNPTkFSUVVCRV9UT0tFTiEsCiAgICB9LAogICAgbWNwOiB7CiAgICAgIGdpdGh1Yk9mZmljaWFsOiB7CiAgICAgICAgZ2l0aHViUGVyc29uYWxBY2Nlc3NUb2tlbjogcHJvY2Vzcy5lbnYuR0lUSFVCX1RPS0VOISwKICAgICAgfSwKICAgICAgc29uYXJxdWJlOiB7CiAgICAgICAgb3JnOiBwcm9jZXNzLmVudi5TT05BUlFVQkVfT1JHISwKICAgICAgICB0b2tlbjogcHJvY2Vzcy5lbnYuU09OQVJRVUJFX1RPS0VOISwKICAgICAgICB1cmw6ICJodHRwczovL3NvbmFyY2xvdWQuaW8iLAogICAgICB9LAogICAgfSwKICB9KTsKCiAgY29uc3QgbWNwVXJsID0gc2J4LmJldGFHZXRNY3BVcmwoKTsKICBjb25zdCBtY3BUb2tlbiA9IGF3YWl0IHNieC5iZXRhR2V0TWNwVG9rZW4oKTsKCiAgYXdhaXQgbmV3IFByb21pc2UoKHJlc29sdmUpID0&#43;IHNldFRpbWVvdXQocmVzb2x2ZSwgMTAwMCkpOwoKICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgYGNsYXVkZSBtY3AgYWRkIC0tdHJhbnNwb3J0IGh0dHAgZTJiLW1jcC1nYXRld2F5ICR7bWNwVXJsfSAtLWhlYWRlciAiQXV0aG9yaXphdGlvbjogQmVhcmVyICR7bWNwVG9rZW59ImAsCiAgICB7IHRpbWVvdXRNczogMCwgb25TdGRvdXQ6IGNvbnNvbGUubG9nLCBvblN0ZGVycjogY29uc29sZS5sb2cgfSwKICApOwoKICBjb25zb2xlLmxvZygiXG5BbmFseXppbmcgY29kZSBxdWFsaXR5IHdpdGggU29uYXJRdWJlLi4uXG4iKTsKCiAgY29uc3QgcHJvbXB0ID0gYFVzaW5nIHRoZSBTb25hclF1YmUgTUNQIHRvb2xzOgogICAgMS4gTGlzdCBhbGwgcHJvamVjdHMgaW4gbXkgb3JnYW5pemF0aW9uCiAgICAyLiBGb3IgdGhlIGZpcnN0IHByb2plY3QsIHNob3c6CiAgICAtIFF1YWxpdHkgZ2F0ZSBzdGF0dXMgKHBhc3MvZmFpbCkKICAgIC0gTnVtYmVyIG9mIGJ1Z3MKICAgIC0gTnVtYmVyIG9mIGNvZGUgc21lbGxzCiAgICAtIE51bWJlciBvZiBzZWN1cml0eSB2dWxuZXJhYmlsaXRpZXMKICAgIDMuIExpc3QgdGhlIHRvcCA1IG1vc3QgY3JpdGljYWwgaXNzdWVzIGZvdW5kYDsKCiAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgIGBlY2hvICcke3Byb21wdC5yZXBsYWNlKC8nL2csICInXFwnJyIpfScgfCBjbGF1ZGUgLXAgLS1kYW5nZXJvdXNseS1za2lwLXBlcm1pc3Npb25zYCwKICAgIHsKICAgICAgdGltZW91dE1zOiAwLAogICAgICBvblN0ZG91dDogY29uc29sZS5sb2csCiAgICAgIG9uU3RkZXJyOiBjb25zb2xlLmxvZywKICAgIH0sCiAgKTsKCiAgYXdhaXQgc2J4LmtpbGwoKTsKfQoKdGVzdFNvbmFyUXViZSgpLmNhdGNoKGNvbnNvbGUuZXJyb3IpOw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">import</span> <span class="s2">&#34;dotenv/config&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">Sandbox</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;e2b&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">testSonarQube() {</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">GITHUB_TOKEN</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">SONARQUBE_TOKEN</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nx">sonarqube</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">org</span>: <span class="kt">process.env.SONARQUBE_ORG</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">token</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">url</span><span class="o">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">1000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span> <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span> <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span> <span class="nx">onStderr</span>: <span class="kt">console.log</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nAnalyzing code quality with SonarQube...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span> <span class="sb">`Using the SonarQube MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="sb">    1. List all projects in my organization
</span></span></span><span class="line"><span class="cl"><span class="sb">    2. For the first project, show:
</span></span></span><span class="line"><span class="cl"><span class="sb">    - Quality gate status (pass/fail)
</span></span></span><span class="line"><span class="cl"><span class="sb">    - Number of bugs
</span></span></span><span class="line"><span class="cl"><span class="sb">    - Number of code smells
</span></span></span><span class="line"><span class="cl"><span class="sb">    - Number of security vulnerabilities
</span></span></span><span class="line"><span class="cl"><span class="sb">    3. List the top 5 most critical issues found`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`echo &#39;</span><span class="si">${</span><span class="nx">prompt</span><span class="p">.</span><span class="nx">replace</span><span class="p">(</span><span class="sr">/&#39;/g</span><span class="p">,</span> <span class="s2">&#34;&#39;\\&#39;&#39;&#34;</span><span class="p">)</span><span class="si">}</span><span class="sb">&#39; | claude -p --dangerously-skip-permissions`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">testSonarQube</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bnB4IHRzeCAwNC10ZXN0LXNvbmFycXViZS50cw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">npx tsx 04-test-sonarqube.ts</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>创建 <code>04_test_sonarqube.py</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmZyb20gZG90ZW52IGltcG9ydCBsb2FkX2RvdGVudgpmcm9tIGUyYiBpbXBvcnQgQXN5bmNTYW5kYm94Cgpsb2FkX2RvdGVudigpCgphc3luYyBkZWYgdGVzdF9zb25hcnF1YmUoKToKICAgIHByaW50KCJDcmVhdGluZyBzYW5kYm94Li4uXG4iKQoKICAgIHNieCA9IGF3YWl0IEFzeW5jU2FuZGJveC5iZXRhX2NyZWF0ZSgKICAgICAgICBlbnZzPXsKICAgICAgICAgICAgIkFOVEhST1BJQ19BUElfS0VZIjogb3MuZ2V0ZW52KCJBTlRIUk9QSUNfQVBJX0tFWSIpLAogICAgICAgICAgICAiR0lUSFVCX1RPS0VOIjogb3MuZ2V0ZW52KCJHSVRIVUJfVE9LRU4iKSwKICAgICAgICAgICAgIlNPTkFSUVVCRV9UT0tFTiI6IG9zLmdldGVudigiU09OQVJRVUJFX1RPS0VOIiksCiAgICAgICAgfSwKICAgICAgICBtY3A9ewogICAgICAgICAgICAiZ2l0aHViT2ZmaWNpYWwiOiB7CiAgICAgICAgICAgICAgICAiZ2l0aHViUGVyc29uYWxBY2Nlc3NUb2tlbiI6IG9zLmdldGVudigiR0lUSFVCX1RPS0VOIiksCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJzb25hcnF1YmUiOiB7CiAgICAgICAgICAgICAgICAib3JnIjogb3MuZ2V0ZW52KCJTT05BUlFVQkVfT1JHIiksCiAgICAgICAgICAgICAgICAidG9rZW4iOiBvcy5nZXRlbnYoIlNPTkFSUVVCRV9UT0tFTiIpLAogICAgICAgICAgICAgICAgInVybCI6ICJodHRwczovL3NvbmFyY2xvdWQuaW8iLAogICAgICAgICAgICB9LAogICAgICAgIH0sCiAgICApCgogICAgbWNwX3VybCA9IHNieC5iZXRhX2dldF9tY3BfdXJsKCkKICAgIG1jcF90b2tlbiA9IGF3YWl0IHNieC5iZXRhX2dldF9tY3BfdG9rZW4oKQoKICAgIGF3YWl0IGFzeW5jaW8uc2xlZXAoMSkKCiAgICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgICAgIGYnY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkge21jcF91cmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIge21jcF90b2tlbn0iJywKICAgICAgICB0aW1lb3V0PTAsCiAgICAgICAgb25fc3Rkb3V0PXByaW50LAogICAgICAgIG9uX3N0ZGVycj1wcmludCwKICAgICkKCiAgICBwcmludCgiXG5BbmFseXppbmcgY29kZSBxdWFsaXR5IHdpdGggU29uYXJRdWJlLi4uXG4iKQoKICAgIHByb21wdCA9ICIiIlVzaW5nIHRoZSBTb25hclF1YmUgTUNQIHRvb2xzOgogICAgMS4gTGlzdCBhbGwgcHJvamVjdHMgaW4gbXkgb3JnYW5pemF0aW9uCiAgICAyLiBGb3IgdGhlIGZpcnN0IHByb2plY3QsIHNob3c6CiAgICAtIFF1YWxpdHkgZ2F0ZSBzdGF0dXMgKHBhc3MvZmFpbCkKICAgIC0gTnVtYmVyIG9mIGJ1Z3MKICAgIC0gTnVtYmVyIG9mIGNvZGUgc21lbGxzCiAgICAtIE51bWJlciBvZiBzZWN1cml0eSB2dWxuZXJhYmlsaXRpZXMKICAgIDMuIExpc3QgdGhlIHRvcCA1IG1vc3QgY3JpdGljYWwgaXNzdWVzIGZvdW5kIiIiCgogICAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgICAgICBmImVjaG8gJ3twcm9tcHR9JyB8IGNsYXVkZSAtcCAtLWRhbmdlcm91c2x5LXNraXAtcGVybWlzc2lvbnMiLAogICAgICAgIHRpbWVvdXQ9MCwKICAgICAgICBvbl9zdGRvdXQ9cHJpbnQsCiAgICAgICAgb25fc3RkZXJyPXByaW50LAogICAgKQoKICAgIGF3YWl0IHNieC5raWxsKCkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICBhc3luY2lvLnJ1bih0ZXN0X3NvbmFycXViZSgpKQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">os</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">asyncio</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">AsyncSandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">test_sonarqube</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;sonarqube&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;org&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_ORG&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;token&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;url&#34;</span><span class="p">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Analyzing code quality with SonarQube...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">prompt</span> <span class="o">=</span> <span class="s2">&#34;&#34;&#34;Using the SonarQube MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="s2">    1. List all projects in my organization
</span></span></span><span class="line"><span class="cl"><span class="s2">    2. For the first project, show:
</span></span></span><span class="line"><span class="cl"><span class="s2">    - Quality gate status (pass/fail)
</span></span></span><span class="line"><span class="cl"><span class="s2">    - Number of bugs
</span></span></span><span class="line"><span class="cl"><span class="s2">    - Number of code smells
</span></span></span><span class="line"><span class="cl"><span class="s2">    - Number of security vulnerabilities
</span></span></span><span class="line"><span class="cl"><span class="s2">    3. List the top 5 most critical issues found&#34;&#34;&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s2">&#34;echo &#39;</span><span class="si">{</span><span class="n">prompt</span><span class="si">}</span><span class="s2">&#39; | claude -p --dangerously-skip-permissions&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">    <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">test_sonarqube</span><span class="p">())</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cHl0aG9uIDA0X3Rlc3Rfc29uYXJxdWJlLnB5', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">python 04_test_sonarqube.py</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


> [!NOTE]
>
> 此脚本可能需要几分钟才能运行。

您应该会看到 Claude 输出 SonarQube 分析结果：

```console {collapse=true}
Creating sandbox...

Analyzing code quality with SonarQube...

## SonarQube Analysis Results

### 1. Projects in Your Organization

Found **1 project**:
- **Project Name**: project-1
- **Project Key**: project-testing

### 2. Project Analysis

...

### 3. Top 5 Most Critical Issues

Found 1 total issues (all are code smells with no critical/blocker severity):

1. **MAJOR Severity** - test.js:2
   - **Rule**: javascript:S1854
   - **Message**: Remove this useless assignment to variable "unusedVariable"
   - **Status**: OPEN

**Summary**: The project is in good health with no bugs or vulnerabilities detected.
```

您现在可以通过自然语言使用 SonarQube MCP 工具分析代码质量。您可以检索质量指标、识别问题，并了解哪些代码需要修复。

## 步骤 5：创建分支并进行代码更改

现在，让我们教 Claude 根据 SonarQube 发现的质量问题来修复代码。








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
      >
        <p>创建 <code>05-fix-code-issue.ts</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiBmaXhDb2RlSXNzdWUoKSB7CiAgY29uc29sZS5sb2coIkNyZWF0aW5nIHNhbmRib3guLi5cbiIpOwoKICBjb25zdCBzYnggPSBhd2FpdCBTYW5kYm94LmJldGFDcmVhdGUoewogICAgZW52czogewogICAgICBBTlRIUk9QSUNfQVBJX0tFWTogcHJvY2Vzcy5lbnYuQU5USFJPUElDX0FQSV9LRVkhLAogICAgICBHSVRIVUJfVE9LRU46IHByb2Nlc3MuZW52LkdJVEhVQl9UT0tFTiEsCiAgICAgIFNPTkFSUVVCRV9UT0tFTjogcHJvY2Vzcy5lbnYuU09OQVJRVUJFX1RPS0VOISwKICAgIH0sCiAgICBtY3A6IHsKICAgICAgZ2l0aHViT2ZmaWNpYWw6IHsKICAgICAgICBnaXRodWJQZXJzb25hbEFjY2Vzc1Rva2VuOiBwcm9jZXNzLmVudi5HSVRIVUJfVE9LRU4hLAogICAgICB9LAogICAgICBzb25hcnF1YmU6IHsKICAgICAgICBvcmc6IHByb2Nlc3MuZW52LlNPTkFSUVVCRV9PUkchLAogICAgICAgIHRva2VuOiBwcm9jZXNzLmVudi5TT05BUlFVQkVfVE9LRU4hLAogICAgICAgIHVybDogImh0dHBzOi8vc29uYXJjbG91ZC5pbyIsCiAgICAgIH0sCiAgICB9LAogIH0pOwoKICBjb25zdCBtY3BVcmwgPSBzYnguYmV0YUdldE1jcFVybCgpOwogIGNvbnN0IG1jcFRva2VuID0gYXdhaXQgc2J4LmJldGFHZXRNY3BUb2tlbigpOwoKICBhd2FpdCBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4gc2V0VGltZW91dChyZXNvbHZlLCAxMDAwKSk7CgogIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICBgY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkgJHttY3BVcmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIgJHttY3BUb2tlbn0iYCwKICAgIHsgdGltZW91dE1zOiAwLCBvblN0ZG91dDogY29uc29sZS5sb2csIG9uU3RkZXJyOiBjb25zb2xlLmxvZyB9LAogICk7CgogIGNvbnN0IHJlcG9QYXRoID0gYCR7cHJvY2Vzcy5lbnYuR0lUSFVCX09XTkVSfS8ke3Byb2Nlc3MuZW52LkdJVEhVQl9SRVBPfWA7CiAgY29uc3QgYnJhbmNoTmFtZSA9IGBxdWFsaXR5LWZpeC0ke0RhdGUubm93KCl9YDsKCiAgY29uc29sZS5sb2coIlxuRml4aW5nIGEgY29kZSBxdWFsaXR5IGlzc3VlLi4uXG4iKTsKCiAgY29uc3QgcHJvbXB0ID0gYFVzaW5nIEdpdEh1YiBhbmQgU29uYXJRdWJlIE1DUCB0b29sczoKCiAgICAxLiBBbmFseXplIGNvZGUgcXVhbGl0eSBpbiByZXBvc2l0b3J5ICIke3JlcG9QYXRofSIgd2l0aCBTb25hclF1YmUKICAgIDIuIEZpbmQgT05FIHNpbXBsZSBpc3N1ZSB0aGF0IGNhbiBiZSBjb25maWRlbnRseSBmaXhlZCAobGlrZSBhbiB1bnVzZWQgdmFyaWFibGUgb3IgY29kZSBzbWVsbCkKICAgIDMuIENyZWF0ZSBhIG5ldyBicmFuY2ggY2FsbGVkICIke2JyYW5jaE5hbWV9IgogICAgNC4gUmVhZCB0aGUgZmlsZSBjb250YWluaW5nIHRoZSBpc3N1ZSB1c2luZyBHaXRIdWIgdG9vbHMKICAgIDUuIEZpeCB0aGUgaXNzdWUgaW4gdGhlIGNvZGUKICAgIDYuIENvbW1pdCB0aGUgZml4IHRvIHRoZSBuZXcgYnJhbmNoIHdpdGggYSBjbGVhciBjb21taXQgbWVzc2FnZQoKICAgIEltcG9ydGFudDogT25seSBmaXggaXNzdWVzIHlvdSdyZSAxMDAlIGNvbmZpZGVudCBhYm91dC4gRXhwbGFpbiB3aGF0IHlvdSdyZSBmaXhpbmcgYW5kIHdoeS5gOwoKICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgYGVjaG8gJyR7cHJvbXB0LnJlcGxhY2UoLycvZywgIidcXCcnIil9JyB8IGNsYXVkZSAtcCAtLWRhbmdlcm91c2x5LXNraXAtcGVybWlzc2lvbnNgLAogICAgewogICAgICB0aW1lb3V0TXM6IDAsCiAgICAgIG9uU3Rkb3V0OiBjb25zb2xlLmxvZywKICAgICAgb25TdGRlcnI6IGNvbnNvbGUubG9nLAogICAgfSwKICApOwoKICBjb25zb2xlLmxvZyhgXG7CnENoZWNrIHlvdXIgcmVwb3NpdG9yeSBmb3IgYnJhbmNoOiAke2JyYW5jaE5hbWV9YCk7CgogIGF3YWl0IHNieC5raWxsKCk7Cn0KCmZpeENvZGVJc3N1ZSgpLmNhdGNoKGNvbnNvbGUuZXJyb3IpOw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">import</span> <span class="s2">&#34;dotenv/config&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">Sandbox</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;e2b&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">fixCodeIssue() {</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">GITHUB_TOKEN</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">SONARQUBE_TOKEN</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nx">sonarqube</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">org</span>: <span class="kt">process.env.SONARQUBE_ORG</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">token</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">url</span><span class="o">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">1000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span> <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span> <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span> <span class="nx">onStderr</span>: <span class="kt">console.log</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">repoPath</span> <span class="o">=</span> <span class="sb">`</span><span class="si">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">GITHUB_OWNER</span><span class="si">}</span><span class="sb">/</span><span class="si">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">GITHUB_REPO</span><span class="si">}</span><span class="sb">`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">branchName</span> <span class="o">=</span> <span class="sb">`quality-fix-</span><span class="si">${</span><span class="nb">Date</span><span class="p">.</span><span class="nx">now</span><span class="p">()</span><span class="si">}</span><span class="sb">`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nFixing a code quality issue...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span> <span class="sb">`Using GitHub and SonarQube MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">    1. Analyze code quality in repository &#34;</span><span class="si">${</span><span class="nx">repoPath</span><span class="si">}</span><span class="sb">&#34; with SonarQube
</span></span></span><span class="line"><span class="cl"><span class="sb">    2. Find ONE simple issue that can be confidently fixed (like an unused variable or code smell)
</span></span></span><span class="line"><span class="cl"><span class="sb">    3. Create a new branch called &#34;</span><span class="si">${</span><span class="nx">branchName</span><span class="si">}</span><span class="sb">&#34;
</span></span></span><span class="line"><span class="cl"><span class="sb">    4. Read the file containing the issue using GitHub tools
</span></span></span><span class="line"><span class="cl"><span class="sb">    5. Fix the issue in the code
</span></span></span><span class="line"><span class="cl"><span class="sb">    6. Commit the fix to the new branch with a clear commit message
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">    Important: Only fix issues you&#39;re 100% confident about. Explain what you&#39;re fixing and why.`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`echo &#39;</span><span class="si">${</span><span class="nx">prompt</span><span class="p">.</span><span class="nx">replace</span><span class="p">(</span><span class="sr">/&#39;/g</span><span class="p">,</span> <span class="s2">&#34;&#39;\\&#39;&#39;&#34;</span><span class="p">)</span><span class="si">}</span><span class="sb">&#39; | claude -p --dangerously-skip-permissions`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="sb">`</span><span class="err">\</span><span class="sb">nCheck your repository for branch: </span><span class="si">${</span><span class="nx">branchName</span><span class="si">}</span><span class="sb">`</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">fixCodeIssue</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bnB4IHRzeCAwNS1maXgtY29kZS1pc3N1ZS50cw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">npx tsx 05-fix-code-issue.ts</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>创建 <code>05_fix_code_issue.py</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmltcG9ydCB0aW1lCmZyb20gZG90ZW52IGltcG9ydCBsb2FkX2RvdGVudgpmcm9tIGUyYiBpbXBvcnQgQXN5bmNTYW5kYm94Cgpsb2FkX2RvdGVudigpCgphc3luYyBkZWYgZml4X2NvZGVfaXNzdWUoKToKICAgIHByaW50KCJDcmVhdGluZyBzYW5kYm94Li4uXG4iKQoKICAgIHNieCA9IGF3YWl0IEFzeW5jU2FuZGJveC5iZXRhX2NyZWF0ZSgKICAgICAgICBlbnZzPXsKICAgICAgICAgICAgIkFOVEhST1BJQ19BUElfS0VZIjogb3MuZ2V0ZW52KCJBTlRIUk9QSUNfQVBJX0tFWSIpLAogICAgICAgICAgICAiR0lUSFVCX1RPS0VOIjogb3MuZ2V0ZW52KCJHSVRIVUJfVE9LRU4iKSwKICAgICAgICAgICAgIlNPTkFSUVVCRV9UT0tFTiI6IG9zLmdldGVudigiU09OQVJRVUJFX1RPS0VOIiksCiAgICAgICAgfSwKICAgICAgICBtY3A9ewogICAgICAgICAgICAiZ2l0aHViT2ZmaWNpYWwiOiB7CiAgICAgICAgICAgICAgICAiZ2l0aHViUGVyc29uYWxBY2Nlc3NUb2tlbiI6IG9zLmdldGVudigiR0lUSFVCX1RPS0VOIiksCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJzb25hcnF1YmUiOiB7CiAgICAgICAgICAgICAgICAib3JnIjogb3MuZ2V0ZW52KCJTT05BUlFVQkVfT1JHIiksCiAgICAgICAgICAgICAgICAidG9rZW4iOiBvcy5nZXRlbnYoIlNPTkFSUVVCRV9UT0tFTiIpLAogICAgICAgICAgICAgICAgInVybCI6ICJodHRwczovL3NvbmFyY2xvdWQuaW8iLAogICAgICAgICAgICB9LAogICAgICAgIH0sCiAgICApCgogICAgbWNwX3VybCA9IHNieC5iZXRhX2dldF9tY3BfdXJsKCkKICAgIG1jcF90b2tlbiA9IGF3YWl0IHNieC5iZXRhX2dldF9tY3BfdG9rZW4oKQoKICAgIGF3YWl0IGFzeW5jaW8uc2xlZXAoMSkKCiAgICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgICAgIGYnY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkge21jcF91cmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIge21jcF90b2tlbn0iJywKICAgICAgICB0aW1lb3V0PTAsCiAgICAgICAgb25fc3Rkb3V0PXByaW50LAogICAgICAgIG9uX3N0ZGVycj1wcmludCwKICAgICkKCiAgICByZXBvX3BhdGggPSBmIntvcy5nZXRlbnYoJ0dJVEhVQl9PV05FUicpfS97b3MuZ2V0ZW52KCdHSVRIVUJfUkVQTycpfSIKICAgIGJyYW5jaF9uYW1lID0gZiJxdWFsaXR5LWZpeC17aW50KHRpbWUudGltZSgpICogMTAwMCl9IgoKICAgIHByaW50KCJcbkZpeGluZyBhIGNvZGUgcXVhbGl0eSBpc3N1ZS4uLlxuIikKCiAgICBwcm9tcHQgPSBmIiIiVXNpbmcgR2l0SHViIGFuZCBTb25hclF1YmUgTUNQIHRvb2xzOgoKICAgIDEuIEFuYWx5emUgY29kZSBxdWFsaXR5IGluIHJlcG9zaXRvcnkgIntyZXBvX3BhdGh9IiB3aXRoIFNvbmFyUXViZQogICAgMi4gRmluZCBPTkUgc2ltcGxlIGlzc3VlIHRoYXQgY2FuIGJlIGNvbmZpZGVudGx5IGZpeGVkIChsaWtlIGFuIHVudXNlZCB2YXJpYWJsZSBvciBjb2RlIHNtZWxsKQogICAgMy4gQ3JlYXRlIGEgbmV3IGJyYW5jaCBjYWxsZWQgInticmFuY2hfbmFtZX0iCiAgICA0LiBSZWFkIHRoZSBmaWxlIGNvbnRhaW5pbmcgdGhlIGlzc3VlIHVzaW5nIEdpdEh1YiB0b29scwogICAgNS4gRml4IHRoZSBpc3N1ZSBpbiB0aGUgY29kZQogICAgNi4gQ29tbWl0IHRoZSBmaXggdG8gdGhlIG5ldyBicmFuY2ggd2l0aCBhIGNsZWFyIGNvbW1pdCBtZXNzYWdlCgogICAgSW1wb3J0YW50OiBPbmx5IGZpeCBpc3N1ZXMgeW91J3JlIDEwMCUgY29uZmlkZW50IGFib3V0LiBFeHBsYWluIHdoYXQgeW91J3JlIGZpeGluZyBhbmQgd2h5LiIiIgoKICAgIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICAgICAgZiJlY2hvICd7cHJvbXB0fScgfCBjbGF1ZGUgLXAgLS1kYW5nZXJvdXNseS1za2lwLXBlcm1pc3Npb25zIiwKICAgICAgICB0aW1lb3V0PTAsCiAgICAgICAgb25fc3Rkb3V0PXByaW50LAogICAgICAgIG9uX3N0ZGVycj1wcmludCwKICAgICkKCiAgICBwcmludChmIlxuIENoZWNrIHlvdXIgcmVwb3NpdG9yeSBmb3IgYnJhbmNoOiB7YnJhbmNoX25hbWV9IikKCiAgICBhd2FpdCBzYngua2lsbCgpCgppZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgYXN5bmNpby5ydW4oZml4X2NvZGVfaXNzdWUoKSk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">os</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">asyncio</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">time</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">AsyncSandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">fix_code_issue</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;sonarqube&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;org&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_ORG&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;token&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;url&#34;</span><span class="p">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">repo_path</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;</span><span class="si">{</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">&#39;GITHUB_OWNER&#39;</span><span class="p">)</span><span class="si">}</span><span class="s2">/</span><span class="si">{</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s1">&#39;GITHUB_REPO&#39;</span><span class="p">)</span><span class="si">}</span><span class="s2">&#34;</span>
</span></span><span class="line"><span class="cl">    <span class="n">branch_name</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;quality-fix-</span><span class="si">{</span><span class="nb">int</span><span class="p">(</span><span class="n">time</span><span class="o">.</span><span class="n">time</span><span class="p">()</span> <span class="o">*</span> <span class="mi">1000</span><span class="p">)</span><span class="si">}</span><span class="s2">&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Fixing a code quality issue...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">prompt</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;&#34;&#34;Using GitHub and SonarQube MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">    1. Analyze code quality in repository &#34;</span><span class="si">{</span><span class="n">repo_path</span><span class="si">}</span><span class="s2">&#34; with SonarQube
</span></span></span><span class="line"><span class="cl"><span class="s2">    2. Find ONE simple issue that can be confidently fixed (like an unused variable or code smell)
</span></span></span><span class="line"><span class="cl"><span class="s2">    3. Create a new branch called &#34;</span><span class="si">{</span><span class="n">branch_name</span><span class="si">}</span><span class="s2">&#34;
</span></span></span><span class="line"><span class="cl"><span class="s2">    4. Read the file containing the issue using GitHub tools
</span></span></span><span class="line"><span class="cl"><span class="s2">    5. Fix the issue in the code
</span></span></span><span class="line"><span class="cl"><span class="s2">    6. Commit the fix to the new branch with a clear commit message
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">    Important: Only fix issues you&#39;re 100% confident about. Explain what you&#39;re fixing and why.&#34;&#34;&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s2">&#34;echo &#39;</span><span class="si">{</span><span class="n">prompt</span><span class="si">}</span><span class="s2">&#39; | claude -p --dangerously-skip-permissions&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2"> Check your repository for branch: </span><span class="si">{</span><span class="n">branch_name</span><span class="si">}</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">    <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">fix_code_issue</span><span class="p">())</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>运行脚本：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cHl0aG9uIDA1X2ZpeF9jb2RlX2lzc3VlLnB5', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">python 05_fix_code_issue.py</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


> [!NOTE]
>
> 此脚本可能需要几分钟才能运行。

Claude 将分析您的仓库并修复一个代码质量问题：

```console {collapse=true}
Creating sandbox...

Fixing a code quality issue...

## Task Completed Successfully!

I've successfully analyzed the repository and fixed a code quality issue. Here's what I did:

### 1. Analysis
Found 1 SonarQube issues in the `<your-repo>` repository:
- **Unused variable** (MINOR severity, line 2)
- Useless assignment (MAJOR severity, line 2)
- For-of loop suggestion (MINOR severity, lines 5-7)

### 2. Issue Fixed
**Location:** test.js:2
**Issue:** Unused variable declaration
**SonarQube Rule:** javascript:S1481
**What was wrong:** The line `const unusedVariable = "this is not used";` declared a variable that was never used anywhere in the function.

### 3. Why This Fix is Safe
- The variable was only declared and assigned, never referenced
- Removing it has zero impact on functionality
- It eliminates dead code and improves code quality
- This is a textbook example of a code smell that should be removed

### 4. Changes Made
- Created branch: `quality-fix-xxxxx`
- Removed the unused variable declaration
- Committed with a clear message explaining the fix and referencing the SonarQube rule

**Commit SHA:** `xxxxxxxxxxxxxxxxxxxxxxxxx`
**Branch:** https://github.com/<github-org>/<your-repo>/tree/quality-fix-xxxxx

The fix is ready for review and can be merged to improve the code quality of the repository!
```

您现在可以在同一个工作流中使用 GitHub 和 SonarQube MCP 工具来读取文件、进行代码更改并提交它们。

## 步骤 6：创建质量门控的拉取请求

最后，让我们构建完整的工作流：分析质量、修复问题，并且仅在做出改进时才创建 PR。








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
      >
        <p>创建 <code>06-quality-gated-pr.ts</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiBxdWFsaXR5R2F0ZWRQUigpIHsKICBjb25zb2xlLmxvZygiQ3JlYXRpbmcgc2FuZGJveCBmb3IgcXVhbGl0eS1nYXRlZCBQUiB3b3JrZmxvdy4uLlxuIik7CgogIGNvbnN0IHNieCA9IGF3YWl0IFNhbmRib3guYmV0YUNyZWF0ZSh7CiAgICBlbnZzOiB7CiAgICAgIEFOVEhST1BJQ19BUElfS0VZOiBwcm9jZXNzLmVudi5BTlRIUk9QSUNfQVBJX0tFWSEsCiAgICAgIEdJVEhVQl9UT0tFTjogcHJvY2Vzcy5lbnYuR0lUSFVCX1RPS0VOISwKICAgICAgU09OQVJRVUJFX1RPS0VOOiBwcm9jZXNzLmVudi5TT05BUlFVQkVfVE9LRU4hLAogICAgfSwKICAgIG1jcDogewogICAgICBnaXRodWJPZmZpY2lhbDogewogICAgICAgIGdpdGh1YlBlcnNvbmFsQWNjZXNzVG9rZW46IHByb2Nlc3MuZW52LkdJVEhVQl9UT0tFTiEsCiAgICAgIH0sCiAgICAgIHNvbmFycXViZTogewogICAgICAgIG9yZzogcHJvY2Vzcy5lbnYuU09OQVJRVUJFX09SRyEsCiAgICAgICAgdG9rZW46IHByb2Nlc3MuZW52LlNPTkFSUVVCRV9UT0tFTiEsCiAgICAgICAgdXJsOiAiaHR0cHM6Ly9zb25hcmNsb3VkLmlvIiwKICAgICAgfSwKICAgIH0sCiAgfSk7CgogIGNvbnN0IG1jcFVybCA9IHNieC5iZXRhR2V0TWNwVXJsKCk7CiAgY29uc3QgbWNwVG9rZW4gPSBhd2FpdCBzYnguYmV0YUdldE1jcFRva2VuKCk7CgogIGF3YWl0IG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiBzZXRUaW1lb3V0KHJlc29sdmUsIDEwMDApKTsKCiAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgIGBjbGF1ZGUgbWNwIGFkZCAtLXRyYW5zcG9ydCBodHRwIGUyYi1tY3AtZ2F0ZXdheSAke21jcFVybH0gLS1oZWFkZXIgIkF1dGhvcml6YXRpb246IEJlYXJlciAke21jcFRva2VufSJgLAogICB7IHRpbWVvdXRNczogMCwgb25TdGRvdXQ6IGNvbnNvbGUubG9nLCBvblN0ZGVycjogY29uc29sZS5sb2cgfSwKICk7CgogY29uc29sZS5sb2coIlxuU3RhcnRpbmcgcXVhbGl0eS1nYXRlZCBQUiB3b3JrZmxvdy4uLlxuIik7CgogY29uc3QgcHJvbXB0ID0gYFVzaW5nIEdpdEh1YiBhbmQgU29uYXJRdWJlIE1DUCB0b29scywgY3JlYXRlIGEgY29tcGxldGUgcXVhbGl0eS1nYXRlZCBQUiB3b3JrZmxvdzoKCiAgIDEuIEFuYWx5emUgdGhlIGN1cnJlbnQgY29kZSBxdWFsaXR5IGluIHJlcG9zaXRvcnkgIiR7cHJvY2Vzcy5lbnYuR0lUSFVCX09XTkVSfS8ke3Byb2Nlc3MuZW52LkdJVEhVQl9SRVBPfSIKICAgMi4gSWRlbnRpZnkgT05FIHNpbXBsZSwgc2FmZS10by1maXggaXNzdWUKICAgMy4gQ3JlYXRlIGEgbmV3IGJyYW5jaCBjYWxsZWQgInF1YWxpdHktZml4LWF1dG9tYXRlZC0ke0RhdGUubm93KCl9IgogICA0LiBGaXggdGhlIGlzc3VlIGFuZCBjb21taXQgdGhlIGNoYW5nZXMKICAgNS4gQ3JlYXRlIGEgcHVsbCByZXF1ZXN0IHdpdGggYSBkZXRhaWxlZCBkZXNjcmlwdGlvbiBvZiB0aGUgcXVhbGl0eSBpbXByb3ZlbWVudAogICA2LiBWZXJpZnkgdGhhdCB0aGUgcXVhbGl0eSBnYXRlIHN0YXR1cyBoYXMgaW1wcm92ZWQKCiAgIE9ubHkgcHJvY2VlZCBpZiB5b3UgY2FuIGNvbmZpZGVudGx5IGZpeCBhbiBpc3N1ZSB3aXRob3V0IGJyZWFraW5nIGZ1bmN0aW9uYWxpdHkuYDsKCiBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICBgZWNobyAnJHtwcm9tcHQucmVwbGFjZSgvJy9nLCAiJ1xcJyciKX0nIHwgY2xhdWRlIC1wIC0tZGFuZ2Vyb3VzbHktc2tpcC1wZXJtaXNzaW9uc2AsCiAgIHsKICAgICB0aW1lb3V0TXM6IDAsCiAgICAgb25TdGRvdXQ6IGNvbnNvbGUubG9nLAogICAgIG9uU3RkZXJyOiBjb25zb2xlLmxvZywKICAgfSwKICk7CgogY29uc29sZS5sb2coIlxuV29ya2Zsb3cgY29tcGxldGVkISBDbGVhbmluZyB1cC4uLiIpOwoKIGF3YWl0IHNieC5raWxsKCk7Cn0KCnF1YWxpdHlHYXRlZFBSKCkuY2F0Y2goY29uc29sZS5lcnJvcik7', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">import</span> <span class="s2">&#34;dotenv/config&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl"><span class="kr">import</span> <span class="p">{</span> <span class="nx">Sandbox</span> <span class="p">}</span> <span class="kr">from</span> <span class="s2">&#34;e2b&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">qualityGatedPR() {</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Creating sandbox for quality-gated PR workflow...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">GITHUB_TOKEN</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">SONARQUBE_TOKEN</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nx">sonarqube</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">org</span>: <span class="kt">process.env.SONARQUBE_ORG</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">token</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nx">url</span><span class="o">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">betaGetMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">1000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">   <span class="p">{</span> <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span> <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span> <span class="nx">onStderr</span>: <span class="kt">console.log</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl"> <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nStarting quality-gated PR workflow...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span> <span class="sb">`Using GitHub and SonarQube MCP tools, create a complete quality-gated PR workflow:
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">   1. Analyze the current code quality in repository &#34;</span><span class="si">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">GITHUB_OWNER</span><span class="si">}</span><span class="sb">/</span><span class="si">${</span><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">GITHUB_REPO</span><span class="si">}</span><span class="sb">&#34;
</span></span></span><span class="line"><span class="cl"><span class="sb">   2. Identify ONE simple, safe-to-fix issue
</span></span></span><span class="line"><span class="cl"><span class="sb">   3. Create a new branch called &#34;quality-fix-automated-</span><span class="si">${</span><span class="nb">Date</span><span class="p">.</span><span class="nx">now</span><span class="p">()</span><span class="si">}</span><span class="sb">&#34;
</span></span></span><span class="line"><span class="cl"><span class="sb">   4. Fix the issue and commit the changes
</span></span></span><span class="line"><span class="cl"><span class="sb">   5. Create a pull request with a detailed description of the quality improvement
</span></span></span><span class="line"><span class="cl"><span class="sb">   6. Verify that the quality gate status has improved
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">   Only proceed if you can confidently fix an issue without breaking functionality.`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">   <span class="sb">`echo &#39;</span><span class="si">${</span><span class="nx">prompt</span><span class="p">.</span><span class="nx">replace</span><span class="p">(</span><span class="sr">/&#39;/g</span><span class="p">,</span> <span class="s2">&#34;&#39;\\&#39;&#39;&#34;</span><span class="p">)</span><span class="si">}</span><span class="sb">&#39; | claude -p --dangerously-skip-permissions`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">   <span class="p">{</span>
</span></span><span class="line"><span class="cl">     <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">     <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">     <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">   <span class="p">},</span>
</span></span><span class="line"><span class="cl"> <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nWorkflow completed! Cleaning up...&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">qualityGatedPR</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>Create <code>06_quality_gated_pr.py</code>:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmltcG9ydCB0aW1lCmZyb20gZG90ZW52IGltcG9ydCBsb2FkX2RvdGVudgpmcm9tIGUyYiBpbXBvcnQgQXN5bmNTYW5kYm94Cgpsb2FkX2RvdGVudigpCgphc3luYyBkZWYgcXVhbGl0eV9nYXRlZF9wcigpOgogICBwcmludCgiQ3JlYXRpbmcgc2FuZGJveCBmb3IgcXVhbGl0eS1nYXRlZCBQUiB3b3JrZmxvdy4uLlxuIikKCiAgIHNieCA9IGF3YWl0IEFzeW5jU2FuZGJveC5iZXRhX2NyZWF0ZSgKICAgICAgIGVudnM9ewogICAgICAgICAgICJBTlRIUk9QSUNfQVBJX0tFWSI6IG9zLmdldGVudigiQU5USFJPUElDX0FQSV9LRVkiKSwKICAgICAgICAgICAiR0lUSFVCX1RPS0VOIjogb3MuZ2V0ZW52KCJHSVRIVUJfVE9LRU4iKSwKICAgICAgICAgICAiU09OQVJRVUJFX1RPS0VOIjogb3MuZ2V0ZW52KCJTT05BUlFVQkVfVE9LRU4iKSwKICAgICAgIH0sCiAgICAgICBtY3A9ewogICAgICAgICAgICJnaXRodWJPZmZpY2lhbCI6IHsKICAgICAgICAgICAgICAgImdpdGh1YlBlcnNvbmFsQWNjZXNzVG9rZW4iOiBvcy5nZXRlbnYoIkdJVEhVQl9UT0tFTiIpLAogICAgICAgICAgIH0sCiAgICAgICAgICAgInNvbmFycXViZSI6IHsKICAgICAgICAgICAgICAgIm9yZyI6IG9zLmdldGVudigiU09OQVJRVUJFX09SRyIpLAogICAgICAgICAgICAgICAidG9rZW4iOiBvcy5nZXRlbnYoIlNPTkFSUVVCRV9UT0tFTiIpLAogICAgICAgICAgICAgICAidXJsIjogImh0dHBzOi8vc29uYXJjbG91ZC5pbyIsCiAgICAgICAgICAgfSwKICAgICAgIH0sCiAgICkKCiAgIG1jcF91cmwgPSBzYnguYmV0YV9nZXRfbWNwX3VybCgpCiAgIG1jcF90b2tlbiA9IGF3YWl0IHNieC5iZXRhX2dldF9tY3BfdG9rZW4oKQoKICAgYXdhaXQgYXN5bmNpby5zbGVlcCgxKQoKICAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgICAgIGYnY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkge21jcF91cmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIge21jcF90b2tlbn0iJywKICAgICAgIHRpbWVvdXQ9MCwKICAgICAgIG9uX3N0ZG91dD1wcmludCwKICAgICAgIG9uX3N0ZGVycj1wcmludCwKICAgKQoKICAgcHJpbnQoIlxuU3RhcnRpbmcgcXVhbGl0eS1nYXRlZCBQUiB3b3JrZmxvdy4uLlxuIikKCiAgIHByb21wdCA9IGYiIiJVc2luZyBHaXRIdWIgYW5kIFNvbmFyUXViZSBNQ1AgdG9vbHMsIGNyZWF0ZSBhIGNvbXBsZXRlIHF1YWxpdHktZ2F0ZWQgUFIgd29ya2Zsb3c6CgogICAxLiBBbmFseXplIHRoZSBjdXJyZW50IGNvZGUgcXVhbGl0eSBpbiByZXBvc2l0b3J5ICJ7b3MuZ2V0ZW52KCJHSVRIVUJfT1dORVIiKX0ve29zLmdldGVudigiR0lUSFVCX1JFUE8iKX0iCiAgIDIuIElkZW50aWZ5IE9ORSBzaW1wbGUsIHNhZmUtdG8tZml4IGlzc3VlCiAgIDMuIENyZWF0ZSBhIG5ldyBicmFuY2ggY2FsbGVkICJxdWFsaXR5LWZpeC1hdXRvbWF0ZWQte2ludCh0aW1lLnRpbWUoKSAqIDEwMDApfSIKICAgNC4gRml4IHRoZSBpc3N1ZSBhbmQgY29tbWl0IHRoZSBjaGFuZ2VzCiAgIDUuIENyZWF0ZSBhIHB1bGwgcmVxdWVzdCB3aXRoIGEgZGV0YWlsZWQgZGVzY3JpcHRpb24gb2YgdGhlIHF1YWxpdHkgaW1wcm92ZW1lbnQKICAgNi4gVmVyaWZ5IHRoYXQgdGhlIHF1YWxpdHkgZ2F0ZSBzdGF0dXMgaGFzIGltcHJvdmVkCgogICBPbmx5IHByb2NlZWQgaWYgeW91IGNhbiBjb25maWRlbnRseSBmaXggYW4gaXNzdWUgd2l0aG91dCBicmVha2luZyBmdW5jdGlvbmFsaXR5LiIiIgoKICAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgICAgIGYiZWNobyAne3Byb21wdH0nIHwgY2xhdWRlIC1wIC0tZGFuZ2Vyb3VzbHktc2tpcC1wZXJtaXNzaW9ucyIsCiAgICAgICB0aW1lb3V0PTAsCiAgICAgICBvbl9zdGRvdXQ9cHJpbnQsCiAgICAgICBvbl9zdGRlcnI9cHJpbnQsCiAgICkKCiAgIHByaW50KCJcbldvcmtmbG93IGNvbXBsZXRlZCEgQ2xlYW5pbmcgdXAuLi4iKQoKICAgYXdhaXQgc2J4LmtpbGwoKQoKaWYgX19uYW1lX18gPT0gIl9fbWFpbl9fIjoKICAgYXN5bmNpby5ydW4ocXVhbGl0eV9nYXRlZF9wcigpKQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">os</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">asyncio</span>
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">time</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">AsyncSandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">quality_gated_pr</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">   <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating sandbox for quality-gated PR workflow...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">       <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">           <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">           <span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">           <span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">       <span class="p">},</span>
</span></span><span class="line"><span class="cl">       <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">           <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">               <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">           <span class="p">},</span>
</span></span><span class="line"><span class="cl">           <span class="s2">&#34;sonarqube&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">               <span class="s2">&#34;org&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_ORG&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">               <span class="s2">&#34;token&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">               <span class="s2">&#34;url&#34;</span><span class="p">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">           <span class="p">},</span>
</span></span><span class="line"><span class="cl">       <span class="p">},</span>
</span></span><span class="line"><span class="cl">   <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">   <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">       <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">   <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Starting quality-gated PR workflow...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="n">prompt</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;&#34;&#34;Using GitHub and SonarQube MCP tools, create a complete quality-gated PR workflow:
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">   1. Analyze the current code quality in repository &#34;</span><span class="si">{</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_OWNER&#34;</span><span class="p">)</span><span class="si">}</span><span class="s2">/</span><span class="si">{</span><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_REPO&#34;</span><span class="p">)</span><span class="si">}</span><span class="s2">&#34;
</span></span></span><span class="line"><span class="cl"><span class="s2">   2. Identify ONE simple, safe-to-fix issue
</span></span></span><span class="line"><span class="cl"><span class="s2">   3. Create a new branch called &#34;quality-fix-automated-</span><span class="si">{</span><span class="nb">int</span><span class="p">(</span><span class="n">time</span><span class="o">.</span><span class="n">time</span><span class="p">()</span> <span class="o">*</span> <span class="mi">1000</span><span class="p">)</span><span class="si">}</span><span class="s2">&#34;
</span></span></span><span class="line"><span class="cl"><span class="s2">   4. Fix the issue and commit the changes
</span></span></span><span class="line"><span class="cl"><span class="s2">   5. Create a pull request with a detailed description of the quality improvement
</span></span></span><span class="line"><span class="cl"><span class="s2">   6. Verify that the quality gate status has improved
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">   Only proceed if you can confidently fix an issue without breaking functionality.&#34;&#34;&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">       <span class="sa">f</span><span class="s2">&#34;echo &#39;</span><span class="si">{</span><span class="n">prompt</span><span class="si">}</span><span class="s2">&#39; | claude -p --dangerously-skip-permissions&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="n">timeout</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">       <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">   <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Workflow completed! Cleaning up...&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">   <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">   <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">quality_gated_pr</span><span class="p">())</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>Run the script:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'cHl0aG9uIDA2X3F1YWxpdHlfZ2F0ZWRfcHIucHk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl">python 06_quality_gated_pr.py</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 总结

您已成功构建了一个完整的自动化代码质量工作流，该工作流：

- 使用 E2B 沙箱隔离运行环境
- 通过 MCP 服务器连接 GitHub 和 SonarQube
- 以自然语言与 AI 代理交互
- 自动检测和修复代码质量问题
- 创建拉取请求以合并改进

这个工作流展示了 AI 驱动的 DevOps 自动化的强大功能，将质量保证直接集成到开发流程中。

## 下一步

- 探索 [E2B 提供的其他 MCP 服务器](https://e2b.dev/docs/mcp/servers)
- 将此工作流集成到您的 CI/CD 管道中
- 添加更多质量检查步骤，如安全扫描或性能测试
- 尝试使用其他 AI 模型，如 Claude Sonnet 或 GPT-4
