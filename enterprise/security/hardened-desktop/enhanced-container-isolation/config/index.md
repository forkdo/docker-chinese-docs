# 配置 Docker 套接字异常和高级设置





  
  
  
  


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



本页介绍如何为增强容器隔离 (ECI) 配置 Docker 套接字异常和其他高级设置。这些配置使受信任的工具（如 Testcontainers）能够在 ECI 下工作，同时保持安全性。

## Docker 套接字挂载权限

默认情况下，增强容器隔离会阻止容器挂载 Docker 套接字，以防止对 Docker 引擎的恶意访问。但是，某些工具需要访问 Docker 套接字。

需要 Docker 套接字访问的常见场景包括：

- 测试框架：管理测试容器的 Testcontainers
- 构建工具：创建临时构建容器的 Paketo buildpacks
- CI/CD 工具：作为部署管道一部分管理容器的工具
- 开发实用程序：用于容器管理的 Docker CLI 容器

## 配置套接字异常

使用设置管理配置 Docker 套接字异常：








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
<li>登录 <a class="link" href="https://app.docker.com" rel="noopener">Docker Home</a>，从左上角的帐户下拉菜单中选择您的组织。</li>
<li>转到 <strong>Admin Console</strong> &gt; <strong>Desktop Settings Management</strong>。</li>
<li>
    
  
  <a class="link" href="/enterprise/security/hardened-desktop/settings-management/configure-admin-console/">创建或编辑设置策略</a>。</li>
<li>找到 <strong>Enhanced Container Isolation</strong> 设置。</li>
<li>使用受信任的镜像和命令限制配置 <strong>Docker socket access control</strong>。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'JSON-file' && 'hidden'"
      >
        <p>创建一个 
    
  
  <a class="link" href="/enterprise/security/hardened-desktop/settings-management/configure-json-file/"><code>admin-settings.json</code> 文件</a> 并添加：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICJjb25maWd1cmF0aW9uRmlsZVZlcnNpb24iOiAyLAogICJlbmhhbmNlZENvbnRhaW5lcklzb2xhdGlvbiI6IHsKICAgICJsb2NrZWQiOiB0cnVlLAogICAgInZhbHVlIjogdHJ1ZSwKICAgICJkb2NrZXJTb2NrZXRNb3VudCI6IHsKICAgICAgImltYWdlTGlzdCI6IHsKICAgICAgICAiaW1hZ2VzIjogWwogICAgICAgICAgImRvY2tlci5pby9sb2NhbHN0YWNrL2xvY2Fsc3RhY2s6KiIsCiAgICAgICAgICAiZG9ja2VyLmlvL3Rlc3Rjb250YWluZXJzL3J5dWs6KiIsCiAgICAgICAgICAiZG9ja2VyOmNsaSIKICAgICAgICBdLAogICAgICAgICJhbGxvd0Rlcml2ZWRJbWFnZXMiOiB0cnVlCiAgICAgIH0sCiAgICAgICJjb21tYW5kTGlzdCI6IHsKICAgICAgICAidHlwZSI6ICJkZW55IiwKICAgICAgICAiY29tbWFuZHMiOiBbInB1c2giLCAiYnVpbGQiXQogICAgICB9CiAgICB9CiAgfQp9', copying: false }"
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
</span></span><span class="line"><span class="cl">    <span class="nt">&#34;locked&#34;</span><span class="p">:</span> <span class="kc">true</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nt">&#34;value&#34;</span><span class="p">:</span> <span class="kc">true</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nt">&#34;dockerSocketMount&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&#34;imageList&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nt">&#34;images&#34;</span><span class="p">:</span> <span class="p">[</span>
</span></span><span class="line"><span class="cl">          <span class="s2">&#34;docker.io/localstack/localstack:*&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">          <span class="s2">&#34;docker.io/testcontainers/ryuk:*&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">          <span class="s2">&#34;docker:cli&#34;</span>
</span></span><span class="line"><span class="cl">        <span class="p">],</span>
</span></span><span class="line"><span class="cl">        <span class="nt">&#34;allowDerivedImages&#34;</span><span class="p">:</span> <span class="kc">true</span>
</span></span><span class="line"><span class="cl">      <span class="p">},</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&#34;commandList&#34;</span><span class="p">:</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nt">&#34;type&#34;</span><span class="p">:</span> <span class="s2">&#34;deny&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">        <span class="nt">&#34;commands&#34;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&#34;push&#34;</span><span class="p">,</span> <span class="s2">&#34;build&#34;</span><span class="p">]</span>
</span></span><span class="line"><span class="cl">      <span class="p">}</span>
</span></span><span class="line"><span class="cl">    <span class="p">}</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 镜像允许列表配置

`imageList` 定义了哪些容器镜像可以挂载 Docker 套接字。

### 镜像引用格式

| 格式 | 描述 |
| :---------------------- | :---------- |
| `<image_name>[:<tag>]` | 镜像名称，带有可选标签。如果省略标签，则使用 `:latest` 标签。如果标签是通配符 `*`，则表示“该镜像的任何标签”。 |
| `<image_name>@<digest>` | 镜像名称，带有特定的存储库摘要（例如，由 `docker buildx imagetools inspect <image>` 报告）。这意味着只允许匹配该名称和摘要的镜像。 |

### 配置示例

测试工具的基本允许列表：

```json
"imageList": {
  "images": [
    "docker.io/testcontainers/ryuk:*",
    "docker:cli",
    "alpine:latest"
  ]
}
```

通配符允许列表（Docker Desktop 4.36 及更高版本）：

```json
"imageList": {
  "images": ["*"]
}
```

> [!WARNING]
>
> 使用 `"*"` 允许所有容器挂载 Docker 套接字，这会降低安全性。仅在明确列出允许的镜像不可行时才使用此选项。

### 安全验证

Docker Desktop 通过以下方式验证允许的镜像：

1. 从注册表下载允许镜像的镜像摘要
2. 在容器启动时将容器镜像摘要与允许列表进行比较
3. 阻止摘要与允许镜像不匹配的容器

这可以防止通过重新标记未经授权的镜像来绕过限制：

```console
$ docker tag malicious-image docker:cli
$ docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli
# 此操作失败，因为摘要与真实的 docker:cli 镜像不匹配
```

## 派生镜像支持

对于像 Paketo buildpacks 这样创建临时本地镜像的工具，您可以允许从受信任的基础镜像派生的镜像。

### 启用派生镜像

```json
"imageList": {
  "images": [
    "paketobuildpacks/builder:base"
  ],
  "allowDerivedImages": true
}
```

当 `allowDerivedImages` 为 true 时，从允许的基础镜像构建的本地镜像（使用 Dockerfile 中的 `FROM`）也将获得 Docker 套接字访问权限。

### 派生镜像要求

- 仅限本地镜像：派生镜像不得存在于远程注册表中
- 基础镜像可用：父镜像必须首先拉取到本地
- 性能影响：验证会使容器启动时间增加最多 1 秒
- 版本兼容性：完全通配符支持需要 Docker Desktop 4.36+

## 命令限制

### 拒绝列表（推荐）

阻止指定的命令，同时允许所有其他命令：

```json
"commandList": {
  "type": "deny",
  "commands": ["push", "build", "image*"]
}
```

### 允许列表

仅允许指定的命令，同时阻止所有其他命令：

```json
"commandList": {
  "type": "allow",
  "commands": ["ps", "container*", "volume*"]
}
```

### 命令通配符

| 通配符 | 阻止/允许 |
| :---------------- | :---------- |
| `"container\*"` | 所有 "docker container ..." 命令 |
| `"image\*"` | 所有 "docker image ..." 命令 |
| `"volume\*"` | 所有 "docker volume ..." 命令 |
| `"network\*"` | 所有 "docker network ..." 命令 |
| `"build\*"` | 所有 "docker build ..." 命令 |
| `"system\*"` | 所有 "docker system ..." 命令 |

### 命令阻止示例

当执行被阻止的命令时：

```console
/ # docker push myimage
Error response from daemon: enhanced container isolation: docker command "/v1.43/images/myimage/push?tag=latest" is blocked; if you wish to allow it, configure the docker socket command list in the Docker Desktop settings.
```

## 常见配置示例

### Testcontainers 设置

用于 Java/Python 测试的 Testcontainers：

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker.io/testcontainers/ryuk:*",
      "testcontainers/*:*"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["push", "build"]
  }
}
```

### CI/CD 管道工具

用于受控的 CI/CD 容器管理：

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:cli",
      "your-registry.com/ci-tools/*:*"
    ]
  },
  "commandList": {
    "type": "allow",
    "commands": ["ps", "container*", "image*"]
  }
}
```

### 开发环境

用于本地开发的 Docker-in-Docker：

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:dind",
      "docker:cli"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["system*"]
  }
}
```

## 安全建议

### 镜像允许列表最佳实践

- 严格限制：只允许您绝对信任和需要的镜像
- 谨慎使用通配符：标签通配符 (`*`) 很方便，但不如特定标签安全
- 定期审查：定期审查和更新您的允许列表
- 摘要固定：在关键环境中使用摘要引用以获得最大安全性

### 命令限制

- 默认拒绝：从拒绝列表开始，阻止危险命令，如 `push` 和 `build`
- 最小权限原则：只允许您的工具实际需要的命令
- 监控使用情况：跟踪哪些命令被阻止以优化您的配置

### 监控和维护

- 定期验证：Docker Desktop 更新后测试您的配置，因为镜像摘要可能会更改。
- 处理摘要不匹配：如果允许的镜像被意外阻止：
    ```console
    $ docker image rm <image>
    $ docker pull <image>
    ```

当上游镜像更新时，这可以解决摘要不匹配的问题。

## 下一步

- 查看 [增强容器隔离限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。
- 查看 [增强容器隔离常见问题解答](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/faq.md)。
