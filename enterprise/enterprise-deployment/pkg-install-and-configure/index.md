# PKG 安装程序





  
  
  
  


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
    
  
  <a class="link" href="https://docs.docker.com/desktop/release-notes/#4360">4.36</a> and later</span>
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



PKG 安装包支持各种 MDM（移动设备管理）解决方案，非常适合批量安装，无需每个用户手动设置。借助此安装包，IT 管理员可以确保 Docker Desktop 的标准化、策略驱动安装，从而提高整个组织的效率和软件管理水平。

## 交互式安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 在 **macOS** 选项卡中，选择 **Download PKG installer** 按钮。
4. 下载后，双击 `Docker.pkg` 运行安装程序。
5. 按照安装向导的说明授权安装程序并继续安装。
   - **简介**：选择 **Continue**。
   - **许可**：查看许可协议并选择 **Agree**。
   - **选择目标**：此步骤可选。建议保留默认安装目标（通常为 `Macintosh HD`）。选择 **Continue**。
   - **安装类型**：选择 **Install**。
   - **安装**：使用您的管理员密码或 Touch ID 进行身份验证。
   - **摘要**：安装完成后，选择 **Close**。

> [!NOTE]
>
> 使用 PKG 安装 Docker Desktop 时，应用内更新会自动禁用。这可以确保组织保持版本一致性，并防止未经批准的更新。对于使用 `.dmg` 安装程序安装的 Docker Desktop，仍支持应用内更新。
>
> 当有可用更新时，Docker Desktop 会通知您。要更新 Docker Desktop，请从 Docker Admin Console 下载最新的安装程序。导航到 **Enterprise deployment** 页面。
>
> 要了解最新版本，请查看[发行说明](/manuals/desktop/release-notes.md)页面。

## 从命令行安装

1. 在 [Docker Home](http://app.docker.com) 中，选择您的组织。
2. 选择 **Admin Console**，然后选择 **Enterprise deployment**。
3. 在 **macOS** 选项卡中，选择 **Download PKG installer** 按钮。
4. 在终端中，运行以下命令：

   ```console
   $ sudo installer -pkg "/path/to/Docker.pkg" -target /Applications
   ```

## 其他资源

- 了解如何使用 [Intune](use-intune.md) 或 [Jamf Pro](use-jamf-pro.md) 部署适用于 Mac 的 Docker Desktop
- 探索如何为您的用户[强制登录](/manuals/enterprise/security/enforce-sign-in/methods.md#plist-method-mac-only)。
