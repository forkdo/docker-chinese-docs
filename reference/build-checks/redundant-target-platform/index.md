---
title: RedundantTargetPlatform
url: /reference/build-checks/redundant-target-platform/
parent:
  title: Build checks
  url: /reference/build-checks/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: Build checks
    url: /reference/build-checks/
  - title: RedundantTargetPlatform
    url: /reference/build-checks/redundant-target-platform/
next:
  title: NoEmptyContinuation
  url: /reference/build-checks/no-empty-continuation/
prev:
  title: ReservedStageName
  url: /reference/build-checks/reserved-stage-name/
---


## Output

```text
Setting platform to predefined $TARGETPLATFORM in FROM is redundant as this is the default behavior
```

## Description

A custom platform can be used for a base image. The default platform is the
same platform as the target output so setting the platform to `$TARGETPLATFORM`
is redundant and unnecessary.

## Examples

❌ Bad: this usage of `--platform` is redundant since `$TARGETPLATFORM` is the default.

```dockerfile
FROM --platform=$TARGETPLATFORM alpine AS builder
RUN apk add --no-cache git
```

✅ Good: omit the `--platform` argument.

```dockerfile
FROM alpine AS builder
RUN apk add --no-cache git
```


