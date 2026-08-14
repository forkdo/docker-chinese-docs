# 治理


沙箱治理涵盖了控制沙箱可通过网络、文件系统以及 MCP 访问哪些内容的策略系统。关于 MCP 的设置与服务器注册，请参阅 [MCP 网关](../mcp-gateway.md)。治理在两个层面上运作：

**本地策略**通过 `sbx policy` CLI 按机器进行配置。它让开发者个人可以自定义其沙箱能够访问哪些域名。请参阅[本地策略](access-controls/local.md)。

**组织策略**在 Docker Home 中集中配置。网络与文件系统策略也可以通过 [Governance API](/reference/api/ai-governance/) 管理。在组织级别定义的控制项会统一应用于组织中的每一个沙箱。组织治理还可以包含针对沙箱 MCP 活动的 MCP 策略。当组织治理生效时，只有组织的允许规则才授予访问权限：本地 `sbx policy` 的允许规则将不再被评估，而本地的拒绝规则仍会在其之上继续生效。请参阅[组织策略](access-controls/organization.md)。

除了这套访问控制策略之外，管理员还可以要求开发者必须以其组织成员身份登录后才能使用沙箱。[登录强制执行](monitor-and-enforce/sign-in-enforcement.md)通过端点管理进行部署，确保开发者无法通过使用个人账户来绕过组织策略。

> [!NOTE]
> 组织治理需要单独的付费订阅。
> [联系 Docker 销售团队](https://www.docker.com/products/ai-governance/#contact-sales)
> 申请访问权限。

## 了解更多

先从[策略概念](concepts.md)开始，了解资源模型、规则语法、MCP 策略基础、评估过程与优先级。

### 访问控制

- [本地策略](access-controls/local.md)：使用 `sbx policy` CLI 在你的机器上配置网络规则。
- [组织策略](access-controls/organization.md)：在整个组织范围内集中管理沙箱策略。
- [网络访问策略](access-controls/network.md)：控制沙箱的出向网络访问。
- [文件系统访问策略](access-controls/filesystem.md)：控制沙箱可以将哪些主机路径挂载为工作区。
- [MCP 访问策略](access-controls/mcp.md)：控制 MCP 服务器注册、工具调用、资源、提示以及审批关卡。

### 监控与强制执行

- [监控策略](monitor-and-enforce/monitoring.md)：使用 `sbx policy ls` 和 `sbx policy log` 检查生效的规则并监控沙箱网络流量。
- [审计日志](audit/)：查看、配置、导出与收集治理审计记录。
- [登录强制执行](monitor-and-enforce/sign-in-enforcement.md)：要求开发者以组织成员身份登录，并通过端点管理强制执行。

### 参考

- [AI Governance API](/reference/api/ai-governance/)：以编程方式管理网络与文件系统的组织策略。
- [MCP 策略参考](reference/mcp-policy.md)：查阅 Docker MCP 策略的动作、资源、属性、上下文字段与审批行为。

