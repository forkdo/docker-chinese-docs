---
description: 在信任沙盒中进行操作
keywords: trust, security, root, keys, repository, sandbox
title: 在内容信任沙盒中进行操作
aliases:
- /security/trust/trust_sandbox/
---

本文介绍如何设置和使用用于试验信任功能的沙盒。该沙盒允许您在本地配置和尝试信任操作，而不会影响您的生产镜像。

在使用此沙盒之前，您应该已通读[信任概述](index.md)。

## 先决条件

这些说明假设您正在 Linux 或 macOS 上运行。您可以在本地计算机或虚拟机上运行此沙盒。您需要在本地计算机或虚拟机中拥有运行 docker 命令的权限。

此沙盒要求您安装两个 Docker 工具：Docker Engine >= 1.10.0 和 Docker Compose >= 1.6.0。要安装 Docker Engine，请从[支持的平台列表](../../install/_index.md)中选择。要安装 Docker Compose，请参阅[此处的详细说明](/manuals/compose/install/_index.md)。

## 沙盒中包含什么？

如果您只是开箱即用信任功能，则只需要 Docker Engine 客户端和访问 Docker Hub 的权限。沙盒模拟生产信任环境，并设置以下附加组件。

| 容器            | 描述                                                                                                                              |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------|
| trustsandbox    | 一个包含最新版本 Docker Engine 和一些预配置证书的容器。这是您的沙盒，您可以在其中使用 `docker` 客户端测试信任操作。                 |
| Registry server | 本地注册表服务。                                                                                                                  |
| Notary server   | 负责管理信任的所有繁重工作的服务。                                                                                                |

这意味着您运行自己的内容信任（Notary）服务器和注册表。如果您只使用 Docker Hub，则不需要这些组件。它们已内置在 Docker Hub 中供您使用。但是，对于沙盒，您需要构建自己的完整模拟生产环境。

在 `trustsandbox` 容器内，您与本地注册表交互，而不是与 Docker Hub 交互。这意味着不会使用您日常的镜像仓库。在您操作期间，它们受到保护。

当您在沙盒中操作时，您还会创建根密钥和仓库密钥。沙盒配置为将所有密钥和文件存储在 `trustsandbox` 容器内部。由于您在沙盒中创建的密钥仅用于操作，因此销毁容器也会销毁它们。

通过为 `trustsandbox` 容器使用 `docker-in-docker` 镜像，您也不会使用您推送和拉取的任何镜像来污染真实的 Docker 守护进程缓存。镜像存储在附加到此容器的匿名卷中，并且可以在销毁容器后销毁。

## 构建沙盒

在本节中，您将使用 Docker Compose 来指定如何设置并链接 `trustsandbox` 容器、Notary 服务器和 Registry 服务器。

1.  创建一个新的 `trustsandbox` 目录并进入该目录。

   ```console
   $ mkdir trustsandbox
   $ cd trustsandbox
   ```

2.  使用您喜欢的编辑器创建一个名为 `compose.yaml` 的文件。例如，使用 vim：

   ```console
   $ touch compose.yaml
   $ vim compose.yaml
   ```

3.  将以下内容添加到新文件中。

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
4.  保存并关闭文件。

5.  在本地系统上运行容器。

   ```console
   $ docker compose up -d
   ```

   第一次运行此命令时，`docker-in-docker`、Notary 服务器和注册表镜像将从 Docker Hub 下载。

## 在沙盒中操作

现在一切设置就绪，您可以进入 `trustsandbox` 容器并开始测试 Docker 内容信任。从主机获取 `trustsandbox` 容器中的 shell。

```console
$ docker container exec -it trustsandbox sh
/ #
```

### 测试一些信任操作

现在，从 `trustsandbox` 容器内部拉取一些镜像。

1.  下载一个 `docker` 镜像以供测试。

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

2.  为其打标签以推送到您的沙盒注册表：

   ```console
   / # docker tag docker/trusttest sandboxregistry:5000/test/trusttest:latest
   ```

3.  启用内容信任。

   ```console
   / # export DOCKER_CONTENT_TRUST=1
   ```

4.  指定信任服务器。

   ```console
   / # export DOCKER_CONTENT_TRUST_SERVER=https://notaryserver:4443
   ```

    此步骤仅在沙盒使用其自己的服务器时才需要。通常，如果您使用 Docker 公共 Hub，则不需要此步骤。

5.  拉取测试镜像。

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Error: remote trust data does not exist for sandboxregistry:5000/test/trusttest: notaryserver:4443 does not have trust data for      sandboxregistry:5000/test/trusttest
   ```
      您会看到错误，因为此内容尚不存在于 `notaryserver` 上。

6.  推送并签署受信任的镜像。
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

    由于这是您第一次推送此仓库，Docker 会创建新的根密钥和仓库密钥，并要求您提供用于加密它们的密码。如果您在此之后再次推送，它只会要求您提供仓库密码，以便它可以解密密钥并再次签名。

7.  尝试拉取您刚刚推送的镜像：

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Pull (1 of 1): sandboxregistry:5000/test/trusttest:latest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926: Pulling from test/trusttest
   Digest: sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Status: Downloaded newer image for sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Tagging sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926 as sandboxregistry:5000   test/trusttest:latest
   ```

### 使用恶意镜像进行测试

当数据损坏而您尝试在启用信任的情况下拉取它时会发生什么？在本节中，您将进入 `sandboxregistry` 并篡改一些数据。然后，您尝试拉取它。

1.  让 `trustsandbox` shell 和容器保持运行。

2.  从主机打开一个新的交互式终端，并获取 `sandboxregistry` 容器中的 shell。

   ```console
   $ docker container exec -it sandboxregistry bash
   root@65084fc6f047:/#
   ```

3.  列出您推送的 `test/trusttest` 镜像的层：

    ```console
    root@65084fc6f047:/# ls -l /var/lib/registry/docker/registry/v2/repositories/test/trusttest/_layers/sha256
    total 12
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042
    drwxr-xr-x 2 root root 4096 Jun 10 17:26 cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
    ```

4.  进入其中一个层的注册表存储（这在另一个目录中）：

   ```console
   root@65084fc6f047:/# cd /var/lib/registry/docker/registry/v2/blobs/sha256/aa/aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042
   ```

5.  向其中一个 `trusttest` 层添加恶意数据：

   ```console
   root@65084fc6f047:/# echo "Malicious data" > data
   ```

6.  返回到您的 `trustsandbox` 终端。

7.  列出 `trusttest` 镜像。

   ```console
   / # docker image ls | grep trusttest
   REPOSITORY                            TAG                 IMAGE ID            CREATED             SIZE
   docker/trusttest                      latest              cc7629d1331a        11 months ago       5.025 MB
   sandboxregistry:5000/test/trusttest   latest              cc7629d1331a        11 months ago       5.025 MB
   sandboxregistry:5000/test/trusttest   <none>              cc7629d1331a        11 months ago       5.025 MB
   ```

8.  从本地缓存中移除 `trusttest:latest` 镜像。

   ```console
   / # docker image rm -f cc7629d1331a
   Untagged: docker/trusttest:latest
   Untagged: sandboxregistry:5000/test/trusttest:latest
   Untagged: sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Deleted: sha256:cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
   Deleted: sha256:2a1f6535dc6816ffadcdbe20590045e6cbf048d63fd4cc753a684c9bc01abeea
   Deleted: sha256:c22f7bc058a9a8ffeb32989b5d3338787e73855bf224af7aa162823da015d44c
   ```

   Docker 不会重新下载它已经缓存的镜像，但您希望 Docker 尝试从注册表下载被篡改的镜像，并因为它无效而拒绝它。

9.  再次拉取镜像。这会从注册表下载镜像，因为您没有缓存它。

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

## 在沙盒中进一步操作

现在，您在本地系统上拥有一个完整的 Docker 内容信任沙盒，可以随意操作并观察其行为。如果您发现 Docker 的任何安全问题，请随时发送电子邮件至 <security@docker.com>。

## 清理沙盒

当您完成操作并想要清理所有已启动的服务以及任何已创建的匿名卷时，只需在您创建 Docker Compose 文件的目录中运行以下命令：

   ```console
   $ docker compose down -v
   ```