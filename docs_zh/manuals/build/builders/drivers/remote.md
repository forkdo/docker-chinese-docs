---
title: 远程驱动
description: |
  远程驱动让你连接到由你自己手动设置和配置的远程 BuildKit 实例。
keywords: build, buildx, driver, builder, remote
aliases:
  - /build/buildx/drivers/remote/
  - /build/building/drivers/remote/
  - /build/drivers/remote/
---

Buildx 远程驱动支持更复杂的自定义构建工作负载，让你可以连接到外部管理的 BuildKit 实例。这对于需要手动管理 BuildKit 守护进程，或 BuildKit 守护进程由其他来源暴露的场景很有用。

## 概要（Synopsis）

```console
$ docker buildx create \
  --name remote \
  --driver remote \
  tcp://localhost:1234
```

下表描述了你可以传递给 `--driver-opt` 的可用驱动专属选项：

| Parameter      | Type    | Default            | Description                                                            |
| -------------- | ------- | ------------------ | ---------------------------------------------------------------------- |
| `key`          | String  |                    | 设置 TLS 客户端密钥。                                                  |
| `cert`         | String  |                    | 要提供给 `buildkitd` 的 TLS 客户端证书的绝对路径。                     |
| `cacert`       | String  |                    | 用于验证的 TLS 证书颁发机构（CA）的绝对路径。                          |
| `servername`   | String  | 端点的主机名。     | 请求中使用的 TLS 服务器名称。                                          |
| `default-load` | Boolean | `false`            | 自动将镜像加载到 Docker Engine 镜像存储。                             |

## 示例：通过 Unix 套接字的远程 BuildKit（Example: Remote BuildKit over Unix sockets）

本指南展示了如何创建一个 BuildKit 守护进程监听 Unix 套接字，并让 Buildx 通过它连接的设置。

1. 确保已安装 [BuildKit](https://github.com/moby/buildkit)。

   例如，你可以用以下命令启动一个 buildkitd 实例：

   ```console
   $ sudo ./buildkitd --group $(id -gn) --addr unix://$HOME/buildkitd.sock
   ```

   或者，请参阅 [Rootless Buildkit 文档](https://github.com/moby/buildkit/blob/master/docs/rootless.md)
   以 rootless 模式运行 buildkitd，或参阅 [BuildKit systemd 示例](https://github.com/moby/buildkit/tree/master/examples/systemd)
   以 systemd 服务方式运行它。

2. 检查你有一个可以连接的 Unix 套接字。

   ```console
   $ ls -lh /home/user/buildkitd.sock
   srw-rw---- 1 root user 0 May  5 11:04 /home/user/buildkitd.sock
   ```

3. 使用远程驱动将 Buildx 连接到它：

   ```console
   $ docker buildx create \
     --name remote-unix \
     --driver remote \
     unix://$HOME/buildkitd.sock
   ```

4. 使用 `docker buildx ls` 列出可用的 builder。然后你应该会看到
   `remote-unix` 位列其中：

   ```console
   $ docker buildx ls
   NAME/NODE           DRIVER/ENDPOINT                        STATUS  PLATFORMS
   remote-unix         remote
     remote-unix0      unix:///home/.../buildkitd.sock        running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
   default *           docker
     default           default                                running linux/amd64, linux/386
   ```

你可以使用 `docker buildx use remote-unix` 将此新 builder 切换为默认，或者在每次构建时使用 `--builder` 指定它：

```console
$ docker buildx build --builder=remote-unix -t test --load .
```

请记住，如果你想将构建结果加载到 Docker 守护进程中，需要使用 `--load` 标志。

## 示例：Docker 容器中的远程 BuildKit（Example: Remote BuildKit in Docker container）

本指南将向你展示如何创建类似于 `docker-container` 驱动的设置，方法是手动启动一个 BuildKit Docker 容器，并使用 Buildx 远程驱动连接到它。此过程将手动创建一个容器并通过其暴露的端口访问它。（你可能直接使用通过 Docker 守护进程连接 BuildKit 的 `docker-container` 驱动会更好，但这里仅用于说明目的。）

1.  为 BuildKit 生成证书。

    你可以使用这个 [bake 定义](https://github.com/moby/buildkit/blob/master/examples/create-certs)
    作为起点：

    ```console
    SAN="localhost 127.0.0.1" docker buildx bake "https://github.com/moby/buildkit.git#master:examples/create-certs"
    ```

    请注意，虽然可以在不使用 TLS 的情况下通过 TCP 暴露 BuildKit，但不建议这样做。这样做会允许在没有任何凭据的情况下任意访问 BuildKit。

2.  在 `.certs/` 中生成证书后，启动容器：

    ```console
    $ docker run -d --rm \
      --name=remote-buildkitd \
      --privileged \
      -p 1234:1234 \
      -v $PWD/.certs:/etc/buildkit/certs \
      moby/buildkit:latest \
      --addr tcp://0.0.0.0:1234 \
      --tlscacert /etc/buildkit/certs/daemon/ca.pem \
      --tlscert /etc/buildkit/certs/daemon/cert.pem \
      --tlskey /etc/buildkit/certs/daemon/key.pem
    ```

    此命令会启动一个 BuildKit 容器，并将守护进程的 1234 端口暴露给 localhost。

3.  使用 Buildx 连接到这个正在运行的容器：

    ```console
    $ docker buildx create \
      --name remote-container \
      --driver remote \
      --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem,servername=<TLS_SERVER_NAME> \
      tcp://localhost:1234
    ```

    或者，使用 `docker-container://` URL 方案在不需要指定端口的情况下连接到 BuildKit 容器：

    ```console
    $ docker buildx create \
      --name remote-container \
      --driver remote \
      docker-container://remote-container
    ```

## 示例：Kubernetes 中的远程 BuildKit（Example: Remote BuildKit in Kubernetes）

本指南将向你展示如何创建类似于 `kubernetes` 驱动的设置，方法是手动创建一个 BuildKit `Deployment`。虽然 `kubernetes` 驱动会在底层执行此操作，但有时手动扩展 BuildKit 是可取的。此外，当从 Kubernetes Pod 内部执行构建时，Buildx builder 需要在每个 Pod 中重新创建或在它们之间复制。

1. 按照 [BuildKit 文档](https://github.com/moby/buildkit/tree/master/examples/kubernetes) 中的说明创建一个 `buildkitd` 的 Kubernetes 部署。

   使用 [create-certs.sh](https://github.com/moby/buildkit/blob/master/examples/kubernetes/create-certs.sh)
   脚本为 BuildKit 守护进程和客户端创建证书，并创建一个连接它们的、带有 Service 的 BuildKit Pod 部署。

2. 假设该 Service 名为 `buildkitd`，在 Buildx 中创建一个远程 builder，确保所列的证书文件存在：

   ```console
   $ docker buildx create \
     --name remote-kubernetes \
     --driver remote \
     --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem \
     tcp://buildkitd.default.svc:1234
   ```

请注意，这仅在集群内部有效，因为 BuildKit 设置指南只创建了一个 `ClusterIP` Service。要远程访问 builder，你可以设置并使用 ingress，但这超出了本指南的范围。

### 在 Kubernetes 中调试远程 builder（Debug a remote builder in Kubernetes）

如果你在访问部署在 Kubernetes 中的远程 builder 时遇到问题，可以使用 `kube-pod://` URL 方案通过 Kubernetes API 直接连接到某个 BuildKit Pod。请注意，此方法只连接到部署中的单个 Pod。

```console
$ kubectl get pods --selector=app=buildkitd -o json | jq -r '.items[].metadata.name'
buildkitd-XXXXXXXXXX-xxxxx
$ docker buildx create \
  --name remote-container \
  --driver remote \
  kube-pod://buildkitd-XXXXXXXXXX-xxxxx
```

或者，使用 `kubectl` 的端口转发机制：

```console
$ kubectl port-forward svc/buildkitd 1234:1234
```

然后你可以将远程驱动指向 `tcp://localhost:1234`。
