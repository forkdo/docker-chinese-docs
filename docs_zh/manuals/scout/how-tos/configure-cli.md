---
title: 使用环境变量配置 Docker Scout
linkTitle: Docker Scout 环境变量
description: 使用这些环境变量配置 Docker Scout CLI 命令的行为
keywords: scout, supply chain, cli, environment, variables, env, vars, configure
aliases:
- /scout/env-vars/
---

以下环境变量可用于配置 Docker Scout CLI 命令，以及对应的 `docker/scout-cli` 容器镜像：

| 名称                                    | 格式    | 说明                                                                                         |
| :-------------------------------------- | ------- | :------------------------------------------------------------------------------------------- |
| DOCKER_SCOUT_CACHE_FORMAT               | 字符串  | 本地镜像缓存的格式；可以是 `oci` 或 `tar`（默认：`oci`）                                      |
| DOCKER_SCOUT_CACHE_DIR                  | 字符串  | 本地 SBOM 缓存存储目录（默认：`$HOME/.docker/scout`）                                         |
| DOCKER_SCOUT_NO_CACHE                   | 布尔值  | 设置为 `true` 时，禁用本地 SBOM 缓存                                                         |
| DOCKER_SCOUT_OFFLINE                    | 布尔值  | 在索引 SBOM 时使用 [离线模式](#offline-mode)                                                 |
| DOCKER_SCOUT_REGISTRY_TOKEN             | 字符串  | 拉取镜像时用于注册表身份验证的令牌                                                             |
| DOCKER_SCOUT_REGISTRY_USER              | 字符串  | 拉取镜像时用于注册表身份验证的用户名                                                           |
| DOCKER_SCOUT_REGISTRY_PASSWORD          | 字符串  | 拉取镜像时用于注册表身份验证的密码或个人访问令牌                                               |
| DOCKER_SCOUT_HUB_USER                   | 字符串  | 用于向 Docker Scout 后端进行身份验证的 Docker Hub 用户名                                     |
| DOCKER_SCOUT_HUB_PASSWORD               | 字符串  | 用于向 Docker Scout 后端进行身份验证的 Docker Hub 密码或个人访问令牌                          |
| DOCKER_SCOUT_NEW_VERSION_WARN           | 布尔值  | 对 Docker Scout CLI 的新版本发出警告                                                           |
| DOCKER_SCOUT_EXPERIMENTAL_WARN          | 布尔值  | 对实验性功能发出警告                                                                           |
| DOCKER_SCOUT_EXPERIMENTAL_POLICY_OUTPUT | 布尔值  | 禁用策略评估的实验性输出                                                                       |

## 离线模式

在正常操作下，Docker Scout 会与外部系统（如 npm、NuGet 或 proxy.golang.org）进行交叉引用，以检索镜像中发现的软件包的额外信息。

当 `DOCKER_SCOUT_OFFLINE` 设置为 `true` 时，Docker Scout 镜像分析将在离线模式下运行。离线模式意味着 Docker Scout 不会向外部系统发出出站请求。

要使用离线模式：

```console
$ export DOCKER_SCOUT_OFFLINE=true
```