---
description: 了解不可变标签及其如何帮助在 Docker Hub 上保持镜像版本一致性。
keywords: Docker Hub, Hub, 仓库内容, 标签, 不可变标签, 版本控制
title: Docker Hub 上的不可变标签
linkTitle: Immutable tags
weight: 11
---
{{< summary-bar feature_name="Immutable tags" >}}

不可变标签提供了一种方式，确保特定的镜像版本一旦发布到 Docker Hub 后就无法更改。此功能通过防止意外覆盖重要的镜像版本，帮助维护容器部署的一致性和可靠性。

## 什么是不可变标签？

不可变标签是镜像标签，一旦推送到 Docker Hub，就无法被覆盖或删除。这确保了镜像的特定版本在其生命周期内始终保持不变，提供：

- 版本一致性
- 可重现的构建
- 防止意外覆盖
- 更好的安全性和合规性

## 启用不可变标签

要为您的仓库启用不可变标签：

1. 登录 [Docker Hub](https://hub.docker.com)。
2. 选择 **My Hub** > **Repositories**。
3. 选择要启用不可变标签的仓库。
4. 进入 **Settings** > **General**。
5. 在 **Tag mutability settings** 下，选择以下选项之一：
   - **All tags are mutable (Default)**：  
     标签可以更改为引用不同的镜像。这允许您在不创建新标签的情况下重新定位标签。
   - **All tags are immutable**：  
     标签在创建后无法更新以指向不同的镜像。这确保了一致性并防止意外更改。这包括 `latest` 标签。
   - **Specific tags are immutable**：  
     使用正则表达式值定义创建后无法更新的特定标签。
6. 选择 **Save**。

启用后，所有标签将被锁定到其特定镜像，确保每个标签始终指向相同的镜像版本且无法修改。

> [!NOTE]
> 此正则表达式实现遵循 [Go regexp 包](https://pkg.go.dev/regexp)，基于 RE2 引擎。更多信息，请访问 [RE2 正则表达式语法](https://github.com/google/re2/wiki/Syntax)。

## 使用不可变标签

启用不可变标签后：

- 您无法推送具有相同标签名称的新镜像
- 您必须为每个新镜像版本使用新的标签名称

要推送镜像，请为您的更新镜像创建新标签并推送到仓库。