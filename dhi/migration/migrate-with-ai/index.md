# 使用 Docker 的 AI 助手进行迁移





  
  
  
  


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
        <span>Docker Desktop 
    
  
  <a class="link" href="/desktop/release-notes/#4380">4.38.0</a> or later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



您可以使用 Docker 的 AI 助手自动将您的 Dockerfile 迁移至使用 Docker 强化镜像 (DHI)。

1. 确保已[启用](/manuals/ai/gordon.md#enable-ask-gordon) Docker 的 AI 助手。
2. 在终端中，导航至包含您的 Dockerfile 的目录。
3. 与助手开始对话：
   ```bash
   docker ai
   ```
4. 输入：
   ```console
   "Migrate my dockerfile to DHI"
   ```
5. 跟随与助手的对话。助手将编辑您的 Dockerfile，因此当它请求访问文件系统及其他权限时，输入 `yes` 以允许助手继续操作。

迁移完成后，您将看到一条成功消息：

```text
已成功迁移至 Docker 强化镜像 (DHI)。更新后的 Dockerfile 成功构建了镜像，且最终镜像中未检测到任何漏洞。
原始 Dockerfile 的功能和优化已得到保留。
```

> [!IMPORTANT]
>
> 与任何 AI 工具一样，您必须验证助手的编辑并测试您的镜像。
