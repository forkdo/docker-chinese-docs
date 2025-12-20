# 构建文本摘要应用

## 概述

在本指南中，您将学习如何构建和运行文本摘要应用。您将使用 Python 和 Bert Extractive Summarizer 构建应用，然后使用 Docker 设置环境并运行该应用。

示例文本摘要应用使用 Bert Extractive Summarizer。该工具利用 HuggingFace Pytorch transformers 库执行抽取式摘要。其工作原理是首先嵌入句子，然后运行聚类算法，找到最接近聚类中心的句子。

## 前提条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 会定期添加新功能，本指南的某些部分可能仅适用于最新版本的 Docker Desktop。
- 您拥有 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但您可以使用任何客户端。

## 获取示例应用

1. 打开终端，使用以下命令克隆示例应用的仓库。

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. 验证是否已克隆仓库。

   您应该在 `Docker-NLP` 目录中看到以下文件。

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

文本摘要应用的源代码位于 `Docker-NLP/04_text_summarization.py` 文件中。在文本或代码编辑器中打开 `04_text_summarization.py`，按以下步骤探索其内容。

1. 导入所需的库。

   ```python
   from summarizer import Summarizer
   ```

   这行代码从 `summarizer` 包导入 `Summarizer` 类，这对您的文本摘要应用至关重要。summarizer 模块实现了 Bert Extractive Summarizer，利用了在 NLP（自然语言处理）领域著名的 HuggingFace Pytorch transformers 库。该库提供对 BERT 等预训练模型的访问，这些模型彻底改变了包括文本摘要在内的语言理解任务。

   BERT 模型（Bidirectional Encoder Representations from Transformers）擅长理解语言中的上下文，使用一种称为“注意力”的机制来确定单词在句子中的重要性。对于摘要，该模型会嵌入句子，然后使用聚类算法识别关键句子，即最接近这些聚类中心的句子，从而有效地捕捉文本的主要思想。

2. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   这个 Python 惯用法确保仅当此脚本是主程序时，才会运行后续代码块。它提供了灵活性，允许脚本既作为独立程序运行，也作为导入模块运行。

3. 创建一个用于持续输入的无限循环。

   ```python
      while True:
         input_text = input("Enter the text for summarization (type 'exit' to end): ")

         if input_text.lower() == 'exit':
            print("Exiting...")
            break
   ```

   一个无限循环会持续提示您输入文本，确保交互性。当您输入 `exit` 时，循环会中断，从而可以有效地控制应用流程。

4. 创建 Summarizer 的实例。

   ```python
         bert_model = Summarizer()
   ```

   在这里，您创建了一个名为 `bert_model` 的 Summarizer 类实例。此实例现在已准备好使用 BERT 模型执行摘要任务，将嵌入句子和聚类等复杂过程简化为一个易于访问的接口。

5. 生成并打印摘要。

   ```python
   summary = bert_model(input_text)
   print(summary)
   ```

   您的输入文本由 bert_model 实例处理，然后返回一个摘要版本。这展示了 Python 高级库的强大功能，能够以最少的代码实现复杂操作。

6. 创建 `requirements.txt`。示例应用已包含 `requirements.txt` 文件，用于指定应用导入所需的必要模块。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

   ```text
   ...

   # 04 text_summarization
   bert-extractive-summarizer==0.10.1

   ...

   torch==2.1.2
   ```

   文本摘要应用需要 `bert-extractive-summarizer` 和 `torch` 模块。summarizer 模块生成输入文本的摘要。这需要 PyTorch，因为用于生成摘要的底层 BERT 模型是用 PyTorch 实现的。

## 探索应用环境

您将使用 Docker 在容器中运行应用。Docker 允许您将应用容器化，为其提供一致且隔离的运行环境。这意味着应用将在其 Docker 容器内按预期运行，而不管底层系统的差异如何。

要在容器中运行应用，需要 Dockerfile。Dockerfile 是一个文本文档，其中包含您在命令行上调用以构建镜像的所有命令。镜像是一个只读模板，包含用于创建 Docker 容器的指令。

示例应用已包含 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释了 `Dockerfile` 的每个部分。更多详情，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令为构建奠定基础。`python:3.8-slim` 是 Python 3.8 镜像的轻量级版本，针对大小和速度进行了优化。使用此精简镜像可以减小 Docker 镜像的整体大小，从而加快下载速度并减少安全漏洞的攻击面。这对于基于 Python 的应用特别有用，因为您可能不需要完整的标准 Python 镜像。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 设置 Docker 镜像内的当前工作目录。通过将其设置为 `/app`，您可以确保 Dockerfile 中的所有后续命令（如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于组织您的 Docker 镜像，因为所有与应用相关的文件都包含在特定目录中。

3. 将 requirements 文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从您的本地机器传输到 Docker 镜像中。此文件列出了应用所需的所有 Python 依赖项。将其复制到容器中可以让下一个命令（`RUN pip install`）在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）来安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减小 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤特定于需要 spaCy 库的 NLP 应用。它下载 `en_core_web_sm` 模型，这是 spaCy 的小型英语语言模型。虽然此应用不需要它，但为了与其他可能使用此 Dockerfile 的 NLP 应用兼容而包含在内。

6. 将应用代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将您的 Python 脚本和 `entrypoint.sh` 脚本复制到镜像的 `/app` 目录中。这至关重要，因为容器需要这些脚本来运行应用。`entrypoint.sh` 脚本尤为重要，因为它决定了容器内应用的启动方式。

7. 为 `entrypoint.sh` 脚本设置权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 的文件权限，使其可执行。此步骤对于确保 Docker 容器可以运行此脚本来启动应用是必要的。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令配置容器以运行 `entrypoint.sh` 作为其默认可执行文件。这意味着当容器启动时，它会自动执行该脚本。

   您可以通过在代码或文本编辑器中打开 `entrypoint.sh` 脚本来探索它。由于示例包含多个应用，该脚本允许您指定容器启动时要运行哪个应用。

## 运行应用

要使用 Docker 运行应用：

1. 构建镜像。

   在终端中，在 `Dockerfile` 所在的目录内运行以下命令。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是该命令的分解说明：

   - `docker build`：这是用于从 Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志代表标签。它为镜像分配一个名称，在本例中为 `basic-nlp`。标签是以后引用镜像的便捷方式，尤其是在将它们推送到注册表或运行容器时。
   - `.`：这是命令的最后一部分，指定构建上下文。句点 (`.`) 表示当前目录。Docker 将在此目录中查找 Dockerfile。构建上下文（在本例中为当前目录）会发送到 Docker 守护进程以启用构建。它包括指定目录中的所有文件和子目录。

   更多详情，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向您的控制台输出多个日志。您将看到它下载并安装依赖项。根据您的网络连接，这可能需要几分钟。Docker 确实具有缓存功能，因此后续构建可以更快。完成后，控制台将返回到提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 04_text_summarization.py
   ```

   以下是该命令的分解说明：

   - `docker run`：这是用于从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：即使未连接，也保持标准输入 (STDIN) 打开。它允许容器在前台保持运行并具有交互性。
     - `-t` 或 `--tty`：这会分配一个伪 TTY，本质上是模拟终端，如命令提示符或 shell。它使您能够与容器内的应用进行交互。
   - `basic-nlp`：这指定用于创建容器的 Docker 镜像的名称。在本例中，它是您使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `04_text_summarization.py`：这是您要在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   更多详情，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   >
   > 对于 Windows 用户，在运行容器时可能会遇到错误。验证 `entrypoint.sh` 中的行尾是否为 `LF` (`\n`) 而不是 `CRLF` (`\r\n`)，然后重新构建镜像。更多详情，请参阅 [避免意外的语法错误，对容器中的文件使用 Unix 风格的行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers)。

   容器启动后，您将在控制台中看到以下内容。

   ```console
   Enter the text for summarization (type 'exit' to end):
   ```

3. 测试应用。

   输入一些文本以获取文本摘要。

   ```console
   Enter the text for summarization (type 'exit' to end): Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making. AI technologies can be classified into two main types: narrow or weak AI, which is designed for a particular task, and general or strong AI, which possesses the ability to understand, learn, and apply knowledge across various domains. One of the most popular approaches in AI is machine learning, where algorithms are trained on large datasets to recognize patterns and make predictions.

   Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making.
   ```

## 总结

在本指南中，您学习了如何构建和运行文本摘要应用。您学习了如何使用 Python 和 Bert Extractive Summarizer 构建应用，然后使用 Docker 设置环境并运行该应用。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Bert Extractive Summarizer](https://github.com/dmmiller612/bert-extractive-summarizer)
- [PyTorch](https://pytorch.org/)
- [Python 文档](https://docs.python.org/3/)

## 下一步

探索更多[自然语言处理指南](./_index.md)。
