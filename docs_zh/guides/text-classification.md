---
title: 构建文本识别应用
linkTitle: 文本分类
keywords: nlp, 自然语言处理, 情感分析, python, nltk, scikit-learn, 文本分类
description: 学习如何使用 Python、NLTK、scikit-learn 和 Docker 构建并运行文本识别应用。
summary: |
  本指南详细介绍如何使用 Docker 容器化文本分类模型。
tags: [ai]
languages: [python]
aliases:
  - /guides/use-case/nlp/text-classification/
params:
  time: 20 分钟
---

## 概述

在本指南中，您将学习如何创建和运行一个文本识别应用。您将使用 Python 结合 scikit-learn 和自然语言工具包 (NLTK) 来构建该应用。然后，您将设置环境并使用 Docker 运行该应用。

该应用使用 NLTK 的 `SentimentIntensityAnalyzer` 分析用户输入文本的情感。它允许用户输入文本，然后对文本进行处理以确定其情感，将其分类为正面或负面。此外，它还会根据预定义的数据集显示模型的准确率和详细分类报告。

## 前提条件

- 您已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 会定期添加新功能，本指南的某些部分可能仅在最新版本的 Docker Desktop 中有效。
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

文本分类应用的源代码位于 `Docker-NLP/03_text_classification.py` 文件中。在文本或代码编辑器中打开 `03_text_classification.py`，按以下步骤探索其内容。

1. 导入所需的库。

   ```python
   import nltk
   from nltk.sentiment import SentimentIntensityAnalyzer
   from sklearn.metrics import accuracy_score, classification_report
   from sklearn.model_selection import train_test_split
   import ssl
   ```

   - `nltk`：用于自然语言处理 (NLP) 的流行 Python 库。
   - `SentimentIntensityAnalyzer`：`nltk` 中用于情感分析的组件。
   - `accuracy_score`、`classification_report`：来自 scikit-learn 的用于评估模型的函数。
   - `train_test_split`：来自 scikit-learn 的用于将数据集拆分为训练集和测试集的函数。
   - `ssl`：用于处理在为 `nltk` 下载数据时可能发生的 SSL 证书问题。

2. 处理 SSL 证书验证。

   ```python
   try:
       _create_unverified_https_context = ssl._create_unverified_context
   except AttributeError:
       pass
   else:
       ssl._create_default_https_context = _create_unverified_https_context
   ```

   此代码块是针对某些环境的变通方法，在这些环境中，通过 NLTK 下载数据可能会因 SSL 证书验证问题而失败。它告诉 Python 忽略 HTTPS 请求的 SSL 证书验证。

3. 下载 NLTK 资源。

   ```python
   nltk.download('vader_lexicon')
   ```

   `vader_lexicon` 是 `SentimentIntensityAnalyzer` 用于情感分析的词典。

4. 定义用于测试的文本和相应的标签。

   ```python
   texts = [...]
   labels = [0, 1, 2, 0, 1, 2]
   ```

   此部分定义了一个小型数据集，包含文本及其对应的标签（0 表示正面，1 表示负面，2 表示垃圾信息）。

5. 拆分测试数据。

   ```python
   X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
   ```

   此部分将数据集拆分为训练集和测试集，其中 20% 的数据作为测试集。由于此应用使用预训练模型，因此不会训练模型。

6. 设置情感分析。

   ```python
   sia = SentimentIntensityAnalyzer()
   ```

   此代码初始化 `SentimentIntensityAnalyzer` 以分析文本的情感。

7. 为测试数据生成预测和分类。

   ```python
   vader_predictions = [sia.polarity_scores(text)["compound"] for text in X_test]
   threshold = 0.2
   vader_classifications = [0 if score > threshold else 1 for score in vader_predictions]
   ```

   此部分为测试集中的每个文本生成情感得分，并根据阈值将它们分类为正面或负面。

8. 评估模型。

   ```python
   accuracy = accuracy_score(y_test, vader_classifications)
   report_vader = classification_report(y_test, vader_classifications, zero_division='warn')
   ```

   此部分计算预测的准确率和分类报告。

9. 指定主执行块。

   ```python
   if __name__ == "__main__":
   ```

   此 Python 惯用法确保仅当此脚本是主程序时，才会运行以下代码块。它提供了灵活性，允许脚本既作为独立程序运行，也作为导入的模块运行。

10. 创建一个用于连续输入的无限循环。

    ```python
       while True:
        input_text = input("Enter the text for classification (type 'exit' to end): ")

          if input_text.lower() == 'exit':
             print("Exiting...")
             break
    ```

    此 while 循环无限运行，直到显式中断。它允许用户连续输入文本进行实体识别，直到他们决定退出。

11. 分析文本。

    ```python
            input_text_score = sia.polarity_scores(input_text)["compound"]
            input_text_classification = 0 if input_text_score > threshold else 1
    ```

12. 打印 VADER 分类报告和情感分析结果。

    ```python
            print(f"Accuracy: {accuracy:.2f}")
            print("\nVADER Classification Report:")
            print(report_vader)

            print(f"\nTest Text (Positive): '{input_text}'")
            print(f"Predicted Sentiment: {'Positive' if input_text_classification == 0 else 'Negative'}")
    ```

13. 创建 `requirements.txt`。示例应用已包含 `requirements.txt` 文件，用于指定应用导入所需的必要包。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

    ```text
    # 01 sentiment_analysis
    nltk==3.6.5

    ...

    # 03 text_classification
    scikit-learn==1.3.2

    ...
    ```

    文本分类应用需要 `nltk` 和 `scikit-learn` 模块。

## 探索应用环境

您将使用 Docker 在容器中运行该应用。Docker 允许您将应用容器化，为其提供一致且隔离的运行环境。这意味着应用在其 Docker 容器内将按预期运行，而不管底层系统的差异如何。

要在容器中运行应用，需要一个 Dockerfile。Dockerfile 是一个文本文档，其中包含您在命令行上调用以组装镜像的所有命令。镜像是一个只读模板，包含用于创建 Docker 容器的指令。

示例应用已包含一个 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释了 `Dockerfile` 的每个部分。有关更多详细信息，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

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

   `COPY` 命令将 `requirements.txt` 文件从您的本地机器传输到 Docker 镜像中。此文件列出了应用所需的所有 Python 依赖项。将其复制到容器中可以让下一个命令 (`RUN pip install`) 在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）来安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减小 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤特定于需要 spaCy 库的 NLP 应用。它下载 `en_core_web_sm` 模型，这是 spaCy 的小型英语语言模型。虽然此应用不需要它，但为了与其他可能使用此 Dockerfile 的 NLP 应用兼容而包含它。

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

   `ENTRYPOINT` 指令将容器配置为运行 `entrypoint.sh` 作为其默认可执行文件。这意味着当容器启动时，它会自动执行该脚本。

   您可以通过在代码或文本编辑器中打开 `entrypoint.sh` 脚本来探索它。由于示例包含多个应用，该脚本允许您指定容器启动时要运行的应用。

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

   有关更多详细信息，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向您的控制台输出多个日志。您将看到它下载并安装依赖项。根据您的网络连接，这可能需要几分钟。Docker 确实具有缓存功能，因此后续构建可以更快。完成后，控制台将返回到提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 03_text_classification.py
   ```

   以下是该命令的分解说明：

   - `docker run`：这是用于从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：即使未附加，也保持标准输入 (STDIN) 打开。它让容器保持在前台运行并具有交互性。
     - `-t` 或 `--tty`：分配一个伪 TTY，本质上模拟一个终端，如命令提示符或 shell。它让您能够与容器内的应用进行交互。
   - `basic-nlp`：指定用于创建容器的 Docker 镜像的名称。在本例中，它是您使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `03_text_classification.py`：这是您要在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   有关更多详细信息，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   >
   > 对于 Windows 用户，在运行容器时可能会收到错误。验证 `entrypoint.sh` 中的行尾是否为 `LF` (`\n`) 而不是 `CRLF` (`\r\n`)，然后重新构建镜像。有关更多详细信息，请参阅 [避免意外的语法错误，对容器中的文件使用 Unix 样式行尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers)。

   容器启动后，您将在控制台中看到以下内容。

   ```console
   Enter the text for classification (type 'exit' to end):
   ```

3. 测试应用。

   输入一些文本以获取文本分类。

   ```console
   Enter the text for classification (type 'exit' to end): I love containers!
   Accuracy: 1.00

   VADER Classification Report:
                 precision    recall  f1-score   support

              0       1.00      1.00      1.00         1
              1       1.00      1.00      1.00         1

       accuracy                           1.00         2
      macro avg       1.00      1.00      1.00         2
   weighted avg       1.00      1.00      1.00         2

   Test Text (Positive): 'I love containers!'
   Predicted Sentiment: Positive
   ```

## 总结

在本指南中，您学习了如何构建和运行文本分类应用。您学习了如何使用 Python 结合 scikit-learn 和 NLTK 构建应用。然后，您学习了如何设置环境并使用 Docker 运行该应用。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [Natural Language Toolkit](https://www.nltk.org/)
- [Python 文档](https://docs.python.org/3/)
- [scikit-learn](https://scikit-learn.org/)

## 下一步

探索更多[自然语言处理指南](./_index.md)。