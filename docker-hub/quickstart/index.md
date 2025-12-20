# Docker Hub 快速入门

Docker Hub 提供了庞大的预构建镜像和资源库，能够加速开发工作流并减少设置时间。您可以基于 Docker Hub 的预构建镜像进行构建，然后使用仓库与您的团队或数百万其他开发者分享和分发您自己的镜像。

本指南将指导您如何查找并运行预构建镜像。随后，您将学习创建自定义镜像并通过 Docker Hub 进行分享。

## 前提条件

- [下载并安装 Docker](../../get-started/get-docker.md)
- [创建 Docker 账户](https://app.docker.com/signup)

## 步骤 1：在 Docker Hub 库中查找镜像

您可以在 Docker Hub 网站、Docker Desktop 仪表板中搜索内容，或者使用 CLI 进行搜索。

要在 Docker Hub 上搜索或浏览内容：








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Hub' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Hub' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Hub'"
        
      >
        Docker Hub
      </button>
    
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
        :class="selected !== 'Docker-Hub' && 'hidden'"
      >
        <ol>
<li>
<p>导航至 <a class="link" href="https://hub.docker.com/explore" rel="noopener">Docker Hub 探索页面</a>。</p>
<p>在 <strong>Explore</strong> 页面上，您可以按目录或类别浏览，或者使用搜索功能快速找到内容。</p>
</li>
<li>
<p>在 <strong>Categories</strong> 下，选择 <strong>Web servers</strong>。</p>
<p>结果显示后，您可以使用页面左侧的筛选器进一步筛选结果。</p>
</li>
<li>
<p>在筛选器中，选择 <strong>Docker Official Image</strong>。</p>
<p>按可信内容筛选可确保您只看到由 Docker 和经验证的发布合作伙伴策划的高质量、安全的镜像。</p>
</li>
<li>
<p>在结果中，选择 <strong>nginx</strong> 镜像。</p>
<p>选择镜像将打开镜像页面，您可以在其中了解有关如何使用该镜像的更多信息。在该页面上，您还可以找到用于拉取镜像的 <code>docker pull</code> 命令。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <ol>
<li>
<p>打开 Docker Desktop 仪表板。</p>
</li>
<li>
<p>选择 <strong>Docker Hub</strong> 视图。</p>
<p>在 <strong>Docker Hub</strong> 视图中，您可以按目录或类别浏览，或者使用搜索功能快速找到内容。</p>
</li>
<li>
<p>将搜索框留空，然后选择 <strong>Search</strong>。</p>
<p>搜索结果将显示在搜索框旁边，现在还附带了额外的筛选器。</p>
</li>
<li>
<p>选择搜索筛选器图标，然后选择 <strong>Docker Official Image</strong> 和 <strong>Web Servers</strong>。</p>
</li>
<li>
<p>在结果中，选择 <strong>nginx</strong> 镜像。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <ol>
<li>
<p>打开终端窗口。</p>


  

  <blockquote
    
    class="admonition admonition-tip admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_5432_1749" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="4" y="1" width="17" height="22">
<path d="M9.93896 22H14.939M10.439 10H14.439M12.439 10L12.439 16M15.439 15.3264C17.8039 14.2029 19.439 11.7924 19.439 9C19.439 5.13401 16.305 2 12.439 2C8.57297 2 5.43896 5.13401 5.43896 9C5.43896 11.7924 7.07402 14.2029 9.43896 15.3264V16C9.43896 16.9319 9.43896 17.3978 9.59121 17.7654C9.79419 18.2554 10.1835 18.6448 10.6736 18.8478C11.0411 19 11.5071 19 12.439 19C13.3708 19 13.8368 19 14.2043 18.8478C14.6944 18.6448 15.0837 18.2554 15.2867 17.7654C15.439 17.3978 15.439 16.9319 15.439 16V15.3264Z" stroke="#6C7E9D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#mask0_5432_1749)">
<rect width="24" height="24" fill="currentColor" fill-opacity="0.8"/>
</g>
</svg>

      </span>
      <span class="admonition-title">
        Tip
      </span>
    </div>
    <div class="admonition-content">
      <p>Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 <strong>&gt;_ Terminal</strong> 即可打开它。</p>
    </div>
  </blockquote>

</li>
<li>
<p>在终端中，运行以下命令。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgc2VhcmNoIC0tZmlsdGVyIGlzLW9mZmljaWFsPXRydWUgbmdpbng=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker search --filter is-official<span class="o">=</span><span class="nb">true</span> nginx
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>与 Docker Hub 和 Docker Desktop 界面不同，您无法使用 <code>docker search</code> 命令按类别浏览。有关该命令的更多详细信息，请参阅 
  <a class="link" href="/reference/cli/docker/search/">docker search</a>。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


现在您已经找到了镜像，是时候将其拉取并在您的设备上运行了。

## 步骤 2：从 Docker Hub 拉取并运行镜像

您可以使用 CLI 或 Docker Desktop 仪表板运行来自 Docker Hub 的镜像。








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
<p>在 Docker Desktop 仪表板中，在 <strong>Docker Hub</strong> 视图中选择 <strong>nginx</strong> 镜像。更多详情，请参阅 <a class="link" href="#%e6%ad%a5%e9%aa%a4-1%e5%9c%a8-docker-hub-%e5%ba%93%e4%b8%ad%e6%9f%a5%e6%89%be%e9%95%9c%e5%83%8f">步骤 1：在 Docker Hub 库中查找镜像</a>。</p>
</li>
<li>
<p>在 <strong>nginx</strong> 屏幕上，选择 <strong>Run</strong>。</p>
<p>如果镜像在您的设备上不存在，它会自动从 Docker Hub 拉取。拉取镜像可能需要几秒或几分钟，具体取决于您的连接速度。镜像拉取完成后，Docker Desktop 中会出现一个窗口，您可以在其中指定运行选项。</p>
</li>
<li>
<p>在 <strong>Host port</strong> 选项中，指定 <code>8080</code>。</p>
</li>
<li>
<p>选择 <strong>Run</strong>。</p>
<p>容器启动后，容器日志将显示出来。</p>
</li>
<li>
<p>选择 <strong>8080:80</strong> 链接以打开服务器，或者在您的 Web 浏览器中访问 <a class="link" href="http://localhost:8080" rel="noopener">http://localhost:8080</a>。</p>
</li>
<li>
<p>在 Docker Desktop 仪表板中，选择 <strong>Stop</strong> 按钮以停止容器。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
      >
        <ol>
<li>
<p>打开终端窗口。</p>


  

  <blockquote
    
    class="admonition admonition-tip admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_5432_1749" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="4" y="1" width="17" height="22">
<path d="M9.93896 22H14.939M10.439 10H14.439M12.439 10L12.439 16M15.439 15.3264C17.8039 14.2029 19.439 11.7924 19.439 9C19.439 5.13401 16.305 2 12.439 2C8.57297 2 5.43896 5.13401 5.43896 9C5.43896 11.7924 7.07402 14.2029 9.43896 15.3264V16C9.43896 16.9319 9.43896 17.3978 9.59121 17.7654C9.79419 18.2554 10.1835 18.6448 10.6736 18.8478C11.0411 19 11.5071 19 12.439 19C13.3708 19 13.8368 19 14.2043 18.8478C14.6944 18.6448 15.0837 18.2554 15.2867 17.7654C15.439 17.3978 15.439 16.9319 15.439 16V15.3264Z" stroke="#6C7E9D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#mask0_5432_1749)">
<rect width="24" height="24" fill="currentColor" fill-opacity="0.8"/>
</g>
</svg>

      </span>
      <span class="admonition-title">
        Tip
      </span>
    </div>
    <div class="admonition-content">
      <p>Docker Desktop 仪表板包含一个内置终端。在仪表板底部，选择 <strong>&gt;_ Terminal</strong> 即可打开它。</p>
    </div>
  </blockquote>

</li>
<li>
<p>在您的终端中，运行以下命令以拉取并运行 Nginx 镜像。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC1wIDgwODA6ODAgLS1ybSBuZ2lueA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run -p 8080:80 --rm nginx
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p><code>docker run</code> 命令会自动拉取并运行镜像，无需先运行 <code>docker pull</code>。要了解有关该命令及其选项的更多信息，请参阅 <a class="link" href="/reference/cli/docker/container/run/"><code>docker run</code> CLI 参考</a>。运行命令后，您应该会看到类似以下的输出。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'VW5hYmxlIHRvIGZpbmQgaW1hZ2UgJ25naW54OmxhdGVzdCcgbG9jYWxseQpsYXRlc3Q6IFB1bGxpbmcgZnJvbSBsaWJyYXJ5L25naW54CmE0ODBhNDk2YmE5NTogUHVsbCBjb21wbGV0ZQpmM2FjZTFiOGNlNDU6IFB1bGwgY29tcGxldGUKMTFkNmZkZDBlOGE3OiBQdWxsIGNvbXBsZXRlCmYxMDkxZGE2ZmQ1YzogUHVsbCBjb21wbGV0ZQo0MGVlYTA3YjUzZDg6IFB1bGwgY29tcGxldGUKNjQ3Njc5NGU1MGY0OiBQdWxsIGNvbXBsZXRlCjcwODUwYjNlYzZiMjogUHVsbCBjb21wbGV0ZQpEaWdlc3Q6IHNoYTI1NjoyODQwMmRiNjlmZWM3YzE3ZTE3OWVhODc4ODI2NjdmMWUwNTQzOTExMzhmNzdmZmFmMGMzZWIzODhlZmMzZmZiClN0YXR1czogRG93bmxvYWRlZCBuZXdlciBpbWFnZSBmb3Igbmdpbng6bGF0ZXN0Ci9kb2NrZXItZW50cnlwb2ludC5zaDogL2RvY2tlci1lbnRyeXBvaW50LmQvIGlzIG5vdCBlbXB0eSwgd2lsbCBhdHRlbXB0IHRvIHBlcmZvcm0gY29uZmlndXJhdGlvbgovZG9ja2VyLWVudHJ5cG9pbnQuc2g6IExvb2tpbmcgZm9yIHNoZWxsIHNjcmlwdHMgaW4gL2RvY2tlci1lbnRyeXBvaW50LmQvCi9kb2NrZXItZW50cnlwb2ludC5zaDogTGF1bmNoaW5nIC9kb2NrZXItZW50cnlwb2ludC5kLzEwLWxpc3Rlbi1vbi1pcHY2LWJ5LWRlZmF1bHQuc2gKMTAtbGlzdGVuLW9uLWlwdjYtYnktZGVmYXVsdC5zaDogaW5mbzogR2V0dGluZyB0aGUgY2hlY2tzdW0gb2YgL2V0Yy9uZ2lueC9jb25mLmQvZGVmYXVsdC5jb25mCjEwLWxpc3Rlbi1vbi1pcHY2LWJ5LWRlZmF1bHQuc2g6IGluZm86IEVuYWJsZWQgbGlzdGVuIG9uIElQdjYgaW4gL2V0Yy9uZ2lueC9jb25mLmQvZGVmYXVsdC5jb25mCi9kb2NrZXItZW50cnlwb2ludC5zaDogU291cmNpbmcgL2RvY2tlci1lbnRyeXBvaW50LmQvMTUtbG9jYWwtcmVzb2x2ZXJzLmVudnNoCi9kb2NrZXItZW50cnlwb2ludC5zaDogTGF1bmNoaW5nIC9kb2NrZXItZW50cnlwb2ludC5kLzIwLWVudnN1YnN0LW9uLXRlbXBsYXRlcy5zaAovZG9ja2VyLWVudHJ5cG9pbnQuc2g6IExhdW5jaGluZyAvZG9ja2VyLWVudHJ5cG9pbnQuZC8zMC10dW5lLXdvcmtlci1wcm9jZXNzZXMuc2gKL2RvY2tlci1lbnRyeXBvaW50LnNoOiBDb25maWd1cmF0aW9uIGNvbXBsZXRlOyByZWFkeSBmb3Igc3RhcnQgdXAKMjAyNC8xMS8wNyAyMTo0Mzo0MSBbbm90aWNlXSAxIzE6IHVzaW5nIHRoZSAiZXBvbGwiIGV2ZW50IG1ldGhvZAoyMDI0LzExLzA3IDIxOjQzOjQxIFtub3RpY2VdIDEjMTogbmdpbngvMS4yNy4yCjIwMjQvMTEvMDcgMjE6NDM6NDEgW25vdGljZV0gMSMxOiBidWlsdCBieSBnY2MgMTIuMi4wIChEZWJpYW4gMTIuMi4wLTE0KQoyMDI0LzExLzA3IDIxOjQzOjQxIFtub3RpY2VdIDEjMTogT1M6IExpbnV4IDYuMTAuMTEtbGludXhraXQKMjAyNC8xMS8wNyAyMTo0Mzo0MSBbbm90aWNlXSAxIzE6IGdldHJsaW1pdChSTElNSVRfTk9GSUxFKTogMTA0ODU3NjoxMDQ4NTc2CjIwMjQvMTEvMDcgMjE6NDM6NDEgW25vdGljZV0gMSMxOiBzdGFydCB3b3JrZXIgcHJvY2Vzc2VzCjIwMjQvMTEvMDcgMjE6NDM6NDEgW25vdGljZV0gMSMxOiBzdGFydCB3b3JrZXIgcHJvY2VzcyAyOQouLi4=', copying: false }"
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
      
        <div
          x-data="{ collapse: true }"
          class="relative overflow-clip"
          x-init="$watch('collapse', value => $refs.root.scrollIntoView({ behavior: 'smooth'}))"
        >
          <div
            x-show="collapse"
            class="absolute z-10 flex h-32 w-full flex-col-reverse items-center overflow-clip pb-4"
          >
            <button @click="collapse = false" class="chip">
              <span>Show more</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
              >
            </button>
          </div>
          <div :class="{ 'h-32': collapse }">
            <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">Unable to find image &#39;nginx:latest&#39; locally
</span></span></span><span class="line"><span class="cl"><span class="go">latest: Pulling from library/nginx
</span></span></span><span class="line"><span class="cl"><span class="go">a480a496ba95: Pull complete
</span></span></span><span class="line"><span class="cl"><span class="go">f3ace1b8ce45: Pull complete
</span></span></span><span class="line"><span class="cl"><span class="go">11d6fdd0e8a7: Pull complete
</span></span></span><span class="line"><span class="cl"><span class="go">f1091da6fd5c: Pull complete
</span></span></span><span class="line"><span class="cl"><span class="go">40eea07b53d8: Pull complete
</span></span></span><span class="line"><span class="cl"><span class="go">6476794e50f4: Pull complete
</span></span></span><span class="line"><span class="cl"><span class="go">70850b3ec6b2: Pull complete
</span></span></span><span class="line"><span class="cl"><span class="go">Digest: sha256:28402db69fec7c17e179ea87882667f1e054391138f77ffaf0c3eb388efc3ffb
</span></span></span><span class="line"><span class="cl"><span class="go">Status: Downloaded newer image for nginx:latest
</span></span></span><span class="line"><span class="cl"><span class="go">/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
</span></span></span><span class="line"><span class="cl"><span class="go">/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
</span></span></span><span class="line"><span class="cl"><span class="go">/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
</span></span></span><span class="line"><span class="cl"><span class="go">10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
</span></span></span><span class="line"><span class="cl"><span class="go">10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
</span></span></span><span class="line"><span class="cl"><span class="go">/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
</span></span></span><span class="line"><span class="cl"><span class="go">/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
</span></span></span><span class="line"><span class="cl"><span class="go">/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
</span></span></span><span class="line"><span class="cl"><span class="go">/docker-entrypoint.sh: Configuration complete; ready for start up
</span></span></span><span class="line"><span class="cl"><span class="go">2024/11/07 21:43:41 [notice] 1#1: using the &#34;epoll&#34; event method
</span></span></span><span class="line"><span class="cl"><span class="go">2024/11/07 21:43:41 [notice] 1#1: nginx/1.27.2
</span></span></span><span class="line"><span class="cl"><span class="go">2024/11/07 21:43:41 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
</span></span></span><span class="line"><span class="cl"><span class="go">2024/11/07 21:43:41 [notice] 1#1: OS: Linux 6.10.11-linuxkit
</span></span></span><span class="line"><span class="cl"><span class="go">2024/11/07 21:43:41 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
</span></span></span><span class="line"><span class="cl"><span class="go">2024/11/07 21:43:41 [notice] 1#1: start worker processes
</span></span></span><span class="line"><span class="cl"><span class="go">2024/11/07 21:43:41 [notice] 1#1: start worker process 29
</span></span></span><span class="line"><span class="cl"><span class="go">...
</span></span></span></code></pre></div>
            <button
              @click="collapse = true"
              x-show="!collapse"
              class="chip mx-auto mt-4 flex items-center  text-sm"
            >
              <span>Hide</span>
              <span class="icon-svg"
                ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
              >
            </button>
          </div>
        </div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>访问 <a class="link" href="http://localhost:8080" rel="noopener">http://localhost:8080</a> 以查看默认的 Nginx 页面，并验证容器是否正在运行。</p>
</li>
<li>
<p>在终端中，按 <kdb>Ctrl+C</kbd> 停止容器。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


您现在已经运行了一个 Web 服务器，无需任何设置或配置。Docker Hub 提供对预构建、即用型容器镜像的即时访问，让您可以快速拉取和运行应用程序，而无需手动安装或配置软件。借助 Docker Hub 庞大的镜像库，您可以轻松地进行实验和部署应用程序，从而提高生产力，使尝试新工具、设置开发环境或在现有软件基础上构建变得更加容易。

您还可以扩展来自 Docker Hub 的镜像，从而快速构建和定制您自己的镜像以满足特定需求。

## 步骤 3：构建镜像并推送到 Docker Hub

1. 创建一个 [Dockerfile](/reference/dockerfile.md) 来指定您的应用程序：

   ```dockerfile
   FROM nginx
   RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/nginx/html/index.html
   ```

   这个 Dockerfile 扩展了来自 Docker Hub 的 Nginx 镜像，以创建一个简单的网站。只需几行代码，您就可以使用 Docker 轻松设置、定制和分享静态网站。

2. 运行以下命令以构建您的镜像。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker build -t <YOUR-USERNAME>/nginx-custom .
   ```

   此命令构建您的镜像并为其打上标签，以便 Docker 了解要将其推送到 Docker Hub 中的哪个仓库。要了解有关该命令及其选项的更多信息，请参阅 [`docker build` CLI 参考](../../reference/cli/docker/buildx/build.md)。运行命令后，您应该会看到类似以下的输出。

   ```console {collapse=true}
   [+] Building 0.6s (6/6) FINISHED                      docker:desktop-linux
    => [internal] load build definition from Dockerfile                  0.0s
    => => transferring dockerfile: 128B                                  0.0s
    => [internal] load metadata for docker.io/library/nginx:latest       0.0s
    => [internal] load .dockerignore                                     0.0s
    => => transferring context: 2B                                       0.0s
    => [1/2] FROM docker.io/library/nginx:latest                         0.1s
    => [2/2] RUN echo "<h1>Hello world from Docker!</h1>" > /usr/share/  0.2s
    => exporting to image                                                0.1s
    => => exporting layers                                               0.0s
    => => writing image sha256:f85ab68f4987847713e87a95c39009a5c9f4ad78  0.0s
    => => naming to docker.io/mobyismyname/nginx-custom                  0.0s
   ```

3. 运行以下命令以测试您的镜像。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker run -p 8080:80 --rm <YOUR-USERNAME>/nginx-custom
   ```

4. 访问 [http://localhost:8080](http://localhost:8080) 以查看页面。您应该会看到 `Hello world from Docker!`。

5. 在终端中，按 CTRL+C 停止容器。

6. 登录 Docker Desktop。在将镜像推送到 Docker Hub 之前，您必须先登录。

7. 运行以下命令将您的镜像推送到 Docker Hub。将 `<YOUR-USERNAME>` 替换为您的 Docker ID。

   ```console
   $ docker push <YOUR-USERNAME>/nginx-custom
   ```

    > [!NOTE]
    >
    > 您必须通过 Docker Desktop 或命令行登录 Docker Hub，并且还必须按照上述步骤正确命名您的镜像。

   该命令将镜像推送到 Docker Hub，并在镜像不存在时自动创建仓库。要了解有关该命令的更多信息，请参阅 [`docker push` CLI 参考](../../reference/cli/docker/image/push.md)。运行命令后，您应该会看到类似以下的输出。

   ```console {collapse=true}
   Using default tag: latest
   The push refers to repository [docker.io/mobyismyname/nginx-custom]
   d0e011850342: Pushed
   e4e9e9ad93c2: Mounted from library/nginx
   6ac729401225: Mounted from library/nginx
   8ce189049cb5: Mounted from library/nginx
   296af1bd2844: Mounted from library/nginx
   63d7ce983cd5: Mounted from library/nginx
   b33db0c3c3a8: Mounted from library/nginx
   98b5f35ea9d3: Mounted from library/nginx
   latest: digest: sha256:7f5223ae866e725a7f86b856c30edd3b86f60d76694df81d90b08918d8de1e3f size: 1985
   ```

  现在您已经创建了仓库并推送了镜像，是时候查看您的仓库并探索其选项了。

## 步骤 4：在 Docker Hub 上查看您的仓库并探索选项

您可以在 Docker Hub 或 Docker Desktop 界面中查看您的 Docker Hub 仓库。








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Hub' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Hub' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Hub'"
        
      >
        Docker Hub
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Desktop'"
        
      >
        Docker Desktop
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Hub' && 'hidden'"
      >
        <ol>
<li>
<p>前往 <a class="link" href="https://hub.docker.com" rel="noopener">Docker Hub</a> 并登录。</p>
<p>登录后，您应该位于 <strong>Repositories</strong> 页面。如果没有，请前往 <a class="link" href="https://hub.docker.com/repositories/" rel="noopener"><strong>Repositories</strong></a> 页面。</p>
</li>
<li>
<p>找到 <strong>nginx-custom</strong> 仓库并选择该行。</p>
<p>选择仓库后，您应该会看到更多关于您仓库的详细信息和选项。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <ol>
<li>
<p>登录 Docker Desktop。</p>
</li>
<li>
<p>选择 <strong>Images</strong> 视图。</p>
</li>
<li>
<p>选择 <strong>Hub repositories</strong> 选项卡。</p>
<p>将显示您的 Docker Hub 仓库列表。</p>
</li>
<li>
<p>找到 <strong>nginx-custom</strong> 仓库，将鼠标悬停在该行上，然后选择 <strong>View in Hub</strong>。</p>
<p>Docker Hub 将打开，您能够查看有关该镜像的更多详细信息。</p>
</li>
</ol>

      </div>
    
  </div>
</div>


您现在已经验证了您的仓库存在于 Docker Hub 上，并且发现了更多关于它的选项。查看后续步骤以了解更多关于其中一些选项的信息。

## 后续步骤

添加[仓库信息](./repos/manage/information.md)以帮助用户查找和使用您的镜像。
