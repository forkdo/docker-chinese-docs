# Docker Compose

Docker Compose 是一款用于定义和运行多容器应用的工具。
它是实现流畅高效开发与部署体验的关键。

Compose 简化了对整个应用栈的控制，让您能够通过单个 YAML 配置文件轻松管理服务、网络和卷。然后，只需一个命令，即可从您的配置文件中创建并启动所有服务。

Compose 适用于所有环境——生产、预发布、开发、测试以及 CI 工作流。它还提供了用于管理应用整个生命周期的命令：

 - 启动、停止和重建服务
 - 查看正在运行的服务的状态
 - 流式传输正在运行的服务的日志输出
 - 在服务上运行一次性命令


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/compose/intro/features-uses/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M621-532q-72 0-123-51t-51-123q0-72 51-123t123-51q72 0 123 51t51 123q0 27-8.5 53T764-606l111 111q9 9 9 21t-9 21q-9 9-21.5 9t-21.5-9L720-564q-23 17-48 24.5t-51 7.5Zm0-60q48 0 81-33t33-81q0-48-33-81t-81-33q-48 0-81 33t-33 81q0 48 33 81t81 33ZM137-80q-24 0-42-18t-18-42v-590q0-24 18-42t42-18h203q13 0 20.5 11t4.5 24q-2 10-2.5 19t-.5 20q0 113 71 177.5T619-474q17 0 33.5-1.5T687-480l82 81q8 8 13 19.5t5 23.5v216q0 24-18 42t-42 18H137Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">为何使用 Compose？</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker Compose 的主要优势</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/compose/intro/compose-application-model/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m289-572 167-267q5-7 11-10.5t14-3.5q8 0 14 3.5t11 10.5l167 267q5 8 4.5 16t-4.5 15q-4 7-10.6 11t-15.4 4H315q-8.91 0-15.6-4.13-6.69-4.12-10.4-10.87-4-7-4.5-15t4.5-16ZM706-80q-72.5 0-123.25-50.75T532-254q0-72.5 50.75-123.25T706-428q72.5 0 123.25 50.75T880-254q0 72.5-50.75 123.25T706-80Zm-586-55v-244q0-12.75 8.63-21.38Q137.25-409 150-409h244q12.75 0 21.38 8.62Q424-391.75 424-379v244q0 12.75-8.62 21.37Q406.75-105 394-105H150q-12.75 0-21.37-8.63Q120-122.25 120-135Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Compose 如何工作</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Compose 的工作原理</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/compose/install" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M479.87-325q-5.87 0-10.87-2-5-2-10-7L308-485q-9-9.27-8.5-21.64.5-12.36 9.11-21.36 9.39-9 21.89-9t21.5 9l98 99v-341q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v341l99-99q8.8-9 20.9-8.5 12.1.5 21.49 9.5 8.61 9 8.61 21.5t-9 21.5L501-334q-5 5-10.13 7-5.14 2-11 2ZM220-160q-24 0-42-18t-18-42v-113q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v113h520v-113q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v113q0 24-18 42t-42 18H220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">安装 Compose</h3>
    </div>
    <div class="card-content">
      <p class="card-description">查看如何安装 Docker Compose 的说明。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/compose/gettingstarted" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-440q-17 0-28.5-11.5T440-480q0-17 11.5-28.5T480-520q17 0 28.5 11.5T520-480q0 17-11.5 28.5T480-440Zm0 360q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0 0q-141 0-240.5-99.5T140-480q0-142 99.5-241T480-820q142 0 241 99t99 241q0 141-99 240.5T480-140Zm64-261q5-2 8.5-5.5t5.5-8.5l118-241q5-10-2.5-17.5T656-676L415-558q-5 2-8.5 5.5T401-544L283-303q-5 10 2.5 17.5T303-283l241-118Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">快速入门</h3>
    </div>
    <div class="card-content">
      <p class="card-description">在构建一个简单的 Python Web 应用的同时，学习 Docker Compose 的核心概念。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="https://github.com/docker/compose/releases" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24 0-42-18t-18-42v-680q0-24 18-42t42-18h336q12.44 0 23.72 5T599-862l183 183q8 8 13 19.28 5 11.28 5 23.72v496q0 24-18 42t-42 18H220Zm331-584q0 12.75 8.63 21.37Q568.25-634 581-634h159L551-820v156ZM450-363v99q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63 12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-99h100q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H510v-100q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v100H350q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5h100Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">查看发行说明</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解最新的功能增强和错误修复。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/compose-file" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M620-140v-35L310-330H180q-24.75 0-42.37-17.63Q120-365.25 120-390v-100q0-24.75 17.63-42.38Q155.25-550 180-550h115l125-139.5V-820q0-24.75 17.63-42.38Q455.25-880 480-880h100q24.75 0 42.38 17.62Q640-844.75 640-820v100q0 24.75-17.62 42.37Q604.75-660 580-660H474L340-510v129l280 139q1-24 18.5-41t41.5-17h100q24.75 0 42.38 17.62Q840-264.75 840-240v100q0 24.75-17.62 42.37Q804.75-80 780-80H680q-24.75 0-42.37-17.63Q620-115.25 620-140Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">探索 Compose 文件参考</h3>
    </div>
    <div class="card-content">
      <p class="card-description">查找有关为 Docker 应用定义服务、网络和卷的信息。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/compose/bridge" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M100-520q0 91 67 152.5T326-308l-68-68q-9-9-9-21t9-21q9-9 21.5-9t21.5 9l118 117q9 9 9 21t-9 21L301-141q-9 9-21 8.5t-21-9.5q-9-9-9-21.5t9-21.5l64-64q-116 6-199.5-73.5T40-520q0-117 81.5-198.5T320-800h90q13 0 21.5 8.5T440-770q0 13-8.5 21.5T410-740h-90q-92 0-156 64t-64 156Zm450 360q-13 0-21.5-8.5T520-190v-220q0-13 8.5-21.5T550-440h300q13 0 21.5 8.5T880-410v220q0 13-8.5 21.5T850-160H550Zm0-360q-13 0-21.5-8.5T520-550v-220q0-13 8.5-21.5T550-800h300q13 0 21.5 8.5T880-770v220q0 13-8.5 21.5T850-520H550Zm30-60h240v-160H580v160Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">使用 Compose Bridge</h3>
    </div>
    <div class="card-content">
      <p class="card-description">将您的 Compose 配置文件转换为不同平台（如 Kubernetes）的配置文件。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/compose/faq" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M484.03-247Q500-247 511-258.03q11-11.03 11-27T510.97-312q-11.03-11-27-11T457-311.97q-11 11.03-11 27T457.03-258q11.03 11 27 11Zm-3.76 167q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Zm2.5-580Q513-660 536-641.5q23 18.5 23 47.2 0 26.3-15.65 45.73Q527.7-529.14 508-512q-23 19-40 42.38-17 23.39-17 52.62 0 11 8.4 17.5T479-393q12 0 19.88-8 7.87-8 10.12-20 3-21 16-38t30.23-30.78Q580-510 596-537q16-27 16-58.61 0-50.39-37.5-83.89T485.55-713Q450-713 417-698t-54 44q-7 10-6.5 21.5t9.47 18.5q11.41 8 23.65 5 12.23-3 20.38-14 12.75-17.9 31.88-27.45Q461-660 482.77-660Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">浏览常见问题</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索常见问题并了解如何提供反馈。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [Docker Compose 安装概述](/compose/install/)

- [Docker Compose 快速入门](/compose/gettingstarted/)

- [Compose Bridge 概述](/compose/bridge/)

- [使用 Compose SDK](/compose/compose-sdk/)

- [发布说明](/compose/release-notes/)

