---
title: 调用主机二进制文件
description: 使用扩展 SDK 从前端添加对主机二进制文件的调用。
keywords: Docker, extensions, sdk, build
aliases:
 - /desktop/extensions-sdk/guides/invoke-host-binaries/
---

在某些情况下，您的扩展可能需要调用主机上的某些命令。例如，您可能希望调用云提供商的 CLI 来创建新资源，或调用扩展提供的工具的 CLI，甚至运行主机上的 shell 脚本。

您可以通过使用扩展 SDK 在容器中执行 CLI 来实现这一点。但是，如果 CLI 在容器中运行，则它需要访问主机的文件系统，这既不容易也不快速。

本页介绍了如何运行作为扩展的一部分并部署到主机上的可执行文件（二进制文件、shell 脚本）。由于扩展可以在多个平台上运行，这意味着您需要为所有希望支持的平台提供可执行文件。

了解更多关于扩展的[架构](../architecture/_index.md)。

> [!NOTE]
>
> 请注意，扩展以用户访问权限运行，此 API 不限于扩展元数据中[主机部分](../architecture/metadata.md#host-section)列出的二进制文件（某些扩展可能在用户交互期间安装软件，并调用新安装的二进制文件，即使未在扩展元数据中列出）。

在此示例中，CLI 是一个简单的 `Hello world` 脚本，必须使用参数调用并返回字符串。

## 将可执行文件添加到扩展中

{{< tabs >}}
{{< tab name="Mac 和 Linux" >}}

为 macOS 和 Linux 创建一个 `bash` 脚本，文件名为 `binaries/unix/hello.sh`，内容如下：

```bash
#!/bin/sh
echo "Hello, $1!"
```

{{< /tab >}}
{{< tab name="Windows" >}}

为 Windows 创建另一个 `批处理脚本`，文件名为 `binaries/windows/hello.cmd`，内容如下：

```bash
@echo off
echo "Hello, %1!"
```

{{< /tab >}}
{{< /tabs >}}

然后更新 `Dockerfile`，将 `binaries` 文件夹复制到扩展的容器文件系统中，并使文件可执行。

```dockerfile
# 将二进制文件复制到正确的文件夹
COPY --chmod=0755 binaries/windows/hello.cmd /windows/hello.cmd
COPY --chmod=0755 binaries/unix/hello.sh /linux/hello.sh
COPY --chmod=0755 binaries/unix/hello.sh /darwin/hello.sh
```

## 从 UI 调用可执行文件

在您的扩展中，使用 Docker Desktop 客户端对象通过 `ddClient.extension.host.cli.exec()` 函数[调用扩展提供的主机上的 shell 脚本](../dev/api/backend.md#invoke-an-extension-binary-on-the-host)。
在此示例中，二进制文件返回一个字符串作为结果，通过 `result?.stdout` 获取，一旦扩展视图被渲染。

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
> 并告诉我们您是否需要一个 Vue 的示例。

{{< /tab >}}
{{< tab name="Angular" >}}

> [!IMPORTANT]
>
> 我们还没有 Angular 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Angular)
> 并告诉我们您是否需要一个 Angular 的示例。

{{< /tab >}}
{{< tab name="Svelte" >}}

> [!IMPORTANT]
>
> 我们还没有 Svelte 的示例。[填写表单](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url&entry.1333218187=Svelte)
> 并告诉我们您是否需要一个 Svelte 的示例。

{{< /tab >}}
{{< /tabs >}}

## 配置元数据文件

主机二进制文件必须在 `metadata.json` 文件中指定，以便 Docker Desktop 在安装扩展时将其复制到主机上。一旦扩展被卸载，复制的二进制文件也会被删除。

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