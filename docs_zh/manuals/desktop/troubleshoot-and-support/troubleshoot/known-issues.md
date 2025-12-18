---
description: 查找 Docker Desktop 的已知问题
keywords: mac, troubleshooting, known issues, Docker Desktop
title: 已知问题
tags: [ 故障排除 ]
weight: 20
aliases:
 - /desktop/troubleshoot/known-issues/
---

{{< tabs >}}
{{< tab name="For Mac with Intel chip" >}}
- Mac 活动监视器报告 Docker 使用的内存是实际使用量的两倍。这是由于 macOS 中的一个 [bug](https://docs.google.com/document/d/17ZiQC1Tp9iH320K-uqVLyiJmk4DHJ3c4zgQetJiKYQM/edit?usp=sharing) 导致的。

- **“Docker.app 已损坏”对话框**：如果你在安装或更新过程中看到“Docker.app 已损坏，无法打开”的对话框，这通常是由于其他应用程序正在使用 Docker CLI 时执行了非原子复制操作导致的。请参阅 [修复 macOS 上的“Docker.app 已损坏”](mac-damaged-dialog.md) 以获取解决步骤。

- 强制弹出 `.dmg` 文件后运行 `Docker.app` 可能导致鲸鱼图标无响应、活动监视器中 Docker 任务显示为未响应，以及某些进程消耗大量 CPU 资源。重启并重新启动 Docker 可解决这些问题。

- Docker Desktop 在 macOS 10.10 Yosemite 及更高版本中使用 `HyperKit` 虚拟机管理程序（https://github.com/docker/hyperkit）。如果你正在开发的工具与 `HyperKit` 存在冲突，例如 [Intel 硬件加速执行管理器（HAXM）](https://software.intel.com/en-us/android/articles/intel-hardware-accelerated-execution-manager/)，目前的变通方法是不要同时运行它们。你可以通过临时退出 Docker Desktop 来暂停 `HyperKit`，以便与其他工具一起工作，并防止 `HyperKit` 干扰。

- 如果你正在使用 [Apache Maven](https://maven.apache.org/) 等需要 `DOCKER_HOST` 和 `DOCKER_CERT_PATH` 环境变量的应用程序，可以指定这些变量通过 Unix 套接字连接到 Docker 实例。例如：

  ```console
  $ export DOCKER_HOST=unix:///var/run/docker.sock
  ```

{{< /tab >}}
{{< tab name="For Mac with Apple silicon" >}}

- 某些命令行工具在未安装 Rosetta 2 时无法正常工作。
  - 旧版本 1.x 的 `docker-compose`。请改用 Compose V2 — 输入 `docker compose`。
  - `docker-credential-ecr-login` 凭据助手。
- 某些镜像不支持 ARM64 架构。你可以添加 `--platform linux/amd64` 来通过仿真运行（或构建）Intel 架构的镜像。

   但是，尝试在仿真环境下于 Apple silicon 机器上运行基于 Intel 的容器可能会崩溃，因为 QEMU 有时无法运行容器。此外，文件系统变更通知 API（`inotify`）在 QEMU 仿真下无法工作。即使容器在仿真下能够正确运行，它们也会比原生版本更慢，并消耗更多内存。

   总之，在基于 Arm 的机器上运行基于 Intel 的容器应被视为“尽力而为”。我们建议在 Apple silicon 机器上尽可能运行 `arm64` 容器，并鼓励容器作者提供 `arm64` 或多架构版本的容器。随着越来越多的镜像被重建以支持[多架构](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/)，此问题应会随时间推移而变得越来越少。
- 用户偶尔可能在 TCP 流半关闭时遇到数据丢失的情况。

{{< /tab >}}
{{< /tabs >}}
