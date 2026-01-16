---
title: DuplicateStageName
url: /reference/build-checks/duplicate-stage-name/
parent:
  title: Build checks
  url: /reference/build-checks/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: Build checks
    url: /reference/build-checks/
  - title: DuplicateStageName
    url: /reference/build-checks/duplicate-stage-name/
next:
  title: CopyIgnoredFile
  url: /reference/build-checks/copy-ignored-file/
prev:
  title: ExposeInvalidFormat
  url: /reference/build-checks/expose-invalid-format/
---


## Output

```text
Duplicate stage name 'foo-base', stage names should be unique
```

## Description

Defining multiple stages with the same name results in an error because the
builder is unable to uniquely resolve the stage name reference.

## Examples

❌ Bad: `builder` is declared as a stage name twice.

```dockerfile
FROM debian:latest AS builder
RUN apt-get update; apt-get install -y curl

FROM golang:latest AS builder
```

✅ Good: stages have unique names.

```dockerfile
FROM debian:latest AS deb-builder
RUN apt-get update; apt-get install -y curl

FROM golang:latest AS go-builder
```


