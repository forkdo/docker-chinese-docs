# 参考文档

本节包含 Docker 平台各种 API、CLI、驱动程序、规范和文件格式的参考文档。

## 文件格式


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/reference/dockerfile/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24 0-42-18t-18-42v-680q0-24 18-42t42-18h315q12 0 23.5 5t19.5 13l204 204q8 8 13 19.5t5 23.5v99q0 8-5 14.5t-13 8.5q-12 5-23 11.5T738-465L518-246q-8 8-13 19.5t-5 23.5v93q0 13-8.5 21.5T470-80H220Zm340-30v-81q0-6 2-11t7-10l212-211q9-9 20-13t22-4q12 0 23 4.5t20 13.5l37 37q9 9 13 20t4 22q0 11-4.5 22.5T902-300L692-89q-5 5-10 7t-11 2h-81q-13 0-21.5-8.5T560-110Zm263-194 37-39-37-37-38 38 38 38ZM550-600h190L520-820l220 220-220-220v190q0 13 8.5 21.5T550-600Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Dockerfile</h3>
    </div>
    <div class="card-content">
      <p class="card-description">定义单个容器的内容和启动行为。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/compose-file/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M620-140v-35L310-330H180q-24.75 0-42.37-17.63Q120-365.25 120-390v-100q0-24.75 17.63-42.38Q155.25-550 180-550h115l125-139.5V-820q0-24.75 17.63-42.38Q455.25-880 480-880h100q24.75 0 42.38 17.62Q640-844.75 640-820v100q0 24.75-17.62 42.37Q604.75-660 580-660H474L340-510v129l280 139q1-24 18.5-41t41.5-17h100q24.75 0 42.38 17.62Q840-264.75 840-240v100q0 24.75-17.62 42.37Q804.75-80 780-80H680q-24.75 0-42.37-17.63Q620-115.25 620-140Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Compose 文件</h3>
    </div>
    <div class="card-content">
      <p class="card-description">定义多容器应用程序。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 命令行界面 (CLI)


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/reference/cli/docker/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-160q-24 0-42-18t-18-42v-520q0-24 18-42t42-18h680q24 0 42 18t18 42v520q0 24-18 42t-42 18H140Zm0-60h680v-436H140v436Zm221-218-83-83q-9-9-8.5-21t9.5-21q9-9 21-9t21 9l104 104q9 9 9 21t-9 21L321-313q-9 9-21 9t-21-9q-9-9-9-21t9-21l82-83Zm159 150q-13 0-21.5-8.5T490-318q0-13 8.5-21.5T520-348h160q13 0 21.5 8.5T710-318q0 13-8.5 21.5T680-288H520Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker CLI</h3>
    </div>
    <div class="card-content">
      <p class="card-description">主要的 Docker CLI，包含所有 <code>docker</code> 命令。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/cli/docker/compose/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-160q-24 0-42-18t-18-42v-520q0-24 18-42t42-18h680q24 0 42 18t18 42v520q0 24-18 42t-42 18H140Zm130-190h300q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H270q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm120-120h300q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H390q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5Zm-119.82 0q12.82 0 21.32-8.68 8.5-8.67 8.5-21.5 0-12.82-8.68-21.32-8.67-8.5-21.5-8.5-12.82 0-21.32 8.68-8.5 8.67-8.5 21.5 0 12.82 8.68 21.32 8.67 8.5 21.5 8.5Zm420 120q12.82 0 21.32-8.68 8.5-8.67 8.5-21.5 0-12.82-8.68-21.32-8.67-8.5-21.5-8.5-12.82 0-21.32 8.68-8.5 8.67-8.5 21.5 0 12.82 8.68 21.32 8.67 8.5 21.5 8.5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Compose CLI</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Docker Compose 的 CLI，用于构建和运行多容器应用程序。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/cli/dockerd/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M150-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h600q24 0 42 18t18 42v60.15h30q12.75 0 21.38 8.64 8.62 8.65 8.62 21.43t-8.62 21.28Q852.75-660 840-660h-30v150h30.18q12.82 0 21.32 8.68 8.5 8.67 8.5 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-30v150h30.18q12.82 0 21.32 8.68 8.5 8.67 8.5 21.5 0 12.82-8.62 21.42-8.63 8.59-21.38 8.59h-30V-180q0 24-18 42t-42 18H150Zm90-120h193q12.75 0 21.38-8.63Q463-257.25 463-270v-140q0-12.75-8.62-21.38Q445.75-440 433-440H240q-12.75 0-21.37 8.62Q210-422.75 210-410v140q0 12.75 8.63 21.37Q227.25-240 240-240Zm283-336h137q12.75 0 21.38-8.63Q690-593.25 690-606v-84q0-12.75-8.62-21.38Q672.75-720 660-720H523q-12.75 0-21.37 8.62Q493-702.75 493-690v84q0 12.75 8.63 21.37Q510.25-576 523-576ZM240-470h193q12.75 0 21.38-8.63Q463-487.25 463-500v-190q0-12.75-8.62-21.38Q445.75-720 433-720H240q-12.75 0-21.37 8.62Q210-702.75 210-690v190q0 12.75 8.63 21.37Q227.25-470 240-470Zm283 230h137q12.75 0 21.38-8.63Q690-257.25 690-270v-246q0-12.75-8.62-21.38Q672.75-546 660-546H523q-12.75 0-21.37 8.62Q493-528.75 493-516v246q0 12.75 8.63 21.37Q510.25-240 523-240Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Daemon CLI (dockerd)</h3>
    </div>
    <div class="card-content">
      <p class="card-description">管理容器的持久进程。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 应用程序编程接口 (API)


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/reference/api/engine/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-375 375-480l105-105 105 105-105 105Zm-85-294-83-83 126-126q9-9 20-13t22-4q11 0 22 4t20 13l126 126-83 83-85-85-85 85ZM208-312 82-438q-9-9-13-20t-4-22q0-11 4-22t13-20l126-126 83 83-85 85 85 85-83 83Zm544 0-83-83 85-85-85-85 83-83 126 126q9 9 13 20t4 22q0 11-4 22t-13 20L752-312ZM438-82 312-208l83-83 85 85 85-85 83 83L522-82q-9 9-20 13t-22 4q-11 0-22-4t-20-13Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Engine API</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Docker 的主要 API，提供对守护进程的程序化访问。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/api/hub/latest/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M358-319q30.94 0 52.97-21.74Q433-362.48 433-393t-22.03-52.26Q388.94-467 358-467q-30.11 0-51.56 21.74Q285-423.52 285-393t21.44 52.26Q327.89-319 358-319Zm244 0q30.53 0 52.26-21.74Q676-362.48 676-393t-21.74-52.26Q632.53-467 602-467q-30.53 0-52.26 21.74Q528-423.52 528-393t21.74 52.26Q571.47-319 602-319ZM479.96-533q30.95 0 53-22.04 22.04-22.05 22.04-53Q555-639 532.97-660T480-681q-30.11 0-51.56 21.44Q407-638.11 407-608q0 30.94 21 52.97Q449-533 479.96-533Zm.31 453q-82.74 0-155.5-31.5Q252-143 197.5-197.5t-86-127.34Q80-397.68 80-480.5t31.5-155.66Q143-709 197.5-763t127.34-85.5Q397.68-880 480.5-880t155.66 31.5Q709-817 763-763t85.5 127Q880-563 880-480.27q0 82.74-31.5 155.5Q817-252 763-197.68q-54 54.31-127 86Q563-80 480.27-80Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Hub API</h3>
    </div>
    <div class="card-content">
      <p class="card-description">与 Docker Hub 交互的 API。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/api/dvp/latest/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M840-270 521-520q-20-16-45.5-12.5T435-508L330-363q-8 11-20.5 12.5T287-357L120-491v-129q0-19 16.5-27t31.5 3l112 84 163-228q15-21 40.5-25t45.5 13l151 120h100q25 0 42.5 17.5T840-620v350ZM120-160v-254l155 124q20 16 45.5 12.5T361-302l105-145q8-11 20.5-12.5T509-453l331 259v34H120Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">DVP Data API</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Docker Verified Publishers 用于获取分析数据的 API。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/reference/api/registry/latest/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-520q161 0 260.5-49T840-680q0-63-99.5-111.5T480-840q-161 0-260.5 48.5T120-680q0 62 99.5 111T480-520Zm0 100q50 0 112-8.5T709.5-455q55.5-18 93-46.5T840-570v100q0 40-37.5 68.5t-93 46.5Q654-337 592-328.5T480-320q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-470v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-420Zm0 200q50 0 112-8.5T709.5-255q55.5-18 93-46.5T840-370v100q0 40-37.5 68.5t-93 46.5Q654-137 592-128.5T480-120q-49 0-111.5-8.5t-118-27q-55.5-18.5-93-47T120-270v-100q0 39 37.5 67.5t93 47q55.5 18.5 118 27T480-220Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Registry API</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Docker Registry 的 API。</p>
    </div>
  
    </a>
  
</div>

  
</div>


- [CLI 参考](https://docs.docker.com/reference/cli/)

- [Build checks](https://docs.docker.com/reference/build-checks/)

- [Compose 文件参考](https://docs.docker.com/reference/compose-file/)

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)

- [示例概览](https://docs.docker.com/reference/samples/)

- [术语表](https://docs.docker.com/reference/glossary/)

