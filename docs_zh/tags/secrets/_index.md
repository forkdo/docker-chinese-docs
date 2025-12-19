---
title: Secrets
description: 在容器中安全地使用敏感信息
---

Secret（机密）是一段数据，例如密码、SSH 私钥、SSL
证书，或任何不应通过网络传输或以未加密形式存储在 Dockerfile 或应用程序源代码中的内容。

Docker 提供了专门指定的功能来管理 secrets。