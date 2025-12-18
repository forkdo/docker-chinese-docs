---
title: 验证你的扩展
linkTitle: 验证
description: 扩展创建流程的第三步
keywords: Docker, Extensions, sdk, validate, install
aliases:
 - /desktop/extensions-sdk/extensions/validation/
 - /desktop/extensions-sdk/build/build-install/
 - /desktop/extensions-sdk/dev/cli/build-test-install-extension/
 - /desktop/extensions-sdk/extensions/validate/
weight: 20
---

在共享或发布扩展之前，请先验证它。验证扩展可确保：

- 使用了 [image labels](labels.md)，以便在市场中正确显示
- 可以正常安装和运行

Extensions CLI 允许你在本地安装和运行扩展之前先验证它。

验证过程会检查扩展的 `Dockerfile` 是否包含所有必需的标签，以及元数据文件是否符合 JSON schema 文件的规范。

运行以下命令进行验证：

```console
$ docker extension validate <name-of-your-extension>
```

如果扩展有效，将显示以下消息：

```console
The extension image "name-of-your-extension" is valid
```

在镜像构建之前，也可以仅验证 `metadata.json` 文件：

```console
$ docker extension validate /path/to/metadata.json
```

用于验证 `metadata.json` 文件的 JSON schema 可在 [releases 页面](https://github.com/docker/extensions-sdk/releases/latest) 找到。