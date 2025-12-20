# 增强型容器隔离常见问题解答





  
  
  
  


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
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



此页面解答了关于增强型容器隔离 (ECI) 的常见问题，这些问题未涵盖在主文档中。

## 开启 ECI 后，我需要改变使用 Docker 的方式吗？

不需要。ECI 会在后台自动创建更安全的容器。您可以继续使用所有现有的 Docker 命令、工作流程和开发工具，无需任何更改。

## 所有容器工作负载都能与 ECI 兼容吗？

大多数容器工作负载在开启 ECI 后都能正常运行。但是，一些需要特定内核级访问权限的高级工作负载可能无法工作。有关受影响工作负载的详细信息，请参阅 [ECI 限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。

## 为什么不直接限制 `--privileged` 标志的使用呢？

特权容器有其合法用途，例如 Docker-in-Docker、Kubernetes-in-Docker 以及访问硬件设备。ECI 提供了更好的解决方案，它允许这些高级工作负载安全运行，同时防止它们危及 Docker Desktop 虚拟机。

## ECI 会影响容器性能吗？

ECI 对容器性能的影响微乎其微。唯一的例外是执行大量 `mount` 和 `umount` 系统调用的容器，因为这些调用会受到 Sysbox 运行时的安全检查。大多数开发工作负载不会出现明显的性能差异。

## 开启 ECI 后，我可以覆盖容器运行时吗？

不可以。开启 ECI 后，所有容器都将使用 Sysbox 运行时，无论使用任何 `--runtime` 标志：

```console
$ docker run --runtime=runc alpine echo "test"
# 这仍然使用 sysbox-runc，而不是 runc
```

`--runtime` 标志会被忽略，以防止用户通过在 Docker Desktop 虚拟机中以真正的 root 身份运行容器来绕过 ECI 安全机制。

## ECI 会保护开启之前创建的容器吗？

不会。ECI 仅保护开启后创建的容器。在开启 ECI 之前，请移除现有容器：

```console
$ docker stop $(docker ps -q)
$ docker rm $(docker ps -aq)
```

更多详情，请参阅 [启用增强型容器隔离](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/enable-eci.md)。

## ECI 保护哪些容器？

ECI 的保护范围因容器类型和 Docker Desktop 版本而异：

### 始终受保护

- 使用 `docker run` 和 `docker create` 创建的容器
- 使用 `docker-container` 构建驱动的容器

### 版本依赖

- Docker Build：在 Docker Desktop 4.30+ 版本中受保护（WSL 2 除外）
- Kubernetes：在 Docker Desktop 4.38+ 版本中使用 kind 配置器时受保护

### 不受保护

- Docker 扩展
- Docker Debug 容器
- 使用 Kubeadm 配置器的 Kubernetes

完整详情，请参阅 [ECI 限制](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations.md)。

## 开启 ECI 后，我可以挂载 Docker 套接字吗？

默认情况下，不可以。出于安全考虑，ECI 会阻止 Docker 套接字绑定挂载。但是，您可以为受信任的镜像（如 Testcontainers）配置例外。

配置详情，请参阅 [配置 Docker 套接字例外](/manuals/enterprise/security/hardened-desktop/enhanced-container-isolation/config.md)。

## ECI 限制哪些绑定挂载？

ECI 限制对 Docker Desktop 虚拟机目录的绑定挂载，但允许在 Docker Desktop 设置中配置的主机目录挂载。
