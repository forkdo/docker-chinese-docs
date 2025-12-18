---
title: 排查代码质量工作流问题
linkTitle: 排查
summary: 解决 E2B 沙箱、MCP 服务器连接以及 GitHub/SonarQube 集成的常见问题。
description: 提供在使用 E2B 构建代码质量工作流时，针对 MCP 工具无法加载、身份验证错误、权限问题、工作流超时等常见问题的解决方案。
weight: 30
---

本页面涵盖在使用 E2B 沙箱和 MCP 服务器构建代码质量工作流时可能遇到的常见问题及其解决方案。

如果您遇到的问题未在本文档中涵盖，请查阅 [E2B 文档](https://e2b.dev/docs)。

## MCP 工具不可用

问题：Claude 报告 `I don't have any MCP tools available`（我没有可用的 MCP 工具）。

解决方案：

1.  确认您使用了授权头：

    ```plaintext
    --header "Authorization: Bearer ${mcpToken}"
    ```

2.  检查您是否等待了 MCP 初始化完成。

    ```typescript
    // typescript
    await new Promise((resolve) => setTimeout(resolve, 1000));
    ```

    ```python
    # python
    await asyncio.sleep(1)
    ```

3.  确保凭据同时存在于 `envs` 和 `mcp` 配置中：

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

4.  验证您的 API 令牌有效且具有正确的权限范围。

## GitHub 工具正常但 SonarQube 不行

问题：GitHub MCP 工具加载成功，但 SonarQube 工具未出现。

解决方案：SonarQube MCP 服务器需要与 GitHub 同时配置。请始终在沙箱配置中同时包含两个服务器，即使您只使用其中一个。

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```typescript
// 即使只使用其中一个，也要包含两个服务器
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

{{< /tab >}}
{{< tab name="Python" >}}

```python
# 即使只使用其中一个，也要包含两个服务器
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

{{< /tab >}}
{{< /tabs >}}

## Claude 无法访问私有仓库

问题：报告 "I don't have access to that repository"（我无法访问该仓库）。

解决方案：

1. 确认您的 GitHub 令牌具有 `repo` 权限范围（不仅仅是 `public_repo`）。
2. 先使用公共仓库测试。
3. 确保 `.env` 文件中的仓库所有者和名称正确：

   {{< tabs group="language" >}}
   {{< tab name="TypeScript" >}}

   ```plaintext
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   ```

   {{< /tab >}}
   {{< tab name="Python" >}}

   ```plaintext
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   ```

   {{< /tab >}}
   {{< /tabs >}}

## 工作流超时或运行时间过长

问题：工作流无法完成或 Claude 信用额度耗尽。

解决方案：

1. 对于复杂工作流，使用 `timeoutMs: 0`（TypeScript）或 `timeout_ms=0`（Python）以允许无限制时间：

   {{< tabs group="language" >}}
   {{< tab name="TypeScript" >}}

   ```typescript
   await sbx.commands.run(
     `echo '${prompt}' | claude -p --dangerously-skip-permissions`,
     {
       timeoutMs: 0, // 无超时
       onStdout: console.log,
       onStderr: console.log,
     },
   );
   ```

   {{< /tab >}}
   {{< tab name="Python" >}}

   ```python
   await sbx.commands.run(
       f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
       timeout_ms=0,  # 无超时
       on_stdout=print,
       on_stderr=print,
   )
   ```

   {{< /tab >}}
   {{< /tabs >}}

2. 将复杂工作流拆分为更小、更专注的任务。
3. 监控您的 Anthropic API 信用额度使用情况。
4. 在提示中添加检查点："每完成一步，在继续之前显示进度"。

## 沙箱清理错误

问题：沙箱未正确清理，导致资源耗尽。

解决方案：始终使用适当的错误处理，在 `finally` 块中执行清理：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

```typescript
async function robustWorkflow() {
  let sbx: Sandbox | undefined;

  try {
    sbx = await Sandbox.betaCreate({
      // ... 配置
    });

    // ... 工作流逻辑
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

{{< /tab >}}
{{< tab name="Python" >}}

```python
async def robust_workflow():
    sbx = None

    try:
        sbx = await AsyncSandbox.beta_create(
            # ... 配置
        )

        # ... 工作流逻辑

    except Exception as error:
        print(f"Workflow failed: {error}")
        sys.exit(1)
    finally:
        if sbx:
            print("Cleaning up sandbox...")
            await sbx.kill()
```

{{< /tab >}}
{{< /tabs >}}

## 环境变量未加载

问题：脚本因环境变量 "undefined" 或 "None" 而失败。

解决方案：

{{< tabs group="language" >}}
{{< tab name="TypeScript" >}}

1. 确保在文件顶部加载了 `dotenv`：

   ```typescript
   import "dotenv/config";
   ```

2. 确认 `.env` 文件位于您的脚本同一目录中。

3. 检查变量名完全匹配（区分大小写）：

   ```typescript
   // .env 文件
   GITHUB_TOKEN = ghp_xxxxx;

   // 在代码中
   process.env.GITHUB_TOKEN; // 正确
   process.env.github_token; // 错误 - 大小写不匹配
   ```

   {{< /tab >}}
   {{< tab name="Python" >}}

   1. 确保在文件顶部加载了 `dotenv`：

      ```python
      from dotenv import load_dotenv
      load_dotenv()
      ```

   2. 确认 `.env` 文件位于您的脚本同一目录中。

   3. 检查变量名完全匹配（区分大小写）：

      ```python
      # .env 文件
      GITHUB_TOKEN=ghp_xxxxx

      # 在代码中
      os.getenv("GITHUB_TOKEN")  # 正确
      os.getenv("github_token")  # 错误 - 大小写不匹配
      ```

   {{< /tab >}}
   {{< /tabs >}}

## SonarQube 返回空结果

问题：SonarQube 分析未返回任何项目或问题。

解决方案：

1. 确认您的 SonarCloud 组织密钥正确。
2. 确保您在 SonarCloud 中至少配置了一个项目。
3. 检查您的 SonarQube 令牌具有必要的权限。
4. 确认您的项目已在 SonarCloud 中至少分析过一次。