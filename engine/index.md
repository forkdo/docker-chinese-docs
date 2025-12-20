# Docker Engine

Docker Engine 是一种开源容器化技术，用于构建和容器化您的应用程序。Docker Engine 作为一个客户端-服务器应用程序运行，包含：

- 一个长期运行的守护进程 [`dockerd`](/reference/cli/dockerd) 的服务器
- 定义程序可用于与 Docker 守护进程通信和指示其操作的接口的 API
- 一个命令行界面（CLI）客户端 [`docker`](/reference/cli/docker/)

CLI 使用 [Docker API](/reference/api/engine/_index.md) 通过脚本或直接 CLI 命令来控制或与 Docker 守护进程交互。许多其他 Docker 应用程序使用底层的 API 和 CLI。守护进程创建和管理 Docker 对象，例如镜像、容器、网络和卷。

有关更多详细信息，请参阅 [Docker 架构](/get-started/docker-overview.md#docker-architecture)。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/engine/install" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M479.87-325q-5.87 0-10.87-2-5-2-10-7L308-485q-9-9.27-8.5-21.64.5-12.36 9.11-21.36 9.39-9 21.89-9t21.5 9l98 99v-341q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v341l99-99q8.8-9 20.9-8.5 12.1.5 21.49 9.5 8.61 9 8.61 21.5t-9 21.5L501-334q-5 5-10.13 7-5.14 2-11 2ZM220-160q-24 0-42-18t-18-42v-113q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v113h520v-113q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v113q0 24-18 42t-42 18H220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">安装 Docker Engine</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何为您的发行版安装开源 Docker Engine。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/storage" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-520q161 0 260.5-49T840-680q0-63-99.5-111.5T480-840q-161 0-260.5 48.5T120-680q0 62 99.5 111T480-520Zm0 100q50 0 112-8.5T709.5-455q55.5-18 93-46.5T840-570v100q0 40-37.5 68.5t-93 46.5Q654-337 592-328.5T480-320q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-470v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-420Zm0 200q50 0 112-8.5T709.5-255q55.5-18 93-46.5T840-370v100q0 40-37.5 68.5t-93 46.5Q654-137 592-128.5T480-120q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-270v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">存储</h3>
    </div>
    <div class="card-content">
      <p class="card-description">在 Docker 容器中使用持久化数据。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/network" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M209.9-80Q156-80 118-118.1q-38-38.1-38-92t38.07-91.9q38.07-38 91.93-38 19 0 36 5.03T278-321l172-171v-131q-43-11-71.5-45.99T350-750q0-53.86 38.1-91.93 38.1-38.07 92-38.07t91.9 38.07q38 38.07 38 91.93 0 46.02-28.5 81.01T510-623v131l172 171q15.45-8.94 32.45-13.97 17-5.03 35.55-5.03 53.86 0 91.93 38.1 38.07 38.1 38.07 92T841.9-118q-38.1 38-92 38T658-118.07q-38-38.07-38-91.93 0-19 5.03-36T639-278L480-438 321-278q8.94 15 13.97 32 5.03 17 5.03 36 0 53.86-38.1 91.93Q263.8-80 209.9-80Zm539.98-60q29.12 0 49.62-20.38 20.5-20.38 20.5-49.5t-20.38-49.62q-20.38-20.5-49.5-20.5t-49.62 20.38q-20.5 20.38-20.5 49.5t20.38 49.62q20.38 20.5 49.5 20.5Zm-270-540q29.12 0 49.62-20.38 20.5-20.38 20.5-49.5t-20.38-49.62q-20.38-20.5-49.5-20.5t-49.62 20.38q-20.5 20.38-20.5 49.5t20.38 49.62q20.38 20.5 49.5 20.5Zm-270 540q29.12 0 49.62-20.38 20.5-20.38 20.5-49.5t-20.38-49.62q-20.38-20.5-49.5-20.5t-49.62 20.38q-20.5 20.38-20.5 49.5t20.38 49.62q20.38 20.5 49.5 20.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">网络</h3>
    </div>
    <div class="card-content">
      <p class="card-description">管理容器之间的网络连接。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/config/containers/logging/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M180-120q-24.75 0-42.37-17.63Q120-155.25 120-180v-600q0-24.75 17.63-42.38Q155.25-840 180-840h375q12.44 0 23.72 5T598-822l224 224q8 8 13 19.28 5 11.28 5 23.72v375q0 24.75-17.62 42.37Q804.75-120 780-120H180Zm129-171h342q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-159h342q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm0-159h216q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H309q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">容器日志</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解如何查看和读取容器日志。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/config/pruning" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M481-415 364-298q11 17 13.5 33t2.5 35q0 64-43 107T230-80q-64 0-107-43T80-230q0-64 43-107t107-43q18 0 35.5 5t36.5 15l116-116-118-118q-17 8-34.5 11t-35.5 3q-64 0-107-43T80-730q0-64 43-107t107-43q64 0 107 43t43 107q0 19-2.5 36T367-662l468 468q23 23 10.5 51.5T801-114q-9 0-17.5-3.5T768-128L481-415Zm118-112-66-66 235-235q7-7 15.5-10.5T801-842q32 0 43.5 29T834-762L599-527ZM230-640q38 0 64-26t26-64q0-38-26-64t-64-26q-38 0-64 26t-26 64q0 38 26 64t64 26Zm253 183q8 0 13.5-5.5T502-476q0-8-5.5-13.5T483-495q-8 0-13.5 5.5T464-476q0 8 5.5 13.5T483-457ZM230-140q38 0 64-26t26-64q0-38-26-64t-64-26q-38 0-64 26t-26 64q0 38 26 64t64 26Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">清理</h3>
    </div>
    <div class="card-content">
      <p class="card-description">清理未使用的资源。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/config/daemon" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M456.82-120q-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-165q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v53h323q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H487v52q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63ZM150-202q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h187q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H150Zm186.82-166q-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-52H150q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h157v-54q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v166q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63ZM457-450q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h353q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H457Zm165.82-165q-12.82 0-21.32-8.63-8.5-8.62-8.5-21.37v-165q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v52h157q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H653v53q0 12.75-8.68 21.37-8.67 8.63-21.5 8.63ZM150-698q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h353q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H150Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">配置守护进程</h3>
    </div>
    <div class="card-content">
      <p class="card-description">深入了解 Docker 守护进程的配置选项。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/engine/security/rootless" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-142q106-35 175.5-128.5T737-480H480v-335l-260 97v196q0 12 .5 20.5T223-480h257v338Zm0 58q-5 0-9.5-1t-9.5-3q-139-47-220-168.5T160-523v-196q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v196q0 145-81 266.5T499-88q-5 2-9.5 3t-9.5 1Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Rootless 模式</h3>
    </div>
    <div class="card-content">
      <p class="card-description">无需 root 权限运行 Docker。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/engine/deprecated/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-160q-24 0-42-18.5T80-220v-520q0-23 18-41.5t42-18.5h256q12.44 0 23.72 5t19.37 13.09L481-740h339q23 0 41.5 18.5T880-680v460q0 23-18.5 41.5T820-160H140Zm410-120h120q20.83 0 35.42-14.58Q720-309.17 720-330v-205h15q10.83 0 17.92-7.12 7.08-7.11 7.08-18 0-10.88-7.08-17.88-7.09-7-17.92-7h-85v-20q0-6-4.5-10.5T635-620h-50q-6 0-10.5 4.5T570-605v20h-85q-10.83 0-17.92 7.12-7.08 7.11-7.08 18 0 10.88 7.08 17.88 7.09 7 17.92 7h15v205q0 20.83 14.58 35.42Q529.17-280 550-280Zm0-255h120v205H550v-205Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">已弃用功能</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解您应停止使用的 Docker Engine 功能。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/engine/release-notes" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24 0-42-18t-18-42v-680q0-24 18-42t42-18h336q12.44 0 23.72 5T599-862l183 183q8 8 13 19.28 5 11.28 5 23.72v496q0 24-18 42t-42 18H220Zm331-584q0 12.75 8.63 21.37Q568.25-634 581-634h159L551-820v156ZM450-363v99q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63 12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-99h100q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H510v-100q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v100H350q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5h100Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">发行说明</h3>
    </div>
    <div class="card-content">
      <p class="card-description">阅读最新版本的发行说明。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 许可

在大型企业（员工超过 250 人或年收入超过 1000 万美元）中通过 Docker Desktop 获得的 Docker Engine 的商业使用，需要[付费订阅](https://www.docker.com/pricing/)。Apache 许可证 2.0 版。完整许可证请参见 [LICENSE](https://github.com/moby/moby/blob/master/LICENSE)。

- [安装 Docker Engine](/engine/install/)

- [存储](/engine/storage/)

- [网络概述](/engine/network/)

- [Docker 守护进程配置概述](/engine/daemon/)

- [查看容器日志](/engine/logging/)

- [Swarm 模式](/engine/swarm/)

- [Docker Engine 安全](/engine/security/)

- [Deprecated Docker Engine features](/engine/deprecated/)

- [Docker Engine managed plugin system](/engine/extend/)

