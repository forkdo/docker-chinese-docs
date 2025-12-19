---
description: 查找 Docker Desktop 的已知问题
keywords: mac, troubleshooting, known issues, Docker Desktop
title: 已知问题
tags: [ Troubleshooting ]
weight: 20
aliases:
 - /desktop/troubleshoot/known-issues/
---

{{< tabs >}}
{{< tab name="适用于搭载 Intel 芯片的 Mac" >}}
- Mac 活动监视器报告 Docker 使用的内存量是其实际使用量的两倍。这是由于 [macOS 的一个 bug](https://docs.google.com/document/d/17ZiQC1Tp9iH320K-uqVLyiJmk4DHJ3c4zgQetJiKYQM/edit?usp=sharing)。

- **"Docker.app 已损坏" 对话框**：如果在安装或更新过程中看到 "Docker.app 已损坏，无法打开" 的对话框，这通常是由于其他应用程序在使用 Docker CLI 时执行了非原子复制操作所致。请参见 [修复 macOS 上的 "Docker.app 已损坏"](mac-damaged-dialog.md) 获取解决步骤。

- 在 `.dmg` 中运行 `Docker.app` 后强制弹出 `.dmg` 可能导致
  鲸鱼图标无响应，Docker 任务在活动监视器中显示为无响应，并且某些进程消耗大量 CPU 资源。重启并重新启动 Docker 以解决这些问题。

- Docker Desktop 在 macOS 10.10 Yosemite 及更高版本中使用 `HyperKit` 虚拟机监控程序
  (https://github.com/docker/hyperkit)。如果您正在使用与 `HyperKit` 有冲突的工具进行开发，例如
  [Intel 硬件加速执行管理器
  (HAXM)](https://software.intel.com/en-us/android/articles/intel-hardware-accelerated-execution-manager/)，
  目前的解决方法是不要同时运行它们。您可以通过退出 Docker Desktop 来暂停
  `HyperKit`，以便在使用 HAXM 时工作。
  这使您可以继续使用其他工具，并防止 `HyperKit`
  干扰。

- 如果您正在使用如 [Apache
  Maven](https://maven.apache.org/) 等期望为 `DOCKER_HOST` 和
  `DOCKER_CERT_PATH` 环境变量设置的应用程序，请指定这些变量以通过 Unix 套接字连接到 Docker
  实例。例如：

  ```console
  $ export DOCKER_HOST=unix:///var/run/docker.sock
  ```

{{< /tab >}}
{{< tab name="适用于搭载 Apple 芯片的 Mac" >}}

- 某些命令行工具在 Rosetta 2 未安装时无法工作。
  - 旧版本 1.x 的 `docker-compose`。请改用 Compose V2 - 输入 `docker compose`。
  - `docker-credential-ecr-login` 凭据助手。
- 某些镜像不支持 ARM64 架构。您可以添加 `--platform linux/amd64` 以使用模拟运行（或构建）Intel 镜像。

   然而，在 Apple 芯片机器上使用模拟运行基于 Intel 的容器时，由于 QEMU 有时无法运行容器，尝试可能会失败。此外，在 QEMU 模拟下，文件系统更改通知 API（`inotify`）无法工作。即使容器在模拟下正确运行，它们也会比原生等效容器更慢并消耗更多内存。

   总之，在基于 Arm 的机器上运行基于 Intel 的容器应被视为“尽力而为”。我们建议尽可能在 Apple 芯片机器上运行 `arm64` 容器，并鼓励容器作者制作 `arm64` 或多架构版本的容器。随着越来越多的镜像重建[支持多种架构](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)，这个问题应会随着时间的推移变得越来越少见。
- 用户可能会在 TCP 流半关闭时偶尔遇到数据丢失。

{{< /tab >}}
{{< /tabs >}}