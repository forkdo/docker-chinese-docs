# E2B 沙盒

Docker 已与 [E2B](https://e2b.dev/) 达成合作，后者是为 AI 智能体提供安全云沙盒的供应商。通过此次合作，每个 E2B 沙盒均可直接访问 Docker 的 [MCP Catalog](https://hub.docker.com/mcp)，该目录汇集了来自 GitHub、Notion 和 Stripe 等发布者的 200 多款工具。

创建沙盒时，您需指定其应访问的 MCP 工具。E2B 会启动这些工具，并通过 Docker MCP Gateway 提供访问权限。

## 示例：使用 GitHub 和 Notion MCP 服务器

本示例演示如何在 E2B 沙盒中连接多个 MCP 服务器。您将使用 Claude 分析 Notion 中的数据并创建 GitHub 问题。

### 前提条件

开始之前，请确保具备以下条件：

- 拥有 API 访问权限的 [E2B 账户](https://e2b.dev/docs/quickstart)
- 用于 Claude 的 Anthropic API 密钥

  > [!NOTE]
  > 本示例使用预装在 E2B 沙盒中的 Claude Code。
  > 不过，您可以调整示例以使用其他自选的 AI 助手。
  > 有关替代连接方法，请参阅 [E2B 的 MCP 文档](https://e2b.dev/docs/mcp/quickstart)。

- 本地已安装 Node.js 18+
- Notion 账户，包含：
  - 包含示例数据的数据库
  - [集成令牌](https://www.notion.com/help/add-and-manage-connections-with-the-api)
- GitHub 账户，包含：
  - 用于测试的仓库
  - 具有 `repo` 作用域的个人访问令牌

### 设置环境

创建新目录并初始化 Node.js 项目：

```console
$ mkdir mcp-e2b-quickstart
$ cd mcp-e2b-quickstart
$ npm init -y
```

通过更新 `package.json` 为项目配置 ES 模块：

```json
{
  "name": "mcp-e2b-quickstart",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node index.js"
  }
}
```

安装所需依赖项：

```console
$ npm install e2b dotenv
```

创建包含凭证的 `.env` 文件：

```console
$ cat > .env << 'EOF'
E2B_API_KEY=your_e2b_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
NOTION_INTEGRATION_TOKEN=ntn_your_notion_integration_token_here
GITHUB_TOKEN=ghp_your_github_pat_here
EOF
```

保护您的凭证：

```console
$ echo ".env" >> .gitignore
$ echo "node_modules/" >> .gitignore
```

### 创建带 MCP 服务器的 E2B 沙盒








<div
  class="tabs"
  
    x-data="{ selected: 'Typescript' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Typescript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Typescript'"
        
      >
        Typescript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Python'"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Typescript' && 'hidden'"
      >
        <p>创建名为 <code>index.ts</code> 的文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiBxdWlja3N0YXJ0KCk6IFByb21pc2U8dm9pZD4gewogIGNvbnNvbGUubG9nKCJDcmVhdGluZyBFMkIgc2FuZGJveCB3aXRoIE5vdGlvbiBhbmQgR2l0SHViIE1DUCBzZXJ2ZXJzLi4uXG4iKTsKCiAgY29uc3Qgc2J4OiBTYW5kYm94ID0gYXdhaXQgU2FuZGJveC5jcmVhdGUoewogICAgZW52czogewogICAgICBBTlRIUk9QSUNfQVBJX0tFWTogcHJvY2Vzcy5lbnYuQU5USFJPUElDX0FQSV9LRVkgYXMgc3RyaW5nLAogICAgfSwKICAgIG1jcDogewogICAgICBub3Rpb246IHsKICAgICAgICBpbnRlcm5hbEludGVncmF0aW9uVG9rZW46IHByb2Nlc3MuZW52CiAgICAgICAgICAuTk9USU9OX0lOVEVHUkFUSU9OX1RPS0VOIGFzIHN0cmluZywKICAgICAgfSwKICAgICAgZ2l0aHViT2ZmaWNpYWw6IHsKICAgICAgICBnaXRodWJQZXJzb25hbEFjY2Vzc1Rva2VuOiBwcm9jZXNzLmVudi5HSVRIVUJfVE9LRU4gYXMgc3RyaW5nLAogICAgICB9LAogICAgfSwKICB9KTsKCiAgY29uc3QgbWNwVXJsID0gc2J4LmdldE1jcFVybCgpOwogIGNvbnN0IG1jcFRva2VuID0gYXdhaXQgc2J4LmdldE1jcFRva2VuKCk7CgogIGNvbnNvbGUubG9nKCJTYW5kYm94IGNyZWF0ZWQgc3VjY2Vzc2Z1bGx5ISIpOwogIGNvbnNvbGUubG9nKGBNQ1AgR2F0ZXdheSBVUkw6ICR7bWNwVXJsfVxuYCk7CgogIC8vIFdhaXQgZm9yIE1DUCBpbml0aWFsaXphdGlvbgogIGF3YWl0IG5ldyBQcm9taXNlPHZvaWQ&#43;KChyZXNvbHZlKSA9PiBzZXRUaW1lb3V0KHJlc29sdmUsIDEwMDApKTsKCiAgLy8gQ29ubmVjdCBDbGF1ZGUgdG8gTUNQIGdhdGV3YXkKICBjb25zb2xlLmxvZygiQ29ubmVjdGluZyBDbGF1ZGUgdG8gTUNQIGdhdGV3YXkuLi4iKTsKICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgYGNsYXVkZSBtY3AgYWRkIC0tdHJhbnNwb3J0IGh0dHAgZTJiLW1jcC1nYXRld2F5ICR7bWNwVXJsfSAtLWhlYWRlciAiQXV0aG9yaXphdGlvbjogQmVhcmVyICR7bWNwVG9rZW59ImAsCiAgICB7CiAgICAgIHRpbWVvdXRNczogMCwKICAgICAgb25TdGRvdXQ6IGNvbnNvbGUubG9nLAogICAgICBvblN0ZGVycjogY29uc29sZS5sb2csCiAgICB9LAogICk7CgogIGNvbnNvbGUubG9nKCJcbkNvbm5lY3Rpb24gc3VjY2Vzc2Z1bCEgQ2xlYW5pbmcgdXAuLi4iKTsKICBhd2FpdCBzYngua2lsbCgpOwp9CgpxdWlja3N0YXJ0KCkuY2F0Y2goY29uc29sZS5lcnJvcik7', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">quickstart</span><span class="p">()</span><span class="o">:</span> <span class="nx">Promise</span><span class="p">&lt;</span><span class="nt">void</span><span class="p">&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Creating E2B sandbox with Notion and GitHub MCP servers...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span>: <span class="kt">Sandbox</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">create</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span> <span class="kr">as</span> <span class="kt">string</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">notion</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">internalIntegrationToken</span>: <span class="kt">process.env</span>
</span></span><span class="line"><span class="cl">          <span class="p">.</span><span class="nx">NOTION_INTEGRATION_TOKEN</span> <span class="kr">as</span> <span class="kt">string</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span> <span class="kr">as</span> <span class="kt">string</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">getMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">getMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Sandbox created successfully!&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="sb">`MCP Gateway URL: </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="err">\</span><span class="sb">n`</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="c1">// Wait for MCP initialization
</span></span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">&lt;</span><span class="nt">void</span><span class="p">&gt;((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">1000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="c1">// Connect Claude to MCP gateway
</span></span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Connecting Claude to MCP gateway...&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nConnection successful! Cleaning up...&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">quickstart</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBucHggdHN4IGluZGV4LnRz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> npx tsx index.ts
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>创建名为 <code>index.py</code> 的文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmZyb20gZG90ZW52IGltcG9ydCBsb2FkX2RvdGVudgpmcm9tIGUyYiBpbXBvcnQgU2FuZGJveAoKbG9hZF9kb3RlbnYoKQoKYXN5bmMgZGVmIHF1aWNrc3RhcnQoKToKICAgIHByaW50KCJDcmVhdGluZyBFMkIgc2FuZGJveCB3aXRoIE5vdGlvbiBhbmQgR2l0SHViIE1DUCBzZXJ2ZXJzLi4uXG4iKQoKICAgIHNieCA9IGF3YWl0IFNhbmRib3guYmV0YV9jcmVhdGUoCiAgICAgICAgZW52cz17CiAgICAgICAgICAgICJBTlRIUk9QSUNfQVBJX0tFWSI6IG9zLmdldGVudigiQU5USFJPUElDX0FQSV9LRVkiKSwKICAgICAgICB9LAogICAgICAgIG1jcD17CiAgICAgICAgICAgICJub3Rpb24iOiB7CiAgICAgICAgICAgICAgICAiaW50ZXJuYWxJbnRlZ3JhdGlvblRva2VuIjogb3MuZ2V0ZW52KCJOT1RJT05fSU5URUdSQVRJT05fVE9LRU4iKSwKICAgICAgICAgICAgfSwKICAgICAgICAgICAgImdpdGh1Yk9mZmljaWFsIjogewogICAgICAgICAgICAgICAgImdpdGh1YlBlcnNvbmFsQWNjZXNzVG9rZW4iOiBvcy5nZXRlbnYoIkdJVEhVQl9UT0tFTiIpLAogICAgICAgICAgICB9LAogICAgICAgIH0sCiAgICApCgogICAgbWNwX3VybCA9IHNieC5iZXRhX2dldF9tY3BfdXJsKCkKICAgIG1jcF90b2tlbiA9IGF3YWl0IHNieC5iZXRhX2dldF9tY3BfdG9rZW4oKQoKICAgIHByaW50KCJTYW5kYm94IGNyZWF0ZWQgc3VjY2Vzc2Z1bGx5ISIpCiAgICBwcmludChmIk1DUCBHYXRld2F5IFVSTDoge21jcF91cmx9XG4iKQoKICAgICMgV2FpdCBmb3IgTUNQIGluaXRpYWxpemF0aW9uCiAgICBhd2FpdCBhc3luY2lvLnNsZWVwKDEpCgogICAgIyBDb25uZWN0IENsYXVkZSB0byBNQ1AgZ2F0ZXdheQogICAgcHJpbnQoIkNvbm5lY3RpbmcgQ2xhdWRlIHRvIE1DUCBnYXRld2F5Li4uIikKCiAgICBkZWYgb25fc3Rkb3V0KG91dHB1dCk6CiAgICAgICAgcHJpbnQob3V0cHV0LCBlbmQ9JycpCgogICAgZGVmIG9uX3N0ZGVycihvdXRwdXQpOgogICAgICAgIHByaW50KG91dHB1dCwgZW5kPScnKQoKICAgIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICAgICAgZidjbGF1ZGUgbWNwIGFkZCAtLXRyYW5zcG9ydCBodHRwIGUyYi1tY3AtZ2F0ZXdheSB7bWNwX3VybH0gLS1oZWFkZXIgIkF1dGhvcml6YXRpb246IEJlYXJlciB7bWNwX3Rva2VufSInLAogICAgICAgIHRpbWVvdXRfbXM9MCwKICAgICAgICBvbl9zdGRvdXQ9b25fc3Rkb3V0LAogICAgICAgIG9uX3N0ZGVycj1vbl9zdGRlcnIKICAgICkKCiAgICBwcmludCgiXG5Db25uZWN0aW9uIHN1Y2Nlc3NmdWwhIENsZWFuaW5nIHVwLi4uIikKICAgIGF3YWl0IHNieC5raWxsKCkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICB0cnk6CiAgICAgICAgYXN5bmNpby5ydW4ocXVpY2tzdGFydCgpKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIHByaW50KGYiRXJyb3I6IHtlfSIp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">Sandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">quickstart</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating E2B sandbox with Notion and GitHub MCP servers...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">Sandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;notion&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;internalIntegrationToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;NOTION_INTEGRATION_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Sandbox created successfully!&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;MCP Gateway URL: </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1"># Wait for MCP initialization</span>
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1"># Connect Claude to MCP gateway</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Connecting Claude to MCP gateway...&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">def</span> <span class="nf">on_stdout</span><span class="p">(</span><span class="n">output</span><span class="p">):</span>
</span></span><span class="line"><span class="cl">        <span class="nb">print</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="s1">&#39;&#39;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">def</span> <span class="nf">on_stderr</span><span class="p">(</span><span class="n">output</span><span class="p">):</span>
</span></span><span class="line"><span class="cl">        <span class="nb">print</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="s1">&#39;&#39;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout_ms</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="n">on_stdout</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="n">on_stderr</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Connection successful! Cleaning up...&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">    <span class="k">try</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">        <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">quickstart</span><span class="p">())</span>
</span></span><span class="line"><span class="cl">    <span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;Error: </span><span class="si">{</span><span class="n">e</span><span class="si">}</span><span class="s2">&#34;</span><span class="p">)</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBweXRob24gaW5kZXgucHk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> python index.py
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


您将看到：

```console
Creating E2B sandbox with Notion and GitHub MCP servers...

Sandbox created successfully!
MCP Gateway URL: https://50005-xxxxx.e2b.app/mcp

Connecting Claude to MCP gateway...
Added HTTP MCP server e2b-mcp-gateway with URL: https://50005-xxxxx.e2b.app/mcp

Connection successful! Cleaning up...
```

### 使用示例工作流进行测试

现在，通过运行一个简单的工作流来测试设置，该工作流将搜索 Notion 并创建 GitHub 问题。








<div
  class="tabs"
  
    x-data="{ selected: 'Typescript' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Typescript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Typescript'"
        
      >
        Typescript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Python'"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Typescript' && 'hidden'"
      >
        

  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>将提示中的 <code>owner/repo</code> 替换为您的实际 GitHub 用户名和仓库名称（例如 <code>yourname/test-repo</code>）。</p>
    </div>
  </blockquote>

<p>使用以下示例更新 <code>index.ts</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjsKaW1wb3J0IHsgU2FuZGJveCB9IGZyb20gImUyYiI7Cgphc3luYyBmdW5jdGlvbiBleGFtcGxlV29ya2Zsb3coKTogUHJvbWlzZTx2b2lkPiB7CiAgY29uc29sZS5sb2coIkNyZWF0aW5nIHNhbmRib3guLi5cbiIpOwoKICBjb25zdCBzYng6IFNhbmRib3ggPSBhd2FpdCBTYW5kYm94LmNyZWF0ZSh7CiAgICBlbnZzOiB7CiAgICAgIEFOVEhST1BJQ19BUElfS0VZOiBwcm9jZXNzLmVudi5BTlRIUk9QSUNfQVBJX0tFWSBhcyBzdHJpbmcsCiAgICB9LAogICAgbWNwOiB7CiAgICAgIG5vdGlvbjogewogICAgICAgIGludGVybmFsSW50ZWdyYXRpb25Ub2tlbjogcHJvY2Vzcy5lbnYKICAgICAgICAgIC5OT1RJT05fSU5URUdSQVRJT05fVE9LRU4gYXMgc3RyaW5nLAogICAgICB9LAogICAgICBnaXRodWJPZmZpY2lhbDogewogICAgICAgIGdpdGh1YlBlcnNvbmFsQWNjZXNzVG9rZW46IHByb2Nlc3MuZW52LkdJVEhVQl9UT0tFTiBhcyBzdHJpbmcsCiAgICAgIH0sCiAgICB9LAogIH0pOwoKICBjb25zdCBtY3BVcmwgPSBzYnguZ2V0TWNwVXJsKCk7CiAgY29uc3QgbWNwVG9rZW4gPSBhd2FpdCBzYnguZ2V0TWNwVG9rZW4oKTsKCiAgY29uc29sZS5sb2coIlNhbmRib3ggY3JlYXRlZCBzdWNjZXNzZnVsbHlcbiIpOwoKICAvLyBXYWl0IGZvciBNQ1Agc2VydmVycyB0byBpbml0aWFsaXplCiAgYXdhaXQgbmV3IFByb21pc2U8dm9pZD4oKHJlc29sdmUpID0&#43;IHNldFRpbWVvdXQocmVzb2x2ZSwgMzAwMCkpOwoKICBjb25zb2xlLmxvZygiQ29ubmVjdGluZyBDbGF1ZGUgdG8gTUNQIGdhdGV3YXkuLi5cbiIpOwogIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICBgY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkgJHttY3BVcmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIgJHttY3BUb2tlbn0iYCwKICAgIHsKICAgICAgdGltZW91dE1zOiAwLAogICAgICBvblN0ZG91dDogY29uc29sZS5sb2csCiAgICAgIG9uU3RkZXJyOiBjb25zb2xlLmxvZywKICAgIH0sCiAgKTsKCiAgY29uc29sZS5sb2coIlxuUnVubmluZyBleGFtcGxlOiBTZWFyY2ggTm90aW9uIGFuZCBjcmVhdGUgR2l0SHViIGlzc3VlLi4uXG4iKTsKCiAgY29uc3QgcHJvbXB0OiBzdHJpbmcgPSBgVXNpbmcgTm90aW9uIGFuZCBHaXRIdWIgTUNQIHRvb2xzOgoxLiBTZWFyY2ggbXkgTm90aW9uIHdvcmtzcGFjZSBmb3IgZGF0YWJhc2VzCjIuIENyZWF0ZSBhIHRlc3QgaXNzdWUgaW4gb3duZXIvcmVwbyB0aXRsZWQgIk1DUCBUb29sa2l0IFRlc3QiIHdpdGggZGVzY3JpcHRpb24gIlRlc3RpbmcgRTJCICsgRG9ja2VyIE1DUCBpbnRlZ3JhdGlvbiIKMy4gQ29uZmlybSBib3RoIG9wZXJhdGlvbnMgY29tcGxldGVkIHN1Y2Nlc3NmdWxseWA7CgogIGF3YWl0IHNieC5jb21tYW5kcy5ydW4oCiAgICBgZWNobyAnJHtwcm9tcHQucmVwbGFjZSgvJy9nLCAiJ1xcJyciKX0nIHwgY2xhdWRlIC1wIC0tZGFuZ2Vyb3VzbHktc2tpcC1wZXJtaXNzaW9uc2AsCiAgICB7CiAgICAgIHRpbWVvdXRNczogMCwKICAgICAgb25TdGRvdXQ6IGNvbnNvbGUubG9nLAogICAgICBvblN0ZGVycjogY29uc29sZS5sb2csCiAgICB9LAogICk7CgogIGF3YWl0IHNieC5raWxsKCk7Cn0KCmV4YW1wbGVXb3JrZmxvdygpLmNhdGNoKGNvbnNvbGUuZXJyb3IpOw==', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">exampleWorkflow</span><span class="p">()</span><span class="o">:</span> <span class="nx">Promise</span><span class="p">&lt;</span><span class="nt">void</span><span class="p">&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">sbx</span>: <span class="kt">Sandbox</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">create</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span> <span class="kr">as</span> <span class="kt">string</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">notion</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">internalIntegrationToken</span>: <span class="kt">process.env</span>
</span></span><span class="line"><span class="cl">          <span class="p">.</span><span class="nx">NOTION_INTEGRATION_TOKEN</span> <span class="kr">as</span> <span class="kt">string</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span> <span class="kr">as</span> <span class="kt">string</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpUrl</span> <span class="o">=</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">getMcpUrl</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">mcpToken</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">getMcpToken</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Sandbox created successfully\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="c1">// Wait for MCP servers to initialize
</span></span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="k">new</span> <span class="nx">Promise</span><span class="p">&lt;</span><span class="nt">void</span><span class="p">&gt;((</span><span class="nx">resolve</span><span class="p">)</span> <span class="o">=&gt;</span> <span class="nx">setTimeout</span><span class="p">(</span><span class="nx">resolve</span><span class="p">,</span> <span class="mi">3000</span><span class="p">));</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Connecting Claude to MCP gateway...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sb">`claude mcp add --transport http e2b-mcp-gateway </span><span class="si">${</span><span class="nx">mcpUrl</span><span class="si">}</span><span class="sb"> --header &#34;Authorization: Bearer </span><span class="si">${</span><span class="nx">mcpToken</span><span class="si">}</span><span class="sb">&#34;`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;\nRunning example: Search Notion and create GitHub issue...\n&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">prompt</span>: <span class="kt">string</span> <span class="o">=</span> <span class="sb">`Using Notion and GitHub MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="sb">1. Search my Notion workspace for databases
</span></span></span><span class="line"><span class="cl"><span class="sb">2. Create a test issue in owner/repo titled &#34;MCP Toolkit Test&#34; with description &#34;Testing E2B + Docker MCP integration&#34;
</span></span></span><span class="line"><span class="cl"><span class="sb">3. Confirm both operations completed successfully`</span><span class="p">;</span>
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
</span></span><span class="line"><span class="cl"><span class="nx">exampleWorkflow</span><span class="p">().</span><span class="k">catch</span><span class="p">(</span><span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">);</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBucHggdHN4IGluZGV4LnRz', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> npx tsx index.ts
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
      >
        <p>使用此示例更新 <code>index.py</code>：</p>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 8V12M12 16H12.01M7.8 21H16.2C17.8802 21 18.7202 21 19.362 20.673C19.9265 20.3854 20.3854 19.9265 20.673 19.362C21 18.7202 21 17.8802 21 16.2V7.8C21 6.11984 21 5.27976 20.673 4.63803C20.3854 4.07354 19.9265 3.6146 19.362 3.32698C18.7202 3 17.8802 3 16.2 3H7.8C6.11984 3 5.27976 3 4.63803 3.32698C4.07354 3.6146 3.6146 4.07354 3.32698 4.63803C3 5.27976 3 6.11984 3 7.8V16.2C3 17.8802 3 18.7202 3.32698 19.362C3.6146 19.9265 4.07354 20.3854 4.63803 20.673C5.27976 21 6.11984 21 7.8 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Important
      </span>
    </div>
    <div class="admonition-content">
      <p>将提示中的 <code>owner/repo</code> 替换为您的实际 GitHub 用户名和仓库名称（例如 <code>yourname/test-repo</code>）。</p>
    </div>
  </blockquote>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0IG9zCmltcG9ydCBhc3luY2lvCmltcG9ydCBzaGxleApmcm9tIGRvdGVudiBpbXBvcnQgbG9hZF9kb3RlbnYKZnJvbSBlMmIgaW1wb3J0IFNhbmRib3gKCmxvYWRfZG90ZW52KCkKCmFzeW5jIGRlZiBleGFtcGxlX3dvcmtmbG93KCk6CiAgICBwcmludCgiQ3JlYXRpbmcgc2FuZGJveC4uLlxuIikKCiAgICBzYnggPSBhd2FpdCBTYW5kYm94LmJldGFfY3JlYXRlKAogICAgICAgIGVudnM9ewogICAgICAgICAgICAiQU5USFJPUElDX0FQSV9LRVkiOiBvcy5nZXRlbnYoIkFOVEhST1BJQ19BUElfS0VZIiksCiAgICAgICAgfSwKICAgICAgICBtY3A9ewogICAgICAgICAgICAibm90aW9uIjogewogICAgICAgICAgICAgICAgImludGVybmFsSW50ZWdyYXRpb25Ub2tlbiI6IG9zLmdldGVudigiTk9USU9OX0lOVEVHUkFUSU9OX1RPS0VOIiksCiAgICAgICAgICAgIH0sCiAgICAgICAgICAgICJnaXRodWJPZmZpY2lhbCI6IHsKICAgICAgICAgICAgICAgICJnaXRodWJQZXJzb25hbEFjY2Vzc1Rva2VuIjogb3MuZ2V0ZW52KCJHSVRIVUJfVE9LRU4iKSwKICAgICAgICAgICAgfSwKICAgICAgICB9LAogICAgKQoKICAgIG1jcF91cmwgPSBzYnguYmV0YV9nZXRfbWNwX3VybCgpCiAgICBtY3BfdG9rZW4gPSBhd2FpdCBzYnguYmV0YV9nZXRfbWNwX3Rva2VuKCkKCiAgICBwcmludCgiU2FuZGJveCBjcmVhdGVkIHN1Y2Nlc3NmdWxseVxuIikKCiAgICAjIFdhaXQgZm9yIE1DUCBzZXJ2ZXJzIHRvIGluaXRpYWxpemUKICAgIGF3YWl0IGFzeW5jaW8uc2xlZXAoMykKCiAgICBwcmludCgiQ29ubmVjdGluZyBDbGF1ZGUgdG8gTUNQIGdhdGV3YXkuLi5cbiIpCgogICAgZGVmIG9uX3N0ZG91dChvdXRwdXQpOgogICAgICAgIHByaW50KG91dHB1dCwgZW5kPScnKQoKICAgIGRlZiBvbl9zdGRlcnIob3V0cHV0KToKICAgICAgICBwcmludChvdXRwdXQsIGVuZD0nJykKCiAgICBhd2FpdCBzYnguY29tbWFuZHMucnVuKAogICAgICAgIGYnY2xhdWRlIG1jcCBhZGQgLS10cmFuc3BvcnQgaHR0cCBlMmItbWNwLWdhdGV3YXkge21jcF91cmx9IC0taGVhZGVyICJBdXRob3JpemF0aW9uOiBCZWFyZXIge21jcF90b2tlbn0iJywKICAgICAgICB0aW1lb3V0X21zPTAsCiAgICAgICAgb25fc3Rkb3V0PW9uX3N0ZG91dCwKICAgICAgICBvbl9zdGRlcnI9b25fc3RkZXJyCiAgICApCgogICAgcHJpbnQoIlxuUnVubmluZyBleGFtcGxlOiBTZWFyY2ggTm90aW9uIGFuZCBjcmVhdGUgR2l0SHViIGlzc3VlLi4uXG4iKQoKICAgIHByb21wdCA9ICIiIlVzaW5nIE5vdGlvbiBhbmQgR2l0SHViIE1DUCB0b29sczoKMS4gU2VhcmNoIG15IE5vdGlvbiB3b3Jrc3BhY2UgZm9yIGRhdGFiYXNlcwoyLiBDcmVhdGUgYSB0ZXN0IGlzc3VlIGluIG93bmVyL3JlcG8gdGl0bGVkICJNQ1AgVG9vbGtpdCBUZXN0IiB3aXRoIGRlc2NyaXB0aW9uICJUZXN0aW5nIEUyQiArIERvY2tlciBNQ1AgaW50ZWdyYXRpb24iCjMuIENvbmZpcm0gYm90aCBvcGVyYXRpb25zIGNvbXBsZXRlZCBzdWNjZXNzZnVsbHkiIiIKCiAgICAjIEVzY2FwZSBzaW5nbGUgcXVvdGVzIGZvciBzaGVsbAogICAgZXNjYXBlZF9wcm9tcHQgPSBwcm9tcHQucmVwbGFjZSgiJyIsICInXFwnJyIpCgogICAgYXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgICAgICBmImVjaG8gJ3tlc2NhcGVkX3Byb21wdH0nIHwgY2xhdWRlIC1wIC0tZGFuZ2Vyb3VzbHktc2tpcC1wZXJtaXNzaW9ucyIsCiAgICAgICAgdGltZW91dF9tcz0wLAogICAgICAgIG9uX3N0ZG91dD1vbl9zdGRvdXQsCiAgICAgICAgb25fc3RkZXJyPW9uX3N0ZGVycgogICAgKQoKICAgIGF3YWl0IHNieC5raWxsKCkKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICB0cnk6CiAgICAgICAgYXN5bmNpby5ydW4oZXhhbXBsZV93b3JrZmxvdygpKQogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgIHByaW50KGYiRXJyb3I6IHtlfSIp', copying: false }"
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
</span></span><span class="line"><span class="cl"><span class="kn">import</span> <span class="nn">shlex</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">e2b</span> <span class="kn">import</span> <span class="n">Sandbox</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">example_workflow</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Creating sandbox...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">Sandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;notion&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;internalIntegrationToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;NOTION_INTEGRATION_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">                <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">mcp_url</span> <span class="o">=</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_url</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp_token</span> <span class="o">=</span> <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">beta_get_mcp_token</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Sandbox created successfully</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1"># Wait for MCP servers to initialize</span>
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">asyncio</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">3</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Connecting Claude to MCP gateway...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">def</span> <span class="nf">on_stdout</span><span class="p">(</span><span class="n">output</span><span class="p">):</span>
</span></span><span class="line"><span class="cl">        <span class="nb">print</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="s1">&#39;&#39;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">def</span> <span class="nf">on_stderr</span><span class="p">(</span><span class="n">output</span><span class="p">):</span>
</span></span><span class="line"><span class="cl">        <span class="nb">print</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">end</span><span class="o">=</span><span class="s1">&#39;&#39;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s1">&#39;claude mcp add --transport http e2b-mcp-gateway </span><span class="si">{</span><span class="n">mcp_url</span><span class="si">}</span><span class="s1"> --header &#34;Authorization: Bearer </span><span class="si">{</span><span class="n">mcp_token</span><span class="si">}</span><span class="s1">&#34;&#39;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout_ms</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="n">on_stdout</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="n">on_stderr</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;</span><span class="se">\n</span><span class="s2">Running example: Search Notion and create GitHub issue...</span><span class="se">\n</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="n">prompt</span> <span class="o">=</span> <span class="s2">&#34;&#34;&#34;Using Notion and GitHub MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="s2">1. Search my Notion workspace for databases
</span></span></span><span class="line"><span class="cl"><span class="s2">2. Create a test issue in owner/repo titled &#34;MCP Toolkit Test&#34; with description &#34;Testing E2B + Docker MCP integration&#34;
</span></span></span><span class="line"><span class="cl"><span class="s2">3. Confirm both operations completed successfully&#34;&#34;&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1"># Escape single quotes for shell</span>
</span></span><span class="line"><span class="cl">    <span class="n">escaped_prompt</span> <span class="o">=</span> <span class="n">prompt</span><span class="o">.</span><span class="n">replace</span><span class="p">(</span><span class="s2">&#34;&#39;&#34;</span><span class="p">,</span> <span class="s2">&#34;&#39;</span><span class="se">\\</span><span class="s2">&#39;&#39;&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">        <span class="sa">f</span><span class="s2">&#34;echo &#39;</span><span class="si">{</span><span class="n">escaped_prompt</span><span class="si">}</span><span class="s2">&#39; | claude -p --dangerously-skip-permissions&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">timeout_ms</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stdout</span><span class="o">=</span><span class="n">on_stdout</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="n">on_stderr</span><span class="o">=</span><span class="n">on_stderr</span>
</span></span><span class="line"><span class="cl">    <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&#34;__main__&#34;</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">    <span class="k">try</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">        <span class="n">asyncio</span><span class="o">.</span><span class="n">run</span><span class="p">(</span><span class="n">example_workflow</span><span class="p">())</span>
</span></span><span class="line"><span class="cl">    <span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">e</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;Error: </span><span class="si">{</span><span class="n">e</span><span class="si">}</span><span class="s2">&#34;</span><span class="p">)</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'JCBweXRob24gd29ya2Zsb3cucHk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> python workflow.py
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


您将看到：

```console
Creating sandbox...

Running example: Search Notion and create GitHub issue...

## Task Completed Successfully

I've completed both operations using the Notion and GitHub MCP tools:

### 1. Notion Workspace Search

Found 3 databases in your Notion workspace:
- **Customer Feedback** - Database with 12 entries tracking feature requests
- **Product Roadmap** - Planning database with 8 active projects
- **Meeting Notes** - Shared workspace with 45 pages

### 2. GitHub Issue Creation

Successfully created test issue:
- **Repository**: your-org/your-repo
- **Issue Number**: #47
- **Title**: "MCP Test"
- **Description**: "Testing E2B + Docker MCP integration"
- **Status**: Open
- **URL**: https://github.com/your-org/your-repo/issues/47

Both operations completed successfully. The MCP servers are properly configured and working.
```

该沙盒连接了多个 MCP 服务器，并协调了跨 Notion 和 GitHub 的工作流。您可以扩展此模式，以组合 Docker MCP Catalog 中的 200 多个 MCP 服务器中的任意一个。

## 相关页面

- [如何使用 SonarQube 和 E2B 构建 AI 驱动的代码质量工作流](/guides/github-sonarqube-sandbox.md)
- [Docker + E2B：构建可信 AI 的未来](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/)
- [Docker 沙盒](/manuals/ai/sandboxes/_index.md)
- [Docker MCP 工具包和目录](/manuals/ai/mcp-catalog-and-toolkit/_index.md)
- [Docker MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)
- [E2B MCP 文档](https://e2b.dev/docs/mcp)
