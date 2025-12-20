# Compose Bridge 概述





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 4.43.0 and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
  </div>



Compose Bridge 将您的 Docker Compose 配置转换为特定于平台的部署格式，例如 Kubernetes 清单。默认情况下，它会生成：

- Kubernetes 清单
- Kustomize 覆盖层 (overlay)

这些输出已准备好部署在启用了 [Kubernetes](/manuals/desktop/settings-and-maintenance/settings.md#kubernetes) 的 Docker Desktop 上。

Compose Bridge 帮助您弥合 Compose 和 Kubernetes 之间的差距，让您在保持 Compose 的简洁性和高效性的同时，更轻松地采用 Kubernetes。

它是一个灵活的工具，您可以利用[默认转换](usage.md)，也可以[创建自定义转换](customize.md)以满足特定的项目需求和要求。

## 工作原理

Compose Bridge 使用转换 (transformation) 将 Compose 模型转换为另一种形式。

转换被打包为一个 Docker 镜像，它接收完全解析后的 Compose 模型作为 `/in/compose.yaml`，并可以在 `/out` 下生成任何目标格式的文件。

Compose Bridge 使用 Go 模板提供了自己的 Kubernetes 转换，因此通过替换或附加您自己的模板，可以轻松地进行扩展和自定义。

有关这些转换如何工作以及如何为您的项目进行自定义的更多详细信息，请参阅[自定义](customize.md)。

Compose Bridge 还支持通过 Docker Model Runner 使用 LLM 的应用程序。

更多详情，请参阅[使用 Model Runner](use-model-runner.md)。

## 下一步是什么？

- [使用 Compose Bridge](usage.md)
- [探索如何自定义 Compose Bridge](customize.md)

- [使用默认的 Compose Bridge 转换](/compose/bridge/usage/)

- [自定义 Compose Bridge](/compose/bridge/customize/)

- [在 Compose Bridge 中使用 Docker Model Runner](/compose/bridge/use-model-runner/)

