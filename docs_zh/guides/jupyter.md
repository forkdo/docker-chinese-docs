---
description: 使用 JupyterLab 和 Docker 运行、开发和共享数据科学项目
keywords: 入门, jupyter, notebook, python, jupyterlab, 数据科学
title: 使用 JupyterLab 进行数据科学
toc_max: 2
summary: |
  使用 Docker 运行 Jupyter 笔记本。
tags: [data-science]
languages: [python]
aliases:
  - /guides/use-case/jupyter/
params:
  time: 20 分钟
---

Docker 和 JupyterLab 是两个强大的工具，可以增强你的数据科学工作流。在本指南中，你将学习如何将它们结合使用，创建和运行可复现的数据科学环境。本指南基于 [使用 JupyterLab 和 Docker 超级加速 AI/ML 开发](https://www.docker.com/blog/supercharging-ai-ml-development-with-jupyterlab-and-docker/)。

在本指南中，你将学习如何：

- 在本地机器上运行个人 Jupyter 服务器和 JupyterLab
- 自定义你的 JupyterLab 环境
- 与其他数据科学家共享你的 JupyterLab 笔记本和环境

## 什么是 JupyterLab？

[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) 是一个围绕计算笔记本文档概念构建的开源应用程序。它支持共享和执行代码、数据处理、可视化，并提供一系列交互功能用于创建图表。

## 为什么将 Docker 和 JupyterLab 结合使用？

通过结合 Docker 和 JupyterLab，你可以同时获得这两个工具的优势，例如：

- 容器化确保所有部署中 JupyterLab 环境的一致性，消除兼容性问题。
- 容器化的 JupyterLab 简化了共享和协作，无需手动设置环境。
- 容器为 JupyterLab 提供可扩展性，支持工作负载分配和使用 Kubernetes 等平台进行高效的资源管理。

## 前置条件

要跟随本指南操作，你必须安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。

## 运行和访问 JupyterLab 容器

在终端中，运行以下命令来启动你的 JupyterLab 容器。

```console
$ docker run --rm -p 8889:8888 quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

以下是命令中值得注意的部分：

- `-p 8889:8888`：将主机的端口 8889 映射到容器的端口 8888。
- `start-notebook.py --NotebookApp.token='my-token'`：设置访问令牌，而不是使用随机令牌。

更多详细信息，请参阅 [Jupyter 服务器选项](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#jupyter-server-options) 和 [docker run CLI 参考](/reference/cli/docker/container/run/)。

如果这是你第一次运行该镜像，Docker 将下载并运行它。下载镜像所需的时间取决于你的网络连接。

镜像下载并运行后，你可以访问容器。在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

要停止容器，在终端中按 `ctrl`+`c`。

要访问系统上现有的笔记本，你可以使用 [绑定挂载](/storage/bind-mounts/)。打开终端并切换到现有笔记本所在的目录。然后根据你的操作系统运行以下命令。

{{< tabs >}}
{{< tab name="Mac / Linux" >}}

```console
$ docker run --rm -p 8889:8888 -v "$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< tab name="Windows (Command Prompt)" >}}

```console
$ docker run --rm -p 8889:8888 -v "%cd%":/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< tab name="Windows (PowerShell)" >}}

```console
$ docker run --rm -p 8889:8888 -v "$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< tab name="Windows (Git Bash)" >}}

```console
$ docker run --rm -p 8889:8888 -v "/$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

{{< /tab >}}
{{< /tabs >}}

`-v` 选项告诉 Docker 将当前工作目录挂载到容器内的 `/home/jovyan/work`。默认情况下，Jupyter 镜像的根目录是 `/home/jovyan`，你只能访问或保存笔记本到容器中的该目录。

现在你可以访问 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token) 并打开绑定挂载目录中的笔记本。

要停止容器，在终端中按 `ctrl`+`c`。

Docker 还有卷（volumes），这是持久化 Docker 容器生成和使用的数据的首选机制。虽然绑定挂载依赖于主机的目录结构和操作系统，但卷完全由 Docker 管理。

## 保存和访问笔记本

删除容器时，容器中的所有数据都会被删除。要将笔记本保存到容器外部，你可以使用 [卷](/engine/storage/volumes/)。

### 使用卷运行 JupyterLab 容器

要使用卷启动容器，打开终端并运行以下命令：

```console
$ docker run --rm -p 8889:8888 -v jupyter-data:/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

`-v` 选项告诉 Docker 创建一个名为 `jupyter-data` 的卷并将其挂载到容器内的 `/home/jovyan/work`。

要访问容器，在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。现在笔记本可以保存到卷中，即使删除容器后仍然可以访问。

### 将笔记本保存到卷中

在本例中，你将使用 scikit-learn 的 [Iris 数据集](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html) 示例。

1. 打开 Web 浏览器并访问你的 JupyterLab 容器 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

2. 在 **启动器** 中，选择 **笔记本** 下的 **Python 3**。

3. 在笔记本中，指定以下内容以安装必要的包。

   ```console
   !pip install matplotlib scikit-learn
   ```

4. 选择播放按钮运行代码。

5. 在笔记本中，指定以下代码。

   ```python
   from sklearn import datasets

   iris = datasets.load_iris()
   import matplotlib.pyplot as plt

   _, ax = plt.subplots()
   scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
   ax.set(xlabel=iris.feature_names[0], ylabel=iris.feature_names[1])
   _ = ax.legend(
      scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes"
   )
   ```

6. 选择播放按钮运行代码。你应该看到 Iris 数据集的散点图。

7. 在顶部菜单中，选择 **文件**，然后选择 **保存笔记本**。

8. 在 `work` 目录中指定一个名称以将笔记本保存到卷中。例如，`work/mynotebook.ipynb`。

9. 选择 **重命名** 保存笔记本。

笔记本现在已保存在卷中。

在终端中，按 `ctrl`+`c` 停止容器。

现在，每次你使用该卷运行新的 Jupyter 容器时，都可以访问保存的笔记本。

当你再次运行新容器并运行数据绘图代码时，需要再次运行 `!pip install matplotlib scikit-learn` 并下载包。你可以通过创建包含已安装包的自定义镜像来避免每次运行新容器时重新安装包。

## 自定义你的 JupyterLab 环境

你可以使用 Docker 创建自定义的 JupyterLab 环境并将其构建为镜像。通过构建自定义镜像，你可以使用所需的包和工具自定义 JupyterLab 环境，确保它在不同部署中保持一致和可复现。构建自定义镜像也使与其他用户共享 JupyterLab 环境或将其用作进一步开发的基础变得更加容易。

### 在 Dockerfile 中定义你的环境

在前面的 Iris 数据集示例中（见[将笔记本保存到卷](#save-a-notebook-to-the-volume)），你每次运行新容器时都必须安装依赖项 `matplotlib` 和 `scikit-learn`。虽然在那个小示例中依赖项下载和安装很快，但随着依赖项列表的增长，这可能成为一个问题。你的环境中可能还需要其他工具、包或文件。

在这种情况下，你可以将依赖项作为环境的一部分安装到镜像中。然后，每次运行容器时，依赖项都会自动安装。

你可以在 Dockerfile 中定义你的环境。Dockerfile 是一个文本文件，指示 Docker 如何创建你的 JupyterLab 环境镜像。镜像包含你在运行 JupyterLab 时需要和想要的所有内容，如文件、包和工具。

在任意目录中，创建一个名为 `Dockerfile` 的新文本文件。在 IDE 或文本编辑器中打开 `Dockerfile`，然后添加以下内容。

```dockerfile
# syntax=docker/dockerfile:1

FROM quay.io/jupyter/base-notebook
RUN pip install --no-cache-dir matplotlib scikit-learn
```

此 Dockerfile 使用 `quay.io/jupyter/base-notebook` 镜像作为基础，然后运行 `pip` 安装依赖项。有关 Dockerfile 指令的更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

在继续之前，请保存对 `Dockerfile` 的更改。

### 将你的环境构建为镜像

有了 `Dockerfile` 定义你的环境后，你可以使用 `docker build` 将镜像构建为你的 `Dockerfile`。

打开终端，将目录更改为 `Dockerfile` 所在的目录，然后运行以下命令。

```console
$ docker build -t my-jupyter-image .
```

该命令使用你的 `Dockerfile` 和上下文构建 Docker 镜像。`-t` 选项指定镜像的名称和标签，在此为 `my-jupyter-image`。`.` 表示当前目录是上下文，这意味着该目录中的文件可以在镜像创建过程中使用。

你可以通过查看 Docker Desktop 中的 `镜像` 视图或在终端中运行 `docker image ls` 命令来验证镜像是否已构建。你应该看到一个名为 `my-jupyter-image` 的镜像。

## 将你的镜像作为容器运行

要将你的镜像作为容器运行，你使用 `docker run` 命令。在 `docker run` 命令中，你将指定你自己的镜像名称。

```console
$ docker run --rm -p 8889:8888 my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

要访问容器，在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

现在你可以在笔记本中使用包，而无需安装它们。

1. 在 **启动器** 中，选择 **笔记本** 下的 **Python 3**。

2. 在笔记本中，指定以下代码。

   ```python
   from sklearn import datasets

   iris = datasets.load_iris()
   import matplotlib.pyplot as plt

   _, ax = plt.subplots()
   scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
   ax.set(xlabel=iris.feature_names[0], ylabel=iris.feature_names[1])
   _ = ax.legend(
      scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes"
   )
   ```

3. 选择播放按钮运行代码。你应该看到 Iris 数据集的散点图。

在终端中，按 `ctrl`+`c` 停止容器。

## 使用 Compose 运行你的容器

Docker Compose 是一个用于定义和运行多容器应用程序的工具。在这种情况下，应用程序不是多容器应用程序，但 Docker Compose 可以通过在文件中定义所有 `docker run` 选项来简化运行。

### 创建 Compose 文件

要使用 Compose，你需要一个 `compose.yaml` 文件。在与 `Dockerfile` 相同的目录中，创建一个名为 `compose.yaml` 的新文件。

在 IDE 或文本编辑器中打开 `compose.yaml` 文件并添加以下内容。

```yaml
services:
  jupyter:
    build:
      context: .
    ports:
      - 8889:8888
    volumes:
      - jupyter-data:/home/jovyan/work
    command: start-notebook.py --NotebookApp.token='my-token'

volumes:
  jupyter-data:
    name: jupyter-data
```

此 Compose 文件指定了 `docker run` 命令中使用的所有选项。有关 Compose 指令的更多详细信息，请参阅 [Compose 文件参考](/reference/compose-file/_index.md)。

在继续之前，请保存对 `compose.yaml` 文件的更改。

### 使用 Compose 运行你的容器

打开终端，将目录更改为 `compose.yaml` 文件所在的目录，然后运行以下命令。

```console
$ docker compose up --build
```

此命令根据 `compose.yaml` 文件中指定的指令构建你的镜像并将其作为容器运行。`--build` 选项确保你的镜像被重建，如果你对 `Dockerfile` 做了更改，这是必要的。

要访问容器，在 Web 浏览器中导航到 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

在终端中，按 `ctrl`+`c` 停止容器。

## 共享你的工作

通过共享你的镜像和笔记本，你可以创建一个便携且可复现的研究环境，其他数据科学家可以轻松访问和使用。此过程不仅促进协作，还确保你的工作保存在一个可以运行而不会出现兼容性问题的环境中。

要共享你的镜像和数据，你将使用 [Docker Hub](https://hub.docker.com/)。Docker Hub 是一个基于云的注册表服务，允许你共享和分发容器镜像。

### 共享你的镜像

1. [注册](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade) 或登录 [Docker Hub](https://hub.docker.com)。

2. 重命名你的镜像，以便 Docker 知道要将其推送到哪个仓库。打开终端并运行以下 `docker tag` 命令。将 `YOUR-USER-NAME` 替换为你的 Docker ID。

   ```console
   $ docker tag my-jupyter-image YOUR-USER-NAME/my-jupyter-image
   ```

3. 运行以下 `docker push` 命令将镜像推送到 Docker Hub。将 `YOUR-USER-NAME` 替换为你的 Docker ID。

   ```console
   $ docker push YOUR-USER-NAME/my-jupyter-image
   ```

4. 验证你已将镜像推送到 Docker Hub。
   1. 访问 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **仓库**。
   3. 查看仓库的 **Last pushed** 时间。

其他用户现在可以使用 `docker run` 命令下载和运行你的镜像。他们需要将 `YOUR-USER-NAME` 替换为你的 Docker ID。

```console
$ docker run --rm -p 8889:8888 YOUR-USER-NAME/my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

### 共享你的卷

此示例使用 Docker Desktop 图形用户界面。或者，在命令行界面中，你可以 [备份卷](/engine/storage/volumes/#back-up-a-volume)，然后 [使用 ORAS CLI 推送](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md#push-a-volume)。

1. 登录 Docker Desktop。
2. 在 Docker 仪表板中，选择 **卷**。
3. 通过选择名称选择 **jupyter-data** 卷。
4. 选择 **导出** 选项卡。
5. 选择 **快速导出**。
6. 对于 **位置**，选择 **注册表**。
7. 在 **注册表** 下的文本框中，指定你的 Docker ID、卷的名称和标签。例如，`YOUR-USERNAME/jupyter-data:latest`。
8. 选择 **保存**。
9. 验证你已将卷导出到 Docker Hub。
   1. 访问 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **仓库**。
   3. 查看仓库的 **Last pushed** 时间。

其他用户现在可以下载和导入你的卷。要导入卷并使用你的镜像运行它：

1. 登录 Docker Desktop。
2. 在 Docker 仪表板中，选择 **卷**。
3. 选择 **创建** 创建一个新卷。
4. 指定新卷的名称。在本例中，使用 `jupyter-data-2`。
5. 选择 **创建**。
6. 在卷列表中，通过选择名称选择 **jupyter-data-2** 卷。
7. 选择 **导入**。
8. 对于 **位置**，选择 **注册表**。
9. 在 **注册表** 下的文本框中，指定与你导出卷到