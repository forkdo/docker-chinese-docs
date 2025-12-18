---
title: 使用 WSL
description: 如何使用 Docker 和 WSL 2 进行开发，以及了解 WSL 的 GPU 支持
keywords: wsl, wsl 2, 开发, docker desktop, windows
aliases:
- /desktop/wsl/use-wsl/
---

以下部分介绍如何使用 Docker 和 WSL 2 开始开发应用程序。我们建议您将代码放在默认的 Linux 发行版中，以获得使用 Docker 和 WSL 2 的最佳开发体验。在 Docker Desktop 中启用 WSL 2 功能后，您就可以在 Linux 发行版中开始处理代码，同时理想情况下您的 IDE 仍保留在 Windows 中。如果您使用的是 [VS Code](https://code.visualstudio.com/download)，这种工作流非常直接。

## 使用 Docker 和 WSL 2 进行开发

1. 打开 VS Code，安装 [Remote - WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) 扩展。此扩展允许您在 Linux 发行版中进行远程开发，而您的 IDE 客户端仍保留在 Windows 中。
2. 打开终端并输入：

    ```console
    $ wsl
    ```
3. 导航到您的项目目录，然后输入：

    ```console
    $ code .
    ```

    这将打开一个新的 VS Code 窗口，该窗口远程连接到您的默认 Linux 发行版，您可以在屏幕的左下角检查连接状态。


或者，您也可以从 **开始** 菜单中打开默认的 Linux 发行版，导航到您的项目目录，然后运行 `code .`