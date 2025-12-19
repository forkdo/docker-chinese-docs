---
title: 构建代码质量检查工作流
linkTitle: 构建工作流
summary: 通过渐进式示例，学习在 E2B 沙箱中使用 GitHub 和 SonarQube MCP 服务器。
description: 创建 E2B 沙箱、发现 MCP 工具、测试单个操作，并构建完整的质量门控 PR 工作流。
weight: 10
---

在本节中，您将逐步构建一个完整的代码质量自动化工作流。您将从创建一个包含 GitHub 和 SonarQube MCP 服务器的 E2B 沙箱开始，然后逐步添加功能，直到拥有一个可投入生产的、能够分析代码质量并创建拉取请求的工作流。

通过按顺序完成每个步骤，您将学习 MCP 服务器的工作原理、如何通过 Claude 与它们交互，以及如何将操作串联起来以构建强大的自动化工作流。

## 先决条件

在开始之前，请确保您拥有：

- 具有 [API 访问权限](https://e2b.dev/docs/api-key) 的 E2B 账户
- [Anthropic API 密钥](https://docs.claude.com/en/api/admin-api/apikeys/get-api-key)

  > [!NOTE]
  >
  > 此示例使用 Claude CLI，它已预装在 E2B 沙箱中，但您可以调整示例以使用您选择的其他 AI 助手。有关替代连接方法，请参阅 [E2B 的 MCP 文档](https://e2b.dev/docs/mcp/quickstart)。

- GitHub 账户，包含：
  - 一个包含待分析代码的仓库
  - 具有 `repo` 范围的 [个人访问令牌](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- SonarCloud 账户，包含：
  - 已创建的 [组织](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/resources-structure/organization)
  - 为您的仓库 [配置的项目](https://docs.sonarsource.com/sonarqube-community-build/project-administration/creating-and-importing-projects)
  - 已生成的 [用户令牌](https://docs.sonarsource.com/sonarqube-server/instance-administration/security/administering-tokens)
- 已安装的语言运行时：
  - TypeScript: [Node.js 18+](https://nodejs.org/en/download)
  - Python: [Python 3.8+](https://www.python.org/downloads/)

> [!NOTE]
>
> 本指南使用 Claude 的 `--dangerously-skip-permissions` 标志来启用 E2B 沙箱中的自动化命令执行。此标志会绕过权限提示，这适用于像 E2B 这样的隔离容器环境，因为沙箱是临时性的，并且与您的本地机器分开。
>
> 但是，请注意 Claude 可以在沙箱内执行任何命令，包括访问该环境中的文件和凭证。仅将此方法用于受信任的代码和工作流。更多信息，请参阅 [Anthropic 关于容器安全的指南](https://docs.anthropic.com/en/docs/claude-code/devcontainer)。

## 设置您的项目

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

1. 为您的工作流创建一个新目录并初始化 Node.js：

   ```bash
   mkdir github-sonarqube-workflow
   cd github-sonarqube-workflow
   npm init -y
   ```

2. 打开 `package.json` 并将其配置为 ES 模块：

   ```json
   {
     "name": "github-sonarqube-workflow",
     "version": "1.0.0",
     "description": "使用 E2B、GitHub 和 SonarQube 的自动化代码质量工作流",
     "type": "module",
     "main": "quality-workflow.ts",
     "scripts": {
       "start": "tsx quality-workflow.ts"
     },
     "keywords": ["e2b", "github", "sonarqube", "mcp", "code-quality"],
     "author": "",
     "license": "MIT"
   }
   ```

3. 安装所需的依赖项：

   ```bash
   npm install e2b dotenv
   npm install -D typescript tsx @types/node
   ```

4. 在项目根目录创建一个 `.env` 文件：

   ```bash
   touch .env
   ```

5. 添加您的 API 密钥和配置，将占位符替换为您的实际凭证：

   ```plaintext
   E2B_API_KEY=your_e2b_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GITHUB_TOKEN=ghp_your_personal_access_token_here
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   SONARQUBE_ORG=your_sonarcloud_org_key
   SONARQUBE_TOKEN=your_sonarqube_user_token
   SONARQUBE_URL=https://sonarcloud.io
   ```

6. 通过将 `.env` 添加到 `.gitignore` 来保护您的凭证：

   ```bash
   echo ".env" >> .gitignore
   echo "node_modules/" >> .gitignore
   ```

{{< /tab >}}
{{< tab name="Python" >}}

1. 为您的工作流创建一个新目录：

   ```bash
   mkdir github-sonarqube-workflow
   cd github-sonarqube-workflow
   ```

2. 创建虚拟环境并激活它：

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # 在 Windows 上: venv\Scripts\activate
   ```

3. 安装所需的依赖项：

   ```bash
   pip install e2b python-dotenv
   ```

4. 在项目根目录创建一个 `.env` 文件：

   ```bash
   touch .env
   ```

5. 添加您的 API 密钥和配置，将占位符替换为您的实际凭证：

   ```plaintext
   E2B_API_KEY=your_e2b_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GITHUB_TOKEN=ghp_your_personal_access_token_here
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   SONARQUBE_ORG=your_sonarcloud_org_key
   SONARQUBE_TOKEN=your_sonarqube_user_token
   SONARQUBE_URL=https://sonarcloud.io
   ```

6. 通过将 `.env` 添加到 `.gitignore` 来保护您的凭证：

   ```bash
   echo ".env" >> .gitignore
   echo "venv/" >> .gitignore
   echo "__pycache__/" >> .gitignore
   ```

{{< /tab >}}
{{< /tabs >}}

## 步骤 1：创建您的第一个沙箱

让我们从创建一个沙箱开始，并验证 MCP 服务器是否已正确配置。

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

在项目根目录创建一个名为 `01-test-connection.ts` 的文件：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function testConnection() {
  console.log(
    "Creating E2B sandbox with GitHub and SonarQube MCP servers...\n",
  );

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
        url: "https://sonarcloud.io",
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  console.log(" Sandbox created successfully!");
  console.log(`MCP Gateway URL: ${mcpUrl}\n`);

  // 等待 MCP 初始化
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // 配置 Claude 使用 MCP 网关
  console.log("Connecting Claude CLI to MCP gateway...");
  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log("\nConnection successful! Cleaning up...");
  await sbx.kill();
}

testConnection().catch(console.error);
```

运行此脚本以验证您的设置：

```bash
npx tsx 01-test-connection.ts
```

{{< /tab >}}
{{< tab name="Python" >}}

在项目根目录创建一个名为 `01_test_connection.py` 的文件：

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def test_connection():
    print("Creating E2B sandbox with GitHub and SonarQube MCP servers...\n")

    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
            "sonarqube": {
                "org": os.getenv("SONARQUBE_ORG"),
                "token": os.getenv("SONARQUBE_TOKEN"),
                "url": "https://sonarcloud.io",
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    print(" Sandbox created successfully!")
    print(f"MCP Gateway URL: {mcp_url}\n")

    # 等待 MCP 初始化
    await asyncio.sleep(1)

    # 配置 Claude 使用 MCP 网关
    print("Connecting Claude CLI to MCP gateway...")
    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print("\n Connection successful! Cleaning up...")
    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(test_connection())
```

运行此脚本以验证您的设置：

```bash
python 01_test_connection.py
```

{{< /tab >}}
{{< /tabs >}}

您的输出应类似于以下示例：

```console {collapse=true}
Creating E2B sandbox with GitHub and SonarQube MCP servers...

✓ Sandbox created successfully!
MCP Gateway URL: https://50005-xxxxx.e2b.app/mcp

Connecting Claude CLI to MCP gateway...
Added HTTP MCP server e2b-mcp-gateway with URL: https://50005-xxxxx.e2b.app/mcp to local config
Headers: {
  "Authorization": "Bearer xxxxx-xxxx-xxxx"
}
File modified: /home/user/.claude.json [project: /home/user]

✓ Connection successful! Cleaning up...
```

您刚刚学习了如何创建一个配置了多个 MCP 服务器的 E2B 沙箱。`betaCreate` 方法初始化了一个包含 Claude CLI 和您指定的 MCP 服务器的云环境。

## 步骤 2：发现可用的 MCP 工具

MCP 服务器公开了 Claude 可以调用的工具。GitHub MCP 服务器提供仓库管理工具，而 SonarQube 提供代码分析工具。通过列出它们的工具，您可以知道可以执行哪些操作。

要尝试列出 MCP 工具：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

创建 `02-list-tools.ts`：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function listTools() {
  console.log("Creating sandbox...\n");

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
        url: "https://sonarcloud.io",
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  // 等待 MCP 初始化
  await new Promise((resolve) => setTimeout(resolve, 1000));

  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  console.log("\nDiscovering available MCP tools...\n");

  const prompt =
    "List all MCP tools you have access to. For each tool, show its exact name and a brief description.";

  await sbx.commands.run(
    `echo '${prompt}' | claude -p --dangerously-skip-permissions`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  await sbx.kill();
}

listTools().catch(console.error);
```

运行脚本：

```bash
npx tsx 02-list-tools.ts
```

{{< /tab >}}
{{< tab name="Python" >}}

创建 `02_list_tools.py`：

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def list_tools():
    print("Creating sandbox...\n")

    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
            "sonarqube": {
                "org": os.getenv("SONARQUBE_ORG"),
                "token": os.getenv("SONARQUBE_TOKEN"),
                "url": "https://sonarcloud.io",
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    # 等待 MCP 初始化
    await asyncio.sleep(1)

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print("\nDiscovering available MCP tools...\n")

    prompt = "List all MCP tools you have access to. For each tool, show its exact name and a brief description."

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(list_tools())
```

运行脚本：

```bash
python 02_list_tools.py
```

{{< /tab >}}
{{< /tabs >}}

在控制台中，您应该会看到一个 MCP 工具列表：

```console {collapse=true}
Creating sandbox...

Sandbox created
Connecting to MCP gateway...

Discovering available MCP tools...

I have access to the following MCP tools:

**GitHub Tools:**
1. mcp__create_repository - Create a new GitHub repository
2. mcp__list_issues - List issues in a repository
3. mcp__create_issue - Create a new issue
4. mcp__get_file_contents - Get file contents from a repository
5. mcp__create_or_update_file - Create or update files in a repository
6. mcp__create_pull_request - Create a pull request
7. mcp__create_branch - Create a new branch
8. mcp__push_files - Push multiple files in a single commit
... (30+ more GitHub tools)

**SonarQube Tools:**
1. mcp__get_projects - List projects in organization
2. mcp__get_quality_gate_status - Get quality gate status for a project
3. mcp__list_project_issues - List quality issues in a project
4. mcp__search_issues - Search for specific quality issues
... (SonarQube analysis tools)
```

## 步骤 3：测试 GitHub MCP 工具

让我们尝试使用 MCP 工具测试 GitHub。从列出仓库问题开始。

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

创建 `03-test-github.ts`：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function testGitHub() {
  console.log("Creating sandbox...\n");

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  await new Promise((resolve) => setTimeout(resolve, 1000));

  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  const repoPath = `${process.env.GITHUB_OWNER}/${process.env.GITHUB_REPO}`;

  console.log(`\nListing issues in ${repoPath}...\n`);

  const prompt = `Using the GitHub MCP tools, list all open issues in the repository "${repoPath}". Show the issue number, title, and author for each.`;

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

testGitHub().catch(console.error);
```

运行脚本：

```bash
npx tsx 03-test-github.ts
```

{{< /tab >}}
{{< tab name="Python" >}}

创建 `03_test_github.py`：

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def test_github():
    print("Creating sandbox...\n")

    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    await asyncio.sleep(1)

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    repo_path = f"{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}"

    print(f"\nListing issues in {repo_path}...\n")

    prompt = f'Using the GitHub MCP tools, list all open issues in the repository "{repo_path}". Show the issue number, title, and author for each.'

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(test_github())
```

运行脚本：

```bash
python 03_test_github.py
```

{{< /tab >}}
{{< /tabs >}}

您应该会看到 Claude 使用 GitHub MCP 工具列出您仓库的问题：

```console {collapse=true}
Creating sandbox...
Connecting to MCP gateway...

Listing issues in <your-repo>...

Here are the first 10 open issues in the <your-repo> repository:

1. **Issue #23577**: Update README (author: user1)
2. **Issue #23575**: release-notes for Compose v2.40.1 version (author: user2)
3. **Issue #23570**: engine-cli: fix `docker volume prune` output (author: user3)
4. **Issue #23568**: Engdocs update (author: user4)
5. **Issue #23565**: add new section (author: user5)
... (continues with more issues)
```

您现在可以向 Claude 发送提示，并通过自然语言与 GitHub 交互。Claude 根据您的提示决定调用什么工具。

## 步骤 4：测试 SonarQube MCP 工具

让我们使用 SonarQube MCP 工具分析代码质量。

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

创建 `04-test-sonarqube.ts`：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function testSonarQube() {
  console.log("Creating sandbox...\n");

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
        url: "https://sonarcloud.io",
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  await new Promise((resolve) => setTimeout(resolve, 1000));

  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  console.log("\nAnalyzing code quality with SonarQube...\n");

  const prompt = `Using the SonarQube MCP tools:
    1. List all projects in my organization
    2. For the first project, show:
    - Quality gate status (pass/fail)
    - Number of bugs
    - Number of code smells
    - Number of security vulnerabilities
    3. List the top 5 most critical issues found`;

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

testSonarQube().catch(console.error);
```

运行脚本：

```bash
npx tsx 04-test-sonarqube.ts
```

{{< /tab >}}
{{< tab name="Python" >}}

创建 `04_test_sonarqube.py`：

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def test_sonarqube():
    print("Creating sandbox...\n")

    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
            "sonarqube": {
                "org": os.getenv("SONARQUBE_ORG"),
                "token": os.getenv("SONARQUBE_TOKEN"),
                "url": "https://sonarcloud.io",
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    await asyncio.sleep(1)

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print("\nAnalyzing code quality with SonarQube...\n")

    prompt = """Using the SonarQube MCP tools:
    1. List all projects in my organization
    2. For the first project, show:
    - Quality gate status (pass/fail)
    - Number of bugs
    - Number of code smells
    - Number of security vulnerabilities
    3. List the top 5 most critical issues found"""

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(test_sonarqube())
```

运行脚本：

```bash
python 04_test_sonarqube.py
```

{{< /tab >}}
{{< /tabs >}}

> [!NOTE]
>
> 此脚本可能需要几分钟才能运行。

您应该会看到 Claude 输出 SonarQube 分析结果：

```console {collapse=true}
Creating sandbox...

Analyzing code quality with SonarQube...

## SonarQube Analysis Results

### 1. Projects in Your Organization

Found **1 project**:
- **Project Name**: project-1
- **Project Key**: project-testing

### 2. Project Analysis

...

### 3. Top 5 Most Critical Issues

Found 1 total issues (all are code smells with no critical/blocker severity):

1. **MAJOR Severity** - test.js:2
   - **Rule**: javascript:S1854
   - **Message**: Remove this useless assignment to variable "unusedVariable"
   - **Status**: OPEN

**Summary**: The project is in good health with no bugs or vulnerabilities detected.
```

您现在可以通过自然语言使用 SonarQube MCP 工具分析代码质量。您可以检索质量指标、识别问题，并了解哪些代码需要修复。

## 步骤 5：创建分支并进行代码更改

现在，让我们教 Claude 根据 SonarQube 发现的质量问题来修复代码。

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

创建 `05-fix-code-issue.ts`：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function fixCodeIssue() {
  console.log("Creating sandbox...\n");

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
        url: "https://sonarcloud.io",
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  await new Promise((resolve) => setTimeout(resolve, 1000));

  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  const repoPath = `${process.env.GITHUB_OWNER}/${process.env.GITHUB_REPO}`;
  const branchName = `quality-fix-${Date.now()}`;

  console.log("\nFixing a code quality issue...\n");

  const prompt = `Using GitHub and SonarQube MCP tools:

    1. Analyze code quality in repository "${repoPath}" with SonarQube
    2. Find ONE simple issue that can be confidently fixed (like an unused variable or code smell)
    3. Create a new branch called "${branchName}"
    4. Read the file containing the issue using GitHub tools
    5. Fix the issue in the code
    6. Commit the fix to the new branch with a clear commit message

    Important: Only fix issues you're 100% confident about. Explain what you're fixing and why.`;

  await sbx.commands.run(
    `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log(`\nCheck your repository for branch: ${branchName}`);

  await sbx.kill();
}

fixCodeIssue().catch(console.error);
```

运行脚本：

```bash
npx tsx 05-fix-code-issue.ts
```

{{< /tab >}}
{{< tab name="Python" >}}

创建 `05_fix_code_issue.py`：

```python
import os
import asyncio
import time
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def fix_code_issue():
    print("Creating sandbox...\n")

    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
            "sonarqube": {
                "org": os.getenv("SONARQUBE_ORG"),
                "token": os.getenv("SONARQUBE_TOKEN"),
                "url": "https://sonarcloud.io",
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    await asyncio.sleep(1)

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    repo_path = f"{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}"
    branch_name = f"quality-fix-{int(time.time() * 1000)}"

    print("\nFixing a code quality issue...\n")

    prompt = f"""Using GitHub and SonarQube MCP tools:

    1. Analyze code quality in repository "{repo_path}" with SonarQube
    2. Find ONE simple issue that can be confidently fixed (like an unused variable or code smell)
    3. Create a new branch called "{branch_name}"
    4. Read the file containing the issue using GitHub tools
    5. Fix the issue in the code
    6. Commit the fix to the new branch with a clear commit message

    Important: Only fix issues you're 100% confident about. Explain what you're fixing and why."""

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print(f"\n Check your repository for branch: {branch_name}")

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(fix_code_issue())
```

运行脚本：

```bash
python 05_fix_code_issue.py
```

{{< /tab >}}
{{< /tabs >}}

> [!NOTE]
>
> 此脚本可能需要几分钟才能运行。

Claude 将分析您的仓库并修复一个代码质量问题：

```console {collapse=true}
Creating sandbox...

Fixing a code quality issue...

## Task Completed Successfully!

I've successfully analyzed the repository and fixed a code quality issue. Here's what I did:

### 1. Analysis
Found 1 SonarQube issues in the `<your-repo>` repository:
- **Unused variable** (MINOR severity, line 2)
- Useless assignment (MAJOR severity, line 2)
- For-of loop suggestion (MINOR severity, lines 5-7)

### 2. Issue Fixed
**Location:** test.js:2
**Issue:** Unused variable declaration
**SonarQube Rule:** javascript:S1481
**What was wrong:** The line `const unusedVariable = "this is not used";` declared a variable that was never used anywhere in the function.

### 3. Why This Fix is Safe
- The variable was only declared and assigned, never referenced
- Removing it has zero impact on functionality
- It eliminates dead code and improves code quality
- This is a textbook example of a code smell that should be removed

### 4. Changes Made
- Created branch: `quality-fix-xxxxx`
- Removed the unused variable declaration
- Committed with a clear message explaining the fix and referencing the SonarQube rule

**Commit SHA:** `xxxxxxxxxxxxxxxxxxxxxxxxx`
**Branch:** https://github.com/<github-org>/<your-repo>/tree/quality-fix-xxxxx

The fix is ready for review and can be merged to improve the code quality of the repository!
```

您现在可以在同一个工作流中使用 GitHub 和 SonarQube MCP 工具来读取文件、进行代码更改并提交它们。

## 步骤 6：创建质量门控的拉取请求

最后，让我们构建完整的工作流：分析质量、修复问题，并且仅在做出改进时才创建 PR。

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

创建 `06-quality-gated-pr.ts`：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function qualityGatedPR() {
  console.log("Creating sandbox for quality-gated PR workflow...\n");

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
        url: "https://sonarcloud.io",
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  await new Promise((resolve) => setTimeout(resolve, 1000));

  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
   { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
 );

 console.log("\nStarting quality-gated PR workflow...\n");

 const prompt = `Using GitHub and SonarQube MCP tools, create a complete quality-gated PR workflow:

   1. Analyze the current code quality in repository "${process.env.GITHUB_OWNER}/${process.env.GITHUB_REPO}"
   2. Identify ONE simple, safe-to-fix issue
   3. Create a new branch called "quality-fix-automated-${Date.now()}"
   4. Fix the issue and commit the changes
   5. Create a pull request with a detailed description of the quality improvement
   6. Verify that the quality gate status has improved

   Only proceed if you can confidently fix an issue without breaking functionality.`;

 await sbx.commands.run(
   `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
   {
     timeoutMs: 0,
     onStdout: console.log,
     onStderr: console.log,
   },
 );

 console.log("\nWorkflow completed! Cleaning up...");

 await sbx.kill();
}

qualityGatedPR().catch(console.error);
{{< /tab >}}
{{< tab name="Python" >}}

Create `06_quality_gated_pr.py`:

```python
import os
import asyncio
import time
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def quality_gated_pr():
   print("Creating sandbox for quality-gated PR workflow...\n")

   sbx = await AsyncSandbox.beta_create(
       envs={
           "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
           "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
           "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
       },
       mcp={
           "githubOfficial": {
               "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
           },
           "sonarqube": {
               "org": os.getenv("SONARQUBE_ORG"),
               "token": os.getenv("SONARQUBE_TOKEN"),
               "url": "https://sonarcloud.io",
           },
       },
   )

   mcp_url = sbx.beta_get_mcp_url()
   mcp_token = await sbx.beta_get_mcp_token()

   await asyncio.sleep(1)

   await sbx.commands.run(
       f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
       timeout=0,
       on_stdout=print,
       on_stderr=print,
   )

   print("\nStarting quality-gated PR workflow...\n")

   prompt = f"""Using GitHub and SonarQube MCP tools, create a complete quality-gated PR workflow:

   1. Analyze the current code quality in repository "{os.getenv("GITHUB_OWNER")}/{os.getenv("GITHUB_REPO")}"
   2. Identify ONE simple, safe-to-fix issue
   3. Create a new branch called "quality-fix-automated-{int(time.time() * 1000)}"
   4. Fix the issue and commit the changes
   5. Create a pull request with a detailed description of the quality improvement
   6. Verify that the quality gate status has improved

   Only proceed if you can confidently fix an issue without breaking functionality."""

   await sbx.commands.run(
       f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
       timeout=0,
       on_stdout=print,
       on_stderr=print,
   )

   print("\nWorkflow completed! Cleaning up...")

   await sbx.kill()

if __name__ == "__main__":
   asyncio.run(quality_gated_pr())
```

Run the script:

```bash
python 06_quality_gated_pr.py
```

{{< /tab >}}
{{< /tabs >}}

## 总结

您已成功构建了一个完整的自动化代码质量工作流，该工作流：

- 使用 E2B 沙箱隔离运行环境
- 通过 MCP 服务器连接 GitHub 和 SonarQube
- 以自然语言与 AI 代理交互
- 自动检测和修复代码质量问题
- 创建拉取请求以合并改进

这个工作流展示了 AI 驱动的 DevOps 自动化的强大功能，将质量保证直接集成到开发流程中。

## 下一步

- 探索 [E2B 提供的其他 MCP 服务器](https://e2b.dev/docs/mcp/servers)
- 将此工作流集成到您的 CI/CD 管道中
- 添加更多质量检查步骤，如安全扫描或性能测试
- 尝试使用其他 AI 模型，如 Claude Sonnet 或 GPT-4