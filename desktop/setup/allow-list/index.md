# Docker Desktop 允许列表





  
  
  
  


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



此页面包含您需要添加到防火墙允许列表中的域名 URL，以确保 Docker Desktop 在您的组织内正常工作。

## 需要允许的域名 URL

| 域名                                                                              | 描述                                  |
| ------------------------------------------------------------------------------------ | -------------------------------------------- |
| https://api.segment.io                                                               | 分析                                    |
| https://cdn.segment.com                                                              | 分析                                    |
| https://notify.bugsnag.com                                                           | 错误报告                                |
| https://sessions.bugsnag.com                                                         | 错误报告                                |
| https://auth.docker.io                                                               | 认证                               |
| https://cdn.auth0.com                                                                | 认证                               |
| https://login.docker.com                                                             | 认证                               |
| https://auth.docker.com                                                              | 认证                               |
| https://desktop.docker.com                                                           | 更新                                       |
| https://hub.docker.com                                                               | Docker Hub                                   |
| https://registry-1.docker.io                                                         | Docker 拉取/推送                             |
| https://production.cloudflare.docker.com                                             | Docker 拉取/推送（付费计划）                |
| https://docker-images-prod.6aa30f8b08e16409b46e0173d6de2f56.r2.cloudflarestorage.com | Docker 拉取/推送（个人计划/匿名） |
| https://docker-pinata-support.s3.amazonaws.com                                       | 故障排除                              |
| https://api.dso.docker.com                                                           | Docker Scout 服务                         |
| https://api.docker.com                                                               | 新 API                                      |
