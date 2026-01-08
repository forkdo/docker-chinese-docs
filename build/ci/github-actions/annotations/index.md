# Add image annotations with GitHub Actions

Annotations let you specify arbitrary metadata for OCI image components, such
as manifests, indexes, and descriptors.

To add annotations when building images with GitHub Actions, use the
[metadata-action] to automatically create OCI-compliant annotations. The
metadata action creates an `annotations` output that you can reference, both
with [build-push-action] and [bake-action].

[metadata-action]: https://github.com/docker/metadata-action#overwrite-labels-and-annotations
[build-push-action]: https://github.com/docker/build-push-action/
[bake-action]: https://github.com/docker/bake-action/








<div
  class="tabs"
  
    x-data="{ selected: 'build-push-action' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'build-push-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'build-push-action'"
        
      >
        build-push-action
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'bake-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'bake-action'"
        
      >
        bake-action
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'build-push-action' && 'hidden'"
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6CgplbnY6CiAgSU1BR0VfTkFNRTogdXNlci9hcHAKCmpvYnM6CiAgZG9ja2VyOgogICAgcnVucy1vbjogdWJ1bnR1LWxhdGVzdAogICAgc3RlcHM6CiAgICAgIC0gbmFtZTogTG9naW4gdG8gRG9ja2VyIEh1YgogICAgICAgIHVzZXM6IGRvY2tlci9sb2dpbi1hY3Rpb25AdjMKICAgICAgICB3aXRoOgogICAgICAgICAgdXNlcm5hbWU6ICR7eyB2YXJzLkRPQ0tFUkhVQl9VU0VSTkFNRSB9fQogICAgICAgICAgcGFzc3dvcmQ6ICR7eyBzZWNyZXRzLkRPQ0tFUkhVQl9UT0tFTiB9fQoKICAgICAgLSBuYW1lOiBTZXQgdXAgRG9ja2VyIEJ1aWxkeAogICAgICAgIHVzZXM6IGRvY2tlci9zZXR1cC1idWlsZHgtYWN0aW9uQHYzCgogICAgICAtIG5hbWU6IEV4dHJhY3QgbWV0YWRhdGEKICAgICAgICBpZDogbWV0YQogICAgICAgIHVzZXM6IGRvY2tlci9tZXRhZGF0YS1hY3Rpb25AdjUKICAgICAgICB3aXRoOgogICAgICAgICAgaW1hZ2VzOiAke3sgZW52LklNQUdFX05BTUUgfX0KCiAgICAgIC0gbmFtZTogQnVpbGQgYW5kIHB1c2gKICAgICAgICB1c2VzOiBkb2NrZXIvYnVpbGQtcHVzaC1hY3Rpb25AdjYKICAgICAgICB3aXRoOgogICAgICAgICAgdGFnczogJHt7IHN0ZXBzLm1ldGEub3V0cHV0cy50YWdzIH19CiAgICAgICAgICBhbm5vdGF0aW9uczogJHt7IHN0ZXBzLm1ldGEub3V0cHV0cy5hbm5vdGF0aW9ucyB9fQogICAgICAgICAgcHVzaDogdHJ1ZQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="nt">on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">push</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">IMAGE_NAME</span><span class="p">:</span><span class="w"> </span><span class="l">user/app</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">docker</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Login to Docker Hub</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/login-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">username</span><span class="p">:</span><span class="w"> </span><span class="l">${{ vars.DOCKERHUB_USERNAME }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">password</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.DOCKERHUB_TOKEN }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up Docker Buildx</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/setup-buildx-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Extract metadata</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">id</span><span class="p">:</span><span class="w"> </span><span class="l">meta</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/metadata-action@v5</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">images</span><span class="p">:</span><span class="w"> </span><span class="l">${{ env.IMAGE_NAME }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build and push</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/build-push-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">tags</span><span class="p">:</span><span class="w"> </span><span class="l">${{ steps.meta.outputs.tags }}</span><span class="w">
</span></span></span><span class="line hl"><span class="cl"><span class="w">          </span><span class="nt">annotations</span><span class="p">:</span><span class="w"> </span><span class="l">${{ steps.meta.outputs.annotations }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">push</span><span class="p">:</span><span class="w"> </span><span class="kc">true</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'bake-action' && 'hidden'"
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6CgplbnY6CiAgSU1BR0VfTkFNRTogdXNlci9hcHAKCmpvYnM6CiAgZG9ja2VyOgogICAgcnVucy1vbjogdWJ1bnR1LWxhdGVzdAogICAgc3RlcHM6CiAgICAgIC0gbmFtZTogTG9naW4gdG8gRG9ja2VyIEh1YgogICAgICAgIHVzZXM6IGRvY2tlci9sb2dpbi1hY3Rpb25AdjMKICAgICAgICB3aXRoOgogICAgICAgICAgdXNlcm5hbWU6ICR7eyB2YXJzLkRPQ0tFUkhVQl9VU0VSTkFNRSB9fQogICAgICAgICAgcGFzc3dvcmQ6ICR7eyBzZWNyZXRzLkRPQ0tFUkhVQl9UT0tFTiB9fQogICAgICAKICAgICAgLSBuYW1lOiBTZXQgdXAgRG9ja2VyIEJ1aWxkeAogICAgICAgIHVzZXM6IGRvY2tlci9zZXR1cC1idWlsZHgtYWN0aW9uQHYzCgogICAgICAtIG5hbWU6IEV4dHJhY3QgbWV0YWRhdGEKICAgICAgICBpZDogbWV0YQogICAgICAgIHVzZXM6IGRvY2tlci9tZXRhZGF0YS1hY3Rpb25AdjUKICAgICAgICB3aXRoOgogICAgICAgICAgaW1hZ2VzOiAke3sgZW52LklNQUdFX05BTUUgfX0KCiAgICAgIC0gbmFtZTogQnVpbGQKICAgICAgICB1c2VzOiBkb2NrZXIvYmFrZS1hY3Rpb25AdjYKICAgICAgICB3aXRoOgogICAgICAgICAgZmlsZXM6IHwKICAgICAgICAgICAgLi9kb2NrZXItYmFrZS5oY2wKICAgICAgICAgICAgY3dkOi8vJHt7IHN0ZXBzLm1ldGEub3V0cHV0cy5iYWtlLWZpbGUtdGFncyB9fQogICAgICAgICAgICBjd2Q6Ly8ke3sgc3RlcHMubWV0YS5vdXRwdXRzLmJha2UtZmlsZS1hbm5vdGF0aW9ucyB9fQogICAgICAgICAgcHVzaDogdHJ1ZQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="nt">on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">push</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">IMAGE_NAME</span><span class="p">:</span><span class="w"> </span><span class="l">user/app</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">docker</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Login to Docker Hub</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/login-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">username</span><span class="p">:</span><span class="w"> </span><span class="l">${{ vars.DOCKERHUB_USERNAME }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">password</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.DOCKERHUB_TOKEN }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up Docker Buildx</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/setup-buildx-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Extract metadata</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">id</span><span class="p">:</span><span class="w"> </span><span class="l">meta</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/metadata-action@v5</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">images</span><span class="p">:</span><span class="w"> </span><span class="l">${{ env.IMAGE_NAME }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/bake-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">files</span><span class="p">:</span><span class="w"> </span><span class="p">|</span><span class="sd">
</span></span></span><span class="line"><span class="cl"><span class="sd">            ./docker-bake.hcl
</span></span></span><span class="line"><span class="cl"><span class="sd">            cwd://${{ steps.meta.outputs.bake-file-tags }}
</span></span></span><span class="line"><span class="cl"><span class="sd">            cwd://${{ steps.meta.outputs.bake-file-annotations }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">push</span><span class="p">:</span><span class="w"> </span><span class="kc">true</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## Configure annotation level

By default, annotations are placed on image manifests. To configure the
[annotation level](../../metadata/annotations.md#specify-annotation-level), set
the `DOCKER_METADATA_ANNOTATIONS_LEVELS` environment variable on the
`metadata-action` step to a comma-separated list of all the levels that you
want to annotate. For example, setting `DOCKER_METADATA_ANNOTATIONS_LEVELS` to
`index` results in annotations on the image index instead of the manifests.

The following example creates annotations on both the image index and
manifests.

```yaml {hl_lines=28}
name: ci

on:
  push:

env:
  IMAGE_NAME: user/app

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

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.IMAGE_NAME }}
        env:
          DOCKER_METADATA_ANNOTATIONS_LEVELS: manifest,index

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          push: true
```

> [!NOTE]
>
> The build must produce the components that you want to annotate. For example,
> to annotate an image index, the build must produce an index. If the build
> produces only a manifest and you specify `index` or `index-descriptor`, the
> build fails.

