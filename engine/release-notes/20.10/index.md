# Docker Engine 20.10 发布说明

本文档描述了 Docker Engine 20.10 版本的最新变更、新增内容、已知问题和修复。

## 20.10.24
<em class="text-gray-400 italic dark:text-gray-500">2023-04-04</em>


### 更新

- 将 Go 运行时更新至 [1.19.7](https://go.dev/doc/devel/release#go1.19.minor)。
- 将 Docker Buildx 更新至 [v0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4)。
- 将 containerd 更新至 [v1.6.20](https://github.com/containerd/containerd/releases/tag/v1.6.20)。
- 将 runc 更新至 [v1.1.5](https://github.com/opencontainers/runc/releases/tag/v1.1.5)。

### 错误修复与增强

- 修复了若干可能导致 Swarm 加密覆盖网络无法保证其安全性的问题，解决了 [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841)、
  [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840) 和
  [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842)。
  - 现在当内核不支持加密覆盖网络时，将报告为错误。
  - 加密覆盖网络现在会主动建立，而不是等待多个节点连接。
  - 通过使用 `xt_bpf` 内核模块，加密覆盖网络现在可以在 Red Hat Enterprise Linux 9 上使用。
  - Swarm 覆盖网络用户应查阅 [GHSA-vwm3-crmr-xfxw](https://github.com/moby/moby/security/advisories/GHSA-vwm3-crmr-xfxw) 以确保未发生意外暴露。
- 升级 github.com/containerd/fifo 至 v1.1.0 以修复潜在的 panic [moby/moby#45216](https://github.com/moby/moby/pull/45242)。
- 修复已安装 cli-plugins 的 Bash 补全缺失问题 [docker/cli#4091](https://github.com/docker/cli/pull/4091)。


## 20.10.23
<em class="text-gray-400 italic dark:text-gray-500">2023-01-19</em>


此版本的 Docker Engine 包含了更新版本的 Docker Compose、Docker Buildx、containerd，以及一些次要的错误修复和增强。

### 更新

- 将 Docker Compose 更新至 [v2.15.1](https://github.com/docker/compose/releases/tag/v2.15.1)。
- 将 Docker Buildx 更新至 [v0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0)。
- 将 containerd (`containerd.io` 软件包) 更新至 [v1.6.15](https://github.com/containerd/containerd/releases/tag/v1.6.15)。
- 更新 `docker-compose-cli` 的软件包版本格式，以允许发行版版本更新 [docker/docker-ce-packaging#822](https://github.com/docker/docker-ce-packaging/pull/822)。
- 将 Go 运行时更新至 [1.18.10](https://go.dev/doc/devel/release#go1.18.minor)。

### 错误修复与增强

- 修复了在启用 BuildKit 的情况下使用 `--add-host=host.docker.internal:host-gateway` 时 `docker build` 失败的问题 [moby/moby#44650](https://github.com/moby/moby/pull/44650)。
- 回退 seccomp：在默认配置文件中阻止对 `AF_VSOCK` 的 socket 调用 [moby/moby#44712](https://github.com/moby/moby/pull/44712)。

  此变更虽然从安全角度看是有利的，但导致了某些用例的行为变化。因此，我们回退了此变更，以确保受影响用户的稳定性和兼容性。

  然而，容器中 `AF_VSOCK` 的用户应认识到，此（特殊）地址族在任何版本的 Linux 内核中目前都不是命名空间的，并可能导致意外行为，例如容器直接与主机虚拟机
