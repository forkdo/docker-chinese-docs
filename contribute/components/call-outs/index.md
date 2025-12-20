# 提示框

我们支持以下主要类别的提示框：

- 提示类型：Note（注意）、Tip（提示）、Important（重要）、Warning（警告）、Caution（小心）

我们还支持摘要栏，用于表示某项功能所需的订阅、版本或管理员角色。
添加摘要栏的方法：

将功能名称添加到 `/data/summary.yaml` 文件中。使用以下属性：

| 属性           | 说明                                                   | 可选值                                                      |
|----------------|-------------------------------------------------------|------------------------------------------------------------|
| `subscription` | 注明使用该功能所需的订阅等级                           | All, Personal, Pro, Team, Business                         |
| `availability` | 注明该功能所处的产品开发阶段                           | Experimental, Beta, Early Access, GA, Retired              |
| `requires`     | 注明该功能所需的最低版本                               | 无特定值，使用字符串描述版本并链接到相关发布说明             |
| `for`          | 注明该功能是否面向 IT 管理员                           | Administrators                                             |

然后，在需要添加摘要栏的页面中使用 `summary-bar` 短代码。注意，功能名称区分大小写。摘要栏中显示的图标会自动渲染。

## 示例





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Business</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-180v-600q0-24.75 17.63-42.38Q115.25-840 140-840h270q24.75 0 42.38 17.62Q470-804.75 470-780v105h350q24.75 0 42.38 17.62Q880-639.75 880-615v435q0 24.75-17.62 42.37Q844.75-120 820-120H140q-24.75 0-42.37-17.63Q80-155.25 80-180Zm60 0h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm165 495h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm165 495h350v-435H470v105h80v60h-80v105h80v60h-80v105Zm185-270v-60h60v60h-60Zm0 165v-60h60v60h-60Z"/></svg>
            
          </span>
        
      </div>
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="https://docs.docker.com/desktop/release-notes/#4360">4.36</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



> [!NOTE]
>
> 注意 `get_hit_count` 函数的编写方式。这个基本的重试循环让我们可以在 redis 服务不可用时多次尝试请求。这在应用启动时非常有用，同时也能在 Redis 服务需要重启时增强应用的弹性。在集群环境中，这也有助于处理节点间的短暂连接中断。

> [!TIP]
>
> 为了使用更小的基础镜像，请使用 `alpine`。

> [!IMPORTANT]
>
> 请将访问令牌视为密码并严格保密。请安全地存储您的令牌（例如，存储在凭据管理器中）。

> [!WARNING]
>
> 删除卷
>
> 默认情况下，运行 `docker compose down` 时不会删除 compose 文件中的命名卷。如果您想删除卷，需要添加 `--volumes` 标志。
>
> Docker Desktop Dashboard 在删除应用堆栈时不会删除卷。

> [!CAUTION]
>
> 此处有风险。

对于以下两种提示框，请参考 [Docker 发布生命周期](/release-lifecycle) 了解更多使用场景信息。

## 格式化

```md
{{< summary-bar feature_name="PKG installer" >}}
```

```html
> [!NOTE]
>
> 注意 `get_hit_count` 函数的编写方式。这个基本的重试循环让我们可以在 redis 服务不可用时多次尝试请求。这在应用启动时非常有用，同时也能在 Redis 服务需要重启时增强应用的弹性。在集群环境中，这也有助于处理节点间的短暂连接中断。

> [!TIP]
>
> 为了使用更小的基础镜像，请使用 `alpine`。

> [!IMPORTANT]
>
> 请将访问令牌视为密码并严格保密。请安全地存储您的令牌（例如，存储在凭据管理器中）。

> [!WARNING]
>
> 删除卷
>
> 默认情况下，运行 `docker compose down` 时不会删除 compose 文件中的命名卷。如果您想删除卷，需要添加 `--volumes` 标志。
>
> Docker Desktop Dashboard 在删除应用堆栈时不会删除卷。

> [!CAUTION]
>
> 此处有风险。
```
