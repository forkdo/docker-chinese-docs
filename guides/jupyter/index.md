# 使用 JupyterLab 进行数据科学

Docker 和 JupyterLab 是两个强大的工具，可以增强您的数据科学工作流程。在本指南中，您将学习如何将它们结合使用，以创建和运行可复现的数据科学环境。本指南基于 [使用 JupyterLab 和 Docker 强化 AI/ML 开发](https://www.docker.com/blog/supercharging-ai-ml-development-with-jupyterlab-and-docker/)。

在本指南中，您将学习如何：

- 在本地机器上运行带有 JupyterLab 的个人 Jupyter Server
- 自定义您的 JupyterLab 环境
- 与其他数据科学家共享您的 JupyterLab notebook 和环境

## 什么是 JupyterLab？

[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) 是一款围绕计算笔记本文档概念构建的开源应用程序。它支持共享和执行代码、数据处理、可视化，并提供一系列用于创建图表的交互功能。

## 为什么将 Docker 和 JupyterLab 结合使用？

通过结合使用 Docker 和 JupyterLab，您可以受益于这两种工具的优势，例如：

- 容器化确保了所有部署中 JupyterLab 环境的一致性，消除了兼容性问题。
- 容器化的 JupyterLab 通过消除手动环境设置的需要，简化了共享和协作。
- 容器为 JupyterLab 提供了可扩展性，支持工作负载分发和高效的资源管理（例如通过 Kubernetes 等平台）。

## 先决条件

要学习本指南，您必须安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。

## 运行并访问 JupyterLab 容器

在终端中，运行以下命令以启动您的 JupyterLab 容器。

```console
$ docker run --rm -p 8889:8888 quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

以下是该命令的显著部分：

- `-p 8889:8888`：将主机的 8889 端口映射到容器的 8888 端口。
- `start-notebook.py --NotebookApp.token='my-token'`：设置访问令牌，而不是使用随机令牌。

更多详情，请参阅 [Jupyter Server 选项](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#jupyter-server-options) 和 [docker run CLI 参考](/reference/cli/docker/container/run/)。

如果这是您第一次运行该镜像，Docker 将下载并运行它。下载镜像所需的时间取决于您的网络连接。

镜像下载并运行后，您可以访问该容器。要访问容器，请在 Web 浏览器中导航至 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

要停止容器，请在终端中按 `ctrl`+`c`。

要访问系统上的现有笔记本，您可以使用[绑定挂载](/storage/bind-mounts/)。打开终端并切换到现有笔记本所在的目录。然后，根据您的操作系统运行以下命令。








<div
  class="tabs"
  
    x-data="{ selected: 'Mac-/-Linux' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Mac-/-Linux' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac-/-Linux'"
        
      >
        Mac / Linux
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Windows-%E5%91%BD%E4%BB%A4%E6%8F%90%E7%A4%BA%E7%AC%A6' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows-%E5%91%BD%E4%BB%A4%E6%8F%90%E7%A4%BA%E7%AC%A6'"
        
      >
        Windows (命令提示符)
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Windows-PowerShell' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows-PowerShell'"
        
      >
        Windows (PowerShell)
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Windows-Git-Bash' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows-Git-Bash'"
        
      >
        Windows (Git Bash)
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac-/-Linux' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC0tcm0gLXAgODg4OTo4ODg4IC12ICIkKHB3ZCk6L2hvbWUvam92eWFuL3dvcmsiIHF1YXkuaW8vanVweXRlci9iYXNlLW5vdGVib29rIHN0YXJ0LW5vdGVib29rLnB5IC0tTm90ZWJvb2tBcHAudG9rZW49J215LXRva2VuJw==', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run --rm -p 8889:8888 -v <span class="s2">&#34;</span><span class="k">$(</span><span class="nb">pwd</span><span class="k">)</span><span class="s2">:/home/jovyan/work&#34;</span> quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token<span class="o">=</span><span class="s1">&#39;my-token&#39;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows-%E5%91%BD%E4%BB%A4%E6%8F%90%E7%A4%BA%E7%AC%A6' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC0tcm0gLXAgODg4OTo4ODg4IC12ICIlY2QlIjovaG9tZS9qb3Z5YW4vd29yayBxdWF5LmlvL2p1cHl0ZXIvYmFzZS1ub3RlYm9vayBzdGFydC1ub3RlYm9vay5weSAtLU5vdGVib29rQXBwLnRva2VuPSdteS10b2tlbic=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run --rm -p 8889:8888 -v <span class="s2">&#34;%cd%&#34;</span>:/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token<span class="o">=</span><span class="s1">&#39;my-token&#39;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows-PowerShell' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC0tcm0gLXAgODg4OTo4ODg4IC12ICIkKHB3ZCk6L2hvbWUvam92eWFuL3dvcmsiIHF1YXkuaW8vanVweXRlci9iYXNlLW5vdGVib29rIHN0YXJ0LW5vdGVib29rLnB5IC0tTm90ZWJvb2tBcHAudG9rZW49J215LXRva2VuJw==', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run --rm -p 8889:8888 -v <span class="s2">&#34;</span><span class="k">$(</span><span class="nb">pwd</span><span class="k">)</span><span class="s2">:/home/jovyan/work&#34;</span> quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token<span class="o">=</span><span class="s1">&#39;my-token&#39;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows-Git-Bash' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgcnVuIC0tcm0gLXAgODg4OTo4ODg4IC12ICIvJChwd2QpOi9ob21lL2pvdnlhbi93b3JrIiBxdWF5LmlvL2p1cHl0ZXIvYmFzZS1ub3RlYm9vayBzdGFydC1ub3RlYm9vay5weSAtLU5vdGVib29rQXBwLnRva2VuPSdteS10b2tlbic=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker run --rm -p 8889:8888 -v <span class="s2">&#34;/</span><span class="k">$(</span><span class="nb">pwd</span><span class="k">)</span><span class="s2">:/home/jovyan/work&#34;</span> quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token<span class="o">=</span><span class="s1">&#39;my-token&#39;</span>
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


`-v` 选项告诉 Docker 将您当前的工作目录挂载到容器内的 `/home/jovyan/work`。默认情况下，Jupyter 镜像的根目录是 `/home/jovyan`，您只能访问或保存笔记本到容器中的该目录。

现在您可以访问 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token) 并打开绑定挂载目录中的笔记本。

要停止容器，请在终端中按 `ctrl`+`c`。

Docker 还有卷（volumes），这是持久化由 Docker 容器生成和使用的数据的首选机制。虽然绑定挂载依赖于主机的目录结构和操作系统，但卷完全由 Docker 管理。

## 保存和访问笔记本

当您移除容器时，该容器中的所有数据都会被删除。要将笔记本保存在容器外部，您可以使用[卷](/engine/storage/volumes/)。

### 使用卷运行 JupyterLab 容器

要使用卷启动容器，请打开终端并运行以下命令：

```console
$ docker run --rm -p 8889:8888 -v jupyter-data:/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

`-v` 选项告诉 Docker 创建一个名为 `jupyter-data` 的卷，并将其挂载到容器的 `/home/jovyan/work` 位置。

要访问容器，请在 Web 浏览器中导航至 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。笔记本现在可以保存到卷中，并且即使容器被删除也可以访问。

### 将笔记本保存到卷中

在这个例子中，您将使用 scikit-learn 中的 [Iris 数据集](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html) 示例。

1. 打开 Web 浏览器并访问您的 JupyterLab 容器，地址为 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

2. 在**启动器 (Launcher)** 中，**笔记本 (Notebook)** 下方，选择 **Python 3**。

3. 在笔记本中，指定以下内容以安装必要的包。

   ```console
   !pip install matplotlib scikit-learn
   ```

4. 选择播放按钮以运行代码。

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

6. 选择播放按钮以运行代码。您应该会看到 Iris 数据集的散点图。

7. 在顶部菜单中，选择 **文件 (File)**，然后选择 **保存笔记本 (Save Notebook)**。

8. 在 `work` 目录中指定一个名称以将笔记本保存到卷中。例如，`work/mynotebook.ipynb`。

9. 选择 **重命名 (Rename)** 以保存笔记本。

笔记本现在已保存在卷中。

在终端中，按 `ctrl`+ `c` 停止容器。

现在，只要您使用该卷运行 Jupyter 容器，就可以访问已保存的笔记本。

当您运行新容器时，如果再次运行数据绘图代码，它将需要运行 `!pip install matplotlib scikit-learn` 并下载包。您可以通过创建自己的镜像（其中包含已安装的包）来避免每次运行新容器时都重新安装包。

## 自定义您的 JupyterLab 环境

您可以创建自己的 JupyterLab 环境，并使用 Docker 将其构建为镜像。通过构建自己的镜像，您可以使用所需的包和工具自定义您的 JupyterLab 环境，并确保它在不同部署中保持一致且可复现。构建自己的镜像还可以更轻松地与他人共享您的 JupyterLab 环境，或将其用作进一步开发的基础。

### 在 Dockerfile 中定义您的环境

在之前的 [将笔记本保存到卷中](#将笔记本保存到卷中) 的 Iris 数据集示例中，您每次运行新容器时都必须安装依赖项 `matplotlib` 和 `scikit-learn`。虽然这个小示例中的依赖项下载和安装很快，但随着依赖项列表的增长，这可能会成为一个问题。可能还有其他您始终希望在环境中使用的工具、包或文件。

在这种情况下，您可以将依赖项作为镜像环境的一部分进行安装。这样，每次运行容器时，依赖项都将始终安装。

您可以在 Dockerfile 中定义您的环境。Dockerfile 是一个文本文件，它指示 Docker 如何创建您的 JupyterLab 环境的镜像。镜像包含运行 JupyterLab 时所需和期望的一切内容，例如文件、包和工具。

在您选择的目录中，创建一个名为 `Dockerfile` 的新文本文件。在 IDE 或文本编辑器中打开 `Dockerfile`，然后添加以下内容。

```dockerfile
# syntax=docker/dockerfile:1

FROM quay.io/jupyter/base-notebook
RUN pip install --no-cache-dir matplotlib scikit-learn
```

此 Dockerfile 使用 `quay.io/jupyter/base-notebook` 镜像作为基础，然后运行 `pip` 来安装依赖项。有关 Dockerfile 中指令的更多详情，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

在继续之前，请将您的更改保存到 `Dockerfile`。

### 将您的环境构建到镜像中

在拥有定义环境的 `Dockerfile` 后，您可以使用 `docker build` 基于您的 `Dockerfile` 构建镜像。

打开终端，切换到 `Dockerfile` 所在的目录，然后运行以下命令。

```console
$ docker build -t my-jupyter-image .
```

该命令根据您的 `Dockerfile` 和上下文构建 Docker 镜像。`-t` 选项指定镜像的名称和标签，在本例中为 `my-jupyter-image`。`.` 表示当前目录是上下文，这意味着该目录中的文件可以在镜像创建过程中使用。

您可以通过在 Docker Desktop 中查看 `Images` 视图，或在终端中运行 `docker image ls` 命令来验证镜像是否已构建。您应该会看到一个名为 `my-jupyter-image` 的镜像。

## 将镜像作为容器运行

要将镜像作为容器运行，您可以使用 `docker run` 命令。在 `docker run` 命令中，您将指定自己的镜像名称。

```console
$ docker run --rm -p 8889:8888 my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

要访问容器，请在 Web 浏览器中导航至 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

您现在可以在笔记本中使用这些包，而无需在笔记本中安装它们。

1. 在**启动器 (Launcher)** 中，**笔记本 (Notebook)** 下方，选择 **Python 3**。

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

3. 选择播放按钮以运行代码。您应该会看到 Iris 数据集的散点图。

在终端中，按 `ctrl`+ `c` 停止容器。

## 使用 Compose 运行您的容器

Docker Compose 是一个用于定义和运行多容器应用程序的工具。在本例中，该应用程序不是多容器应用程序，但 Docker Compose 可以通过在一个文件中定义所有 `docker run` 选项来使其更易于运行。

### 创建 Compose 文件

要使用 Compose，您需要一个 `compose.yaml` 文件。在与 `Dockerfile` 相同的目录中，创建一个名为 `compose.yaml` 的新文件。

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

此 Compose 文件指定了您在 `docker run` 命令中使用的所有选项。有关 Compose 指令的更多详情，请参阅 [Compose 文件参考](/reference/compose-file/_index.md)。

在继续之前，请将您的更改保存到 `compose.yaml` 文件。

### 使用 Compose 运行您的容器

打开终端，切换到 `compose.yaml` 文件所在的目录，然后运行以下命令。

```console
$ docker compose up --build
```

此命令构建您的镜像，并使用 `compose.yaml` 文件中指定的指令将其作为容器运行。`--build` 选项确保重新构建您的镜像，如果您对 `Dockerfile` 进行了更改，这是必要的。

要访问容器，请在 Web 浏览器中导航至 [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token)。

在终端中，按 `ctrl`+ `c` 停止容器。

## 分享您的工作

通过共享您的镜像和笔记本，您可以创建一个可移植且可复制的研究环境，其他数据科学家可以轻松访问和使用。此过程不仅促进了协作，还确保您的工作保存在一个可以无兼容性问题运行的环境中。

要共享您的镜像和数据，您将使用 [Docker Hub](https://hub.docker.com/)。Docker Hub 是一项基于云的注册服务，可让您共享和分发容器镜像。

### 共享您的镜像

1. [注册](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade)或登录 [Docker Hub](https://hub.docker.com)。

2. 重命名您的镜像，以便 Docker 知道要将其推送到哪个存储库。打开终端并运行以下 `docker tag` 命令。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker tag my-jupyter-image YOUR-USER-NAME/my-jupyter-image
   ```

3. 运行以下 `docker push` 命令将镜像推送到 Docker Hub。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker push YOUR-USER-NAME/my-jupyter-image
   ```

4. 验证您是否已将镜像推送到 Docker Hub。
   1. 转到 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **Repositories**。
   3. 查看您存储库的 **Last pushed** 时间。

其他用户现在可以使用 `docker run` 命令下载并运行您的镜像。他们需要将 `YOUR-USER-NAME` 替换为您的 Docker ID。

```console
$ docker run --rm -p 8889:8888 YOUR-USER-NAME/my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

### 共享您的卷

此示例使用 Docker Desktop 图形用户界面。或者，在命令行界面中，您可以[备份卷](/engine/storage/volumes/#back-up-a-volume)，然后[使用 ORAS CLI 推送它](/manuals/docker-hub/repos/manage/hub-images/oci-artifacts.md#push-a-volume)。

1. 登录 Docker Desktop。
2. 在 Docker 仪表板中，选择 **Volumes**。
3. 通过选择名称选择 **jupyter-data** 卷。
4. 选择 **Exports** 选项卡。
5. 选择 **Quick export**。
6. 对于 **Location**，选择 **Registry**。
7. 在 **Registry** 下的文本框中，指定您的 Docker ID、卷的名称和标签。例如，`YOUR-USERNAME/jupyter-data:latest`。
8. 选择 **Save**。
9. 验证您是否已将卷导出到 Docker Hub。
   1. 转到 [Docker Hub](https://hub.docker.com)。
   2. 选择 **My Hub** > **Repositories**。
   3. 查看您存储库的 **Last pushed** 时间。

其他用户现在可以下载并导入您的卷。要导入卷然后使用您的镜像运行它：

1. 登录 Docker Desktop。
2. 在 Docker 仪表板中，选择 **Volumes**。
3. 选择 **Create** 以创建新卷。
4. 指定新卷的名称。在此示例中，使用 `jupyter-data-2`。
5. 选择 **Create**。
6. 在卷列表中，通过选择名称选择 **jupyter-data-2** 卷。
7. 选择 **Import**。
8. 对于 **Location**，选择 **Registry**。
9. 在 **Registry** 下的文本框中，指定与您导出卷到的存储库相同的名称。例如，`YOUR-USERNAME/jupyter-data:latest`。
10. 选择 **Import**。
11. 在终端中，运行 `docker run` 以使用导入的卷运行您的镜像。将 `YOUR-USER-NAME` 替换为您的 Docker ID。

   ```console
   $ docker run --rm -p 8889:8888 -v jupyter-data-2:/home/jovyan/work YOUR-USER-NAME/my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
   ```

## 总结

在本指南中，您学习了如何利用 Docker 和 JupyterLab 来创建可复现的数据科学环境，从而促进数据科学项目的开发和共享。这包括运行个人 JupyterLab 服务器、使用必要的工具和包自定义环境，以及与其他数据科学家共享笔记本和环境。

相关信息：

- [Dockerfile 参考](/reference/dockerfile/)
- [Compose 文件参考](/reference/compose-file/)
- [Docker CLI 参考](reference/cli/docker/)
- [Jupyter Docker Stacks 文档](https://jupyter-docker-stacks.readthedocs.io/en/latest/)
