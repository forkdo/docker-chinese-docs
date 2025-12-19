---
title: 自动补全
weight: 10
description: 设置您的 Shell，以获取 Docker 命令和标志的自动补全功能
keywords: cli, shell, fish, bash, zsh, completion, options
aliases:
  - /config/completion/
---

您可以使用 `docker completion` 命令为 Docker CLI 生成 Shell 补全脚本。当您在终端中输入命令并按下 `<Tab>` 键时，该补全脚本可为您提供命令、标志以及 Docker 对象（例如容器和卷名称）的单词补全功能。

您可以为以下 Shell 生成补全脚本：

- [Bash](#bash)
- [Zsh](#zsh)
- [fish](#fish)

## Bash

要在 Bash 中获取 Docker CLI 补全功能，首先需要安装 `bash-completion` 包，该包包含许多用于 Shell 补全的 Bash 函数。

```bash
# 使用 APT 安装：
sudo apt install bash-completion

# 使用 Homebrew 安装（Bash 4 或更高版本）：
brew install bash-completion@2
# 旧版 Bash 的 Homebrew 安装方式：
brew install bash-completion

# 使用 pacman 安装：
sudo pacman -S bash-completion
```

安装 `bash-completion` 后，在您的 Shell 配置文件中引用该脚本（在此示例中为 `.bashrc`）：

```bash
# 在 Linux 上：
cat <<EOT >> ~/.bashrc
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
EOT

# 在 macOS / 使用 Homebrew 时：
cat <<EOT >> ~/.bash_profile
[[ -r "$(brew --prefix)/etc/profile.d/bash_completion.sh" ]] && . "$(brew --prefix)/etc/profile.d/bash_completion.sh"
EOT
```

然后重新加载您的 Shell 配置：

```console
$ source ~/.bashrc
```

现在，您可以使用 `docker completion` 命令生成 Bash 补全脚本：

```console
$ mkdir -p ~/.local/share/bash-completion/completions
$ docker completion bash > ~/.local/share/bash-completion/completions/docker
```

## Zsh

Zsh 的[补全系统](http://zsh.sourceforge.net/Doc/Release/Completion-System.html)可以处理补全事宜，只要补全能够通过 `FPATH` 引用即可。

如果您使用 Oh My Zsh，则可以将补全脚本存储在 `~/.oh-my-zsh/completions` 目录中，而无需修改 `~/.zshrc` 即可安装补全功能。

```console
$ mkdir -p ~/.oh-my-zsh/completions
$ docker completion zsh > ~/.oh-my-zsh/completions/_docker
```

如果您不使用 Oh My Zsh，请将补全脚本存储在您选择的目录中，并将该目录添加到 `.zshrc` 中的 `FPATH`。

```console
$ mkdir -p ~/.docker/completions
$ docker completion zsh > ~/.docker/completions/_docker
```

```console
$ cat <<"EOT" >> ~/.zshrc
FPATH="$HOME/.docker/completions:$FPATH"
autoload -Uz compinit
compinit
EOT
```

## Fish

fish shell 原生支持[补全系统](https://fishshell.com/docs/current/#tab-completion)。
要激活 Docker 命令的补全功能，请将补全脚本复制或符号链接到您的 fish shell `completions/` 目录：

```console
$ mkdir -p ~/.config/fish/completions
$ docker completion fish > ~/.config/fish/completions/docker.fish
```