#!/usr/bin/env bash

#============================================================
# File: deploy.sh
# Description: 部署
# URL: 
# Author: Jetsung Chan <i@jetsung.com>
# Version: 0.2.0
# CreatedAt: 2025-12-16
# UpdatedAt: 2026-01-08
#============================================================


if [[ -n "${DEBUG:-}" ]]; then
    set -eux
else
    set -euo pipefail
fi

DEFAULT_BRANCH="main"
HUGO_VERSION=0.141.0

DELETE_FILE="deleted_docs.txt"
ADD_FILE="new_docs.txt"
MODIFIED_FILE="modified_docs.txt"
TRANSLATE_LIST="translate_list.txt"

install_hugo() {
    curl -L https://fx4.cn/hugo | bash -s -- -v "$HUGO_VERSION" -w
}

# 增量更新
incremental_update() {
    [[ -d docsite ]] || mkdir docsite
    
    pushd docsite
    if [[ -d .git ]]; then
        git remote set-url upstream https://github.com/docker/docs.git
    else
        git init
        git remote add upstream https://github.com/docker/docs.git
    fi
    git fetch upstream main
    git checkout upstream/main -- content
    popd

    cp -r docsite/content .
    rm -rf docs
    mv content docs

    # 记录删除的文件
    git ls-files --deleted docs/ | tee "$DELETE_FILE"
    export ROOT_DIR=$(grep root_dir config.toml | cut -d'"' -f 2 | sed 's|^\./||')
    export OUTPUT_DIR=$(grep output_dir config.toml | cut -d'"' -f 2 | sed 's|^\./||')
    # sed -i "s|^$ROOT_DIR/|$OUTPUT_DIR/|g" "$DELETE_FILE"
    # 删除对应的输出文件
    while read -r file; do
        new_file="${file/$ROOT_DIR/$OUTPUT_DIR}"
        echo "$new_file"
        rm -rf "$new_file" || true
    done < "$DELETE_FILE"

    # 更新 git 索引
    git add .
    # 记录新增和修改的文件
    git diff --cached --name-only --diff-filter=A docs/ | tee "$ADD_FILE"
    git diff --cached --name-only --diff-filter=M docs/ | tee "$MODIFIED_FILE"

    cat "$ADD_FILE" "$MODIFIED_FILE" | tee "$TRANSLATE_LIST"

    # 移除以 .png .jpg .jpeg .gif 结尾的文件
    sed -i '/\.\(png\|jpg\|jpeg\|gif\)$/d' "$TRANSLATE_LIST"

    # 合并 config.toml
    merge_config

    # # 翻译增量文件
    # if ! command -v aitr &> /dev/null; then
    #     echo "正在安装 aitr ..."
    #     curl -L https://fx4.cn/aitr | bash
    # fi

    # 调用 aitr 进行翻译
    if command -v aitr &> /dev/null; then
        aitr --input translate_list.txt --list --output translated
        cp -r "translated/${ROOT_DIR}/"* "${OUTPUT_DIR}"/
    else
        echo "aitr 未安装，跳过构建步骤。"
    fi
}

merge_config() {
    if [[ -f config.example.toml ]]; then
        sed '/providers/,$d' ./config.example.toml | tee config.toml
    fi

    if [[ -f aitr.toml ]]; then
        sed -n '/logging/,$p' aitr.toml | tee -a config.toml
    fi
}

# Patch Hugo layouts to avoid errors on missing metadata
patch_hugo_layouts() {
    if [[ -d docsite/layouts ]]; then
        sed -i 's/errorf "\[summary-bar\]/warnf "[summary-bar]/g' docsite/layouts/shortcodes/summary-bar.html || true
        sed -i 's/errorf "\[tags\]/warnf "[tags]/g' docsite/layouts/partials/tags.html || true
        sed -i 's/errorf "\[languages\]/warnf "[languages]/g' docsite/layouts/partials/languages.html || true
    fi
}

# 复制 docs_zh 至  content
copy_docs_zh() {
    if [[ ! -d docsite ]]; then
        git clone https://github.com/docker/docs.git docsite
    fi
    patch_hugo_layouts
    cp -r docs_zh/* docsite/content
}

# 本地测试
start_dev() {
    copy_docs_zh
    cd docsite
    npm install
    hugo server -D
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
            -r|--start)
                start_dev
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
