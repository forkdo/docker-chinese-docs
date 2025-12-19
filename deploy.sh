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
    curl -L https://fx4.cn/hugo | bash -s -- -v "$HUGO_VERSION" -w
}

# 增量更新
incremental_update() {
    git remote set-url upstream https://github.com/docker/docs.git
    git fetch upstream main
    git checkout upstream/main -- content
    rm -rf docs
    mv content docs
    # git diff docs/
}

# 复制 docs_zh 至  content
copy_docs_zh() {
    if [[ ! -d docsite ]]; then
        git clone https://github.com/docker/docs.git docsite
    fi
    cp -r docs_zh/* docsite/content
}

# 调用翻译脚本
translate() {
    uv run translate.py
}

usage() {
    cat << EOF
用法: $0 [选项]

选项:
  -c --copy      复制 docs_zh
  -i --incremental   增量更新
  -s --hugo      安装 Hugo extended（linux-amd64）
  -t --translate  调用翻译脚本
  -h --help      显示此帮助信息

示例:
  $0 --hugo
  $0 --translate
EOF
}

main() {
    if [[ $# -eq 0 ]]; then
        usage
        exit 1
    fi

    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--copy)
                copy_docs_zh
                shift
                ;;
            -i|--incremental)
                incremental_update
                shift
                ;;
            -s|--hugo)
                install_hugo
                shift
                ;;
            -t|--translate)
                translate
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
