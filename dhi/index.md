# Docker Hardened Images


Docker Hardened Images (DHI) 提供由 Docker 维护的精简、安全且可用于生产环境的容器镜像、Helm chart 和系统软件包。DHI 旨在减少漏洞并简化合规性，可以轻松集成到您现有的基于 Docker 的工作流中，几乎无需重新调整工具。

DHI 提供以下三种订阅方案。

| 功能 | Community | Select | Enterprise |
|---|---|---|---|
| 加固的精简镜像 | ✅ | ✅ | ✅ |
| 近零 CVE | ✅ | ✅ | ✅ |
| 可验证的 SBOM 与 SLSA Build L3 溯源 | ✅ | ✅ | ✅ |
| 完整、不做抑制的 CVE 可见性 | ✅ | ✅ | ✅ |
| 直接替换采用，无需更改工作流 | ✅ | ✅ | ✅ |
| Apache 2.0 许可下的完整开源镜像目录 | ✅ | ✅ | ✅ |
| 基于 Docker Hardened System Packages 构建 | ✅ | ✅ | ✅ |
| Docker 发布补丁遵循上游节奏 | ✅ | ✅ | ✅ |
| FIPS/STIG 变体 | ❌ | ✅ | ✅ |
| 关键 CVE 在 7 天内修复，附带 SLA 保障的持续打补丁 | ❌ | ✅ | ✅ |
| 定制化 | ❌ | ✅ 最多 5 个 | ✅ 无限制 |
| 访问 Hardened System Packages 仓库 | ❌ | ❌ | ✅ |
| 可获得完整目录访问权限 | ❌ | ❌ | ✅ |
| 可选购延长生命周期支持附加服务 | ❌ | ❌ | ✅ 额外 5 年加固更新 |

有关定价和更多详情，请参阅 [Docker Hardened Images 订阅对比](https://www.docker.com/products/hardened-images/#compare)。

## Community 功能

DHI 的核心功能可在 Apache 2.0 许可下免费使用、共享和基于其进行构建。

- [近零 CVE](/dhi/explore/security-concepts/cves/)：持续扫描和打补丁，将已知漏洞保持在最低水平
- [Distroless 变体](/dhi/explore/security-concepts/distroless/)：移除不必要的组件，将攻击面减少多达 95%
- 非 root 执行：容器默认以非 root 用户运行
- [加固系统软件包](/dhi/how-to/hardened-packages/)：从源码构建、经过加密签名并由 Docker 验证的系统软件包
- 每个镜像都带有 [SLSA Build Level 3 溯源](/dhi/explore/security-concepts/slsa/)、[签名的 SBOM](/dhi/explore/security-concepts/sbom/)、[VEX 声明](/dhi/explore/security-concepts/vex/)和[加密签名](/dhi/explore/security-concepts/signatures/)
- 基于 Alpine 和 Debian 构建，提供 [glibc 和 musl 变体](/dhi/explore/security-concepts/glibc-musl/)；同时提供开发和运行时镜像变体
- 可与现有 Docker 工作流、CI/CD 流水线和工具协同工作，无需重新调整工具
- [Helm chart](/dhi/how-to/helm/)：由 Docker 提供的 chart，基于上游源构建，经过与 DHI 的兼容性测试，并在 DHI 目录中以 OCI 制品形式提供；包含 SLSA Level 3 溯源、SBOM 和加密签名

## Select 与 Enterprise 功能

面向具有严格安全或合规要求的组织：

- 针对关键和高危 CVE 修复的 [7 天 SLA](https://docs.docker.com/go/dhi-sla/)
- [启用 FIPS](/dhi/explore/security-concepts/fips/) 和 [STIG-ready](/dhi/explore/security-concepts/stig/) 合规变体
- [定制化](/dhi/how-to/customize/)：添加软件包、工具、证书和配置（Select 最多 5 个，Enterprise 无限制）
- [企业软件包仓库](/dhi/how-to/hardened-packages/)访问权限和完整目录访问权限（Enterprise）
- 延长生命周期支持：EOL 之后的安全补丁、更新的 SBOM、溯源和签名（Enterprise 附加服务）

## 开始使用

探索以下部分，以开始使用 Docker Hardened Images，将它们集成到您的工作流中，并了解是什么使其安全且企业就绪。



