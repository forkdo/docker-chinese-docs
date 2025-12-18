---
title: 部署与编排
keywords: 编排, 部署, kubernetes, swarm,
description: 了解 Docker 的一些基础知识并安装 Docker Desktop。
aliases:
  - /get-started/orchestration/
  - /guides/deployment-orchestration/orchestration/
summary: |
  探索使用 Docker 进行容器编排的基础知识。
tags: [deploy]
params:
  time: 10 分钟
---

容器化技术使应用程序能够迁移到云环境和数据中心，并具备良好的可扩展性。容器有效地保证了应用程序在任何环境中都能以相同的方式运行，让你能够快速、轻松地充分利用所有这些环境。此外，当你的应用程序规模扩大时，你需要一些工具来帮助自动化维护这些应用程序，自动替换失败的容器，并在容器的生命周期内管理更新和重新配置的发布。

用于管理、扩展和维护容器化应用程序的工具被称为编排器（orchestrator）。目前最流行的两种编排工具是 Kubernetes 和 Docker Swarm。Docker Desktop 为这两种编排器提供了开发环境。

高级模块将教你如何：

1. [在开发机器上设置和使用 Kubernetes 环境](kube-deploy.md)
2. [在开发机器上设置和使用 Swarm 环境](swarm-deploy.md)

## 启用 Kubernetes

Docker Desktop 可以快速、轻松地为你设置 Kubernetes。请按照适合你操作系统的设置和验证说明进行操作：

{{< tabs group="os" >}}
{{< tab name="Mac 和 Linux" >}}

### Mac

1.  在 Docker Dashboard 中，导航到 **Settings**（设置），并选择 **Kubernetes**（Kubernetes）选项卡。

2.  勾选 **Enable Kubernetes**（启用 Kubernetes）复选框，然后选择 **Apply**（应用）。Docker Desktop 会自动为你设置 Kubernetes。当在 **Settings**（设置）中看到“Kubernetes _running_”旁边显示绿灯时，说明 Kubernetes 已成功启用。

3.  要确认 Kubernetes 已启动并运行，请创建一个名为 `pod.yaml` 的文本文件，内容如下：

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: demo
    spec:
      containers:
        - name: testpod
          image: alpine:latest
          command: ["ping", "8.8.8.8"]
    ```

    这描述了一个包含单个容器的 Pod，隔离了一个简单的 ping 8.8.8.8 操作。

4.  在终端中，导航到创建 `pod.yaml` 的目录，然后创建你的 Pod：

    ```console
    $ kubectl apply -f pod.yaml
    ```

5.  检查你的 Pod 是否已启动并运行：

    ```console
    $ kubectl get pods
    ```

    你应该看到类似以下内容：

    ```shell
    NAME      READY     STATUS    RESTARTS   AGE
    demo      1/1       Running   0          4s
    ```

6.  检查你是否获得了 ping 进程预期的日志：

    ```console
    $ kubectl logs demo
    ```

    你应该看到健康 ping 进程的输出：

    ```shell
    PING 8.8.8.8 (8.8.8.8): 56 data bytes
    64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
    64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
    64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
    ...
    ```

7.  最后，拆除你的测试 Pod：

    ```console
    $ kubectl delete -f pod.yaml
    ```

{{< /tab >}}
{{< tab name="Windows" >}}

### Windows

1. 在 Docker Dashboard 中，导航到 **Settings**（设置），并选择 **Kubernetes**（Kubernetes）选项卡。

2. 勾选 **Enable Kubernetes**（启用 Kubernetes）复选框，然后选择 **Apply**（应用）。Docker Desktop 会自动为你设置 Kubernetes。当在 **Settings**（设置）菜单中看到“Kubernetes _running_”旁边显示绿灯时，说明 Kubernetes 已成功启用。

3. 要确认 Kubernetes 已启动并运行，请创建一个名为 `pod.yaml` 的文本文件，内容如下：

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: demo
   spec:
     containers:
       - name: testpod
         image: alpine:latest
         command: ["ping", "8.8.8.8"]
   ```

   这描述了一个包含单个容器的 Pod，隔离了一个简单的 ping 8.8.8.8 操作。

4. 在 PowerShell 中，导航到创建 `pod.yaml` 的目录，然后创建你的 Pod：

   ```console
   $ kubectl apply -f pod.yaml
   ```

5. 检查你的 Pod 是否已启动并运行：

   ```console
   $ kubectl get pods
   ```

   你应该看到类似以下内容：

   ```shell
   NAME      READY     STATUS    RESTARTS   AGE
   demo      1/1       Running   0          4s
   ```

6. 检查你是否获得了 ping 进程预期的日志：

   ```console
   $ kubectl logs demo
   ```

   你应该看到健康 ping 进程的输出：

   ```shell
   PING 8.8.8.8 (8.8.8.8): 56 data bytes
   64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
   64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
   64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
   ...
   ```

7. 最后，拆除你的测试 Pod：

   ```console
   $ kubectl delete -f pod.yaml
   ```

{{< /tab >}}
{{< /tabs >}}

## 启用 Docker Swarm

Docker Desktop 主要运行在 Docker Engine 上，Docker Engine 内置了运行 Swarm 所需的所有功能。请按照适合你操作系统的设置和验证说明进行操作：

{{< tabs group="os" >}}
{{< tab name="Mac" >}}

### Mac

1. 打开终端，初始化 Docker Swarm 模式：

   ```console
   $ docker swarm init
   ```

   如果一切顺利，你应该看到类似以下的消息：

   ```shell
   Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.

   To add a worker to this swarm, run the following command:

       docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377

   To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
   ```

2. 运行一个简单的 Docker 服务，使用基于 alpine 的文件系统，并隔离一个 ping 8.8.8.8 操作：

   ```console
   $ docker service create --name demo alpine:latest ping 8.8.8.8
   ```

3. 检查你的服务是否创建了一个正在运行的容器：

   ```console
   $ docker service ps demo
   ```

   你应该看到类似以下内容：

   ```shell
   ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
   463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
   ```

4. 检查你是否获得了 ping 进程预期的日志：

   ```console
   $ docker service logs demo
   ```

   你应该看到健康 ping 进程的输出：

   ```shell
   demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
   ...
   ```

5. 最后，拆除你的测试服务：

   ```console
   $ docker service rm demo
   ```

{{< /tab >}}
{{< tab name="Windows" >}}

### Windows

1. 打开 PowerShell，初始化 Docker Swarm 模式：

   ```console
   $ docker swarm init
   ```

   如果一切顺利，你应该看到类似以下的消息：

   ```shell
   Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.

   To add a worker to this swarm, run the following command:

       docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377

   To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
   ```

2. 运行一个简单的 Docker 服务，使用基于 alpine 的文件系统，并隔离一个 ping 8.8.8.8 操作：

   ```console
   $ docker service create --name demo alpine:latest ping 8.8.8.8
   ```

3. 检查你的服务是否创建了一个正在运行的容器：

   ```console
   $ docker service ps demo
   ```

   你应该看到类似以下内容：

   ```shell
   ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
   463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
   ```

4. 检查你是否获得了 ping 进程预期的日志：

   ```console
   $ docker service logs demo
   ```

   你应该看到健康 ping 进程的输出：

   ```shell
   demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
   ...
   ```

5. 最后，拆除你的测试服务：

   ```console
   $ docker service rm demo
   ```

{{< /tab >}}
{{< /tabs >}}

## 总结

至此，你已经确认可以在 Kubernetes 和 Swarm 中运行简单的容器化工作负载。下一步是编写 YAML 文件来描述如何运行和管理这些容器。

- [部署到 Kubernetes](kube-deploy.md)
- [部署到 Swarm](swarm-deploy.md)

## CLI 参考

本文中使用的所有 CLI 命令的进一步文档可在此处找到：

- [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
- [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)
- [`kubectl logs`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
- [`kubectl delete`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)
- [`docker swarm init`](/reference/cli/docker/swarm/init/)
- [`docker service *`](/reference/cli/docker/service/)