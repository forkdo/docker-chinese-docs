---
title: 通过扩展与 Kubernetes 交互
linkTitle: 与 Kubernetes 交互
description: 如何从扩展连接到 Kubernetes 集群
keywords: Docker, Extensions, sdk, Kubernetes
aliases:
 - /desktop/extensions-sdk/dev/kubernetes/
 - /desktop/extensions-sdk/guides/kubernetes/
---

Extensions SDK 并未提供任何 API 方法来直接与 Docker Desktop 托管的 Kubernetes 集群或使用其他工具（如 KinD）创建的集群进行交互。但是，本页提供了一种方法，让您可以通过其他 SDK API 从扩展中间接地与 Kubernetes 集群进行交互。

如果您希望请求一个能直接与 Docker Desktop 托管的 Kubernetes 交互的 API，可以在 Extensions SDK GitHub 仓库中为 [此议题](https://github.com/docker/extensions-sdk/issues/181) 点赞。

## 先决条件

### 开启 Kubernetes

您可以使用 Docker Desktop 内置的 Kubernetes 来启动一个 Kubernetes 单节点集群。
`kubeconfig` 文件用于在与 `kubectl` 命令行工具或其他客户端结合使用时，配置对 Kubernetes 的访问。
Docker Desktop 会方便地在用户的主目录下提供一个本地预配置的 `kubeconfig` 文件和 `kubectl` 命令。对于希望从 Docker Desktop 利用 Kubernetes 的用户来说，这是一种快速实现访问的便捷方式。

## 将 `kubectl` 作为扩展的一部分分发

如果您的扩展需要与 Kubernetes 集群交互，建议将 `kubectl` 命令行工具包含在您的扩展中。这样做后，安装您扩展的用户会在其主机上获得 `kubectl`。

要了解如何为多个平台将 `kubectl` 命令行工具作为 Docker 扩展镜像的一部分进行分发，请参阅 [构建多架构扩展](../extensions/extensions/multi-arch.md#adding-multi-arch-binaries)。

## 示例

以下代码片段已整合在 [Kubernetes 示例扩展](https://github.com/docker/extensions-sdk/tree/main/samples/kubernetes-sample-extension) 中。它展示了如何通过分发 `kubectl` 命令行工具来与 Kubernetes 集群进行交互。

### 检查 Kubernetes API 服务器是否可访问

一旦 `kubectl` 命令行工具被添加到扩展镜像的 `Dockerfile` 中，并在 `metadata.json` 中定义后，当扩展安装时，Extensions 框架会将 `kubectl` 部署到用户的主机上。

您可以使用 JS API `ddClient.extension.host?.cli.exec` 来执行 `kubectl` 命令，例如，检查在特定上下文下 Kubernetes API 服务器是否可访问：

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

以下是从主机文件系统持久化和读取 `kubeconfig` 文件的不同方法。用户可以随时向 `kubeconfig` 文件添加、编辑或删除 Kubernetes 上下文。

> 警告
>
> `kubeconfig` 文件非常敏感，如果被获取，可能会让攻击者获得对 Kubernetes 集群的管理访问权限。

### 扩展的后端容器

如果您需要扩展在读取 `kubeconfig` 文件后对其进行持久化，您可以使用一个后端容器，该容器暴露一个 HTTP POST 端点，将文件内容存储在内存中或容器文件系统的某个位置。这样，如果用户从扩展导航到 Docker Desktop 的其他部分然后再返回，您就不需要再次读取 `kubeconfig` 文件。

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

卷是持久化 Docker 容器生成和使用的数据的首选机制。您可以利用它们来持久化 `kubeconfig` 文件。
通过将 `kubeconfig` 持久化在卷中，当扩展面板关闭时，您就不需要再次读取 `kubeconfig` 文件。这使得它成为在从扩展导航到 Docker Desktop 其他部分时持久化数据的理想选择。

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

`localStorage` 是浏览器 Web 存储的机制之一。它允许用户以键值对的形式将数据保存在浏览器中，以供以后使用。
`localStorage` 在浏览器（扩展面板）关闭时不会清除数据。这使得它成为在从扩展导航到 Docker Desktop 其他部分时持久化数据的理想选择。

```typescript
localStorage.setItem("kubeconfig", kubeConfig);
```

```typescript
localStorage.getItem("kubeconfig");
```