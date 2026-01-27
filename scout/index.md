# Docker Scout


容器镜像由层（layers）和软件包组成，这些都可能存在漏洞。
这些漏洞可能会危及容器和应用程序的安全性。

Docker Scout 是一种主动增强软件供应链安全性的解决方案。
通过分析您的镜像，Docker Scout 会生成一个组件清单，也称为软件物料清单（SBOM）。
该 SBOM 会与一个持续更新的漏洞数据库进行比对，以识别安全弱点。

Docker Scout 是一个独立的服务和平台，您可以通过 Docker Desktop、Docker Hub、Docker CLI 和 Docker Scout Dashboard 与其交互。
Docker Scout 还支持与第三方系统（如容器注册表和 CI 平台）集成。


