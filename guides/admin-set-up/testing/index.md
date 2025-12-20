# 测试

## SSO 和 SCIM 测试

通过使用链接到 Docker 账户的电子邮件地址（该账户属于已验证域名的一部分）登录 Docker Desktop 或 Docker Hub 来测试 SSO 和 SCIM。
使用其 Docker 用户名登录的开发者不受 SSO 和 SCIM 设置的影响。

> [!重要提示]
>
> 部分用户可能需要通过 CLI 登录 Docker Hub，为此他们需要一个[个人访问令牌 (PAT)](/manuals/security/access-tokens.md)。

## 测试注册表访问管理和镜像访问管理

> [!警告]
>
> 在继续之前请与您的用户沟通，因为此步骤将影响所有登录您 Docker 组织的现有用户。

如果您计划使用[注册表访问管理 (RAM)](/manuals/enterprise/security/hardened-desktop/registry-access-management.md) 和/或[镜像访问管理 (IAM)](/manuals/enterprise/security/hardened-desktop/image-access-management.md)：

1. 确保您的测试开发者使用其组织凭据登录 Docker Desktop
2. 让他们尝试通过 Docker CLI 拉取未经授权的镜像或来自不允许的注册表的镜像
3. 验证他们收到一条错误消息，表明该注册表受到组织限制

## 部署设置并强制为测试组登录

通过 MDM 部署 Docker 设置，并强制一小部分测试用户组登录。让该组在 Docker Desktop 和 Docker Hub 上使用容器测试其开发工作流，以确保所有设置和强制登录功能均按预期运行。

## 测试 Docker Build Cloud 功能

让您的 Docker Desktop 测试人员之一[连接到您创建的云构建器并使用它进行构建](/manuals/build-cloud/usage.md)。

## 测试 Testcontainers Cloud

让测试开发者[连接到 Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started) 并在云中运行容器，以验证设置是否正确工作。

## 验证 Docker Scout 对仓库的监控

检查 [Docker Scout 仪表板](https://scout.docker.com/)，以确认已为启用 Docker Scout 的仓库正确接收数据。

## 验证对 Docker Hardened Images 的访问

让测试开发者尝试[拉取 Docker Hardened Image](/manuals/dhi/get-started.md)，以确认团队拥有适当的访问权限，并能将这些镜像集成到其工作流中。
