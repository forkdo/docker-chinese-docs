# 启用增强型容器隔离





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Business</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-180v-600q0-24.75 17.63-42.38Q115.25-840 140-840h270q24.75 0 42.38 17.62Q470-804.75 470-780v105h350q24.75 0 42.38 17.62Q880-639.75 880-615v435q0 24.75-17.62 42.37Q844.75-120 820-120H140q-24.75 0-42.37-17.63Q80-155.25 80-180Zm60 0h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm165 495h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm165 495h350v-435H470v105h80v60h-80v105h80v60h-80v105Zm185-270v-60h60v60h-60Zm0 165v-60h60v60h-60Z"/></svg>
            
          </span>
        
      </div>
    

    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



ECI 可在保持开发者完整生产力的同时，防止恶意容器破坏 Docker Desktop。

本页介绍如何开启增强型容器隔离（ECI）并验证其是否正常工作。

## 先决条件

开始前，您必须满足以下条件：

- Docker Business 订阅
- Docker Desktop 4.13 或更高版本
- [强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)（仅适用于管理组织范围设置的 administrators）

## 启用增强型容器隔离

### 开发者操作

在 Docker Desktop 设置中开启 ECI：

1. 在 Docker Desktop 中登录您的组织。您的组织必须拥有
Docker Business 订阅。
1. 停止并删除所有现有容器：

    ```console
    $ docker stop $(docker ps -q)
    $ docker rm $(docker ps -aq)
    ```

1. 在 Docker Desktop 中，转到 **Settings** > **General**。
1. 勾选 **Use Enhanced Container Isolation** 复选框。
1. 选择 **Apply and restart**。

> [!IMPORTANT]
>
> ECI 无法保护在开启该功能前已创建的容器。开启 ECI 前请删除现有容器。

### 管理员操作

使用 Settings Management 在组织范围内配置增强型容器隔离：








<div
  class="tabs"
  
    x-data="{ selected: 'Admin-Console' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Admin-Console' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Admin-Console'"
        
      >
        Admin Console
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'JSON-file' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'JSON-file'"
        
      >
        JSON file
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Admin-Console' && 'hidden'"
      >
        <ol>
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a> 并从左上角账户下拉菜单中选择您的组织。</li>
<li>转到 <strong>Admin Console</strong> &gt; <strong>Desktop Settings Management</strong>。</li>
<li>
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/">创建或编辑设置策略</a>。</li>
<li>将 <strong>Enhanced Container Isolation</strong> 设置为 <strong>Always enabled</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'JSON-file' && 'hidden'"
      >
        <ol>
<li>
<p>创建 
    
  
  <a class="link" href="https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/"><code>admin-settings.json</code> 文件</a> 并添加：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICJjb25maWd1cmF0aW9uRmlsZVZlcnNpb24iOiAyLAogICJlbmhhbmNlZENvbnRhaW5lcklzb2xhdGlvbiI6IHsKICAgICJ2YWx1ZSI6IHRydWUsCiAgICAibG9ja2VkIjogdHJ1ZQogIH0KfQ==', copying: false }"
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
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;configurationFileVersion&#34;</span><span class="p">:</span> <span class="mi">2</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&#34;enhancedContainerIsolation&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nt">&#34;value&#34;</span><span class="p">:</span> <span class="kc">true</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nt">&#34;locked&#34;</span><span class="p">:</span> <span class="kc">true</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>根据需要配置以下选项：</p>
<ul>
<li><code>&quot;value&quot;: true</code>：默认开启 ECI（必需）</li>
<li><code>&quot;locked&quot;: true</code>：防止开发者关闭 ECI</li>
<li><code>&quot;locked&quot;: false</code>：允许开发者控制该设置</li>
</ul>
</li>
</ol>

      </div>
    
  </div>
</div>


### 应用配置

ECI 设置生效需满足以下条件：

- 新安装：用户启动 Docker Desktop 并登录
- 现有安装：用户必须完全退出 Docker Desktop 并重新启动

> [!IMPORTANT]
>
> 仅从 Docker Desktop 菜单重启不够。用户必须完全退出并重新打开 Docker Desktop。

您还可以为需要 Docker API 访问的可信镜像配置 [Docker socket 挂载权限](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。

## 验证增强型容器隔离是否已激活

开启 ECI 后，请通过以下方法验证其是否正常工作。

### 检查用户命名空间映射

运行容器并检查用户命名空间映射：

```console
$ docker run --rm alpine cat /proc/self/uid_map
```

ECI 开启时：

```text
0     100000      65536
```

这表示容器 root 用户 (0) 映射到 Docker Desktop VM 中的非特权用户 (100000)，用户 ID 范围为 64K。每个容器获得专属用户 ID 范围以实现隔离。

ECI 关闭时：

```text
0          0 4294967295
```

这表示容器 root 用户 (0) 直接映射到 VM root 用户 (0)，隔离性较弱。

### 检查容器运行时

验证正在使用的容器运行时：

```console
$ docker inspect --format='{{.HostConfig.Runtime}}' <container_name>
```

ECI 开启时返回 `sysbox-runc`。ECI 关闭时返回
`runc`。

### 测试安全限制

验证 ECI 安全限制是否生效。

测试命名空间共享：

```console
$ docker run -it --rm --pid=host alpine
```

ECI 开启时，此命令会因 Sysbox 容器无法与主机共享命名空间而失败。

测试 Docker socket 访问：

```console
$ docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock alpine
```

ECI 开启时，此命令会失败，除非您已为可信镜像配置 Docker socket 例外。

## 强制 ECI 时用户看到的内容

当管理员通过 Settings Management 强制实施增强型容器隔离时：

- **Use Enhanced Container Isolation** 设置在 Docker Desktop 设置中显示为开启状态。
- 若设置为 `"locked": true`，该设置将被锁定并置灰。
- 所有新容器自动使用 Linux 用户命名空间。
- 现有开发工作流无需修改即可继续运行。
- 用户在 `docker inspect` 输出中看到 `sysbox-runc` 作为容器运行时。

## 后续步骤

- 查看 [配置 Docker socket 例外和高级设置](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。
- 查看 [增强型容器隔离限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。
