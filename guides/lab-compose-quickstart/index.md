# 实验：Docker Compose 快速上手


使用 Docker Compose 构建一个 Python Flask 与 Redis 的访问计数应用，从一个
最简的 `compose.yaml` 开始，在每一步中逐步加入生产级
特性。

## 启动实验













<ol>
<li>
<p>Start the labspace:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgY29tcG9zZSAtcCBsYWJzcGFjZSAtZiBvY2k6Ly9kb2NrZXJzYW1wbGVzL2xhYnNwYWNlLWNvbXBvc2UtcXVpY2tzdGFydCB1cCAtZA==', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker compose -p labspace -f oci://dockersamples/labspace-compose-quickstart up -d
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>Open your browser to <a class="link" href="http://localhost:3030" rel="noopener">http://localhost:3030</a>.</p>
</li>
<li>
<p>When you're done, tear down the labspace:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgY29tcG9zZSAtcCBsYWJzcGFjZSBkb3du', copying: false }"
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
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path d="M7.5 3.375c0-1.036.84-1.875 1.875-1.875h.375a3.75 3.75 0 0 1 3.75 3.75v1.875C13.5 8.161 14.34 9 15.375 9h1.875A3.75 3.75 0 0 1 21 12.75v3.375C21 17.16 20.16 18 19.125 18h-9.75A1.875 1.875 0 0 1 7.5 16.125V3.375Z"/>
  <path d="M15 5.25a5.23 5.23 0 0 0-1.279-3.434 9.768 9.768 0 0 1 6.963 6.963A5.23 5.23 0 0 0 17.25 7.5h-1.875A.375.375 0 0 1 15 7.125V5.25ZM4.875 6H6v10.125A3.375 3.375 0 0 0 9.375 19.5H16.5v1.125c0 1.035-.84 1.875-1.875 1.875h-9.75A1.875 1.875 0 0 1 3 20.625V7.875C3 6.839 3.84 6 4.875 6Z"/>
</svg>
</span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" data-slot="icon">
  <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd"/>
</svg>
</span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker compose -p labspace down
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>



## 你将学到什么

完成本 Labspace 后，你将掌握以下内容：

- 在 `compose.yaml` 文件中定义多服务应用，并用 Compose 命令管理它
- 使用健康检查和 `depends_on` 条件控制服务的启动顺序
- 使用 Compose watch 模式迭代代码，无需手动重新构建
- 使用命名卷让数据在容器重启后依然保留
- 使用 `include` 指令将技术栈拆分到多个文件中实现模块化
- 使用 `config`、`logs` 和 `exec` 检查并调试运行中的技术栈

## 模块

| #   | 模块                             | 说明                                                                  |
| --- | -------------------------------- | --------------------------------------------------------------------- |
| 1   | 引言                             | 浏览初始应用并验证环境                                                |
| 2   | 定义服务                         | 编写第一个 `compose.yaml`，启动 Flask 与 Redis 技术栈                 |
| 3   | 健康检查与启动顺序               | 添加 Redis 健康检查和 `depends_on`，消除竞态条件                      |
| 4   | 使用 watch 模式实时开发          | 配置 watch 模式，无需手动重建即可同步代码变更                         |
| 5   | 持久化与调试                     | 添加命名卷，让 Redis 数据在 `docker compose down` 后依然保留          |
| 6   | 使用多个 Compose 文件            | 将 Redis 抽取到 `infra.yaml`，并用 `include` 组合各文件               |
| 7   | 其他命令                         | 使用 `config`、`logs -f` 和 `exec` 检查运行中的技术栈                 |
| 8   | 回顾                             | 回顾所构建的内容并探索后续步骤                                        |

