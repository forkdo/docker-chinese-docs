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


- [Introduction to Bake](https://docs.docker.com/build/bake/introduction/)

- [Bake targets](https://docs.docker.com/build/bake/targets/)

- [Inheritance in Bake](https://docs.docker.com/build/bake/inheritance/)

- [Variables in Bake](https://docs.docker.com/build/bake/variables/)

- [Expression evaluation in Bake](https://docs.docker.com/build/bake/expressions/)

- [Functions](https://docs.docker.com/build/bake/funcs/)

- [Matrix targets](https://docs.docker.com/build/bake/matrices/)

- [Using Bake with additional contexts](https://docs.docker.com/build/bake/contexts/)

- [Bake file reference](https://docs.docker.com/build/bake/reference/)

- [Bake standard library functions](https://docs.docker.com/build/bake/stdlib/)

- [Building with Bake from a Compose file](https://docs.docker.com/build/bake/compose-file/)

- [Overriding configurations](https://docs.docker.com/build/bake/overrides/)

- [Remote Bake file definition](https://docs.docker.com/build/bake/remote-definition/)

