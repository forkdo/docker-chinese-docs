# Docker Offload 快速开始





  
  
  
  


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



[Docker Offload](./about.md) 让您可以在云中构建和运行容器，同时使用本地的 Docker Desktop 工具和工作流。这意味着更快的构建速度、访问强大的云资源，以及无缝的开发体验。

本快速开始指南涵盖了开发者开始使用 Docker Offload 所需的步骤。

> [!NOTE]
>
> 如果您是组织所有者，要开始使用 Docker Offload，必须先[注册](https://www.docker.com/products/docker-offload/)并为您的组织订阅 Docker Offload。订阅后，请参阅以下内容：
>
> - [管理 Docker 产品](../admin/organization/manage-products.md) 了解如何为组织中的开发者管理访问权限。
> - [用量和计费](./usage.md) 了解如何设置计费和监控用量。

## 前置条件

- 您必须已安装 [Docker Desktop](/desktop/)。Docker Offload 适用于 Docker Desktop 4.50 或更高版本。
- 您必须能够访问 Docker Offload。您的组织所有者必须已为组织[注册](https://www.docker.com/products/docker-offload/) Docker Offload。
- 您的组织必须有可用的承诺用量或已启用按需用量。这由您的组织所有者设置。详细信息请参阅 [Docker Offload 用量和计费](/offload/usage/)。

## 步骤 1：验证 Docker Offload 访问权限

要访问 Docker Offload，您必须是已订阅 Docker Offload 的组织成员。作为开发者，您可以通过检查 Docker Desktop 仪表板标题中是否出现 Docker Offload 切换开关来验证这一点。

1. 启动 Docker Desktop 并登录。
2. 在 Docker Desktop 仪表板标题中，查找 Docker Offload 切换开关。

![Offload 切换开关](./images/offload-toggle.png)

如果您看到 Docker Offload 切换开关，说明您已获得 Docker Offload 访问权限，可以继续下一步。如果您没有看到 Docker Offload 切换开关，请检查 Docker Offload 是否在您的 [Docker Desktop 设置](./configuration.md) 中被禁用，然后联系您的管理员，确认您的组织已订阅 Docker Offload 并已为您的组织启用访问权限。

## 步骤 2：启动 Docker Offload

您可以通过 CLI 或 Docker Desktop 仪表板标题启动 Docker Offload。以下步骤描述了如何使用 CLI 启动 Docker Offload。

1. 启动 Docker Desktop 并登录。
2. 打开终端并运行以下命令启动 Docker Offload：

   ```console
   $ docker offload start
   ```

   > [!TIP]
   >
   > 要了解有关 Docker Offload CLI 命令的更多信息，请参阅 [Docker Offload CLI 参考](/reference/cli/docker/offload/)。

3. 如果您是多个拥有 Docker Offload 访问权限的组织成员，您可以选择一个配置文件。所选组织将负责任何用量。

启动 Docker Offload 后，您将在 Docker Desktop 仪表板标题中看到云图标
(




  


<img
  loading="lazy"
  src=".././images/cloud-mode.png"
  alt="Offload 模式图标"
  
  class="inline my-0 not-prose"
/>
)
，Docker Desktop 仪表板将显示为紫色。您可以在终端中运行 `docker offload status` 命令来检查 Docker Offload 的状态。

## 步骤 3：使用 Docker Offload 运行容器

启动 Docker Offload 后，Docker Desktop 会连接到一个安全的云环境，该环境与您的本地体验相匹配。当您运行构建或容器时，它们会在远程执行，但行为与本地运行完全相同。

要验证 Docker Offload 是否正常工作，请运行一个容器：

```console
$ docker run --rm hello-world
```

如果 Docker Offload 正常工作，您将在终端输出中看到 `Hello from Docker!`。

## 步骤 4：监控您的 Offload 用量

当 Docker Offload 启动并且您已开始会话（例如，您已运行容器）时，您可以在 Docker Desktop 仪表板页脚中沙漏图标
(




  


<img
  loading="lazy"
  src=".././images/hourglass-icon.png"
  alt="Offload 会话时长"
  
  class="inline my-0 not-prose"
/>
)
旁边看到当前会话时长估算。

此外，当 Docker Offload 启动时，您可以通过在 Docker Desktop 仪表板左侧导航中选择 **Offload** > **Insights** 来查看详细的会话信息。

## 步骤 5：停止 Docker Offload

Docker Offload 在一段时间不活动后会自动[idle](./configuration.md#understand-active-and-idle-states)。您可以在任何时候停止它。要停止 Docker Offload：

```console
$ docker offload stop
```

停止 Docker Offload 后，云环境将被终止，所有正在运行的容器和镜像将被删除。当 Docker Offload 空闲约 5 分钟后，环境也会被终止，所有正在运行的容器和镜像将被删除。

要再次启动 Docker Offload，运行 `docker offload start` 命令。

## 下一步

在 Docker Desktop 中配置您的空闲超时。更多信息请参阅 [配置 Docker Offload](./configuration.md)。
