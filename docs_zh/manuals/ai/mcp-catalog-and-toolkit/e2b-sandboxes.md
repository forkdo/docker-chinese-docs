---
title: E2B 沙盒
description: 专为 AI 智能体设计的基于云的安全沙盒，内置 Docker MCP Gateway 集成
keywords: E2B, 云沙盒, MCP Gateway, AI 智能体, MCP Catalog
aliases:
- /ai/mcp-catalog-and-toolkit/sandboxes/
---

Docker 已与 [E2B](https://e2b.dev/) 达成合作，后者是为 AI 智能体提供安全云沙盒的供应商。通过此次合作，每个 E2B 沙盒均可直接访问 Docker 的 [MCP Catalog](https://hub.docker.com/mcp)，该目录汇集了来自 GitHub、Notion 和 Stripe 等发布者的 200 多款工具。

创建沙盒时，您需指定其应访问的 MCP 工具。E2B 会启动这些工具，并通过 Docker MCP Gateway 提供访问权限。

## 示例：使用 GitHub 和 Notion MCP 服务器

本示例演示如何在 E2B 沙盒中连接多个 MCP 服务器。您将使用 Claude 分析 Notion 中的数据并创建 GitHub 问题。

### 前提条件

开始之前，请确保具备以下条件：

- 拥有 API 访问权限的 [E2B 账户](https://e2b.dev/docs/quickstart)
- 用于 Claude 的 Anthropic API 密钥

  > [!NOTE]
  > 本示例使用预装在 E2B 沙盒中的 Claude Code。
  > 不过，您可以调整示例以使用其他自选的 AI 助手。
  > 有关替代连接方法，请参阅 [E2B 的 MCP 文档](https://e2b.dev/docs/mcp/quickstart)。

- 本地已安装 Node.js 18+
- Notion 账户，包含：
  - 包含示例数据的数据库
  - [集成令牌](https://www.notion.com/help/add-and-manage-connections-with-the-api)
- GitHub 账户，包含：
  - 用于测试的仓库
  - 具有 `repo` 作用域的个人访问令牌

### 设置环境

创建新目录并初始化 Node.js 项目：

```console
$ mkdir mcp-e2b-quickstart
$ cd mcp-e2b-quickstart
$ npm init -y
```

通过更新 `package.json` 为项目配置 ES 模块：

```json
{
  "name": "mcp-e2b-quickstart",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node index.js"
  }
}
```

安装所需依赖项：

```console
$ npm install e2b dotenv
```

创建包含凭证的 `.env` 文件：

```console
$ cat > .env << 'EOF'
E2B_API_KEY=your_e2b_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
NOTION_INTEGRATION_TOKEN=ntn_your_notion_integration_token_here
GITHUB_TOKEN=ghp_your_github_pat_here
EOF
```

保护您的凭证：

```console
$ echo ".env" >> .gitignore
$ echo "node_modules/" >> .gitignore
```

### 创建带 MCP 服务器的 E2B 沙盒

{{< tabs group="" >}}
{{< tab name="Typescript">}}

创建名为 `index.ts` 的文件：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function quickstart(): Promise<void> {
  console.log("Creating E2B sandbox with Notion and GitHub MCP servers...\n");

  const sbx: Sandbox = await Sandbox.create({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY as string,
    },
    mcp: {
      notion: {
        internalIntegrationToken: process.env
          .NOTION_INTEGRATION_TOKEN as string,
      },
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN as string,
      },
    },
  });

  const mcpUrl = sbx.getMcpUrl();
  const mcpToken = await sbx.getMcpToken();

  console.log("Sandbox created successfully!");
  console.log(`MCP Gateway URL: ${mcpUrl}\n`);

  // Wait for MCP initialization
  await new Promise<void>((resolve) => setTimeout(resolve, 1000));

  // Connect Claude to MCP gateway
  console.log("Connecting Claude to MCP gateway...");
  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log("\nConnection successful! Cleaning up...");
  await sbx.kill();
}

quickstart().catch(console.error);
```

运行脚本：

```console
$ npx tsx index.ts
```

{{< /tab >}}
{{< tab name="Python">}}

创建名为 `index.py` 的文件：

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import Sandbox

load_dotenv()

async def quickstart():
    print("Creating E2B sandbox with Notion and GitHub MCP servers...\n")

    sbx = await Sandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        },
        mcp={
            "notion": {
                "internalIntegrationToken": os.getenv("NOTION_INTEGRATION_TOKEN"),
            },
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    print("Sandbox created successfully!")
    print(f"MCP Gateway URL: {mcp_url}\n")

    # Wait for MCP initialization
    await asyncio.sleep(1)

    # Connect Claude to MCP gateway
    print("Connecting Claude to MCP gateway...")

    def on_stdout(output):
        print(output, end='')

    def on_stderr(output):
        print(output, end='')

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout_ms=0,
        on_stdout=on_stdout,
        on_stderr=on_stderr
    )

    print("\nConnection successful! Cleaning up...")
    await sbx.kill()

if __name__ == "__main__":
    try:
        asyncio.run(quickstart())
    except Exception as e:
        print(f"Error: {e}")

```

运行脚本：

```console
$ python index.py
```

{{< /tab >}}
{{< /tabs >}}

您将看到：

```console
Creating E2B sandbox with Notion and GitHub MCP servers...

Sandbox created successfully!
MCP Gateway URL: https://50005-xxxxx.e2b.app/mcp

Connecting Claude to MCP gateway...
Added HTTP MCP server e2b-mcp-gateway with URL: https://50005-xxxxx.e2b.app/mcp

Connection successful! Cleaning up...
```

### 使用示例工作流进行测试

现在，通过运行一个简单的工作流来测试设置，该工作流将搜索 Notion 并创建 GitHub 问题。

{{< tabs group="" >}}
{{< tab name="Typescript">}}

> [!IMPORTANT]
>
> 将提示中的 `owner/repo` 替换为您的实际 GitHub 用户名和仓库名称（例如 `yourname/test-repo`）。

使用以下示例更新 `index.ts`：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function exampleWorkflow(): Promise<void> {
  console.log("Creating sandbox...\n");

  const sbx: Sandbox = await Sandbox.create({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY as string,
    },
    mcp: {
      notion: {
        internalIntegrationToken: process.env
          .NOTION_INTEGRATION_TOKEN as string,
      },
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN as string,
      },
    },
  });

  const mcpUrl = sbx.getMcpUrl();
  const mcpToken = await sbx.getMcpToken();

  console.log("Sandbox created successfully\n");

  // Wait for MCP servers to initialize
  await new Promise<void>((resolve) => setTimeout(resolve, 3000));

  console.log("Connecting Claude to MCP gateway...\n");
  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log("\nRunning example: Search Notion and create GitHub issue...\n");

  const prompt: string = `Using Notion and GitHub MCP tools:
1. Search my Notion workspace for databases
2. Create a test issue in owner/repo titled "MCP Toolkit Test" with description "Testing E2B + Docker MCP integration"
3. Confirm both operations completed successfully`;

  await sbx.commands.run(
    `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  await sbx.kill();
}

exampleWorkflow().catch(console.error);
```

运行脚本：

```console
$ npx tsx index.ts
```

{{< /tab >}}
{{< tab name="Python">}}

使用此示例更新 `index.py`：

> [!IMPORTANT]
>
> 将提示中的 `owner/repo` 替换为您的实际 GitHub 用户名和仓库名称（例如 `yourname/test-repo`）。

```python
import os
import asyncio
import shlex
from dotenv import load_dotenv
from e2b import Sandbox

load_dotenv()

async def example_workflow():
    print("Creating sandbox...\n")

    sbx = await Sandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        },
        mcp={
            "notion": {
                "internalIntegrationToken": os.getenv("NOTION_INTEGRATION_TOKEN"),
            },
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    print("Sandbox created successfully\n")

    # Wait for MCP servers to initialize
    await asyncio.sleep(3)

    print("Connecting Claude to MCP gateway...\n")

    def on_stdout(output):
        print(output, end='')

    def on_stderr(output):
        print(output, end='')

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout_ms=0,
        on_stdout=on_stdout,
        on_stderr=on_stderr
    )

    print("\nRunning example: Search Notion and create GitHub issue...\n")

    prompt = """Using Notion and GitHub MCP tools:
1. Search my Notion workspace for databases
2. Create a test issue in owner/repo titled "MCP Toolkit Test" with description "Testing E2B + Docker MCP integration"
3. Confirm both operations completed successfully"""

    # Escape single quotes for shell
    escaped_prompt = prompt.replace("'", "'\\''")

    await sbx.commands.run(
        f"echo '{escaped_prompt}' | claude -p --dangerously-skip-permissions",
        timeout_ms=0,
        on_stdout=on_stdout,
        on_stderr=on_stderr
    )

    await sbx.kill()

if __name__ == "__main__":
    try:
        asyncio.run(example_workflow())
    except Exception as e:
        print(f"Error: {e}")
```

运行脚本：

```console
$ python workflow.py
```

{{< /tab >}}
{{< /tabs >}}

您将看到：

```console
Creating sandbox...

Running example: Search Notion and create GitHub issue...

## Task Completed Successfully

I've completed both operations using the Notion and GitHub MCP tools:

### 1. Notion Workspace Search

Found 3 databases in your Notion workspace:
- **Customer Feedback** - Database with 12 entries tracking feature requests
- **Product Roadmap** - Planning database with 8 active projects
- **Meeting Notes** - Shared workspace with 45 pages

### 2. GitHub Issue Creation

Successfully created test issue:
- **Repository**: your-org/your-repo
- **Issue Number**: #47
- **Title**: "MCP Test"
- **Description**: "Testing E2B + Docker MCP integration"
- **Status**: Open
- **URL**: https://github.com/your-org/your-repo/issues/47

Both operations completed successfully. The MCP servers are properly configured and working.
```

该沙盒连接了多个 MCP 服务器，并协调了跨 Notion 和 GitHub 的工作流。您可以扩展此模式，以组合 Docker MCP Catalog 中的 200 多个 MCP 服务器中的任意一个。

## 相关页面

- [如何使用 SonarQube 和 E2B 构建 AI 驱动的代码质量工作流](/guides/github-sonarqube-sandbox.md)
- [Docker + E2B：构建可信 AI 的未来](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/)
- [Docker 沙盒](/manuals/ai/sandboxes/_index.md)
- [Docker MCP 工具包和目录](/manuals/ai/mcp-catalog-and-toolkit/_index.md)
- [Docker MCP Gateway](/manuals/ai/mcp-catalog-and-toolkit/mcp-gateway.md)
- [E2B MCP 文档](https://e2b.dev/docs/mcp)