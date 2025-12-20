# Compose 文件参考

>**刚接触 Docker Compose？**
>
> 查找有关 [Docker Compose 的关键特性和使用场景](/manuals/compose/intro/features-uses.md) 的更多信息，或 [尝试快速入门指南](/manuals/compose/gettingstarted.md)。

Compose 规范是 Compose 文件格式的最新且推荐的版本。它帮助您定义 [Compose 文件](/manuals/compose/intro/compose-application-model.md)，用于配置 Docker 应用程序的服务、网络、卷等。

Compose 文件格式的旧版本 2.x 和 3.x 已合并到 Compose 规范中。它在 Docker Compose CLI 的 1.27.0 及以上版本（也称为 Compose v2）中实现。

Docker Docs 上的 Compose 规范是 Docker Compose 的实现。如果您希望实现自己的 Compose 规范版本，请参阅 [Compose 规范仓库](https://github.com/compose-spec/compose-spec)。

使用以下链接导航 Compose 规范的关键部分。

> [!TIP]
>
> 希望在 VS Code 中获得更好的 Compose 文件编辑体验？
> 查看 [Docker VS Code 扩展（Beta）](https://marketplace.visualstudio.com/items?itemName=docker.docker)，支持代码检查、代码导航和漏洞扫描功能。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/reference/compose-file/version-and-name/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24.75 0-42.37-17.63Q120-155.25 120-180v-600q0-24.75 17.63-42.38Q155.25-840 180-840h375q12.44 0 23.72 5T598-822l224 224q8 8 13 19.28 5 11.28 5 23.72v375q0 24.75-17.62 42.37Q804.75-120 780-120H180Zm129-171h342q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-159h342q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-159h216q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Version and name top-level element</h3>
    </div>
    <div class="card-content">
      <p class="card-description">理解 Compose 的 version 和 name 属性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/compose-file/services/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M740-149 517-371l57-57 223 223q12 12 12 28t-12 28q-12 12-28.5 12T740-149Zm-581 0q-12-12-12-28.5t12-28.5l261-261-107-107-2 2q-9 9-21 9t-21-9l-23-23v97q0 10-9.5 13.5T220-488L102-606q-7-7-3.5-16.5T112-632h98l-27-27q-9-9-9-21t9-21l110-110q17-17 37-23t44-6q21 0 36 5.5t32 18.5q5 5 5.5 11t-4.5 11l-95 95 27 27q9 9 9 21t-9 21l-3 3 104 104 122-122q-8-13-12.5-30t-4.5-36q0-53 38.5-91.5T711-841q8 0 14.5.5T737-838q6 3 7.5 9.5T741-817l-61 61q-5 5-5 11t5 11l53 53q5 5 11 5t11-5l59-59q5-5 13-4t11 8q2 6 2.5 12.5t.5 14.5q0 53-38.5 91.5T711-579q-18 0-31-2.5t-24-7.5L215-148q-12 12-28 11.5T159-149Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Services top-level element</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索 Compose 的所有 services 属性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/compose-file/networks/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M120-140v-150q0-24.75 17.63-42.38Q155.25-350 180-350h60v-100q0-24.75 17.63-42.38Q275.25-510 300-510h150v-100h-60q-24.75 0-42.37-17.63Q330-645.25 330-670v-150q0-24.75 17.63-42.38Q365.25-880 390-880h180q24.75 0 42.38 17.62Q630-844.75 630-820v150q0 24.75-17.62 42.37Q594.75-610 570-610h-60v100h150q24.75 0 42.38 17.62Q720-474.75 720-450v100h60q24.75 0 42.38 17.62Q840-314.75 840-290v150q0 24.75-17.62 42.37Q804.75-80 780-80H600q-24.75 0-42.37-17.63Q540-115.25 540-140v-150q0-24.75 17.63-42.38Q575.25-350 600-350h60v-100H300v100h60q24.75 0 42.38 17.62Q420-314.75 420-290v150q0 24.75-17.62 42.37Q384.75-80 360-80H180q-24.75 0-42.37-17.63Q120-115.25 120-140Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Networks top-level element</h3>
    </div>
    <div class="card-content">
      <p class="card-description">查找 Compose 的所有 networks 属性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/compose-file/volumes/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-520q161 0 260.5-49T840-680q0-63-99.5-111.5T480-840q-161 0-260.5 48.5T120-680q0 62 99.5 111T480-520Zm0 100q50 0 112-8.5T709.5-455q55.5-18 93-46.5T840-570v100q0 40-37.5 68.5t-93 46.5Q654-337 592-328.5T480-320q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-470v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-420Zm0 200q50 0 112-8.5T709.5-255q55.5-18 93-46.5T840-370v100q0 40-37.5 68.5t-93 46.5Q654-137 592-128.5T480-120q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-270v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Volumes top-level element</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索 Compose 的所有 volumes 属性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/compose-file/configs/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M421-80q-14 0-25-9t-13-23l-15-94q-19-7-40-19t-37-25l-86 40q-14 6-28 1.5T155-226L97-330q-8-13-4.5-27t15.5-23l80-59q-2-9-2.5-20.5T185-480q0-9 .5-20.5T188-521l-80-59q-12-9-15.5-23t4.5-27l58-104q8-13 22-17.5t28 1.5l86 40q16-13 37-25t40-18l15-95q2-14 13-23t25-9h118q14 0 25 9t13 23l15 94q19 7 40.5 18.5T669-710l86-40q14-6 27.5-1.5T804-734l59 104q8 13 4.5 27.5T852-580l-80 57q2 10 2.5 21.5t.5 21.5q0 10-.5 21t-2.5 21l80 58q12 8 15.5 22.5T863-330l-58 104q-8 13-22 17.5t-28-1.5l-86-40q-16 13-36.5 25.5T592-206l-15 94q-2 14-13 23t-25 9H421Zm59-270q54 0 92-38t38-92q0-54-38-92t-92-38q-54 0-92 38t-38 92q0 54 38 92t92 38Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Configs top-level element</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Compose 中的 configs。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/compose-file/secrets/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24.75 0-42.37-17.63Q160-115.25 160-140v-434q0-24.75 17.63-42.38Q195.25-634 220-634h70v-96q0-78.85 55.61-134.42Q401.21-920 480.11-920q78.89 0 134.39 55.58Q670-808.85 670-730v96h70q24.75 0 42.38 17.62Q800-598.75 800-574v434q0 24.75-17.62 42.37Q764.75-80 740-80H220Zm260.17-200q31.83 0 54.33-22.03T557-355q0-30-22.67-54.5t-54.5-24.5q-31.83 0-54.33 24.5t-22.5 55q0 30.5 22.67 52.5t54.5 22ZM350-634h260v-96q0-54.17-37.88-92.08-37.88-37.92-92-37.92T388-822.08q-38 37.91-38 92.08v96Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Secrets top-level element</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Compose 中的 secrets。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [Version and name top-level elements](/reference/compose-file/version-and-name/)

- [在 Docker Compose 中定义服务](/reference/compose-file/services/)

- [在 Docker Compose 中定义和管理网络](/reference/compose-file/networks/)

- [在 Docker Compose 中定义和管理卷](/reference/compose-file/volumes/)

- [Configs 顶级元素](/reference/compose-file/configs/)

- [Secrets](/reference/compose-file/secrets/)

- [片段](/reference/compose-file/fragments/)

- [扩展](/reference/compose-file/extension/)

- [插值](/reference/compose-file/interpolation/)

- [合并 Compose 文件](/reference/compose-file/merge/)

- [使用 include 模块化 Compose 文件](/reference/compose-file/include/)

- [模型](/reference/compose-file/models/)

- [学习在 Docker Compose 中使用配置文件](/reference/compose-file/profiles/)

- [Compose 构建规范](/reference/compose-file/build/)

- [Compose 部署规范](/reference/compose-file/deploy/)

- [Compose 开发规范](/reference/compose-file/develop/)

- [旧版本](/reference/compose-file/legacy-versions/)

