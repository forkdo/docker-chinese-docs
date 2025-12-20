# Docker Build Cloud





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Pro</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M730-530H630q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h100v-100q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v100h100q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H790v100q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-100Zm-370 49q-66 0-108-42t-42-108q0-66 42-108t108-42q66 0 108 42t42 108q0 66-42 108t-108 42ZM40-220v-34q0-35 17.5-63.5T108-360q75-33 133.34-46.5t118.5-13.5Q420-420 478-406.5T611-360q33 15 51 43t18 63v34q0 24.75-17.62 42.37Q644.75-160 620-160H100q-24.75 0-42.37-17.63Q40-195.25 40-220Z"/></svg>
            
          </span>
        
          <span>Team</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M30-240q-12.75 0-21.37-8.63Q0-257.25 0-270v-23q0-38.57 41.5-62.78Q83-380 150.38-380q12.16 0 23.39.5t22.23 2.15q-8 17.35-12 35.17-4 17.81-4 37.18v65H30Zm240 0q-12.75 0-21.37-8.63Q240-257.25 240-270v-35q0-32 17.5-58.5T307-410q32-20 76.5-30t96.5-10q53 0 97.5 10t76.5 30q32 20 49 46.5t17 58.5v35q0 12.75-8.62 21.37Q702.75-240 690-240H270Zm510 0v-65q0-19.86-3.5-37.43T765-377.27q11-1.73 22.17-2.23 11.17-.5 22.83-.5 67.5 0 108.75 23.77T960-293v23q0 12.75-8.62 21.37Q942.75-240 930-240H780ZM149.57-410q-28.57 0-49.07-20.56Q80-451.13 80-480q0-29 20.56-49.5Q121.13-550 150-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T149.57-410Zm660 0q-28.57 0-49.07-20.56Q740-451.13 740-480q0-29 20.56-49.5Q781.13-550 810-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T809.57-410ZM480-480q-50 0-85-35t-35-85q0-51 35-85.5t85-34.5q51 0 85.5 34.5T600-600q0 50-34.5 85T480-480Z"/></svg>
            
          </span>
        
          <span>Business</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-180v-600q0-24.75 17.63-42.38Q115.25-840 140-840h270q24.75 0 42.38 17.62Q470-804.75 470-780v105h350q24.75 0 42.38 17.62Q880-639.75 880-615v435q0 24.75-17.62 42.37Q844.75-120 820-120H140q-24.75 0-42.37-17.63Q80-155.25 80-180Zm60 0h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm165 495h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm165 495h350v-435H470v105h80v60h-80v105h80v60h-80v105Zm185-270v-60h60v60h-60Zm0 165v-60h60v60h-60Z"/></svg>
            
          </span>
        
      </div>
    

    

    

    
  </div>



Docker Build Cloud 是一项服务，可让您在本地和 CI 中更快地构建容器镜像。构建在针对您的工作负载优化配置的云基础设施上运行，无需任何配置。该服务使用远程构建缓存，确保任何位置和所有团队成员都能快速构建。

## Docker Build Cloud 的工作原理

使用 Docker Build Cloud 与运行常规构建没有区别。您使用 `docker buildx build` 像平常一样调用构建命令。不同之处在于构建的执行位置和方式。

默认情况下，当您调用构建命令时，构建在本地运行的 BuildKit 实例上执行，该实例与 Docker 守护进程捆绑在一起。而使用 Docker Build Cloud 时，您将构建请求发送到云中远程运行的 BuildKit 实例。所有数据在传输过程中都会被加密。

远程构建器执行构建步骤，并将生成的构建输出发送到您指定的目标。例如，发送回您的本地 Docker Engine 镜像存储，或发送到镜像注册表。

Docker Build Cloud 相比本地构建提供了多项优势：

- 提升构建速度
- 共享构建缓存
- 原生多平台构建

最棒的部分是：您无需担心管理构建器或基础设施。只需连接到您的构建器，然后开始构建即可。分配给组织的每个云构建器都完全隔离到单个 Amazon EC2 实例，具有专用的 EBS 卷用于构建缓存，并支持传输加密。这意味着云构建器之间没有共享的进程或数据。

> [!NOTE]
>
> Docker Build Cloud 目前仅在美东地区提供。欧洲和亚洲的用户相比北美地区的用户可能会遇到更高的延迟。
>
> 多地区构建器支持已在路线图中。

## 获取 Docker Build Cloud

要开始使用 Docker Build Cloud，[创建一个 Docker 账户](/accounts/create-account/)。有两种方式可以获取 Docker Build Cloud：

- 拥有免费个人账户的用户可以选择参加 7 天免费试用，并可选择订阅以继续使用。要开始免费试用，请登录 [Docker Build Cloud Dashboard](https://app.docker.com/build/) 并按照屏幕说明操作。
- 所有拥有付费 Docker 订阅的用户都可以使用 Docker Build Cloud，该服务已包含在他们的 Docker 产品套件中。更多信息请参阅 [Docker 订阅和功能](https://www.docker.com/pricing/)。

注册并创建构建器后，请继续[在本地环境中设置构建器](./setup.md)。

有关 Docker Build Cloud 的角色和权限信息，请参阅[角色和权限](/manuals/enterprise/security/roles-and-permissions.md#docker-build-cloud-permissions)。

- [Docker Build Cloud 设置](/build-cloud/setup/)

- [使用 Docker Build Cloud](/build-cloud/usage/)

- [在 CI 中使用 Docker Build Cloud](/build-cloud/ci/)

- [优化云端构建](/build-cloud/optimization/)

- [Builder settings](/build-cloud/builder-settings/)

- [Docker Build Cloud 发布说明](/build-cloud/release-notes/)

