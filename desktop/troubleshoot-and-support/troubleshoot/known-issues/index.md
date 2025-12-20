# 已知问题








<div
  class="tabs"
  
    x-data="{ selected: '%E9%80%82%E7%94%A8%E4%BA%8E%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E9%80%82%E7%94%A8%E4%BA%8E%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E9%80%82%E7%94%A8%E4%BA%8E%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac'"
        
      >
        适用于搭载 Intel 芯片的 Mac
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E9%80%82%E7%94%A8%E4%BA%8E%E6%90%AD%E8%BD%BD-Apple-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E9%80%82%E7%94%A8%E4%BA%8E%E6%90%AD%E8%BD%BD-Apple-%E8%8A%AF%E7%89%87%E7%9A%84-Mac'"
        
      >
        适用于搭载 Apple 芯片的 Mac
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E9%80%82%E7%94%A8%E4%BA%8E%E6%90%AD%E8%BD%BD-Intel-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' && 'hidden'"
      >
        <ul>
<li>
<p>Mac 活动监视器报告 Docker 使用的内存量是其实际使用量的两倍。这是由于 <a class="link" href="https://docs.google.com/document/d/17ZiQC1Tp9iH320K-uqVLyiJmk4DHJ3c4zgQetJiKYQM/edit?usp=sharing" rel="noopener">macOS 的一个 bug</a>。</p>
</li>
<li>
<p><strong>&quot;Docker.app 已损坏&quot; 对话框</strong>：如果在安装或更新过程中看到 &quot;Docker.app 已损坏，无法打开&quot; 的对话框，这通常是由于其他应用程序在使用 Docker CLI 时执行了非原子复制操作所致。请参见 <a class="link" href="/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/">修复 macOS 上的 &quot;Docker.app 已损坏&quot;</a> 获取解决步骤。</p>
</li>
<li>
<p>在 <code>.dmg</code> 中运行 <code>Docker.app</code> 后强制弹出 <code>.dmg</code> 可能导致
鲸鱼图标无响应，Docker 任务在活动监视器中显示为无响应，并且某些进程消耗大量 CPU 资源。重启并重新启动 Docker 以解决这些问题。</p>
</li>
<li>
<p>Docker Desktop 在 macOS 10.10 Yosemite 及更高版本中使用 <code>HyperKit</code> 虚拟机监控程序
(<a class="link" href="https://github.com/docker/hyperkit" rel="noopener">https://github.com/docker/hyperkit</a>)。如果您正在使用与 <code>HyperKit</code> 有冲突的工具进行开发，例如
<a class="link" href="https://software.intel.com/en-us/android/articles/intel-hardware-accelerated-execution-manager/" rel="noopener">Intel 硬件加速执行管理器
(HAXM)</a>，
目前的解决方法是不要同时运行它们。您可以通过退出 Docker Desktop 来暂停
<code>HyperKit</code>，以便在使用 HAXM 时工作。
这使您可以继续使用其他工具，并防止 <code>HyperKit</code>
干扰。</p>
</li>
<li>
<p>如果您正在使用如 <a class="link" href="https://maven.apache.org/" rel="noopener">Apache
Maven</a> 等期望为 <code>DOCKER_HOST</code> 和
<code>DOCKER_CERT_PATH</code> 环境变量设置的应用程序，请指定这些变量以通过 Unix 套接字连接到 Docker
实例。例如：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBleHBvcnQgRE9DS0VSX0hPU1Q9dW5peDovLy92YXIvcnVuL2RvY2tlci5zb2Nr', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> <span class="nb">export</span> <span class="nv">DOCKER_HOST</span><span class="o">=</span>unix:///var/run/docker.sock
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
</ul>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E9%80%82%E7%94%A8%E4%BA%8E%E6%90%AD%E8%BD%BD-Apple-%E8%8A%AF%E7%89%87%E7%9A%84-Mac' && 'hidden'"
      >
        <ul>
<li>
<p>某些命令行工具在 Rosetta 2 未安装时无法工作。</p>
<ul>
<li>旧版本 1.x 的 <code>docker-compose</code>。请改用 Compose V2 - 输入 <code>docker compose</code>。</li>
<li><code>docker-credential-ecr-login</code> 凭据助手。</li>
</ul>
</li>
<li>
<p>某些镜像不支持 ARM64 架构。您可以添加 <code>--platform linux/amd64</code> 以使用模拟运行（或构建）Intel 镜像。</p>
<p>然而，在 Apple 芯片机器上使用模拟运行基于 Intel 的容器时，由于 QEMU 有时无法运行容器，尝试可能会失败。此外，在 QEMU 模拟下，文件系统更改通知 API（<code>inotify</code>）无法工作。即使容器在模拟下正确运行，它们也会比原生等效容器更慢并消耗更多内存。</p>
<p>总之，在基于 Arm 的机器上运行基于 Intel 的容器应被视为“尽力而为”。我们建议尽可能在 Apple 芯片机器上运行 <code>arm64</code> 容器，并鼓励容器作者制作 <code>arm64</code> 或多架构版本的容器。随着越来越多的镜像重建<a class="link" href="https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/" rel="noopener">支持多种架构</a>，这个问题应会随着时间的推移变得越来越少见。</p>
</li>
<li>
<p>用户可能会在 TCP 流半关闭时偶尔遇到数据丢失。</p>
</li>
</ul>

      </div>
    
  </div>
</div>

