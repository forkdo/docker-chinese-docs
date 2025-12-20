# Docker Hub 上的不可变标签




  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Beta
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M360-360H217q-18 0-26.5-16t2.5-31l338-488q8-11 20-15t24 1q12 5 19 16t5 24l-39 309h176q19 0 27 17t-4 32L388-66q-8 10-20.5 13T344-55q-11-5-17.5-16T322-95l38-265Z"/></svg></span>
            
          
            
          
            
          
            
          
            
          
        </span>
      </div>
    

    

    
  </div>



不可变标签提供了一种确保特定镜像版本在发布到 Docker Hub 后保持不变的方法。此功能通过防止意外覆盖重要镜像版本，帮助维护容器部署的一致性和可靠性。

## 什么是不可变标签？

不可变标签是指一旦推送到 Docker Hub 后，就无法被覆盖或删除的镜像标签。这确保了镜像的特定版本在其整个生命周期中保持完全相同，从而提供：

- 版本一致性
- 可重现的构建
- 防止意外覆盖
- 更好的安全性和合规性

## 启用不可变标签

要为仓库启用不可变标签：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 选择要为其启用不可变标签的仓库。
4. 转到 **Settings** > **General**。
5. 在 **Tag mutability settings** 下，选择以下选项之一：
   - **All tags are mutable (Default)**：  
     标签可以更改以引用不同的镜像。这允许您在不创建新标签的情况下重新定位标签。
   - **All tags are immutable**：  
     标签创建后无法更新以指向不同的镜像。这确保了 consistency 并防止意外更改。这包括 `latest` 标签。
   - **Specific tags are immutable**：  
     使用正则表达式值定义创建后无法更新的特定标签。
6. 选择 **Save**。

启用后，所有标签都会被锁定到其特定的镜像，确保每个标签始终指向相同的镜像版本且无法修改。

> [!NOTE]
> 此正则表达式实现遵循 [Go regexp package](https://pkg.go.dev/regexp)，它基于 RE2 引擎。有关更多信息，请访问 [RE2 Regular Expression Syntax](https://github.com/google/re2/wiki/Syntax)。

## 使用不可变标签

启用不可变标签后：

- 您无法使用相同的标签名称推送新镜像
- 每个新镜像版本必须使用新的标签名称

要推送镜像，请为更新后的镜像创建一个新标签并将其推送到仓库。
