# 在 Docker Desktop 中使用 Gordon




Gordon 已集成到 Docker Desktop 中。从侧边栏访问它即可打开 Gordon 视图。

## 基本用法

要访问 Gordon：

1. 打开 Docker Desktop 并登录你的 Docker 账户。
2. 在侧边栏中选择 **Gordon**。
3. 在输入框中输入你的问题或请求。
4. 按 <kbd>Enter</kbd> 或选择发送按钮。

Gordon 会在聊天视图中回复，并在整个会话过程中保持上下文。

## 工作目录

工作目录为 Gordon 的文件操作设定默认上下文。你可以在启动 Gordon 时选择工作目录，或在对话过程中使用目录图标进行更改：

1. 选择 Gordon 输入区域中的目录图标。
2. 浏览并选择其他目录。

## 上下文帮助

Gordon 图标会出现在 Docker Desktop 的各个位置。选择它会打开 Gordon，并预先加载你正在处理的项目的上下文，例如容器日志或构建输出。

## 用量指示器

Docker Desktop 会显示用量指示器，让你了解距离所在层级的额度上限还有多少。详情参见[用量限制与层级](../usage-limits.md)。

## 禁用 Gordon

要禁用 Gordon：

1. 打开 Docker Desktop 设置。
2. 导航到 **AI** 部分。
3. 取消勾选 **Enable Gordon** 选项。
4. 选择 **Apply**。

## 配置工具

你可以控制 Gordon 能访问哪些工具。有关启用、禁用和精细调整工具权限的详情，参见[配置工具](./configure-tools.md)。

