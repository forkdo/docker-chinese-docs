---
title: 构建语言翻译应用程序
linkTitle: 语言翻译
keywords: nlp, natural language processing, text summarization, python, language translation, googletrans
description: 学习如何使用 Python、Googletrans 和 Docker 构建并运行语言翻译应用程序。
summary: |
  本指南演示如何使用 Docker 部署语言翻译模型以执行自然语言处理（NLP）任务。
tags: [ai]
languages: [python]
aliases:
  - /guides/use-case/nlp/language-translation/
params:
  time: 20 分钟
---

## 概述

本指南将带你构建并运行一个语言翻译应用程序。你将使用 Python 和 Googletrans 构建应用程序，然后使用 Docker 设置环境并运行应用程序。

该应用程序展示了 Googletrans 库在语言翻译中的简单但实用的应用，涵盖了基本的 Python 和 Docker 概念。Googletrans 是一个免费且无限制的 Python 库，实现了 Google Translate API。它使用 Google Translate Ajax API 来调用诸如 detect 和 translate 等方法。

## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 定期添加新功能，本指南中的某些部分可能仅与 Docker Desktop 的最新版本兼容。
- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 获取示例应用程序

1. 打开终端，使用以下命令克隆示例应用程序的仓库。

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. 验证你已克隆仓库。

   你应该在 `Docker-NLP` 目录中看到以下文件。

   ```text
   01_sentiment_analysis.py
   02_name_entity_recognition.py
   03_text_classification.py
   04_text_summarization.py
   05_language_translation.py
   entrypoint.sh
   requirements.txt
   Dockerfile
   README.md
   ```

## 探索应用程序代码

应用程序的源代码位于 `Docker-NLP/05_language_translation.py` 文件中。在文本或代码编辑器中打开 `05_language_translation.py` 以在以下步骤中探索其内容。

1. 导入所需的库。

   ```python
   from googletrans import Translator
   ```

   此行从 `googletrans` 导入 `Translator` 类。Googletrans 是一个 Python 库，提供对 Google Translate 的 AJAX API 的接口。

2. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   此 Python 习语确保以下代码块仅在此脚本作为主程序时运行。它提供了灵活性，允许脚本既作为独立程序又作为导入模块运行。

3. 创建一个用于连续输入的无限循环。

   ```python
      while True:
         input_text = input("Enter the text for translation (type 'exit' to end): ")

         if input_text.lower() == 'exit':
            print("Exiting...")
            break
   ```

   此处建立了一个无限循环，持续提示你输入文本，确保交互性。当你输入 `exit` 时循环中断，允许你有效控制应用程序流程。

4. 创建 Translator 实例。

   ```python
         translator = Translator()
   ```

   这创建了 Translator 类的实例，执行翻译。

5. 翻译文本。

   ```python
         translated_text = translator.translate(input_text, dest='fr').text
   ```

   此处调用 `translator.translate` 方法并传入用户输入。`dest='fr'` 参数指定翻译的目标语言为法语。`.text` 属性获取翻译后的字符串。有关可用语言代码的更多详细信息，请参阅 [Googletrans 文档](https://py-googletrans.readthedocs.io/en/latest/)。

6. 打印原始文本和翻译文本。

   ```python
         print(f"Original Text: {input_text}")
         print(f"Translated Text: {translated_text}")
   ```

   这两行打印用户输入的原始文本和翻译后的文本。

7. 创建 `requirements.txt`。示例应用程序已包含 `requirements.txt` 文件，用于指定应用程序导入的必要模块。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

   ```text
   ...

   # 05 language_translation
   googletrans==4.0.0-rc1
   ```

   语言翻译应用程序仅需要 `googletrans`。

## 探索应用程序环境

你将使用 Docker 在容器中运行应用程序。Docker 让你将应用程序容器化，提供一致且隔离的运行环境。这意味着应用程序将在其 Docker 容器内按预期运行，无论底层系统差异如何。

要在容器中运行应用程序，需要 Dockerfile。Dockerfile 是一个文本文档，包含组装镜像所需的所有命令。镜像是一个只读模板，包含创建 Docker 容器的指令。

示例应用程序已包含 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释 `Dockerfile` 的每个部分。更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令设置构建的基础。`python:3.8-slim` 是 Python 3.8 镜像的轻量版本，针对大小和速度进行了优化。使用此精简镜像可减少 Docker 镜像的整体大小，加快下载速度，并减少安全漏洞的攻击面。这对于可能不需要完整标准 Python 镜像的基于 Python 的应用程序特别有用。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 设置 Docker 镜像内的当前工作目录。通过将其设置为 `/app`，你确保 Dockerfile 中的所有后续命令（如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于组织 Docker 镜像，因为所有与应用程序相关的文件都包含在特定目录中。

3. 将需求文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从本地机器传输到 Docker 镜像中。此文件列出了应用程序所需的所有 Python 依赖项。将其复制到容器中允许下一个命令（`RUN pip install`）在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减少 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤针对需要 spaCy 库的 NLP 应用程序。它下载 `en_core_web_sm` 模型，这是 spaCy 的小型英语语言模型。虽然此应用程序不需要，但为了与其他可能使用此 Dockerfile 的 NLP 应用程序兼容而包含它。

6. 将应用程序代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将你的 Python 脚本和 `entrypoint.sh` 脚本复制到镜像的 `/app` 目录中。这很关键，因为容器需要这些脚本来运行应用程序。`entrypoint.sh` 脚本尤其重要，因为它决定了应用程序在容器内如何启动。

7. 设置 `entrypoint.sh` 脚本的权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 文件的权限，使其可执行。此步骤是必要的，以确保 Docker 容器可以运行此脚本来启动应用程序。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令配置容器在启动时自动运行 `entrypoint.sh` 作为默认可执行文件。

   你可以在代码或文本编辑器中打开 `entrypoint.sh` 脚本以探索其内容。由于示例包含多个应用程序，该脚本允许你在容器启动时指定要运行哪个应用程序。

## 运行应用程序

要使用 Docker 运行应用程序：

1. 构建镜像。

   在终端中，在 `Dockerfile` 所在目录内运行以下命令。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是命令的分解：

   - `docker build`：这是从 Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是位于指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志代表标签。它为镜像分配一个名称，在此情况下为 `basic-nlp`。标签是稍后引用镜像的便捷方式，特别是在将镜像推送到注册表或运行容器时。
   - `.`：这是命令的最后一部分，指定构建上下文。句点（`.`）表示当前目录。Docker 将在此目录中查找 Dockerfile。构建上下文（在本例中为当前目录）被发送到 Docker 守护进程以启用构建。它包括指定目录中的所有文件和子目录。

   有关更多详细信息，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向控制台输出多个日志。你将看到它下载并安装依赖项。根据你的网络连接，这可能需要几分钟。Docker 确实具有缓存功能，因此后续构建可能更快。完成后控制台将返回提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 05_language_translation.py
   ```

   以下是命令的分解：

   - `docker run`：这是从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：这即使未连接也保持标准输入（STDIN）打开。它允许容器在前台保持运行并具有交互性。
     - `-t` 或 `--tty`：这分配一个伪 TTY，本质上模拟终端，如命令提示符或 shell。它让你可以与容器内的应用程序交互。
   - `basic-nlp`：这指定用于创建容器的 Docker 镜像的名称。在本例中，它是你使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `05_language_translation.py`：这是你希望在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   有关更多详细信息，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   >
   > 对于 Windows 用户，运行容器时可能会遇到错误。验证 `entrypoint.sh` 中的行尾是 `LF`（`\n`）而不是 `CRLF`（`\r\n`），然后重建镜像。更多详细信息，请参阅 [避免意外语法错误，对容器中的文件使用 Unix 风格的行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line-endings-for-files-in-containers)。

   容器启动后，你将在控制台中看到以下内容。

   ```console
   Enter the text for translation (type 'exit' to end):
   ```

3. 测试应用程序。

   输入一些文本以获取文本翻译。

   ```console
   Enter the text for translation (type 'exit' to end): Hello, how are you doing?
   Original Text: Hello, how are you doing?
   Translated Text: Bonjour comment allez-vous?
   ```

## 总结

在本指南中，你学习了如何构建并运行语言翻译应用程序。你学习了如何使用 Python 和 Googletrans 构建应用程序，然后使用 Docker 设置环境并运行应用程序。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Googletrans](https://github.com/ssut/py-googletrans)
- [Python 文档](https://docs.python.org/3/)

## 后续步骤

探索更多 [自然语言处理指南](./_index.md)。