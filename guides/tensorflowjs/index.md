# 使用 TensorFlow.js 进行人脸检测

本指南介绍如何将 TensorFlow.js 与 Docker 无缝集成以执行人脸检测。在本指南中，您将了解如何：

- 使用 Docker 运行容器化的 TensorFlow.js 应用程序。
- 在 Web 应用程序中使用 TensorFlow.js 实现人脸检测。
- 为 TensorFlow.js Web 应用程序构建 Dockerfile。
- 使用 Docker Compose 进行实时应用程序开发和更新。
- 在 Docker Hub 上共享您的 Docker 镜像，以促进部署并扩大影响范围。

> **致谢**
>
> Docker 感谢 [Harsh Manvar](https://github.com/harsh4870) 对本指南的贡献。

## 先决条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。
- 您已安装 [Git 客户端](https://git-scm.com/downloads)。本指南中的示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 什么是 TensorFlow.js？

[TensorFlow.js](https://www.tensorflow.org/js) 是一个开源 JavaScript 机器学习库，使您能够在浏览器或 Node.js 中训练和部署 ML 模型。它支持从头开始创建新模型或使用预训练模型，从而直接在 Web 环境中实现广泛的 ML 应用程序。TensorFlow.js 提供高效的计算，使 Web 开发人员无需具备深厚的 ML 专业知识即可轻松完成复杂的 ML 任务。

## 为什么将 TensorFlow.js 与 Docker 结合使用？

- 环境一致性和简化部署：Docker 将 TensorFlow.js 应用程序及其依赖项打包到容器中，确保在所有环境中一致运行并简化部署。
- 高效开发和轻松扩展：Docker 通过热重载等功能提高开发效率，并便于使用 Kubernetes 等编排工具轻松扩展 TensorFlow.js 应用程序。
- 隔离性和增强安全性：Docker 在安全环境中隔离 TensorFlow.js 应用程序，最大限度地减少冲突和安全漏洞，同时以有限权限运行应用程序。

## 获取并运行示例应用程序

在终端中，使用以下命令克隆示例应用程序。

```console
$ git clone https://github.com/harsh4870/TensorJS-Face-Detection
```

克隆应用程序后，您会注意到该应用程序包含一个 `Dockerfile`。此 Dockerfile 使您只需 Docker 即可在本地构建和运行该应用程序。

在以容器形式运行应用程序之前，您必须将其构建为镜像。在 `TensorJS-Face-Detection` 目录中运行以下命令，构建名为 `face-detection-tensorjs` 的镜像。

```console
$ docker build -t face-detection-tensorjs .
```

该命令将应用程序构建为镜像。根据您的网络连接，首次运行该命令时可能需要几分钟时间下载必要的组件。

要将镜像作为容器运行，请在终端中运行以下命令。

```console
$ docker run -p 80:80 face-detection-tensorjs
```

该命令运行容器，并将容器中的端口 80 映射到系统上的端口 80。

应用程序运行后，打开 Web 浏览器并访问 [http://localhost:80](http://localhost:80) 以使用应用程序。您可能需要授予应用程序访问网络摄像头的权限。

在 Web 应用程序中，您可以更改后端以使用以下选项之一：

- WASM
- WebGL
- CPU

要停止应用程序，请在终端中按 `ctrl`+`c`。

## 关于应用程序

示例应用程序使用 [MediaPipe](https://developers.google.com/mediapipe/)（一个用于构建多模态机器学习管道的综合性框架）执行实时人脸检测。它专门使用 BlazeFace 模型（一种用于检测图像中人脸的轻量级模型）。

在 TensorFlow.js 或类似的基于 Web 的机器学习框架中，可以使用 WASM、WebGL 和 CPU 后端来执行操作。这些后端各自利用现代浏览器中可用的不同资源和技术，各有其优缺点。以下部分简要介绍了不同后端的特点。

### WASM

WebAssembly (WASM) 是一种低级、类似汇编的语言，具有紧凑的二进制格式，可在 Web 浏览器中以接近原生的速度运行。它允许将使用 C/C++ 等语言编写的代码编译为可在浏览器中执行的二进制文件。

当需要高性能且 WebGL 后端不受支持，或者您希望在不依赖 GPU 的情况下在所有设备上保持一致性能时，WASM 是一个不错的选择。

### WebGL

WebGL 是一种浏览器 API，允许在网页画布中利用 GPU 加速物理和图像处理及效果。

WebGL 非常适合可并行化且能显著受益于 GPU 加速的操作，例如深度学习模型中常见的矩阵乘法和卷积。

### CPU

CPU 后端使用纯 JavaScript 执行，利用设备的中央处理单元 (CPU)。此后端具有最广泛的兼容性，当 WebGL 或 WASM 后端不可用或不适用时，它可作为备用选项。

## 探索应用程序代码

在以下部分中，探索每个文件的用途及其内容。

### index.html 文件

`index.html` 文件用作 Web 应用程序的前端，该应用程序利用 TensorFlow.js 从网络摄像头视频源进行实时人脸检测。它集成了多种技术和库，以便直接在浏览器中实现机器学习。它使用多个 TensorFlow.js 库，包括：

- tfjs-core 和 tfjs-converter，用于核心 TensorFlow.js 功能和模型转换。
- tfjs-backend-webgl、tfjs-backend-cpu 和 tf-backend-wasm 脚本，用于 TensorFlow.js 可用于处理的不同计算后端选项。这些后端允许应用程序通过利用用户的硬件功能来高效执行机器学习任务。
- BlazeFace 库，一种用于人脸检测的 TensorFlow 模型。

它还使用以下附加库：

- dat.GUI，用于创建图形界面以实时与应用程序的设置（例如切换 TensorFlow.js 后端）进行交互。
- Stats.min.js，用于显示性能指标（如 FPS）以监控应用程序运行期间的效率。






<div
  id="indexhtml"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
      index.html
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'PHN0eWxlPgogIGJvZHkgewogICAgbWFyZ2luOiAyNXB4OwogIH0KCiAgLnRydWUgewogICAgY29sb3I6IGdyZWVuOwogIH0KCiAgLmZhbHNlIHsKICAgIGNvbG9yOiByZWQ7CiAgfQoKICAjbWFpbiB7CiAgICBwb3NpdGlvbjogcmVsYXRpdmU7CiAgICBtYXJnaW46IDUwcHggMDsKICB9CgogIGNhbnZhcyB7CiAgICBwb3NpdGlvbjogYWJzb2x1dGU7CiAgICB0b3A6IDA7CiAgICBsZWZ0OiAwOwogIH0KCiAgI2Rlc2NyaXB0aW9uIHsKICAgIG1hcmdpbi10b3A6IDIwcHg7CiAgICB3aWR0aDogNjAwcHg7CiAgfQoKICAjZGVzY3JpcHRpb24tdGl0bGUgewogICAgZm9udC13ZWlnaHQ6IGJvbGQ7CiAgICBmb250LXNpemU6IDE4cHg7CiAgfQo8L3N0eWxlPgoKPGJvZHk&#43;CiAgPGRpdiBpZD0ibWFpbiI&#43;CiAgICA8dmlkZW8KICAgICAgaWQ9InZpZGVvIgogICAgICBwbGF5c2lubGluZQogICAgICBzdHlsZT0iCiAgICAgIC13ZWJraXQtdHJhbnNmb3JtOiBzY2FsZVgoLTEpOwogICAgICB0cmFuc2Zvcm06IHNjYWxlWCgtMSk7CiAgICAgIHdpZHRoOiBhdXRvOwogICAgICBoZWlnaHQ6IGF1dG87CiAgICAgICIKICAgID48L3ZpZGVvPgogICAgPGNhbnZhcyBpZD0ib3V0cHV0Ij48L2NhbnZhcz4KICAgIDx2aWRlbwogICAgICBpZD0idmlkZW8iCiAgICAgIHBsYXlzaW5saW5lCiAgICAgIHN0eWxlPSIKICAgICAgLXdlYmtpdC10cmFuc2Zvcm06IHNjYWxlWCgtMSk7CiAgICAgIHRyYW5zZm9ybTogc2NhbGVYKC0xKTsKICAgICAgdmlzaWJpbGl0eTogaGlkZGVuOwogICAgICB3aWR0aDogYXV0bzsKICAgICAgaGVpZ2h0OiBhdXRvOwogICAgICAiCiAgICA&#43;PC92aWRlbz4KICA8L2Rpdj4KPC9ib2R5Pgo8c2NyaXB0IHNyYz0iaHR0cHM6Ly91bnBrZy5jb20vQHRlbnNvcmZsb3cvdGZqcy1jb3JlQDIuMS4wL2Rpc3QvdGYtY29yZS5qcyI&#43;PC9zY3JpcHQ&#43;CjxzY3JpcHQgc3JjPSJodHRwczovL3VucGtnLmNvbS9AdGVuc29yZmxvdy90ZmpzLWNvbnZlcnRlckAyLjEuMC9kaXN0L3RmLWNvbnZlcnRlci5qcyI&#43;PC9zY3JpcHQ&#43;Cgo8c2NyaXB0IHNyYz0iaHR0cHM6Ly91bnBrZy5jb20vQHRlbnNvcmZsb3cvdGZqcy1iYWNrZW5kLXdlYmdsQDIuMS4wL2Rpc3QvdGYtYmFja2VuZC13ZWJnbC5qcyI&#43;PC9zY3JpcHQ&#43;CjxzY3JpcHQgc3JjPSJodHRwczovL3VucGtnLmNvbS9AdGVuc29yZmxvdy90ZmpzLWJhY2tlbmQtY3B1QDIuMS4wL2Rpc3QvdGYtYmFja2VuZC1jcHUuanMiPjwvc2NyaXB0Pgo8c2NyaXB0IHNyYz0iLi90Zi1iYWNrZW5kLXdhc20uanMiPjwvc2NyaXB0PgoKPHNjcmlwdCBzcmM9Imh0dHBzOi8vdW5wa2cuY29tL0B0ZW5zb3JmbG93LW1vZGVscy9ibGF6ZWZhY2VAMC4wLjUvZGlzdC9ibGF6ZWZhY2UuanMiPjwvc2NyaXB0Pgo8c2NyaXB0IHNyYz0iaHR0cHM6Ly9jZG5qcy5jbG91ZGZsYXJlLmNvbS9hamF4L2xpYnMvZGF0LWd1aS8wLjcuNi9kYXQuZ3VpLm1pbi5qcyI&#43;PC9zY3JpcHQ&#43;CjxzY3JpcHQgc3JjPSJodHRwczovL2NkbmpzLmNsb3VkZmxhcmUuY29tL2FqYXgvbGlicy9zdGF0cy5qcy9yMTYvU3RhdHMubWluLmpzIj48L3NjcmlwdD4KPHNjcmlwdCBzcmM9Ii4vaW5kZXguanMiPjwvc2NyaXB0Pg==', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-html" data-lang="html"><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">style</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">  <span class="nt">body</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">margin</span><span class="p">:</span> <span class="mi">25</span><span class="kt">px</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="p">.</span><span class="nc">true</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">color</span><span class="p">:</span> <span class="kc">green</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="p">.</span><span class="nc">false</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">color</span><span class="p">:</span> <span class="kc">red</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="p">#</span><span class="nn">main</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">position</span><span class="p">:</span> <span class="kc">relative</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="k">margin</span><span class="p">:</span> <span class="mi">50</span><span class="kt">px</span> <span class="mi">0</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nt">canvas</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">position</span><span class="p">:</span> <span class="kc">absolute</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="k">top</span><span class="p">:</span> <span class="mi">0</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="k">left</span><span class="p">:</span> <span class="mi">0</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="p">#</span><span class="nn">description</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">margin-top</span><span class="p">:</span> <span class="mi">20</span><span class="kt">px</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="k">width</span><span class="p">:</span> <span class="mi">600</span><span class="kt">px</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="p">#</span><span class="nn">description-title</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="k">font-weight</span><span class="p">:</span> <span class="kc">bold</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="k">font-size</span><span class="p">:</span> <span class="mi">18</span><span class="kt">px</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;/</span><span class="nt">style</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">body</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">  <span class="p">&lt;</span><span class="nt">div</span> <span class="na">id</span><span class="o">=</span><span class="s">&#34;main&#34;</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;</span><span class="nt">video</span>
</span></span><span class="line"><span class="cl">      <span class="na">id</span><span class="o">=</span><span class="s">&#34;video&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="na">playsinline</span>
</span></span><span class="line"><span class="cl">      <span class="na">style</span><span class="o">=</span><span class="s">&#34;
</span></span></span><span class="line"><span class="cl"><span class="s">      -webkit-transform: scaleX(-1);
</span></span></span><span class="line"><span class="cl"><span class="s">      transform: scaleX(-1);
</span></span></span><span class="line"><span class="cl"><span class="s">      width: auto;
</span></span></span><span class="line"><span class="cl"><span class="s">      height: auto;
</span></span></span><span class="line"><span class="cl"><span class="s">      &#34;</span>
</span></span><span class="line"><span class="cl">    <span class="p">&gt;&lt;/</span><span class="nt">video</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;</span><span class="nt">canvas</span> <span class="na">id</span><span class="o">=</span><span class="s">&#34;output&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">canvas</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">    <span class="p">&lt;</span><span class="nt">video</span>
</span></span><span class="line"><span class="cl">      <span class="na">id</span><span class="o">=</span><span class="s">&#34;video&#34;</span>
</span></span><span class="line"><span class="cl">      <span class="na">playsinline</span>
</span></span><span class="line"><span class="cl">      <span class="na">style</span><span class="o">=</span><span class="s">&#34;
</span></span></span><span class="line"><span class="cl"><span class="s">      -webkit-transform: scaleX(-1);
</span></span></span><span class="line"><span class="cl"><span class="s">      transform: scaleX(-1);
</span></span></span><span class="line"><span class="cl"><span class="s">      visibility: hidden;
</span></span></span><span class="line"><span class="cl"><span class="s">      width: auto;
</span></span></span><span class="line"><span class="cl"><span class="s">      height: auto;
</span></span></span><span class="line"><span class="cl"><span class="s">      &#34;</span>
</span></span><span class="line"><span class="cl">    <span class="p">&gt;&lt;/</span><span class="nt">video</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">  <span class="p">&lt;/</span><span class="nt">div</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;/</span><span class="nt">body</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;https://unpkg.com/@tensorflow/tfjs-core@2.1.0/dist/tf-core.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;https://unpkg.com/@tensorflow/tfjs-converter@2.1.0/dist/tf-converter.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;https://unpkg.com/@tensorflow/tfjs-backend-webgl@2.1.0/dist/tf-backend-webgl.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;https://unpkg.com/@tensorflow/tfjs-backend-cpu@2.1.0/dist/tf-backend-cpu.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;./tf-backend-wasm.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;https://unpkg.com/@tensorflow-models/blazeface@0.0.5/dist/blazeface.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.7.6/dat.gui.min.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;https://cdnjs.cloudflare.com/ajax/libs/stats.js/r16/Stats.min.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span>
</span></span><span class="line"><span class="cl"><span class="p">&lt;</span><span class="nt">script</span> <span class="na">src</span><span class="o">=</span><span class="s">&#34;./index.js&#34;</span><span class="p">&gt;&lt;/</span><span class="nt">script</span><span class="p">&gt;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

  </div>
</div>



### index.js 文件

`index.js` 文件执行人脸检测逻辑。它演示了 Web 开发和机器学习集成中的几个高级概念。以下是其一些关键组件和功能：

- Stats.js：脚本首先创建一个 Stats 实例，以实时监控和显示应用程序的帧速率 (FPS)。这有助于性能分析，尤其是在测试不同 TensorFlow.js 后端对应用程序速度的影响时。
- TensorFlow.js：该应用程序允许用户通过 dat.GUI 提供的图形界面在 TensorFlow.js 的不同计算后端（wasm、webgl 和 cpu）之间切换。更改后端可能会影响性能和兼容性，具体取决于设备和浏览器。addFlagLabels 函数动态检查并显示是否支持 SIMD（单指令多数据）和多线程，这与 wasm 后端的性能优化相关。
- setupCamera 函数：使用 MediaDevices Web API 初始化用户的网络摄像头。它配置视频流不包含音频并使用前置摄像头 (facingMode: 'user')。一旦视频元数据加载完毕，它就会解析带有视频元素的 promise，然后用于人脸检测。
- BlazeFace：此应用程序的核心是 renderPrediction 函数，该函数使用 BlazeFace 模型执行实时人脸检测，这是一种用于检测图像中人脸的轻量级模型。该函数在每个动画帧上调用 model.estimateFaces 以从视频源检测人脸。对于每个检测到的人脸，它会在视频上叠加的画布上绘制一个红色矩形框和蓝色的人脸特征点。






<div
  id="indexjs"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
      index.js
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'Y29uc3Qgc3RhdHMgPSBuZXcgU3RhdHMoKTsKc3RhdHMuc2hvd1BhbmVsKDApOwpkb2N1bWVudC5ib2R5LnByZXBlbmQoc3RhdHMuZG9tRWxlbWVudCk7CgpsZXQgbW9kZWwsIGN0eCwgdmlkZW9XaWR0aCwgdmlkZW9IZWlnaHQsIHZpZGVvLCBjYW52YXM7Cgpjb25zdCBzdGF0ZSA9IHsKICBiYWNrZW5kOiAid2FzbSIsCn07Cgpjb25zdCBndWkgPSBuZXcgZGF0LkdVSSgpOwpndWkKICAuYWRkKHN0YXRlLCAiYmFja2VuZCIsIFsid2FzbSIsICJ3ZWJnbCIsICJjcHUiXSkKICAub25DaGFuZ2UoYXN5bmMgKGJhY2tlbmQpID0&#43;IHsKICAgIGF3YWl0IHRmLnNldEJhY2tlbmQoYmFja2VuZCk7CiAgICBhZGRGbGFnTGFibGVzKCk7CiAgfSk7Cgphc3luYyBmdW5jdGlvbiBhZGRGbGFnTGFibGVzKCkgewogIGlmICghZG9jdW1lbnQucXVlcnlTZWxlY3RvcigiI3NpbWRfc3VwcG9ydGVkIikpIHsKICAgIGNvbnN0IHNpbWRTdXBwb3J0TGFiZWwgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCJkaXYiKTsKICAgIHNpbWRTdXBwb3J0TGFiZWwuaWQgPSAic2ltZF9zdXBwb3J0ZWQiOwogICAgc2ltZFN1cHBvcnRMYWJlbC5zdHlsZSA9ICJmb250LXdlaWdodDogYm9sZCI7CiAgICBjb25zdCBzaW1kU3VwcG9ydGVkID0gYXdhaXQgdGYuZW52KCkuZ2V0QXN5bmMoIldBU01fSEFTX1NJTURfU1VQUE9SVCIpOwogICAgc2ltZFN1cHBvcnRMYWJlbC5pbm5lckhUTUwgPSBgU0lNRCBzdXBwb3J0ZWQ6IDxzcGFuIGNsYXNzPSR7c2ltZFN1cHBvcnRlZH0&#43;JHtzaW1kU3VwcG9ydGVkfTxzcGFuPmA7CiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCIjZGVzY3JpcHRpb24iKS5hcHBlbmRDaGlsZChzaW1kU3VwcG9ydExhYmVsKTsKICB9CgogIGlmICghZG9jdW1lbnQucXVlcnlTZWxlY3RvcigiI3RocmVhZHNfc3VwcG9ydGVkIikpIHsKICAgIGNvbnN0IHRocmVhZFN1cHBvcnRMYWJlbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoImRpdiIpOwogICAgdGhyZWFkU3VwcG9ydExhYmVsLmlkID0gInRocmVhZHNfc3VwcG9ydGVkIjsKICAgIHRocmVhZFN1cHBvcnRMYWJlbC5zdHlsZSA9ICJmb250LXdlaWdodDogYm9sZCI7CiAgICBjb25zdCB0aHJlYWRzU3VwcG9ydGVkID0gYXdhaXQgdGYKICAgICAgLmVudigpCiAgICAgIC5nZXRBc3luYygiV0FTTV9IQVNfTVVMVElUSFJFQURfU1VQUE9SVCIpOwogICAgdGhyZWFkU3VwcG9ydExhYmVsLmlubmVySFRNTCA9IGBUaHJlYWRzIHN1cHBvcnRlZDogPHNwYW4gY2xhc3M9JHt0aHJlYWRzU3VwcG9ydGVkfT4ke3RocmVhZHNTdXBwb3J0ZWR9PC9zcGFuPmA7CiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCIjZGVzY3JpcHRpb24iKS5hcHBlbmRDaGlsZCh0aHJlYWRTdXBwb3J0TGFiZWwpOwogIH0KfQoKYXN5bmMgZnVuY3Rpb24gc2V0dXBDYW1lcmEoKSB7CiAgdmlkZW8gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgidmlkZW8iKTsKCiAgY29uc3Qgc3RyZWFtID0gYXdhaXQgbmF2aWdhdG9yLm1lZGlhRGV2aWNlcy5nZXRVc2VyTWVkaWEoewogICAgYXVkaW86IGZhbHNlLAogICAgdmlkZW86IHsgZmFjaW5nTW9kZTogInVzZXIiIH0sCiAgfSk7CiAgdmlkZW8uc3JjT2JqZWN0ID0gc3RyZWFtOwoKICByZXR1cm4gbmV3IFByb21pc2UoKHJlc29sdmUpID0&#43;IHsKICAgIHZpZGVvLm9ubG9hZGVkbWV0YWRhdGEgPSAoKSA9PiB7CiAgICAgIHJlc29sdmUodmlkZW8pOwogICAgfTsKICB9KTsKfQoKY29uc3QgcmVuZGVyUHJlZGljdGlvbiA9IGFzeW5jICgpID0&#43;IHsKICBzdGF0cy5iZWdpbigpOwoKICBjb25zdCByZXR1cm5UZW5zb3JzID0gZmFsc2U7CiAgY29uc3QgZmxpcEhvcml6b250YWwgPSB0cnVlOwogIGNvbnN0IGFubm90YXRlQm94ZXMgPSB0cnVlOwogIGNvbnN0IHByZWRpY3Rpb25zID0gYXdhaXQgbW9kZWwuZXN0aW1hdGVGYWNlcygKICAgIHZpZGVvLAogICAgcmV0dXJuVGVuc29ycywKICAgIGZsaXBIb3Jpem9udGFsLAogICAgYW5ub3RhdGVCb3hlcywKICApOwoKICBpZiAocHJlZGljdGlvbnMubGVuZ3RoID4gMCkgewogICAgY3R4LmNsZWFyUmVjdCgwLCAwLCBjYW52YXMud2lkdGgsIGNhbnZhcy5oZWlnaHQpOwoKICAgIGZvciAobGV0IGkgPSAwOyBpIDwgcHJlZGljdGlvbnMubGVuZ3RoOyBpKyspIHsKICAgICAgaWYgKHJldHVyblRlbnNvcnMpIHsKICAgICAgICBwcmVkaWN0aW9uc1tpXS50b3BMZWZ0ID0gcHJlZGljdGlvbnNbaV0udG9wTGVmdC5hcnJheVN5bmMoKTsKICAgICAgICBwcmVkaWN0aW9uc1tpXS5ib3R0b21SaWdodCA9IHByZWRpY3Rpb25zW2ldLmJvdHRvbVJpZ2h0LmFycmF5U3luYygpOwogICAgICAgIGlmIChhbm5vdGF0ZUJveGVzKSB7CiAgICAgICAgICBwcmVkaWN0aW9uc1tpXS5sYW5kbWFya3MgPSBwcmVkaWN0aW9uc1tpXS5sYW5kbWFya3MuYXJyYXlTeW5jKCk7CiAgICAgICAgfQogICAgICB9CgogICAgICBjb25zdCBzdGFydCA9IHByZWRpY3Rpb25zW2ldLnRvcExlZnQ7CiAgICAgIGNvbnN0IGVuZCA9IHByZWRpY3Rpb25zW2ldLmJvdHRvbVJpZ2h0OwogICAgICBjb25zdCBzaXplID0gW2VuZFswXSAtIHN0YXJ0WzBdLCBlbmRbMV0gLSBzdGFydFsxXV07CiAgICAgIGN0eC5maWxsU3R5bGUgPSAicmdiYSgyNTUsIDAsIDAsIDAuNSkiOwogICAgICBjdHguZmlsbFJlY3Qoc3RhcnRbMF0sIHN0YXJ0WzFdLCBzaXplWzBdLCBzaXplWzFdKTsKCiAgICAgIGlmIChhbm5vdGF0ZUJveGVzKSB7CiAgICAgICAgY29uc3QgbGFuZG1hcmtzID0gcHJlZGljdGlvbnNbaV0ubGFuZG1hcmtzOwoKICAgICAgICBjdHguZmlsbFN0eWxlID0gImJsdWUiOwogICAgICAgIGZvciAobGV0IGogPSAwOyBqIDwgbGFuZG1hcmtzLmxlbmd0aDsgaisrKSB7CiAgICAgICAgICBjb25zdCB4ID0gbGFuZG1hcmtzW2pdWzBdOwogICAgICAgICAgY29uc3QgeSA9IGxhbmRtYXJrc1tqXVsxXTsKICAgICAgICAgIGN0eC5maWxsUmVjdCh4LCB5LCA1LCA1KTsKICAgICAgICB9CiAgICAgIH0KICAgIH0KICB9CgogIHN0YXRzLmVuZCgpOwoKICByZXF1ZXN0QW5pbWF0aW9uRnJhbWUocmVuZGVyUHJlZGljdGlvbik7Cn07Cgpjb25zdCBzZXR1cFBhZ2UgPSBhc3luYyAoKSA9PiB7CiAgYXdhaXQgdGYuc2V0QmFja2VuZChzdGF0ZS5iYWNrZW5kKTsKICBhZGRGbGFnTGFibGVzKCk7CiAgYXdhaXQgc2V0dXBDYW1lcmEoKTsKICB2aWRlby5wbGF5KCk7CgogIHZpZGVvV2lkdGggPSB2aWRlby52aWRlb1dpZHRoOwogIHZpZGVvSGVpZ2h0ID0gdmlkZW8udmlkZW9IZWlnaHQ7CiAgdmlkZW8ud2lkdGggPSB2aWRlb1dpZHRoOwogIHZpZGVvLmhlaWdodCA9IHZpZGVvSGVpZ2h0OwoKICBjYW52YXMgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgib3V0cHV0Iik7CiAgY2FudmFzLndpZHRoID0gdmlkZW9XaWR0aDsKICBjYW52YXMuaGVpZ2h0ID0gdmlkZW9IZWlnaHQ7CiAgY3R4ID0gY2FudmFzLmdldENvbnRleHQoIjJkIik7CiAgY3R4LmZpbGxTdHlsZSA9ICJyZ2JhKDI1NSwgMCwgMCwgMC41KSI7CgogIG1vZGVsID0gYXdhaXQgYmxhemVmYWNlLmxvYWQoKTsKCiAgcmVuZGVyUHJlZGljdGlvbigpOwp9OwoKc2V0dXBQYWdlKCk7', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-javascript" data-lang="javascript"><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">stats</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">Stats</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="nx">stats</span><span class="p">.</span><span class="nx">showPanel</span><span class="p">(</span><span class="mi">0</span><span class="p">);</span>
</span></span><span class="line"><span class="cl"><span class="nb">document</span><span class="p">.</span><span class="nx">body</span><span class="p">.</span><span class="nx">prepend</span><span class="p">(</span><span class="nx">stats</span><span class="p">.</span><span class="nx">domElement</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kd">let</span> <span class="nx">model</span><span class="p">,</span> <span class="nx">ctx</span><span class="p">,</span> <span class="nx">videoWidth</span><span class="p">,</span> <span class="nx">videoHeight</span><span class="p">,</span> <span class="nx">video</span><span class="p">,</span> <span class="nx">canvas</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">state</span> <span class="o">=</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nx">backend</span><span class="o">:</span> <span class="s2">&#34;wasm&#34;</span><span class="p">,</span>
</span></span><span class="line"><span class="cl"><span class="p">};</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">gui</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">dat</span><span class="p">.</span><span class="nx">GUI</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="nx">gui</span>
</span></span><span class="line"><span class="cl">  <span class="p">.</span><span class="nx">add</span><span class="p">(</span><span class="nx">state</span><span class="p">,</span> <span class="s2">&#34;backend&#34;</span><span class="p">,</span> <span class="p">[</span><span class="s2">&#34;wasm&#34;</span><span class="p">,</span> <span class="s2">&#34;webgl&#34;</span><span class="p">,</span> <span class="s2">&#34;cpu&#34;</span><span class="p">])</span>
</span></span><span class="line"><span class="cl">  <span class="p">.</span><span class="nx">onChange</span><span class="p">(</span><span class="kr">async</span> <span class="p">(</span><span class="nx">backend</span><span class="p">)</span> <span class="p">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="kr">await</span> <span class="nx">tf</span><span class="p">.</span><span class="nx">setBackend</span><span class="p">(</span><span class="nx">backend</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">    <span class="nx">addFlagLables</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">addFlagLables</span><span class="p">()</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">&#34;#simd_supported&#34;</span><span class="p">))</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="kr">const</span> <span class="nx">simdSupportLabel</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="s2">&#34;div&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">    <span class="nx">simdSupportLabel</span><span class="p">.</span><span class="nx">id</span> <span class="o">=</span> <span class="s2">&#34;simd_supported&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="nx">simdSupportLabel</span><span class="p">.</span><span class="nx">style</span> <span class="o">=</span> <span class="s2">&#34;font-weight: bold&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="kr">const</span> <span class="nx">simdSupported</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">tf</span><span class="p">.</span><span class="nx">env</span><span class="p">().</span><span class="nx">getAsync</span><span class="p">(</span><span class="s2">&#34;WASM_HAS_SIMD_SUPPORT&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">    <span class="nx">simdSupportLabel</span><span class="p">.</span><span class="nx">innerHTML</span> <span class="o">=</span> <span class="sb">`SIMD supported: &lt;span class=</span><span class="si">${</span><span class="nx">simdSupported</span><span class="si">}</span><span class="sb">&gt;</span><span class="si">${</span><span class="nx">simdSupported</span><span class="si">}</span><span class="sb">&lt;span&gt;`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">&#34;#description&#34;</span><span class="p">).</span><span class="nx">appendChild</span><span class="p">(</span><span class="nx">simdSupportLabel</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">&#34;#threads_supported&#34;</span><span class="p">))</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="kr">const</span> <span class="nx">threadSupportLabel</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">createElement</span><span class="p">(</span><span class="s2">&#34;div&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">    <span class="nx">threadSupportLabel</span><span class="p">.</span><span class="nx">id</span> <span class="o">=</span> <span class="s2">&#34;threads_supported&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="nx">threadSupportLabel</span><span class="p">.</span><span class="nx">style</span> <span class="o">=</span> <span class="s2">&#34;font-weight: bold&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="kr">const</span> <span class="nx">threadsSupported</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">tf</span>
</span></span><span class="line"><span class="cl">      <span class="p">.</span><span class="nx">env</span><span class="p">()</span>
</span></span><span class="line"><span class="cl">      <span class="p">.</span><span class="nx">getAsync</span><span class="p">(</span><span class="s2">&#34;WASM_HAS_MULTITHREAD_SUPPORT&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">    <span class="nx">threadSupportLabel</span><span class="p">.</span><span class="nx">innerHTML</span> <span class="o">=</span> <span class="sb">`Threads supported: &lt;span class=</span><span class="si">${</span><span class="nx">threadsSupported</span><span class="si">}</span><span class="sb">&gt;</span><span class="si">${</span><span class="nx">threadsSupported</span><span class="si">}</span><span class="sb">&lt;/span&gt;`</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">    <span class="nb">document</span><span class="p">.</span><span class="nx">querySelector</span><span class="p">(</span><span class="s2">&#34;#description&#34;</span><span class="p">).</span><span class="nx">appendChild</span><span class="p">(</span><span class="nx">threadSupportLabel</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">async</span> <span class="kd">function</span> <span class="nx">setupCamera</span><span class="p">()</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nx">video</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">getElementById</span><span class="p">(</span><span class="s2">&#34;video&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">stream</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">navigator</span><span class="p">.</span><span class="nx">mediaDevices</span><span class="p">.</span><span class="nx">getUserMedia</span><span class="p">({</span>
</span></span><span class="line"><span class="cl">    <span class="nx">audio</span><span class="o">:</span> <span class="kc">false</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nx">video</span><span class="o">:</span> <span class="p">{</span> <span class="nx">facingMode</span><span class="o">:</span> <span class="s2">&#34;user&#34;</span> <span class="p">},</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl">  <span class="nx">video</span><span class="p">.</span><span class="nx">srcObject</span> <span class="o">=</span> <span class="nx">stream</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">return</span> <span class="k">new</span> <span class="nb">Promise</span><span class="p">((</span><span class="nx">resolve</span><span class="p">)</span> <span class="p">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nx">video</span><span class="p">.</span><span class="nx">onloadedmetadata</span> <span class="o">=</span> <span class="p">()</span> <span class="p">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="nx">resolve</span><span class="p">(</span><span class="nx">video</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">    <span class="p">};</span>
</span></span><span class="line"><span class="cl">  <span class="p">});</span>
</span></span><span class="line"><span class="cl"><span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">renderPrediction</span> <span class="o">=</span> <span class="kr">async</span> <span class="p">()</span> <span class="p">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="nx">stats</span><span class="p">.</span><span class="nx">begin</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">returnTensors</span> <span class="o">=</span> <span class="kc">false</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">flipHorizontal</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">annotateBoxes</span> <span class="o">=</span> <span class="kc">true</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="kr">const</span> <span class="nx">predictions</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">model</span><span class="p">.</span><span class="nx">estimateFaces</span><span class="p">(</span>
</span></span><span class="line"><span class="cl">    <span class="nx">video</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nx">returnTensors</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nx">flipHorizontal</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">    <span class="nx">annotateBoxes</span><span class="p">,</span>
</span></span><span class="line"><span class="cl">  <span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="k">if</span> <span class="p">(</span><span class="nx">predictions</span><span class="p">.</span><span class="nx">length</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">    <span class="nx">ctx</span><span class="p">.</span><span class="nx">clearRect</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="nx">canvas</span><span class="p">.</span><span class="nx">width</span><span class="p">,</span> <span class="nx">canvas</span><span class="p">.</span><span class="nx">height</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">    <span class="k">for</span> <span class="p">(</span><span class="kd">let</span> <span class="nx">i</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="nx">i</span> <span class="o">&lt;</span> <span class="nx">predictions</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span> <span class="nx">i</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">      <span class="k">if</span> <span class="p">(</span><span class="nx">returnTensors</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">topLeft</span> <span class="o">=</span> <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">topLeft</span><span class="p">.</span><span class="nx">arraySync</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">        <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">bottomRight</span> <span class="o">=</span> <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">bottomRight</span><span class="p">.</span><span class="nx">arraySync</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">        <span class="k">if</span> <span class="p">(</span><span class="nx">annotateBoxes</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">          <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">landmarks</span> <span class="o">=</span> <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">landmarks</span><span class="p">.</span><span class="nx">arraySync</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">        <span class="p">}</span>
</span></span><span class="line"><span class="cl">      <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">      <span class="kr">const</span> <span class="nx">start</span> <span class="o">=</span> <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">topLeft</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">      <span class="kr">const</span> <span class="nx">end</span> <span class="o">=</span> <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">bottomRight</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">      <span class="kr">const</span> <span class="nx">size</span> <span class="o">=</span> <span class="p">[</span><span class="nx">end</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">-</span> <span class="nx">start</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nx">end</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">-</span> <span class="nx">start</span><span class="p">[</span><span class="mi">1</span><span class="p">]];</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ctx</span><span class="p">.</span><span class="nx">fillStyle</span> <span class="o">=</span> <span class="s2">&#34;rgba(255, 0, 0, 0.5)&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">      <span class="nx">ctx</span><span class="p">.</span><span class="nx">fillRect</span><span class="p">(</span><span class="nx">start</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nx">start</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="nx">size</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nx">size</span><span class="p">[</span><span class="mi">1</span><span class="p">]);</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">      <span class="k">if</span> <span class="p">(</span><span class="nx">annotateBoxes</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">        <span class="kr">const</span> <span class="nx">landmarks</span> <span class="o">=</span> <span class="nx">predictions</span><span class="p">[</span><span class="nx">i</span><span class="p">].</span><span class="nx">landmarks</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">        <span class="nx">ctx</span><span class="p">.</span><span class="nx">fillStyle</span> <span class="o">=</span> <span class="s2">&#34;blue&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">        <span class="k">for</span> <span class="p">(</span><span class="kd">let</span> <span class="nx">j</span> <span class="o">=</span> <span class="mi">0</span><span class="p">;</span> <span class="nx">j</span> <span class="o">&lt;</span> <span class="nx">landmarks</span><span class="p">.</span><span class="nx">length</span><span class="p">;</span> <span class="nx">j</span><span class="o">++</span><span class="p">)</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">          <span class="kr">const</span> <span class="nx">x</span> <span class="o">=</span> <span class="nx">landmarks</span><span class="p">[</span><span class="nx">j</span><span class="p">][</span><span class="mi">0</span><span class="p">];</span>
</span></span><span class="line"><span class="cl">          <span class="kr">const</span> <span class="nx">y</span> <span class="o">=</span> <span class="nx">landmarks</span><span class="p">[</span><span class="nx">j</span><span class="p">][</span><span class="mi">1</span><span class="p">];</span>
</span></span><span class="line"><span class="cl">          <span class="nx">ctx</span><span class="p">.</span><span class="nx">fillRect</span><span class="p">(</span><span class="nx">x</span><span class="p">,</span> <span class="nx">y</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">        <span class="p">}</span>
</span></span><span class="line"><span class="cl">      <span class="p">}</span>
</span></span><span class="line"><span class="cl">    <span class="p">}</span>
</span></span><span class="line"><span class="cl">  <span class="p">}</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">stats</span><span class="p">.</span><span class="nx">end</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">requestAnimationFrame</span><span class="p">(</span><span class="nx">renderPrediction</span><span class="p">);</span>
</span></span><span class="line"><span class="cl"><span class="p">};</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">setupPage</span> <span class="o">=</span> <span class="kr">async</span> <span class="p">()</span> <span class="p">=&gt;</span> <span class="p">{</span>
</span></span><span class="line"><span class="cl">  <span class="kr">await</span> <span class="nx">tf</span><span class="p">.</span><span class="nx">setBackend</span><span class="p">(</span><span class="nx">state</span><span class="p">.</span><span class="nx">backend</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="nx">addFlagLables</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="kr">await</span> <span class="nx">setupCamera</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">  <span class="nx">video</span><span class="p">.</span><span class="nx">play</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">videoWidth</span> <span class="o">=</span> <span class="nx">video</span><span class="p">.</span><span class="nx">videoWidth</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="nx">videoHeight</span> <span class="o">=</span> <span class="nx">video</span><span class="p">.</span><span class="nx">videoHeight</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="nx">video</span><span class="p">.</span><span class="nx">width</span> <span class="o">=</span> <span class="nx">videoWidth</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="nx">video</span><span class="p">.</span><span class="nx">height</span> <span class="o">=</span> <span class="nx">videoHeight</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">canvas</span> <span class="o">=</span> <span class="nb">document</span><span class="p">.</span><span class="nx">getElementById</span><span class="p">(</span><span class="s2">&#34;output&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="nx">canvas</span><span class="p">.</span><span class="nx">width</span> <span class="o">=</span> <span class="nx">videoWidth</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="nx">canvas</span><span class="p">.</span><span class="nx">height</span> <span class="o">=</span> <span class="nx">videoHeight</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">  <span class="nx">ctx</span> <span class="o">=</span> <span class="nx">canvas</span><span class="p">.</span><span class="nx">getContext</span><span class="p">(</span><span class="s2">&#34;2d&#34;</span><span class="p">);</span>
</span></span><span class="line"><span class="cl">  <span class="nx">ctx</span><span class="p">.</span><span class="nx">fillStyle</span> <span class="o">=</span> <span class="s2">&#34;rgba(255, 0, 0, 0.5)&#34;</span><span class="p">;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">model</span> <span class="o">=</span> <span class="kr">await</span> <span class="nx">blazeface</span><span class="p">.</span><span class="nx">load</span><span class="p">();</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">  <span class="nx">renderPrediction</span><span class="p">();</span>
</span></span><span class="line"><span class="cl"><span class="p">};</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="nx">setupPage</span><span class="p">();</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

  </div>
</div>



### tf-backend-wasm.js 文件

`tf-backend-wasm.js` 文件是 [TensorFlow.js 库](https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-wasm) 的一部分。它包含 TensorFlow.js WASM 后端的初始化逻辑、一些与 WASM 二进制文件交互的实用程序，以及用于为 WASM 二进制文件设置自定义路径的函数。

### tfjs-backend-wasm-simd.wasm 文件

`tfjs-backend-wasm-simd.wasm` 文件是 [TensorFlow.js 库](https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-wasm) 的一部分。它是一个 WASM 二进制文件，用于 WebAssembly 后端，专门优化以利用 SIMD（单指令多数据）指令。

## 探索 Dockerfile

在基于 Docker 的项目中，Dockerfile 是构建应用程序环境的基础资产。

Dockerfile 是一个文本文件，用于指示 Docker 如何创建应用程序环境的镜像。镜像包含运行应用程序时所需的一切，例如文件、包和工具。

以下是此项目的 Dockerfile。

```dockerfile
FROM nginx:stable-alpine3.17-slim
WORKDIR /usr/share/nginx/html
COPY . .
```

此 Dockerfile 定义了一个镜像，该镜像使用来自 Alpine Linux 基础镜像的 Nginx 提供静态内容。

## 使用 Compose 进行开发

Docker Compose 是一个用于定义和运行多容器 Docker 应用程序的工具。使用 Compose，您可以使用 YAML 文件配置应用程序的服务、网络和卷。在这种情况下，该应用程序不是多容器应用程序，但 Docker Compose 具有其他对开发有用的功能，例如 [Compose Watch](/manuals/compose/how-tos/file-watch.md)。

示例应用程序还没有 Compose 文件。要创建 Compose 文件，请在 `TensorJS-Face-Detection` 目录中创建一个名为 `compose.yaml` 的文本文件，然后添加以下内容。

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 80:80
    develop:
      watch:
        - action: sync
          path: .
          target: /usr/share/nginx/html
```

此 Compose 文件定义了一个使用同一目录中的 Dockerfile 构建的服务。它将主机上的端口 80 映射到容器中的端口 80。它还有一个 `develop` 子部分，其中包含 `watch` 属性，该属性定义了一组规则，用于根据本地文件更改控制服务的自动更新。有关 Compose 指令的更多详细信息，请参阅 [Compose 文件参考](/reference/compose-file/_index.md)。

保存对 `compose.yaml` 文件所做的更改，然后运行以下命令以运行应用程序。

```console
$ docker compose watch
```

应用程序运行后，打开 Web 浏览器并访问 [http://localhost:80](http://localhost:80) 以使用应用程序。您可能需要授予应用程序访问网络摄像头的权限。

现在，您可以更改源代码，并看到这些更改自动反映在容器中，而无需重建和重新运行容器。

打开 `index.js` 文件，并将第 83 行的特征点更新为绿色而不是蓝色。

```diff
-        ctx.fillStyle = "blue";
+        ctx.fillStyle = "green";
```

保存对 `index.js` 文件所做的更改，然后刷新浏览器页面。特征点现在应显示为绿色。

要停止应用程序，请在终端中按 `ctrl`+`c`。

## 共享您的镜像

在 Docker Hub 上发布您的 Docker 镜像可简化其他人的部署流程，使其能够无缝集成到各种项目中。它还能促进您的容器化解决方案的采用，扩大其在开发人员生态系统中的影响。要共享您的镜像：

1. [注册](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade) 或登录 [Docker Hub](https://hub.docker.com)。

2. 重建您的镜像以包含对应用程序所做的更改。这次，在镜像名称前加上您的 Docker ID。Docker 使用该名称来确定将其推送到哪个仓库。打开终端并在 `TensorJS-Face-Detection` 目录中运行以下命令。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker build -t YOUR-USER-NAME/face-detection-tensorjs .
   ```

3. 运行以下 `docker push` 命令以将镜像推送到 Docker Hub。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker push YOUR-USER-NAME/face-detection-tensorjs
   ```

4. 验证您是否已将镜像推送到 Docker Hub。
   1. 转到 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **Repositories**。
   3. 查看仓库的 **Last pushed** 时间。

现在，其他用户可以使用 `docker run` 命令下载并运行您的镜像。他们需要将 `YOUR-USER-NAME` 替换为您的 Docker ID。

```console
$ docker run -p 80:80 YOUR-USER-NAME/face-detection-tensorjs
```

## 总结

本指南演示了如何利用 TensorFlow.js 和 Docker 在 Web 应用程序中进行人脸检测。它强调了运行容器化 TensorFlow.js 应用程序的简便性，以及使用 Docker Compose 进行实时代码更改的开发方式。此外，它还介绍了如何在 Docker Hub 上共享您的 Docker 镜像，以简化其他人的部署流程，从而增强应用程序在开发人员社区中的影响力。

相关信息：

- [TensorFlow.js 网站](https://www.tensorflow.org/js)
- [MediaPipe 网站](https://developers.google.com/mediapipe/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Compose 文件参考](/reference/compose-file/_index.md)
- [Docker CLI 参考](/reference/cli/docker/)
- [Docker 博客：使用 TensorFlow.js 加速机器学习](https://www.docker.com/blog/accelerating-machine-learning-with-tensorflow-js-using-pretrained-models-and-docker/)
