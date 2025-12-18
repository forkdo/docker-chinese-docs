---
title: 构建一个文本识别应用
linkTitle: 文本分类
keywords: nlp, natural language processing, sentiment analysis, python, nltk, scikit-learn, text classification
description: 了解如何使用 Python、NLTK、scikit-learn 和 Docker 构建并运行一个文本识别应用。
summary: |
  本指南详细介绍了如何使用 Docker 容器化文本分类模型。
tags: [ai]
languages: [python]
aliases:
  - /guides/use-case/nlp/text-classification/
params:
  time: 20 分钟
---

## 概述

在本指南中，你将学习如何创建并运行一个文本识别应用。你将使用 Python 配合 scikit-learn 和自然语言工具包（NLTK）来构建该应用。然后，你将设置环境并使用 Docker 运行该应用。

该应用使用 NLTK 的 SentimentIntensityAnalyzer 分析用户输入文本的情感倾向。它允许用户输入文本，然后处理该文本以确定其情感，并将其分类为正面或负面。此外，它还会基于预定义的数据集显示其情感分析模型的准确率和详细的分类报告。

## 前置条件

- 你已安装最新版本的 [Docker Desktop](/get-started/get-docker.md)。Docker 定期添加新功能，本指南中的某些部分可能仅在 Docker Desktop 的最新版本中有效。
- 你已安装 [Git 客户端](https://git-scm.com/downloads)。本节示例使用基于命令行的 Git 客户端，但你可以使用任何客户端。

## 获取示例应用

1. 打开终端，使用以下命令克隆示例应用的仓库。

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

## 探索应用代码

文本分类应用的源代码位于 `Docker-NLP/03_text_classification.py` 文件中。在文本或代码编辑器中打开 `03_text_classification.py` 以在以下步骤中探索其内容。

1. 导入所需的库。

   ```python
   import nltk
   from nltk.sentiment import SentimentIntensityAnalyzer
   from sklearn.metrics import accuracy_score, classification_report
   from sklearn.model_selection import train_test_split
   import ssl
   ```

   - `nltk`：一个流行的 Python 自然语言处理（NLP）库。
   - `SentimentIntensityAnalyzer`：`nltk` 中用于情感分析的组件。
   - `accuracy_score`、`classification_report`：来自 scikit-learn 的用于评估模型的函数。
   - `train_test_split`：来自 scikit-learn 的将数据集拆分为训练集和测试集的函数。
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

   此代码块是针对某些环境中通过 NLTK 下载数据可能因 SSL 证书验证问题而失败的情况的变通方案。它告诉 Python 忽略 HTTPS 请求的 SSL 证书验证。

3. 下载 NLTK 资源。

   ```python
   nltk.download('vader_lexicon')
   ```

   `vader_lexicon` 是 `SentimentIntensityAnalyzer` 用于情感分析的词典。

4. 定义测试文本及对应的标签。

   ```python
   texts = [...]
   labels = [0, 1, 2, 0, 1, 2]
   ```

   此部分定义了一小组文本及其对应的标签（0 表示正面，1 表示负面，2 表示垃圾信息）。

5. 拆分测试数据。

   ```python
   X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
   ```

   此部分将数据集拆分为训练集和测试集，其中 20% 的数据作为测试集。由于此应用使用预训练模型，因此不会训练模型。

6. 设置情感分析。

   ```python
   sia = SentimentIntensityAnalyzer()
   ```

   此代码初始化 `SentimentIntensityAnalyzer` 以分析文本的情感倾向。

7. 为测试数据生成预测和分类。

   ```python
   vader_predictions = [sia.polarity_scores(text)["compound"] for text in X_test]
   threshold = 0.2
   vader_classifications = [0 if score > threshold else 1 for score in vader_predictions]
   ```

   此部分为测试集中的每个文本生成情感分数，并根据阈值将其分类为正面或负面。

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

   此 Python 习语确保以下代码块仅在该脚本作为主程序时运行。它提供了灵活性，允许脚本既可作为独立程序又可作为导入模块运行。

10. 创建一个无限循环以持续输入。

    ```python
       while True:
        input_text = input("Enter the text for classification (type 'exit' to end): ")

          if input_text.lower() == 'exit':
             print("Exiting...")
             break
    ```

    此 while 循环无限运行，直到显式中断。它允许用户持续输入文本进行实体识别，直到决定退出。

11. 分析文本。

    ```python
            input_text_score = sia.polarity_scores(input_text)["compound"]
            input_text_classification = 0 if input_text_score > threshold else 1
    ```

12. 打印 VADER 分类报告和情感分析。

    ```python
            print(f"Accuracy: {accuracy:.2f}")
            print("\nVADER Classification Report:")
            print(report_vader)

            print(f"\nTest Text (Positive): '{input_text}'")
            print(f"Predicted Sentiment: {'Positive' if input_text_classification == 0 else 'Negative'}")
    ```

13. 创建 `requirements.txt`。示例应用已包含 `requirements.txt` 文件，用于指定应用导入的必要包。在代码或文本编辑器中打开 `requirements.txt` 以探索其内容。

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

你将使用 Docker 在容器中运行应用。Docker 让你可以容器化应用，为运行它提供一致且隔离的环境。这意味着应用将在其 Docker 容器中按预期运行，无论底层系统的差异如何。

要在容器中运行应用，需要 Dockerfile。Dockerfile 是一个文本文档，包含组装镜像所需的所有命令。镜像是一个只读模板，包含创建 Docker 容器的指令。

示例应用已包含 `Dockerfile`。在代码或文本编辑器中打开 `Dockerfile` 以探索其内容。

以下步骤解释 `Dockerfile` 的每个部分。更多详情，请参阅 [Dockerfile 参考](/reference/dockerfile/)。

1. 指定基础镜像。

   ```dockerfile
   FROM python:3.8-slim
   ```

   此命令设置构建的基础。`python:3.8-slim` 是 Python 3.8 镜像的轻量版本，针对大小和速度进行了优化。使用此精简镜像可减少 Docker 镜像的整体大小，从而加快下载速度并减少安全漏洞的攻击面。这对于可能不需要完整标准 Python 镜像的基于 Python 的应用特别有用。

2. 设置工作目录。

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` 在 Docker 镜像内设置当前工作目录。通过将其设置为 `/app`，你确保 Dockerfile 中的所有后续命令（如 `COPY` 和 `RUN`）都在此目录中执行。这也有助于组织 Docker 镜像，因为所有与应用相关的文件都包含在特定目录中。

3. 将需求文件复制到镜像中。

   ```dockerfile
   COPY requirements.txt /app
   ```

   `COPY` 命令将 `requirements.txt` 文件从你的本地机器传输到 Docker 镜像中。此文件列出了应用所需的所有 Python 依赖项。将其复制到容器中可以让下一个命令（`RUN pip install`）在镜像环境中安装这些依赖项。

4. 在镜像中安装 Python 依赖项。

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   此行使用 `pip`（Python 的包安装程序）安装 `requirements.txt` 中列出的包。`--no-cache-dir` 选项禁用缓存，通过不存储不必要的缓存数据来减少 Docker 镜像的大小。

5. 运行其他命令。

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   此步骤针对需要 spaCy 库的 NLP 应用。它下载 `en_core_web_sm` 模型，这是 spaCy 的小型英语语言模型。虽然此应用不需要，但为了与其他可能使用此 Dockerfile 的 NLP 应用兼容而包含它。

6. 将应用代码复制到镜像中。

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   这些命令将你的 Python 脚本和 `entrypoint.sh` 脚本复制到镜像的 `/app` 目录中。这很关键，因为容器需要这些脚本来运行应用。`entrypoint.sh` 脚本尤其重要，因为它决定了应用在容器内如何启动。

7. 设置 `entrypoint.sh` 脚本的权限。

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   此命令修改 `entrypoint.sh` 文件的权限，使其可执行。此步骤是必要的，以确保 Docker 容器可以运行此脚本来启动应用。

8. 设置入口点。

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   `ENTRYPOINT` 指令配置容器在启动时自动执行 `entrypoint.sh` 作为默认可执行文件。这意味着当容器启动时，它会自动执行该脚本。

   你可以在代码或文本编辑器中打开 `entrypoint.sh` 脚本以探索其内容。由于示例包含多个应用，该脚本允许你在容器启动时指定要运行哪个应用。

## 运行应用

使用 Docker 运行应用：

1. 构建镜像。

   在终端中，运行以下命令（在 `Dockerfile` 所在目录中）。

   ```console
   $ docker build -t basic-nlp .
   ```

   以下是该命令的分解：

   - `docker build`：这是从 Dockerfile 和上下文构建 Docker 镜像的主要命令。上下文通常是位于指定位置的一组文件，通常是包含 Dockerfile 的目录。
   - `-t basic-nlp`：这是用于标记镜像的选项。`-t` 标志表示标签。它为镜像分配一个名称，在此情况下为 `basic-nlp`。标签是稍后引用镜像的便捷方式，尤其是在推送到注册表或运行容器时。
   - `.`：这是命令的最后一部分，指定构建上下文。句点（`.`）表示当前目录。Docker 将在此目录中查找 Dockerfile。构建上下文（在本例中为当前目录）被发送到 Docker 守护进程以启用构建。它包括指定目录中的所有文件和子目录。

   更多详情，请参阅 [docker build CLI 参考](/reference/cli/docker/buildx/build/)。

   Docker 在构建镜像时会向你的控制台输出多个日志。你将看到它下载并安装依赖项。根据你的网络连接，这可能需要几分钟。Docker 确实具有缓存功能，因此后续构建可能更快。完成后，控制台将返回提示符。

2. 将镜像作为容器运行。

   在终端中，运行以下命令。

   ```console
   $ docker run -it basic-nlp 03_text_classification.py
   ```

   以下是该命令的分解：

   - `docker run`：这是从 Docker 镜像运行新容器的主要命令。
   - `-it`：这是两个选项的组合：
     - `-i` 或 `--interactive`：这保持标准输入（STDIN）打开，即使未连接。它让容器保持在前台运行并具有交互性。
     - `-t` 或 `--tty`：这分配一个伪 TTY，本质上模拟终端，如命令提示符或 shell。它让你可以与容器内的应用交互。
   - `basic-nlp`：这指定用于创建容器的 Docker 镜像的名称。在本例中，它是你使用 `docker build` 命令创建的名为 `basic-nlp` 的镜像。
   - `03_text_classification.py`：这是你想要在 Docker 容器内运行的脚本。它被传递给 `entrypoint.sh` 脚本，该脚本在容器启动时运行它。

   更多详情，请参阅 [docker run CLI 参考](/reference/cli/docker/container/run/)。

   > [!NOTE]
   >
   > 对于 Windows 用户，运行容器时可能会遇到错误。验证 `entrypoint.sh` 中的行结尾是 `LF`（`\n`）而不是 `CRLF`（`\r\n`），然后重建镜像。更多详情，请参阅 [避免意外的语法错误，对容器中的文件使用 Unix 风格的行结尾](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line-endings-for-files-in-containers)。

   容器启动后，你将在控制台中看到以下内容。

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

在本指南中，你学习了如何构建并运行一个文本分类应用。你学习了如何使用 Python 配合 scikit-learn 和 NLTK 构建应用。然后你学习了如何设置环境并使用 Docker 运行应用。

相关信息：

- [Docker CLI 参考](/reference/cli/docker/)
- [Dockerfile 参考](/reference/dockerfile/)
- [自然语言工具包](https://www.nltk.org/)
- [Python 文档](https://docs.python.org/3/)
- [scikit-learn](https://scikit-learn.org/)

## 后续步骤

探索更多 [自然语言处理指南](./_index.md)。