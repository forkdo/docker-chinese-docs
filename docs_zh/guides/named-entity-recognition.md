---
title: 构建一个命名实体识别应用
linkTitle: 命名实体识别
keywords: nlp, natural language processing, named entity recognition, python, spacy, ner
description: 学习如何使用 Python、spaCy 和 Docker 构建并运行一个命名实体识别应用。
summary: |
  本指南将指导你如何使用 Docker 容器化命名实体识别（NER）模型。
tags: [ai]
languages: [python]
aliases:
  - /guides/use-case/nlp/named-entity-recognition/
params:
  time: 20 分钟
---

## 概述

本指南将带你逐步构建并运行一个命名实体识别（NER）应用。你将使用 Python 和 spaCy 构建应用，然后使用 Docker 设置环境并运行该应用。

该应用会处理输入的文本，识别并打印出命名实体，例如人名、组织或地点。

## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 会定期添加新功能，本指南中的某些部分可能仅在 Docker Desktop 的最新版本中可用。
- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 获取示例应用

1. 打开终端，使用以下命令克隆示例应用的仓库。

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. 验证你已成功克隆仓库。

   在你的 `Docker-NLP` 目录中，你应该看到以下文件。

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

## 探索应用代码

命名实体识别应用的源代码位于 `Docker-NLP/02_name_entity_recognition.py` 文件中。在文本编辑器或代码编辑器中打开 `02_name_entity_recognition.py`，以便在接下来的步骤中探索其内容。

1. 导入所需的库。

   ```python
   import spacy
   ```

   这行代码导入了 `spaCy` 库。`spaCy` 是 Python 中一个流行的自然语言处理（NLP）库。

2. 加载语言模型。

   ```python
   nlp = spacy.load("en_core_web_sm")
   ```

   这里，`spacy.load` 函数加载了一个语言模型。`en_core_web_sm` 是一个小巧的英语语言模型，可用于各种 NLP 任务，包括分词、词性标注和命名实体识别。

3. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   这是 Python 的一种惯用写法，确保下面的代码块仅在该脚本作为主程序运行时执行。它提供了灵活性，使脚本既能作为独立程序运行，也能作为模块被导入。

4. 创建一个无限循环以持续接收输入。

   ```python
      while True:
   ```

   这个 while 循环会无限次运行，直到被显式中断。它允许用户持续输入文本进行实体识别，直到决定退出为止。

5. 获取用户输入。

   ```python
   input_text = input("Enter the text for entity recognition (type 'exit' to end): ")
   ```

   这行代码提示用户输入文本。程序将对输入的文本执行实体识别。

6. 定义退出条件。

   ```python
   if input_text.lower() == 'exit':
      print("Exiting...")
      break
   ```

   如果用户输入的内容转换为小写后等于 `exit`，程序会打印 **Exiting...** 并跳出 while 循环，从而结束程序。

7. 执行命名实体识别。

   ```python
   doc = nlp(input_text)

   for ent in doc.ents:
      print(f"Entity: {ent.text}, Type: {ent.label_}")
   ```

   - `doc = nlp(input_text)`：这里，nlp 模型处理用户输入的文本，生成一个 Doc 对象，该对象包含各种 NLP 属性，包括识别出的实体。
   - `for ent in doc.ents:`：这个循环遍历文本中找到的实体。
   - `print(f"Entity: {ent.text}, Type: {ent.label_}")`：对于每个实体，它会打印出实体文本及其类型（如 PERSON、ORG 或 GPE）。

8. 创建 `requirements.txt`。

   示例应用已包含 `requirements.txt` 文件，用于指定应用导入所需的包。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

   ```text
   # 02 named_entity_recognition
   spacy==3.7.2

   ...
   ```

   命名实体识别应用只需要 `spacy` 包。

## 探索应用环境

你将使用 Docker 在容器中运行应用。Docker 可以将应用容器化，提供一致且隔离的运行环境。这意味着应用将在其 Docker 容器内按预期运行，不受底层系统差异的影响。

要在容器中运行应用，需要一个 Dockerfile。Dockerfile 是一个文本文档，包含组装镜像所需的所有命令。镜像（image）是一个只读模板，包含创建 Docker 容器的指令。

示例应用已包含一个 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释了 `Dockerfile` 的每个部分。更多详细信息，请参阅 [Dockerfile 参考文档](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令为构建设置基础。`python:3.8-slim` 是 Python 3.8 镜像的轻量版本，针对大小和速度进行了优化。使用此精简镜像可减少 Docker 镜像的总体大小，从而加快下载速度，并减少安全漏洞的攻击面。这对于不需要完整标准 Python 镜像的 Python 应用特别有用。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 设置 Docker 镜像内的当前工作目录。通过将其设置为 `/app`，可确保 Dockerfile 中的所有后续命令（如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于组织 Docker 镜像，因为所有与应用相关的文件都包含在特定目录中。

3. 将依赖文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从本地机器传输到 Docker 镜像中。此文件列出了应用所需的所有 Python 依赖项。将其复制到容器中，下一步命令（`RUN pip install`）就可以在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减少 Docker 镜像的大小。

5. 运行额外命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤针对需要 spaCy 库的 NLP 应用。它下载 `en_core_web_sm` 模型，这是 spaCy 的小规模英语语言模型。

6. 将应用代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将 Python 脚本和 `entrypoint.sh` 脚本复制到镜像的 `/app` 目录中。这很关键，因为容器需要这些脚本才能运行应用。`entrypoint.sh` 脚本尤其重要，它决定了应用在容器内如何启动。

7. 设置 `entrypoint.sh` 脚本的权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 文件的权限，使其可执行。此步骤是必要的，以确保 Docker 容器能够运行此脚本启动应用。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令配置容器在启动时自动运行 `entrypoint.sh` 作为默认可执行文件。这意味着当容器启动时，它会自动执行该脚本。

   你可以在代码或文本编辑器中打开 `entrypoint.sh` 脚本以进一步探索。由于示例包含多个应用，该脚本允许你在容器启动时指定要运行哪个应用。

## 运行应用

使用 Docker 运行应用的步骤如下：

1. 构建镜像。

   在终端中，于 `Dockerfile` 所在目录运行以下命令。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是命令的详细说明：

   - `docker build`：这是从 Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是在指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志代表标签（tag）。它为镜像分配一个名称，在本例中为 `basic-nlp`。标签是稍后引用镜像的便捷方式，尤其是在将镜像推送到注册表或运行容器时。
   - `.`：这是命令的最后一部分，指定构建上下文。句点（`.`）表示当前目录。Docker 将在此目录中查找 Dockerfile。构建上下文（在本例中为当前目录）会被发送到 Docker 守护进程以启用构建，它包含指定目录中的所有文件和子目录。

   更多详细信息，请参阅 [docker build CLI 参考文档](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向控制台输出多个日志。你将看到它下载并安装依赖项。根据你的网络连接，这可能需要几分钟。Docker 具有缓存功能，因此后续构建可能更快。完成后，控制台将返回提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 02_name_entity_recognition.py
   ```

   以下是命令的详细说明：

   - `docker run`：这是从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：此选项即使未附加也保持标准输入（STDIN）打开。它允许容器在前台保持运行并具有交互性。
     - `-t` 或 `--tty`：此选项分配一个伪 TTY，本质上模拟终端（如命令提示符或 shell）。它使你能够与容器内的应用交互。
   - `basic-nlp`：这指定用于创建容器的 Docker 镜像的名称。在本例中，它是你使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `02_name_entity_recognition.py`：这是你希望在 Docker 容器内运行的脚本。它会被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   更多详细信息，请参阅 [docker run CLI 参考文档](/reference/cli/docker/container/run/)。

   > [!NOTE]
   >
   > 对于 Windows 用户，运行容器时可能会遇到错误。请验证 `entrypoint.sh` 中的行结尾是 `LF`（`\n`）而不是 `CRLF`（`\r\n`），然后重建镜像。更多详细信息，请参阅 [避免意外的语法错误，在容器中使用 Unix 风格的行结尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line-endings-for-files-in-containers)。

   容器启动后，你将在控制台中看到以下内容。

   ```console
   Enter the text for entity recognition (type 'exit' to end):
   ```

3. 测试应用。

   输入一些信息以获取命名实体识别结果。

   ```console
   Enter the text for entity recognition (type 'exit' to end): Apple Inc. is planning to open a new store in San Francisco. Tim Cook is the CEO of Apple.

   Entity: Apple Inc., Type: ORG
   Entity: San Francisco, Type: GPE
   Entity: Tim Cook, Type: PERSON
   Entity: Apple, Type: ORG
   ```

## 总结

本指南演示了如何构建并运行一个命名实体识别应用。你学习了如何使用 Python 和 spaCy 构建应用，然后使用 Docker 设置环境并运行该应用。

相关信息：

- [Docker CLI 参考文档](/reference/cli/docker/)
- [Dockerfile 参考文档](/reference/dockerfile/)
- [spaCy](https://spacy.io/)
- [Python 文档](https://docs.python.org/3/)

## 后续步骤

探索更多 [自然语言处理指南](./_index.md)。