# 
1. 确保 Gordon 已[启用](/manuals/ai/gordon.md#enable-ask-gordon)。
1. 在 Gordon 的工具箱中，确保 Gordon 的 [Developer MCP Toolkit 已启用](/manuals/ai/gordon/mcp/built-in-tools.md#configuration)。
1. 在终端中，导航到包含您的 Dockerfile 的目录。
1. 与 Gordon 开始对话：
   ```bash
   docker ai
   ```
1. 输入：
   ```console
   "Migrate my dockerfile to DHI"
   ```
1. 按照与 Gordon 的对话进行操作。Gordon 将编辑您的 Dockerfile，因此当它请求访问文件系统等权限时，请输入 `yes` 以允许 Gordon 继续。

   > [!NOTE]
   > 要了解有关 Gordon 数据保留及其可以访问的数据的更多信息，请参阅 [Gordon](/manuals/ai/gordon.md#what-data-does-gordon-access)。

迁移完成后，您将看到一条成功消息：

```text
The migration to Docker Hardened Images (DHI) is complete. The updated Dockerfile
successfully builds the image, and no vulnerabilities were detected in the final image.
The functionality and optimizations of the original Dockerfile have been preserved.
```

> [!IMPORTANT]
> 与任何 AI 工具一样，您必须验证 Gordon 的编辑并测试您的镜像。
