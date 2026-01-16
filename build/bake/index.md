---
title: Bake
url: /build/bake/
parent:
  title: Docker Build
  url: /build/
breadcrumbs:
  - title: 手册
    url: /manuals/
  - title: Docker Build
    url: /build/
  - title: Bake
    url: /build/bake/
children:
  - title: Introduction to Bake
    url: /build/bake/introduction/
    description: Get started with using Bake to build your project
  - title: Bake targets
    url: /build/bake/targets/
    description: Learn how to define and use targets in Bake
  - title: Inheritance in Bake
    url: /build/bake/inheritance/
    description: Learn how to inherit attributes from other targets in Bake
  - title: Variables in Bake
    url: /build/bake/variables/
  - title: Expression evaluation in Bake
    url: /build/bake/expressions/
    description: Learn about advanced Bake features, like user-defined functions
  - title: Functions
    url: /build/bake/funcs/
    description: Learn about built-in and user-defined HCL functions with Bake
  - title: Matrix targets
    url: /build/bake/matrices/
    description: Learn how to define and use matrix targets in Bake to fork a single target into multiple different variants
  - title: Using Bake with additional contexts
    url: /build/bake/contexts/
    description: Additional contexts are useful when you want to pin image versions,
or reference the output of other targets

  - title: Bake file reference
    url: /build/bake/reference/
  - title: Bake standard library functions
    url: /build/bake/stdlib/
  - title: Building with Bake from a Compose file
    url: /build/bake/compose-file/
    description: Build your compose services with Bake
  - title: Overriding configurations
    url: /build/bake/overrides/
    description: Learn how to override configurations in Bake files to build with different attributes.
  - title: Remote Bake file definition
    url: /build/bake/remote-definition/
    description: Build with Bake using a remote file definition using Git or HTTP
---


Bake is a feature of Docker Buildx that lets you define your build configuration
using a declarative file, as opposed to specifying a complex CLI expression. It
also lets you run multiple builds concurrently with a single invocation.

A Bake file can be written in HCL, JSON, or YAML formats, where the YAML format
is an extension of a Docker Compose file. Here's an example Bake file in HCL
format:

```hcl {title=docker-bake.hcl}
group "default" {
  targets = ["frontend", "backend"]
}

target "frontend" {
  context = "./frontend"
  dockerfile = "frontend.Dockerfile"
  args = {
    NODE_VERSION = "22"
  }
  tags = ["myapp/frontend:latest"]
}

target "backend" {
  context = "./backend"
  dockerfile = "backend.Dockerfile"
  args = {
    GO_VERSION = "1.24"
  }
  tags = ["myapp/backend:latest"]
}
```

The `group` block defines a group of targets that can be built concurrently.
Each `target` block defines a build target with its own configuration, such as
the build context, Dockerfile, and tags.

To invoke a build using the above Bake file, you can run:

```console
$ docker buildx bake
```

This executes the `default` group, which builds the `frontend` and `backend`
targets concurrently.

## Get started

To learn how to get started with Bake, head over to the [Bake introduction](./introduction.md).

