---
description: 在无 root 模式下容器 UID 和 GID 如何映射到主机
keywords: security, namespaces, rootless, uid, gid, subuid, subgid
title: UID/GID 映射
weight: 15
---

无 root 模式和 [`userns-remap` 模式](../userns-remap.md) 将容器 UID 和 GID 映射到主机的方式不同。

- 在 `userns-remap` 模式下，容器的 UID `0` 被映射到 `/etc/subuid` 中为 remap 用户列出的第一个从属 UID，容器的 UID `n` 被映射到 `subuid + n`。
- 在无 root 模式下，容器的 UID `0` 被映射到运行无 root Docker 的主机用户的 UID（即 `id -u` 的结果）；容器的 UID `n`（对于 `n >= 1`）被映射到 `subuid + (n - 1)`。

GID 遵循相同的规则，使用 `/etc/subgid`。

这一差异在设置 bind 挂载目录的文件权限时很重要：在无 root 模式下，由你的主机用户拥有的文件在容器内显示为 `root` 所有。
