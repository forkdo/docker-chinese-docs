# 构建驱动


构建驱动是关于 BuildKit 后端如何运行以及在哪里运行的配置。驱动设置是可自定义的，并允许对 builder 进行细粒度控制。Buildx 支持以下驱动：

- `docker`：使用与 Docker 守护进程捆绑的 BuildKit 库。
- `docker-container`：使用 Docker 创建一个专用的 BuildKit 容器。
- `kubernetes`：在 Kubernetes 集群中创建 BuildKit Pod。
- `remote`：直接连接到手动管理的 BuildKit 守护进程。

不同的驱动支持不同的用例。默认的 `docker` 驱动优先考虑简单性和易用性。它对缓存和输出格式等高级特性的支持有限，且不可配置。其他驱动提供了更大的灵活性，更擅长处理高级场景。

下表概述了驱动之间的一些差异。

| Feature                      |  `docker`   | `docker-container` | `kubernetes` |      `remote`      |
| :--------------------------- | :---------: | :----------------: | :----------: | :----------------: |
| **自动加载镜像**             |     ✅      |                    |              |                    |
| **缓存导出**                 |     ✅\*     |         ✅         |      ✅      |         ✅         |
| **Tarball 输出**             |             |         ✅         |      ✅      |         ✅         |
| **多架构镜像**               |             |         ✅         |      ✅      |         ✅         |
| **BuildKit 配置**            |             |         ✅         |      ✅      | 外部管理           |

\* _`docker` 驱动不支持所有的缓存导出选项。
详见 [Cache storage backends](/manuals/build/cache/backends/_index.md)。_

## 加载到本地镜像存储（Loading to local image store）

与使用默认 `docker` 驱动不同，使用其他驱动构建的镜像不会自动加载到本地镜像存储。如果你不指定输出，构建结果只会导出到构建缓存。

要使用非默认驱动构建镜像并将其加载到镜像存储，请在构建命令中使用 `--load` 标志：

   ```console
   $ docker buildx build --load -t <image> --builder=container .
   ...
   => exporting to oci image format                                                                                                      7.7s
   => => exporting layers                                                                                                                4.9s
   => => exporting manifest sha256:4e4ca161fa338be2c303445411900ebbc5fc086153a0b846ac12996960b479d3                                      0.0s
   => => exporting config sha256:adf3eec768a14b6e183a1010cb96d91155a82fd722a1091440c88f3747f1f53f                                        0.0s
   => => sending tarball                                                                                                                 2.8s
   => importing to docker
   ```

   使用此选项，构建完成后镜像即可在镜像存储中可用：

   ```console
   $ docker image ls
   REPOSITORY                       TAG               IMAGE ID       CREATED             SIZE
   <image>                          latest            adf3eec768a1   2 minutes ago       197MB
   ```

### 默认加载（Load by default）



你可以将自定义构建驱动配置为与默认 `docker` 驱动类似的行为，即默认将镜像加载到本地镜像存储。为此，请在创建 builder 时设置 `default-load` 驱动选项：

```console
$ docker buildx create --driver-opt default-load=true
```

请注意，与 `docker` 驱动一样，如果你使用 `--output` 指定了不同的输出格式，除非你也显式指定 `--output type=docker` 或使用 `--load` 标志，否则结果不会被加载到镜像存储。

## 下一步（What's next）

阅读关于每个驱动的说明：

  - [Docker 驱动](./docker.md)
  - [Docker 容器驱动](./docker-container.md)
  - [Kubernetes 驱动](./kubernetes.md)
- [远程驱动](./remote.md)

