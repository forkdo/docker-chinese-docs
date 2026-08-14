# 监控策略


`sbx policy ls` 和 `sbx policy log` 让你可以合并查看所有生效的策略规则和沙箱网络活动，无论这些规则来自本地配置还是组织治理。它们既可用于验证你编写的规则，也可用于调试某个请求为何被阻止或允许。

## Listing rules（列出规则）

使用 `sbx policy ls` 查看所有生效的策略及其当前状态：

```console
$ sbx policy ls
POLICY                                 SOURCE   APPLIES TO          SUMMARY
local-policy                           local    all                 network: 42 allow, 1 deny; filesystem read: 1 allow; filesystem write: 1 allow
1b2633ea-e604-48bb-a5e6-3ac86ba383fe   kit      sandbox:my-sandbox  network: 3 allow
```

各列含义：

- `POLICY`：策略名称。
- `SOURCE`：策略的来源。`local` 表示你的本地配置——预设或你用 `sbx policy` 添加的规则。`kit` 表示一个 [kit](../../customize/kits.md#control-network-access)。`org` 表示你的组织。
- `APPLIES TO`：策略适用于哪些沙箱。`all` 表示该策略是全局的。`sandbox:<name>` 将其限定到单个沙箱；配置档（profile）名称将其限定到使用该配置档的沙箱。
- `SUMMARY`：按类型和决策统计的规则计数——例如 `network: 5 allow, 1 deny`。

要查看包含规则 ID 和资源的完整规则级细节，传入 `--wide`。要检查单个策略或规则，使用 `sbx policy inspect`：

```console
$ sbx policy inspect Balanced
```

使用 `--source` 按来源筛选（`local`、`org` 或 `kit`），使用 `--decision` 按结果筛选（`allow` 或 `deny`）。

当你传入 `--include-inactive` 时还会出现一个 `STATUS` 列；参见 [Showing inactive rules](#showing-inactive-rules)。

当组织治理生效时，输出开头会有一行摘要，显示由哪个组织管理该策略、同步状态，以及隐藏了多少非激活规则：

```console
$ sbx policy ls
Governance: Managed by my-org | Sync: OK, last synced 08:21:01 | Hidden: 9 inactive rules. Show with: sbx policy ls --include-inactive

POLICY               SOURCE   APPLIES TO   SUMMARY
default filesystem   org      all          filesystem read: 2 allow; filesystem write: 7 allow, 2 deny
default network      org      all          network: 38 allow, 4 deny
```

`Governance` 显示由哪个组织管理该策略，`Sync` 确认守护进程已拉取最新规则。如果同步状态显示错误或时间戳陈旧，守护进程可能没有最新的组织策略。运行 `sbx policy reset` 强制重新拉取。`Hidden` 报告有多少非激活规则被隐藏，以及如何显示它们。

### Showing inactive rules（显示非激活规则）

当组织治理生效时，本地及 kit 定义的 allow 规则不会被评估，因此 `sbx policy ls` 默认隐藏它们。要同时列出它们——例如，确认组织策略覆盖了哪些 allow 规则——传入 `--include-inactive`。这会添加一个 `STATUS` 列：

```console
$ sbx policy ls --include-inactive
Governance: Managed by my-org | Sync: OK, last synced 08:41:06

POLICY                       SOURCE   APPLIES TO   SUMMARY                                                    STATUS
default filesystem           org      all          filesystem read: 2 allow; filesystem write: 7 allow, 2 deny   active
default network              org      all          network: 38 allow, 4 deny                                   active
default-fs-read-allow-all    local    all          filesystem read: 1 allow                                    inactive
default-fs-write-allow-all   local    all          filesystem write: 1 allow                                   inactive
```

非激活策略在 `STATUS` 列中显示 `inactive`。在组织治理生效期间它们没有任何效果。本地及 kit 定义的 deny 规则保持激活且不会被隐藏，因为 deny 仍会叠加在组织策略之上生效。参见 [Precedence](../concepts.md#precedence)。

使用 `--type network` 或 `--type filesystem` 只显示该类型的策略。若不带沙箱参数，`sbx policy ls` 会显示所有沙箱中的每个策略。传入沙箱名称可筛选出全局策略以及限定到该沙箱的策略：

```console
$ sbx policy ls my-sandbox
```

### Filesystem rules（文件系统规则）

`sbx policy ls` 会将文件系统策略与网络策略一并列出。文件系统规则控制沙箱可将哪些主机路径挂载为工作区。传入 `--type filesystem` 只显示它们：

```console
$ sbx policy ls --type filesystem
POLICY         SOURCE   APPLIES TO   SUMMARY
local-policy   local    all          filesystem read: 1 allow; filesystem write: 1 allow
```

可写的工作区挂载必须同时被 `filesystem:read` 和 `filesystem:write` 规则允许；只读挂载仅需 `filesystem:read`。默认本地策略允许对所有路径进行读写访问，即上面所示的两条 `default-fs-*` 规则。有关规则语法和路径模式，参见 [Policy concepts](../concepts.md#filesystem-rules)。

## Monitoring traffic（监控流量）

使用 `sbx policy log` 查看你的沙箱联系了哪些主机以及匹配了哪些规则：

```console
$ sbx policy log
Blocked requests:
SANDBOX      TYPE     HOST                   PROXY        RULE            REASON         LAST SEEN        COUNT
my-sandbox   network  blocked.example.com    transparent  domain-blocked  default-deny   10:15:25 29-Jan  1

Allowed requests:
SANDBOX      TYPE     HOST                   PROXY          RULE             REASON   LAST SEEN        COUNT
my-sandbox   network  api.anthropic.com      forward        domain-allowed            10:15:23 29-Jan  42
my-sandbox   network  registry.npmjs.org     forward-bypass domain-allowed            10:15:20 29-Jan  18
my-sandbox   network  app.example.com        browser-open                             10:15:10 29-Jan  1
```

`PROXY` 列显示请求是如何离开沙箱的：

| 值               | 说明                                                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------------------- |
| `forward`        | 通过前向代理路由。支持 [凭据注入](../../security/credentials.md)。                                              |
| `forward-bypass` | 通过前向代理路由，但不进行凭据注入。                                                                           |
| `transparent`    | 被透明代理拦截。策略会被强制执行，但无法进行凭据注入。                                                         |
| `network`        | 非 HTTP 流量（原始 TCP、UDP、ICMP）。TCP 可以通过策略规则允许。UDP 和 ICMP 始终被阻止。                        |
| `browser-open`   | 沙箱进程请求在主机浏览器中打开某个 URL。在打开 URL 之前会强制执行策略。                                        |

`RULE` 列标识匹配该请求的策略规则。当守护进程记录了额外上下文时，`REASON` 列会包含这些内容。

通过将沙箱名称作为参数传入可按沙箱名筛选：

```console
$ sbx policy log my-sandbox
```

使用 `--limit N` 只显示最后 `N` 条记录，`--json` 输出机器可读格式，或 `--type network` 按策略类型筛选。`sbx policy log` 仅记录网络流量；文件系统挂载决策尚不可在日志中查看。

