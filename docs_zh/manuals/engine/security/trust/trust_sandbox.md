---
description: 在信任沙箱中操作
keywords: 信任, 安全, root, 密钥, 仓库, 沙箱
title: 在内容信任沙箱中操作
aliases:
- /security/trust/trust_sandbox/
---

本文档说明如何设置和使用一个用于信任实验的沙箱。该沙箱允许您在本地配置和尝试信任操作，而不会影响您的生产镜像。

在操作此沙箱之前，您应该已经阅读过[信任概述](index.md)。

## 前置条件

这些说明假设您正在 Linux 或 macOS 上运行。您可以在本地机器或虚拟机上运行此沙箱。您需要具有在本地机器或虚拟机上运行 Docker 命令的权限。

此沙箱需要您安装两个 Docker 工具：Docker Engine >= 1.10.0 和 Docker Compose >= 1.6.0。要安装 Docker Engine，请从[支持的平台列表](../../install/_index.md)中选择。要安装 Docker Compose，请参阅[此处的详细说明](/manuals/compose/install/_index.md)。

## 沙箱包含什么？

如果您仅使用开箱即用的信任功能，您只需要 Docker Engine 客户端和对 Docker Hub 的访问权限。沙箱模拟了一个生产信任环境，并设置了以下附加组件。

| 容器       | 描述                                                                                                                                 |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| trustsandbox    | 一个包含最新版本 Docker Engine 和一些预配置证书的容器。这是您的沙箱，您可以在其中使用 `docker` 客户端测试信任操作。 |
| Registry server | 一个本地注册表服务。                                                                                                                 |
| Notary server   | 执行所有信任管理繁重工作的服务                                                                               |

这意味着您运行自己的内容信任（Notary）服务器和注册表。如果您仅与 Docker Hub 一起工作，您就不需要这些组件。它们已经内置到 Docker Hub 中供您使用。但是对于沙箱，您构建了自己的完整模拟生产环境。

在 `trustsandbox` 容器内，您与本地注册表交互，而不是与 Docker Hub 交互。这意味着您日常使用的镜像仓库不会被使用。它们在您玩耍时受到保护。

当您在沙箱中玩耍时，您还会创建 root 和仓库密钥。沙箱配置为将所有密钥和文件存储在 `trustsandbox` 容器内。由于您在沙箱中创建的密钥仅用于娱乐，销毁容器也会销毁它们。

通过为 `trustsandbox` 容器使用 `docker-in-docker` 镜像，您也不会用推送和拉取的镜像污染您真正的 Docker 守护进程缓存。镜像存储在附加到此容器的匿名卷中，可以在销毁容器后删除。

## 构建沙箱

在本节中，您将使用 Docker Compose 来指定如何设置和链接 `trustsandbox` 容器、Notary 服务器和 Registry 服务器。

1. 创建一个新的 `trustsandbox` 目录并进入该目录。

   ```console
   $ mkdir trustsandbox
   $ cd trustsandbox
   ```

2. 使用您喜欢的编辑器创建一个名为 `compose.yaml` 的文件。例如，使用 vim：

   ```console
   $ touch compose.yaml
   $ vim compose.yaml
   ```

3. 将以下内容添加到新文件中。

   ```yaml
   version: "2"
   services:
     notaryserver:
       image: dockersecurity/notary_autobuilds:server-v0.5.1
       volumes:
         - notarycerts:/var/lib/notary/fixtures
       networks:
         - sandbox
       environment:
         - NOTARY_SERVER_STORAGE_TYPE=memory
         - NOTARY_SERVER_TRUST_SERVICE_TYPE=local
     sandboxregistry:
       image: registry:3
       networks:
         - sandbox
       container_name: sandboxregistry
     trustsandbox:
       image: docker:dind
       networks:
         - sandbox
       volumes:
         - notarycerts:/notarycerts
       privileged: true
       container_name: trustsandbox
       entrypoint: ""
       command: |-
           sh -c '
               cp /notarycerts/root-ca.crt /usr/local/share/ca-certificates/root-ca.crt &&
               update-ca-certificates &&
               dockerd-entrypoint.sh --insecure-registry sandboxregistry:5000'
   volumes:
     notarycerts:
       external: false
   networks:
     sandbox:
       external: false
   ```

4. 保存并关闭文件。

5. 在您的本地系统上运行容器。

   ```console
   $ docker compose up -d
   ```

   第一次运行时，`docker-in-docker`、Notary 服务器和注册表镜像将从 Docker Hub 下载。

## 在沙箱中玩耍

现在一切已设置好，您可以进入 `trustsandbox` 容器并开始测试 Docker 内容信任。从您的主机上，获取 `trustsandbox` 容器的 shell。

```console
$ docker container exec -it trustsandbox sh
/ #
```

### 测试一些信任操作

现在，从 `trustsandbox` 容器内下载一些镜像。

1. 下载一个 `docker` 镜像进行测试。

   ```console
   / # docker pull docker/trusttest
   docker pull docker/trusttest
   Using default tag: latest
   latest: Pulling from docker/trusttest   
   b3dbab3810fc: Pull complete
   a9539b34a6ab: Pull complete
   Digest: sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a
   Status: Downloaded newer image for docker/trusttest:latest
   ```

2. 标记它以便推送到您的沙箱注册表：

   ```console
   / # docker tag docker/trusttest sandboxregistry:5000/test/trusttest:latest
   ```

3. 启用内容信任。

   ```console
   / # export DOCKER_CONTENT_TRUST=1
   ```

4. 识别信任服务器。

   ```console
   / # export DOCKER_CONTENT_TRUST_SERVER=https://notaryserver:4443
   ```

    此步骤仅在沙箱使用自己的服务器时是必要的。通常，如果您使用 Docker 公共中心，则不需要此步骤。

5. 拉取测试镜像。

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Error: remote trust data does not exist for sandboxregistry:5000/test/trusttest: notaryserver:4443 does not have trust data for      sandboxregistry:5000/test/trusttest
   ```

      您看到错误，因为此内容在 `notaryserver` 上尚不存在。

6. 推送并签署受信任的镜像。
   ```console
   / # docker push sandboxregistry:5000/test/trusttest:latest
   The push refers to a repository [sandboxregistry:5000/test/trusttest]
   5f70bf18a086: Pushed
   c22f7bc058a9: Pushed
   latest: digest: sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926 size: 734
   Signing and pushing trust metadata
   You are about to create a new root signing key passphrase. This passphrase
   will be used to protect the most sensitive key in your signing system. Please
   choose a long, complex passphrase and be careful to keep the password and the
   key file itself secure and backed up. It is highly recommended that you use a
   password manager to generate the passphrase and keep it safe. There will be no
   way to recover this key. You can find the key in your config directory.
   Enter passphrase for new root key with ID 27ec255:
   Repeat passphrase for new root key with ID 27ec255:
   Enter passphrase for new repository key with ID 58233f9 (sandboxregistry:5000/test/trusttest):
   Repeat passphrase for new repository key with ID 58233f9 (sandboxregistry:5000/test/trusttest):
   Finished initializing "sandboxregistry:5000/test/trusttest"
   Successfully signed "sandboxregistry:5000/test/trusttest":latest
   ```

    由于您是第一次推送此仓库，Docker 创建新的 root 和仓库密钥并要求您提供用于加密它们的密码短语。如果您之后再次推送，它只会要求您提供仓库密码短语，以便它可以解密密钥并再次签名。

7. 尝试拉取您刚刚推送的镜像：

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Pull (1 of 1): sandboxregistry:5000/test/trusttest:latest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926: Pulling from test/trusttest
   Digest: sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Status: Downloaded newer image for sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Tagging sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926 as sandboxregistry:5000   test/trusttest:latest
   ```

### 测试恶意镜像

当数据被破坏且您在启用信任时尝试拉取它会发生什么？在本节中，您将进入 `sandboxregistry` 并篡改一些数据。然后，您尝试拉取它。

1. 保持 `trustsandbox` shell 和容器运行。

2. 从您的主机打开一个新的交互式终端，并获取 `sandboxregistry` 容器的 shell。

   ```console
   $ docker container exec -it sandboxregistry bash
   root@65084fc6f047:/#
   ```

3. 列出您推送的 `test/trusttest` 镜像的层：

    ```console
    root@65084fc6f047:/# ls -l /var/lib/registry/docker/registry/v2/repositories/test/trusttest/_layers/sha256
    total 12
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
    ```

4. 进入注册表存储中的一个层（在不同目录中）：

   ```console
   root@65084fc6f047:/# cd /var/lib/registry/docker/registry/v2/blobs/sha256/aa/aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042
   ```

5. 向 `trusttest` 层之一添加恶意数据：

   ```console
   root@65084fc6f047:/# echo "Malicious data" > data
   ```

6. 回到您的 `trustsandbox` 终端。

7. 列出 `trusttest` 镜像。

   ```console
   / # docker image ls | grep trusttest
   REPOSITORY                            TAG                 IMAGE ID            CREATED             SIZE
   docker/trusttest                      latest              cc7629d1331a        11 months ago       5.025 MB
   sandboxregistry:5000/test/trusttest   latest              cc7629d1331a        11 months ago       5.025 MB
   sandboxregistry:5000/test/trusttest   <none>              cc7629d1331a        11 months ago       5.025 MB
   ```

8. 从本地缓存中删除 `trusttest:latest` 镜像。

   ```console
   / # docker image rm -f cc7629d1331a
   Untagged: docker/trusttest:latest
   Untagged: sandboxregistry:5000/test/trusttest:latest
   Untagged: sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Deleted: sha256:cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
   Deleted: sha256:2a1f6535dc6816ffadcdbe20590045e6cbf048d63fd4cc753a684c9bc01abeea
   Deleted: sha256:c22f7bc058a9a8ffeb32989b5d3338787e73855bf224af7aa162823da015d44c
   ```

   Docker 不会重新下载已缓存的镜像，但您希望 Docker 尝试从注册表下载被篡改的镜像并因其无效而拒绝它。

9. 再次拉取镜像。这会从注册表下载镜像，因为您本地没有缓存。

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Pull (1 of 1): sandboxregistry:5000/test/trusttest:latest@sha256:35d5bc26fd358da8320c137784fe590d8fcf9417263ef261653e8e1c7f15672e
   sha256:35d5bc26fd358da8320c137784fe590d8fcf9417263ef261653e8e1c7f15672e: Pulling from test/trusttest

   aac0c133338d: Retrying in 5 seconds
   a3ed95caeb02: Download complete
   error pulling image configuration: unexpected EOF
   ```

   拉取未完成，因为信任系统无法验证镜像。

## 在沙箱中更多玩耍

现在，您在本地系统上有了完整的 Docker 内容信任沙箱，请随意玩耍，看看它的行为。如果您发现 Docker 的任何安全问题，请随时发送邮件至 <security@docker.com>。

## 清理您的沙箱

当您完成后，想要清理所有已启动的服务和已创建的匿名卷时，只需在创建 Docker Compose 文件的目录中运行以下命令：

   ```console
   $ docker compose down -v
   ```