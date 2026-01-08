# 扩展 SDK 概览

本节中的资源可帮助您创建自己的 Docker 扩展。

Docker CLI 工具提供了一组命令来帮助您构建和发布扩展，这些扩展被打包为特殊格式的 Docker 镜像。

镜像文件系统的根目录下有一个 `metadata.json` 文件，用于描述扩展的内容。这是 Docker 扩展的基本要素。

扩展可以包含 UI 部分和在主机或 Desktop 虚拟机中运行的后端部分。更多信息请参阅 [架构](architecture/_index.md)。

您可以通过 Docker Hub 分发扩展。不过，您也可以在本地开发扩展，而无需将扩展推送到 Docker Hub。详情请参阅 [扩展分发](extensions/DISTRIBUTION.md)。



> 已经构建了一个扩展？
>
> 请通过 [反馈表单](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form) 告诉我们您的使用体验。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/extensions/extensions-sdk/process/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m222-299 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-235q-9 9-21 9t-21-9L101-335q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm0-320 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-555q-9 9-21 9t-21-9L101-655q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm328 329q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Zm0-320q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">构建和发布流程</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解构建和发布扩展的流程。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/extensions/extensions-sdk/quickstart/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-440q-17 0-28.5-11.5T440-480q0-17 11.5-28.5T480-520q17 0 28.5 11.5T520-480q0 17-11.5 28.5T480-440Zm0 360q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0 0q-141 0-240.5-99.5T140-480q0-142 99.5-241T480-820q142 0 241 99t99 241q0 141-99 240.5T480-140Zm64-261q5-2 8.5-5.5t5.5-8.5l118-241q5-10-2.5-17.5T656-676L415-558q-5 2-8.5 5.5T401-544L283-303q-5 10 2.5 17.5T303-283l241-118Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">快速入门指南</h3>
    </div>
    <div class="card-content">
      <p class="card-description">遵循快速入门指南快速创建一个基本的 Docker 扩展。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/extensions/extensions-sdk/design/design-guidelines/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m357-513 90-90-75-75-27 27q-9 9-21 9t-21-9q-9-9-9-21t9-21l27-27-75-74-90 90 192 191Zm346 348 90-91-75-75-27 27q-9 9-21 9t-21-9q-9-9-9-21t9-21l27-27-74-74-90 90 191 192Zm-87-520 70 70 94-94-70-70-94 94ZM150-120q-13 0-21.5-8.5T120-150v-114q0-6 2-11t7-10l185-185-202-202q-14-14-13.5-32t13.5-32l110-112q14-14 32-14t32 14l204 203 178-178q9-9 20-13t22-4q11 0 22 4t20 13l71 71q9 9 13 20t4 22q0 11-4 22t-13 20L645-490l203 203q14 14 14 32t-14 32L737-113q-14 14-32 14t-32-14L471-315 285-129q-5 5-10 7t-11 2H150Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">查看设计指南</h3>
    </div>
    <div class="card-content">
      <p class="card-description">确保您的扩展符合 Docker 的设计指南和原则。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/extensions/extensions-sdk/extensions/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m450-531-99 99q-8.8 9-20.9 8.5-12.1-.5-21.49-9.5-8.61-9-8.61-21.5t9-21.5l150-150q5-5 10.13-7 5.14-2 11-2 5.87 0 10.87 2 5 2 10 7l151 151q9 9 9 21t-8.61 21q-9.39 9-21.89 9t-21.5-9l-99-98v341q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-341Zm-290-96v-113q0-24 18-42t42-18h520q24 0 42 18t18 42v113q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-113H220v113q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">发布您的扩展</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何将您的扩展发布到 Marketplace。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/extensions/extensions-sdk/guides/kubernetes/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m234-292 69 69q9 9 9 21t-9 21q-9 9-21 9t-21-9L141-301q-5-5-7-10t-2-11q0-6 2-11t7-10l120-120q9-9 21-9t21 9q9 9 9 21t-9 21l-69 69h256q13 0 21.5 8.5T520-322q0 13-8.5 21.5T490-292H234Zm376 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T640-322q0 12-8.5 21t-21.5 9Zm120 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T760-322q0 12-8.5 21t-21.5 9Zm-4-316H470q-13 0-21.5-8.5T440-638q0-13 8.5-21.5T470-668h256l-69-69q-9-9-9-21t9-21q9-9 21-9t21 9l120 120q5 5 7 10t2 11q0 6-2 11t-7 10L699-497q-9 9-21 9t-21-9q-9-9-9-21t9-21l69-69Zm-496 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T260-638q0 12-8.5 21t-21.5 9Zm120 0q-12 0-21-9t-9-21q0-13 9-21.5t21-8.5q13 0 21.5 8.5T380-638q0 12-8.5 21t-21.5 9Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">与 Kubernetes 交互</h3>
    </div>
    <div class="card-content">
      <p class="card-description">查找有关如何从您的 Docker 扩展中间接与 Kubernetes 集群交互的信息。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/extensions/extensions-sdk/extensions/multi-arch/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">多架构扩展</h3>
    </div>
    <div class="card-content">
      <p class="card-description">为您的扩展构建多个架构版本。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [构建和发布流程](/extensions/extensions-sdk/process/)

- [快速入门](/extensions/extensions-sdk/quickstart/)

- [第二部分：发布](/extensions/extensions-sdk/extensions/)

- [扩展架构](/extensions/extensions-sdk/architecture/)

- [Docker 扩展的 UI 样式概览](/extensions/extensions-sdk/design/)

- [](/extensions/extensions-sdk/dev/)

