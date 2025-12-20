# Multi-platform builds

A multi-platform build refers to a single build invocation that targets
multiple different operating system or CPU architecture combinations. When
building images, this lets you create a single image that can run on multiple
platforms, such as `linux/amd64`, `linux/arm64`, and `windows/amd64`.

## Why multi-platform builds?

Docker solves the "it works on my machine" problem by packaging applications
and their dependencies into containers. This makes it easy to run the same
application on different environments, such as development, testing, and
production.

But containerization by itself only solves part of the problem. Containers
share the host kernel, which means that the code that's running inside the
container must be compatible with the host's architecture. This is why you
can't run a `linux/amd64` container on an arm64 host (without using emulation),
or a Windows container on a Linux host.

Multi-platform builds solve this problem by packaging multiple variants of the
same application into a single image. This enables you to run the same image on
different types of hardware, such as development machines running x86-64 or
ARM-based Amazon EC2 instances in the cloud, without the need for emulation.

### Difference between single-platform and multi-platform images

Multi-platform images have a different structure than single-platform images.
Single-platform images contain a single manifest that points to a single
configuration and a single set of layers. Multi-platform images contain a
manifest list, pointing to multiple manifests, each of which points to a
different configuration and set of layers.

![Multi-platform image structure](/build/images/single-vs-multiplatform-image.svg)

When you push a multi-platform image to a registry, the registry stores the
manifest list and all the individual manifests. When you pull the image, the
registry returns the manifest list, and Docker automatically selects the
correct variant based on the host's architecture. For example, if you run a
multi-platform image on an ARM-based Raspberry Pi, Docker selects the
`linux/arm64` variant. If you run the same image on an x86-64 laptop, Docker
selects the `linux/amd64` variant (if you're using Linux containers).

## Prerequisites

To build multi-platform images, you first need to make sure that your Docker
environment is set up to support it. There are two ways you can do that:

- You can switch from the "classic" image store to the containerd image store.
- You can create and use a custom builder.

The "classic" image store of the Docker Engine does not support multi-platform
images. Switching to the containerd image store ensures that your Docker Engine
can push, pull, and build multi-platform images.

Creating a custom builder that uses a driver with multi-platform support,
such as the `docker-container` driver, will let you build multi-platform images
without switching to a different image store. However, you still won't be able
to load the multi-platform images you build into your Docker Engine image
store. But you can push them to a container registry directly with `docker
build --push`.








<div
  class="tabs"
  
    x-data="{ selected: 'containerd-image-store' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'containerd-image-store' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'containerd-image-store'"
        
      >
        containerd image store
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Custom-builder' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Custom-builder'"
        
      >
        Custom builder
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'containerd-image-store' && 'hidden'"
      >
        <p>The steps for enabling the containerd image store depends on whether you're
using Docker Desktop or Docker Engine standalone:</p>
<ul>
<li>
<p>If you're using Docker Desktop, enable the containerd image store in the

    
  
  <a class="link" href="/desktop/features/containerd/">Docker Desktop settings</a>.</p>
</li>
<li>
<p>If you're using Docker Engine standalone, enable the containerd image store
using the 
    
  
  <a class="link" href="/engine/storage/containerd/">daemon configuration file</a>.</p>
</li>
</ul>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Custom-builder' && 'hidden'"
      >
        <p>To create a custom builder, use the <code>docker buildx create</code> command to create a
builder that uses the <code>docker-container</code> driver.</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'JCBkb2NrZXIgYnVpbGR4IGNyZWF0ZSBcCiAgLS1uYW1lIGNvbnRhaW5lci1idWlsZGVyIFwKICAtLWRyaXZlciBkb2NrZXItY29udGFpbmVyIFwKICAtLWJvb3RzdHJhcCAtLXVzZQ==', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker buildx create <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span><span class="go">  --name container-builder \
</span></span></span><span class="line"><span class="cl"><span class="go">  --driver docker-container \
</span></span></span><span class="line"><span class="cl"><span class="go">  --bootstrap --use
</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>Builds with the <code>docker-container</code> driver aren't automatically loaded to your
Docker Engine image store. For more information, see 
    
  
  <a class="link" href="/build/builders/drivers/">Build
drivers</a>.</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


If you're using Docker Engine standalone and you need to build multi-platform
images using emulation, you also need to install QEMU, see [Install QEMU
manually](#install-qemu-manually).

## Build multi-platform images

When triggering a build, use the `--platform` flag to define the target
platforms for the build output, such as `linux/amd64` and `linux/arm64`:

```console
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

## Strategies

You can build multi-platform images using three different strategies,
depending on your use case:

1. Using emulation, via [QEMU](#qemu)
2. Use a builder with [multiple native nodes](#multiple-native-nodes)
3. Use [cross-compilation](#cross-compilation) with multi-stage builds

### QEMU

Building multi-platform images under emulation with QEMU is the easiest way to
get started if your builder already supports it. Using emulation requires no
changes to your Dockerfile, and BuildKit automatically detects the
architectures that are available for emulation.

> [!NOTE]
>
> Emulation with QEMU can be much slower than native builds, especially for
> compute-heavy tasks like compilation and compression or decompression.
>
> Use [multiple native nodes](#multiple-native-nodes) or
> [cross-compilation](#cross-compilation) instead, if possible.

Docker Desktop supports running and building multi-platform images under
emulation by default. No configuration is necessary as the builder uses the
QEMU that's bundled within the Docker Desktop VM.

#### Install QEMU manually

If you're using a builder outside of Docker Desktop, such as if you're using
Docker Engine on Linux, or a custom remote builder, you need to install QEMU
and register the executable types on the host OS. The prerequisites for
installing QEMU are:

- Linux kernel version 4.8 or later
- `binfmt-support` version 2.1.7 or later
- The QEMU binaries must be statically compiled and registered with the
  `fix_binary` flag

Use the [`tonistiigi/binfmt`](https://github.com/tonistiigi/binfmt) image to
install QEMU and register the executable types on the host with a single
command:

```console
$ docker run --privileged --rm tonistiigi/binfmt --install all
```

This installs the QEMU binaries and registers them with
[`binfmt_misc`](https://en.wikipedia.org/wiki/Binfmt_misc), enabling QEMU to
execute non-native file formats for emulation.

Once QEMU is installed and the executable types are registered on the host OS,
they work transparently inside containers. You can verify your registration by
checking if `F` is among the flags in `/proc/sys/fs/binfmt_misc/qemu-*`.

### Multiple native nodes

Using multiple native nodes provide better support for more complicated cases
that QEMU can't handle, and also provides better performance.

You can add additional nodes to a builder using the `--append` flag.

The following command creates a multi-node builder from Docker contexts named
`node-amd64` and `node-arm64`. This example assumes that you've already added
those contexts.

```console
$ docker buildx create --use --name mybuild node-amd64
mybuild
$ docker buildx create --append --name mybuild node-arm64
$ docker buildx build --platform linux/amd64,linux/arm64 .
```

While this approach has advantages over emulation, managing multi-node builders
introduces some overhead of setting up and managing builder clusters.
Alternatively, you can use Docker Build Cloud, a service that provides managed
multi-node builders on Docker's infrastructure. With Docker Build Cloud, you
get native multi-platform ARM and X86 builders without the burden of
maintaining them. Using cloud builders also provides additional benefits, such
as a shared build cache.

After signing up for Docker Build Cloud, add the builder to your local
environment and start building.

```console
$ docker buildx create --driver cloud <ORG>/<BUILDER_NAME>
cloud-<ORG>-<BUILDER_NAME>
$ docker build \
  --builder cloud-<ORG>-<BUILDER_NAME> \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  --tag <IMAGE_NAME> \
  --push .
```

For more information, see [Docker Build Cloud](/manuals/build-cloud/_index.md).

### Cross-compilation

Depending on your project, if the programming language you use has good support
for cross-compilation, you can leverage multi-stage builds to build binaries
for target platforms from the native architecture of the builder. Special build
arguments, such as `BUILDPLATFORM` and `TARGETPLATFORM`, are automatically
available for use in your Dockerfile.

In the following example, the `FROM` instruction is pinned to the native
platform of the builder (using the `--platform=$BUILDPLATFORM` option) to
prevent emulation from kicking in. Then the pre-defined `$BUILDPLATFORM` and
`$TARGETPLATFORM` build arguments are interpolated in a `RUN` instruction. In
this case, the values are just printed to stdout with `echo`, but this
illustrates how you would pass them to the compiler for cross-compilation.

```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:alpine AS build
ARG TARGETPLATFORM
ARG BUILDPLATFORM
RUN echo "I am running on $BUILDPLATFORM, building for $TARGETPLATFORM" > /log
FROM alpine
COPY --from=build /log /log
```

## Examples

Here are some examples of multi-platform builds:

- [Simple multi-platform build using emulation](#simple-multi-platform-build-using-emulation)
- [Multi-platform Neovim build using Docker Build Cloud](#multi-platform-neovim-build-using-docker-build-cloud)
- [Cross-compiling a Go application](#cross-compiling-a-go-application)

### Simple multi-platform build using emulation

This example demonstrates how to build a simple multi-platform image using
emulation with QEMU. The image contains a single file that prints the
architecture of the container.

Prerequisites:

- Docker Desktop, or Docker Engine with [QEMU installed](#install-qemu-manually)
- containerd image store enabled

Steps:

1. Create an empty directory and navigate to it:

   ```console
   $ mkdir multi-platform
   $ cd multi-platform
   ```

2. Create a simple Dockerfile that prints the architecture of the container:

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM alpine
   RUN uname -m > /arch
   ```

3. Build the image for `linux/amd64` and `linux/arm64`:

   ```console
   $ docker build --platform linux/amd64,linux/arm64 -t multi-platform .
   ```

4. Run the image and print the architecture:

   ```console
   $ docker run --rm multi-platform cat /arch
   ```

   - If you're running on an x86-64 machine, you should see `x86_64`.
   - If you're running on an ARM machine, you should see `aarch64`.

### Multi-platform Neovim build using Docker Build Cloud

This example demonstrates how run a multi-platform build using Docker Build
Cloud to compile and export [Neovim](https://github.com/neovim/neovim) binaries
for the `linux/amd64` and `linux/arm64` platforms.

Docker Build Cloud provides managed multi-node builders that support native
multi-platform builds without the need for emulation, making it much faster to
do CPU-intensive tasks like compilation.

Prerequisites:

- You've [signed up for Docker Build Cloud and created a builder](/manuals/build-cloud/setup.md)

Steps:

1. Create an empty directory and navigate to it:

   ```console
   $ mkdir docker-build-neovim
   $ cd docker-build-neovim
   ```

2. Create a Dockerfile that builds Neovim.

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM debian:bookworm AS build
   WORKDIR /work
   RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
       --mount=type=cache,target=/var/lib/apt,sharing=locked \
       apt-get update && apt-get install -y \
       build-essential \
       cmake \
       curl \
       gettext \
       ninja-build \
       unzip
   ADD https://github.com/neovim/neovim.git#stable .
   RUN make CMAKE_BUILD_TYPE=RelWithDebInfo
   
   FROM scratch
   COPY --from=build /work/build/bin/nvim /
   ```

3. Build the image for `linux/amd64` and `linux/arm64` using Docker Build Cloud:

   ```console
   $ docker build \
      --builder <cloud-builder> \
      --platform linux/amd64,linux/arm64 \
      --output ./bin .
   ```

   This command builds the image using the cloud builder and exports the
   binaries to the `bin` directory.

4. Verify that the binaries are built for both platforms. You should see the
   `nvim` binary for both `linux/amd64` and `linux/arm64`.

   ```console
   $ tree ./bin
   ./bin
   ├── linux_amd64
   │   └── nvim
   └── linux_arm64
       └── nvim
   
   3 directories, 2 files
   ```

### Cross-compiling a Go application

This example demonstrates how to cross-compile a Go application for multiple
platforms using multi-stage builds. The application is a simple HTTP server
that listens on port 8080 and returns the architecture of the container.
This example uses Go, but the same principles apply to other programming
languages that support cross-compilation.

Cross-compilation with Docker builds works by leveraging a series of
pre-defined (in BuildKit) build arguments that give you information about
platforms of the builder and the build targets. You can use these pre-defined
arguments to pass the platform information to the compiler.

In Go, you can use the `GOOS` and `GOARCH` environment variables to specify the
target platform to build for.

Prerequisites:

- Docker Desktop or Docker Engine

Steps:

1. Create an empty directory and navigate to it:

   ```console
   $ mkdir go-server
   $ cd go-server
   ```

2. Create a base Dockerfile that builds the Go application:

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM golang:alpine AS build
   WORKDIR /app
   ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
   RUN go build -o server .
   
   FROM alpine
   COPY --from=build /app/server /server
   ENTRYPOINT ["/server"]
   ```

   This Dockerfile can't build multi-platform with cross-compilation yet. If
   you were to try to build this Dockerfile with `docker build`, the builder
   would attempt to use emulation to build the image for the specified
   platforms.

3. To add cross-compilation support, update the Dockerfile to use the
   pre-defined `BUILDPLATFORM`, `TARGETOS` and `TARGETARCH` build arguments.

   - Pin the `golang` image to the platform of the builder using the
     `--platform=$BUILDPLATFORM` option.
   - Add `ARG` instructions for the Go compilation stages to make the
     `TARGETOS` and `TARGETARCH` build arguments available to the commands in
     this stage.
   - Set the `GOOS` and `GOARCH` environment variables to the values of
     `TARGETOS` and `TARGETARCH`. The Go compiler uses these variables to do
     cross-compilation.

   






<div
  class="tabs"
  
    x-data="{ selected: 'Updated-Dockerfile' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Updated-Dockerfile' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Updated-Dockerfile'"
        
      >
        Updated Dockerfile
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Old-Dockerfile' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Old-Dockerfile'"
        
      >
        Old Dockerfile
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Diff' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Diff'"
        
      >
        Diff
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Updated-Dockerfile' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQpGUk9NIC0tcGxhdGZvcm09JEJVSUxEUExBVEZPUk0gZ29sYW5nOmFscGluZSBBUyBidWlsZApBUkcgVEFSR0VUT1MKQVJHIFRBUkdFVEFSQ0gKV09SS0RJUiAvYXBwCkFERCBodHRwczovL2dpdGh1Yi5jb20vZHZka3NuL2J1aWxkbWUuZ2l0I2ViNjI3OWUwYWQ4YTEwMDAzNzE4NjU2YzY4Njc1MzliZDk0MjZhZDggLgpSVU4gR09PUz0ke1RBUkdFVE9TfSBHT0FSQ0g9JHtUQVJHRVRBUkNIfSBnbyBidWlsZCAtbyBzZXJ2ZXIgLgoKRlJPTSBhbHBpbmUKQ09QWSAtLWZyb209YnVpbGQgL2FwcC9zZXJ2ZXIgL3NlcnZlcgpFTlRSWVBPSU5UIFsiL3NlcnZlciJd', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> --platform=$BUILDPLATFORM golang:alpine AS build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> TARGETOS<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ARG</span> TARGETARCH<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ADD</span> https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> <span class="nv">GOOS</span><span class="o">=</span><span class="si">${</span><span class="nv">TARGETOS</span><span class="si">}</span> <span class="nv">GOARCH</span><span class="o">=</span><span class="si">${</span><span class="nv">TARGETARCH</span><span class="si">}</span> go build -o server .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> alpine</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build /app/server /server<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Old-Dockerfile' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQpGUk9NIGdvbGFuZzphbHBpbmUgQVMgYnVpbGQKV09SS0RJUiAvYXBwCkFERCBodHRwczovL2dpdGh1Yi5jb20vZHZka3NuL2J1aWxkbWUuZ2l0I2ViNjI3OWUwYWQ4YTEwMDAzNzE4NjU2YzY4Njc1MzliZDk0MjZhZDggLgpSVU4gZ28gYnVpbGQgLW8gc2VydmVyIC4KCkZST00gYWxwaW5lCkNPUFkgLS1mcm9tPWJ1aWxkIC9hcHAvc2VydmVyIC9zZXJ2ZXIKRU5UUllQT0lOVCBbIi9zZXJ2ZXIiXQ==', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="c"># syntax=docker/dockerfile:1</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> golang:alpine AS build</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /app</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ADD</span> https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> go build -o server .<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">FROM</span><span class="s"> alpine</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">COPY</span> --from<span class="o">=</span>build /app/server /server<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">ENTRYPOINT</span> <span class="p">[</span><span class="s2">&#34;/server&#34;</span><span class="p">]</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Diff' && 'hidden'"
      >
        <div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IyBzeW50YXg9ZG9ja2VyL2RvY2tlcmZpbGU6MQotRlJPTSBnb2xhbmc6YWxwaW5lIEFTIGJ1aWxkCitGUk9NIC0tcGxhdGZvcm09JEJVSUxEUExBVEZPUk0gZ29sYW5nOmFscGluZSBBUyBidWlsZAorQVJHIFRBUkdFVE9TCitBUkcgVEFSR0VUQVJDSApXT1JLRElSIC9hcHAKQUREIGh0dHBzOi8vZ2l0aHViLmNvbS9kdmRrc24vYnVpbGRtZS5naXQjZWI2Mjc5ZTBhZDhhMTAwMDM3MTg2NTZjNjg2NzUzOWJkOTQyNmFkOCAuCi1SVU4gZ28gYnVpbGQgLW8gc2VydmVyIC4KK1JVTiBHT09TPSR7VEFSR0VUT1N9IEdPQVJDSD0ke1RBUkdFVEFSQ0h9IGdvIGJ1aWxkIC1vIHNlcnZlciAuCgpGUk9NIGFscGluZQpDT1BZIC0tZnJvbT1idWlsZCAvYXBwL3NlcnZlciAvc2VydmVyCkVOVFJZUE9JTlQgWyIvc2VydmVyIl0=', copying: false }"
        class="
          top-1
         absolute right-2 z-10 text-gray-300 dark:text-gray-500"
        title="copy"
        @click="window.navigator.clipboard.writeText(atob(code).replaceAll(/^[\$>]\s+/gm, ''));
      copying = true;
      setTimeout(() => copying = false, 2000);"
      >
        <span
          :class="{ 'group-hover:block' : !copying }"
          class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M300-200q-24 0-42-18t-18-42v-560q0-24 18-42t42-18h440q24 0 42 18t18 42v560q0 24-18 42t-42 18H300ZM180-80q-24 0-42-18t-18-42v-590q0-13 8.5-21.5T150-760q13 0 21.5 8.5T180-730v590h470q13 0 21.5 8.5T680-110q0 13-8.5 21.5T650-80H180Z"/></svg></span
        >
        <span :class="{ 'group-hover:block' : copying }" class="icon-svg hidden"
          ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m421-389-98-98q-9-9-22-9t-23 10q-9 9-9 22t9 22l122 123q9 9 21 9t21-9l239-239q10-10 10-23t-10-23q-10-9-23.5-8.5T635-603L421-389Zm59 309q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Z"/></svg></span
        >
      </button>
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-diff" data-lang="diff"><span class="line"><span class="cl"># syntax=docker/dockerfile:1
</span></span><span class="line"><span class="cl"><span class="gd">-FROM golang:alpine AS build
</span></span></span><span class="line"><span class="cl"><span class="gd"></span><span class="gi">+FROM --platform=$BUILDPLATFORM golang:alpine AS build
</span></span></span><span class="line"><span class="cl"><span class="gi">+ARG TARGETOS
</span></span></span><span class="line"><span class="cl"><span class="gi">+ARG TARGETARCH
</span></span></span><span class="line"><span class="cl"><span class="gi"></span>WORKDIR /app
</span></span><span class="line"><span class="cl">ADD https://github.com/dvdksn/buildme.git#eb6279e0ad8a10003718656c6867539bd9426ad8 .
</span></span><span class="line"><span class="cl"><span class="gd">-RUN go build -o server .
</span></span></span><span class="line"><span class="cl"><span class="gd"></span><span class="gi">+RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} go build -o server .
</span></span></span><span class="line"><span class="cl"><span class="gi"></span>
</span></span><span class="line"><span class="cl">FROM alpine
</span></span><span class="line"><span class="cl">COPY --from=build /app/server /server
</span></span><span class="line"><span class="cl">ENTRYPOINT [&#34;/server&#34;]
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


4. Build the image for `linux/amd64` and `linux/arm64`:

   ```console
   $ docker build --platform linux/amd64,linux/arm64 -t go-server .
   ```

This example has shown how to cross-compile a Go application for multiple
platforms with Docker builds. The specific steps on how to do cross-compilation
may vary depending on the programming language you're using. Consult the
documentation for your programming language to learn more about cross-compiling
for different platforms.

> [!TIP]
> You may also want to consider checking out
> [xx - Dockerfile cross-compilation helpers](https://github.com/tonistiigi/xx).
> `xx` is a Docker image containing utility scripts that make cross-compiling with Docker builds easier.

