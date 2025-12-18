---
title: 使用 Docker Model Runner 和 Compose Bridge
linkTitle: 使用 Model Runner
weight: 30
description: 如何使用 Docker Model Runner 和 Compose Bridge 实现一致的部署
keywords: docker compose bridge, 自定义 compose bridge, compose bridge 模板, compose 到 kubernetes, compose bridge 转换, go templates docker, model runner, ai, llms
---

Compose Bridge 支持模型感知的部署。它可以部署和配置 Docker Model Runner，这是一个托管和服务化机器 LLM 的轻量级服务。

这减少了 LLM 启用服务的手动设置，并保持 Docker Desktop 和 Kubernetes 环境之间部署的一致性。

如果您的 `compose.yaml` 文件中包含顶级 `models` 元素，Compose Bridge 会：

- 自动为每个模型的端点和名称注入环境变量。
- 为 Docker Desktop 和 Kubernetes 配置不同的模型端点。
- 在 Helm values 中启用时，可选地在 Kubernetes 中部署 Docker Model Runner。

## 配置模型运行器设置

使用生成的 Helm Charts 部署时，您可以通过 Helm values 控制模型运行器的配置。

```yaml
# 模型运行器设置
modelRunner:
    # Docker Desktop 设置为 false（使用主机实例）
    # 独立 Kubernetes 集群设置为 true
    enabled: false
    # enabled=false（Docker Desktop）时使用的端点
    hostEndpoint: "http://host.docker.internal:12434/engines/v1/"
    # enabled=true 时的部署设置
    image: "docker/model-runner:latest"
    imagePullPolicy: "IfNotPresent"
    # GPU 支持
    gpu:
        enabled: false
        vendor: "nvidia" # nvidia 或 amd
        count: 1
    # 节点调度（取消注释并根据需要自定义）
    # nodeSelector:
    #   accelerator: nvidia-tesla-t4
    # tolerations: []
    # affinity: {}

    # 安全上下文
    securityContext:
        allowPrivilegeEscalation: false
    # 环境变量（取消注释并按需添加）
    # env:
    #   DMR_ORIGINS: "http://localhost:31246"
    resources:
        limits:
            cpu: "1000m"
            memory: "2Gi"
        requests:
            cpu: "100m"
            memory: "256Mi"
    # 模型存储
    storage:
        size: "100Gi"
        storageClass: "" # 空值使用默认存储类
    # 预拉取的模型
    models:
        - ai/qwen2.5:latest
        - ai/mxbai-embed-large
```

## 部署模型运行器

### Docker Desktop

当 `modelRunner.enabled` 为 `false` 时，Compose Bridge 配置您的工作负载连接到主机上运行的 Docker Model Runner：

```text
http://host.docker.internal:12434/engines/v1/
```

该端点会自动注入到您的服务容器中。

### Kubernetes

当 `modelRunner.enabled` 为 `true` 时，Compose Bridge 使用生成的清单在您的集群中部署 Docker Model Runner，包括：

- 部署：运行 `docker-model-runner` 容器
- 服务：暴露端口 `80`（映射到容器端口 `12434`）
- `PersistentVolumeClaim`：存储模型文件

`modelRunner.enabled` 设置还决定了 `model-runner-deployment` 的副本数量：

- 当为 `true` 时，部署副本数设置为 1，Docker Model Runner 部署在 Kubernetes 集群中。
- 当为 `false` 时，副本数为 0，不部署任何 Docker Model Runner 资源。