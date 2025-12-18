#!/usr/bin/env bash

#============================================================
# File: translate.sh
# Description: AI 翻译
# URL: 
# Author: Jetsung Chan <i@jetsung.com>
# Version: 0.1.0
# CreatedAt: 2025-12-16
# UpdatedAt: 2025-12-16
#============================================================


if [[ -n "${DEBUG:-}" ]]; then
    set -eux
else
    set -euo pipefail
fi

DEFAULT_BRANCH="main"
HUGO_VERSION=0.141.0

install_hugo() {
    curl -sLJ -o "/tmp/hugo.tar.gz" "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz" 
    tar -C /tmp -xf /tmp/hugo.tar.gz
    chmod +x /tmp/hugo
    /tmp/hugo version
    echo "/tmp/hugo version"
}

# 增量更新
incremental_update() {
    git remote add upstream https://github.com/docker/docs.git
    git fetch upstream main
    git checkout upstream/main -- content
    rm -rf docs
    mv content docs
    git diff docs
}

usage() {
    cat << EOF
用法: $0 [选项]

选项:
  --hugo      安装 Hugo extended（linux-amd64）
  --help      显示此帮助信息

示例:
  $0 --hugo
EOF
}

main() {
    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi

    while [[ $# -gt 0 ]]; do
        case $1 in
            --hugo)
                install_hugo
                shift
                ;;
            --help|-h)
                usage
                exit 0
                ;;
            *)
                echo "未知参数: $1" >&2
                usage
                exit 1
                ;;
        esac
    done
}

main "$@"
