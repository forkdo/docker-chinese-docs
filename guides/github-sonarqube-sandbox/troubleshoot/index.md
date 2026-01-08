# 故障排除代码质量工作流

本页介绍在使用 E2B 沙盒和 MCP 服务器构建代码质量工作流时可能遇到的常见问题及其解决方案。

如果您遇到此处未涵盖的问题，请查阅 [E2B 文档](https://e2b.dev/docs)。

## MCP 工具不可用

问题：Claude 报告 `I don't have any MCP tools available`（我没有可用的 MCP 工具）。

解决方案：

1.  确认您正在使用授权标头：

    ```plaintext
    --header "Authorization: Bearer ${mcpToken}"
    ```

2.  检查您是否在等待 MCP 初始化。

    ```typescript
    // typescript
    await new Promise((resolve) => setTimeout(resolve, 1000));
    ```

    ```python
    # python
    await asyncio.sleep(1)
    ```

3.  确保证书同时存在于 `envs` 和 `mcp` 配置中：

    ```typescript
    // typescript
    const sbx = await Sandbox.betaCreate({
      envs: {
        ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
        GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
        SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
      },
      mcp: {
        githubOfficial: {
          githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
        },
        sonarqube: {
          org: process.env.SONARQUBE_ORG!,
          token: process.env.SONARQUBE_TOKEN!,
          url: "https://sonarcloud.io",
        },
      },
    });
    ```

    ```python
    # python
    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
            "sonarqube": {
                "org": os.getenv("SONARQUBE_ORG"),
                "token": os.getenv("SONARQUBE_TOKEN"),
                "url": "https://sonarcloud.io",
            },
        },
    )
    ```

4.  验证您的 API 令牌有效且具有正确的权限范围。

## GitHub 工具正常但 SonarQube 不行

问题：GitHub MCP 工具加载，但 SonarQube 工具未显示。

解决方案：SonarQube MCP 服务器需要同时配置 GitHub。即使您只测试其中一个，也请始终在沙盒配置中包含这两个服务器。








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
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Ly8g5Y2z5L2/5Y&#43;q5L2/55So5LiA5Liq77yM5Lmf6KaB5YyF5ZCr5Lik5Liq5pyN5Yqh5ZmoCmNvbnN0IHNieCA9IGF3YWl0IFNhbmRib3guYmV0YUNyZWF0ZSh7CiAgZW52czogewogICAgQU5USFJPUElDX0FQSV9LRVk6IHByb2Nlc3MuZW52LkFOVEhST1BJQ19BUElfS0VZISwKICAgIEdJVEhVQl9UT0tFTjogcHJvY2Vzcy5lbnYuR0lUSFVCX1RPS0VOISwKICAgIFNPTkFSUVVCRV9UT0tFTjogcHJvY2Vzcy5lbnYuU09OQVJRVUJFX1RPS0VOISwKICB9LAogIG1jcDogewogICAgZ2l0aHViT2ZmaWNpYWw6IHsKICAgICAgZ2l0aHViUGVyc29uYWxBY2Nlc3NUb2tlbjogcHJvY2Vzcy5lbnYuR0lUSFVCX1RPS0VOISwKICAgIH0sCiAgICBzb25hcnF1YmU6IHsKICAgICAgb3JnOiBwcm9jZXNzLmVudi5TT05BUlFVQkVfT1JHISwKICAgICAgdG9rZW46IHByb2Nlc3MuZW52LlNPTkFSUVVCRV9UT0tFTiEsCiAgICAgIHVybDogImh0dHBzOi8vc29uYXJjbG91ZC5pbyIsCiAgICB9LAogIH0sCn0pOw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="c1">// 即使只使用一个，也要包含两个服务器
</span></span></span><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">  <span class="nx">envs</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nx">ANTHROPIC_API_KEY</span>: <span class="kt">process.env.ANTHROPIC_API_KEY</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nx">GITHUB_TOKEN</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nx">SONARQUBE_TOKEN</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="nx">mcp</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nx">githubOfficial</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">githubPersonalAccessToken</span>: <span class="kt">process.env.GITHUB_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="nx">sonarqube</span><span class="o">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">org</span>: <span class="kt">process.env.SONARQUBE_ORG</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">token</span>: <span class="kt">process.env.SONARQUBE_TOKEN</span><span class="o">!</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">      <span class="nx">url</span><span class="o">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">},</span>
</span></span><span class="line"><span class="cl"><span class="p">});</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
        x-data="{ code: 'IyDljbPkvb/lj6rkvb/nlKjkuIDkuKrvvIzkuZ/opoHljIXlkKvkuKTkuKrmnI3liqHlmagKc2J4ID0gYXdhaXQgQXN5bmNTYW5kYm94LmJldGFfY3JlYXRlKAogICAgZW52cz17CiAgICAgICAgIkFOVEhST1BJQ19BUElfS0VZIjogb3MuZ2V0ZW52KCJBTlRIUk9QSUNfQVBJX0tFWSIpLAogICAgICAgICJHSVRIVUJfVE9LRU4iOiBvcy5nZXRlbnYoIkdJVEhVQl9UT0tFTiIpLAogICAgICAgICJTT05BUlFVQkVfVE9LRU4iOiBvcy5nZXRlbnYoIlNPTkFSUVVCRV9UT0tFTiIpLAogICAgfSwKICAgIG1jcD17CiAgICAgICAgImdpdGh1Yk9mZmljaWFsIjogewogICAgICAgICAgICAiZ2l0aHViUGVyc29uYWxBY2Nlc3NUb2tlbiI6IG9zLmdldGVudigiR0lUSFVCX1RPS0VOIiksCiAgICAgICAgfSwKICAgICAgICAic29uYXJxdWJlIjogewogICAgICAgICAgICAib3JnIjogb3MuZ2V0ZW52KCJTT05BUlFVQkVfT1JHIiksCiAgICAgICAgICAgICJ0b2tlbiI6IG9zLmdldGVudigiU09OQVJRVUJFX1RPS0VOIiksCiAgICAgICAgICAgICJ1cmwiOiAiaHR0cHM6Ly9zb25hcmNsb3VkLmlvIiwKICAgICAgICB9LAogICAgfSwKKQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="c1"># 即使只使用一个，也要包含两个服务器</span>
</span></span><span class="line"><span class="cl"><span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="n">envs</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;ANTHROPIC_API_KEY&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="n">mcp</span><span class="o">=</span><span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="s2">&#34;githubOfficial&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;githubPersonalAccessToken&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">        <span class="s2">&#34;sonarqube&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;org&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_ORG&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;token&#34;</span><span class="p">:</span> <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;SONARQUBE_TOKEN&#34;</span><span class="p">),</span>
</span></span><span class="line"><span class="cl">            <span class="s2">&#34;url&#34;</span><span class="p">:</span> <span class="s2">&#34;https://sonarcloud.io&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="p">},</span>
</span></span><span class="line"><span class="cl">    <span class="p">},</span>
</span></span><span class="line"><span class="cl"><span class="p">)</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## Claude 无法访问私有仓库

问题："I don't have access to that repository"（我无权访问该仓库）。

解决方案：

1. 验证您的 GitHub 令牌具有 `repo` 权限范围（不仅仅是 `public_repo`）。
2. 先使用公共仓库进行测试。
3. 确保 `.env` 中的仓库所有者和名称正确：

   






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
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'R0lUSFVCX09XTkVSPXlvdXJfZ2l0aHViX3VzZXJuYW1lCkdJVEhVQl9SRVBPPXlvdXJfcmVwb3NpdG9yeV9uYW1l', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-plaintext" data-lang="plaintext"><span class="line"><span class="cl">GITHUB_OWNER=your_github_username
</span></span><span class="line"><span class="cl">GITHUB_REPO=your_repository_name</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
        x-data="{ code: 'R0lUSFVCX09XTkVSPXlvdXJfZ2l0aHViX3VzZXJuYW1lCkdJVEhVQl9SRVBPPXlvdXJfcmVwb3NpdG9yeV9uYW1l', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-plaintext" data-lang="plaintext"><span class="line"><span class="cl">GITHUB_OWNER=your_github_username
</span></span><span class="line"><span class="cl">GITHUB_REPO=your_repository_name</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 工作流超时或运行时间过长

问题：工作流未完成或 Claude 额度耗尽。

解决方案：

1. 对于复杂的工作流，使用 `timeoutMs: 0`（TypeScript）或 `timeout_ms=0`（Python）以允许无限制时间：

   






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
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'YXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICBgZWNobyAnJHtwcm9tcHR9JyB8IGNsYXVkZSAtcCAtLWRhbmdlcm91c2x5LXNraXAtcGVybWlzc2lvbnNgLAogIHsKICAgIHRpbWVvdXRNczogMCwgLy8g5peg6LaF5pe2CiAgICBvblN0ZG91dDogY29uc29sZS5sb2csCiAgICBvblN0ZGVycjogY29uc29sZS5sb2csCiAgfSwKKTs=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">commands</span><span class="p">.</span><span class="nx">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">  <span class="sb">`echo &#39;</span><span class="si">${</span><span class="nx">prompt</span><span class="si">}</span><span class="sb">&#39; | claude -p --dangerously-skip-permissions`</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nx">timeoutMs</span>: <span class="kt">0</span><span class="p">,</span> <span class="c1">// 无超时
</span></span></span><span class="line"><span class="cl">    <span class="nx">onStdout</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nx">onStderr</span>: <span class="kt">console.log</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="p">},</span>
</span></span><span class="line"><span class="cl"><span class="p">);</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
        x-data="{ code: 'YXdhaXQgc2J4LmNvbW1hbmRzLnJ1bigKICAgIGYiZWNobyAne3Byb21wdH0nIHwgY2xhdWRlIC1wIC0tZGFuZ2Vyb3VzbHktc2tpcC1wZXJtaXNzaW9ucyIsCiAgICB0aW1lb3V0X21zPTAsICAjIOaXoOi2heaXtgogICAgb25fc3Rkb3V0PXByaW50LAogICAgb25fc3RkZXJyPXByaW50LAop', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">commands</span><span class="o">.</span><span class="n">run</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="sa">f</span><span class="s2">&#34;echo &#39;</span><span class="si">{</span><span class="n">prompt</span><span class="si">}</span><span class="s2">&#39; | claude -p --dangerously-skip-permissions&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="n">timeout_ms</span><span class="o">=</span><span class="mi">0</span><span class="p">,</span>  <span class="c1"># 无超时</span>
</span></span><span class="line"><span class="cl">    <span class="n">on_stdout</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="n">on_stderr</span><span class="o">=</span><span class="nb">print</span><span class="p">,</span>
</span></span><span class="line"><span class="cl"><span class="p">)</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


2. 将复杂的工作流分解为更小、更专注的任务。
3. 监控您的 Anthropic API 额度使用情况。
4. 在提示中添加检查点：“完成每一步后，在继续之前显示进度”。

## 沙盒清理错误

问题：沙盒未被正确清理，导致资源耗尽。

解决方案：始终在 `finally` 块中使用适当的错误处理进行清理：








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
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'YXN5bmMgZnVuY3Rpb24gcm9idXN0V29ya2Zsb3coKSB7CiAgbGV0IHNieDogU2FuZGJveCB8IHVuZGVmaW5lZDsKCiAgdHJ5IHsKICAgIHNieCA9IGF3YWl0IFNhbmRib3guYmV0YUNyZWF0ZSh7CiAgICAgIC8vIC4uLiDphY3nva4KICAgIH0pOwoKICAgIC8vIC4uLiDlt6XkvZzmtYHpgLvovpEKICB9IGNhdGNoIChlcnJvcikgewogICAgY29uc29sZS5lcnJvcigiV29ya2Zsb3cgZmFpbGVkOiIsIGVycm9yKTsKICAgIHByb2Nlc3MuZXhpdCgxKTsKICB9IGZpbmFsbHkgewogICAgaWYgKHNieCkgewogICAgICBjb25zb2xlLmxvZygiQ2xlYW5pbmcgdXAgc2FuZGJveC4uLiIpOwogICAgICBhd2FpdCBzYngua2lsbCgpOwogICAgfQogIH0KfQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">robustWorkflow() {</span>
</span></span><span class="line"><span class="cl">  <span class="kd">let</span> <span class="nx">sbx</span>: <span class="kt">Sandbox</span> <span class="o">|</span> <span class="kc">undefined</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">try</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nx">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="nx">Sandbox</span><span class="p">.</span><span class="nx">betaCreate</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">      <span class="c1">// ... 配置
</span></span></span><span class="line"><span class="cl">    <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="c1">// ... 工作流逻辑
</span></span></span><span class="line"><span class="cl">  <span class="p">}</span> <span class="k">catch</span> <span class="p">(</span><span class="nx">error</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nx">console</span><span class="p">.</span><span class="nx">error</span><span class="p">(</span><span class="s2">&#34;Workflow failed:&#34;</span><span class="p">,</span> <span class="nx">error</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">    <span class="nx">process</span><span class="p">.</span><span class="nx">exit</span><span class="p">(</span><span class="mi">1</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span> <span class="k">finally</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">if</span> <span class="p">(</span><span class="nx">sbx</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">console</span><span class="p">.</span><span class="nx">log</span><span class="p">(</span><span class="s2">&#34;Cleaning up sandbox...&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">      <span class="k">await</span> <span class="nx">sbx</span><span class="p">.</span><span class="nx">kill</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">    <span class="p">}</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
        x-data="{ code: 'YXN5bmMgZGVmIHJvYnVzdF93b3JrZmxvdygpOgogICAgc2J4ID0gTm9uZQoKICAgIHRyeToKICAgICAgICBzYnggPSBhd2FpdCBBc3luY1NhbmRib3guYmV0YV9jcmVhdGUoCiAgICAgICAgICAgICMgLi4uIOmFjee9rgogICAgICAgICkKCiAgICAgICAgIyAuLi4g5bel5L2c5rWB6YC76L6RCgogICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlcnJvcjoKICAgICAgICBwcmludChmIldvcmtmbG93IGZhaWxlZDoge2Vycm9yfSIpCiAgICAgICAgc3lzLmV4aXQoMSkKICAgIGZpbmFsbHk6CiAgICAgICAgaWYgc2J4OgogICAgICAgICAgICBwcmludCgiQ2xlYW5pbmcgdXAgc2FuZGJveC4uLiIpCiAgICAgICAgICAgIGF3YWl0IHNieC5raWxsKCk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="k">async</span> <span class="k">def</span> <span class="nf">robust_workflow</span><span class="p">():</span>
</span></span><span class="line"><span class="cl">    <span class="n">sbx</span> <span class="o">=</span> <span class="kc">None</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">try</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">        <span class="n">sbx</span> <span class="o">=</span> <span class="k">await</span> <span class="n">AsyncSandbox</span><span class="o">.</span><span class="n">beta_create</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">            <span class="c1"># ... 配置</span>
</span></span><span class="line"><span class="cl">        <span class="p">)</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">        <span class="c1"># ... 工作流逻辑</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">except</span> <span class="ne">Exception</span> <span class="k">as</span> <span class="n">error</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&#34;Workflow failed: </span><span class="si">{</span><span class="n">error</span><span class="si">}</span><span class="s2">&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">        <span class="n">sys</span><span class="o">.</span><span class="n">exit</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">    <span class="k">finally</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">        <span class="k">if</span> <span class="n">sbx</span><span class="p">:</span>
</span></span><span class="line"><span class="cl">            <span class="nb">print</span><span class="p">(</span><span class="s2">&#34;Cleaning up sandbox...&#34;</span><span class="p">)</span>
</span></span><span class="line"><span class="cl">            <span class="k">await</span> <span class="n">sbx</span><span class="o">.</span><span class="n">kill</span><span class="p">()</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 环境变量未加载

问题：脚本因环境变量为 "undefined" 或 "None" 而失败。

解决方案：








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
<p>确保在文件顶部加载了 <code>dotenv</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'aW1wb3J0ICJkb3RlbnYvY29uZmlnIjs=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">import</span> <span class="s2">&#34;dotenv/config&#34;</span><span class="p">;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>验证 <code>.env</code> 文件与您的脚本位于同一目录中。</p>
</li>
<li>
<p>检查变量名称是否完全匹配（区分大小写）：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Ly8gLmVudiDmlofku7YKR0lUSFVCX1RPS0VOID0gZ2hwX3h4eHh4OwoKLy8g5Zyo5Luj56CB5LitCnByb2Nlc3MuZW52LkdJVEhVQl9UT0tFTjsgLy8g5q2j56GuCnByb2Nlc3MuZW52LmdpdGh1Yl90b2tlbjsgLy8g6ZSZ6K&#43;vIC0g5aSn5bCP5YaZ5LiN5Yy56YWN', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="c1">// .env 文件
</span></span></span><span class="line"><span class="cl"><span class="nx">GITHUB_TOKEN</span> <span class="o">=</span> <span class="nx">ghp_xxxxx</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1">// 在代码中
</span></span></span><span class="line"><span class="cl"><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">GITHUB_TOKEN</span><span class="p">;</span> <span class="c1">// 正确
</span></span></span><span class="line"><span class="cl"><span class="nx">process</span><span class="p">.</span><span class="nx">env</span><span class="p">.</span><span class="nx">github_token</span><span class="p">;</span> <span class="c1">// 错误 - 大小写不匹配
</span></span></span></code></pre></div>
      
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
<p>确保在文件顶部加载了 <code>dotenv</code>：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ZnJvbSBkb3RlbnYgaW1wb3J0IGxvYWRfZG90ZW52CmxvYWRfZG90ZW52KCk=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="kn">from</span> <span class="nn">dotenv</span> <span class="kn">import</span> <span class="n">load_dotenv</span>
</span></span><span class="line"><span class="cl"><span class="n">load_dotenv</span><span class="p">()</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>验证 <code>.env</code> 文件与您的脚本位于同一目录中。</p>
</li>
<li>
<p>检查变量名称是否完全匹配（区分大小写）：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyAuZW52IOaWh&#43;S7tgpHSVRIVUJfVE9LRU49Z2hwX3h4eHh4CgojIOWcqOS7o&#43;eggeS4rQpvcy5nZXRlbnYoIkdJVEhVQl9UT0tFTiIpICAjIOato&#43;ehrgpvcy5nZXRlbnYoImdpdGh1Yl90b2tlbiIpICAjIOmUmeivryAtIOWkp&#43;Wwj&#43;WGmeS4jeWMuemFjQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="c1"># .env 文件</span>
</span></span><span class="line"><span class="cl"><span class="n">GITHUB_TOKEN</span><span class="o">=</span><span class="n">ghp_xxxxx</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 在代码中</span>
</span></span><span class="line"><span class="cl"><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;GITHUB_TOKEN&#34;</span><span class="p">)</span>  <span class="c1"># 正确</span>
</span></span><span class="line"><span class="cl"><span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="s2">&#34;github_token&#34;</span><span class="p">)</span>  <span class="c1"># 错误 - 大小写不匹配</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
  </div>
</div>


## SonarQube 返回空结果

问题：SonarQube 分析未返回任何项目或问题。

解决方案：

1. 验证您的 SonarCloud 组织密钥是否正确。
2. 确保您在 SonarCloud 中至少配置了一个项目。
3. 检查您的 SonarQube 令牌是否具有必要的权限。
4. 确认您的项目已在 SonarCloud 中至少分析过一次。
