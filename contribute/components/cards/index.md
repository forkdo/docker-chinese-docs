# 卡片

可以使用 `card` 短代码在页面中添加卡片。  
此短代码的参数如下：

| 参数        | 描述                                                                 |
|-------------|----------------------------------------------------------------------|
| title       | 卡片的标题                                                           |
| icon        | 卡片的图标标识符                                                     |
| image       | 使用自定义图片替代图标（与 icon 互斥）                               |
| link        | （可选）点击卡片时跳转的链接目标                                     |
| description | 描述文本，支持 Markdown 格式                                         |

> [!NOTE]
>
> 卡片中的 Markdown 描述存在一个已知限制：  
> 不能包含指向其他 .md 文档的相对链接，这类链接将无法正确渲染。  
> 请改用目标页面的 URL 绝对路径链接。
>
> 例如，不要写成 `../install/linux.md`，而应写成：  
> `/engine/install/linux/`。

## 示例

<div class="card">
  
    <a href="https://docs.docker.com/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M480-140q-11 0-22-4t-19-12l-53-49Q262-320 171-424.5T80-643q0-90 60.5-150.5T290-854q51 0 101 24.5t89 80.5q44-56 91-80.5t99-24.5q89 0 149.5 60.5T880-643q0 114-91 218.5T574-205l-53 49q-8 8-19 12t-22 4Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">开始使用 Docker</h3>
    </div>
    <div class="card-content">
      <p class="card-description">使用 Docker 构建、共享并运行您的应用</p>
    </div>
  
    </a>
  
</div>



## 标记语法

```go
{{< card
  title="开始使用 Docker"
  icon=favorite
  link=https://docs.docker.com/
  description="使用 Docker 构建、共享并运行您的应用"
>}}
```

### 网格布局

还提供了一个内置的 `grid` 短代码，用于生成卡片网格布局。  
在大屏幕上为 3x3 网格，中等屏幕为 2x2，小屏幕则为单列。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/desktop/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M330-150v-50H140q-24 0-42-18t-18-42v-520q0-24 18-42t42-18h330q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v520h680v-110q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v110q0 24-18 42t-42 18H630v50q0 12.75-8.62 21.37Q612.75-120 600-120H360q-12.75 0-21.37-8.63Q330-137.25 330-150Zm320-378v-282q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v282l93-93q9-9 21-9t21 9q9 9 9 21t-9 21L701-435q-9 9-21 9t-21-9L515-579q-9-9-9-21t9-21q9-9 21-9t21 9l93 93Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Desktop</h3>
    </div>
    <div class="card-content">
      <p class="card-description">桌面上的 Docker。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/engine/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M150-120q-24 0-42-18t-18-42v-600q0-24 18-42t42-18h600q24 0 42 18t18 42v60.15h30q12.75 0 21.38 8.64 8.62 8.65 8.62 21.43t-8.62 21.28Q852.75-660 840-660h-30v150h30.18q12.82 0 21.32 8.68 8.5 8.67 8.5 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-30v150h30.18q12.82 0 21.32 8.68 8.5 8.67 8.5 21.5 0 12.82-8.62 21.42-8.63 8.59-21.38 8.59h-30V-180q0 24-18 42t-42 18H150Zm90-120h193q12.75 0 21.38-8.63Q463-257.25 463-270v-140q0-12.75-8.62-21.38Q445.75-440 433-440H240q-12.75 0-21.37 8.62Q210-422.75 210-410v140q0 12.75 8.63 21.37Q227.25-240 240-240Zm283-336h137q12.75 0 21.38-8.63Q690-593.25 690-606v-84q0-12.75-8.62-21.38Q672.75-720 660-720H523q-12.75 0-21.37 8.62Q493-702.75 493-690v84q0 12.75 8.63 21.37Q510.25-576 523-576ZM240-470h193q12.75 0 21.38-8.63Q463-487.25 463-500v-190q0-12.75-8.62-21.38Q445.75-720 433-720H240q-12.75 0-21.37 8.62Q210-702.75 210-690v190q0 12.75 8.63 21.37Q227.25-470 240-470Zm283 230h137q12.75 0 21.38-8.63Q690-257.25 690-270v-246q0-12.75-8.62-21.38Q672.75-546 660-546H523q-12.75 0-21.37 8.62Q493-528.75 493-516v246q0 12.75 8.63 21.37Q510.25-240 523-240Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Engine</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Vrrrrooooommm</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/build/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M354-370q-97 0-165-67.5T121-602q0-20 3-37.5t11-36.5q3-8 9-12t13-6q7-2 14 0t13 8l113 113 92-86-118-118q-6-6-8-13t0-14q2-7 6-12.5t12-8.5q19-8 36-11.5t37-3.5q99 0 168.5 69.5T592-602q0 24-5 47t-13 46l221 221q27 26 26.5 63.5T793-161q-26 24-61.5 23.5T670-164L447-388q-23 8-46 13t-47 5Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Build</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Clang bang</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/compose/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M604-180v-65h-94q-24.75 0-42.37-17.63Q450-280.25 450-305v-350h-93v70q0 24.75-17.62 42.37Q321.75-525 297-525H140q-24.75 0-42.37-17.63Q80-560.25 80-585v-195q0-24.75 17.63-42.38Q115.25-840 140-840h157q24.75 0 42.38 17.62Q357-804.75 357-780v65h247v-65q0-24.75 17.63-42.38Q639.25-840 664-840h156q24.75 0 42.38 17.62Q880-804.75 880-780v195q0 24.75-17.62 42.37Q844.75-525 820-525H664q-24.75 0-42.37-17.63Q604-560.25 604-585v-70h-94v350h94v-70q0-24.75 17.63-42.38Q639.25-435 664-435h156q24.75 0 42.38 17.62Q880-399.75 880-375v195q0 24.75-17.62 42.37Q844.75-120 820-120H664q-24.75 0-42.37-17.63Q604-155.25 604-180Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Compose</h3>
    </div>
    <div class="card-content">
      <p class="card-description">Figgy!</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/docker-hub/" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M234-40q-48 0-81-33t-33-81q0-48 33-81t81-33q14 0 24.5 2.5T280-258l85-106q-19-23-29-52.5t-5-61.5l-121-41q-15 25-39.5 39T114-466q-48 0-81-33T0-580q0-48 33-81t81-33q48 0 81 33t33 81v4l122 42q18-32 43.5-49t56.5-24v-129q-39-11-61.5-43T366-846q0-48 33-81t81-33q48 0 81 33t33 81q0 35-23 67t-61 43v129q31 7 57 24t44 49l121-42v-4q0-48 33-81t81-33q48 0 81 33t33 81q0 48-33 81t-81 33q-32 0-57-14t-39-39l-121 41q5 32-4.5 61.5T595-364l85 106q11-5 21.5-7.5T726-268q48 0 81 33t33 81q0 48-33 81t-81 33q-48 0-81-33t-33-81q0-20 5.5-36t15.5-31l-85-106q-32 17-68.5 17T411-327l-84 107q10 15 15.5 30.5T348-154q0 48-33 81t-81 33Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">Docker Hub</h3>
    </div>
    <div class="card-content">
      <p class="card-description">内容超多，哇哦</p>
    </div>
  
    </a>
  
</div>

  
</div>


`grid` 是与 `card` 独立的短代码，但底层实现的是同一组件。  
插入网格的标记语法稍显特殊：`grid` 短代码不接受任何参数，  
它的作用仅仅是定义网格在页面中的显示位置。

```go
{{< grid >}}
```

网格的数据在页面的 front matter 中通过 `grid` 键定义，格式如下：

```yaml
# 页面的 front matter 部分
title: 某个页面
grid:
  - title: "Docker Engine"
    description: Vrrrrooooommm
    icon: "developer_board"
    link: "/engine/"
  - title: "Docker Build"
    description: Clang bang
    icon: "build"
    link: "/build/"
```
