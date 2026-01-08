---
title: 示例
description: 从 agent 示例中获取灵感
keywords:
- ai
- agent
- cagent
weight: 40
---

从以下 agent 示例中获取灵感。
更多示例请参阅 [cagent GitHub 仓库](https://github.com/docker/cagent/tree/main/examples)。

## 开发团队

{{% cagent-example.inline "dev-team.yaml" %}}
{{- $example := .Get 0 }}
{{- $baseUrl := "https://raw.githubusercontent.com/docker/cagent/refs/heads/main/examples" }}
{{- $url := fmt.Printf "%s/%s" $baseUrl $example }}
{{- with resources.GetRemote $url }}
{{ $data := .Content | transform.Unmarshal }}

```yaml {collapse=true}
{{ .Content }}
```

{{ end }}
{{% /cagent-example.inline %}}

## Go 开发者

{{% cagent-example.inline "gopher.yaml" /%}}

## 技术博客作者

{{% cagent-example.inline "blog.yaml" /%}}