---
title: Python 的代码检查、格式化和类型检查
linkTitle: 代码检查和类型检查
weight: 25
keywords: Python, linting, formatting, type checking, ruff, pyright
description: 了解如何为你的 Python 应用设置代码检查、格式化和类型检查。
aliases:
  - /language/python/lint-format-typing/
---

## 前置条件

完成 [开发你的应用](develop.md)。

## 概述

在本节中，你将学习如何为你的 Python 应用设置代码质量工具。包括：

- 使用 Ruff 进行代码检查和格式化
- 使用 Pyright 进行静态类型检查
- 使用 pre-commit hooks 自动化检查

## 使用 Ruff 进行代码检查和格式化

Ruff 是一个用 Rust 编写的极快的 Python 代码检查和格式化工具。它用一个统一的工具替代了 flake8、isort 和 black 等多个工具。

在使用 Ruff 之前，先在你的 Python 环境中安装它：

```bash
pip install ruff
```

如果你使用虚拟环境，请确保它已激活，这样运行下面的命令时 `ruff` 命令才可用。

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

运行以下命令检查和格式化你的代码：

```bash
# 检查错误
ruff check .

# 自动修复可修复的错误
ruff check --fix .

# 格式化代码
ruff format .
```

## 使用 Pyright 进行类型检查

Pyright 是一个快速的 Python 静态类型检查工具，对现代 Python 特性支持良好。

在 `pyproject.toml` 中添加 `Pyright` 配置：

```toml
[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
```

### 运行 Pyright

检查代码中的类型错误：

```bash
pyright
```

## 设置 pre-commit hooks

pre-commit hooks 在每次提交前自动运行检查。以下 `.pre-commit-config.yaml` 片段设置了 Ruff：

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

在本节中，你学会了如何：

- 配置和使用 Ruff 进行代码检查和格式化
- 设置 Pyright 进行静态类型检查
- 使用 pre-commit hooks 自动化检查

这些工具帮助保持代码质量，并在开发早期发现错误。

## 后续步骤

- [配置 GitHub Actions](configure-github-actions.md) 自动运行这些检查
- 自定义代码检查规则以匹配团队的风格偏好
- 探索高级类型检查功能