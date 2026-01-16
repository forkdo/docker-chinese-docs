---
title: ReservedStageName
url: /reference/build-checks/reserved-stage-name/
parent:
  title: Build checks
  url: /reference/build-checks/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: Build checks
    url: /reference/build-checks/
  - title: ReservedStageName
    url: /reference/build-checks/reserved-stage-name/
next:
  title: RedundantTargetPlatform
  url: /reference/build-checks/redundant-target-platform/
prev:
  title: SecretsUsedInArgOrEnv
  url: /reference/build-checks/secrets-used-in-arg-or-env/
---


## Output

```text
'scratch' is reserved and should not be used as a stage name
```

## Description

Reserved words should not be used as names for stages in multi-stage builds.
The reserved words are:

- `context`
- `scratch`

## Examples

❌ Bad: `scratch` and `context` are reserved names.

```dockerfile
FROM alpine AS scratch
FROM alpine AS context
```

✅ Good: the stage name `builder` is not reserved.

```dockerfile
FROM alpine AS builder
```


