---
title: 从扩展与 Kubernetes 交互
linkTitle: 与 Kubernetes 交互
description: 如何从扩展连接到 Kubernetes 集群
keywords: Docker, Extensions, sdk, Kubernetes
aliases:
- /desktop/extensions-sdk/dev/kubernetes/
- /desktop/extensions-sdk/guides/kubernetes/
---

Extensions SDK 不提供任何直接与 Docker Desktop 管理的 Kubernetes 集群或其他使用 KinD 等工具创建的集群进行交互的 API 方法。不过，本页面提供了一种方法，让您可以通过其他 SDK API 从扩展中间接与 Kubernetes 集群进行交互。

如需请求可直接与 Docker Desktop 管理的 Kubernetes 集群交互的 API，您可以在 Extensions SDK GitHub 仓库中为此 [议题](https://github.com/docker/extensions-sdk/issues/181) 投票。

## 先决条件

### 启用 Kubernetes

您可以使用 Docker Desktop 内置的 Kubernetes 功能来启动一个单节点 Kubernetes 集群。
`kubeconfig` 文件用于配置对 Kubernetes 的访问权限，通常与 `kubectl` 命令行工具或其他客户端配合使用。
Docker Desktop 会在用户的 home 目录下方便地提供一个本地预配置的 `kubeconfig` 文件和 `kubectl` 命令。这对于希望利用 Docker Desktop 使用 Kubernetes 的用户来说，是一种快速入门的便捷方式。

## 将 `kubectl` 作为扩展的一部分打包

如果您的扩展需要与 Kubernetes 集群交互，建议您将 `kubectl` 命令行工具作为扩展的一部分包含进来。这样，安装您扩展的用户就会在主机上安装 `kubectl`。

要了解如何将适用于多个平台的 `kubectl` 命令行工具作为 Docker 扩展镜像的一部分打包，请参阅 [构建多架构扩展](../extensions/multi-arch.md#adding-multi-arch-binaries)。

## 示例

以下代码片段已在 [Kubernetes 示例扩展](https://github.com/docker/extensions-sdk/tree/main/samples/kubernetes-sample-extension) 中整合。它展示了如何通过打包 `kubectl` 命令行工具与 Kubernetes 集群进行交互。

### 检查 Kubernetes API 服务器是否可达

一旦在 `Dockerfile` 中将 `kubectl` 命令行工具添加到扩展镜像中，并在 `metadata.json` 中定义，Extensions 框架就会在扩展安装时将 `kubectl` 部署到用户的主机上。

您可以使用 JS API `ddClient.extension.host?.cli.exec` 来发出 `kubectl` 命令，例如，检查在特定上下文下 Kubernetes API 服务器是否可达：

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

以下是在主机文件系统中持久化和读取 `kubeconfig` 文件的不同方法。用户可以随时向 `kubeconfig` 文件添加、编辑或删除 Kubernetes 上下文。

> 警告
>
> `kubeconfig` 文件非常敏感，如果被攻击者获取，可能会获得对 Kubernetes 集群的管理权限。

### 扩展的后端容器

如果您需要扩展在读取 `kubeconfig` 文件后仍能持久化该文件，可以设置一个后端容器，暴露一个 HTTP POST 端点来存储文件内容，可以存储在内存中或容器文件系统的某个位置。这样，即使用户从扩展导航到 Docker Desktop 的其他部分，然后再返回，您也不需要再次读取 `kubeconfig` 文件。

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

  // 调用后端容器，将检索到的 kubeconfig 存储到容器的内存或文件系统中
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

卷是持久化由 Docker 容器生成和使用的数据的推荐机制。您可以利用卷来持久化 `kubeconfig` 文件。
通过将 `kubeconfig` 持久化到卷中，当扩展面板关闭时，您就不需要再次读取 `kubeconfig` 文件。这使得它在从扩展导航到 Docker Desktop 其他部分时持久化数据非常理想。

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

`localStorage` 是浏览器 Web 存储的一种机制。它允许用户将数据以键值对的形式保存在浏览器中，以便日后使用。
`localStorage` 在浏览器（扩展面板）关闭时不会清除数据。这使得它在从扩展导航到 Docker Desktop 其他部分时持久化数据非常理想。

```typescript
localStorage.setItem("kubeconfig", kubeConfig);
```

```typescript
localStorage.getItem("kubeconfig");
```