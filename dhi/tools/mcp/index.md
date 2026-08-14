# Use the DHI MCP server


Docker Hardened Images (DHI) MCP 服务器通过模型上下文协议 (MCP) 暴露 DHI 目录，让您能够使用自然语言直接从 AI 助手查询仓库、检查镜像元数据、检索 SBOM 并检查 CVE。

DHI MCP 服务器具有以下特点：

- 远程。无需安装本地二进制文件。您的 AI 助手直接连接到 `https://dhi.io/mcp`。
- 兼容任何支持 MCP 的 AI 助手，包括 Claude、Cursor 等。

大多数工具是公开的，无需凭据。镜像管理工具（`dhi_list_mirrors`、`dhi_create_mirror`、`dhi_remove_mirror`）需要具有目标组织所有者访问权限的 Docker Hub 用户名和个人访问令牌 (PAT)。凭据作为 MCP 客户端配置中的 HTTP Basic 认证头传递 —— 它们绝不作为工具参数传递。

## 连接您的 AI 助手

配置因客户端而异。选择您的 AI 助手对应的标签页。

**Claude Desktop**



将以下内容添加到您的 Claude Desktop 配置文件中：

```json
{
  "mcpServers": {
    "dhi": {
      "url": "https://dhi.io/mcp"
    }
  }
}
```

配置文件位于：
- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

**Cursor**



将以下内容添加到项目中的 `.cursor/mcp.json`，或全局添加到 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "dhi": {
      "url": "https://dhi.io/mcp"
    }
  }
}
```

**Claude Code**



运行以下命令以添加 DHI MCP 服务器：

```console
$ claude mcp add dhi --url https://dhi.io/mcp
```

或手动添加到项目中的 `.claude/mcp.json`：

```json
{
  "mcpServers": {
    "dhi": {
      "url": "https://dhi.io/mcp"
    }
  }
}
```

**Docker Agent**



在您的 [Docker Agent](/manuals/ai/docker-agent/_index.md) YAML 配置中，将 DHI MCP 服务器添加为远程工具集：

```yaml
toolsets:
  - type: mcp
    remote:
      url: "https://dhi.io/mcp"
      transport_type: streamable
```

例如，要创建一个能够回答有关 DHI 目录问题的代理：

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    description: DHI catalog assistant
    instruction: |
      Help me find and evaluate Docker Hardened Images.
      Search the DHI catalog, inspect image details, check CVEs,
      and retrieve SBOMs and attestations as needed.
    toolsets:
      - type: mcp
        remote:
          url: "https://dhi.io/mcp"
          transport_type: streamable
```

使用以下命令运行代理：

```console
$ docker agent run dhi-agent.yaml
```



## 可用工具

DHI MCP 服务器提供十个工具，AI 助手会根据您的提问自动调用：

| 工具 | 功能 |
|------|-------------|
| `dhi_list_repositories` | 按名称、类型、类别、FIPS 或 STIG 合规性搜索和筛选 DHI 目录 |
| `dhi_get_repository` | 获取仓库的完整详情：标签定义、构建配置、平台和每个清单的漏洞数量 |
| `dhi_get_tag_definition` | 获取单个标签定义的深入视图 |
| `dhi_get_image_details` | 获取每个摘要的详情：标签、平台、大小、层数和包数、漏洞严重级别数量以及证明类型 |
| `dhi_get_image_packages` | 检索完整的软件物料清单 (SBOM)：包名、版本、类型、purl、许可证和文件位置 |
| `dhi_get_image_cves` | 列出 CVE，包含严重性、CVSS 评分、修复版本、EPSS 评分和 CISA 已利用标志；可按最低严重性或无修复项进行筛选 |
| `dhi_get_image_attestations` | 列出特定镜像摘要的 SBOM、来源、签名及其他证明 |
| `dhi_list_mirrors` | 列出 Docker Hub 组织已镜像的 DHI 仓库 —— 需要身份验证 |
| `dhi_create_mirror` | 开始将 DHI 仓库镜像到 Docker Hub 组织 —— 需要身份验证 |
| `dhi_remove_mirror` | 按镜像 ID 停止镜像某个仓库 —— 需要身份验证 |

## 为镜像工具进行身份验证

镜像工具需要具有目标组织所有者访问权限的 Docker Hub 用户名和[个人访问令牌 (PAT)](/security/access-tokens/)，作为 HTTP Basic 认证头传递。使用以下命令生成该值：

```console
$ printf 'USERNAME:dckr_pat_...' | base64 | tr -d '\n'
```

然后将其添加到您的 MCP 客户端配置中：

> [!WARNING]
> Base64 编码并非加密。您配置文件中的值实际上等同于明文密码。请勿将该文件提交到版本控制或分享它。

```json
{
  "mcpServers": {
    "dhi": {
      "url": "https://dhi.io/mcp",
      "headers": {
        "Authorization": "Basic <base64-value>"
      }
    }
  }
}
```

在没有凭据的情况下，只读目录工具可正常工作，而镜像工具会返回身份验证错误。

## 工具返回的内容

每个工具都返回结构化数据，您的 AI 助手可以对其进行汇总、比较或据此采取行动：

- `dhi_list_repositories` 返回仓库列表，包含显示名称、发行版、平台、FIPS/STIG 标志、包含的工具和类别。
- `dhi_get_repository` 返回完整的仓库记录，包括所有标签定义及其标签、构建配置、镜像索引，以及包含漏洞计数的每平台清单摘要。
- `dhi_get_tag_definition` 返回标签、构建参数、入口点、环境变量、运行用户，以及单个标签定义的每平台清单。
- `dhi_get_image_details` 返回镜像平台、压缩大小、层数量、包数量、按级别的漏洞严重性计数、标签，以及证明谓词类型列表。
- `dhi_get_image_packages` 返回镜像中的每个包，包含其名称、版本、类型（`deb`、`rpm`、`apk` 等）、purl、许可证以及找到它的文件路径。
- `dhi_get_image_cves` 返回影响镜像的每个 CVE，包含其严重性、CVSS 评分和向量、受影响的包、修复版本（如果有）、EPSS 概率评分，以及指示 CISA 是否将其列为已被积极利用的标志。
- `dhi_get_image_attestations` 返回附加到镜像摘要的每个证明的谓词类型和 OCI 引用。
- `dhi_list_mirrors` 返回给定组织的每个镜像的 ID、源 DHI 仓库、目标仓库和镜像状态。
- `dhi_create_mirror` 开始将 DHI 源仓库镜像到指定的组织和目标仓库名称。
- `dhi_remove_mirror` 停止指定镜像 ID 的镜像。它不会删除目标仓库 —— 只是停止同步新镜像。

