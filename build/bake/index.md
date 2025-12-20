# Bake

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


- [Introduction to Bake](/build/bake/introduction/)

- [Bake targets](/build/bake/targets/)

- [Inheritance in Bake](/build/bake/inheritance/)

- [Variables in Bake](/build/bake/variables/)

- [Expression evaluation in Bake](/build/bake/expressions/)

- [Functions](/build/bake/funcs/)

- [Matrix targets](/build/bake/matrices/)

- [Using Bake with additional contexts](/build/bake/contexts/)

- [Bake file reference](/build/bake/reference/)

- [Bake standard library functions](/build/bake/stdlib/)

- [Building with Bake from a Compose file](/build/bake/compose-file/)

- [Overriding configurations](/build/bake/overrides/)

- [Remote Bake file definition](/build/bake/remote-definition/)

