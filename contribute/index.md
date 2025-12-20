# 为 Docker 文档做贡献

我们重视来自 Docker 社区的文档贡献。我们希望尽可能简化您为 Docker 文档做出贡献的流程。

贡献指南可在 `docker/docs` GitHub 仓库的 [CONTRIBUTING.md](https://github.com/docker/docs/blob/main/CONTRIBUTING.md) 文件中找到。请使用以下链接查看我们的风格指南以及如何使用页面模板和组件的说明。


<div
  class="not-prose md:grid-cols-2 lg:grid-cols-3 grid grid-cols-1 gap-4 mb-6"
>
  
  
    
    <div class="card">
  
    <a href="/contribute/style/grammar" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M512-250q50-25 98-37.5T712-300q38 0 78.5 6t69.5 16v-429q-34-17-72-25t-76-8q-54 0-104.5 16.5T512-677v427Zm-30 79q-8 0-14.5-1.5T456-178q-47-29-100-45t-108-16q-37 0-72 9t-70 22q-23 11-44.5-3T40-251v-463q0-15 7-27.5T68-761q42-20 87.5-29.5T248-800q63 0 122.5 17T482-731q51-35 109.5-52T712-800q47 0 92 9.5t87 29.5q14 7 21.5 19.5T920-714v463q0 28-22.5 42.5t-44.5.5q-34-14-69-22.5t-72-8.5q-54 0-106 16t-98 45q-5 4-11.5 5.5T482-171Zm78-437q0-6 4-11.5t9-7.5q30-11 61.5-17t65.5-6q22 0 43 2.5t41 7.5q6 2 11 7.5t5 12.5q0 11-7.5 17t-18.5 3q-17-5-35.5-7.5T700-610q-29 0-56 5.5T591-588q-14 5-22.5-.5T560-608Zm0 220q0-6 4-12t9-8q30-11 61.5-16.5T700-430q22 0 43 2.5t41 7.5q6 2 11 7.5t5 12.5q0 11-7.5 17t-18.5 3q-17-5-35.5-7.5T700-390q-29 0-56 5t-53 16q-14 5-22.5 0t-8.5-19Zm0-110q0-6 4-11.5t9-7.5q30-11 61.5-17t65.5-6q22 0 43 2.5t41 7.5q6 2 11 7.5t5 12.5q0 11-7.5 17t-18.5 3q-17-5-35.5-7.5T700-500q-29 0-56 5.5T591-478q-14 5-22.5-.5T560-498Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">语法与风格</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索 Docker 的语法与风格指南</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/contribute/style/formatting" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M140-120q-24.75 0-42.37-17.63Q80-155.25 80-180v-642q0-5.25 4.5-7.13Q89-831 93-827l54 54 55-56q4.64-5 10.82-5 6.18 0 11.18 5l56 56 56-56q4.64-5 10.82-5 6.18 0 11.18 5l55 56 56-56q4.64-5 10.82-5 6.18 0 11.18 5l56 56 55-56q4.64-5 10.82-5 6.18 0 11.18 5l56 56 56-56q4.64-5 10.82-5 6.18 0 11.18 5l55 56 54-54q4-4 8.5-2.13 4.5 1.88 4.5 7.13v642q0 24.75-17.62 42.37Q844.75-120 820-120H140Zm0-60h310v-280H140v280Zm370 0h310v-110H510v110Zm0-170h310v-110H510v110ZM140-520h680v-120H140v120Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">格式规范</h3>
    </div>
    <div class="card-content">
      <p class="card-description">按照我们文档的其余部分格式化您的内容。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/contribute/style/recommended-words" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m222-299 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-235q-9 9-21 9t-21-9L101-335q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm0-320 158-158q9-9 21-8.5t21.39 9.5q8.61 9 8.61 21t-9 21L243-555q-9 9-21 9t-21-9L101-655q-9-9-9-21t9-21q9-9 21-8.5t21 8.5l79 78Zm328 329q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Zm0-320q-12.75 0-21.37-8.68-8.63-8.67-8.63-21.5 0-12.82 8.63-21.32 8.62-8.5 21.37-8.5h300q12.75 0 21.38 8.68 8.62 8.67 8.62 21.5 0 12.82-8.62 21.32-8.63 8.5-21.38 8.5H550Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">推荐词汇表</h3>
    </div>
    <div class="card-content">
      <p class="card-description">为您的内容选择合适的词汇。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/contribute/file-conventions" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M220-80q-24 0-42-18t-18-42v-680q0-24 18-42t42-18h336q12.44 0 23.72 5T599-862l183 183q8 8 13 19.28 5 11.28 5 23.72v496q0 24-18 42t-42 18H220Zm331-584q0 12.75 8.63 21.37Q568.25-634 581-634h159L551-820v156ZM450-363v99q0 12.75 8.68 21.37 8.67 8.63 21.5 8.63 12.82 0 21.32-8.63 8.5-8.62 8.5-21.37v-99h100q12.75 0 21.38-8.68 8.62-8.67 8.62-21.5 0-12.82-8.62-21.32-8.63-8.5-21.38-8.5H510v-100q0-12.75-8.68-21.38-8.67-8.62-21.5-8.62-12.82 0-21.32 8.62-8.5 8.63-8.5 21.38v100H350q-12.75 0-21.37 8.68-8.63 8.67-8.63 21.5 0 12.82 8.63 21.32 8.62 8.5 21.37 8.5h100Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">源文件约定</h3>
    </div>
    <div class="card-content">
      <p class="card-description">创建新页面的指导原则。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/contribute/style/terminology" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="m563-164 219-219q9-9 21-9t21 9q9 9 9 21t-9 21L605-122q-9 9-20 13t-22 4q-11 0-22-4t-20-13l-96-96q-9-9-9-21t9-21q9-9 21-9t21 9l96 96ZM238-454l-47 123q-3 9-11 14t-17 5q-16 0-24.5-13t-3.5-28l177-466q4-9 11.5-14.5T341-839h24q10 0 17.5 5.5T394-819l176 465q6 15-3 28.5T541-312q-10 0-18-5.5T511-332l-46-122H238Zm19-58h189l-92-254h-5l-92 254Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">术语表</h3>
    </div>
    <div class="card-content">
      <p class="card-description">探索常用的 Docker 术语。</p>
    </div>
  
    </a>
  
</div>

  
    
    <div class="card">
  
    <a href="/contribute/style/voice-tone" class="card-link">
  
    <div class="card-header">
      
      
      <div class="card-icon">
        
          <span class="card-img svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M736.84-70Q724-70 715.5-78.63 707-87.25 707-100q0-6 2.18-12.1 2.18-6.09 5.82-9.9 44-44 69.5-102.5T810-350q0-67.19-25.5-125.6Q759-534 715-578q-3.64-3.8-5.82-9.89-2.18-6.09-2.18-12.18 0-12.93 8.63-21.43 8.62-8.5 21.37-8.5 6 0 11.63 2.62 5.62 2.63 9.37 6.38 52 52 82 121.5t30 149.01q0 80.49-30 149.99Q810-131 758-79q-3.78 3.75-9.44 6.37Q742.89-70 736.84-70ZM623-184q-12.75 0-21.37-8.63Q593-201.25 593-214q0-6 2.63-11.63 2.62-5.62 6.37-9.37 23-23 35.5-52.12 12.5-29.12 12.5-63Q650-384 637.5-413T602-465q-4-4-6.5-9.63-2.5-5.62-2.5-11.62 0-12.75 8.63-21.25 8.62-8.5 21.37-8.5 7 0 12.5 2t9.5 7q30 30 47.5 70.37 17.5 40.36 17.5 86.5 0 46.13-17.5 86.63Q675-223 645-193q-4 5-9.5 7t-12.5 2ZM310-365h-90v29q0 38 23.5 67.5T304-229l12 3q32.8 8.22 36.9 41.11Q357-152 327-135q-50.06 27.95-105.03 40.47Q167-82 110-80q-12 1-21-7.63-9-8.62-9-21.37 0-12.75 8.5-21.38Q97-139 110-140q42-2 82.86-10.32Q233.73-158.64 274-174q-49-24-81.5-66T160-336v-59q0-12.75 8.63-21.38Q177.25-425 190-425h130v-100q0-12.75 8.63-21.38Q337.25-555 350-555h111L331-805q-6-11-1.5-23t15.5-17.5q11-5.5 22.5-2T385-833l130 251q16 30-1.44 58.5T462-495h-82v60q0 28.87-20.56 49.44Q338.88-365 310-365Z"/></svg>
          </span>
        
      </div>
      
      <h3 class="card-title">语态与语气</h3>
    </div>
    <div class="card-content">
      <p class="card-description">了解我们在写作中如何使用语态与语气。</p>
    </div>
  
    </a>
  
</div>

  
</div>


### 其他资源

另请参阅：

- 您可以添加到文档中的实用组件部分。
- 关于 Docker 的[语态与语气](style/voice-tone.md)的信息。
- 一份[写作清单](checklist.md)，帮助您在为 Docker 文档做贡献时参考。

- [源文件规范](https://docs.docker.com/contribute/file-conventions/)

- [内容中的 UI 元素](https://docs.docker.com/contribute/ui/)

- [写作清单](https://docs.docker.com/contribute/checklist/)

- [编写 Docker 使用指南的规范](https://docs.docker.com/contribute/guides/)

