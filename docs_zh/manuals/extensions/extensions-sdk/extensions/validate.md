---
title: 验证您的扩展
linkTitle: 验证
description: 扩展创建过程的第三步
keywords: Docker, Extensions, sdk, validate, install
aliases:
 - /desktop/extensions-sdk/extensions/validation/
 - /desktop/extensions-sdk/build/build-install/
 - /desktop/extensions-sdk/dev/cli/build-test-install-extension/
 - /desktop/extensions-sdk/extensions/validate/
weight: 20
---

在分享或发布扩展之前，请先对其进行验证。验证扩展可确保扩展：

- 构建时包含了[镜像标签](labels.md)，以便在市场中正确显示
- 能够正常安装和运行

Extensions CLI 允许您在本地安装和运行扩展之前对其进行验证。

验证过程会检查扩展的 `Dockerfile` 是否指定了所有必需的标签，以及元数据文件是否符合 JSON 模式文件的要求。

要进行验证，请运行：

```console
$ docker extension validate <your-extension-name>
```

如果您的扩展有效，将显示以下消息：

```console
The extension image "your-extension-name" is valid
```

在构建镜像之前，也可以仅验证 `metadata.json` 文件：

```console
$ docker extension validate /path/to/metadata.json
```

用于验证 `metadata.json` 文件的 JSON 模式可以在[发布页面](https://github.com/docker/extensions-sdk/releases/latest)下找到。