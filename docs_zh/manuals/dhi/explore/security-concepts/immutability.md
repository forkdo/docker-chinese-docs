---
aliases:
  - /dhi/core-concepts/immutability/
title: Immutable infrastructure
linktitle: Immutability
description: 了解镜像摘要、只读容器以及已签名的元数据如何确保 Docker Hardened Images 防篡改且不可变。
keywords: immutable container image, read-only docker image, configuration drift prevention, secure redeployment, image digest verification
---

不可变基础设施（Immutable infrastructure）是一种安全与运维模型，其中的服务器、容器和镜像等组件在部署后永远不会被修改。与其修补或重新配置运行中的系统，不如用新版本将它们整体替换。

在使用 Docker Hardened Images 时，不可变性是一种最佳实践，能够强化你软件供应链的安全态势。

## 为什么不可变性很重要（Why immutability matters）

可变系统更难保障安全和审计。实时打补丁或手动更新会引入如下风险：

- 配置漂移（Configuration drift）
- 未跟踪的变更
- 环境不一致
- 攻击面扩大

不可变基础设施通过仅经由受控、可重复的构建与部署来引入变更，从而解决了这些问题。

## Docker Hardened Images 如何支持不可变性

Docker Hardened Images 被构建为最小化、锁定且非交互式，从而抑制就地修改。例如：

- 许多 DHI 镜像不包含 shell、包管理器和调试工具
- DHI 镜像设计为在部署前经过扫描和签名
- 鼓励 DHI 用户重建并重新部署镜像，而不是修补运行中的容器

这种设计符合不可变实践，并确保：

- 更新经由 CI/CD 流水线进行
- 所有变更都经过版本化且可审计
- 系统能够一致地回滚或复现

## 实践中的不可变模式（Immutable patterns in practice）

一些利用不可变性的常见模式包括：

- 容器替换：与其登录到容器中修复 bug 或打补丁，不如重建镜像并重新部署。
- 基础设施即代码（IaC）：在受版本控制的文件中定义你的基础设施和镜像配置。
- 蓝绿部署或金丝雀部署：将新镜像与旧镜像一起发布，并逐步将流量切换到新版本。

通过将不可变基础设施原则与加固镜像相结合，你可以创建出一种可预测、安全且能抵御篡改、并将长期风险最小化的部署工作流。
