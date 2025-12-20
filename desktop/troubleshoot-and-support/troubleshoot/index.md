# 排查 Docker Desktop 问题

本页包含有关如何诊断和排查 Docker Desktop 问题的信息，以及如何查看日志。

## 故障排查菜单

要导航到 **故障排查**，请执行以下任一操作：

- 选择 Docker 菜单 Docker 菜单 





<img
  loading="lazy"
  src="../../images/whale-x.svg"
  alt="whale menu"
  
  class="inline my-0 not-prose"
/>
，然后选择 **故障排查**。
- 选择 Docker 仪表板右上角附近的 **故障排查** 图标。

**故障排查** 菜单包含以下选项：

- **重启 Docker Desktop**。

- **重置 Kubernetes 集群**。选择此选项可删除所有堆栈和 Kubernetes 资源。有关更多信息，请参阅 [Kubernetes](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes)。

- **清理/清除数据**。此选项会重置所有 Docker 数据，但不会重置为出厂默认设置。选择此选项会导致现有设置丢失。

- **重置为出厂默认设置**：选择此选项可将 Docker Desktop 上的所有选项重置为其初始状态，与首次安装 Docker Desktop 时相同。

如果您是 Mac 或 Linux 用户，还可以选择从系统中 **卸载** Docker Desktop。

## 诊断

> [!TIP]
>
> 如果在故障排查中找不到解决方案，请浏览 GitHub 仓库或创建新问题：
>
> - [docker/for-mac](https://github.com/docker/for-mac/issues)
> - [docker/for-win](https://github.com/docker/for-win/issues)
> - [docker/desktop-linux](https://github.com/docker/desktop-linux/issues)

### 从应用内诊断

1. 在 **故障排查** 中，选择 **获取支持**。这将打开应用内支持页面并开始收集诊断信息。
2. 当诊断信息收集过程完成后，选择 **上传以获取诊断 ID**。
3. 当诊断信息上传后，Docker Desktop 会打印一个诊断 ID。复制此 ID。
4. 使用您的诊断 ID 获取帮助：
   - 如果您有付费 Docker 订阅，请选择 **联系支持**。这将打开 Docker Desktop 支持表单。填写所需信息，并将您在步骤三中复制的 ID 添加到 **诊断 ID 字段**。然后，选择 **提交工单** 以请求 Docker Desktop 支持。
     > [!NOTE]
     >
     > 您必须登录 Docker Desktop 才能访问支持表单。有关 Docker Desktop 支持涵盖的内容，请参阅 [支持](/manuals/support/_index.md)。
   - 如果您没有付费 Docker 订阅，请选择 **报告 Bug** 以在 GitHub 上打开新的 Docker Desktop 问题。填写所需信息，并确保添加您在步骤三中复制的诊断 ID。

### 从错误消息诊断

1. 当出现错误消息时，选择 **收集诊断信息**。
2. 当诊断信息上传后，Docker Desktop 会打印一个诊断 ID。复制此 ID。
3. 使用您的诊断 ID 获取帮助：
   - 如果您有付费 Docker 订阅，请选择 **联系支持**。这将打开 Docker Desktop 支持表单。填写所需信息，并将您在步骤三中复制的 ID 添加到 **诊断 ID 字段**。然后，选择 **提交工单** 以请求 Docker Desktop 支持。
     > [!NOTE]
     >
     > 您必须登录 Docker Desktop 才能访问支持表单。有关 Docker Desktop 支持涵盖的内容，请参阅 [支持](/manuals/support/_index.md)。
   - 如果您没有付费 Docker 订阅，您可以在 GitHub 上为 [Mac](https://github.com/docker/for-mac/issues)、[Windows](https://github.com/docker/for-win/issues) 或 [Linux](https://github.com/docker/for-linux/issues) 打开新的 Docker Desktop 问题。填写所需信息，并确保添加步骤二中打印的诊断 ID。

### 从终端诊断

在某些情况下，自己运行诊断很有用，例如，如果 Docker Desktop 无法启动。








<div
  class="tabs"
  
    
      x-data="{ selected: 'Windows' }"
    
    @tab-select.window="$event.detail.group === 'os' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Windows'})"
        
      >
        Windows
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Mac'})"
        
      >
        Mac
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Linux'})"
        
      >
        Linux
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows' && 'hidden'"
      >
        <ol>
<li>
<p>找到 <code>com.docker.diagnose</code> 工具：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBDOlxQcm9ncmFtIEZpbGVzXERvY2tlclxEb2NrZXJccmVzb3VyY2VzXGNvbS5kb2NrZXIuZGlhZ25vc2UuZXhl', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> C:<span class="se">\P</span>rogram Files<span class="se">\D</span>ocker<span class="se">\D</span>ocker<span class="se">\r</span>esources<span class="se">\c</span>om.docker.diagnose.exe
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>创建并上传诊断 ID。在 PowerShell 中运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAmICJDOlxQcm9ncmFtIEZpbGVzXERvY2tlclxEb2NrZXJccmVzb3VyY2VzXGNvbS5kb2NrZXIuZGlhZ25vc2UuZXhlIiBnYXRoZXIgLXVwbG9hZA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="p">&amp;</span> <span class="s2">&#34;C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe&#34;</span> gather -upload
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>
<p>诊断完成后，终端会显示您的诊断 ID 和诊断文件的路径。诊断 ID 由您的用户 ID 和时间戳组成。例如 <code>BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051</code>。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac' && 'hidden'"
      >
        <ol>
<li>
<p>找到 <code>com.docker.diagnose</code> 工具：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAvQXBwbGljYXRpb25zL0RvY2tlci5hcHAvQ29udGVudHMvTWFjT1MvY29tLmRvY2tlci5kaWFnbm9zZQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> /Applications/Docker.app/Contents/MacOS/com.docker.diagnose
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>创建并上传诊断 ID。运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAvQXBwbGljYXRpb25zL0RvY2tlci5hcHAvQ29udGVudHMvTWFjT1MvY29tLmRvY2tlci5kaWFnbm9zZSBnYXRoZXIgLXVwbG9hZA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> /Applications/Docker.app/Contents/MacOS/com.docker.diagnose gather -upload
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>
<p>诊断完成后，终端会显示您的诊断 ID 和诊断文件的路径。诊断 ID 由您的用户 ID 和时间戳组成。例如 <code>BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051</code>。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Linux' && 'hidden'"
      >
        <ol>
<li>
<p>找到 <code>com.docker.diagnose</code> 工具：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAvb3B0L2RvY2tlci1kZXNrdG9wL2Jpbi9jb20uZG9ja2VyLmRpYWdub3Nl', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> /opt/docker-desktop/bin/com.docker.diagnose
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>创建并上传诊断 ID。运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAvb3B0L2RvY2tlci1kZXNrdG9wL2Jpbi9jb20uZG9ja2VyLmRpYWdub3NlIGdhdGhlciAtdXBsb2Fk', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> /opt/docker-desktop/bin/com.docker.diagnose gather -upload
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>
<p>诊断完成后，终端会显示您的诊断 ID 和诊断文件的路径。诊断 ID 由您的用户 ID 和时间戳组成。例如 <code>BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051</code>。</p>

      </div>
    
  </div>
</div>


要查看诊断文件的内容：








<div
  class="tabs"
  
    
      x-data="{ selected: 'Windows' }"
    
    @tab-select.window="$event.detail.group === 'os' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Windows'})"
        
      >
        Windows
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Mac'})"
        
      >
        Mac
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Linux'})"
        
      >
        Linux
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows' && 'hidden'"
      >
        <ol>
<li>
<p>解压文件。在 PowerShell 中，将诊断文件的路径复制并粘贴到以下命令中，然后运行它。它应该类似于以下示例：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBFeHBhbmQtQXJjaGl2ZSAtTGl0ZXJhbFBhdGggIkM6XFVzZXJzXHRlc3RVc2VyXEFwcERhdGFcTG9jYWxcVGVtcFw1REU5OTc4QS0zODQ4LTQyOUUtODc3Ni05NTBGQzg2OTE4NkZcMjAyMzA2MDcxMDE2MDIuemlwIiAtRGVzdGluYXRpb25QYXRoICJDOlxVc2Vyc1x0ZXN0dXNlclxBcHBEYXRhXExvY2FsXFRlbXBcNURFOTk3OEEtMzg0OC00MjlFLTg3NzYtOTUwRkM4NjkxODZGXDIwMjMwNjA3MTAxNjAyIg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-powershell" data-lang="powershell"><span class="line"><span class="cl"><span class="p">$</span> <span class="nb">Expand-Archive</span> <span class="n">-LiteralPath</span> <span class="s2">&#34;C:\Users\testUser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602.zip&#34;</span> <span class="n">-DestinationPath</span> <span class="s2">&#34;C:\Users\testuser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>在您首选的文本编辑器中打开文件。运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBjb2RlIDxwYXRoLXRvLWZpbGU&#43;', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-powershell" data-lang="powershell"><span class="line"><span class="cl"><span class="p">$</span> <span class="n">code</span> <span class="p">&lt;</span><span class="nb">path-to</span><span class="o">-file</span><span class="p">&gt;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac' && 'hidden'"
      >
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
        x-data="{ code: 'JCBvcGVuIC90bXAvPHlvdXItZGlhZ25vc3RpY3MtSUQ&#43;LnppcA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> open /tmp/&lt;your-diagnostics-ID&gt;.zip
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Linux' && 'hidden'"
      >
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
        x-data="{ code: 'JCB1bnppcCDigJNsIC90bXAvPHlvdXItZGlhZ25vc3RpY3MtSUQ&#43;LnppcA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> unzip –l /tmp/&lt;your-diagnostics-ID&gt;.zip
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


#### 使用您的诊断 ID 获取帮助

如果您有付费 Docker 订阅，请选择 **联系支持**。这将打开 Docker Desktop 支持表单。填写所需信息，并将您在步骤三中复制的 ID 添加到 **诊断 ID 字段**。然后，选择 **提交工单** 以请求 Docker Desktop 支持。

如果您没有付费 Docker 订阅，请在 GitHub 上创建问题：

- [Linux 版](https://github.com/docker/desktop-linux/issues)
- [Mac 版](https://github.com/docker/for-mac/issues)
- [Windows 版](https://github.com/docker/for-win/issues)

### 自诊断工具

> [!IMPORTANT]
>
> 此工具已弃用。

## 查看日志

除了使用诊断选项提交日志外，您还可以自己浏览日志。








<div
  class="tabs"
  
    
      x-data="{ selected: 'Windows' }"
    
    @tab-select.window="$event.detail.group === 'os' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Windows'})"
        
      >
        Windows
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Mac'})"
        
      >
        Mac
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'os', name:
          'Linux'})"
        
      >
        Linux
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows' && 'hidden'"
      >
        <p>在 PowerShell 中运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBjb2RlICRFbnY6TE9DQUxBUFBEQVRBXERvY2tlclxsb2c=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-powershell" data-lang="powershell"><span class="line"><span class="cl"><span class="p">$</span> <span class="n">code</span> <span class="nv">$Env:LOCALAPPDATA</span><span class="p">\</span><span class="n">Docker</span><span class="p">\</span><span class="n">log</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>这将在您首选的文本编辑器中打开所有日志供您探索。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac' && 'hidden'"
      >
        
<h3 class=" scroll-mt-20 flex items-center gap-2" id="从终端">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bb%8e%e7%bb%88%e7%ab%af">
    从终端
  </a>
</h3>

<p>要在命令行中查看 Docker Desktop 日志的实时流，请从您首选的 shell 运行以下脚本。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBwcmVkPSdwcm9jZXNzIG1hdGNoZXMgIi4qKG9ja2VyfHZwbmtpdCkuKiIgfHwgKHByb2Nlc3MgaW4geyJ0YXNrZ2F0ZWQtaGVscGVyIiwgImxhdW5jaHNlcnZpY2VzZCIsICJrZXJuZWwifSAmJiBldmVudE1lc3NhZ2UgY29udGFpbnNbY10gImRvY2tlciIpJwokIC91c3IvYmluL2xvZyBzdHJlYW0gLS1zdHlsZSBzeXNsb2cgLS1sZXZlbD1kZWJ1ZyAtLWNvbG9yPWFsd2F5cyAtLXByZWRpY2F0ZSAiJHByZWQi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="nv">pred</span><span class="o">=</span><span class="s1">&#39;process matches &#34;.*(ocker|vpnkit).*&#34; || (process in {&#34;taskgated-helper&#34;, &#34;launchservicesd&#34;, &#34;kernel&#34;} &amp;&amp; eventMessage contains[c] &#34;docker&#34;)&#39;</span>
</span></span><span class="line"><span class="cl"><span class="gp">$</span> /usr/bin/log stream --style syslog --level<span class="o">=</span>debug --color<span class="o">=</span>always --predicate <span class="s2">&#34;</span><span class="nv">$pred</span><span class="s2">&#34;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>或者，要将最近一天的日志 (<code>1d</code>) 收集到文件中，请运行：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCAvdXNyL2Jpbi9sb2cgc2hvdyAtLWRlYnVnIC0taW5mbyAtLXN0eWxlIHN5c2xvZyAtLWxhc3QgMWQgLS1wcmVkaWNhdGUgIiRwcmVkIiA&#43;L3RtcC9sb2dzLnR4dA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> /usr/bin/log show --debug --info --style syslog --last 1d --predicate <span class="s2">&#34;</span><span class="nv">$pred</span><span class="s2">&#34;</span> &gt;/tmp/logs.txt
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h3 class=" scroll-mt-20 flex items-center gap-2" id="从控制台应用">
  <a class="text-black dark:text-white no-underline hover:underline" href="#%e4%bb%8e%e6%8e%a7%e5%88%b6%e5%8f%b0%e5%ba%94%e7%94%a8">
    从控制台应用
  </a>
</h3>

<p>Mac 提供了一个名为 <strong>控制台</strong> 的内置日志查看器，您可以使用它来检查 Docker 日志。</p>
<p>控制台位于 <code>/Applications/Utilities</code>。您可以使用 Spotlight 搜索找到它。</p>
<p>要读取 Docker 应用日志消息，请在控制台窗口搜索栏中键入 <code>docker</code> 并按 Enter。然后选择 <code>ANY</code> 以展开 <code>docker</code> 搜索条目旁边的下拉列表，并选择 <code>Process</code>。</p>

  
  
    








<figure
  x-data="{ zoom: false }"
  @click="zoom = ! zoom"
  class="cursor-pointer hover:opacity-90"
>
  <img
    loading="lazy"
    src="/desktop/images/console.png"
    alt="Mac 控制台搜索 Docker 应用"
    
    
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
        src="/desktop/images/console.png"
        alt="Mac 控制台搜索 Docker 应用"
      />
    </div>
  </template>
</figure>
<p>您可以使用控制台日志查询来搜索日志、以各种方式过滤结果并创建报告。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Linux' && 'hidden'"
      >
        <p>您可以通过运行以下命令访问 Docker Desktop 日志：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBqb3VybmFsY3RsIC0tdXNlciAtLXVuaXQ9ZG9ja2VyLWRlc2t0b3A=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> journalctl --user --unit<span class="o">=</span>docker-desktop
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>您还可以在 <code>$HOME/.docker/desktop/log/</code> 中找到 Docker Desktop 中包含的内部组件的日志。</p>

      </div>
    
  </div>
</div>


## 查看 Docker 守护进程日志

请参阅 [读取守护进程日志](/manuals/engine/daemon/logs.md) 部分，了解如何查看 Docker 守护进程日志。

## 更多资源

- 查看特定的 [故障排查主题](topics.md)。
- 查看 [已知问题](known-issues.md) 信息
- [修复 macOS 上的 "Docker.app 已损坏" 问题](mac-damaged-dialog.md) - 解决 macOS 安装问题
- [获取 Docker 产品支持](/manuals/support/_index.md)

- [Docker Desktop 故障排除主题](/desktop/troubleshoot-and-support/troubleshoot/topics/)

- [已知问题](/desktop/troubleshoot-and-support/troubleshoot/known-issues/)

- [修复 macOS 上“Docker.app 已损坏，无法打开”的问题](/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/)

