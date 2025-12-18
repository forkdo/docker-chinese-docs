---
description: 了解如何在 Docker Hub 上管理仓库标签。
keywords: Docker Hub, Hub, 仓库内容, 标签
title: Docker Hub 上的标签
linkTitle: 标签
weight: 10
---

标签（Tags）允许您在单个 Docker Hub 仓库中管理多个版本的镜像。通过为每个镜像添加特定的 `:<tag>`，例如 `docs/base:testing`，您可以组织和区分适用于各种用例的镜像版本。如果未指定标签，镜像默认使用 `latest` 标签。

## 标记本地镜像

要标记本地镜像，请使用以下方法之一：

- 构建镜像时，使用 `docker build -t <组织或用户名命名空间>/<仓库名称>[:<标签>]`。
- 使用 `docker tag <现有镜像> <组织或用户名命名空间>/<仓库名称>[:<标签>]` 为现有本地镜像重新打标签。
- 提交更改时，使用 `docker commit <现有容器> <组织或用户名命名空间>/<仓库名称>[:<标签>]`。

然后，您可以将此镜像推送到由其名称或标签指定的仓库：

```console
$ docker push <组织或用户名命名空间>/<仓库名称>:<标签>
```

镜像将被上传并在 Docker Hub 上可用。

## 查看仓库标签

您可以查看可用的标签以及关联镜像的大小。

1. 登录到 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表出现。

3. 选择一个仓库。

   该仓库的 **General** 页面出现。

4. 选择 **Tags** 标签页。

您可以选择标签的摘要（digest）以查看更多详细信息。

## 删除仓库标签

只有仓库所有者或被授予权限的团队成员才能删除标签。

1. 登录到 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。

   您的仓库列表出现。

3. 选择一个仓库。

   该仓库的 **General** 页面出现。

4. 选择 **Tags** 标签页。

5. 选择要删除的标签旁边的对应复选框。

6. 选择 **Delete**。

   确认对话框出现。

7. 选择 **Delete**。