---
title: FromAsCasing
url: /reference/build-checks/from-as-casing/
parent:
  title: Build checks
  url: /reference/build-checks/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: Build checks
    url: /reference/build-checks/
  - title: FromAsCasing
    url: /reference/build-checks/from-as-casing/
next:
  title: ExposeProtoCasing
  url: /reference/build-checks/expose-proto-casing/
prev:
  title: FromPlatformFlagConstDisallowed
  url: /reference/build-checks/from-platform-flag-const-disallowed/
---


## Output

```text
'as' and 'FROM' keywords' casing do not match
```

## Description

While Dockerfile keywords can be either uppercase or lowercase, mixing case
styles is not recommended for readability. This rule reports violations where
mixed case style occurs for a `FROM` instruction with an `AS` keyword declaring
a stage name.

## Examples

❌ Bad: `FROM` is uppercase, `AS` is lowercase.

```dockerfile
FROM debian:latest as builder
```

✅ Good: `FROM` and `AS` are both uppercase

```dockerfile
FROM debian:latest AS deb-builder
```

✅ Good: `FROM` and `AS` are both lowercase.

```dockerfile
from debian:latest as deb-builder
```

## Related errors

- [`FileConsistentCommandCasing`](./consistent-instruction-casing.md)


