---
description: 了解如何在 TensorFlow.js Web 应用程序中部署预训练模型以执行人脸检测。
keywords: tensorflow.js, machine learning, ml, mediapipe, blazeface, face detection
title: 使用 TensorFlow.js 进行人脸检测
summary: '本指南介绍如何在 Docker 容器中运行 TensorFlow.js。

  '
tags:
- ai
languages:
- js
aliases:
- /guides/use-case/tensorflowjs/
params:
  time: 20 分钟
---

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

{{< accordion title="index.html" >}}

```html
<style>
  body {
    margin: 25px;
  }

  .true {
    color: green;
  }

  .false {
    color: red;
  }

  #main {
    position: relative;
    margin: 50px 0;
  }

  canvas {
    position: absolute;
    top: 0;
    left: 0;
  }

  #description {
    margin-top: 20px;
    width: 600px;
  }

  #description-title {
    font-weight: bold;
    font-size: 18px;
  }
</style>

<body>
  <div id="main">
    <video
      id="video"
      playsinline
      style="
      -webkit-transform: scaleX(-1);
      transform: scaleX(-1);
      width: auto;
      height: auto;
      "
    ></video>
    <canvas id="output"></canvas>
    <video
      id="video"
      playsinline
      style="
      -webkit-transform: scaleX(-1);
      transform: scaleX(-1);
      visibility: hidden;
      width: auto;
      height: auto;
      "
    ></video>
  </div>
</body>
<script src="https://unpkg.com/@tensorflow/tfjs-core@2.1.0/dist/tf-core.js"></script>
<script src="https://unpkg.com/@tensorflow/tfjs-converter@2.1.0/dist/tf-converter.js"></script>

<script src="https://unpkg.com/@tensorflow/tfjs-backend-webgl@2.1.0/dist/tf-backend-webgl.js"></script>
<script src="https://unpkg.com/@tensorflow/tfjs-backend-cpu@2.1.0/dist/tf-backend-cpu.js"></script>
<script src="./tf-backend-wasm.js"></script>

<script src="https://unpkg.com/@tensorflow-models/blazeface@0.0.5/dist/blazeface.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.7.6/dat.gui.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/stats.js/r16/Stats.min.js"></script>
<script src="./index.js"></script>
```

{{< /accordion >}}

### index.js 文件

`index.js` 文件执行人脸检测逻辑。它演示了 Web 开发和机器学习集成中的几个高级概念。以下是其一些关键组件和功能：

- Stats.js：脚本首先创建一个 Stats 实例，以实时监控和显示应用程序的帧速率 (FPS)。这有助于性能分析，尤其是在测试不同 TensorFlow.js 后端对应用程序速度的影响时。
- TensorFlow.js：该应用程序允许用户通过 dat.GUI 提供的图形界面在 TensorFlow.js 的不同计算后端（wasm、webgl 和 cpu）之间切换。更改后端可能会影响性能和兼容性，具体取决于设备和浏览器。addFlagLabels 函数动态检查并显示是否支持 SIMD（单指令多数据）和多线程，这与 wasm 后端的性能优化相关。
- setupCamera 函数：使用 MediaDevices Web API 初始化用户的网络摄像头。它配置视频流不包含音频并使用前置摄像头 (facingMode: 'user')。一旦视频元数据加载完毕，它就会解析带有视频元素的 promise，然后用于人脸检测。
- BlazeFace：此应用程序的核心是 renderPrediction 函数，该函数使用 BlazeFace 模型执行实时人脸检测，这是一种用于检测图像中人脸的轻量级模型。该函数在每个动画帧上调用 model.estimateFaces 以从视频源检测人脸。对于每个检测到的人脸，它会在视频上叠加的画布上绘制一个红色矩形框和蓝色的人脸特征点。

{{< accordion title="index.js" >}}

```javascript
const stats = new Stats();
stats.showPanel(0);
document.body.prepend(stats.domElement);

let model, ctx, videoWidth, videoHeight, video, canvas;

const state = {
  backend: "wasm",
};

const gui = new dat.GUI();
gui
  .add(state, "backend", ["wasm", "webgl", "cpu"])
  .onChange(async (backend) => {
    await tf.setBackend(backend);
    addFlagLables();
  });

async function addFlagLables() {
  if (!document.querySelector("#simd_supported")) {
    const simdSupportLabel = document.createElement("div");
    simdSupportLabel.id = "simd_supported";
    simdSupportLabel.style = "font-weight: bold";
    const simdSupported = await tf.env().getAsync("WASM_HAS_SIMD_SUPPORT");
    simdSupportLabel.innerHTML = `SIMD supported: <span class=${simdSupported}>${simdSupported}<span>`;
    document.querySelector("#description").appendChild(simdSupportLabel);
  }

  if (!document.querySelector("#threads_supported")) {
    const threadSupportLabel = document.createElement("div");
    threadSupportLabel.id = "threads_supported";
    threadSupportLabel.style = "font-weight: bold";
    const threadsSupported = await tf
      .env()
      .getAsync("WASM_HAS_MULTITHREAD_SUPPORT");
    threadSupportLabel.innerHTML = `Threads supported: <span class=${threadsSupported}>${threadsSupported}</span>`;
    document.querySelector("#description").appendChild(threadSupportLabel);
  }
}

async function setupCamera() {
  video = document.getElementById("video");

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: { facingMode: "user" },
  });
  video.srcObject = stream;

  return new Promise((resolve) => {
    video.onloadedmetadata = () => {
      resolve(video);
    };
  });
}

const renderPrediction = async () => {
  stats.begin();

  const returnTensors = false;
  const flipHorizontal = true;
  const annotateBoxes = true;
  const predictions = await model.estimateFaces(
    video,
    returnTensors,
    flipHorizontal,
    annotateBoxes,
  );

  if (predictions.length > 0) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < predictions.length; i++) {
      if (returnTensors) {
        predictions[i].topLeft = predictions[i].topLeft.arraySync();
        predictions[i].bottomRight = predictions[i].bottomRight.arraySync();
        if (annotateBoxes) {
          predictions[i].landmarks = predictions[i].landmarks.arraySync();
        }
      }

      const start = predictions[i].topLeft;
      const end = predictions[i].bottomRight;
      const size = [end[0] - start[0], end[1] - start[1]];
      ctx.fillStyle = "rgba(255, 0, 0, 0.5)";
      ctx.fillRect(start[0], start[1], size[0], size[1]);

      if (annotateBoxes) {
        const landmarks = predictions[i].landmarks;

        ctx.fillStyle = "blue";
        for (let j = 0; j < landmarks.length; j++) {
          const x = landmarks[j][0];
          const y = landmarks[j][1];
          ctx.fillRect(x, y, 5, 5);
        }
      }
    }
  }

  stats.end();

  requestAnimationFrame(renderPrediction);
};

const setupPage = async () => {
  await tf.setBackend(state.backend);
  addFlagLables();
  await setupCamera();
  video.play();

  videoWidth = video.videoWidth;
  videoHeight = video.videoHeight;
  video.width = videoWidth;
  video.height = videoHeight;

  canvas = document.getElementById("output");
  canvas.width = videoWidth;
  canvas.height = videoHeight;
  ctx = canvas.getContext("2d");
  ctx.fillStyle = "rgba(255, 0, 0, 0.5)";

  model = await blazeface.load();

  renderPrediction();
};

setupPage();
```

{{< /accordion >}}

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