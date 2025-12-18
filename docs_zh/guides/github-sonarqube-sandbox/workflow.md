---
title: Build a code quality check workflow
linkTitle: Build workflow
summary: Learn to use GitHub and SonarQube MCP servers in E2B sandboxes through progressive examples.
description: Create E2B sandboxes, discover MCP tools, test individual operations, and build complete quality-gated PR workflows.
weight: 10
---

In this section, you'll build a complete code quality automation workflow
step-by-step. You'll start by creating an E2B sandbox with GitHub and
SonarQube MCP servers, then progressively add functionality until you have a
production-ready workflow that analyzes code quality and creates pull requests.

By working through each step sequentially, you'll learn how MCP servers work,
how to interact with them through Claude, and how to chain operations together
to build powerful automation workflows.

## Prerequisites

Before you begin, make sure you have:

- E2B account with [API access](https://e2b.dev/docs/api-key)
- [Anthropic API key](https://docs.claude.com/en/api/admin-api/apikeys/get-api-key)

  > [!NOTE]
  >
  > This example uses Claude CLI which comes pre-installed in E2B sandboxes, but you can adapt the example to work with other AI assistants of your choice. See [E2B's MCP documentation](https://e2b.dev/docs/mcp/quickstart) for alternative connection methods.

- GitHub account with:
  - A repository containing code to analyze
  - [Personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with `repo` scope
- SonarCloud account with:
  - [Organization](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/resources-structure/organization) created
  - [Project configured](https://docs.sonarsource.com/sonarqube-community-build/project-administration/creating-and-importing-projects) for your repository
  - [User token](https://docs.sonarsource.com/sonarqube-server/instance-administration/security/administering-tokens) generated
- Language runtime installed:
  - TypeScript: [Node.js 18+](https://nodejs.org/en/download)
  - Python: [Python 3.8+](https://www.python.org/downloads/)

> [!NOTE]
>
> This guide uses Claude's `--dangerously-skip-permissions` flag to enable
> automated command execution in E2B sandboxes. This flag bypasses permission
> prompts, which is appropriate for isolated container environments like E2B
> where sandboxes are disposable and separate from your local machine.
>
> However, be aware that Claude can execute any commands within the sandbox,
> including accessing files and credentials available in that environment. Only
> use this approach with trusted code and workflows. For more information,
> see [Anthropic's guidance on container security](https://docs.anthropic.com/en/docs/claude-code/devcontainer).

## Set up your project

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

1. Create a new directory for your workflow and initialize Node.js:

   ```bash
   mkdir github-sonarqube-workflow
   cd github-sonarqube-workflow
   npm init -y
   ```

2. Open `package.json` and configure it for ES modules:

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

3. Install required dependencies:

   ```bash
   npm install e2b dotenv
   npm install -D typescript tsx @types/node
   ```

4. Create a `.env` file in your project root:

   ```bash
   touch .env
   ```

5. Add your API keys and configuration, replacing the placeholders with your actual credentials:

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

6. Protect your credentials by adding `.env` to `.gitignore`:

   ```bash
   echo ".env" >> .gitignore
   echo "node_modules/" >> .gitignore
   ```

{{< /tab >}}
{{< tab name="Python" >}}

1. Create a new directory for your workflow:

   ```bash
   mkdir github-sonarqube-workflow
   cd github-sonarqube-workflow
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:

   ```bash
   pip install e2b python-dotenv
   ```

4. Create a `.env` file in your project root:

   ```bash
   touch .env
   ```

5. Add your API keys and configuration, replacing the placeholders with your actual credentials:

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

6. Protect your credentials by adding `.env` to `.gitignore`:

   ```bash
   echo ".env" >> .gitignore
   echo "venv/" >> .gitignore
   echo "__pycache__/" >> .gitignore
   ```

{{< /tab >}}
{{< /tabs >}}

## Step 1: Create your first sandbox

Let's start by creating a sandbox and verifying the MCP servers are configured correctly.

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

Create a file named `01-test-connection.ts` in your project root:

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

  console.log("\nConnection successful! Cleaning up...");
  await sbx.kill();
}

testConnection().catch(console.error);
```

Run this script to verify your setup:

```bash
npx tsx 01-test-connection.ts
```

{{< /tab >}}
{{< tab name="Python" >}}

Create a file named `01_test_connection.py` in your project root:

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

Run this script to verify your setup:

```bash
python 01_test_connection.py
```

{{< /tab >}}
{{< /tabs >}}

Your output should look similar to the following example:

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

You've just learned how to create an E2B sandbox with multiple MCP servers
configured. The `betaCreate` method initializes a cloud environment
with Claude CLI and your specified MCP servers.

## Step 2: Discover available MCP tools

MCP servers expose tools that Claude can call. The GitHub MCP server provides
repository management tools, while SonarQube provides code analysis tools.
By listing their tools, you know what operations are possible.

To try listing MCP tools:

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

Create `02-list-tools.ts`:

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

Run the script:

```bash
npx tsx 02-list-tools.ts
```

{{< /tab >}}
{{< tab name="Python" >}}

Create `02_list_tools.py`:

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

Run the script:

```bash
python 02_list_tools.py
```

{{< /tab >}}
{{< /tabs >}}

In the console, you should see a list of MCP tools:

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

## Step 3: Test GitHub MCP tools

Let's try testing GitHub using MCP tools. Start simple by listing
repository issues.

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

Create `03-test-github.ts`:

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
    `echo '${prompt.replace(/'/g,