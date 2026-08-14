# 容器设备接口（CDI）


<!-- vale Docker.We = NO -->

[容器设备接口（CDI）](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md)
是一项规范，旨在标准化设备（如 GPU、FPGA 及其他硬件加速器）如何暴露给容器并被容器使用。其目的是
为在容器化环境中使用硬件设备提供一种更一致、更安全的机制，解决与设备特定设置和配置相关的挑战。

除了使容器能够与设备节点交互外，CDI 还允许你为设备指定额外的配置，例如环境变量、主机挂载（如
共享对象）和可执行钩子（hooks）。

## 入门（Getting started）

要开始使用 CDI，你需要搭建一个兼容的环境。这包括安装 Docker v27+（已
[配置 CDI](/reference/cli/dockerd.md#configure-cdi-devices)）以及 Buildx v0.22+。

你还需要使用 JSON 或 YAML 文件在以下位置之一创建
[设备规范](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md#cdi-json-specification)：

* `/etc/cdi`
* `/var/run/cdi`
* `/etc/buildkit/cdi`

> [!NOTE]
> 如果你直接使用 BuildKit，可以通过设置 [`buildkitd.toml` 配置文件](../buildkit/configure.md)
> 的 `cdi` 段落中的 `specDirs` 选项来更改位置。如果你使用带 `docker` 驱动的 Docker 守护进程进行
> 构建，请参阅 [配置 CDI 设备](/reference/cli/dockerd.md#configure-cdi-devices) 文档。

> [!NOTE]
> 如果你在 WSL 上创建容器构建器，需要确保已安装 [Docker Desktop](../../desktop/_index.md) 且已启用
> [WSL 2 GPU 半虚拟化](../../desktop/features/gpu.md#prerequisites)。还需要 Buildx v0.27+ 才能在容器中
> 挂载 WSL 库。

## 使用简单 CDI 规范进行构建（Building with a simple CDI specification）

让我们从一个简单的 CDI 规范开始，它将一个环境变量注入构建环境，并将其写入 `/etc/cdi/foo.yaml`：

```yaml {title="/etc/cdi/foo.yaml"}
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
- name: foo
  containerEdits:
    env:
    - FOO=injected
```

检查 `default` 构建器，确认 `vendor1.com/device` 被检测为设备：

```console
$ docker buildx inspect
Name:   default
Driver: docker

Nodes:
Name:             default
Endpoint:         default
Status:           running
BuildKit version: v0.23.2
Platforms:        linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/amd64/v4, linux/386
Labels:
 org.mobyproject.buildkit.worker.moby.host-gateway-ip: 172.17.0.1
Devices:
 Name:                  vendor1.com/device=foo
 Automatically allowed: false
GC Policy rule#0:
 All:            false
 Filters:        type==source.local,type==exec.cachemount,type==source.git.checkout
 Keep Duration:  48h0m0s
 Max Used Space: 658.9MiB
GC Policy rule#1:
 All:            false
 Keep Duration:  1440h0m0s
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
GC Policy rule#2:
 All:            false
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
GC Policy rule#3:
 All:            true
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
```

现在让我们创建一个 Dockerfile 来使用此设备：

```dockerfile
# syntax=docker/dockerfile:1-labs
FROM busybox
RUN --device=vendor1.com/device \
  env | grep ^FOO=
```

这里我们使用 [`RUN --device` 命令](/reference/dockerfile.md#run---device) 并设置 `vendor1.com/device`，
它请求规范中可用的第一个设备。在本例中它使用 `foo`，即 `/etc/cdi/foo.yaml` 中的第一个设备。

> [!NOTE]
> [`RUN --device` 命令](/reference/dockerfile.md#run---device) 仅在
> [`labs` 通道](../buildkit/frontend.md#labs-channel) 中提供，自
> [Dockerfile frontend v1.14.0-labs](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.0-labs)
> 起，在稳定语法中尚不可用。

现在让我们构建此 Dockerfile：

```console
$ docker buildx build .
[+] Building 0.4s (5/5) FINISHED                                                                                                        docker:default
 => [internal] load build definition from Dockerfile                                                                                    0.0s 
 => => transferring dockerfile: 155B                                                                                                    0.0s
 => resolve image config for docker-image://docker/dockerfile:1-labs                                                                    0.1s 
 => CACHED docker-image://docker/dockerfile:1-labs@sha256:9187104f31e3a002a8a6a3209ea1f937fb7486c093cbbde1e14b0fa0d7e4f1b5              0.0s
 => [internal] load metadata for docker.io/library/busybox:latest                                                                       0.1s 
 => [internal] load .dockerignore                                                                                                       0.0s
 => => transferring context: 2B                                                                                                         0.0s 
ERROR: failed to build: failed to solve: failed to load LLB: device vendor1.com/device=foo is requested by the build but not allowed
```

它失败了，因为如上 `buildx inspect` 输出所示，设备 `vendor1.com/device=foo` 未被构建自动允许：

```text
Devices:
 Name:                  vendor1.com/device=foo
 Automatically allowed: false
```

要允许该设备，你可以使用 [`--allow` 标志](/reference/cli/docker/buildx/build/#allow) 配合
`docker buildx build` 命令：

```console
$ docker buildx build --allow device .
```

或者，你可以在 CDI 规范中设置 `org.mobyproject.buildkit.device.autoallow` 注解，以自动允许该设备在所有
构建中使用：

```yaml {title="/etc/cdi/foo.yaml"}
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
- name: foo
  containerEdits:
    env:
    - FOO=injected
annotations:
  org.mobyproject.buildkit.device.autoallow: true
```

现在再次使用 `--allow device` 标志运行构建：

```console
$ docker buildx build --progress=plain --allow device .
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 159B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker/dockerfile:1-labs
#2 DONE 0.1s

#3 docker-image://docker/dockerfile:1-labs@sha256:9187104f31e3a002a8a6a3209ea1f937fb7486c093cbbde1e14b0fa0d7e4f1b5
#3 CACHED

#4 [internal] load metadata for docker.io/library/busybox:latest
#4 DONE 0.1s

#5 [internal] load .dockerignore
#5 transferring context: 2B done
#5 DONE 0.0s

#6 [1/2] FROM docker.io/library/busybox:latest@sha256:f85340bf132ae937d2c2a763b8335c9bab35d6e8293f70f606b9c6178d84f42b
#6 CACHED

#7 [2/2] RUN --device=vendor1.com/device   env | grep ^FOO=
#7 0.155 FOO=injected
#7 DONE 0.2s
```

构建成功，输出显示 `FOO` 环境变量已按 CDI 规范中的指定被注入到构建环境中。

## 设置带有 GPU 支持的容器构建器（Set up a container builder with GPU support）

在本节中，我们将向你展示如何使用 NVIDIA GPU 设置
[容器构建器](../builders/drivers/docker-container.md)。自 Buildx v0.22 起，在创建新的容器构建器时，
如果主机的内核中已安装 GPU 驱动，会自动向容器构建器添加 GPU 请求。这类似于使用
[`docker run` 的 `--gpus=all`](/reference/cli/docker/container/run/#gpus) 命令。

现在让我们使用 Buildx 创建一个名为 `gpubuilder` 的容器构建器：

```console
$ docker buildx create --name gpubuilder --driver-opt "image=moby/buildkit:buildx-stable-1-gpu" --bootstrap
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1-gpu
#1 pulling image moby/buildkit:buildx-stable-1-gpu 1.0s done
#1 creating container buildx_buildkit_gpubuilder0
#1 creating container buildx_buildkit_gpubuilder0 8.8s done
#1 DONE 9.8s
gpubuilder
```

> [!NOTE]
> 我们制作了一个特别定制的 BuildKit 镜像，因为当前的 BuildKit 发布镜像基于 Alpine，不支持 NVIDIA 驱动。
> 以下镜像基于 Ubuntu，并安装 NVIDIA 客户端库，且在构建期间请求设备时为容器构建器生成 GPU 的 CDI 规范。

让我们检查此构建器：

```console
$ docker buildx inspect gpubuilder
Name:          gpubuilder
Driver:        docker-container
Last Activity: 2025-07-10 08:18:09 +0000 UTC

Nodes:
Name:                  gpubuilder0
Endpoint:              unix:///var/run/docker.sock
Driver Options:        image="moby/buildkit:buildx-stable-1-gpu"
Status:                running
BuildKit daemon flags: --allow-insecure-entitlement=network.host
BuildKit version:      v0.26.2
Platforms:             linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/arm64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
Labels:
 org.mobyproject.buildkit.worker.executor:         oci
 org.mobyproject.buildkit.worker.hostname:         d6aa9cbe8462
 org.mobyproject.buildkit.worker.network:          host
 org.mobyproject.buildkit.worker.oci.process-mode: sandbox
 org.mobyproject.buildkit.worker.selinux.enabled:  false
 org.mobyproject.buildkit.worker.snapshotter:      overlayfs
Devices:
 Name:      nvidia.com/gpu
 On-Demand: true
GC Policy rule#0:
 All:            false
 Filters:        type==source.local,type==exec.cachemount,type==source.git.checkout
 Keep Duration:  48h0m0s
 Max Used Space: 488.3MiB
GC Policy rule#1:
 All:            false
 Keep Duration:  1440h0m0s
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
GC Policy rule#2:
 All:            false
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
GC Policy rule#3:
 All:            true
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
```

我们可以看到 `nvidia.com/gpu` 供应商被检测为构建器中的一个设备，这意味着检测到了驱动。

可选地，你可以使用 `nvidia-smi` 检查容器是否有 NVIDIA GPU 设备可用：

```console
$ docker exec -it buildx_buildkit_gpubuilder0 nvidia-smi -L
GPU 0: Tesla T4 (UUID: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84)
```

## 使用 GPU 支持进行构建（Building with GPU support）

让我们创建一个将使用 GPU 设备的简单 Dockerfile：

```dockerfile
# syntax=docker/dockerfile:1-labs
FROM ubuntu
RUN --device=nvidia.com/gpu nvidia-smi -L
```

现在使用我们之前创建的 `gpubuilder` 构建器运行构建：

```console
$ docker buildx --builder gpubuilder build --progress=plain .
#0 building with "gpubuilder" instance using docker-container driver
...

#7 preparing device nvidia.com/gpu
#7 0.000 > apt-get update
...
#7 4.872 > apt-get install -y gpg
...
#7 10.16 Downloading NVIDIA GPG key
#7 10.21 > apt-get update
...
#7 12.15 > apt-get install -y --no-install-recommends nvidia-container-toolkit-base
...
#7 17.80 time="2025-04-15T08:58:16Z" level=info msg="Generated CDI spec with version 0.8.0"
#7 DONE 17.8s

#8 [2/2] RUN --device=nvidia.com/gpu nvidia-smi -L
#8 0.527 GPU 0: Tesla T4 (UUID: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84)
#8 DONE 1.6s
```

你可能注意到了，步骤 `#7` 通过安装客户端库和 toolkit 来为 GPU 生成 CDI 规范，从而准备 `nvidia.com/gpu`
设备。

随后 `nvidia-smi -L` 命令在容器中使用 GPU 设备执行。输出显示了 GPU UUID。

你可以用以下命令检查容器构建器中生成的 CDI 规范：

```console
$ docker exec -it buildx_buildkit_gpubuilder0 cat /etc/cdi/nvidia.yaml
```

对于此处使用的 EC2 实例 [`g4dn.xlarge`](https://aws.amazon.com/ec2/instance-types/g4/)，它看起来如下：

```yaml {collapse=true}
cdiVersion: 0.6.0
containerEdits:
  deviceNodes:
  - path: /dev/nvidia-modeset
  - path: /dev/nvidia-uvm
  - path: /dev/nvidia-uvm-tools
  - path: /dev/nvidiactl
  env:
  - NVIDIA_VISIBLE_DEVICES=void
  hooks:
  - args:
    - nvidia-cdi-hook
    - create-symlinks
    - --link
    - ../libnvidia-allocator.so.1::/usr/lib/x86_64-linux-gnu/gbm/nvidia-drm_gbm.so
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - create-symlinks
    - --link
    - libcuda.so.1::/usr/lib/x86_64-linux-gnu/libcuda.so
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - enable-cuda-compat
    - --host-driver-version=570.133.20
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - update-ldcache
    - --folder
    - /usr/lib/x86_64-linux-gnu
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  mounts:
  - containerPath: /run/nvidia-persistenced/socket
    hostPath: /run/nvidia-persistenced/socket
    options:
    - ro
    - nosuid
    - nodev
    - bind
    - noexec
  - containerPath: /usr/bin/nvidia-cuda-mps-control
    hostPath: /usr/bin/nvidia-cuda-mps-control
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-cuda-mps-server
    hostPath: /usr/bin/nvidia-cuda-mps-server
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-debugdump
    hostPath: /usr/bin/nvidia-debugdump
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-persistenced
    hostPath: /usr/bin/nvidia-persistenced
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-smi
    hostPath: /usr/bin/nvidia-smi
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libcuda.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libcuda.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libcudadebugger.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libcudadebugger.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-allocator.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-allocator.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-cfg.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-cfg.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-gpucomp.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-gpucomp.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-nscq.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-nscq.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-nvvm.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-nvvm.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-opencl.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-opencl.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11-openssl3.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11-openssl3.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /lib/firmware/nvidia/570.133.20/gsp_ga10x.bin
    hostPath: /lib/firmware/nvidia/570.133.20/gsp_ga10x.bin
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /lib/firmware/nvidia/570.133.20/gsp_tu10x.bin
    hostPath: /lib/firmware/nvidia/570.133.20/gsp_tu10x.bin
    options:
    - ro
    - nosuid
    - nodev
    - bind
devices:
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: "0"
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: all
kind: nvidia.com/gpu
```

恭喜你完成了第一次使用 GPU 设备配合 BuildKit 和 CDI 的构建。

