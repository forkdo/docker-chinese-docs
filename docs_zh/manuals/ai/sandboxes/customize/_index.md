---
title: 自定义沙箱
linkTitle: Customize
description: 构建可复用的沙箱镜像，使用工具和凭据扩展代理，并使用模板和套件定义自定义代理。
keywords: sandboxes, sbx, customize, templates, kits, mixins, custom agents
weight: 60
aliases:
  - /ai/sandboxes/agents/custom-environments/
params:
  sidebar:
    badge:
      color: blue
      text: Early Access
---

{{< summary-bar feature_name="Docker Sandboxes sbx" >}}

除了内置默认值之外，Docker Sandboxes 提供两种自定义沙箱的方式：

- [模板](templates.md) — 内置了工具、软件包和配置的可复用沙箱镜像。使用 Dockerfile 扩展基础镜像，或将运行中的沙箱保存为模板。
- [套件（Kits）](kits.md) — 声明式 YAML 制品，在运行时使用工具、凭据、网络规则和文件扩展代理，或从零定义一个新的代理。

套件处于实验阶段。用于创建、加载和管理套件的套件文件格式、CLI 命令和体验会随着功能的演进而变化。请在 [docker/sbx-releases](https://github.com/docker/sbx-releases) 仓库中提交反馈和错误报告。

## 模板与套件，并排对比

模板是沙箱运行的 Docker 镜像。它使用 Dockerfile 提前构建（或从运行中的沙箱保存），推送到镜像仓库，并在创建沙箱时拉取。将属于镜像的内容用模板：系统软件包、语言工具链、大型依赖项——任何你不想每次启动沙箱都重新安装的东西。

套件是应用于沙箱创建的 YAML 制品。套件可以运行安装命令、将文件放入沙箱、声明网络和凭据规则，以及（对于沙箱套件）定义代理运行的模板镜像。将随代理或团队而变化的内容用套件：共享的 linter 配置、项目特定的安装步骤、代理所通信服务的凭据注入。

模板和套件可以协同工作。沙箱套件的 `sandbox.image` 字段指向一个模板：模板提供基础环境，套件在其之上叠加配置、密钥和运行时行为。一个团队可以发布一个重量级模板和数个轻量套件，而无需在每次变更时重新构建镜像。

## 何时使用哪个

| 目标                                              | 选项                                                          |
| ------------------------------------------------- | ------------------------------------------------------------- |
| 将工具和软件包预装到可复用的基础镜像中            | [模板](templates.md)                                          |
| 捕获一个已配置的运行中沙箱以便复用                | [已保存的模板](templates.md#saving-a-sandbox-as-a-template)   |
| 通过 YAML 为代理运行添加工具、凭据或配置          | [套件（mixin）](kits.md)                                      |
| 从零定义一个新的代理                              | [套件（sandbox）](kits.md#define-an-agent)                    |

模板和套件可以一起使用。模板将重量级工具烘焙进镜像以实现快速沙箱启动；叠加在其上的套件添加每次运行的凭据、配置或额外能力。

## 教程

- [构建你自己的代理套件](build-an-agent.md) — 将 [Amp](https://ampcode.com/) 打包为沙箱套件的分步演示。
