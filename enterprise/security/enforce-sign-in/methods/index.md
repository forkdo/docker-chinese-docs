# 配置登录强制执行





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Team</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M30-240q-12.75 0-21.37-8.63Q0-257.25 0-270v-23q0-38.57 41.5-62.78Q83-380 150.38-380q12.16 0 23.39.5t22.23 2.15q-8 17.35-12 35.17-4 17.81-4 37.18v65H30Zm240 0q-12.75 0-21.37-8.63Q240-257.25 240-270v-35q0-32 17.5-58.5T307-410q32-20 76.5-30t96.5-10q53 0 97.5 10t76.5 30q32 20 49 46.5t17 58.5v35q0 12.75-8.62 21.37Q702.75-240 690-240H270Zm510 0v-65q0-19.86-3.5-37.43T765-377.27q11-1.73 22.17-2.23 11.17-.5 22.83-.5 67.5 0 108.75 23.77T960-293v23q0 12.75-8.62 21.37Q942.75-240 930-240H780ZM149.57-410q-28.57 0-49.07-20.56Q80-451.13 80-480q0-29 20.56-49.5Q121.13-550 150-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T149.57-410Zm660 0q-28.57 0-49.07-20.56Q740-451.13 740-480q0-29 20.56-49.5Q781.13-550 810-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T809.57-410ZM480-480q-50 0-85-35t-35-85q0-51 35-85.5t85-34.5q51 0 85.5 34.5T600-600q0 50-34.5 85T480-480Z"/></svg>
            
          </span>
        
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



您可以通过多种方法强制执行 Docker Desktop 的登录。请选择最适合您组织的基础设施和安全要求的方法。

## 选择您的方法

| 方法 | 平台 |
|:-------|:---------|
| 注册表项 | 仅限 Windows |
| 配置文件 | 仅限 macOS |
| `plist` 文件 | 仅限 macOS |
| `registry.json` | 所有平台 |

> [!TIP]
>
> 对于 macOS，配置文件提供了最高的安全性，因为它们受到 Apple 系统完整性保护 (SIP) 的保护。

## Windows：注册表项方法








<div
  class="tabs"
  
    x-data="{ selected: '%E6%89%8B%E5%8A%A8%E8%AE%BE%E7%BD%AE' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E6%89%8B%E5%8A%A8%E8%AE%BE%E7%BD%AE' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%89%8B%E5%8A%A8%E8%AE%BE%E7%BD%AE'"
        
      >
        手动设置
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E7%BB%84%E7%AD%96%E7%95%A5%E9%83%A8%E7%BD%B2' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E7%BB%84%E7%AD%96%E7%95%A5%E9%83%A8%E7%BD%B2'"
        
      >
        组策略部署
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%89%8B%E5%8A%A8%E8%AE%BE%E7%BD%AE' && 'hidden'"
      >
        <p>要手动配置注册表项方法：</p>
<ol>
<li>
<p>创建注册表项：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBIS0VZX0xPQ0FMX01BQ0hJTkVcU09GVFdBUkVcUG9saWNpZXNcRG9ja2VyXERvY2tlciBEZXNrdG9w', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> HKEY_LOCAL_MACHINE<span class="se">\S</span>OFTWARE<span class="se">\P</span>olicies<span class="se">\D</span>ocker<span class="se">\D</span>ocker Desktop
</span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>
<p>创建一个多字符串值名称 <code>allowedOrgs</code>。</p>
</li>
<li>
<p>使用您的组织名称作为字符串数据：</p>
<ul>
<li>仅使用小写字母</li>
<li>每行添加一个组织</li>
<li>请勿使用空格或逗号作为分隔符</li>
</ul>
</li>
<li>
<p>重启 Docker Desktop。</p>
</li>
<li>
<p>验证 Docker Desktop 中是否出现 <code>Sign in required!</code> 提示。</p>
</li>
</ol>


  

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
      <p>您可以在 Docker Desktop 4.36 及更高版本中添加多个组织。在 4.35 及更早版本中，添加多个组织会导致登录强制执行静默失败。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E7%BB%84%E7%AD%96%E7%95%A5%E9%83%A8%E7%BD%B2' && 'hidden'"
      >
        <p>使用组策略在您的组织内部署注册表项：</p>
<ol>
<li>使用所需的键结构创建注册表脚本。</li>
<li>在组策略管理中，创建或编辑一个 GPO。</li>
<li>导航到 <strong>计算机配置</strong> &gt; <strong>首选项</strong> &gt; <strong>Windows 设置</strong> &gt; <strong>注册表</strong>。</li>
<li>右键单击 <strong>注册表</strong> &gt; <strong>新建</strong> &gt; <strong>注册表项</strong>。</li>
<li>配置注册表项：
<ul>
<li>操作：<strong>更新</strong></li>
<li>路径：<code>HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Docker\Docker Desktop</code></li>
<li>值名称：<code>allowedOrgs</code></li>
<li>值数据：您的组织名称</li>
</ul>
</li>
<li>将 GPO 链接到目标组织单位 (OU)。</li>
<li>使用 <code>gpupdate/force</code> 在小范围用户组中进行测试。</li>
<li>验证后在整个组织内部署。</li>
</ol>

      </div>
    
  </div>
</div>


## macOS：配置文件方法（推荐）





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 4.36 and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



配置文件为 macOS 提供了最安全的强制执行方法，因为它们受到 Apple 系统完整性保护的保护。

该有效负载是一个键值对的字典。Docker Desktop 支持以下键：

- `allowedOrgs`：在一个字符串中设置组织列表，每个组织用分号分隔。

在 Docker Desktop 4.48 及更高版本中，还支持以下键：

- `overrideProxyHTTP`：设置用于传出 HTTP 请求的 HTTP 代理 URL。
- `overrideProxyHTTPS`：设置用于传出 HTTPS 请求的 HTTP 代理 URL。
- `overrideProxyExclude`：绕过指定主机和域的代理设置。使用逗号分隔的列表。
- `overrideProxyPAC`：设置 PAC 文件所在的文件路径。它优先于所选代理上的远程 PAC 文件。
- `overrideProxyEmbeddedPAC`：设置内存中 PAC 文件的内容。它优先于 `overrideProxyPAC`。

通过配置文件覆盖至少一个代理设置将自动锁定这些设置，因为它们由 macOS 管理。


1. 创建一个名为 `docker.mobileconfig` 的文件，并包含以下内容：
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
      <key>PayloadContent</key>
      <array>
         <dict>
            <key>PayloadType</key>
            <string>com.docker.config</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>PayloadIdentifier</key>
            <string>com.docker.config</string>
            <key>PayloadUUID</key>
            <string>eed295b0-a650-40b0-9dda-90efb12be3c7</string>
            <key>PayloadDisplayName</key>
            <string>Docker Desktop Configuration</string>
            <key>PayloadDescription</key>
            <string>Configuration profile to manage Docker Desktop settings.</string>
            <key>PayloadOrganization</key>
            <string>Your Company Name</string>
            <key>allowedOrgs</key>
            <string>first_org;second_org</string>
            <key>overrideProxyHTTP</key>
            <string>http://company.proxy:port</string>
            <key>overrideProxyHTTPS</key>
            <string>https://company.proxy:port</string>
         </dict>
      </array>
      <key>PayloadType</key>
      <string>Configuration</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>PayloadIdentifier</key>
      <string>com.yourcompany.docker.config</string>
      <key>PayloadUUID</key>
      <string>0deedb64-7dc9-46e5-b6bf-69d64a9561ce</string>
      <key>PayloadDisplayName</key>
      <string>Docker Desktop Config Profile</string>
      <key>PayloadDescription</key>
      <string>Config profile to enforce Docker Desktop settings for allowed organizations.</string>
      <key>PayloadOrganization</key>
      <string>Your Company Name</string>
   </dict>
   </plist>
   ```
1. 替换占位符：
   - 将 `com.yourcompany.docker.config` 更改为您的公司标识符
   - 将 `Your Company Name` 替换为您的组织名称
   - 将 `PayloadUUID` 替换为随机生成的 UUID
   - 用您的组织名称（用分号分隔）更新 `allowedOrgs` 的值
   - 将 `company.proxy:port` 替换为 http/https 代理服务器主机（或 IP 地址）和端口
1. 使用您的 MDM 解决方案部署配置文件。
1. 在 **系统设置** > **通用** > **VPN 与设备管理** 下的 **设备（托管）** 中验证配置文件是否存在。确保配置文件以正确的名称和设置列出。

一些 MDM 解决方案允许您将有效负载指定为纯键值设置字典，而无需完整的 `.mobileconfig` 包装器：

```xml
<dict>
   <key>allowedOrgs</key>
   <string>first_org;second_org</string>
   <key>overrideProxyHTTP</key>
   <string>http://company.proxy:port</string>
   <key>overrideProxyHTTPS</key>
   <string>https://company.proxy:port</string>
</dict>
```

## macOS：plist 文件方法

对于 Docker Desktop 4.32 及更高版本的 macOS，请使用此替代方法。








<div
  class="tabs"
  
    x-data="{ selected: '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA'"
        
      >
        手动创建
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Shell-%E8%84%9A%E6%9C%AC%E9%83%A8%E7%BD%B2' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Shell-%E8%84%9A%E6%9C%AC%E9%83%A8%E7%BD%B2'"
        
      >
        Shell 脚本部署
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA' && 'hidden'"
      >
        <ol>
<li>创建文件 <code>/Library/Application Support/com.docker.docker/desktop.plist</code>。</li>
<li>添加此内容，将 <code>myorg1</code> 和 <code>myorg2</code> 替换为您的组织名称：
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHBsaXN0IFBVQkxJQyAiLS8vQXBwbGUvL0RURCBQTElTVCAxLjAvL0VOIiAiaHR0cDovL3d3dy5hcHBsZS5jb20vRFREcy9Qcm9wZXJ0eUxpc3QtMS4wLmR0ZCI&#43;CjxwbGlzdCB2ZXJzaW9uPSIxLjAiPgogIDxkaWN0PgogICAgICA8a2V5PmFsbG93ZWRPcmdzPC9rZXk&#43;CiAgICAgIDxhcnJheT4KICAgICAgICAgIDxzdHJpbmc&#43;bXlvcmcxPC9zdHJpbmc&#43;CiAgICAgICAgICA8c3RyaW5nPm15b3JnMjwvc3RyaW5nPgogICAgICA8L2FycmF5PgogIDwvZGljdD4KPC9wbGlzdD4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-xml" data-lang="xml"><span class="line"><span class="cl"><span class="cp">&lt;?xml version=&#34;1.0&#34; encoding=&#34;UTF-8&#34;?&gt;</span>
</span></span><span class="line"><span class="cl"><span class="cp">&lt;!DOCTYPE plist PUBLIC &#34;-//Apple//DTD PLIST 1.0//EN&#34; &#34;http://www.apple.com/DTDs/PropertyList-1.0.dtd&#34;&gt;</span>
</span></span><span class="line"><span class="cl"><span class="nt">&lt;plist</span> <span class="na">version=</span><span class="s">&#34;1.0&#34;</span><span class="nt">&gt;</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&lt;dict&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&lt;key&gt;</span>allowedOrgs<span class="nt">&lt;/key&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&lt;array&gt;</span>
</span></span><span class="line"><span class="cl">          <span class="nt">&lt;string&gt;</span>myorg1<span class="nt">&lt;/string&gt;</span>
</span></span><span class="line"><span class="cl">          <span class="nt">&lt;string&gt;</span>myorg2<span class="nt">&lt;/string&gt;</span>
</span></span><span class="line"><span class="cl">      <span class="nt">&lt;/array&gt;</span>
</span></span><span class="line"><span class="cl">  <span class="nt">&lt;/dict&gt;</span>
</span></span><span class="line"><span class="cl"><span class="nt">&lt;/plist&gt;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>设置文件权限以防止非管理员用户编辑。</li>
<li>重启 Docker Desktop。</li>
<li>验证 Docker Desktop 中是否出现 <code>Sign in required!</code> 提示。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Shell-%E8%84%9A%E6%9C%AC%E9%83%A8%E7%BD%B2' && 'hidden'"
      >
        <p>创建并部署一个脚本，用于在整个组织内分发：</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyEvYmluL2Jhc2gKCiMg5aaC5p6c55uu5b2V5LiN5a2Y5Zyo5YiZ5Yib5bu6CnN1ZG8gbWtkaXIgLXAgIi9MaWJyYXJ5L0FwcGxpY2F0aW9uIFN1cHBvcnQvY29tLmRvY2tlci5kb2NrZXIiCgojIOWGmeWFpSBwbGlzdCDmlofku7YKc3VkbyBkZWZhdWx0cyB3cml0ZSAiL0xpYnJhcnkvQXBwbGljYXRpb24gU3VwcG9ydC9jb20uZG9ja2VyLmRvY2tlci9kZXNrdG9wLnBsaXN0IiBhbGxvd2VkT3JncyAtYXJyYXkgIm15b3JnMSIgIm15b3JnMiIKCiMg6K6&#43;572u6YCC5b2T55qE5p2D6ZmQCnN1ZG8gY2htb2QgNjQ0ICIvTGlicmFyeS9BcHBsaWNhdGlvbiBTdXBwb3J0L2NvbS5kb2NrZXIuZG9ja2VyL2Rlc2t0b3AucGxpc3QiCnN1ZG8gY2hvd24gcm9vdDphZG1pbiAiL0xpYnJhcnkvQXBwbGljYXRpb24gU3VwcG9ydC9jb20uZG9ja2VyLmRvY2tlci9kZXNrdG9wLnBsaXN0Ig==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-bash" data-lang="bash"><span class="line"><span class="cl"><span class="cp">#!/bin/bash
</span></span></span><span class="line"><span class="cl"><span class="cp"></span>
</span></span><span class="line"><span class="cl"><span class="c1"># 如果目录不存在则创建</span>
</span></span><span class="line"><span class="cl">sudo mkdir -p <span class="s2">&#34;/Library/Application Support/com.docker.docker&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 写入 plist 文件</span>
</span></span><span class="line"><span class="cl">sudo defaults write <span class="s2">&#34;/Library/Application Support/com.docker.docker/desktop.plist&#34;</span> allowedOrgs -array <span class="s2">&#34;myorg1&#34;</span> <span class="s2">&#34;myorg2&#34;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 设置适当的权限</span>
</span></span><span class="line"><span class="cl">sudo chmod <span class="m">644</span> <span class="s2">&#34;/Library/Application Support/com.docker.docker/desktop.plist&#34;</span>
</span></span><span class="line"><span class="cl">sudo chown root:admin <span class="s2">&#34;/Library/Application Support/com.docker.docker/desktop.plist&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>使用 SSH、远程支持工具或您首选的部署方法来部署此脚本。</p>

      </div>
    
  </div>
</div>


## 所有平台：registry.json 方法

registry.json 方法适用于所有平台，并提供灵活的部署选项。

### 文件位置

在相应的位置创建 `registry.json` 文件：

| 平台 | 位置 |
| --- | --- |
| Windows | `/ProgramData/DockerDesktop/registry.json` |
| Mac | `/Library/Application Support/com.docker.docker/registry.json` |
| Linux | `/usr/share/docker-desktop/registry/registry.json` |

### 基本设置








<div
  class="tabs"
  
    x-data="{ selected: '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA'"
        
      >
        手动创建
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E5%91%BD%E4%BB%A4%E8%A1%8C%E8%AE%BE%E7%BD%AE' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%91%BD%E4%BB%A4%E8%A1%8C%E8%AE%BE%E7%BD%AE'"
        
      >
        命令行设置
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E5%AE%89%E8%A3%85%E6%97%B6%E8%AE%BE%E7%BD%AE' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E5%AE%89%E8%A3%85%E6%97%B6%E8%AE%BE%E7%BD%AE'"
        
      >
        安装时设置
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%89%8B%E5%8A%A8%E5%88%9B%E5%BB%BA' && 'hidden'"
      >
        <ol>
<li>确保用户是您 Docker 组织的成员。</li>
<li>在适合您平台的位置创建 <code>registry.json</code> 文件。</li>
<li>添加此内容，将组织名称替换为您自己的：
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'ewogICAiYWxsb3dlZE9yZ3MiOiBbIm15b3JnMSIsICJteW9yZzIiXQp9', copying: false }"
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
</span></span><span class="line"><span class="cl">   <span class="nt">&#34;allowedOrgs&#34;</span><span class="p">:</span> <span class="p">[</span><span class="s2">&#34;myorg1&#34;</span><span class="p">,</span> <span class="s2">&#34;myorg2&#34;</span><span class="p">]</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>
</li>
<li>设置文件权限以防止用户编辑。</li>
<li>重启 Docker Desktop。</li>
<li>验证 Docker Desktop 中是否出现 <code>Sign in required!</code> 提示。</li>
</ol>


  

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
      <p>如果用户在强制执行登录后无法启动 Docker Desktop，
他们可能需要更新到最新版本。</p>
    </div>
  </blockquote>


      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%91%BD%E4%BB%A4%E8%A1%8C%E8%AE%BE%E7%BD%AE' && 'hidden'"
      >
        
<h4 class=" scroll-mt-20 flex items-center gap-2" id="windows-以管理员身份运行-powershell">
  <a class="text-black dark:text-white no-underline hover:underline" href="#windows-%e4%bb%a5%e7%ae%a1%e7%90%86%e5%91%98%e8%ba%ab%e4%bb%bd%e8%bf%90%e8%a1%8c-powershell">
    Windows (以管理员身份运行 PowerShell)
  </a>
</h4>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'U2V0LUNvbnRlbnQgL1Byb2dyYW1EYXRhL0RvY2tlckRlc2t0b3AvcmVnaXN0cnkuanNvbiAneyJhbGxvd2VkT3JncyI6WyJteW9yZzEiLCJteW9yZzIiXX0n', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-shell" data-lang="shell"><span class="line"><span class="cl">Set-Content /ProgramData/DockerDesktop/registry.json <span class="s1">&#39;{&#34;allowedOrgs&#34;:[&#34;myorg1&#34;,&#34;myorg2&#34;]}&#39;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h4 class=" scroll-mt-20 flex items-center gap-2" id="macos">
  <a class="text-black dark:text-white no-underline hover:underline" href="#macos">
    macOS
  </a>
</h4>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'c3VkbyBta2RpciAtcCAiL0xpYnJhcnkvQXBwbGljYXRpb24gU3VwcG9ydC9jb20uZG9ja2VyLmRvY2tlciIKZWNobyAneyJhbGxvd2VkT3JncyI6WyJteW9yZzEiLCJteW9yZzIiXX0nIHwgc3VkbyB0ZWUgIi9MaWJyYXJ5L0FwcGxpY2F0aW9uIFN1cHBvcnQvY29tLmRvY2tlci5kb2NrZXIvcmVnaXN0cnkuanNvbiI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">sudo mkdir -p &#34;/Library/Application Support/com.docker.docker&#34;
</span></span></span><span class="line"><span class="cl"><span class="go">echo &#39;{&#34;allowedOrgs&#34;:[&#34;myorg1&#34;,&#34;myorg2&#34;]}&#39; | sudo tee &#34;/Library/Application Support/com.docker.docker/registry.json&#34;
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h4 class=" scroll-mt-20 flex items-center gap-2" id="linux">
  <a class="text-black dark:text-white no-underline hover:underline" href="#linux">
    Linux
  </a>
</h4>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'c3VkbyBta2RpciAtcCAvdXNyL3NoYXJlL2RvY2tlci1kZXNrdG9wL3JlZ2lzdHJ5CmVjaG8gJ3siYWxsb3dlZE9yZ3MiOlsibXlvcmcxIiwibXlvcmcyIl19JyB8IHN1ZG8gdGVlIC91c3Ivc2hhcmUvZG9ja2VyLWRlc2t0b3AvcmVnaXN0cnkvcmVnaXN0cnkuanNvbg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">sudo mkdir -p /usr/share/docker-desktop/registry
</span></span></span><span class="line"><span class="cl"><span class="go">echo &#39;{&#34;allowedOrgs&#34;:[&#34;myorg1&#34;,&#34;myorg2&#34;]}&#39; | sudo tee /usr/share/docker-desktop/registry/registry.json
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E5%AE%89%E8%A3%85%E6%97%B6%E8%AE%BE%E7%BD%AE' && 'hidden'"
      >
        <p>在安装 Docker Desktop 期间创建 registry.json 文件：</p>

<h4 class=" scroll-mt-20 flex items-center gap-2" id="windows">
  <a class="text-black dark:text-white no-underline hover:underline" href="#windows">
    Windows
  </a>
</h4>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBQb3dlclNoZWxsClN0YXJ0LVByb2Nlc3MgJy5cRG9ja2VyIERlc2t0b3AgSW5zdGFsbGVyLmV4ZScgLVdhaXQgJ2luc3RhbGwgLS1hbGxvd2VkLW9yZz1teW9yZycKCiMg5ZG95Luk5o&#43;Q56S656ymCiJEb2NrZXIgRGVza3RvcCBJbnN0YWxsZXIuZXhlIiBpbnN0YWxsIC0tYWxsb3dlZC1vcmc9bXlvcmc=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-shell" data-lang="shell"><span class="line"><span class="cl"><span class="c1"># PowerShell</span>
</span></span><span class="line"><span class="cl">Start-Process <span class="s1">&#39;.\Docker Desktop Installer.exe&#39;</span> -Wait <span class="s1">&#39;install --allowed-org=myorg&#39;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="c1"># 命令提示符</span>
</span></span><span class="line"><span class="cl"><span class="s2">&#34;Docker Desktop Installer.exe&#34;</span> install --allowed-org<span class="o">=</span>myorg</span></span></code></pre></div>
      
    </div>
  </div>
</div>

<h4 class=" scroll-mt-20 flex items-center gap-2" id="macos">
  <a class="text-black dark:text-white no-underline hover:underline" href="#macos">
    macOS
  </a>
</h4>

<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'c3VkbyBoZGl1dGlsIGF0dGFjaCBEb2NrZXIuZG1nCnN1ZG8gL1ZvbHVtZXMvRG9ja2VyL0RvY2tlci5hcHAvQ29udGVudHMvTWFjT1MvaW5zdGFsbCAtLWFsbG93ZWQtb3JnPW15b3JnCnN1ZG8gaGRpdXRpbCBkZXRhY2ggL1ZvbHVtZXMvRG9ja2Vy', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="go">sudo hdiutil attach Docker.dmg
</span></span></span><span class="line"><span class="cl"><span class="go">sudo /Volumes/Docker/Docker.app/Contents/MacOS/install --allowed-org=myorg
</span></span></span><span class="line"><span class="cl"><span class="go">sudo hdiutil detach /Volumes/Docker
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 方法优先级

当同一系统上存在多种配置方法时，Docker Desktop 使用以下优先级顺序：

1. 注册表项（仅限 Windows）
2. 配置文件（仅限 macOS）
3. plist 文件（仅限 macOS）
4. registry.json 文件

> [!IMPORTANT]
>
> Docker Desktop 4.36 及更高版本支持在单个配置中设置多个组织。早期版本（4.35 及以下）在指定多个组织时会静默失败。

## 登录强制执行问题排查

如果登录强制执行不起作用：

- 验证文件位置和权限
- 检查组织名称是否使用了小写字母
- 重启 Docker Desktop 或重启系统
- 确认用户是指定组织的成员
- 将 Docker Desktop 更新到最新版本
