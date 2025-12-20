# 将镜像推送到仓库

要向 Docker Hub 上的仓库添加内容，您需要先为您的 Docker 镜像打上标签，然后将其推送到您的仓库。此过程可让您与他人共享镜像或在不同的环境中使用它们。

1. 为您的 Docker 镜像打上标签。

   `docker tag` 命令为您的 Docker 镜像分配一个标签，该标签包含您的 Docker Hub 命名空间和仓库名称。通用语法为：

   ```console
   $ docker tag [SOURCE_IMAGE[:TAG]] [NAMESPACE/REPOSITORY[:TAG]]
   ```

   示例：

   如果您的本地镜像名为 `my-app`，并且您希望将其标记为 `my-namespace/my-repo` 仓库的 `v1.0` 版本，请运行：

   ```console
   $ docker tag my-app my-namespace/my-repo:v1.0
   ```

2. 将镜像推送到 Docker Hub。

   使用 `docker push` 命令将您已标记的镜像上传到 Docker Hub 上的指定仓库。

   示例：

   ```console
   $ docker push my-namespace/my-repo:v1.0
   ```

   此命令将标记为 `v1.0` 的镜像推送到 `my-namespace/my-repo` 仓库。

3. 在 Docker Hub 上验证镜像。
