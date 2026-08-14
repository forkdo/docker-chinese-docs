---
title: OIDC 连接概述
linkTitle: OIDC 连接
description: 使用短期 OpenID Connect 令牌将 GitHub Actions 验证到 Docker
keywords: oidc connections, openid connect, github actions, jwt, subject claims, rulesets, enterprise security, workload authentication
tags: [admin]
weight: 35
---

{{< summary-bar feature_name="OIDC connections" >}}

OIDC 连接在 Docker 和受信任的第三方之间建立信任关系，因此您无需维护长期有效的凭据。当您创建 OIDC 连接时，Docker 会与另一个能够授予对您 Docker 资源精细访问权限的供应商交换短期令牌。

## OIDC 连接的工作原理

OIDC 连接遵循 OpenID Connect（OIDC）标准。建立信任关系包括创建连接、配置工作流和测试。例如，Docker 与 GitHub 之间的信任关系遵循以下步骤：

- GitHub 为工作流运行签发 JWT ID 令牌。
- 在验证过程中，Docker：
  - 根据 GitHub 的公钥注册表验证令牌
  - 将根据主题声明（subject claims）与在 [Docker Home](https://app.docker.com/) 中创建的规则集（rulesets）进行匹配
- Docker 返回访问令牌，使 GitHub Action 能够登录 Docker 并访问资源。

在 OIDC 工作流期间创建和交换的所有令牌都是短期的，并且按工作流签发。

## OIDC 连接与 OAT

[组织访问令牌（OATs）](/manuals/enterprise/security/access-tokens.md)在组织级别提供对您 Docker 资源的编程访问。与个人访问令牌不同，OAT 不绑定到个别成员，因此当成员身份变更时访问仍然持续。

OIDC 连接不会取代 OAT。OIDC 连接将工作流验证为好像它是一个用户，然后在验证后授权访问。

虽然 OAT 通过组织成员身份管理对您 Docker 资源的访问，但 OIDC 连接在 GitHub Actions 工作流请求更改您的 Docker 资源时对其进行验证。

## 后续步骤

- [创建 OIDC 连接](/manuals/enterprise/security/oidc-connections/create-manage.md)
- [OIDC 规则集和主题声明](/manuals/enterprise/security/oidc-connections/rulesets-claims.md)
