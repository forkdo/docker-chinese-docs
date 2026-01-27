# 支持的代理




Docker Sandboxes 支持多种 AI 编码代理。所有代理都在带有私有 Docker 守护进程的 microVM 中隔离运行。

## 支持的代理

| 代理 | 命令 | 状态 | 说明 |
| ----------- | -------- | ------------ | -------------------------- |
| Claude Code | `claude` | 实验性 | 经过最多测试的实现 |
| Codex | `codex` | 实验性 | 开发中 |
| Gemini | `gemini` | 实验性 | 开发中 |
| cagent | `cagent` | 实验性 | 开发中 |
| Kiro | `kiro` | 实验性 | 开发中 |

## 实验性状态

所有代理均为实验性功能。这意味着：

- Docker Desktop 版本之间可能发生破坏性变更
- 功能可能不完整或发生重大变化
- 稳定性和性能未达到生产就绪水平
- 支持和文档有限

请将沙箱用于开发和测试，而非生产工作负载。

## 使用不同的代理

代理类型在创建沙箱时指定：

```console
$ docker sandbox create claude ~/my-project
$ docker sandbox create codex ~/my-project
$ docker sandbox create gemini ~/my-project
$ docker sandbox create cagent ~/my-project
$ docker sandbox create kiro ~/my-project
```

每个代理都在其独立的隔离沙箱中运行。代理类型在创建时绑定到沙箱，之后无法更改。

## 代理特定配置

不同的代理可能需要不同的身份验证方法或配置。请参阅代理特定的文档：

- [Claude Code 配置](claude-code.md)

## 要求

- Docker Desktop 4.58 或更高版本
- 平台支持：
  - 支持 virtualization.framework 的 macOS
  - 支持 Hyper-V 的 Windows \[实验性\]

- 所选代理的 API 密钥或凭据

## 后续步骤

- [Claude Code 配置](claude-code.md)
- [自定义模板](templates.md)
- [有效使用沙箱](workflows.md)
