# 自定义代码质量检查工作流

现在您已经了解了如何在 E2B 沙箱中使用 GitHub 和 SonarQube 自动化代码质量工作流的基础知识，可以根据需要自定义工作流。

## 重点关注特定质量问题

修改提示词以优先处理某些问题类型：








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
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
        x-data="{ code: 'Y29uc3QgcHJvbXB0ID0gYFVzaW5nIFNvbmFyUXViZSBhbmQgR2l0SHViIE1DUCB0b29sczoKCkZvY3VzIG9ubHkgb246Ci0gU2VjdXJpdHkgdnVsbmVyYWJpbGl0aWVzIChDUklUSUNBTCBwcmlvcml0eSkKLSBCdWdzIChISUdIIHByaW9yaXR5KQotIFNraXAgY29kZSBzbWVsbHMgZm9yIHRoaXMgaXRlcmF0aW9uCgpBbmFseXplICIke3JlcG9QYXRofSIgYW5kIGZpeCB0aGUgaGlnaGVzdCBwcmlvcml0eSBpc3N1ZXMgZmlyc3QuYDs=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span> <span class="sb">`Using SonarQube and GitHub MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">Focus only on:
</span></span></span><span class="line"><span class="cl"><span class="sb">- Security vulnerabilities (CRITICAL priority)
</span></span></span><span class="line"><span class="cl"><span class="sb">- Bugs (HIGH priority)
</span></span></span><span class="line"><span class="cl"><span class="sb">- Skip code smells for this iteration
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">Analyze &#34;</span><span class="si">${</span><span class="nx">repoPath</span><span class="si">}</span><span class="sb">&#34; and fix the highest priority issues first.`</span><span class="p">;</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'cHJvbXB0ID0gZiIiIlVzaW5nIFNvbmFyUXViZSBhbmQgR2l0SHViIE1DUCB0b29sczoKCkZvY3VzIG9ubHkgb246Ci0gU2VjdXJpdHkgdnVsbmVyYWJpbGl0aWVzIChDUklUSUNBTCBwcmlvcml0eSkKLSBCdWdzIChISUdIIHByaW9yaXR5KQotIFNraXAgY29kZSBzbWVsbHMgZm9yIHRoaXMgaXRlcmF0aW9uCgpBbmFseXplICJ7cmVwb19wYXRofSIgYW5kIGZpeCB0aGUgaGlnaGVzdCBwcmlvcml0eSBpc3N1ZXMgZmlyc3QuIiIi', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="n">prompt</span> <span class="o">=</span> <span class="sa">f</span><span class="s2">&#34;&#34;&#34;Using SonarQube and GitHub MCP tools:
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">Focus only on:
</span></span></span><span class="line"><span class="cl"><span class="s2">- Security vulnerabilities (CRITICAL priority)
</span></span></span><span class="line"><span class="cl"><span class="s2">- Bugs (HIGH priority)
</span></span></span><span class="line"><span class="cl"><span class="s2">- Skip code smells for this iteration
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">Analyze &#34;</span><span class="si">{</span><span class="n">repo_path</span><span class="si">}</span><span class="s2">&#34; and fix the highest priority issues first.&#34;&#34;&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 与 CI/CD 集成

将此工作流添加到 GitHub Actions，以便在拉取请求时自动运行：








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
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
        x-data="{ code: 'bmFtZTogQXV0b21hdGVkIHF1YWxpdHkgY2hlY2tzCm9uOgogIHB1bGxfcmVxdWVzdDoKICAgIHR5cGVzOiBbb3BlbmVkLCBzeW5jaHJvbml6ZV0KCmpvYnM6CiAgcXVhbGl0eToKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIHVzZXM6IGFjdGlvbnMvY2hlY2tvdXRAdjQKICAgICAgLSB1c2VzOiBhY3Rpb25zL3NldHVwLW5vZGVAdjQKICAgICAgICB3aXRoOgogICAgICAgICAgbm9kZS12ZXJzaW9uOiAiMTgiCiAgICAgIC0gcnVuOiBucG0gaW5zdGFsbAogICAgICAtIHJ1bjogbnB4IHRzeCAwNi1xdWFsaXR5LWdhdGVkLXByLnRzCiAgICAgICAgZW52OgogICAgICAgICAgRTJCX0FQSV9LRVk6ICR7eyBzZWNyZXRzLkUyQl9BUElfS0VZIH19CiAgICAgICAgICBBTlRIUk9QSUNfQVBJX0tFWTogJHt7IHNlY3JldHMuQU5USFJPUElDX0FQSV9LRVkgfX0KICAgICAgICAgIEdJVEhVQl9UT0tFTjogJHt7IHNlY3JldHMuR0lUSFVCX1RPS0VOIH19CiAgICAgICAgICBTT05BUlFVQkVfVE9LRU46ICR7eyBzZWNyZXRzLlNPTkFSUVVCRV9UT0tFTiB9fQogICAgICAgICAgR0lUSFVCX09XTkVSOiAke3sgZ2l0aHViLnJlcG9zaXRvcnlfb3duZXIgfX0KICAgICAgICAgIEdJVEhVQl9SRVBPOiAke3sgZ2l0aHViLmV2ZW50LnJlcG9zaXRvcnkubmFtZSB9fQogICAgICAgICAgU09OQVJRVUJFX09SRzogeW91ci1vcmcta2V5', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Automated quality checks</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">pull_request</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">types</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="l">opened, synchronize]</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">quality</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">actions/checkout@v4</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">actions/setup-node@v4</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">node-version</span><span class="p">:</span><span class="w"> </span><span class="s2">&#34;18&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l">npm install</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l">npx tsx 06-quality-gated-pr.ts</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">E2B_API_KEY</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.E2B_API_KEY }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">ANTHROPIC_API_KEY</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.ANTHROPIC_API_KEY }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">GITHUB_TOKEN</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.GITHUB_TOKEN }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SONARQUBE_TOKEN</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.SONARQUBE_TOKEN }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">GITHUB_OWNER</span><span class="p">:</span><span class="w"> </span><span class="l">${{ github.repository_owner }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">GITHUB_REPO</span><span class="p">:</span><span class="w"> </span><span class="l">${{ github.event.repository.name }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SONARQUBE_ORG</span><span class="p">:</span><span class="w"> </span><span class="l">your-org-key</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'bmFtZTogQXV0b21hdGVkIHF1YWxpdHkgY2hlY2tzCm9uOgogIHB1bGxfcmVxdWVzdDoKICAgIHR5cGVzOiBbb3BlbmVkLCBzeW5jaHJvbml6ZV0KCmpvYnM6CiAgcXVhbGl0eToKICAgIHJ1bnMtb246IHVidW50dS1sYXRlc3QKICAgIHN0ZXBzOgogICAgICAtIHVzZXM6IGFjdGlvbnMvY2hlY2tvdXRAdjQKICAgICAgLSB1c2VzOiBhY3Rpb25zL3NldHVwLXB5dGhvbkB2NQogICAgICAgIHdpdGg6CiAgICAgICAgICBweXRob24tdmVyc2lvbjogIjMuOCIKICAgICAgLSBydW46IHBpcCBpbnN0YWxsIGUyYiBweXRob24tZG90ZW52CiAgICAgIC0gcnVuOiBweXRob24gMDZfcXVhbGl0eV9nYXRlZF9wci5weQogICAgICAgIGVudjoKICAgICAgICAgIEUyQl9BUElfS0VZOiAke3sgc2VjcmV0cy5FMkJfQVBJX0tFWSB9fQogICAgICAgICAgQU5USFJPUElDX0FQSV9LRVk6ICR7eyBzZWNyZXRzLkFOVEhST1BJQ19BUElfS0VZIH19CiAgICAgICAgICBHSVRIVUJfVE9LRU46ICR7eyBzZWNyZXRzLkdJVEhVQl9UT0tFTiB9fQogICAgICAgICAgU09OQVJRVUJFX1RPS0VOOiAke3sgc2VjcmV0cy5TT05BUlFVQkVfVE9LRU4gfX0KICAgICAgICAgIEdJVEhVQl9PV05FUjogJHt7IGdpdGh1Yi5yZXBvc2l0b3J5X293bmVyIH19CiAgICAgICAgICBHSVRIVUJfUkVQTzogJHt7IGdpdGh1Yi5ldmVudC5yZXBvc2l0b3J5Lm5hbWUgfX0KICAgICAgICAgIFNPTkFSUVVCRV9PUkc6IHlvdXItb3JnLWtleQ==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-yaml" data-lang="yaml"><span class="line"><span class="cl"><span class="nt">name</span><span class="p">:</span><span class="w"> </span><span class="l">Automated quality checks</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">on</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">pull_request</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">types</span><span class="p">:</span><span class="w"> </span><span class="p">[</span><span class="l">opened, synchronize]</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="nt">jobs</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">  </span><span class="nt">quality</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">runs-on</span><span class="p">:</span><span class="w"> </span><span class="l">ubuntu-latest</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">    </span><span class="nt">steps</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">actions/checkout@v4</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">uses</span><span class="p">:</span><span class="w"> </span><span class="l">actions/setup-python@v5</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">with</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">python-version</span><span class="p">:</span><span class="w"> </span><span class="s2">&#34;3.8&#34;</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l">pip install e2b python-dotenv</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">      </span>- <span class="nt">run</span><span class="p">:</span><span class="w"> </span><span class="l">python 06_quality_gated_pr.py</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">        </span><span class="nt">env</span><span class="p">:</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">E2B_API_KEY</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.E2B_API_KEY }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">ANTHROPIC_API_KEY</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.ANTHROPIC_API_KEY }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">GITHUB_TOKEN</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.GITHUB_TOKEN }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SONARQUBE_TOKEN</span><span class="p">:</span><span class="w"> </span><span class="l">${{ secrets.SONARQUBE_TOKEN }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">GITHUB_OWNER</span><span class="p">:</span><span class="w"> </span><span class="l">${{ github.repository_owner }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">GITHUB_REPO</span><span class="p">:</span><span class="w"> </span><span class="l">${{ github.event.repository.name }}</span><span class="w">
</span></span></span><span class="line"><span class="cl"><span class="w">          </span><span class="nt">SONARQUBE_ORG</span><span class="p">:</span><span class="w"> </span><span class="l">your-org-key</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 按文件模式过滤

针对代码库的特定部分：








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
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
        x-data="{ code: 'Y29uc3QgcHJvbXB0ID0gYEFuYWx5emUgY29kZSBxdWFsaXR5IGJ1dCBvbmx5IGNvbnNpZGVyOgotIEZpbGVzIGluIHNyYy8qKi8qLmpzCi0gRXhjbHVkZSB0ZXN0IGZpbGVzICgqLnRlc3QuanMsICouc3BlYy5qcykKLSBFeGNsdWRlIGJ1aWxkIGFydGlmYWN0cyBpbiBkaXN0LwoKRm9jdXMgb24gcHJvZHVjdGlvbiBjb2RlIG9ubHkuYDs=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span> <span class="sb">`Analyze code quality but only consider:
</span></span></span><span class="line"><span class="cl"><span class="sb">- Files in src/**/*.js
</span></span></span><span class="line"><span class="cl"><span class="sb">- Exclude test files (*.test.js, *.spec.js)
</span></span></span><span class="line"><span class="cl"><span class="sb">- Exclude build artifacts in dist/
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">Focus on production code only.`</span><span class="p">;</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'cHJvbXB0ID0gIiIiQW5hbHl6ZSBjb2RlIHF1YWxpdHkgYnV0IG9ubHkgY29uc2lkZXI6Ci0gRmlsZXMgaW4gc3JjLyoqLyouanMKLSBFeGNsdWRlIHRlc3QgZmlsZXMgKCoudGVzdC5qcywgKi5zcGVjLmpzKQotIEV4Y2x1ZGUgYnVpbGQgYXJ0aWZhY3RzIGluIGRpc3QvCgpGb2N1cyBvbiBwcm9kdWN0aW9uIGNvZGUgb25seS4iIiI=', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="n">prompt</span> <span class="o">=</span> <span class="s2">&#34;&#34;&#34;Analyze code quality but only consider:
</span></span></span><span class="line"><span class="cl"><span class="s2">- Files in src/**/*.js
</span></span></span><span class="line"><span class="cl"><span class="s2">- Exclude test files (*.test.js, *.spec.js)
</span></span></span><span class="line"><span class="cl"><span class="s2">- Exclude build artifacts in dist/
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">Focus on production code only.&#34;&#34;&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 设置质量阈值

定义何时应创建 PR：








<div
  class="tabs"
  
    
      x-data="{ selected: 'TypeScript' }"
    
    @tab-select.window="$event.detail.group === 'language' ? selected =
    $event.detail.name : null"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'TypeScript' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'TypeScript'})"
        
      >
        TypeScript
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Python' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="$dispatch('tab-select', { group: 'language', name:
          'Python'})"
        
      >
        Python
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'TypeScript' && 'hidden'"
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
        x-data="{ code: 'Y29uc3QgcHJvbXB0ID0gYFF1YWxpdHkgZ2F0ZSB0aHJlc2hvbGRzOgotIE9ubHkgY3JlYXRlIFBSIGlmOgogICogQnVnIGNvdW50IGRlY3JlYXNlcyBieSBhdCBsZWFzdCAxCiAgKiBObyBuZXcgc2VjdXJpdHkgdnVsbmVyYWJpbGl0aWVzIGludHJvZHVjZWQKICAqIENvZGUgY292ZXJhZ2UgZG9lcyBub3QgZGVjcmVhc2UKICAqIFRlY2huaWNhbCBkZWJ0IHJlZHVjZXMgYnkgYXQgbGVhc3QgMTUgbWludXRlcwoKSWYgY2hhbmdlcyBkbyBub3QgbWVldCB0aGVzZSB0aHJlc2hvbGRzLCBleHBsYWluIHdoeSBhbmQgc2tpcCBQUiBjcmVhdGlvbi5gOw==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-typescript" data-lang="typescript"><span class="line"><span class="cl"><span class="kr">const</span> <span class="nx">prompt</span> <span class="o">=</span> <span class="sb">`Quality gate thresholds:
</span></span></span><span class="line"><span class="cl"><span class="sb">- Only create PR if:
</span></span></span><span class="line"><span class="cl"><span class="sb">  * Bug count decreases by at least 1
</span></span></span><span class="line"><span class="cl"><span class="sb">  * No new security vulnerabilities introduced
</span></span></span><span class="line"><span class="cl"><span class="sb">  * Code coverage does not decrease
</span></span></span><span class="line"><span class="cl"><span class="sb">  * Technical debt reduces by at least 15 minutes
</span></span></span><span class="line"><span class="cl"><span class="sb">
</span></span></span><span class="line"><span class="cl"><span class="sb">If changes do not meet these thresholds, explain why and skip PR creation.`</span><span class="p">;</span></span></span></code></pre></div>
      
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
        x-data="{ code: 'cHJvbXB0ID0gIiIiUXVhbGl0eSBnYXRlIHRocmVzaG9sZHM6Ci0gT25seSBjcmVhdGUgUFIgaWY6CiAgKiBCdWcgY291bnQgZGVjcmVhc2VzIGJ5IGF0IGxlYXN0IDEKICAqIE5vIG5ldyBzZWN1cml0eSB2dWxuZXJhYmlsaXRpZXMgaW50cm9kdWNlZAogICogQ29kZSBjb3ZlcmFnZSBkb2VzIG5vdCBkZWNyZWFzZQogICogVGVjaG5pY2FsIGRlYnQgcmVkdWNlcyBieSBhdCBsZWFzdCAxNSBtaW51dGVzCgpJZiBjaGFuZ2VzIGRvIG5vdCBtZWV0IHRoZXNlIHRocmVzaG9sZHMsIGV4cGxhaW4gd2h5IGFuZCBza2lwIFBSIGNyZWF0aW9uLiIiIg==', copying: false }"
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
      
        <div class="highlight"><pre tabindex="0" class="chroma"><code class="language-python" data-lang="python"><span class="line"><span class="cl"><span class="n">prompt</span> <span class="o">=</span> <span class="s2">&#34;&#34;&#34;Quality gate thresholds:
</span></span></span><span class="line"><span class="cl"><span class="s2">- Only create PR if:
</span></span></span><span class="line"><span class="cl"><span class="s2">  * Bug count decreases by at least 1
</span></span></span><span class="line"><span class="cl"><span class="s2">  * No new security vulnerabilities introduced
</span></span></span><span class="line"><span class="cl"><span class="s2">  * Code coverage does not decrease
</span></span></span><span class="line"><span class="cl"><span class="s2">  * Technical debt reduces by at least 15 minutes
</span></span></span><span class="line"><span class="cl"><span class="s2">
</span></span></span><span class="line"><span class="cl"><span class="s2">If changes do not meet these thresholds, explain why and skip PR creation.&#34;&#34;&#34;</span></span></span></code></pre></div>
      
    </div>
  </div>
</div>

      </div>
    
  </div>
</div>


## 后续步骤

了解如何排查常见问题。
