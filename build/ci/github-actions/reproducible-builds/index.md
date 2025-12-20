# Reproducible builds with GitHub Actions

`SOURCE_DATE_EPOCH` is a [standardized environment variable][source_date_epoch]
for instructing build tools to produce a reproducible output.
Setting the environment variable for a build makes the timestamps in the
image index, config, and file metadata reflect the specified Unix time.

[source_date_epoch]: https://reproducible-builds.org/docs/source-date-epoch/

To set the environment variable in GitHub Actions,
use the built-in `env` property on the build step.

## Unix epoch timestamps

The following example sets the `SOURCE_DATE_EPOCH` variable to 0, Unix epoch.








<div
  class="tabs"
  
    
      x-data="{ selected: 'docker/build-push-action' }"
    
    @tab-select.window="$event.detail.group === 'action' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'docker/build-push-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'action', name:
          'docker/build-push-action'})"
        
      >
        <code>docker/build-push-action</code>
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'docker/bake-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'action', name:
          'docker/bake-action'})"
        
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6Cgpqb2JzOgogIGRvY2tlcjoKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIG5hbWU6IFNldCB1cCBEb2NrZXIgQnVpbGR4CiAgICAgICAgdXNlczogZG9ja2VyL3NldHVwLWJ1aWxkeC1hY3Rpb25AdjMKCiAgICAgIC0gbmFtZTogQnVpbGQKICAgICAgICB1c2VzOiBkb2NrZXIvYnVpbGQtcHVzaC1hY3Rpb25AdjYKICAgICAgICB3aXRoOgogICAgICAgICAgdGFnczogdXNlci9hcHA6bGF0ZXN0CiAgICAgICAgZW52OgogICAgICAgICAgU09VUkNFX0RBVEVfRVBPQ0g6IDA=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up Docker Buildx</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/setup-buildx-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/build-push-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">tags</span><span class="p">:</span><span class="w"> </span><span class="l">user/app:latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SOURCE_DATE_EPOCH</span><span class="p">:</span><span class="w"> </span><span class="m">0</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6Cgpqb2JzOgogIGRvY2tlcjoKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIG5hbWU6IFNldCB1cCBEb2NrZXIgQnVpbGR4CiAgICAgICAgdXNlczogZG9ja2VyL3NldHVwLWJ1aWxkeC1hY3Rpb25AdjMKCiAgICAgIC0gbmFtZTogQnVpbGQKICAgICAgICB1c2VzOiBkb2NrZXIvYmFrZS1hY3Rpb25AdjYKICAgICAgICBlbnY6CiAgICAgICAgICBTT1VSQ0VfREFURV9FUE9DSDogMA==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up Docker Buildx</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/setup-buildx-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/bake-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SOURCE_DATE_EPOCH</span><span class="p">:</span><span class="w"> </span><span class="m">0</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## Git commit timestamps

The following example sets `SOURCE_DATE_EPOCH` to the Git commit timestamp.








<div
  class="tabs"
  
    
      x-data="{ selected: 'docker/build-push-action' }"
    
    @tab-select.window="$event.detail.group === 'action' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'docker/build-push-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'action', name:
          'docker/build-push-action'})"
        
      >
        <code>docker/build-push-action</code>
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'docker/bake-action' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'action', name:
          'docker/bake-action'})"
        
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6Cgpqb2JzOgogIGRvY2tlcjoKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIG5hbWU6IFNldCB1cCBEb2NrZXIgQnVpbGR4CiAgICAgICAgdXNlczogZG9ja2VyL3NldHVwLWJ1aWxkeC1hY3Rpb25AdjMKCiAgICAgIC0gbmFtZTogR2V0IEdpdCBjb21taXQgdGltZXN0YW1wcwogICAgICAgIHJ1bjogZWNobyAiVElNRVNUQU1QPSQoZ2l0IGxvZyAtMSAtLXByZXR0eT0lY3QpIiA&#43;PiAkR0lUSFVCX0VOVgoKICAgICAgLSBuYW1lOiBCdWlsZAogICAgICAgIHVzZXM6IGRvY2tlci9idWlsZC1wdXNoLWFjdGlvbkB2NgogICAgICAgIHdpdGg6CiAgICAgICAgICB0YWdzOiB1c2VyL2FwcDpsYXRlc3QKICAgICAgICBlbnY6CiAgICAgICAgICBTT1VSQ0VfREFURV9FUE9DSDogJHt7IGVudi5USU1FU1RBTVAgfX0=', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up Docker Buildx</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/setup-buildx-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Get Git commit timestamps</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l">echo &#34;TIMESTAMP=$(git log -1 --pretty=%ct)&#34; &gt;&gt; $GITHUB_ENV</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/build-push-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">tags</span><span class="p">:</span><span class="w"> </span><span class="l">user/app:latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SOURCE_DATE_EPOCH</span><span class="p">:</span><span class="w"> </span><span class="l">${{ env.TIMESTAMP }}</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'bmFtZTogY2kKCm9uOgogIHB1c2g6Cgpqb2JzOgogIGRvY2tlcjoKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIG5hbWU6IFNldCB1cCBEb2NrZXIgQnVpbGR4CiAgICAgICAgdXNlczogZG9ja2VyL3NldHVwLWJ1aWxkeC1hY3Rpb25AdjMKCiAgICAgIC0gbmFtZTogR2V0IEdpdCBjb21taXQgdGltZXN0YW1wcwogICAgICAgIHJ1bjogZWNobyAiVElNRVNUQU1QPSQoZ2l0IGxvZyAtMSAtLXByZXR0eT0lY3QpIiA&#43;PiAkR0lUSFVCX0VOVgoKICAgICAgLSBuYW1lOiBCdWlsZAogICAgICAgIHVzZXM6IGRvY2tlci9iYWtlLWFjdGlvbkB2NgogICAgICAgIGVudjoKICAgICAgICAgIFNPVVJDRV9EQVRFX0VQT0NIOiAke3sgZW52LlRJTUVTVEFNUCB9fQ==', copying: false }"
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
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Set up Docker Buildx</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/setup-buildx-action@v3</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Get Git commit timestamps</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l">echo &#34;TIMESTAMP=$(git log -1 --pretty=%ct)&#34; &gt;&gt; $GITHUB_ENV</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Build</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">docker/bake-action@v6</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SOURCE_DATE_EPOCH</span><span class="p">:</span><span class="w"> </span><span class="l">${{ env.TIMESTAMP }}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## Additional information

For more information about the `SOURCE_DATE_EPOCH` support in BuildKit,
see [BuildKit documentation](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#source_date_epoch).

