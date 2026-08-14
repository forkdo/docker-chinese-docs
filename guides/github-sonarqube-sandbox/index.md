# 如何基于 SonarQube 和 E2B 构建 AI 驱动的代码质量工作流


本指南演示如何使用 [E2B 沙箱](https://e2b.dev/docs) 与 Docker 的 MCP 目录，构建一套 AI 驱动的代码质量工作流。你将创建一个系统，自动使用 SonarQube 分析 GitHub 仓库中的代码质量问题，并生成带有修复内容的拉取请求。

## 你将构建什么

你将构建一个 Node.js 脚本，用于启动一个 E2B 沙箱、连接 GitHub 与 SonarQube 的 MCP 服务器，并使用 Claude Code 分析代码质量、提出改进建议。这些 MCP 服务器以容器形式运行，作为 E2B 沙箱的一部分。

## 你将学到什么

通过本指南，你将学到：

- 如何创建带有多个 MCP 服务器的 E2B 沙箱
- 如何为 AI 工作流配置 GitHub 与 SonarQube 的 MCP 服务器
- 如何在沙箱内使用 Claude Code 与外部工具交互
- 如何构建能创建带质量门禁的拉取请求的自动化代码审查工作流

## 为何使用 E2B 沙箱？

与本地执行相比，在 E2B 沙箱中运行这套工作流具有多项优势：

- 安全性：AI 生成的代码运行在隔离的容器中，保护你的本地环境与凭据
- 零配置：无需在本地安装 SonarQube、GitHub CLI 或管理依赖
- 可扩展性：代码扫描等资源密集型操作在云端运行，不消耗本地资源

## 了解更多

阅读 Docker 博客文章：[Docker + E2B：构建可信 AI 的未来](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/)。

## 构建代码质量检查工作流

在本节中，你将逐步构建一个完整的代码质量自动化工作流。你将从创建一个带有 GitHub 和 SonarQube MCP 服务器的 E2B 沙箱开始，然后逐步添加功能，最终得到一个能够分析代码质量并创建拉取请求的生产就绪工作流。

通过按顺序完成每一步，你将了解 MCP 服务器的工作原理、如何通过 Claude 与之交互，以及如何将多个操作串联起来构建强大的自动化工作流。

### 前置条件

开始之前，请确保你已具备：

- 拥有 [API 访问权限](https://e2b.dev/docs/api-key) 的 E2B 账户
- [Anthropic API 密钥](https://docs.claude.com/en/api/admin-api/apikeys/get-api-key)

  > [!NOTE]
  >
  > 本示例使用了 E2B 沙箱中预装的 Claude CLI，你也可以对示例进行调整以适配你选择的其他 AI 助手。有关其他连接方式，请参阅 [E2B 的 MCP 文档](https://e2b.dev/docs/mcp/quickstart)。

- 具备以下条件的 GitHub 账户：
  - 一个包含待分析代码的仓库
  - 具备 `repo` 权限范围的 [个人访问令牌](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- 具备以下条件的 SonarCloud 账户：
  - 已创建 [组织](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/resources-structure/organization)
  - 已为你的仓库 [配置项目](https://docs.sonarsource.com/sonarqube-community-build/project-administration/creating-and-importing-projects)
  - 已生成 [用户令牌](https://docs.sonarsource.com/sonarqube-server/instance-administration/security/administering-tokens)
- 已安装语言运行时：
  - TypeScript：[Node.js 18+](https://nodejs.org/en/download)
  - Python：[Python 3.8+](https://www.python.org/downloads/)

> [!NOTE]
>
> 本指南使用了 Claude 的 `--dangerously-skip-permissions` 标志，以在 E2B 沙箱中启用自动化命令执行。该标志会跳过权限提示，对于 E2B 这类沙箱与本地机器相互隔离、一次性使用的容器环境而言是合适的。
>
> 但请注意，Claude 可以在沙箱内执行任意命令，包括访问该环境中可用的文件和凭据。请仅对可信的代码和工作流使用这种方式。更多信息请参阅 [Anthropic 关于容器安全的指南](https://docs.anthropic.com/en/docs/claude-code/devcontainer)。

### 搭建你的项目

**TypeScript**



1. 为你的工作流创建一个新目录并初始化 Node.js：

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
     "description": "Automated code quality workflow using E2B, GitHub, and SonarQube",
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

3. 安装所需的依赖：

   ```bash
   npm install e2b dotenv
   npm install -D typescript tsx @types/node
   ```

4. 在项目根目录创建一个 `.env` 文件：

   ```bash
   touch .env
   ```

5. 添加你的 API 密钥与配置，将占位符替换为你的真实凭据：

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

6. 将 `.env` 加入 `.gitignore` 以保护你的凭据：

   ```bash
   echo ".env" >> .gitignore
   echo "node_modules/" >> .gitignore
   ```

**Python**



1. 为你的工作流创建一个新目录：

   ```bash
   mkdir github-sonarqube-workflow
   cd github-sonarqube-workflow
   ```

2. 创建虚拟环境并激活它：

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # 在 Windows 上：venv\Scripts\activate
   ```

3. 安装所需的依赖：

   ```bash
   pip install e2b python-dotenv
   ```

4. 在项目根目录创建一个 `.env` 文件：

   ```bash
   touch .env
   ```

5. 添加你的 API 密钥与配置，将占位符替换为你的真实凭据：

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

6. 将 `.env` 加入 `.gitignore` 以保护你的凭据：

   ```bash
   echo ".env" >> .gitignore
   echo "venv/" >> .gitignore
   echo "__pycache__/" >> .gitignore
   ```



### 第 1 步：创建你的第一个沙箱

让我们从创建一个沙箱并验证 MCP 服务器配置是否正确开始。

**TypeScript**



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

  // Wait for MCP initialization
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Configure Claude to use the MCP gateway
  console.log("Connecting Claude CLI to MCP gateway...");
  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log("\n Connection successful! Cleaning up...");
  await sbx.kill();
}

testConnection().catch(console.error);
```

运行此脚本以验证你的配置：

```bash
npx tsx 01-test-connection.ts
```

**Python**



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

    # Wait for MCP initialization
    await asyncio.sleep(1)

    # Configure Claude to use the MCP gateway
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

运行此脚本以验证你的配置：

```bash
python 01_test_connection.py
```



你的输出应类似于以下示例：

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

你刚刚学会了如何创建一个配置了多个 MCP 服务器的 E2B 沙箱。`betaCreate` 方法会初始化一个包含 Claude CLI 及你所指定 MCP 服务器的云端环境。

### 第 2 步：发现可用的 MCP 工具

MCP 服务器会暴露可供 Claude 调用的工具。GitHub MCP 服务器提供仓库管理工具，而 SonarQube 提供代码分析工具。通过列出这些工具，你就知道可执行哪些操作了。

尝试列出 MCP 工具：

**TypeScript**



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

  // Wait for MCP initialization
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

**Python**



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

    # Wait for MCP initialization
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



在控制台中，你应该会看到 MCP 工具的列表：

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

### 第 3 步：测试 GitHub 的 MCP 工具

让我们尝试使用 MCP 工具测试 GitHub。从简单地列出仓库的 issue 开始。

**TypeScript**



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

**Python**



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



你应该会看到 Claude 使用 GitHub 的 MCP 工具列出你仓库的 issue：

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

你现在可以向 Claude 发送提示词，通过自然语言的方式与 GitHub 交互。Claude 会根据你的提示词决定调用哪个工具。

### 第 4 步：测试 SonarQube 的 MCP 工具

让我们使用 SonarQube 的 MCP 工具来分析代码质量。

**TypeScript**



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

**Python**



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
                "url": "https://sonarcloud.io",
                "token": os.getenv("SONARQUBE_TOKEN"),
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



> [!NOTE]
>
> 此脚本可能需要几分钟才能运行完成。

你应该会看到 Claude 输出 SonarQube 的分析结果：

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

你现在可以使用 SonarQube 的 MCP 工具，通过自然语言分析代码质量。你可以获取质量指标、识别问题，并了解哪些代码需要修复。

### 第 5 步：创建分支并修改代码

现在，让我们教 Claude 根据 SonarQube 发现的质量问题来修复代码。

**TypeScript**



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

  console.log(`\nCheck your repository for branch: ${branchName}`);

  await sbx.kill();
}

fixCodeIssue().catch(console.error);
```

运行脚本：

```bash
npx tsx 05-fix-code-issue.ts
```

**Python**



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



> [!NOTE]
>
> 此脚本可能需要几分钟才能运行完成。

Claude 会分析你的仓库并修复一个代码质量问题：

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

你现在可以在同一工作流中使用 GitHub 与 SonarQube 的 MCP 工具来读取文件、修改代码并提交它们。

### 第 6 步：创建带质量门禁的拉取请求

最后，让我们构建完整的工作流：分析质量、修复问题，并且仅在确有改进时才创建 PR。

**TypeScript**



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

  const repoPath = `${process.env.GITHUB_OWNER}/${process.env.GITHUB_REPO}`;
  const branchName = `quality-improvements-${Date.now()}`;

  console.log("\nRunning quality-gated PR workflow...\n");

  const prompt = `You are a code quality engineer. Using GitHub and SonarQube MCP tools:

    STEP 1: ANALYSIS
    - Get current code quality status from SonarQube for "${repoPath}"
    - Record the current number of bugs, code smells, and vulnerabilities
    - Identify 1-3 issues that you can confidently fix

    STEP 2: FIX ISSUES
    - Create branch "${branchName}"
    - For each issue you're fixing:
        * Read the file with the issue
        * Make the fix
        * Commit with a descriptive message
    - Only fix issues where you're 100% confident the fix is correct

    STEP 3: VERIFICATION
        - After your fixes, check if quality metrics would improve
        - Calculate: Would this reduce bugs/smells/vulnerabilities?

    STEP 4: QUALITY GATE
        - Only proceed if your changes improve quality
        - If quality would not improve, explain why and stop

    STEP 5: CREATE PR (only if quality gate passes)
        - Create a pull request from "${branchName}" to main
        - Title: "Quality improvements: [describe what you fixed]"
        - Description should include:
            * What issues you fixed
            * Before/after quality metrics
            * Why these fixes improve code quality
        - Add a comment with detailed SonarQube analysis

    Be thorough and explain your decisions at each step.`;

  await sbx.commands.run(
    `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log(`\n Workflow complete! Check ${repoPath} for new pull request.`);

  await sbx.kill();
}

qualityGatedPR().catch(console.error);
```

运行脚本：

```bash
npx tsx 06-quality-gated-pr.ts
```

**Python**



创建 `06_quality_gated_pr.py`：

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

    repo_path = f"{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}"
    branch_name = f"quality-improvements-{int(time.time() * 1000)}"

    print("\nRunning quality-gated PR workflow...\n")

    prompt = f"""You are a code quality engineer. Using GitHub and SonarQube MCP tools:

    STEP 1: ANALYSIS
    - Get current code quality status from SonarQube for "{repo_path}"
    - Record the current number of bugs, code smells, and vulnerabilities
    - Identify 1-3 issues that you can confidently fix

    STEP 2: FIX ISSUES
    - Create branch "{branch_name}"
    - For each issue you are fixing:
        Read the file with the issue
        Make the fix
        Commit with a descriptive message
    - Only fix issues where you are 100 percent confident the fix is correct

    STEP 3: VERIFICATION
        - After your fixes, check if quality metrics would improve
        - Calculate: Would this reduce bugs/smells/vulnerabilities?

    STEP 4: QUALITY GATE
        - Only proceed if your changes improve quality
        - If quality would not improve, explain why and stop

    STEP 5: CREATE PR (only if quality gate passes)
        - Create a pull request from "{branch_name}" to main
        - Title: "Quality improvements: [describe what you fixed]"
        - Description should include:
            What issues you fixed
            Before/after quality metrics
            Why these fixes improve code quality
        - Add a comment with detailed SonarQube analysis

    Be thorough and explain your decisions at each step."""

    await sbx.commands.run(
        f"echo '{prompt.replace(chr(39), chr(39) + chr(92) + chr(39) + chr(39))}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print(f"\n Workflow complete! Check {repo_path} for new pull request.")

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(quality_gated_pr())
```

运行脚本：

```bash
python 06_quality_gated_pr.py
```



> [!NOTE]
>
> 此脚本可能需要几分钟才能运行完成。

Claude 将运行整个工作流，创建质量改进并在 GitHub 中打开一个 PR：

```console {collapse=true}
Creating sandbox for quality-gated PR workflow...

Running quality-gated PR workflow...

## Complete - Code Quality Improvement Successfully Executed

### Summary of Work Completed

**Pull Request Created:** https://github.com/<github-org>/<your-repo>/pull/1

---

### STEP 1: ANALYSIS

**Current State:**
- **Bugs:** 0
- **Vulnerabilities:** 0
- **Code Smells:** 1
- **Lines of Code:** 12
- **All Ratings:** A (Reliability, Security, Maintainability)

**Issues Identified (all in test.js):**
1. xxxxxxxxx - Unused variable declaration (MINOR)

---

### STEP 2: FIX ISSUES

**Branch Created:** `quality-improvements-xxxxxxxx`

**Changes Made:**
1. **Removed unused variable** (line 2) - Eliminated dead code that served no purpose
2. **Modernized loop pattern** (lines 5-7) - Converted `for (let i = 0; i < items.length; i++)` to `for (const item of items)`

**Commit:** xxxxxxxxxx

---

### STEP 3: VERIFICATION

**Expected Impact:**
- Code Smells: 1 → 0 (100% reduction)
- Bugs: 0 → 0 (maintained)
- Vulnerabilities: 0 → 0 (maintained)
- All quality ratings maintained at A

---

### STEP 4: QUALITY GATE PASSED

**Decision Criteria Met:**
- ✅ Reduces code smells by 100%
- ✅ No new bugs or vulnerabilities introduced
- ✅ Code is more readable and maintainable
- ✅ Follows modern JavaScript best practices
- ✅ All fixes are low-risk refactorings with no behavioral changes

---

### STEP 5: CREATE PR

**Pull Request Details:**
- **Number:** #1
- **Title:** Quality improvements: Remove unused variable and modernize for loop
- **Branch:** quality-improvements-xxxxxxxx → main
- **URL:** https://github.com/<github-org)/<your-repo>/pull/1

**PR Includes:**
- Comprehensive description with before/after metrics
- Detailed SonarQube analysis comment with issue breakdown
- Code comparison showing improvements
- Quality metrics table

The pull request is now ready for review and merge!
```

你现在已构建了一个完整、包含条件逻辑的多步骤工作流。Claude 会用 SonarQube 分析质量、使用 GitHub 工具进行修复、验证改进，并且仅在质量确有提升时才创建 PR。

### 第 7 步：添加错误处理

生产级工作流需要错误处理。让我们让工作流更加健壮。

**TypeScript**



创建 `07-robust-workflow.ts`：

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function robustWorkflow() {
  let sbx: Sandbox | undefined;

  try {
    console.log("Creating sandbox...\n");

    sbx = await Sandbox.betaCreate({
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

    console.log("\nRunning workflow with error handling...\n");

    const prompt = `Run a quality improvement workflow for "${repoPath}".

    ERROR HANDLING RULES:
    1. If SonarQube is unreachable, explain the error and stop gracefully
    2. If GitHub API fails, retry once, then explain and stop
    3. If no fixable issues are found, explain why and exit (this is not an error)
    4. If file modifications fail, explain which file and why
    5. At each step, check for errors before proceeding

    Run the workflow and handle any errors you encounter professionally.`;

    await sbx.commands.run(
      `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
      {
        timeoutMs: 0,
        onStdout: console.log,
        onStderr: console.log,
      },
    );

    console.log("\n Workflow completed");
  } catch (error) {
    const err = error as Error;
    console.error("\n Workflow failed:", err.message);

    if (err.message.includes("403")) {
      console.error("\n Check your E2B account has MCP gateway access");
    } else if (err.message.includes("401")) {
      console.error("\n Check your API tokens are valid");
    } else if (err.message.includes("Credit balance")) {
      console.error("\n Check your Anthropic API credit balance");
    }

    process.exit(1);
  } finally {
    if (sbx) {
      console.log("\n Cleaning up sandbox...");
      await sbx.kill();
    }
  }
}

robustWorkflow().catch(console.error);
```

运行脚本：

```bash
npx tsx 07-robust-workflow.ts
```

**Python**



创建 `07_robust_workflow.py`：

```python
import os
import asyncio
import sys
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def robust_workflow():
    sbx = None

    try:
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
            timeout=0,  # Fixed: was timeout_ms
            on_stdout=print,
            on_stderr=print,
        )

        repo_path = f"{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}"

        print("\nRunning workflow with error handling...\n")

        prompt = f"""Run a quality improvement workflow for "{repo_path}".

        ERROR HANDLING RULES:
        1. If SonarQube is unreachable, explain the error and stop gracefully
        2. If GitHub API fails, retry once, then explain and stop
        3. If no fixable issues are found, explain why and exit (this is not an error)
        4. If file modifications fail, explain which file and why
        5. At each step, check for errors before proceeding

        Run the workflow and handle any errors you encounter professionally."""

        await sbx.commands.run(
            f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
            timeout=0,
            on_stdout=print,
            on_stderr=print,
        )

        print("\n Workflow completed")

    except Exception as error:
        print(f"\n Workflow failed: {str(error)}")

        error_msg = str(error)
        if "403" in error_msg:
            print("\n Check your E2B account has MCP gateway access")
        elif "401" in error_msg:
            print("\n Check your API tokens are valid")
        elif "Credit balance" in error_msg:
            print("\n Check your Anthropic API credit balance")

        sys.exit(1)

    finally:
        if sbx:
            print("\n Cleaning up sandbox...")
            await sbx.kill()

if __name__ == "__main__":
    asyncio.run(robust_workflow())
```

运行脚本：

```bash
python 07_robust_workflow.py
```



Claude 将运行整个工作流，如果遇到错误，会以健壮的报错信息作出响应。

### 后续步骤

在下一节中，你将根据自己的需求对工作流进行定制。

## 定制代码质量检查工作流

既然你已经了解了在 E2B 沙箱中使用 GitHub 和 SonarQube 自动化代码质量工作流的基础知识，就可以根据自己的需求来定制工作流了。

### 聚焦于特定的质量问题

修改提示词以优先处理某些问题类型：

**TypeScript**



```typescript
const prompt = `Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "${repoPath}" and fix the highest priority issues first.`;
```

**Python**



```python
prompt = f"""Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "{repo_path}" and fix the highest priority issues first."""
```



### 与 CI/CD 集成

将此工作流添加到 GitHub Actions 中，使其在拉取请求上自动运行：

**TypeScript**



```yaml
name: Automated quality checks
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v5
        with:
          node-version: "24"
      - run: npm install
      - run: npx tsx 06-quality-gated-pr.ts
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```

**Python**



```yaml
name: Automated quality checks
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.14"
      - run: pip install e2b python-dotenv
      - run: python 06_quality_gated_pr.py
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```



### 按文件模式过滤

针对代码库中特定的部分：

**TypeScript**



```typescript
const prompt = `Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only.`;
```

**Python**



```python
prompt = """Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only."""
```



### 设置质量阈值

定义何时应当创建 PR：

**TypeScript**



```typescript
const prompt = `Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation.`;
```

**Python**



```python
prompt = """Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation."""
```



### 后续步骤

了解如何排查常见问题。

## 排查代码质量工作流

本页介绍在构建基于 E2B 沙箱与 MCP 服务器的代码质量工作流时可能遇到的常见问题及其解决方案。

如果你遇到的问题未在此处涵盖，请查看 [E2B 文档](https://e2b.dev/docs)。

### MCP 工具不可用

问题：Claude 报告 `I don't have any MCP tools available`。

解决方案：

1. 确认你使用了授权请求头：

    ```plaintext
    --header "Authorization: Bearer ${mcpToken}"
    ```

2. 确认你在等待 MCP 初始化完成。

    ```typescript
    // typescript
    await new Promise((resolve) => setTimeout(resolve, 1000));
    ```

    ```python
    # python
    await asyncio.sleep(1)
    ```

3. 确保凭据同时出现在 `envs` 和 `mcp` 配置中：

    ```typescript
    // typescript
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
    ```

    ```python
    # python
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
    ```

4. 验证你的 API 令牌有效且具备正确的权限范围。

### GitHub 工具可用但 SonarQube 不可用

问题：GitHub 的 MCP 工具加载了，但 SonarQube 的工具没有出现。

解决方案：SonarQube 的 MCP 服务器需要同时配置 GitHub。即使你只测试其中一个，也始终在你的沙箱配置中同时包含这两个服务器。

**TypeScript**



```typescript
// Include both servers even if only using one
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
```

**Python**



```python
# Include both servers even if only using one
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
```



### Claude 无法访问私有仓库

问题："I don't have access to that repository"。

解决方案：

1. 确认你的 GitHub 令牌具备 `repo` 权限范围（而不仅仅是 `public_repo`）。
2. 先用一个公开仓库进行测试。
3. 确保你的 `.env` 中仓库所有者与名称填写正确：

   **TypeScript**



   ```plaintext
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   ```

   **Python**



   ```plaintext
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   ```

   

### 工作流超时或运行时间过长

问题：工作流未能完成，或 Claude 的额度耗尽。

解决方案：

1. 对复杂工作流使用 `timeoutMs: 0`（TypeScript）或 `timeout_ms=0`（Python），以允许无限制时间：

   **TypeScript**



   ```typescript
   await sbx.commands.run(
     `echo '${prompt}' | claude -p --dangerously-skip-permissions`,
     {
       timeoutMs: 0, // No timeout
       onStdout: console.log,
       onStderr: console.log,
     },
   );
   ```

   **Python**



   ```python
   await sbx.commands.run(
       f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
       timeout_ms=0,  # No timeout
       on_stdout=print,
       on_stderr=print,
   )
   ```

   

2. 将复杂工作流拆分为更小、更聚焦的任务。
3. 监控你的 Anthropic API 额度使用情况。
4. 在提示词中加入检查点："After each step, show progress before continuing"（每一步完成后，先展示进度再继续）。

### 沙箱清理错误

问题：沙箱未能被正确清理，导致资源耗尽。

解决方案：始终使用 `finally` 代码块中的错误处理来清理资源：

**TypeScript**



```typescript
async function robustWorkflow() {
  let sbx: Sandbox | undefined;

  try {
    sbx = await Sandbox.betaCreate({
      // ... configuration
    });

    // ... workflow logic
  } catch (error) {
    console.error("Workflow failed:", error);
    process.exit(1);
  } finally {
    if (sbx) {
      console.log("Cleaning up sandbox...");
      await sbx.kill();
    }
  }
}
```

**Python**



```python
async def robust_workflow():
    sbx = None

    try:
        sbx = await AsyncSandbox.beta_create(
            # ... configuration
        )

        # ... workflow logic

    except Exception as error:
        print(f"Workflow failed: {error}")
        sys.exit(1)
    finally:
        if sbx:
            print("Cleaning up sandbox...")
            await sbx.kill()
```



### 环境变量未加载

问题：脚本因环境变量为 "undefined" 或 "None" 而失败。

解决方案：

**TypeScript**



1. 确保 `dotenv` 已加载到文件顶部：

   ```typescript
   import "dotenv/config";
   ```

2. 确认 `.env` 文件与你的脚本位于同一目录。

3. 检查变量名是否完全一致（区分大小写）：

   ```typescript
   // .env file
   GITHUB_TOKEN = ghp_xxxxx;

   // In code
   process.env.GITHUB_TOKEN; // Correct
   process.env.github_token; // Wrong - case doesn't match
   ```

   **Python**


   1. 确保 `dotenv` 已加载到文件顶部：

      ```python
      from dotenv import load_dotenv
      load_dotenv()
      ```

   2. 确认 `.env` 文件与你的脚本位于同一目录。

   3. 检查变量名是否完全一致（区分大小写）：

      ```python
      # .env file
      GITHUB_TOKEN=ghp_xxxxx

      # In code
      os.getenv("GITHUB_TOKEN")  # Correct
      os.getenv("github_token")  # Wrong - case doesn't match
      ```

   

### SonarQube 返回空结果

问题：SonarQube 分析没有返回任何项目或问题。

解决方案：

1. 确认你的 SonarCloud 组织密钥正确。
2. 确保你在 SonarCloud 中至少配置了一个项目。
3. 检查你的 SonarQube 令牌具备必要的权限。
4. 确认你的项目已在 SonarCloud 中至少分析过一次。

