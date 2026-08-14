<!-- FILE: manuals/ai/sandboxes/security/defaults.md -->

---
title: 默认安全态势
linkTitle: 默认值
weight: 15
description: 在您更改任何设置之前，沙盒允许什么、阻止什么。
keywords: docker sandboxes, security defaults, network policy, credentials, shared skills, sbx
---

使用 `sbx run` 且不加任何额外标志创建的沙盒具有以下安全态势。

## 网络默认值

所有出站 HTTP 和 HTTPS 流量都被阻止，除非有显式规则允许（默认拒绝）。所有非 HTTP 协议（原始 TCP、UDP 包括 DNS，以及 ICMP）在网络层被阻止。发往私有 IP 范围、环回地址和链路本地地址的流量也被阻止。

运行 `sbx policy ls` 查看你安装中的活动网络规则。可以使用 `sbx policy` CLI 按机器自定义规则，或跨组织集中管理。组织级规则优先于本地规则。请参阅 [网络访问策略](../governance/access-controls/network.md)。

## 工作区默认值

沙盒默认使用直接挂载。agent 直接查看并修改你的工作树，更改会立即出现在你的宿主上。

agent 可以读取、写入和删除工作区目录中的任何文件，包括隐藏文件、配置文件、构建脚本和 Git hooks。在 agent 会话后需要审查的内容，请参阅 [工作区隔离](isolation.md#workspace-isolation)。

## 共享技能默认值

受支持 agent 的沙盒默认以读写方式挂载一个持久的共享技能存储。每个使用该存储的沙盒都可以更改其他参与沙盒可能加载的技能。创建沙盒时使用 `--no-share-skills` 可将其排除在这个共享信任边界之外。请参阅 [共享 agent 技能](../workflows.md#share-agent-skills)。

## 凭据默认值

除非你使用 `sbx secret` 或环境变量提供凭据，否则沙盒没有任何可用的凭据。当提供凭据时，宿主侧代理将其注入到出站 HTTP 头部中。agent 无法读取原始凭据值。

设置说明请参阅 [凭据](credentials.md)。

## agent 在沙盒内部的能力

agent 在沙盒 VM 内部拥有完全控制权：

- `sudo` 访问（agent 以非 root 用户运行，但拥有 sudo 权限）
- 一个用于构建镜像和运行容器的私有 Docker Engine
- 通过 `apt`、`pip`、`npm` 及其他包管理器安装包
- 对 VM 文件系统的完全读写访问

agent 在 VM 内部安装或创建的一切，包括包、Docker 镜像和配置更改，都会在停止和重启周期之间持续存在。当你使用 `sbx rm` 移除沙盒时，VM 及其内容被删除。工作区文件和共享技能存储保留在宿主上。

## 默认阻止的内容

以下内容对所有沙盒都被阻止，并且不能通过策略配置更改：

- 对显式挂载的工作区和共享技能存储之外的宿主文件系统的访问
- 宿主 Docker 守护进程
- 宿主网络和 localhost
- 沙盒之间的直接网络通信
- 原始 TCP、UDP 和 ICMP 连接
- 到私有 IP 范围和链路本地地址的流量

到不在允许列表中的域的出站 HTTP/HTTPS 默认也被阻止，但你可以使用 `sbx policy allow` 添加允许规则。
