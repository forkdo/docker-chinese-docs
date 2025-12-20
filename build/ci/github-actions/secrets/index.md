# Using secrets with GitHub Actions

A build secret is sensitive information, such as a password or API token, consumed as part of the build process.
Docker Build supports two forms of secrets:

- [Secret mounts](#secret-mounts) add secrets as files in the build container
  (under `/run/secrets` by default).
- [SSH mounts](#ssh-mounts) add SSH agent sockets or keys into the build container.

This page shows how to use secrets with GitHub Actions.
For an introduction to secrets in general, see [Build secrets](/manuals/build/building/secrets.md).

## Secret mounts

In the following example uses and exposes the [`GITHUB_TOKEN` secret](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret)
as provided by GitHub in your workflow.

First, create a `Dockerfile` that uses the secret:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=github_token,env=GITHUB_TOKEN ...
```

In this example, the secret name is `github_token`. The following workflow
exposes this secret using the `secrets` input:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build
        uses: docker/build-push-action@v6
        with:
          platforms: linux/amd64,linux/arm64
          tags: user/app:latest
          secrets: |
            "github_token=${{ secrets.GITHUB_TOKEN }}"
```

> [!NOTE]
>
> You can also expose a secret file to the build with the `secret-files` input:
>
> ```yaml
> secret-files: |
>   "MY_SECRET=./secret.txt"
> ```

If you're using [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
and need to handle multi-line value, you will need to place the key-value pair
between quotes:

```yaml
secrets: |
  "MYSECRET=${{ secrets.GPG_KEY }}"
  GIT_AUTH_TOKEN=abcdefghi,jklmno=0123456789
  "MYSECRET=aaaaaaaa
  bbbbbbb
  ccccccccc"
  FOO=bar
  "EMPTYLINE=aaaa

  bbbb
  ccc"
  "JSON_SECRET={""key1"":""value1"",""key2"":""value2""}"
```

| Key              | Value                               |
| ---------------- | ----------------------------------- |
| `MYSECRET`       | `***********************`           |
| `GIT_AUTH_TOKEN` | `abcdefghi,jklmno=0123456789`       |
| `MYSECRET`       | `aaaaaaaa\nbbbbbbb\nccccccccc`      |
| `FOO`            | `bar`                               |
| `EMPTYLINE`      | `aaaa\n\nbbbb\nccc`                 |
| `JSON_SECRET`    | `{"key1":"value1","key2":"value2"}` |

> [!NOTE]
>
> Double escapes are needed for quote signs.

## SSH mounts

SSH mounts let you authenticate with SSH servers.
For example to perform a `git clone`,
or to fetch application packages from a private repository.

The following Dockerfile example uses an SSH mount
to fetch Go modules from a private GitHub repository.

```dockerfile {collapse=1}
# syntax=docker/dockerfile:1

ARG GO_VERSION="1.24"

FROM golang:${GO_VERSION}-alpine AS base
ENV CGO_ENABLED=0
ENV GOPRIVATE="github.com/foo/*"
RUN apk add --no-cache file git rsync openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
WORKDIR /src

FROM base AS vendor
# this step configure git and checks the ssh key is loaded
RUN --mount=type=ssh <<EOT
  set -e
  echo "Setting Git SSH protocol"
  git config --global url."git@github.com:".insteadOf "https://github.com/"
  (
    set +e
    ssh -T git@github.com
    if [ ! "$?" = "1" ]; then
      echo "No GitHub SSH key loaded exiting..."
      exit 1
    fi
  )
EOT
# this one download go modules
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=ssh \
    go mod download -x

FROM vendor AS build
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache \
    go build ...
```

To build this Dockerfile, you must specify an SSH mount that the builder can
use in the steps with `--mount=type=ssh`.

The following GitHub Action workflow uses the `MrSquaare/ssh-setup-action`
third-party action to bootstrap SSH setup on the GitHub runner. The action
creates a private key defined by the GitHub Action secret `SSH_GITHUB_PPK` and
adds it to the SSH agent socket file at `SSH_AUTH_SOCK`. The SSH mount in the
build step assume `SSH_AUTH_SOCK` by default, so there's no need to specify the
ID or path for the SSH agent socket explicitly.








<div
  class="tabs"
  
    x-data="{ selected: 'docker/build-push-action' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'docker/build-push-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'docker/build-push-action'"
        
      >
        <code>docker/build-push-action</code>
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'docker/bake-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'docker/bake-action'"
        
      >
        <code>docker/bake-action</code>
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'docker/build-push-action' && 'hidden'"
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6Cgpqb2JzOgogIGRvY2tlcjoKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIG5hbWU6IFNldCB1cCBTU0gKICAgICAgICB1c2VzOiBNclNxdWFhcmUvc3NoLXNldHVwLWFjdGlvbkAyZDAyOGI3MGI1ZTM5N2NmODMxNGM2ZWFlYTIyOWE2YzNlMzQ5NzdhICMgdjMuMS4wCiAgICAgICAgd2l0aDoKICAgICAgICAgIGhvc3Q6IGdpdGh1Yi5jb20KICAgICAgICAgIHByaXZhdGUta2V5OiAke3sgc2VjcmV0cy5TU0hfR0lUSFVCX1BQSyB9fQogICAgICAgICAgcHJpdmF0ZS1rZXktbmFtZTogZ2l0aHViLXBwawoKICAgICAgLSBuYW1lOiBCdWlsZCBhbmQgcHVzaAogICAgICAgIHVzZXM6IGRvY2tlci9idWlsZC1wdXNoLWFjdGlvbkB2NgogICAgICAgIHdpdGg6CiAgICAgICAgICBzc2g6IGRlZmF1bHQKICAgICAgICAgIHB1c2g6IHRydWUKICAgICAgICAgIHRhZ3M6IHVzZXIvYXBwOmxhdGVzdA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">ci</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="nt">on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">push</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">docker</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up SSH</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a</span><span class="w"> </span><span class="c"># v3.1.0</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">host</span><span class="p">:</span><span class="w"> </span><span class="l">github.com</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">private-key</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.SSH_GITHUB_PPK }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">private-key-name</span><span class="p">:</span><span class="w"> </span><span class="l">github-ppk</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build and push</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/build-push-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">ssh</span><span class="p">:</span><span class="w"> </span><span class="l">default</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">push</span><span class="p">:</span><span class="w"> </span><span class="kc">true</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">tags</span><span class="p">:</span><span class="w"> </span><span class="l">user/app:latest</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'docker/bake-action' && 'hidden'"
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6Cgpqb2JzOgogIGRvY2tlcjoKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIG5hbWU6IFNldCB1cCBTU0gKICAgICAgICB1c2VzOiBNclNxdWFhcmUvc3NoLXNldHVwLWFjdGlvbkAyZDAyOGI3MGI1ZTM5N2NmODMxNGM2ZWFlYTIyOWE2YzNlMzQ5NzdhICMgdjMuMS4wCiAgICAgICAgd2l0aDoKICAgICAgICAgIGhvc3Q6IGdpdGh1Yi5jb20KICAgICAgICAgIHByaXZhdGUta2V5OiAke3sgc2VjcmV0cy5TU0hfR0lUSFVCX1BQSyB9fQogICAgICAgICAgcHJpdmF0ZS1rZXktbmFtZTogZ2l0aHViLXBwawoKICAgICAgLSBuYW1lOiBCdWlsZAogICAgICAgIHVzZXM6IGRvY2tlci9iYWtlLWFjdGlvbkB2NgogICAgICAgIHdpdGg6CiAgICAgICAgICBzZXQ6IHwKICAgICAgICAgICAgKi5zc2g9ZGVmYXVsdA==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">ci</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="nt">on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">push</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w"></span><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">docker</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up SSH</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a</span><span class="w"> </span><span class="c"># v3.1.0</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">host</span><span class="p">:</span><span class="w"> </span><span class="l">github.com</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">private-key</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.SSH_GITHUB_PPK }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">private-key-name</span><span class="p">:</span><span class="w"> </span><span class="l">github-ppk</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/bake-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">set</span><span class="p">:</span><span class="w"> </span><span class="p">|</span><span class="sd">
</span></span></span><span class="line"><span class="cl"><span class="sd">            *.ssh=default</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


