# Droid


本指南涵盖在沙箱环境中使用 Droid（Factory 公司推出的 AI 编程代理）的身份验证、配置与操作方法。

官方文档：[Droid](https://docs.factory.ai/)

## 快速开始

创建沙箱并为项目目录运行 Droid：

```console
$ sbx run droid ~/my-project
```

工作空间参数为可选，默认为当前目录：

```console
$ cd ~/my-project
$ sbx run droid
```

## 身份验证

Droid 需要使用 [Factory 账户](https://factory.ai)。这两种身份验证方式都会直接向 Factory 的服务验证您的身份——与其他需要您提供模型提供商密钥的代理不同，Factory 通过您的 Factory 账户来管理模型访问。

**API 密钥**：使用[存储的密钥](../security/credentials.md#stored-secrets)保存您的 Factory API 密钥：

```console
$ sbx secret set droid
```

**OAuth**：如果未设置 API 密钥，Droid 会在首次运行时提示您交互式登录。代理会处理 OAuth 流程，因此凭据不会存储在沙箱内部。

## 配置

沙箱不会获取您主机上的用户级配置。沙箱内部仅能使用工作目录中的项目级配置。相关变通方法请参阅
[为什么沙箱不使用我的用户级代理配置？](../faq.md#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)。

### Default startup command

沙箱运行 `droid`，不带任何隐式标志。`--` 之后的参数会直接透传：

```console
$ sbx run droid -- exec "fix the build"
```

## Base image

模板：`docker/sandbox-templates:droid-docker`

已预配置为无需批准提示即可运行。身份验证状态会在沙箱重启后保留。

如需预装工具或自定义此环境，请参阅[自定义](../customize/)。
