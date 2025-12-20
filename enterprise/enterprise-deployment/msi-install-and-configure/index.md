# MSI 安装程序





  
  
  
  


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
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="https://docs.docker.com/desktop/release-notes/#4320">4.32</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
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



MSI 安装包支持各种 MDM（移动设备管理）解决方案，非常适合批量安装，无需用户手动设置。借助此安装包，IT 管理员可以确保 Docker Desktop 的标准化、策略驱动安装，从而提高整个组织的效率和软件管理水平。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 在 **Windows OS** 选项卡中，选择 **Download MSI installer** 按钮。
4. 下载后，双击 `Docker Desktop Installer.msi` 运行安装程序。
5. 接受许可协议后，选择安装位置。默认情况下，Docker Desktop 安装在 `C:\Program Files\Docker\Docker`。
6. 配置 Docker Desktop 安装。您可以：

    - 创建桌面快捷方式

    - 将 Docker Desktop 服务启动类型设置为自动

    - 禁用 Windows 容器使用

    - 选择 Docker Desktop 后端：WSL 或 Hyper-V。如果您的系统仅支持一种，则无法选择。
7. 按照安装向导上的说明授权安装程序并继续安装。
8. 安装成功后，选择 **Finish** 完成安装过程。

如果您的管理员帐户与用户帐户不同，您必须将用户添加到 **docker-users** 组才能访问需要更高权限的功能，例如创建和管理 Hyper-V 虚拟机或使用 Windows 容器：

1. 以**管理员**身份运行**计算机管理**。
2. 导航到**本地用户和组** > **组** > **docker-users**。
3. 右键单击以将用户添加到组中。
4. 注销并重新登录以使更改生效。

> [!NOTE]
>
> 使用 MSI 安装 Docker Desktop 时，应用内更新会自动禁用。这可以确保组织保持版本一致性并防止未经批准的更新。对于使用 .exe 安装程序安装的 Docker Desktop，应用内更新仍然受支持。
>
> 当有可用更新时，Docker Desktop 会通知您。要更新 Docker Desktop，请从 Docker Admin Console 下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要了解最新版本，请查看[发行说明](/manuals/desktop/release-notes.md)页面。

## 从命令行安装

本节介绍使用 PowerShell 进行 Docker Desktop 的命令行安装。它提供了您可以运行的常见安装命令。您还可以添加其他参数，这些参数在[配置选项](#configuration-options)中概述。

安装 Docker Desktop 时，您可以在交互式安装和非交互式安装之间进行选择。

交互式安装（不指定 `/quiet` 或 `/qn`）会显示用户界面，让您选择自己的属性。

通过用户界面安装时，可以：

- 选择目标文件夹
- 创建桌面快捷方式
- 配置 Docker Desktop 服务启动类型
- 禁用 Windows 容器
- 在 WSL 或 Hyper-V 引擎之间进行选择

非交互式安装是静默的，任何额外的配置都必须作为参数传递。

### 常见安装命令

> [!IMPORTANT]
>
> 运行以下任何命令都需要管理员权限。

#### 交互式安装并记录详细日志

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log"
```

#### 交互式安装但不记录详细日志

```powershell
msiexec /i "DockerDesktop.msi"
```

#### 非交互式安装并记录详细日志

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet
```

#### 非交互式安装并禁止重启

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart
```

#### 非交互式安装并使用管理员设置

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart ADMINSETTINGS="{""configurationFileVersion"":2,""enhancedContainerIsolation"":{""value"":true,""locked"":false}}" ALLOWEDORG="your-organization"
```

#### 交互式安装并允许用户无需管理员权限即可切换到 Windows 容器

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /quiet /norestart ALLOWEDORG="your-organization" ALWAYSRUNSERVICE=1
```

#### 交互式安装并指定 PAC 文件

```powershell
PowerShell
 msiexec --% /i "DockerDesktop.msi" /L*V ".\msi.log"  PROXYHTTPMODE="manual" OVERRIDEPROXYPAC="http://localhost:8080/myproxy.pac"
```

#### 交互式安装并指定 PAC 脚本

```powershell
PowerShell
 msiexec --% /i "DockerDesktop.msi" /L*V ".\msi.log"  PROXYHTTPMODE="manual" OVERRIDEPROXYEMBEDDEDPAC="function FindProxyForURL(url,host) {return ""DIRECT"" ;; }"
```

#### 使用被动显示选项安装

当您想要执行非交互式安装但显示进度对话框时，可以使用 `/passive` 显示选项代替 `/quiet`。

在被动模式下，安装程序不会向用户显示任何提示或错误消息，并且安装无法取消。

例如：

```powershell
msiexec /i "DockerDesktop.msi" /L*V ".\msi.log" /passive /norestart
```

> [!TIP]
>
> 创建期望 JSON 字符串的值时：
>
> - 该属性期望一个 JSON 格式的字符串
> - 字符串应用双引号括起来
> - 字符串不应包含任何空格
> - 属性名称应为双引号

### 常见卸载命令

卸载 Docker Desktop 时，需要使用最初用于安装应用程序的相同 `.msi` 文件。

如果您不再拥有原始的 `.msi` 文件，则需要使用与安装关联的产品代码。要查找产品代码，请运行：

```powershell
Get-WmiObject Win32_Product | Select-Object IdentifyingNumber, Name | Where-Object {$_.Name -eq "Docker Desktop"}
```

它应返回类似于以下内容的输出：

```text
IdentifyingNumber                      Name
-----------------                      ----
{10FC87E2-9145-4D7D-B493-2E99E8D8E103} Docker Desktop
```
> [!NOTE]
>
> 此命令可能需要一些时间，具体取决于已安装应用程序的数量。

`IdentifyingNumber` 是应用程序的产品代码，可用于卸载 Docker Desktop。例如：

```powershell
msiexec /x {10FC87E2-9145-4D7D-B493-2E99E8D8E103} /L*V ".\msi.log" /quiet
```

#### 交互式卸载并记录详细日志

```powershell
msiexec /x "DockerDesktop.msi" /L*V ".\msi.log"
```

#### 交互式卸载但不记录详细日志

```powershell
msiexec /x "DockerDesktop.msi"
```

#### 非交互式卸载并记录详细日志

```powershell
msiexec /x "DockerDesktop.msi" /L*V ".\msi.log" /quiet
```

#### 非交互式卸载但不记录详细日志

```powershell
msiexec /x "DockerDesktop.msi" /quiet
```

### 配置选项

> [!IMPORTANT]
>
> 除了以下自定义属性外，Docker Desktop MSI 安装程序还支持标准的 [Windows Installer 命令行选项](https://learn.microsoft.com/en-us/windows/win32/msi/standard-installer-command-line-options)。

| 属性 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `ENABLEDESKTOPSHORTCUT` | 创建桌面快捷方式。 | 1 |
| `INSTALLFOLDER` | 指定 Docker Desktop 将要安装的自定义位置。 | C:\Program Files\Docker |
| `ADMINSETTINGS` | 自动创建一个 `admin-settings.json` 文件，用于在组织内的客户端计算机上[控制某些 Docker Desktop 设置](/manuals/enterprise/security/hardened-desktop/settings-management/_index.md)。必须与 `ALLOWEDORG` 属性一起使用。 | 无 |
| `ALLOWEDORG` | 要求用户在运行应用程序时登录并成为指定的 Docker Hub 组织的一部分。这会在 `HKLM\Software\Policies\Docker\Docker Desktop` 中创建一个名为 `allowedOrgs` 的注册表项。 | 无 |
| `ALWAYSRUNSERVICE` | 允许用户在不需要管理员权限的情况下切换到 Windows 容器 | 0 |
| `DISABLEWINDOWSCONTAINERS` | 禁用 Windows 容器集成 | 0 |
| `ENGINE` | 设置用于运行容器的 Docker 引擎。可以是 `wsl`、`hyperv` 或 `windows` | `wsl` |
| `PROXYENABLEKERBEROSNTLM` | 设置为 1 时，启用对 Kerberos 和 NTLM 代理身份验证的支持。适用于 Docker Desktop 4.33 及更高版本 | 0 |
| `PROXYHTTPMODE` | 设置 HTTP 代理模式。可以是 `system` 或 `manual` | `system` |
| `OVERRIDEPROXYHTTP` | 设置必须用于传出 HTTP 请求的 HTTP 代理的 URL。 | 无 |
| `OVERRIDEPROXYHTTPS` | 设置必须用于传出 HTTPS 请求的 HTTP 代理的 URL。 | 无 |
| `OVERRIDEPROXYEXCLUDE` | 绕过主机和域的代理设置。使用逗号分隔的列表。 | 无 |
| `OVERRIDEPROXYPAC` | 设置 PAC 文件 URL。此设置仅在使用 `manual` 代理模式时生效。 | 无 |
| `OVERRIDEPROXYEMBEDDEDPAC` | 指定嵌入式 PAC（代理自动配置）脚本。此设置仅在使用 `manual` 代理模式时生效，并且优先于 `OVERRIDEPROXYPAC` 标志。 | 无 |
| `HYPERVDEFAULTDATAROOT` | 指定 Hyper-V 虚拟机磁盘的默认位置。 | 无 |
| `WINDOWSCONTAINERSDEFAULTDATAROOT` | 指定 Windows 容器的默认位置。 | 无 |
| `WSLDEFAULTDATAROOT` | 指定 WSL 发行版磁盘的默认位置。 | 无 |
| `DISABLEANALYTICS` | 设置为 1 时，将禁用 MSI 的分析收集。有关更多信息，请参阅[分析](#analytics)。 | 0 |

此外，您还可以使用 `/norestart` 或 `/forcerestart` 来控制重启行为。

默认情况下，安装程序在成功安装后会重新启动计算机。当以静默方式运行时，重启是自动的，不会提示用户。

## 分析

MSI 安装程序仅收集与安装相关的匿名使用统计数据。这是为了更好地了解用户行为，并通过识别和解决问题或优化流行功能来改善用户体验。

### 如何选择退出








<div
  class="tabs"
  
    x-data="{ selected: '%E4%BB%8E-GUI' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E-GUI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BB%8E-GUI'"
        
      >
        从 GUI
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%BB%8E%E5%91%BD%E4%BB%A4%E8%A1%8C' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%BB%8E%E5%91%BD%E4%BB%A4%E8%A1%8C'"
        
      >
        从命令行
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E-GUI' && 'hidden'"
      >
        <p>当您从默认安装程序 GUI 安装 Docker Desktop 时，选择 <strong>Welcome</strong> 对话框左下角的 <strong>Disable analytics</strong> 复选框。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%BB%8E%E5%91%BD%E4%BB%A4%E8%A1%8C' && 'hidden'"
      >
        <p>当您从命令行安装 Docker Desktop 时，使用 <code>DISABLEANALYTICS</code> 属性。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'bXNpZXhlYyAvaSAid2luXG1zaVxiaW5cZW4tVVNcRG9ja2VyRGVza3RvcC5tc2kiIC9MKlYgIi5cbXNpLmxvZyIgRElTQUJMRUFOQUxZVElDUz0x', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-powershell" data-lang="powershell"><span class="line"><span class="cl"><span class="n">msiexec</span> <span class="p">/</span><span class="n">i</span> <span class="s2">&#34;win\msi\bin\en-US\DockerDesktop.msi&#34;</span> <span class="p">/</span><span class="n">L</span><span class="p">*</span><span class="n">V</span> <span class="s2">&#34;.\msi.log&#34;</span> <span class="n">DISABLEANALYTICS</span><span class="p">=</span><span class="mf">1</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


### 持久性

如果您决定为安装禁用分析，您的选择将保留在注册表中，并在未来的升级和卸载中得到遵守。

但是，当 Docker Desktop 卸载时，该密钥会被删除，必须通过之前的方法之一重新配置。

注册表密钥如下：

```powershell
SOFTWARE\Docker Inc.\Docker Desktop\DisableMsiAnalytics
```

禁用分析时，此密钥设置为 `1`。

## 其他资源

- [查看常见问题解答](/manuals/enterprise/enterprise-deployment/faq.md)
