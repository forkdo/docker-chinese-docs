--- 
title: 使用 Docker 的 AI 助手进行迁移
linktitle: AI 辅助迁移
description: 使用 Docker 的 AI 助手自动将 Dockerfile 迁移至 Docker Hardened Images
weight: 15
keywords: ai 助手, 迁移 dockerfile, docker hardened images, 自动迁移
params:
  sidebar:
    badge:
      color: violet
      text: 实验性功能
---

{{< summary-bar feature_name="Ask Gordon DHI 迁移" >}}

你可以使用 Docker 的 AI 助手，自动将 Dockerfile 迁移至 Docker Hardened Images (DHI)。

1. 确保已 [启用](/manuals/ai/gordon.md#enable-ask-gordon) Docker 的 AI 助手。
2. 在终端中，导航至包含 Dockerfile 的目录。
3. 启动与助手的对话：
   ```bash
   docker ai
   ```
4. 输入：
   ```console
   "将我的 dockerfile 迁移至 DHI"
   ```
5. 按照助手的对话进行操作。助手将编辑你的 Dockerfile，当它请求访问文件系统等资源时，输入 `yes` 允许助手继续。

迁移完成后，你会看到成功消息：

```text
Docker Hardened Images (DHI) 的迁移已完成。更新后的 Dockerfile 成功构建了镜像，
最终镜像中未检测到任何漏洞。原始 Dockerfile 的功能和优化已得到保留。
```

> [!IMPORTANT]
>
> 与任何 AI 工具一样，你必须验证助手的编辑并测试你的镜像。