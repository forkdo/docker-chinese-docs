# 通过 CLI 进行通用环境集成





您可以通过在 CI 工作流中运行 Docker Scout CLI 客户端来创建通用环境集成。CLI 客户端可在 GitHub 上作为二进制文件获取，也可在 Docker Hub 上作为容器镜像获取。使用该客户端调用 `docker scout environment` 命令，将您的镜像分配给环境。

有关如何使用 `docker scout environment` 命令的更多信息，请参阅 [CLI 参考](/reference/cli/docker/scout/environment.md)。

## 示例

在开始之前，请在您的 CI 系统中设置以下环境变量：

- `DOCKER_SCOUT_HUB_USER`：您的 Docker Hub 用户名
- `DOCKER_SCOUT_HUB_PASSWORD`：您的 Docker Hub 个人访问令牌

确保您的项目可以访问这些变量。








<div
  class="tabs"
  
    x-data="{ selected: 'Circle-CI' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Circle-CI' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Circle-CI'"
        
      >
        Circle CI
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'GitLab' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'GitLab'"
        
      >
        GitLab
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Azure-DevOps' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Azure-DevOps'"
        
      >
        Azure DevOps
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Jenkins' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Jenkins'"
        
      >
        Jenkins
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Circle-CI' && 'hidden'"
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
        x-data="{ code: 'dmVyc2lvbjogMi4xCgpqb2JzOgogIHJlY29yZF9lbnZpcm9ubWVudDoKICAgIG1hY2hpbmU6CiAgICAgIGltYWdlOiB1YnVudHUtMjIwNDpjdXJyZW50CiAgICBpbWFnZTogbmFtZXNwYWNlL3JlcG8KICAgIHN0ZXBzOgogICAgICAtIHJ1bjogfAogICAgICAgICAgaWYgW1sgLXogIiRDSVJDTEVfVEFHIiBdXTsgdGhlbgogICAgICAgICAgICB0YWc9IiRDSVJDTEVfVEFHIgogICAgICAgICAgICBlY2hvICJSdW5uaW5nIHRhZyAnJENJUkNMRV9UQUcnIgogICAgICAgICAgZWxzZQogICAgICAgICAgICB0YWc9IiRDSVJDTEVfQlJBTkNIIgogICAgICAgICAgICBlY2hvICJSdW5uaW5nIG9uIGJyYW5jaCAnJENJX0NPTU1JVF9CUkFOQ0gnIgogICAgICAgICAgZmkgICAgCiAgICAgICAgICBlY2hvICJ0YWcgPSAkdGFnIgogICAgICAtIHJ1bjogZG9ja2VyIHJ1biAtaXQgXAogICAgICAgICAgLWUgRE9DS0VSX1NDT1VUX0hVQl9VU0VSPSRET0NLRVJfU0NPVVRfSFVCX1VTRVIgXAogICAgICAgICAgLWUgRE9DS0VSX1NDT1VUX0hVQl9QQVNTV09SRD0kRE9DS0VSX1NDT1VUX0hVQl9QQVNTV09SRCBcCiAgICAgICAgICBkb2NrZXIvc2NvdXQtY2xpOjEuMC4yIGVudmlyb25tZW50IFwKICAgICAgICAgIC0tb3JnICI8TVlfRE9DS0VSX09SRz4iIFwKICAgICAgICAgICI8RU5WSVJPTk1FTlQ&#43;IiAke2ltYWdlfToke3RhZ30=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">version</span><span class="p">:</span><span class="w"> </span><span class="m">2.1</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">record_environment</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">machine</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-2204:current</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">namespace/repo</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="p">|</span><span class="sd">
</span></span></span><span class="line"><span class="cl"><span class="sd">          if [[ -z &#34;$CIRCLE_TAG&#34; ]]; then
</span></span></span><span class="line"><span class="cl"><span class="sd">            tag=&#34;$CIRCLE_TAG&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">            echo &#34;Running tag &#39;$CIRCLE_TAG&#39;&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">          else
</span></span></span><span class="line"><span class="cl"><span class="sd">            tag=&#34;$CIRCLE_BRANCH&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">            echo &#34;Running on branch &#39;$CI_COMMIT_BRANCH&#39;&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">          fi    
</span></span></span><span class="line"><span class="cl"><span class="sd">          echo &#34;tag = $tag&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l">docker run -it \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span>-<span class="l">e DOCKER_SCOUT_HUB_USER=$DOCKER_SCOUT_HUB_USER \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span>-<span class="l">e DOCKER_SCOUT_HUB_PASSWORD=$DOCKER_SCOUT_HUB_PASSWORD \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="l">docker/scout-cli:1.0.2 environment \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span>--<span class="l">org &#34;&lt;MY_DOCKER_ORG&gt;&#34; \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="s2">&#34;&lt;ENVIRONMENT&gt;&#34;</span><span class="w"> </span><span class="l">${image}:${tag}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'GitLab' && 'hidden'"
      >
        <p>以下示例使用 <a class="link" href="https://docs.gitlab.com/runner/executors/docker.html" rel="noopener">Docker 执行器</a>。</p>
<div
  data-pagefind-ignore
  x-data
  x-ref="root"
  class="group mt-2 mb-4 flex w-full scroll-mt-2 flex-col items-start gap-4 rounded bg-gray-50 p-2 outline outline-1 outline-offset-[-1px] outline-gray-200 dark:bg-gray-900 dark:outline-gray-800"
>
  
  <div class="relative w-full">
    
    
    <div class="syntax-light dark:syntax-dark not-prose w-full">
      <button
        x-data="{ code: 'dmFyaWFibGVzOgogIGltYWdlOiBuYW1lc3BhY2UvcmVwbwoKcmVjb3JkX2Vudmlyb25tZW50OgogIGltYWdlOiBkb2NrZXIvc2NvdXQtY2xpOjEuMC4yCiAgc2NyaXB0OgogICAgLSB8CiAgICAgIGlmIFtbIC16ICIkQ0lfQ09NTUlUX1RBRyIgXV07IHRoZW4KICAgICAgICB0YWc9ImxhdGVzdCIKICAgICAgICBlY2hvICJSdW5uaW5nIHRhZyAnJENJX0NPTU1JVF9UQUcnIgogICAgICBlbHNlCiAgICAgICAgdGFnPSIkQ0lfQ09NTUlUX1JFRl9TTFVHIgogICAgICAgIGVjaG8gIlJ1bm5pbmcgb24gYnJhbmNoICckQ0lfQ09NTUlUX0JSQU5DSCciCiAgICAgIGZpICAgIAogICAgICBlY2hvICJ0YWcgPSAkdGFnIgogICAgLSBlbnZpcm9ubWVudCAtLW9yZyA8TVlfRE9DS0VSX09SRz4gIlBST0RVQ1RJT04iICR7aW1hZ2V9OiR7dGFnfQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">variables</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">namespace/repo</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">record_environment</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="l">docker/scout-cli:1.0.2</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">script</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span>- <span class="p">|</span><span class="sd">
</span></span></span><span class="line"><span class="cl"><span class="sd">      if [[ -z &#34;$CI_COMMIT_TAG&#34; ]]; then
</span></span></span><span class="line"><span class="cl"><span class="sd">        tag=&#34;latest&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">        echo &#34;Running tag &#39;$CI_COMMIT_TAG&#39;&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">      else
</span></span></span><span class="line"><span class="cl"><span class="sd">        tag=&#34;$CI_COMMIT_REF_SLUG&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">        echo &#34;Running on branch &#39;$CI_COMMIT_BRANCH&#39;&#34;
</span></span></span><span class="line"><span class="cl"><span class="sd">      fi    
</span></span></span><span class="line"><span class="cl"><span class="sd">      echo &#34;tag = $tag&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span>- <span class="l">environment --org &lt;MY_DOCKER_ORG&gt; &#34;PRODUCTION&#34; ${image}:${tag}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Azure-DevOps' && 'hidden'"
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
        x-data="{ code: 'dHJpZ2dlcjoKICAtIG1haW4KCnJlc291cmNlczoKICAtIHJlcG86IHNlbGYKCnZhcmlhYmxlczoKICB0YWc6ICIkKEJ1aWxkLkJ1aWxkSWQpIgogIGltYWdlOiAibmFtZXNwYWNlL3JlcG8iCgpzdGFnZXM6CiAgLSBzdGFnZTogRG9ja2VyIFNjb3V0CiAgICBkaXNwbGF5TmFtZTogRG9ja2VyIFNjb3V0IGVudmlyb25tZW50IGludGVncmF0aW9uCiAgICBqb2JzOgogICAgICAtIGpvYjogUmVjb3JkCiAgICAgICAgZGlzcGxheU5hbWU6IFJlY29yZCBlbnZpcm9ubWVudAogICAgICAgIHBvb2w6CiAgICAgICAgICB2bUltYWdlOiB1YnVudHUtbGF0ZXN0CiAgICAgICAgc3RlcHM6CiAgICAgICAgICAtIHRhc2s6IERvY2tlckAyCiAgICAgICAgICAtIHNjcmlwdDogZG9ja2VyIHJ1biAtaXQgXAogICAgICAgICAgICAgIC1lIERPQ0tFUl9TQ09VVF9IVUJfVVNFUj0kRE9DS0VSX1NDT1VUX0hVQl9VU0VSIFwKICAgICAgICAgICAgICAtZSBET0NLRVJfU0NPVVRfSFVCX1BBU1NXT1JEPSRET0NLRVJfU0NPVVRfSFVCX1BBU1NXT1JEIFwKICAgICAgICAgICAgICBkb2NrZXIvc2NvdXQtY2xpOjEuMC4yIGVudmlyb25tZW50IFwKICAgICAgICAgICAgICAtLW9yZyAiPE1ZX0RPQ0tFUl9PUkc&#43;IiBcCiAgICAgICAgICAgICAgIjxFTlZJUk9OTUVOVD4iICQoaW1hZ2UpOiQodGFnKQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">trigger</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span>- <span class="l">main</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">resources</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span>- <span class="nt">repo</span><span class="p">:</span><span class="w"> </span><span class="l">self</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">variables</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">tag</span><span class="p">:</span><span class="w"> </span><span class="s2">&#34;$(Build.BuildId)&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">image</span><span class="p">:</span><span class="w"> </span><span class="s2">&#34;namespace/repo&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">stages</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span>- <span class="nt">stage</span><span class="p">:</span><span class="w"> </span><span class="l">Docker Scout</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">displayName</span><span class="p">:</span><span class="w"> </span><span class="l">Docker Scout environment integration</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">job</span><span class="p">:</span><span class="w"> </span><span class="l">Record</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">displayName</span><span class="p">:</span><span class="w"> </span><span class="l">Record environment</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">pool</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">vmImage</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span>- <span class="nt">task</span><span class="p">:</span><span class="w"> </span><span class="l">Docker@2</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span>- <span class="nt">script</span><span class="p">:</span><span class="w"> </span><span class="l">docker run -it \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">              </span>-<span class="l">e DOCKER_SCOUT_HUB_USER=$DOCKER_SCOUT_HUB_USER \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">              </span>-<span class="l">e DOCKER_SCOUT_HUB_PASSWORD=$DOCKER_SCOUT_HUB_PASSWORD \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">              </span><span class="l">docker/scout-cli:1.0.2 environment \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">              </span>--<span class="l">org &#34;&lt;MY_DOCKER_ORG&gt;&#34; \</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">              </span><span class="s2">&#34;&lt;ENVIRONMENT&gt;&#34;</span><span class="w"> </span><span class="l">$(image):$(tag)</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Jenkins' && 'hidden'"
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
        x-data="{ code: 'c3RhZ2UoJ0FuYWx5emUgaW1hZ2UnKSB7CiAgICBzdGVwcyB7CiAgICAgICAgLy8gSW5zdGFsbCBEb2NrZXIgU2NvdXQKICAgICAgICBzaCAnY3VybCAtc1NmTCBodHRwczovL3Jhdy5naXRodWJ1c2VyY29udGVudC5jb20vZG9ja2VyL3Njb3V0LWNsaS9tYWluL2luc3RhbGwuc2ggfCBzaCAtcyAtLSAtYiAvdXNyL2xvY2FsL2JpbicKICAgICAgICAKICAgICAgICAvLyBMb2cgaW50byBEb2NrZXIgSHViCiAgICAgICAgc2ggJ2VjaG8gJERPQ0tFUl9TQ09VVF9IVUJfUEFTU1dPUkQgfCBkb2NrZXIgbG9naW4gLXUgJERPQ0tFUl9TQ09VVF9IVUJfVVNFUiAtLXBhc3N3b3JkLXN0ZGluJwoKICAgICAgICAvLyBBbmFseXplIGFuZCBmYWlsIG9uIGNyaXRpY2FsIG9yIGhpZ2ggdnVsbmVyYWJpbGl0aWVzCiAgICAgICAgc2ggJ2RvY2tlci1zY291dCBlbnZpcm9ubWVudCAtLW9yZyAiPE1ZX0RPQ0tFUl9PUkc&#43;IiAiPEVOVklST05NRU5UPiIgJElNQUdFX1RBRwogICAgfQp9', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-groovy" data-lang="groovy"><span class="line"><span class="cl"><span class="n">stage</span><span class="o">(</span><span class="s1">&#39;Analyze image&#39;</span><span class="o">)</span> <span class="o">{</span>
</span></span><span class="line"><span class="cl">    <span class="n">steps</span> <span class="o">{</span>
</span></span><span class="line"><span class="cl">        <span class="c1">// Install Docker Scout
</span></span></span><span class="line"><span class="cl">        <span class="n">sh</span> <span class="s1">&#39;curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /usr/local/bin&#39;</span>
</span></span><span class="line"><span class="cl">        
</span></span><span class="line"><span class="cl">        <span class="c1">// Log into Docker Hub
</span></span></span><span class="line"><span class="cl">        <span class="n">sh</span> <span class="s1">&#39;echo $DOCKER_SCOUT_HUB_PASSWORD | docker login -u $DOCKER_SCOUT_HUB_USER --password-stdin&#39;</span>
</span></span><span class="line"><span class="cl">
</span></span><span class="line"><span class="cl">        <span class="c1">// Analyze and fail on critical or high vulnerabilities
</span></span></span><span class="line"><span class="cl">        <span class="n">sh</span> <span class="err">&#39;</span><span class="n">docker</span><span class="o">-</span><span class="n">scout</span> <span class="n">environment</span> <span class="o">--</span><span class="n">org</span> <span class="s2">&#34;&lt;MY_DOCKER_ORG&gt;&#34;</span> <span class="s2">&#34;&lt;ENVIRONMENT&gt;&#34;</span> <span class="n">$IMAGE_TAG</span>
</span></span><span class="line"><span class="cl">    <span class="o">}</span>
</span></span><span class="line"><span class="cl"><span class="o">}</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>

