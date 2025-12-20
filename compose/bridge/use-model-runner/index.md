# 在 Compose Bridge 中使用 Docker Model Runner

Compose Bridge 支持模型感知部署。它可以部署和配置 Docker Model Runner，这是一个用于托管和服务机器 LLM 的轻量级服务。

这减少了启用 LLM 的服务的手动设置工作，并确保在 Docker Desktop 和 Kubernetes 环境之间保持一致的部署。

如果您的 `compose.yaml` 文件中包含顶级的 `models` 元素，Compose Bridge 将会：

- 为每个模型的端点和名称自动注入环境变量。
- 针对 Docker Desktop 和 Kubernetes 分别配置模型端点。
- 在 Helm 值中启用时，可选择性地在 Kubernetes 中部署 Docker Model Runner。

## 配置模型运行器设置

使用生成的 Helm Charts 进行部署时，您可以通过 Helm 值来控制模型运行器的配置。

```yaml
# Model Runner settings
modelRunner:
    # 对于 Docker Desktop 设置为 false（使用主机实例）
    # 对于独立的 Kubernetes 集群设置为 true
    enabled: false
    # 当 enabled=false 时使用的端点（Docker Desktop）
    hostEndpoint: "http://host.docker.internal:12434/engines/v1/"
    # 当 enabled=true 时的部署设置
    image: "docker/model-runner:latest"
    imagePullPolicy: "IfNotPresent"
    # GPU 支持
    gpu:
        enabled: false
        vendor: "nvidia" # nvidia 或 amd
        count: 1
    # 节点调度（根据需要取消注释并自定义）
    # nodeSelector:
    #   accelerator: nvidia-tesla-t4
    # tolerations: []
    # affinity: {}

    # 安全上下文
    securityContext:
        allowPrivilegeEscalation: false
    # 环境变量（根据需要取消注释并添加）
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
        storageClass: "" # 留空则使用默认存储类
    # 要预先拉取的模型
    models:
        - ai/qwen2.5:latest
        - ai/mxbai-embed-large
```

## 部署模型运行器

### Docker Desktop

当 `modelRunner.enabled` 为 `false` 时，Compose Bridge 会将您的工作负载配置为连接到主机上运行的 Docker Model Runner：

```text
http://host.docker.internal:12434/engines/v1/
```

该端点会自动注入到您的服务容器中。

### Kubernetes

当 `modelRunner.enabled` 为 `true` 时，Compose Bridge 使用生成的清单在您的集群中部署 Docker Model Runner，包括：

- Deployment：运行 `docker-model-runner` 容器
- Service：暴露端口 `80`（映射到容器端口 `12434`）
- `PersistentVolumeClaim`：存储模型文件

`modelRunner.enabled` 设置还决定了 `model-runner-deployment` 的副本数量：

- 当设置为 `true` 时，部署副本数设置为 1，并在 Kubernetes 集群中部署 Docker Model Runner。
- 当设置为 `false` 时，副本数为 0，且不会部署任何 Docker Model Runner 资源。
