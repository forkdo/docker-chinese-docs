# Optimize cache usage in builds

When building with Docker, a layer is reused from the build cache if the
instruction and the files it depends on hasn't changed since it was previously
built. Reusing layers from the cache speeds up the build process because Docker
doesn't have to rebuild the layer again.

Here are a few techniques you can use to optimize build caching and speed up
the build process:

- [Order your layers](#order-your-layers): Putting the commands in your
  Dockerfile into a logical order can help you avoid unnecessary cache
  invalidation.
- [Keep the context small](#keep-the-context-small): The context is the set of
  files and directories that are sent to the builder to process a build
  instruction. Keeping the context as small as possible reduces the amount of data that
  needs to be sent to the builder, and reduces the likelihood of cache
  invalidation.
- [Use bind mounts](#use-bind-mounts): Bind mounts let you mount a file or
  directory from the host machine into the build container. Using bind mounts
  can help you avoid unnecessary layers in the image, which can slow down the
  build process.
- [Use cache mounts](#use-cache-mounts): Cache mounts let you specify a
  persistent package cache to be used during builds. The persistent cache helps
  speed up build steps, especially steps that involve installing packages using
  a package manager. Having a persistent cache for packages means that even if
  you rebuild a layer, you only download new or changed packages.
- [Use an external cache](#use-an-external-cache): An external cache lets you
  store build cache at a remote location. The external cache image can be
  shared between multiple builds, and across different environments.

## Order your layers

Putting the commands in your Dockerfile into a logical order is a great place
to start. Because a change causes a rebuild for steps that follow, try to make
expensive steps appear near the beginning of the Dockerfile. Steps that change
often should appear near the end of the Dockerfile, to avoid triggering
rebuilds of layers that haven't changed.

Consider the following example. A Dockerfile snippet that runs a JavaScript
build from the source files in the current directory:

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY . .          # Copy over all files in the current directory
RUN npm install   # Install dependencies
RUN npm build     # Run build
```

This Dockerfile is rather inefficient. Updating any file causes a reinstall of
all dependencies every time you build the Docker image even if the dependencies
didn't change since last time.

Instead, the `COPY` command can be split in two. First, copy over the package
management files (in this case, `package.json` and `yarn.lock`). Then, install
the dependencies. Finally, copy over the project source code, which is subject
to frequent change.

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY package.json yarn.lock .    # Copy package management files
RUN npm install                  # Install dependencies
COPY . .                         # Copy over project files
RUN npm build                    # Run build
```

By installing dependencies in earlier layers of the Dockerfile, there is
no need to rebuild those layers when a project file has changed.

## Keep the context small

The easiest way to make sure your context doesn't include unnecessary files is
to create a `.dockerignore` file in the root of your build context. The
`.dockerignore` file works similarly to `.gitignore` files, and lets you
exclude files and directories from the build context.

Here's an example `.dockerignore` file that excludes the `node_modules`
directory, all files and directories that start with `tmp`:

```plaintext {title=".dockerignore"}
node_modules
tmp*
```

Ignore-rules specified in the `.dockerignore` file apply to the entire build
context, including subdirectories. This means it's a rather coarse-grained
mechanism, but it's a good way to exclude files and directories that you know
you don't need in the build context, such as temporary files, log files, and
build artifacts.

## Use bind mounts

You might be familiar with bind mounts for when you run containers with `docker
run` or Docker Compose. Bind mounts let you mount a file or directory from the
host machine into a container.

```bash
# bind mount using the -v flag
docker run -v $(pwd):/path/in/container image-name
# bind mount using the --mount flag
docker run --mount=type=bind,src=.,dst=/path/in/container image-name
```

To use bind mounts in a build, you can use the `--mount` flag with the `RUN`
instruction in your Dockerfile:

```dockerfile
FROM golang:latest
WORKDIR /app
RUN --mount=type=bind,target=. go build -o /app/hello
```

In this example, the current directory is mounted into the build container
before the `go build` command gets executed. The source code is available in
the build container for the duration of that `RUN` instruction. When the
instruction is done executing, the mounted files are not persisted in the final
image, or in the build cache. Only the output of the `go build` command
remains.

The `COPY` and `ADD` instructions in a Dockerfile lets you copy files from the
build context into the build container. Using bind mounts is beneficial for
build cache optimization because you're not adding unnecessary layers to the
cache. If you have build context that's on the larger side, and it's only used
to generate an artifact, you're better off using bind mounts to temporarily
mount the source code required to generate the artifact into the build. If you
use `COPY` to add the files to the build container, BuildKit will include all
of those files in the cache, even if the files aren't used in the final image.

There are a few things to be aware of when using bind mounts in a build:

- Bind mounts are read-only by default. If you need to write to the mounted
  directory, you need to specify the `rw` option. However, even with the `rw`
  option, the changes are not persisted in the final image or the build cache.
  The file writes are sustained for the duration of the `RUN` instruction, and
  are discarded after the instruction is done.
- Mounted files are not persisted in the final image. Only the output of the
  `RUN` instruction is persisted in the final image. If you need to include
  files from the build context in the final image, you need to use the `COPY`
  or `ADD` instructions.
- If the target directory is not empty, the contents of the target directory
  are hidden by the mounted files. The original contents are restored after the
  `RUN` instruction is done.

  




<div
  id="example"
  x-data="{ open: false }"
  class="my-6 rounded-sm border border-gray-200 bg-white py-2 dark:border-gray-700 dark:bg-gray-900"
>
  <button
    class="not-prose flex w-full justify-between px-4 py-2"
    x-on:click="open = ! open"
  >
    <div class=" flex items-center gap-2">
      Example
    </div>
    <span :class="{ 'hidden' : !open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M316-400q-6.75 0-10.87-4.64-4.13-4.63-4.13-10.81 0-1.55 5-10.55l158-157q3-3 7.06-5 4.07-2 8.94-2 4.88 0 8.94 2t7.06 5l158 157q2 2 3.5 4.76 1.5 2.77 1.5 5.92 0 6.32-4.12 10.82-4.13 4.5-10.88 4.5H316Z"/></svg></span
    >
    <span :class="{ 'hidden' : open }" class="icon-svg"
      ><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M464-376 306-533q-2-2-3.5-4.76-1.5-2.77-1.5-5.92 0-6.32 4.13-10.82 4.12-4.5 10.87-4.5h328q6.75 0 10.88 4.64 4.12 4.63 4.12 10.81 0 1.55-5 10.55L496-376q-3 3-7.06 5t-8.94 2q-4.87 0-8.94-2-4.06-2-7.06-5Z"/></svg></span
    >
  </button>
  <div x-show="open" x-collapse class="px-4">
    <p>For example, given a build context with only a <code>Dockerfile</code> in it:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'LgrilJTilIDilIAgRG9ja2VyZmlsZQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-plaintext" data-lang="plaintext"><span class="line"><span class="cl">.
</span></span><span class="line"><span class="cl">└── Dockerfile</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>And a Dockerfile that mounts the current directory into the build container:</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'RlJPTSBhbHBpbmU6bGF0ZXN0CldPUktESVIgL3dvcmsKUlVOIHRvdWNoIGZvby50eHQKUlVOIC0tbW91bnQ9dHlwZT1iaW5kLHRhcmdldD0uIGxzClJVTiBscw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">FROM</span><span class="s"> alpine:latest</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">WORKDIR</span><span class="s"> /work</span><span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> touch foo.txt<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>bind,target<span class="o">=</span>. ls<span class="err">
</span></span></span><span class="line"><span class="cl"><span class="err"></span><span class="k">RUN</span> ls</span></span></code></pre></div>
      
    </div>
  </div>
</div>
<p>The first <code>ls</code> command with the bind mount shows the contents of the mounted
directory. The second <code>ls</code> lists the contents of the original build context.</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
    <div class="flex w-full items-center gap-2">
      <div
        class="flex items-center gap-2.5 rounded bg-gray-100 px-2 py-0.5 dark:bg-gray-800"
      >
        <div class="font-normal text-gray-500 dark:text-gray-200">
          Build log
        </div>
      </div>
    </div>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'IzggW3N0YWdlLTAgMy81XSBSVU4gdG91Y2ggZm9vLnR4dAojOCBET05FIDAuMXMKCiM5IFtzdGFnZS0wIDQvNV0gUlVOIC0tbW91bnQ9dGFyZ2V0PS4gbHMgLTEKIzkgMC4wNDAgRG9ja2VyZmlsZQojOSBET05FIDAuMHMKCiMxMCBbc3RhZ2UtMCA1LzVdIFJVTiBscyAtMQojMTAgMC4wNDYgZm9vLnR4dAojMTAgRE9ORSAwLjFz', copying: false }"
        class="
          -top-10
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-plaintext" data-lang="plaintext"><span class="line"><span class="cl">#8 [stage-0 3/5] RUN touch foo.txt
</span></span><span class="line"><span class="cl">#8 DONE 0.1s
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">#9 [stage-0 4/5] RUN --mount=target=. ls -1
</span></span><span class="line"><span class="cl">#9 0.040 Dockerfile
</span></span><span class="line"><span class="cl">#9 DONE 0.0s
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">#10 [stage-0 5/5] RUN ls -1
</span></span><span class="line"><span class="cl">#10 0.046 foo.txt
</span></span><span class="line"><span class="cl">#10 DONE 0.1s</span></span></code></pre></div>
      
    </div>
  </div>
</div>

  </div>
</div>



## Use cache mounts

Regular cache layers in Docker correspond to an exact match of the instruction
and the files it depends on. If the instruction and the files it depends on
have changed since the layer was built, the layer is invalidated, and the build
process has to rebuild the layer.

Cache mounts are a way to specify a persistent cache location to be used during
builds. The cache is cumulative across builds, so you can read and write to the
cache multiple times. This persistent caching means that even if you need to
rebuild a layer, you only download new or changed packages. Any unchanged
packages are reused from the cache mount.

To use cache mounts in a build, you can use the `--mount` flag with the `RUN`
instruction in your Dockerfile:

```dockerfile
FROM node:latest
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm npm install
```

In this example, the `npm install` command uses a cache mount for the
`/root/.npm` directory, the default location for the npm cache. The cache mount
is persisted across builds, so even if you end up rebuilding the layer, you
only download new or changed packages. Any changes to the cache are persisted
across builds, and the cache is shared between multiple builds.

How you specify cache mounts depends on the build tool you're using. If you're
unsure how to specify cache mounts, refer to the documentation for the build
tool you're using. Here are a few examples:








<div
  class="tabs"
  
    x-data="{ selected: 'Go' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Go' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Go'"
        
      >
        Go
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Apt' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Apt'"
        
      >
        Apt
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Python'"
        
      >
        Python
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Ruby' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Ruby'"
        
      >
        Ruby
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Rust' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Rust'"
        
      >
        Rust
      </button>
    
      <button
        class="tab-item"
        :class="selected === '.NET' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '.NET'"
        
      >
        .NET
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'PHP' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'PHP'"
        
      >
        PHP
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Go' && 'hidden'"
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
        x-data="{ code: 'UlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L2dvL3BrZy9tb2QgXAogICAgZ28gYnVpbGQgLW8gL2FwcC9oZWxsbw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/go/pkg/mod <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    go build -o /app/hello</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Apt' && 'hidden'"
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
        x-data="{ code: 'UlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3Zhci9jYWNoZS9hcHQsc2hhcmluZz1sb2NrZWQgXAogIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3Zhci9saWIvYXB0LHNoYXJpbmc9bG9ja2VkIFwKICBhcHQgdXBkYXRlICYmIGFwdC1nZXQgLS1uby1pbnN0YWxsLXJlY29tbWVuZHMgaW5zdGFsbCAteSBnY2M=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/var/cache/apt,sharing<span class="o">=</span>locked <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>  --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/var/lib/apt,sharing<span class="o">=</span>locked <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>  apt update <span class="o">&amp;&amp;</span> apt-get --no-install-recommends install -y gcc</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Python' && 'hidden'"
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
        x-data="{ code: 'UlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3Jvb3QvLmNhY2hlL3BpcCBcCiAgICBwaXAgaW5zdGFsbCAtciByZXF1aXJlbWVudHMudHh0', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.cache/pip <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    pip install -r requirements.txt</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Ruby' && 'hidden'"
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
        x-data="{ code: 'UlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3Jvb3QvLmdlbSBcCiAgICBidW5kbGUgaW5zdGFsbA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.gem <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    bundle install</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Rust' && 'hidden'"
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
        x-data="{ code: 'UlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L2FwcC90YXJnZXQvIFwKICAgIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3Vzci9sb2NhbC9jYXJnby9naXQvZGIgXAogICAgLS1tb3VudD10eXBlPWNhY2hlLHRhcmdldD0vdXNyL2xvY2FsL2NhcmdvL3JlZ2lzdHJ5LyBcCiAgICBjYXJnbyBidWlsZA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/app/target/ <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/usr/local/cargo/git/db <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/usr/local/cargo/registry/ <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    cargo build</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '.NET' && 'hidden'"
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
        x-data="{ code: 'UlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3Jvb3QvLm51Z2V0L3BhY2thZ2VzIFwKICAgIGRvdG5ldCByZXN0b3Jl', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/root/.nuget/packages <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    dotnet restore</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'PHP' && 'hidden'"
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
        x-data="{ code: 'UlVOIC0tbW91bnQ9dHlwZT1jYWNoZSx0YXJnZXQ9L3RtcC9jYWNoZSBcCiAgICBjb21wb3NlciBpbnN0YWxs', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-dockerfile" data-lang="dockerfile"><span class="line"><span class="cl"><span class="k">RUN</span> --mount<span class="o">=</span><span class="nv">type</span><span class="o">=</span>cache,target<span class="o">=</span>/tmp/cache <span class="se">\
</span></span></span><span class="line"><span class="cl"><span class="se"></span>    composer install</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


It's important that you read the documentation for the build tool you're using
to make sure you're using the correct cache mount options. Package managers
have different requirements for how they use the cache, and using the wrong
options can lead to unexpected behavior. For example, Apt needs exclusive
access to its data, so the caches use the option `sharing=locked` to ensure
parallel builds using the same cache mount wait for each other and not access
the same cache files at the same time.

## Use an external cache

The default cache storage for builds is internal to the builder (BuildKit
instance) you're using. Each builder uses its own cache storage. When you
switch between different builders, the cache is not shared between them. Using
an external cache lets you define a remote location for pushing and pulling
cache data.

External caches are especially useful for CI/CD pipelines, where the builders
are often ephemeral, and build minutes are precious. Reusing the cache between
builds can drastically speed up the build process and reduce cost. You can even
make use of the same cache in your local development environment.

To use an external cache, you specify the `--cache-to` and `--cache-from`
options with the `docker buildx build` command.

- `--cache-to` exports the build cache to the specified location.
- `--cache-from` specifies remote caches for the build to use.

The following example shows how to set up a GitHub Actions workflow using
`docker/build-push-action`, and push the build cache layers to an OCI registry
image:

```yaml {title=".github/workflows/ci.yml"}
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

This setup tells BuildKit to look for cache in the `user/app:buildcache` image.
And when the build is done, the new build cache is pushed to the same image,
overwriting the old cache.

This cache can be used locally as well. To pull the cache in a local build,
you can use the `--cache-from` option with the `docker buildx build` command:

```console
$ docker buildx build --cache-from type=registry,ref=user/app:buildcache .
```

## Summary

Optimizing cache usage in builds can significantly speed up the build process.
Keeping the build context small, using bind mounts, cache mounts, and external
caches are all techniques you can use to make the most of the build cache and
speed up the build process.

For more information about the concepts discussed in this guide, see:

- [.dockerignore files](/manuals/build/concepts/context.md#dockerignore-files)
- [Cache invalidation](/manuals/build/cache/invalidation.md)
- [Cache mounts](/reference/dockerfile.md#run---mounttypecache)
- [Cache backend types](/manuals/build/cache/backends/_index.md)
- [Building best practices](/manuals/build/building/best-practices.md)

