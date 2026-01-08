---
title: Python 的代码检查、格式化与类型检查
linkTitle: 代码检查与类型检查
weight: 25
keywords: Python, linting, formatting, type checking, ruff, pyright
description: 了解如何为您的 Python 应用程序设置代码检查、格式化和类型检查。
aliases:
- /language/python/lint-format-typing/
---

## 前提条件

请先完成 [开发您的应用程序](develop.md)。

## 概述

在本节中，您将学习如何为 Python 应用程序设置代码质量工具。这些工具包括：

- 使用 Ruff 进行代码检查和格式化
- 使用 Pyright 进行静态类型检查
- 通过 pre-commit 钩子自动化检查流程

## 使用 Ruff 进行代码检查和格式化

Ruff 是一个用 Rust 编写的、速度极快的 Python 代码检查器和格式化工具。它用一个统一的工具取代了 flake8、isort 和 black 等多个工具。

在使用 Ruff 之前，请先在您的 Python 环境中安装它：

```bash
pip install ruff
```

如果您使用的是虚拟环境，请确保它已激活，以便在运行以下命令时可以使用 `ruff` 命令。

创建一个 `pyproject.toml` 文件：

```toml
[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]
```

### 使用 Ruff

运行以下命令来检查和格式化您的代码：

```bash
# 检查错误
ruff check .

# 自动修复可修复的错误
ruff check --fix .

# 格式化代码
ruff format .
```

## 使用 Pyright 进行类型检查

Pyright 是一个快速的 Python 静态类型检查器，与现代 Python 特性配合良好。

在 `pyproject.toml` 中添加 `Pyright` 配置：

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
```

### 运行 Pyright

要检查代码中的类型错误：

```bash
pyright
```

## 设置 pre-commit 钩子

Pre-commit 钩子会在每次提交之前自动运行检查。以下 `.pre-commit-config.yaml` 片段设置了 Ruff：

```yaml
  https: https://github.com/charliermarsh/ruff-pre-commit
  rev: v0.2.2
  hooks:
    - id: ruff
      args: [--fix]
    - id: ruff-format
```

安装和使用方法：

```bash
pre-commit install
git commit -m "Test commit"  # 自动运行检查
```

## 总结

在本节中，您学习了如何：

- 配置和使用 Ruff 进行代码检查和格式化
- 设置 Pyright 进行静态类型检查
- 使用 pre-commit 钩子自动化检查流程

这些工具有助于维护代码质量，并在开发早期发现错误。

## 后续步骤

- [配置 GitHub Actions](configure-github-actions.md) 以自动运行这些检查
- 自定义代码检查规则以符合您团队的风格偏好
- 探索高级类型检查功能