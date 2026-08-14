---
title: 在 Red Hat OpenShift 上使用 Docker Hardened Images
description: 在 Red Hat OpenShift 容器平台上部署 Docker Hardened Images，涵盖安全上下文约束、任意用户 ID 分配、文件权限以及最佳实践。
summary: 学习如何在 Red Hat OpenShift 上部署 Docker Hardened Images（DHI），配置安全上下文约束（SCC），处理任意用户 ID 分配，并为运行时和开发镜像变体设置文件权限。
keywords: docker hardened images, dhi, openshift, OCP, SCC, security context constraints, non-root, distroless, containers, red hat
params:
  tags: [security]
  proficiencyLevel: Intermediate
  time: 30 minutes
  prerequisites:
    - 一个 OpenShift 集群（推荐 4.11 或更高版本）
    - 已认证到集群的 oc CLI
    - 有权访问 Docker Hardened Images 的 Docker Hub 账户
    - 熟悉 OpenShift 安全上下文约束（SCC）
---

Docker Hardened Images（DHI）可以部署在 Red Hat OpenShift 容器平台上，但 OpenShift 的安全模型与标准 Kubernetes 不同，需要特定的配置。由于 OpenShift 使用任意分配的用户 ID 来运行容器，而不是镜像的默认值，因此你必须在 Dockerfile 中调整文件归属和组权限，以确保可写路径保持可访问。

本指南介绍如何在 OpenShift 环境中部署 Docker Hardened Images，涵盖安全上下文约束（SCC）、任意用户 ID 分配、文件权限要求，以及针对运行时和开发镜像变体的最佳实践。

## OpenShift 安全与 Kubernetes 的区别

OpenShift 通过安全上下文约束（SCC）对 Kubernetes 进行了扩展，SCC 控制着一个 pod 可以执行的操作以及它可以访问的资源。虽然原生 Kubernetes 使用 Pod 安全标准的（PSS）来实现类似目的，但 SCC 更加细粒度，并且默认强制执行。

影响 DHI 部署的关键区别：

**任意用户 ID。** 默认情况下，OpenShift 使用从每个项目所分配范围内任意选取的用户 ID（UID）来运行容器。默认的 `restricted-v2` SCC（在 OpenShift 4.11 中引入）使用 `MustRunAsRange` 策略，它会用项目所分配范围内的一个 UID（通常从高于 1000000000 的值开始）覆盖容器镜像中的 `USER` 指令。这意味着即使 DHI 镜像指定了一个非 root 用户（UID 65532），OpenShift 仍会以一个不同的、不可预测的 UID 来运行该容器。

**root 组要求。** OpenShift 将该任意 UID 分配给 root 组（GID 0）。容器进程始终以 `gid=0(root)` 运行。该进程需要写入的任何目录或文件，必须由 root 组（GID 0）拥有，并具备组读/写权限。这在 [Red Hat 的镜像创建指南](https://docs.openshift.com/container-platform/4.14/openshift_images/create-images.html#use-uid_create-images) 中有说明。

> [!IMPORTANT]
>
> DHI 镜像默认将文件归属设置为 `nonroot:nonroot`（65532:65532）。由于 OpenShift 的任意 UID 不在 `nonroot` 组（65532）中，它无法写入这些文件——即使该 pod 已被 SCC 接纳且容器已启动。你必须将任何可写路径的组归属更改为 GID 0。这是在 OpenShift 上部署 DHI 时最常见的权限错误来源。

**能力限制。** `restricted-v2` SCC 默认丢弃所有 Linux 能力，并强制 `allowPrivilegeEscalation: false`、`runAsNonRoot: true` 以及类型为 `RuntimeDefault` 的 `seccompProfile`。DHI 运行时镜像已经满足这些约束，因为它们以非 root 用户运行，并且不需要提升的能力。

## 将 DHI 镜像拉取至 OpenShift

在部署之前，先创建一个镜像拉取密钥（image pull secret），使你的 OpenShift 集群能够向 DHI 镜像仓库或你在 Docker Hub 上镜像的仓库进行认证。

### 创建镜像拉取密钥

```console
oc create secret docker-registry dhi-pull-secret \
    --docker-server=docker.io \
    --docker-username=<your-docker-username> \
    --docker-password=<your-docker-access-token> \
    --docker-email=<your-email>
```

如果你是直接从 `dhi.io` 而非镜像仓库拉取，请将 `--docker-server=dhi.io` 设置为 `dhi.io`。

### 将密钥关联到服务账户

将拉取密钥关联到项目中的 `default` 服务账户，使所有部署都能自动拉取 DHI 镜像：

```console
oc secrets link default dhi-pull-secret --for=pull
```

若要改为将该密钥与特定服务账户一起使用：

```console
oc secrets link <service-account-name> dhi-pull-secret --for=pull
```

## 基于 DHI 构建 OpenShift 兼容的镜像

DHI 运行时镜像是 distroless 的——它们不包含 shell、包管理器，也不包含支持 `RUN` 命令的环境。这意味着你**不能在运行时阶段使用 `RUN` 命令**。所有针对 OpenShift 的文件权限调整必须在 `-dev` 构建阶段完成，并且结果必须使用 `COPY --chown` 复制到运行时阶段。

针对 OpenShift 兼容性的核心模式：

1. 使用 DHI `-dev` 变体作为构建阶段（它带有 shell）。
1. 构建你的应用，并在构建阶段设置 GID 0 归属。
1. 使用 `COPY --chown=<UID>:0` 将结果复制到 DHI 运行时镜像中。

### 示例：用于 OpenShift 的 Nginx

```dockerfile
# Build stage — has a shell, can run commands
FROM YOUR_ORG/dhi-nginx:1.29-alpine3.23-dev AS build

# Copy custom config and set root group ownership
COPY nginx.conf /tmp/nginx.conf
COPY default.conf /tmp/default.conf

# Prepare writable directories with GID 0
# (Nginx needs to write to cache, logs, and PID file locations)
RUN mkdir -p /tmp/nginx-cache /tmp/nginx-run && \
    chgrp -R 0 /tmp/nginx-cache /tmp/nginx-run && \
    chmod -R g=u /tmp/nginx-cache /tmp/nginx-run

# Runtime stage — distroless, NO shell, NO RUN commands
FROM YOUR_ORG/dhi-nginx:1.29-alpine3.23

COPY --from=build --chown=65532:0 /tmp/nginx.conf /etc/nginx/nginx.conf
COPY --from=build --chown=65532:0 /tmp/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build --chown=65532:0 /tmp/nginx-cache /var/cache/nginx
COPY --from=build --chown=65532:0 /tmp/nginx-run /var/run
```

> [!IMPORTANT]
>
> 将文件复制到运行时阶段时，始终使用 `--chown=<UID>:0`（user:root-group）。这确保 OpenShift 分配的任意 UID 能够通过 root 组归属访问这些文件。绝不要在运行时阶段使用 `RUN`——distroless DHI 镜像没有 shell。

> [!NOTE]
>
> DHI 镜像的 UID 因镜像而异。大多数使用 65532（`nonroot`），但有些（如 Node.js 镜像）可能使用不同的 UID。请通过以下命令核实：
> `docker inspect dhi.io/<image>:<tag> --format '{{.Config.User}}'`

部署到 OpenShift：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-dhi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-dhi
  template:
    metadata:
      labels:
        app: nginx-dhi
    spec:
      containers:
        - name: nginx
          image: YOUR_ORG/dhi-nginx:1.29-alpine3.23
          ports:
            - containerPort: 8080
          securityContext:
            allowPrivilegeEscalation: false
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
            capabilities:
              drop:
                - ALL
      imagePullSecrets:
        - name: dhi-pull-secret
```

DHI Nginx 默认监听 8080 端口（而非 80），这与非 root 要求兼容。无需更改 SCC。

### 示例：用于 OpenShift 的 Node.js 应用

```dockerfile
# Build stage — dev variant has shell and npm
FROM YOUR_ORG/dhi-node:24-alpine3.23-dev AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Set GID 0 on everything the runtime needs to write
RUN chgrp -R 0 /app/dist /app/node_modules && \
    chmod -R g=u /app/dist /app/node_modules

# Runtime stage — distroless, NO shell
FROM YOUR_ORG/dhi-node:24-alpine3.23
WORKDIR /app
COPY --from=build --chown=65532:0 /app/dist ./dist
COPY --from=build --chown=65532:0 /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

部署：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: node-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: node-app
  template:
    metadata:
      labels:
        app: node-app
    spec:
      containers:
        - name: app
          image: YOUR_ORG/dhi-node-app:latest
          ports:
            - containerPort: 3000
          securityContext:
            allowPrivilegeEscalation: false
            runAsNonRoot: true
            seccompProfile:
              type: RuntimeDefault
            capabilities:
              drop:
                - ALL
      imagePullSecrets:
        - name: dhi-pull-secret
```

## 处理任意用户 ID

OpenShift 的 `restricted-v2` SCC 为容器进程分配一个随机 UID。该 UID 不会存在于镜像内部的 `/etc/passwd` 中，但容器仍会运行——只是该进程没有与之关联的用户名。

这可能导致以下几类应用出现问题：

- 查找当前用户的主目录或用户名
- 写入由特定 UID 拥有的目录
- 检查 `/etc/passwd` 中是否存在运行中的用户

### 为任意 UID 添加 `passwd` 条目

某些应用（尤其是那些使用特定 Python 或 Java 库的应用）要求运行用户拥有一条有效的 `/etc/passwd` 条目。你可以通过一个包装入口点脚本来处理这个问题。

由于该模式需要 shell，它仅适用于 DHI `-dev` 变体，或适用于包含 shell 的 DHI Enterprise 定制镜像。请在构建阶段准备镜像：

```dockerfile
FROM YOUR_ORG/dhi-python:3.13-alpine3.23-dev AS build
# ... build your application ...

# Make /etc/passwd group-writable so the entrypoint can append to it
RUN chgrp 0 /etc/passwd && chmod g=u /etc/passwd

# Create the entrypoint wrapper
RUN printf '#!/bin/sh\n\
if ! whoami > /dev/null 2>&1; then\n\
  if [ -w /etc/passwd ]; then\n\
    echo "${USER_NAME:-appuser}:x:$(id -u):0:dynamic user:/tmp:/sbin/nologin" >> /etc/passwd\n\
  fi\n\
fi\n\
exec "$@"\n' > /entrypoint.sh && chmod +x /entrypoint.sh

# This pattern requires a -dev variant as runtime (has shell)
FROM YOUR_ORG/dhi-python:3.13-alpine3.23-dev
COPY --from=build --chown=65532:0 /app ./app
COPY --from=build --chown=65532:0 /entrypoint.sh /entrypoint.sh
COPY --from=build --chown=65532:0 /etc/passwd /etc/passwd
USER 65532
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app/main.py"]
```

> [!NOTE]
>
> 对于 distroless 运行时镜像（没有 shell），passwd 注入模式是不可能的。相反，请使用 `nonroot` SCC（在下一节中描述）以镜像内置的 UID 运行，这样现有的 `/etc/passwd` 条目就能与运行中的进程相匹配。或者，在大多数情况下，OpenShift 4.x 会自动将该任意 UID 注入到 `/etc/passwd` 中，这为许多应用解决了该问题。

## 使用 non-root SCC 固定 UID

如果你的应用需要以镜像中定义的特定 UID（对于 DHI 通常为 65532）运行，可以使用 `nonroot` SCC 来替代默认的 `restricted-v2`。`nonroot` SCC 使用 `MustRunAsNonRoot` 策略，允许任何非零 UID。

> [!IMPORTANT]
>
> 要使 `nonroot` SCC 生效，镜像的 `USER` 指令必须指定一个**数字** UID（例如 `65532`），而不是像 `nonroot` 这样的用户名字符串。OpenShift 无法验证一个用户名是否映射到非零 UID。请通过以下命令核实你的 DHI 镜像：
> `docker inspect YOUR_ORG/dhi-node:24-alpine3.23 --format '{{.Config.User}}'`
> 如果输出是字符串而非数字，请在 pod spec 中显式设置 `runAsUser`。

创建一个服务账户并授予它 `nonroot` SCC：

```console
oc create serviceaccount dhi-nonroot
oc adm policy add-scc-to-user nonroot -z dhi-nonroot
```

在部署中引用该服务账户：

```yaml
spec:
  template:
    spec:
      serviceAccountName: dhi-nonroot
      containers:
        - name: app
          image: YOUR_ORG/dhi-node:24-alpine3.23
          securityContext:
            runAsUser: 65532
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            seccompProfile:
              type: RuntimeDefault
            capabilities:
              drop:
                - ALL
```

部署后核实 SCC 分配情况：

```console
oc get pod <pod-name> -o jsonpath='{.metadata.annotations.openshift\.io/scc}'
```

这应当返回 `nonroot`。

使用带有固定 UID 的 `nonroot` SCC 时，进程以 65532 运行（与镜像的文件归属相匹配），因此对于已经由 65532 拥有的路径，GID 0 调整并非严格要求。不过，为了同时兼容 `restricted-v2` 和 `nonroot` 这两种 SCC，仍然建议应用 `chown <UID>:0`。

## 在 OpenShift 中使用 DHI dev 变体

DHI `-dev` 变体包含 shell、包管理器和开发工具。它们默认以 root（UID 0）运行，这与 OpenShift 的 `restricted-v2` SCC 相冲突。有三种应对方法：

### 方案 1：仅在构建阶段使用 dev 变体（推荐）

仅在 Dockerfile 构建阶段使用 `-dev` 变体，绝不直接将它们部署到 OpenShift：

```dockerfile
FROM YOUR_ORG/dhi-node:24-alpine3.23-dev AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Set root group ownership for OpenShift compatibility
RUN chgrp -R 0 /app/dist /app/node_modules && \
    chmod -R g=u /app/dist /app/node_modules

FROM YOUR_ORG/dhi-node:24-alpine3.23
WORKDIR /app
COPY --from=build --chown=65532:0 /app/dist ./dist
COPY --from=build --chown=65532:0 /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

最终的运行时镜像是非 root 且 distroless 的，完全兼容 `restricted-v2`。

### 方案 2：授予 `anyuid` SCC 用于调试

如果你需要在 OpenShift 中直接运行 `-dev` 变体进行调试，请将 `anyuid` SCC 授予一个专用的服务账户：

```console
oc create serviceaccount dhi-debug
oc adm policy add-scc-to-user anyuid -z dhi-debug
```

然后在你的 pod 中引用它：

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dhi-debug
spec:
  serviceAccountName: dhi-debug
  containers:
    - name: debug
      image: YOUR_ORG/dhi-node:24-alpine3.23-dev
      command: ["sleep", "infinity"]
  imagePullSecrets:
    - name: dhi-pull-secret
```

> [!IMPORTANT]
>
> `anyuid` SCC 允许以包括 root 在内的任意 UID 运行。仅将其用于临时调试——绝不要用于生产工作负载。

### 方案 3：使用 `oc debug` 或临时容器

对于没有 shell 的 distroless 运行时镜像，请使用 OpenShift 原生的调试工具，而非 `docker debug`（后者仅适用于 Docker Engine，不适用于 OpenShift 上的 CRI-O）。

使用 `oc debug` 创建一个带有调试 shell 的 pod 副本：

```console
# Create a debug pod based on a deployment
oc debug deployment/nginx-dhi

# Override the image to use a -dev variant with a shell
oc debug deployment/nginx-dhi --image=YOUR_ORG/dhi-node:24-alpine3.23-dev
```

使用临时容器（OpenShift 4.12+ / Kubernetes 1.25+）：

```console
kubectl debug -it <pod-name> --image=YOUR_ORG/dhi-node:24-alpine3.23-dev \
    --target=app -- sh
```

这会将一个临时调试容器附加到正在运行的 pod 上，而不会重启它，并共享该 pod 的进程命名空间。

> [!NOTE]
>
> `docker debug` 是面向本地开发的 Docker Desktop/CLI 功能。它在 OpenShift 集群上不可用，因为 OpenShift 使用 CRI-O 作为其容器运行时。

## 在 OpenShift 上部署 DHI Helm 图表

DHI 为流行应用提供了预配置的 Helm 图表。在 OpenShift 上部署这些图表时，你可能需要调整安全上下文设置。

### 先检查图表 values

在安装之前，先检查该图表暴露了哪些安全上下文 values：

```console
helm registry login dhi.io

helm show values oci://dhi.io/<chart-name> --version <version> | grep -A 20 securityContext
```

可用的 value 路径因图表而异，因此在设置覆盖项之前，请始终检查 `values.yaml`。

### 使用 OpenShift 覆盖项进行安装

以下示例展示了一个典型的安装模式。请根据 `helm show values` 针对你的特定图表返回的结果来调整 `--set` 路径：

```console
helm install my-release oci://dhi.io/<chart-name> \
    --version <version> \
    --set "imagePullSecrets[0].name=dhi-pull-secret" \
    -f openshift-values.yaml
```

创建一个 `openshift-values.yaml`，其中包含适合你图表的、与安全上下文相关的覆盖项：

```yaml
# Example — adjust keys based on `helm show values` output
podSecurityContext:
  runAsNonRoot: true
  seccompProfile:
    type: RuntimeDefault

securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

> [!NOTE]
>
> DHI Helm 图表的 value 路径在各图表之间并不统一。例如，某个图表可能使用 `image.imagePullSecrets`，而另一个则使用 `global.imagePullSecrets`。请始终查阅特定图表的文档或 `values.yaml`。

## 验证你的部署

将 DHI 镜像部署到 OpenShift 之后，验证其安全配置。

### 检查已分配的 SCC

```console
oc get pods -o 'custom-columns=NAME:.metadata.name,SCC:.metadata.annotations.openshift\.io/scc'
```

运行时 DHI 镜像应显示 `restricted-v2`（如果你配置过，则为 `nonroot`）。

### 检查运行中的 UID

```console
oc exec <pod-name> -- id
```

在 `restricted-v2` SCC 下，你应当看到类似以下的输出：

```text
uid=1000650000 gid=0(root) groups=0(root),1000650000
```

该 UID 来自项目所分配的范围，并且主 GID 始终为 0（root 组）。在使用 `nonroot` SCC 且 `runAsUser: 65532` 的情况下，你会看到 `uid=65532`。

### 确认镜像为 distroless

```console
oc exec <pod-name> -- sh -c "echo hello"
```

对于运行时（非 dev）DHI 镜像，该命令应当失败，并提示在 `$PATH` 中找不到 `sh`。确切的错误格式在不同 CRI-O 版本之间有所差异。

### 扫描已部署的镜像

使用 Docker Scout 来验证已部署镜像的安全态势（从你的本地机器运行，而非在集群上运行）：

```console
docker scout cves YOUR_ORG/dhi-nginx:1.29-alpine3.23
docker scout quickview YOUR_ORG/dhi-nginx:1.29-alpine3.23
```

## 常见问题与解决方案

**Pod 启动失败，提示 “container has runAsNonRoot and image has group or user ID set to root.”** 这通常发生在使用默认的 `restricted-v2` SCC 部署 DHI `-dev` 变体时。请改用运行时变体，或者将 `anyuid` SCC 授予该服务账户。

**应用无法写入某个目录。** OpenShift 分配的任意 UID 没有写入权限。这是 DHI 在 OpenShift 上最常见的问题。所有可写路径必须由 GID 0 拥有，并具备组写权限。请在构建阶段修复此问题：
`chgrp -R 0 /path && chmod -R g=u /path`，然后使用 `COPY --chown=<UID>:0` 复制到运行时阶段。

**应用失败，提示 “user not found” 或 “no matching entries in passwd file.”** 某些应用需要一条有效的 `/etc/passwd` 条目。在大多数情况下，OpenShift 4.x 会自动将该任意 UID 注入到 `/etc/passwd` 中。如果你的应用仍然失败，请使用 passwd 注入模式（需要一个 `-dev` 变体），或者使用 `nonroot` SCC 以镜像内置的 UID 运行。

**Pod 无法绑定到 80 或 443 端口。** 低于 1024 的端口需要 root 权限。DHI 镜像默认使用非特权端口（例如 Nginx 使用 8080）。请将你的 OpenShift Service 配置为将外部端口映射到容器的非特权端口：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-dhi
spec:
  ports:
    - port: 80
      targetPort: 8080
  selector:
    app: nginx-dhi
```

**ImagePullBackOff，提示 “unauthorized: authentication required.”** 请核实拉取密钥配置正确，并且已关联到服务账户。使用 `oc get secret dhi-pull-secret` 和 `oc describe sa default` 进行检查。

**Dockerfile 构建失败，运行时阶段提示 “exec: not found”。** 你正在 distroless 运行时阶段使用 `RUN`。DHI 运行时镜像没有 shell，因此 `RUN` 命令无法执行。请将所有 `RUN` 命令移到 `-dev` 构建阶段，并使用 `COPY --chown` 来传递结果。

## DHI 与 OpenShift 兼容性总结

|特性                         |DHI 运行时                       |DHI `-dev`           |DHI 配合 Enterprise 定制        |
|-----------------------------|---------------------------------|--------------------|---------------------------------|
|默认 SCC（`restricted-v2`） |是，需配合 GID 0 权限           |需要 `anyuid`       |是，需配合 GID 0 权限           |
|默认非 root                 |是（UID 65532）                 |否（root）          |是（可配置 UID）                |
|任意 UID 支持               |是，需配合 `chown <UID>:0`      |是                  |是，需配合 `chown <UID>:0`      |
|Distroless（无 shell）      |是——Dockerfile 中无 `RUN`       |否                  |是——Dockerfile 中无 `RUN`       |
|非特权端口                  |是（高于 1024）                 |可配置              |是（高于 1024）                 |
|SLSA Build Level 3          |是                               |是                  |是                              |
|集群内调试                  |`oc debug` / 临时容器            |`oc exec`（含 shell）|`oc debug` / 临时容器            |

## 后续步骤

- [在 Kubernetes 中使用镜像](/dhi/how-to/k8s/) — 通用的 DHI Kubernetes 部署指南。
- [定制镜像](/dhi/how-to/customize/) — 使用 Enterprise 定制向 DHI 镜像添加包。
- [调试容器](/dhi/how-to/troubleshoot/#general-debugging) — 使用 Docker Debug（本地开发）排查 distroless 容器。
- [管理 SCC](https://docs.openshift.com/container-platform/4.14/authentication/managing-security-context-constraints.html) — Red Hat 关于安全上下文约束的参考文档。
- [为 OpenShift 创建镜像](https://docs.openshift.com/container-platform/4.14/openshift_images/create-images.html) — Red Hat 关于构建 OpenShift 兼容容器镜像的指南。
