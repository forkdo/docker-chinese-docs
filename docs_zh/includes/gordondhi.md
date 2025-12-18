1. 确保已[启用 Gordon](/manuals/ai/gordon.md#enable-ask-gordon)。
1. 在 Gordon 工具箱中，确保已启用 Gordon 的[开发者 MCP 工具包](/manuals/ai/gordon/mcp/built-in-tools.md#configuration)。
1. 在终端中，导航到包含 Dockerfile 的目录。
1. 启动与 Gordon 的对话：
   ```bash
   docker ai
   ```
1. 输入：
   ```console
   "将我的 dockerfile 迁移到 DHI"
   ```
1. 按照与 Gordon 的对话进行操作。Gordon 会编辑您的 Dockerfile，因此当它请求访问文件系统等资源时，请输入 `yes` 以允许 Gordon 继续。

   > [!NOTE]
   > 要了解有关 Gordon 数据保留及其可访问数据的更多信息，请参阅 [Gordon](/manuals/ai/gordon.md#what-data-does-gordon-access)。

迁移完成后，您会看到成功消息：

```text
Docker 硬化镜像 (DHI) 迁移已完成。更新后的 Dockerfile 成功构建了镜像，并且在最终镜像中未检测到任何漏洞。原始 Dockerfile 的功能和优化已得到保留。
```

> [!IMPORTANT]
> 与任何 AI 工具一样，您必须验证 Gordon 的编辑并测试您的镜像。