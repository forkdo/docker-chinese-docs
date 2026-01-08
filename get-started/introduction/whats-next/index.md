# 下一步

以下部分提供了分步指南，帮助你理解核心 Docker 概念、构建镜像以及运行容器。

## 基础知识

开始学习容器、镜像、镜像仓库和 Docker Compose 的核心概念。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/the-basics/what-is-a-container/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">什么是容器？</h3>
    </div>
    <div class="card-content">
      <p class="card-description">学习如何运行你的第一个容器。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/the-basics/what-is-an-image/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">什么是镜像？</h3>
    </div>
    <div class="card-content">
      <p class="card-description">学习镜像层的基础知识。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/the-basics/what-is-a-registry/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">什么是镜像仓库？</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解容器镜像仓库，探索其互操作性，并与镜像仓库进行交互。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/the-basics/what-is-docker-compose/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">什么是 Docker Compose？</h3>
    </div>
    <div class="card-content">
      <p class="card-description">更好地理解 Docker Compose。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 构建镜像

使用 Dockerfile、构建缓存和多阶段构建来制作优化的容器镜像。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/building-images/understanding-image-layers/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">理解镜像层</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解容器镜像的层。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/building-images/writing-a-dockerfile/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">编写 Dockerfile</h3>
    </div>
    <div class="card-content">
      <p class="card-description">学习如何使用 Dockerfile 创建镜像。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">构建、标记和发布镜像</h3>
    </div>
    <div class="card-content">
      <p class="card-description">学习如何构建、标记镜像，并将其发布到 Docker Hub 或任何其他镜像仓库。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/building-images/using-the-build-cache/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">使用构建缓存</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解构建缓存，哪些更改会使缓存失效，以及如何有效使用构建缓存。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/building-images/multi-stage-builds/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">多阶段构建</h3>
    </div>
    <div class="card-content">
      <p class="card-description">更好地理解多阶段构建及其优势。</p>
    </div>
  
    </a>
  
</div>

  
</div>


## 运行容器

掌握暴露端口、覆盖默认值、持久化数据、共享文件以及管理多容器应用的基本技巧。


<div
  class="not-prose md:grid-cols-2 xl:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/running-containers/publishing-ports/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">发布端口</h3>
    </div>
    <div class="card-content">
      <p class="card-description">理解在 Docker 中发布和暴露端口的重要性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/running-containers/overriding-container-defaults/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">覆盖容器默认值</h3>
    </div>
    <div class="card-content">
      <p class="card-description">学习如何使用 <code>docker run</code> 命令覆盖容器默认值。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/running-containers/persisting-container-data/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">持久化容器数据</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解 Docker 中数据持久化的重要性。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/running-containers/sharing-local-files/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">与容器共享本地文件</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索 Docker 中可用的各种存储选项及其常见用法。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/get-started/docker-concepts/running-containers/multi-container-applications/" class="card-link">
  
    <div class="card-header">
      
      
      <h3 class="card-title">多容器应用</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解多容器应用的重要性以及它们与单容器应用的区别。</p>
    </div>
  
    </a>
  
</div>

  
</div>

