---
title: GPU 访问
weight: 40
description: 如何从容器访问 NVIDIA GPU
keywords: docker, GPU, NVIDIA, cuda, nvidia-smi, device, container toolkit
---

## 访问 NVIDIA GPU

### 先决条件

访问官方 [NVIDIA 驱动程序页面](https://www.nvidia.com/Download/index.aspx) 下载并安装合适的驱动程序。安装完成后请重启系统。

验证您的 GPU 正在运行且可访问。

### 安装 NVIDIA Container Toolkit

按照官方的 NVIDIA Container Toolkit [安装说明](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) 进行操作。

### 暴露 GPU 以供使用

在启动容器时包含 `--gpus` 标志以访问 GPU 资源。

要暴露所有可用的 GPU：

```console
$ docker run -it --rm --gpus all ubuntu nvidia-smi
```

输出如下所示：

```text
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.288.01             Driver Version: 535.288.01   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA L4                      Off | 00000000:31:00.0 Off |                    0 |
| N/A   40C    P0              27W /  72W |      0MiB / 23034MiB |      4%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
```

GPU 表格最左侧的列显示每个 GPU 的索引（在上例中，NVIDIA L4 为 `0`）。使用这些索引号通过 `device` 选项指定特定的 GPU。

要按索引暴露单个 GPU：

```console
$ docker run -it --rm --gpus device=0 ubuntu nvidia-smi
```

要按 UUID 暴露 GPU，首先使用 `nvidia-smi -L` 列出 UUID：

```console
$ nvidia-smi -L
GPU 0: NVIDIA L4 (UUID: GPU-3a23c669-1f69-c64e-cf85-44e9b07e7a2a)
```

然后将 UUID 传递给 `--gpus`：

```console
$ docker run -it --rm --gpus device=GPU-3a23c669-1f69-c64e-cf85-44e9b07e7a2a ubuntu nvidia-smi
```

在具有多个 GPU 的系统上，您可以通过索引暴露多个 GPU。`device` 值必须加引号，因为它包含逗号：

```console
$ docker run -it --rm --gpus '"device=0,2"' ubuntu nvidia-smi
```

这会暴露索引为 `0` 和 `2` 的 GPU——即 `nvidia-smi` 输出中列出的第一个和第三个 GPU。

> [!NOTE]
>
> NVIDIA GPU 只能由运行单一引擎的系统访问。

### 设置 NVIDIA 能力

您可以手动设置能力。例如，在 Ubuntu 上，您可以运行以下命令：

```console
$ docker run --gpus 'all,capabilities=utility' --rm ubuntu nvidia-smi
```

这会启用 `utility` 驱动程序能力，从而将 `nvidia-smi` 工具添加到容器中。

能力和其他配置可以通过环境变量在镜像中设置。有关有效的变量，请参阅 [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html) 文档。这些变量可以在 Dockerfile 中设置。

您也可以使用 CUDA 镜像，它会自动设置这些变量。请参阅官方的 [CUDA 镜像](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/cuda) NGC 目录页面。
