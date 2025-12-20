# 使用 Jamf Pro 部署





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



了解如何使用 Jamf Pro 部署适用于 Mac 的 Docker Desktop，包括上传安装程序以及创建部署策略。

首先，上传软件包：

1. 在 Jamf Pro 控制台中，导航至 **计算机** > **管理设置** > **计算机管理** > **软件包**。
2. 选择 **新建** 以添加新软件包。
3. 上传 `Docker.pkg` 文件。

接下来，创建用于部署的策略：

1. 导航至 **计算机** > **策略**。
2. 选择 **新建** 以创建新策略。
3. 为策略输入名称，例如“部署 Docker Desktop”。
4. 在 **软件包** 选项卡下，添加您上传的 Docker 软件包。
5. 配置范围以指定要在哪些设备或设备组上安装 Docker。
6. 保存策略并部署。

有关更多信息，请参阅 [Jamf Pro 官方文档](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html)。

## 其他资源

- 了解如何为您的用户[强制登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。
