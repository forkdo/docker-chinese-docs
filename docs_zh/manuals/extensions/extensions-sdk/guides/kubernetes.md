---
title: 从扩展中与 Kubernetes 交互
linkTitle: 与 Kubernetes 交互
description: 如何从扩展中连接到 Kubernetes 集群
keywords: Docker, Extensions, sdk, Kubernetes
aliases:
 - /desktop/extensions-sdk/dev/kubernetes/
 - /desktop/extensions-sdk/guides/kubernetes/
---

Extensions SDK 不提供直接与 Docker Desktop 管理的 Kubernetes 集群或使用 KinD 等其他工具创建的任何其他集群交互的 API 方法。但是，本文档提供了一种方法，让您可以使用其他 SDK API 从扩展中与 Kubernetes 集群进行间接交互。

如果您需要直接与 Docker Desktop 管理的 Kubernetes 交互的 API，可以在 Extensions SDK GitHub 仓库的 [此问题](https://github.com/docker/extensions-sdk/issues/181) 中进行投票。

## 前提条件

### 启用 Kubernetes

您可以使用 Docker Desktop 中内置的 Kubernetes 启动单节点 Kubernetes 集群。
`kubeconfig` 文件用于在与 `kubectl` 命令行工具或其他客户端结合使用时配置对 Kubernetes 的访问。
Docker Desktop 为用户在其家目录中方便地提供了一个本地预配置的 `kubeconfig` 文件和 `kubectl` 命令。这对于希望从 Docker Desktop 利用 Kubernetes 的用户来说是一种便捷的快速上手方式。

## 将 `kubectl` 作为扩展的一部分打包

如果您的扩展需要与 Kubernetes 集群交互，建议您将 `kubectl` 命令行工具作为扩展的一部分包含在内。通过这样做，安装您扩展的用户将在其主机上安装 `kubectl`。

要了解如何将 `kubectl` 命令行工具作为多平台的一部分打包到您的 Docker 扩展镜像中，请参阅 [构建多架构扩展](../extensions/multi-arch.md#adding-multi-arch-binaries)。

## 示例

以下代码片段已整理在 [Kubernetes 示例扩展](https://github.com/docker/extensions-sdk/tree/main/samples/kubernetes-sample-extension) 中。它展示了如何通过打包 `kubectl` 命令行工具来与 Kubernetes 集群交互。

### 检查 Kubernetes API 服务器是否可访问

一旦在 `Dockerfile` 中将 `kubectl` 命令行工具添加到扩展镜像中，并在 `metadata.json` 中定义，Extensions 框架在安装扩展时会将 `kubectl` 部署到用户的主机上。

您可以使用 JS API `ddClient.extension.host?.cli.exec` 来发出 `kubectl` 命令，例如，检查在给定特定上下文的情况下 Kubernetes API 服务器是否可访问：

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "cluster-info",
  "--request-timeout",
  "2s",
  "--context",
  "docker-desktop",
]);
```

### 列出 Kubernetes 上下文

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "config",
  "view",
  "-o",
  "jsonpath='{.contexts}'",
]);
```

### 列出 Kubernetes 命名空间

```typescript
const output = await ddClient.extension.host?.cli.exec("kubectl", [
  "get",
  "namespaces",
  "--no-headers",
  "-o",
  'custom-columns=":metadata.name"',
  "--context",
  "docker-desktop",
]);
```

## 持久化 kubeconfig 文件

下面提供了在主机文件系统上持久化和读取 `kubeconfig` 文件的不同方法。用户可以随时向 `kubeconfig` 文件添加、编辑或删除 Kubernetes 上下文。

> 警告
>
> `kubeconfig` 文件非常敏感，如果被发现，可能会让攻击者获得 Kubernetes 集群的管理权限。

### 扩展的后端容器

如果您需要扩展在读取后持久化 `kubeconfig` 文件，可以使用一个后端容器，该容器暴露一个 HTTP POST 端点，将文件内容存储在内存中或容器文件系统的某个位置。这样，如果用户从扩展导航到 Docker Desktop 的其他部分然后返回，您就不需要再次读取 `kubeconfig` 文件。

```typescript
export const updateKubeconfig = async () => {
  const kubeConfig = await ddClient.extension.host?.cli.exec("kubectl", [
    "config",
    "view",
    "--raw",
    "--minify",
    "--context",
    "docker-desktop",
  ]);
  if (kubeConfig?.stderr) {
    console.log("error", kubeConfig?.stderr);
    return false;
  }

  // 调用后端容器将检索到的 kubeconfig 存储到容器的内存或文件系统中
  try {
    await ddClient.extension.vm?.service?.post("/store-kube-config", {
      data: kubeConfig?.stdout,
    });
  } catch (err) {
    console.log("error", JSON.stringify(err));
  }
};
```

### Docker 卷

卷是持久化 Docker 容器生成和使用的数据的首选机制。您可以利用它们来持久化 `kubeconfig` 文件。
通过在卷中持久化 `kubeconfig`，当扩展窗格关闭时，您不需要再次读取 `kubeconfig` 文件。这使其非常适合在从扩展导航到 Docker Desktop 的其他部分时持久化数据。

```typescript
const kubeConfig = await ddClient.extension.host?.cli.exec("kubectl", [
  "config",
  "view",
  "--raw",
  "--minify",
  "--context",
  "docker-desktop",
]);
if (kubeConfig?.stderr) {
  console.log("error", kubeConfig?.stderr);
  return false;
}

await ddClient.docker.cli.exec("run", [
  "--rm",
  "-v",
  "my-vol:/tmp",
  "alpine",
  "/bin/sh",
  "-c",
  `"touch /tmp/.kube/config && echo '${kubeConfig?.stdout}' > /tmp/.kube/config"`,
]);
```

### 扩展的 `localStorage`

`localStorage` 是浏览器 Web 存储的机制之一。它允许用户将数据作为键值对保存在浏览器中以供以后使用。
`localStorage` 在浏览器（扩展窗格）关闭时不会清除数据。这使其非常适合在从扩展导航到 Docker Desktop 的其他部分时持久化数据。

```typescript
localStorage.setItem("kubeconfig", kubeConfig);
```

```typescript
localStorage.getItem("kubeconfig");
```