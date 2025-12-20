# 管理漏洞例外

容器镜像中发现的漏洞有时需要额外的上下文。
仅仅因为镜像包含一个有漏洞的软件包，并不意味着该漏洞可被利用。Docker Scout 中的**例外**允许您确认已接受的风险或解决镜像分析中的误报。

通过否定不适用的漏洞，您可以更轻松地理解漏洞在镜像上下文中的安全影响，并帮助您和镜像的下游消费者更好地理解这些影响。

在 Docker Scout 中，例外会自动纳入分析结果。如果镜像包含将 CVE 标记为不适用的例外，则该 CVE 会从分析结果中排除。

## 创建例外

要为镜像创建例外，您可以：

- 在 [Docker Scout 仪表板](/manuals/scout/how-tos/create-exceptions-gui.md) 或 Docker Desktop 的 GUI 中创建例外。
- 创建 [VEX](/manuals/scout/how-tos/create-exceptions-vex.md) 文档并将其附加到镜像。

推荐的创建例外方式是使用 Docker Scout 仪表板或 Docker Desktop。GUI 提供了用户友好的界面来创建例外。它还允许您为多个镜像或整个组织一次性创建例外。

## 查看例外

要查看镜像的例外，您需要具备适当的权限。

- 使用 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外对您的 Docker 组织成员可见。未认证用户或非您组织成员的用户无法看到这些例外。
- 使用 [VEX 文档](/manuals/scout/how-tos/create-exceptions-vex.md) 创建的例外对任何可以拉取镜像的用户可见，因为 VEX 文档存储在镜像清单或镜像的文件系统中。

### 在 Docker Scout 仪表板或 Docker Desktop 中查看例外

Docker Scout 仪表板中漏洞页面的 **Exceptions** 选项卡列出了您组织中所有镜像的所有例外。在这里，您可以查看每个例外的更多详细信息、被抑制的 CVE、例外适用的镜像、例外类型和创建方式等。

对于使用 [GUI](/manuals/scout/how-tos/create-exceptions-gui.md) 创建的例外，选择操作菜单可以编辑或删除例外。

要查看特定镜像标签的所有例外：








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Scout-Dashboard' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Scout-Dashboard' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Scout-Dashboard'"
        
      >
        Docker Scout Dashboard
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Desktop'"
        
      >
        Docker Desktop
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Scout-Dashboard' && 'hidden'"
      >
        <ol>
<li>转到 <a class="link" href="https://scout.docker.com/reports/images" rel="noopener">Images 页面</a>。</li>
<li>选择您要检查的标签。</li>
<li>打开 <strong>Exceptions</strong> 选项卡。</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <ol>
<li>在 Docker Desktop 中打开 <strong>Images</strong> 视图。</li>
<li>打开 <strong>Hub</strong> 选项卡。</li>
<li>选择您要检查的标签。</li>
<li>打开 <strong>Exceptions</strong> 选项卡。</li>
</ol>

      </div>
    
  </div>
</div>


### 在 CLI 中查看例外





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    
      
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Availability:</span>
        <span>
          Experimental
          
            
          
            
          
            
              <span class="icon-svg"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M172-120q-41.78 0-59.39-39T124-230l248-280v-270h-52q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h320q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5h-52v270l248 280q29 32 11.39 71T788-120H172Z"/></svg></span>
            
          
            
          
            
          
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Scout CLI 
    
  
  <a class="link" href="/scout/release-notes/cli/#1150">1.15.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



当您运行 `docker scout cves <image>` 时，CLI 中会突出显示漏洞例外。如果 CVE 被例外抑制，CVE ID 旁边会显示 `SUPPRESSED` 标签。还会显示有关例外的详细信息。

![CLI 输出中的 SUPPRESSED 标签](/scout/images/suppressed-cve-cli.png)

> [!IMPORTANT]
> 要在 CLI 中查看例外，您必须将 CLI 配置为使用与创建例外相同的 Docker 组织。
>
> 要为 CLI 配置组织，请运行：
>
> ```console
> $ docker scout configure organization <organization>
> ```
>
> 将 `<organization>` 替换为您的 Docker 组织名称。
>
> 您也可以使用 `--org` 标志为每个命令单独设置组织：
>
> ```console
> $ docker scout cves --org <organization> <image>
> ```

要从输出中排除被抑制的 CVE，请使用 `--ignore-suppressed` 标志：

```console
$ docker scout cves --ignore-suppressed <image>
```
