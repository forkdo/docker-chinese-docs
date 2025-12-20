# Docker Offload 使用与计费





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Early Access
          
            
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M263-465q26-69 64.5-130.5T415-712l-77-15q-20-4-39.5 2T265-705L129-568q-11 11-8 26.5t17 21.5l125 55Zm580-398q-109-8-206.5 37.5T461-702q-50 50-88.5 106.5T309-473q-4 10-4 20t8 18l135 135q8 8 18 8t20-4q66-24 122.5-63T715-448q78-78 124-175.5T877-830q-1-6-3.5-11.5T866-852q-5-5-10.5-7.5T843-863ZM586-573q-20-20-20-49.5t20-49.5q20-20 49.5-20t49.5 20q20 20 20 49.5T685-573q-20 20-49.5 20T586-573ZM479-250l54 125q6 15 22 17.5t27-8.5l136-136q14-14 20-33.5t2-39.5l-14-77q-55 49-116.5 87.5T479-250Zm-317-68q35-35 85-35.5t85 34.5q35 35 35 85t-35 85q-48 48-113.5 57T87-74q9-66 18.5-131.5T162-318Z"/></svg></span>
            
          
            
          
            
          
            
          
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 4.50 and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



> [!NOTE]
>
> 为 Docker Offload Beta 授予的所有免费试用额度自授予之日起 90 天后过期。若要在试用额度到期后继续使用 Docker Offload Beta，您可以在 [Docker Home 计费](https://app.docker.com/billing) 页面上启用按需使用功能。

## 了解使用和计费模式

Docker Offload 提供两种使用模式，以满足不同团队的需求和使用模式：

- **承诺使用量 (Committed usage)**：为您的组织提供承诺的云端计算时间。
- **按需使用量 (On-demand usage)**：提供随用随付的灵活性。您可以在[计费](#manage-billing)页面中启用或禁用按需使用。

## 管理计费

对于 Docker Offload，您可以在 [Docker Home 计费](https://app.docker.com/billing) 的 **Docker Offload** 页面上查看和配置计费。在此页面上，您可以：

- 查看您的承诺使用量
- 查看云资源的费率
- 管理按需计费，包括设置每月限额
- 跟踪您组织的 Docker Offload 使用情况
- 添加或更改付款方式

您必须是组织所有者才能管理计费。有关计费的更多信息，请参阅[计费](../billing/_index.md)。

## 监控您的使用情况

Docker Home 中的 **Offload 概览 (Offload overview)** 页面提供了对您如何使用云资源来构建和运行容器的可见性。

要监控您的使用情况：

1. 登录 [Docker Home](https://app.docker.com/)。
2. 选择您要监控使用情况的账户。
3. 选择 **Offload** > **Offload 概览 (Offload overview)**。

提供以下小组件：

- **我的近期会话 (My recent sessions)**：此小组件显示您的总会话时长，以及最近会话时长的细分。
- **我的前 10 个镜像 (My top 10 images)**：此小组件显示在运行会话中 Docker Offload 使用的前 10 个镜像。它提供了对最常使用镜像的洞察，帮助您了解容器使用模式。
- **我的活动会话 (My active sessions)**：此小组件显示当前任何活动的 Docker Offload 会话。

### 查看近期活动

Docker Home 中的 **近期活动 (Recent activity)** 页面提供了有关您近期 Docker Offload 会话的详细信息。这包括会话 ID、开始日期和时间、持续时间以及容器数量。

要查看**近期活动 (Recent activity)** 页面：

1. 登录 [Docker Home](https://app.docker.com/)。
2. 选择您要管理 Docker Offload 的账户。
3. 选择 **Offload** > **近期活动 (Recent activity)**。
