# 如何备份和恢复 Docker Desktop 数据

使用此流程可以备份和恢复您的镜像和容器数据。这在您需要重置虚拟机磁盘、将 Docker 环境迁移到新计算机，或从 Docker Desktop 更新或安装失败中恢复时非常有用。

> [!IMPORTANT]
>
> 如果您使用卷或绑定挂载来存储容器数据，可能不需要备份容器，但请务必记住创建容器时使用的选项，或使用 [Docker Compose 文件](/reference/compose-file/_index.md)以便在重新安装后以相同配置重新创建容器。

## 如果 Docker Desktop 运行正常

### 保存数据

1. 使用 [`docker container commit`](/reference/cli/docker/container/commit.md) 将容器提交为镜像。

   提交容器会将文件系统更改和某些容器配置（如标签和环境变量）存储为本地镜像。请注意，环境变量可能包含敏感信息（如密码或代理认证），因此在将结果镜像推送到注册表时需谨慎。

   另外请注意，附加到容器的卷中的文件系统更改不会包含在镜像中，必须单独备份。

   如果您使用了[命名卷](/manuals/engine/storage/_index.md#more-details-about-mount-types)来存储容器数据（如数据库），请参考存储部分的[备份、恢复或迁移数据卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)页面。

2. 使用 [`docker push`](/reference/cli/docker/image/push.md) 将您在本地构建并希望保留的任何镜像推送到 [Docker Hub 注册表](/manuals/docker-hub/_index.md)。
   
   > [!TIP]
   >
   > 如果您的镜像包含敏感内容，[将仓库可见性设置为私有](/manuals/docker-hub/repos/_index.md)。

   或者，使用 [`docker image save -o images.tar image1 [image2 ...]`](/reference/cli/docker/image/save.md) 将您希望保留的任何镜像保存到本地 `.tar` 文件中。

备份数据后，您可以卸载当前版本的 Docker Desktop 并[安装不同版本](/manuals/desktop/release-notes.md)或重置 Docker Desktop 为出厂默认设置。

### 恢复数据

1. 加载您的镜像。

   - 如果您推送到 Docker Hub：
   
      ```console
      $ docker pull <my-backup-image>
      ```
   
   - 如果您保存了 `.tar` 文件：
   
      ```console
      $ docker image load -i images.tar
      ```

2. 如有必要，使用 [`docker run`](/reference/cli/docker/container/run.md) 或 [Docker Compose](/manuals/compose/_index.md) 重新创建容器。

要恢复卷数据，请参考[备份、恢复或迁移数据卷](/manuals/engine/storage/volumes.md#back-up-restore-or-migrate-data-volumes)。 

## 如果 Docker Desktop 无法启动

如果 Docker Desktop 无法启动且必须重新安装，您可以直接从磁盘备份其 VM 磁盘和镜像数据。在备份这些文件之前，Docker Desktop 必须完全停止。








<div
  class="tabs"
  
    x-data="{ selected: 'Windows' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows'"
        
      >
        Windows
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac'"
        
      >
        Mac
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Linux'"
        
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
<p>备份 Docker 容器/镜像。</p>
<p>备份以下文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JUxPQ0FMQVBQREFUQSVcRG9ja2VyXHdzbFxkYXRhXGRvY2tlcl9kYXRhLnZoZHg=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">%</span>LOCALAPPDATA%<span class="se">\D</span>ocker<span class="se">\w</span>sl<span class="se">\d</span>ata<span class="se">\d</span>ocker_data.vhdx
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>将其复制到安全位置。</p>
</li>
<li>
<p>备份 WSL 发行版。</p>
<p>如果您运行任何 WSL Linux 发行版（Ubuntu、Alpine 等），请使用 <a class="link" href="https://learn.microsoft.com/en-us/windows/wsl/faq#how-can-i-back-up-my-wsl-distributions-" rel="noopener">Microsoft 指南</a> 备份它们。</p>
</li>
<li>
<p>恢复。</p>
<p>重新安装 Docker Desktop 后，将 <code>docker_data.vhdx</code> 恢复到相同位置，并在需要时重新导入您的 WSL 发行版。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac' && 'hidden'"
      >
        <ol>
<li>
<p>备份 Docker 容器/镜像。</p>
<p>备份以下文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'fi9MaWJyYXJ5L0NvbnRhaW5lcnMvY29tLmRvY2tlci5kb2NrZXIvRGF0YS92bXMvMC9kYXRhL0RvY2tlci5yYXc=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>将其复制到安全位置。</p>
</li>
<li>
<p>恢复。</p>
<p>重新安装 Docker Desktop 后，将 <code>Docker.raw</code> 恢复到相同位置。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Linux' && 'hidden'"
      >
        <ol>
<li>
<p>备份 Docker 容器/镜像：</p>
<p>备份以下文件：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'fi8uZG9ja2VyL2Rlc2t0b3Avdm1zLzAvZGF0YS9Eb2NrZXIucmF3', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">~/.docker/desktop/vms/0/data/Docker.raw
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>将其复制到安全位置。</p>
</li>
<li>
<p>恢复。</p>
<p>重新安装 Docker Desktop 后，将 <code>Docker.raw</code> 恢复到相同位置。</p>
</li>
</ol>

      </div>
    
  </div>
</div>

