---
title: StageNameCasing
url: /reference/build-checks/stage-name-casing/
parent:
  title: Build checks
  url: /reference/build-checks/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: Build checks
    url: /reference/build-checks/
  - title: StageNameCasing
    url: /reference/build-checks/stage-name-casing/
next:
  title: SecretsUsedInArgOrEnv
  url: /reference/build-checks/secrets-used-in-arg-or-env/
prev:
  title: UndefinedArgInFrom
  url: /reference/build-checks/undefined-arg-in-from/
---


## Output

```text
Stage name 'BuilderBase' should be lowercase
```

## Description

To help distinguish Dockerfile instruction keywords from identifiers, this rule
forces names of stages in a multi-stage Dockerfile to be all lowercase.

## Examples

❌ Bad: mixing uppercase and lowercase characters in the stage name.

```dockerfile
FROM alpine AS BuilderBase
```

✅ Good: stage name is all in lowercase.

```dockerfile
FROM alpine AS builder-base
```


