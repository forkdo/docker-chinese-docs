---
title: ExposeProtoCasing
url: /reference/build-checks/expose-proto-casing/
parent:
  title: Build checks
  url: /reference/build-checks/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: Build checks
    url: /reference/build-checks/
  - title: ExposeProtoCasing
    url: /reference/build-checks/expose-proto-casing/
next:
  title: ExposeInvalidFormat
  url: /reference/build-checks/expose-invalid-format/
prev:
  title: FromAsCasing
  url: /reference/build-checks/from-as-casing/
---


## Output

```text
Defined protocol '80/TcP' in EXPOSE instruction should be lowercase
```

## Description

Protocol names in the [`EXPOSE`](https://docs.docker.com/reference/dockerfile/#expose)
instruction should be specified in lowercase to maintain consistency and
readability. This rule checks for protocols that are not in lowercase and
reports them.

## Examples

❌ Bad: protocol is not in lowercase.

```dockerfile
FROM alpine
EXPOSE 80/TcP
```

✅ Good: protocol is in lowercase.

```dockerfile
FROM alpine
EXPOSE 80/tcp
```


