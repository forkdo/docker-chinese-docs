--- 
title: 使用 Docker 的 AI 助手进行迁移
linktitle: AI 辅助迁移
description: 使用 Docker 的 AI 助手自动将您的 Dockerfile 迁移至 Docker 强化镜像 (DHI)
weight: 15
keywords: ai assistant, migrate dockerfile, docker hardened images, automated migration
params:
  sidebar:
    badge:
      color: violet
      text: Experimental
---

{{< summary-bar feature_name="Ask Gordon DHI migration" >}}

您可以使用 Docker 的 AI 助手自动将您的 Dockerfile 迁移至使用 Docker 强化镜像 (DHI)。

1. 确保已[启用](/manuals/ai/gordon.md#enable-ask-gordon) Docker 的 AI 助手。
2. 在终端中，导航至包含您的 Dockerfile 的目录。
3. 与助手开始对话：
   ```bash
   docker ai
   ```
4. 输入：
   ```console
   "Migrate my dockerfile to DHI"
   ```
5. 跟随与助手的对话。助手将编辑您的 Dockerfile，因此当它请求访问文件系统及其他权限时，输入 `yes` 以允许助手继续操作。

迁移完成后，您将看到一条成功消息：

```text
已成功迁移至 Docker 强化镜像 (DHI)。更新后的 Dockerfile 成功构建了镜像，且最终镜像中未检测到任何漏洞。
原始 Dockerfile 的功能和优化已得到保留。
```

> [!IMPORTANT]
>
> 与任何 AI 工具一样，您必须验证助手的编辑并测试您的镜像。