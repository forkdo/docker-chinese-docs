# Docker Hub 上的标签

标签让您能够在单个 Docker Hub 仓库中管理多个版本的镜像。通过为每个镜像添加特定的 `:<tag>`，例如 `docs/base:testing`，您可以组织并区分不同用途的镜像版本。如果未指定标签，镜像将默认使用 `latest` 标签。

## 标记本地镜像

要标记本地镜像，请使用以下方法之一：

- 构建镜像时，使用 `docker build -t <org-or-user-namespace>/<repo-name>[:<tag>]`。
- 使用 `docker tag <existing-image> <org-or-user-namespace>/<repo-name>[:<tag>]` 重新标记现有的本地镜像。
- 提交更改时，使用 `docker commit <existing-container> <org-or-user-namespace>/<repo-name>[:<tag>]`。

然后，您可以将此镜像推送到由其名称或标签指定的仓库：

```console
$ docker push <org-or-user-namespace>/<repo-name>:<tag>
```

镜像随后会被上传，并可在 Docker Hub 中使用。

## 查看仓库标签

您可以查看可用标签及其关联镜像的大小。

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表将显示出来。

3. 选择一个仓库。

   该仓库的 **General** 页面将显示出来。

4. 选择 **Tags** 选项卡。

您可以选择标签的摘要以查看更多详细信息。

## 删除仓库标签

只有仓库所有者或拥有相应权限的其他团队成员才能删除标签。

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表将显示出来。

3. 选择一个仓库。

   该仓库的 **General** 页面将显示出来。

4. 选择 **Tags** 选项卡。

5. 选择要删除的标签旁边的相应复选框。

6. 选择 **Delete**。

   将出现一个确认对话框。

7. 选择 **Delete**。
