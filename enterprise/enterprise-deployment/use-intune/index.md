# 使用 Intune 部署





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    

    

    

    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">For:</span>
        <span>Administrators</span>
        
          <span class="icon-svg">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M693-80q-78 0-133-55.5T505-267q0-78 55-133.5T693-456q77 0 132.5 55.5T881-267q0 76-55.5 131.5T693-80ZM160-522v-197q0-19 11-34.5t28-22.5l260-97q11-4 21-4t21 4l260 97q17 7 28 22.5t11 34.5v190q0 14-11 21.5t-24 2.5q-17-5-35.5-8t-36.5-3q-103 0-175.5 73T445-267q0 40 13.5 79t38.5 71q10 13 2.5 26T478-82q-69-20-122-51.5T251-237q-43-60-67-132.5T160-522Zm531 252q26 0 44-19t18-45q0-26-18-44t-44-18q-26 0-45 18t-19 44q0 26 19 45t45 19Zm-1 125q28 0 53-11t43-31q4-5 2.5-11t-6.5-8q-22-10-45-15.5t-47-5.5q-24 0-47 5t-45 16q-5 2-7 8t2 11q18 21 43.5 31.5T690-145Z"/></svg>
          </span>
        
      </div>
    
  </div>



了解如何使用 Microsoft Intune 在 Windows 和 macOS 设备上部署 Docker Desktop。本指南涵盖应用创建、安装程序配置以及分配给用户或设备。








<div
  class="tabs"
  
    x-data="{ selected: 'Windows' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Windows' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Windows'"
        
      >
        Windows
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Mac' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Mac'"
        
      >
        Mac
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Windows' && 'hidden'"
      >
        <ol>
<li>
<p>登录到您的 Intune 管理中心。</p>
</li>
<li>
<p>添加新应用。选择 <strong>Apps</strong>（应用），然后 <strong>Windows</strong>，再选择 <strong>Add</strong>（添加）。</p>
</li>
<li>
<p>对于应用类型，选择 <strong>Windows app (Win32)</strong>。</p>
</li>
<li>
<p>选择 <code>intunewin</code> 包。</p>
</li>
<li>
<p>填写所需详细信息，例如描述、发布者或应用版本，然后选择 <strong>Next</strong>（下一步）。</p>
</li>
<li>
<p>可选：在 <strong>Program</strong>（程序）选项卡上，您可以更新 <strong>Install command</strong>（安装命令）字段以满足您的需求。该字段已预填充 <code>msiexec /i &quot;DockerDesktop.msi&quot; /qn</code>。有关您可以进行的更改示例，请参阅<a class="link" href="/enterprise/enterprise-deployment/msi-install-and-configure/">常见安装场景</a>。</p>


  

  <blockquote
    
    class="admonition admonition-tip admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<mask id="mask0_5432_1749" style="mask-type:alpha" maskUnits="userSpaceOnUse" x="4" y="1" width="17" height="22">
<path d="M9.93896 22H14.939M10.439 10H14.439M12.439 10L12.439 16M15.439 15.3264C17.8039 14.2029 19.439 11.7924 19.439 9C19.439 5.13401 16.305 2 12.439 2C8.57297 2 5.43896 5.13401 5.43896 9C5.43896 11.7924 7.07402 14.2029 9.43896 15.3264V16C9.43896 16.9319 9.43896 17.3978 9.59121 17.7654C9.79419 18.2554 10.1835 18.6448 10.6736 18.8478C11.0411 19 11.5071 19 12.439 19C13.3708 19 13.8368 19 14.2043 18.8478C14.6944 18.6448 15.0837 18.2554 15.2867 17.7654C15.439 17.3978 15.439 16.9319 15.439 16V15.3264Z" stroke="#6C7E9D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</mask>
<g mask="url(#mask0_5432_1749)">
<rect width="24" height="24" fill="currentColor" fill-opacity="0.8"/>
</g>
</svg>

      </span>
      <span class="admonition-title">
        Tip
      </span>
    </div>
    <div class="admonition-content">
      <p>建议您配置 Intune 部署，以便在成功安装后安排计算机重启。</p>
<p>这是因为 Docker Desktop 安装程序会根据您的引擎选择安装 Windows 功能，并且还会更新 <code>docker-users</code> 本地组的成员资格。</p>
<p>您可能还需要设置 Intune 以根据返回代码确定行为，并监视返回代码 <code>3010</code>。返回代码 3010 表示安装成功但需要重启。</p>
    </div>
  </blockquote>

</li>
<li>
<p>完成剩余的选项卡，然后检查并创建应用。</p>
</li>
</ol>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Mac' && 'hidden'"
      >
        <p>首先，上传包：</p>
<ol>
<li>登录到您的 Intune 管理中心。</li>
<li>添加新应用。选择 <strong>Apps</strong>（应用），然后 <strong>macOS</strong>，再选择 <strong>Add</strong>（添加）。</li>
<li>选择 <strong>Line-of-business app</strong>（业务线应用），然后选择 <strong>Select</strong>（选择）。</li>
<li>上传 <code>Docker.pkg</code> 文件并填写所需详细信息。</li>
</ol>
<p>接下来，分配应用：</p>
<ol>
<li>应用添加后，在 Intune 中导航到 <strong>Assignments</strong>（分配）。</li>
<li>选择 <strong>Add group</strong>（添加组）并选择您要将应用分配到的用户或设备组。</li>
<li>选择 <strong>Save</strong>（保存）。</li>
</ol>

      </div>
    
  </div>
</div>


## 其他资源

- [查看常见问题解答](faq.md)。
- 了解如何为您的用户[强制执行登录](/manuals/enterprise/security/enforce-sign-in/_index.md)。
