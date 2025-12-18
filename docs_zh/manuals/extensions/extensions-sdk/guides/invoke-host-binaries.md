---
title: 调用宿主机二进制文件
description: 使用扩展 SDK 从前端调用宿主机上的二进制文件。
keywords: Docker, extensions, sdk, build
aliases:
 - /desktop/extensions-sdk/guides/invoke-host-binaries/
---

在某些情况下，您的扩展可能需要从宿主机调用一些命令。例如，您可能需要调用云提供商的 CLI 来创建新资源，或调用扩展提供的工具的 CLI，甚至运行宿主机上的 shell 脚本。

您可以通过扩展 SDK 在容器中执行 CLI 来实现这一点。但该 CLI 需要访问宿主机的文件系统，如果它在容器中运行，这既不方便也不高效。

本文档介绍如何在宿主机上运行作为扩展一部分分发并部署到宿主机的可执行文件（二进制文件、shell 脚本）。由于扩展可以在多个平台上运行，这意味着您需要为所有要支持的平台提供相应的可执行文件。

深入了解扩展的[架构](../architecture/_index.md)。

> [!NOTE]
>
> 请注意，扩展以用户权限运行，此 API 不限制在扩展元数据的 [host 部分](../architecture/metadata.md#host-section) 中列出的二进制文件（某些扩展可能在用户交互期间安装软件，并调用新安装的二进制文件，即使它们未在扩展元数据中列出）。

在本示例中，CLI 是一个简单的 `Hello world` 脚本，需要带参数调用并返回字符串。

## 将可执行文件添加到扩展

{{< tabs >}}
{{< tab name="Mac 和 Linux" >}}

为 macOS 和 Linux 创建一个 `bash` 脚本，文件路径为 `binaries/unix/hello.sh`，内容如下：

```bash
#!/bin/sh
echo "Hello, $1!"
```

{{< /tab >}}
{{< tab name="Windows" >}}

为 Windows 创建一个 `batch script`，文件路径为 `binaries/windows/hello.cmd`，内容如下：

```bash
@echo off
echo "Hello, %1!"
```

{{< /tab >}}
{{< /tabs >}}

然后更新 `Dockerfile`，将 `binaries` 文件夹复制到扩展容器的文件系统中，并使文件可执行。

```dockerfile
# Copy the binaries into the right folder
COPY --chmod=0755 binaries/windows/hello.cmd /windows/hello.cmd
COPY --chmod=0755 binaries/unix/hello.sh /linux/hello.sh
COPY --chmod=0755 binaries/unix/hello.sh /darwin/hello.sh
```

## 从 UI 调用可执行文件

在您的扩展中，使用 Docker Desktop Client 对象通过 `ddClient.extension.host.cli.exec()` 函数[调用扩展提供的 shell 脚本](../dev/api/backend.md#invoke-an-extension-binary-on-the-host)。
在本示例中，二进制文件返回一个字符串作为结果，通过 `result?.stdout` 获取，扩展视图渲染后立即执行。

{{< tabs group="framework" >}}
{{< tab name="React" >}}

```typescript
export function App() {
  const ddClient = createDockerDesktopClient();
  const [hello, setHello] = useState("");

  useEffect(() => {
    const run = async () => {
      let binary = "hello.sh";
      if (ddClient.host.platform === 'win32') {
        binary = "hello.cmd";
      }

      const result = await ddClient.extension.host?.cli.exec(binary, ["world"]);
      setHello(result?.stdout);

    };
    run();
  }, [ddClient]);
    
  return (
    <div>
      {hello}
    </div>
  );
}
```

{{< /tab >}}
{{< tab name="Vue" >}}

> [!IMPORTANT]
>
> 我们还没有 Vue 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Vue)
> 并告诉我们您是否需要 Vue 示例。

{{< /tab >}}
{{< tab name="Angular" >}}

> [!IMPORTANT]
>
> 我们还没有 Angular 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> 并告诉我们您是否需要 Angular 示例。

{{< /tab >}}
{{< tab name="Svelte" >}}

> [!IMPORTANT]
>
> 我们还没有 Svelte 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> 并告诉我们您是否需要 Svelte 示例。

{{< /tab >}}
{{< /tabs >}}

## 配置元数据文件

宿主机二进制文件必须在 `metadata.json` 文件中指定，以便 Docker Desktop 在安装扩展时将它们复制到宿主机。一旦扩展被卸载，已复制的二进制文件也会被删除。

```json
{
  "vm": {
    ...
  },
  "ui": {
    ...
  },
  "host": {
    "binaries": [
      {
        "darwin": [
          {
            "path": "/darwin/hello.sh"
          }
        ],
        "linux": [
          {
            "path": "/linux/hello.sh"
          }
        ],
        "windows": [
          {
            "path": "/windows/hello.cmd"
          }
        ]
      }
    ]
  }
}
```

`path` 必须引用容器内二进制文件的路径。