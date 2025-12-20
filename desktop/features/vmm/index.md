# Docker Desktop for Mac 的虚拟机管理器

Docker Desktop 支持多种虚拟机管理器 (VMM)，用于运行容器的 Linux 虚拟机。您可以根据系统架构（Intel 或 Apple Silicon）、性能需求和功能要求选择最合适的选项。本页概述了可用的选项。

要更改 VMM，请转到 **设置** > **常规** > **虚拟机管理器**。

## Docker VMM





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Requires:</span>
        <span>Docker Desktop 
    
  
  <a class="link" href="/desktop/release-notes/#4350">4.35.0</a> and later</span>
        <span class="icon-svg">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-240q-24 0-42-18t-18-42v-480q0-24 18-42t42-18h367q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H140v480h680v-109q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v109q0 24-18 42t-42 18H652l39 38q5 5 7 10.54 2 5.55 2 11.46v30q0 12.75-8.62 21.37Q682.75-120 670-120H290q-12.75 0-21.37-8.63Q260-137.25 260-150v-31q0-5.57 2-10.78 2-5.22 7-10.22l38-38H140Zm457-221v-349q0-12.75 8.68-21.38 8.67-8.62 21.5-8.62 12.82 0 21.32 8.62 8.5 8.63 8.5 21.38v349l100-99q9-8 21.1-8.5 12.1-.5 20.9 8.5 9 9 9 21t-9 21L627-346 455-518q-9-9-9-21t9-21q9-9 21-9t21 9l100 99Z"/></svg>
        </span>
      </div>
    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Docker Desktop on Mac with Apple Silicon</span>
        
      </div>
    
  </div>



Docker VMM 是一种新的、针对容器优化的虚拟机管理程序。通过优化 Linux 内核和虚拟机管理程序层，Docker VMM 在常见的开发者任务中提供了显著的性能提升。

Docker VMM 提供的一些关键性能提升包括：
 - 更快的 I/O 操作：在冷缓存情况下，使用 `find` 遍历大型共享文件系统的速度比使用 Apple Virtualization 框架时快 2 倍。
 - 改进的缓存：在热缓存情况下，性能最多可提升 25 倍，甚至超过原生 Mac 操作。

这些改进直接影响那些在容器化开发过程中依赖频繁文件访问和整体系统响应性的开发者。Docker VMM 在速度上实现了显著飞跃，使工作流程更顺畅，迭代周期更快。

> [!NOTE]
>
> Docker VMM 要求至少为 Docker Linux 虚拟机分配 4GB 内存。在启用 Docker VMM 之前，需要增加内存，这可以在 **设置** 的 **资源** 选项卡中完成。

### 已知问题

由于 Docker VMM 仍处于 Beta 阶段，存在一些已知限制：

- Docker VMM 目前不支持 Rosetta，因此 amd64 架构的模拟速度较慢。Docker 正在探索潜在的解决方案。
- 某些数据库（如 MongoDB 和 Cassandra）在使用 Docker VMM 的 virtiofs 时可能会失败。预计此问题将在未来的版本中解决。

## Apple Virtualization 框架

Apple Virtualization 框架是 Mac 上管理虚拟机的稳定且成熟的选项。多年来，它一直是许多 Mac 用户的可靠选择。该框架最适合那些偏好经过验证的解决方案、具有良好性能和广泛兼容性的开发者。

## 适用于 Apple Silicon 的 QEMU（传统）

> [!NOTE]
>
> QEMU 已在 4.44 及更高版本中弃用。有关更多信息，请参阅 [博客公告](https://www.docker.com/blog/docker-desktop-for-mac-qemu-virtualization-option-to-be-deprecated-in-90-days/) 

QEMU 是 Apple Silicon Mac 的传统虚拟化选项，主要用于旧用例。

Docker 建议过渡到更新的替代方案，如 Docker VMM 或 Apple Virtualization 框架，因为它们提供了更优越的性能和持续的支持。特别是 Docker VMM，为使用 Apple Silicon 的开发者提供了显著的速度提升和更高效的开发环境，使其成为一个引人注目的选择。

请注意，这与在 [多平台构建](/manuals/build/building/multi-platform.md#qemu) 中使用 QEMU 模拟非原生架构无关。

## 适用于基于 Intel 的 Mac 的 HyperKit（传统）

> [!NOTE]
>
> HyperKit 将在未来的版本中弃用。

HyperKit 是另一个传统虚拟化选项，专门用于基于 Intel 的 Mac。与 QEMU 一样，它仍然可用，但已被视为弃用。Docker 建议切换到现代替代方案，以获得更好的性能并使您的设置面向未来。
