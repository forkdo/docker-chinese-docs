# 数据与 Gordon




本页介绍 Gordon 访问哪些数据、如何使用这些数据，以及有哪些隐私保护措施。

## Gordon 访问哪些数据

当你使用 Gordon 时，它访问的数据取决于你的查询和配置。

### 本地文件

当你使用 `docker ai` 命令时，Gordon 可以访问你系统上的文件和目录。工作目录为文件操作设置了默认上下文。

在 Docker Desktop 中，如果你在 Gordon 视图中询问特定文件或目录，系统会提示你选择相关上下文。

### 本地镜像

Gordon 与 Docker Desktop 集成，可以查看本地镜像存储中的所有镜像。这包括你构建或从注册表拉取的镜像。

### Docker 环境

Gordon 可以访问你的 Docker 守护进程状态，包括：

- 运行中和已停止的容器
- 容器日志和配置
- 镜像和镜像层
- 卷和网络
- 构建缓存

## 数据保留策略

Gordon 的数据保留因你的订阅层级而异：

### 付费订阅

Docker 及其 AI 提供方不会保留你 Gordon 会话的任何输入或输出。你的查询、Gordon 的响应，以及任何被处理的代码或文件都不会被存储。这适用于所有付费订阅：Docker Desktop 套餐（Pro、Team、Business）和 Gordon 套餐（Plus、Max、Ultra）。

### 个人（免费）订阅

匿名化的对话记录会存储 5 天，以帮助保证服务质量和防范滥用。单个查询和响应作为你对话历史的一部分被保留。

### 所有订阅

数据绝不会用于训练 AI 模型或与第三方共享。所有传输到 Gordon 后端的数据在传输过程中都经过加密。Docker 的第三方 AI 提供方在零数据保留协议下处理请求：它们不存储你的提示或 Gordon 的响应。

## 敏感数据保护

Gordon 会使用 [portcullis](https://github.com/docker/portcullis)（Docker 的开源脱敏库）自动检测并从你的请求中编辑密钥和其他敏感信息。覆盖约 240 种模式，包括：

- 云提供方凭证（AWS、GCP、Azure 等）
- API 令牌（GitHub、GitLab、Docker Hub、Slack、OpenAI、Stripe 等）
- PEM 私钥和 JWT
- 数据库连接字符串密码
- 银行卡号、IBAN 和美国社会安全号码

检测到的内容会在你的请求被处理之前替换为 `[REDACTED]`。

## 数据安全

你的数据通过传输加密得到保护。对于付费订阅，不会发生持久化存储——Gordon 会处理你的请求并立即丢弃数据。

有关隐私条款的问题，请查看 [Gordon 补充条款](https://www.docker.com/legal/docker-ai-supplemental-terms/)。

## 组织数据策略

对于 Business 订阅，管理员可以使用设置管理为他们的组织启用或禁用 Gordon。在启用 Gordon 之前，请审查你组织的数据处理要求。

有关配置详情，请参阅 [设置管理](/enterprise/security/hardened-desktop/settings-management/)。

## 禁用 Gordon

你可以随时禁用 Gordon：

个人用户：

1. 打开 Docker Desktop 设置。
2. 导航到 **AI** 部分。
3. 清除 **Enable Gordon**（启用 Gordon）选项。
4. 选择 **Apply**（应用）。

Business 组织：

管理员可以使用设置管理为整个组织禁用 Gordon。详情请参阅 [设置管理](/enterprise/security/hardened-desktop/settings-management/)。

## 关于隐私的问题

有关 Docker 隐私实践的问题：

- 查看 [Docker 隐私政策](https://www.docker.com/legal/privacy/)
- 阅读 [Gordon 补充条款](https://www.docker.com/legal/docker-ai-supplemental-terms/)
- 联系 Docker 支持以咨询具体问题

