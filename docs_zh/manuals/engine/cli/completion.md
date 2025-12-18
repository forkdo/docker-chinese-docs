---
title: 命令补全
weight: 10
description: 配置你的 shell 以获得 Docker 命令和标志的自动补全功能
keywords: cli, shell, fish, bash, zsh, completion, options
aliases:
  - /config/completion/
---

你可以使用 `docker completion` 命令为 Docker CLI 生成 shell 补全脚本。补全脚本会在你于终端中键入 `<Tab>` 时，为命令、标志和 Docker 对象（如容器和卷名称）提供自动补全功能。

你可以为以下 shell 生成补全脚本：

- [Bash](#bash)
- [Zsh](#zsh)
- [fish](#fish)

## Bash

要在 Bash 中获得 Docker CLI 补全功能，首先需要安装 `bash-completion` 包，该包包含多个用于 shell 补全的 Bash 函数。

```bash
# 使用 APT 安装：
sudo apt install bash-completion

# 使用 Homebrew 安装（Bash 版本 4 或更高）：
brew install bash-completion@2
# Homebrew 安装旧版本 Bash：
brew install bash-completion

# 使用 pacman 安装：
sudo pacman -S bash-completion
```

安装 `bash-completion` 后，将脚本加载到你的 shell 配置文件中（本例中为 `.bashrc`）：

```bash
# 在 Linux 上：
cat <<EOT >> ~/.bashrc
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
EOT

# 在 macOS / 使用 Homebrew 上：
cat <<EOT >> ~/.bash_profile
[[ -r "$(brew --prefix)/etc/profile.d/bash_completion.sh" ]] && . "$(brew --prefix)/etc/profile.d/bash_completion.sh"
EOT
```

然后重新加载你的 shell 配置：

```console
$ source ~/.bashrc
```

现在你可以使用 `docker completion` 命令生成 Bash 补全脚本：

```console
$ mkdir -p ~/.local/share/bash-completion/completions
$ docker completion bash > ~/.local/share/bash-completion/completions/docker
```

## Zsh

Zsh 的 [补全系统](http://zsh.sourceforge.net/Doc/Release/Completion-System.html) 会自动处理，只要补全脚本可以通过 `FPATH` 加载即可。

如果你使用 Oh My Zsh，可以将补全脚本安装到 `~/.oh-my-zsh/completions` 目录中，而无需修改 `~/.zshrc`。

```console
$ mkdir -p ~/.oh-my-zsh/completions
$ docker completion zsh > ~/.oh-my-zsh/completions/_docker
```

如果你不使用 Oh My Zsh，请将补全脚本存储在任意目录中，并将该目录添加到 `.zshrc` 中的 `FPATH`。

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

fish shell 原生支持 [补全系统](https://fishshell.com/docs/current/#tab-completion)。要启用 Docker 命令的补全功能，只需将补全脚本复制或符号链接到你的 fish shell `completions/` 目录：

```console
$ mkdir -p ~/.config/fish/completions
$ docker completion fish > ~/.config/fish/completions/docker.fish
```