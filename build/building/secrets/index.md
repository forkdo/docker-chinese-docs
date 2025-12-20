# Build secrets

A build secret is any piece of sensitive information, such as a password or API
token, consumed as part of your application's build process.

Build arguments and environment variables are inappropriate for passing secrets
to your build, because they persist in the final image. Instead, you should use
secret mounts or SSH mounts, which expose secrets to your builds securely.

## Types of build secrets

- [Secret mounts](#secret-mounts) are general-purpose mounts for passing
  secrets into your build. A secret mount takes a secret from the build client
  and makes it temporarily available inside the build container, for the
  duration of the build instruction. This is useful if, for example, your build
  needs to communicate with a private artifact server or API.
- [SSH mounts](#ssh-mounts) are special-purpose mounts for making SSH sockets
  or keys available inside builds. They're commonly used when you need to fetch
  private Git repositories in your builds.
- [Git authentication for remote contexts](#git-authentication-for-remote-contexts)
  is a set of pre-defined secrets for when you build with a remote Git context
  that's also a private repository. These secrets are "pre-flight" secrets:
  they are not consumed within your build instruction, but they're used to
  provide the builder with the necessary credentials to fetch the context.

## Using build secrets

For secret mounts and SSH mounts, using build secrets is a two-step process.
First you need to pass the secret into the `docker build` command, and then you
need to consume the secret in your Dockerfile.

To pass a secret to a build, use the [`docker build --secret`
flag](/reference/cli/docker/buildx/build.md#secret), or the
equivalent options for [Bake](../bake/reference.md#targetsecret).








<div
  class="tabs"
  
    x-data="{ selected: 'CLI' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'CLI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'CLI'"
        
      >
        CLI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Bake' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Bake'"
        
      >
        Bake
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'CLI' && 'hidden'"
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
        x-data="{ code: 'JCBkb2NrZXIgYnVpbGQgLS1zZWNyZXQgaWQ9YXdzLHNyYz0kSE9NRS8uYXdzL2NyZWRlbnRpYWxzIC4=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-console" data-lang="console"><span class="line"><span class="cl"><span class="gp">$</span> docker build --secret <span class="nv">id</span><span class="o">=</span>aws,src<span class="o">=</span><span class="nv">$HOME</span>/.aws/credentials .
</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Bake' && 'hidden'"
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
        x-data="{ code: 'dmFyaWFibGUgIkhPTUUiIHsKICBkZWZhdWx0ID0gbnVsbAp9Cgp0YXJnZXQgImRlZmF1bHQiIHsKICBzZWNyZXQgPSBbCiAgICAiaWQ9YXdzLHNyYz0ke0hPTUV9Ly5hd3MvY3JlZGVudGlhbHMiCiAgXQp9', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-hcl" data-lang="hcl"><span class="line"><span class="cl"><span class="k">variable</span> <span class="s2">&#34;HOME&#34;</span> {
</span></span><span class="line"><span class="cl"><span class="n">  default</span> <span class="o">=</span> <span class="k">null</span>
</span></span><span class="line"><span class="cl">}
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl"><span class="k">target</span> <span class="s2">&#34;default&#34;</span> {
</span></span><span class="line"><span class="cl"><span class="n">  secret</span> <span class="o">=</span> <span class="p">[</span>
</span></span><span class="line"><span class="cl"><span class="n">    &#34;id</span><span class="o">=</span><span class="n">aws,src</span><span class="o">=</span><span class="si">${</span><span class="err">HOME</span><span class="si">}</span><span class="err">/</span><span class="p">.</span><span class="k">aws</span><span class="err">/</span><span class="k">credentials</span><span class="err">&#34;</span>
</span></span><span class="line"><span class="cl">  <span class="p">]</span>
</span></span><span class="line"><span class="cl">}</span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


To consume a secret in a build and make it accessible to the `RUN` instruction,
use the [`--mount=type=secret`](/reference/dockerfile.md#run---mounttypesecret)
flag in the Dockerfile.

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

## Secret mounts

Secret mounts expose secrets to the build containers, as files or environment
variables. You can use secret mounts to pass sensitive information to your
builds, such as API tokens, passwords, or SSH keys.

### Sources

The source of a secret can be either a
[file](/reference/cli/docker/buildx/build.md#file) or an
[environment variable](/reference/cli/docker/buildx/build.md#env).
When you use the CLI or Bake, the type can be detected automatically. You can
also specify it explicitly with `type=file` or `type=env`.

The following example mounts the environment variable `KUBECONFIG` to secret ID `kube`,
as a file in the build container at `/run/secrets/kube`.

```console
$ docker build --secret id=kube,env=KUBECONFIG .
```

When you use secrets from environment variables, you can omit the `env` parameter
to bind the secret to a file with the same name as the variable.
In the following example, the value of the `API_TOKEN` variable
is mounted to `/run/secrets/API_TOKEN` in the build container.

```console
$ docker build --secret id=API_TOKEN .
```

### Target

When consuming a secret in a Dockerfile, the secret is mounted to a file by
default. The default file path of the secret, inside the build container, is
`/run/secrets/<id>`. You can customize how the secrets get mounted in the build
container using the `target` and `env` options for the `RUN --mount` flag in
the Dockerfile.

The following example takes secret id `aws` and mounts it to a file at
`/run/secrets/aws` in the build container.

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

To mount a secret as a file with a different name, use the `target` option in
the `--mount` flag.

```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp ...
```

To mount a secret as an environment variable instead of a file, use the
`env` option in the `--mount` flag.

```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=aws-session-token,env=AWS_SESSION_TOKEN \
    aws s3 cp ...
```

It's possible to use the `target` and `env` options together to mount a secret
as both a file and an environment variable.

## SSH mounts

If the credential you want to use in your build is an SSH agent socket or key,
you can use the SSH mount instead of a secret mount. Cloning private Git
repositories is a common use case for SSH mounts.

The following example clones a private GitHub repository using a [Dockerfile
SSH mount](/reference/dockerfile.md#run---mounttypessh).

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD git@github.com:me/myprivaterepo.git /src/
```

To pass an SSH socket the build, you use the [`docker build --ssh`
flag](/reference/cli/docker/buildx/build.md#ssh), or equivalent
options for [Bake](../bake/reference.md#targetssh).

```console
$ docker buildx build --ssh default .
```

## Git authentication for remote contexts

BuildKit supports two pre-defined build secrets, `GIT_AUTH_TOKEN` and
`GIT_AUTH_HEADER`. Use them to specify HTTP authentication parameters when
building with remote, private Git repositories, including:

- Building with a private Git repository as build context
- Fetching private Git repositories in a build with `ADD`

For example, say you have a private GitLab project at
`https://gitlab.com/example/todo-app.git`, and you want to run a build using
that repository as the build context. An unauthenticated `docker build` command
fails because the builder isn't authorized to pull the repository:

```console
$ docker build https://gitlab.com/example/todo-app.git
[+] Building 0.4s (1/1) FINISHED
 => ERROR [internal] load git source https://gitlab.com/example/todo-app.git
------
 > [internal] load git source https://gitlab.com/example/todo-app.git:
0.313 fatal: could not read Username for 'https://gitlab.com': terminal prompts disabled
------
```

To authenticate the builder to the Git server, set the `GIT_AUTH_TOKEN`
environment variable to contain a valid GitLab access token, and pass it as a
secret to the build:

```console
$ GIT_AUTH_TOKEN=$(cat gitlab-token.txt) docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://gitlab.com/example/todo-app.git
```

The `GIT_AUTH_TOKEN` also works with `ADD` to fetch private Git repositories as
part of your build:

```dockerfile
FROM alpine
ADD https://gitlab.com/example/todo-app.git /src
```

### HTTP authentication scheme

By default, Git authentication over HTTP uses the Bearer authentication scheme:

```http
Authorization: Bearer <GIT_AUTH_TOKEN>
```

If you need to use a Basic scheme, with a username and password, you can set
the `GIT_AUTH_HEADER` build secret:

```console
$ export GIT_AUTH_TOKEN=$(cat gitlab-token.txt)
$ export GIT_AUTH_HEADER=basic
$ docker build \
  --secret id=GIT_AUTH_TOKEN \
  --secret id=GIT_AUTH_HEADER \
  https://gitlab.com/example/todo-app.git
```

BuildKit currently only supports the Bearer and Basic schemes.

### Multiple hosts

You can set the `GIT_AUTH_TOKEN` and `GIT_AUTH_HEADER` secrets on a per-host
basis, which lets you use different authentication parameters for different
hostnames. To specify a hostname, append the hostname as a suffix to the secret
ID:

```console
$ export GITLAB_TOKEN=$(cat gitlab-token.txt)
$ export GERRIT_TOKEN=$(cat gerrit-username-password.txt)
$ export GERRIT_SCHEME=basic
$ docker build \
  --secret id=GIT_AUTH_TOKEN.gitlab.com,env=GITLAB_TOKEN \
  --secret id=GIT_AUTH_TOKEN.gerrit.internal.example,env=GERRIT_TOKEN \
  --secret id=GIT_AUTH_HEADER.gerrit.internal.example,env=GERRIT_SCHEME \
  https://gitlab.com/example/todo-app.git
```

