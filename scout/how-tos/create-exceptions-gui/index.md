# 使用 GUI 创建例外

Docker Scout Dashboard 和 Docker Desktop 提供了用户友好的界面，用于为容器镜像中发现的[例外](/manuals/scout/explore/exceptions.md)创建例外。例外可让您确认已接受的风险或解决镜像分析中的误报。

## 先决条件

要在 Docker Scout Dashboard 或 Docker Desktop 中创建例外，您需要一个 Docker 账户，该账户对拥有镜像的 Docker 组织拥有 **Editor** 或 **Owner** 权限。

## 步骤

使用 Docker Scout Dashboard 或 Docker Desktop 为镜像中的漏洞创建例外：








<div
  class="tabs"
  
    x-data="{ selected: 'Docker-Scout-Dashboard' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Scout-Dashboard' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Scout-Dashboard'"
        
      >
        Docker Scout Dashboard
      </button>
    
      <button
        class="tab-item"
        :class="selected === 'Docker-Desktop' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = 'Docker-Desktop'"
        
      >
        Docker Desktop
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Scout-Dashboard' && 'hidden'"
      >
        <ol>
<li>前往 <a class="link" href="https://scout.docker.com/reports/images" rel="noopener">Images 页面</a>。</li>
<li>选择包含您要为其创建例外的漏洞的镜像标签。</li>
<li>打开 <strong>Image layers</strong> 选项卡。</li>
<li>选择包含您要为其创建例外的漏洞的层。</li>
<li>在 <strong>Vulnerabilities</strong> 选项卡中，找到您要为其创建例外的漏洞。漏洞按软件包分组。找到包含您要为其创建例外的漏洞的软件包，然后展开该软件包。</li>
<li>选择漏洞旁边的 <strong>Create exception</strong> 按钮。</li>
</ol>
<p>选择 <strong>Create exception</strong> 按钮会打开 <strong>Create exception</strong> 侧面板。在此面板中，您可以提供例外的详细信息：</p>
<ul>
<li>
<p><strong>Exception type</strong>：例外类型。支持的类型有：</p>
<ul>
<li>
<p><strong>Accepted risk</strong>：由于安全风险极小、修复成本高、依赖上游修复或类似原因，漏洞未被解决。</p>
</li>
<li>
<p><strong>False positive</strong>：漏洞在您的特定用例、配置中不存在安全风险，或者由于已采取的措施阻止了漏洞利用。</p>
<p>如果您选择 <strong>False positive</strong>，则必须提供为什么该漏洞是误报的理由：</p>
</li>
</ul>
</li>
<li>
<p><strong>Additional details</strong>：您想提供的关于该例外的任何其他信息。</p>
</li>
<li>
<p><strong>Scope</strong>：例外的范围。范围可以是：</p>
<ul>
<li><strong>Image</strong>：例外适用于所选镜像。</li>
<li><strong>All images in repository</strong>：例外适用于仓库中的所有镜像。</li>
<li><strong>Specific repository</strong>：例外适用于指定仓库中的所有镜像。</li>
<li><strong>All images in my organization</strong>：例外适用于您组织中的所有镜像。</li>
</ul>
</li>
<li>
<p><strong>Package scope</strong>：例外的范围。软件包范围可以是：</p>
<ul>
<li><strong>Selected package</strong>：例外适用于所选软件包。</li>
<li><strong>Any packages</strong>：例外适用于易受此 CVE 影响的所有软件包。</li>
</ul>
</li>
</ul>
<p>填写完详细信息后，选择 <strong>Create</strong> 按钮以创建例外。</p>
<p>例外现已创建，并计入您所选镜像的分析结果中。该例外也会列在 Docker Scout Dashboard 中 <a class="link" href="https://scout.docker.com/reports/vulnerabilities/exceptions" rel="noopener">Vulnerabilities 页面</a> 的 <strong>Exceptions</strong> 选项卡上。</p>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== 'Docker-Desktop' && 'hidden'"
      >
        <ol>
<li>在 Docker Desktop 中打开 <strong>Images</strong> 视图。</li>
<li>打开 <strong>Hub</strong> 选项卡。</li>
<li>选择包含您要为其创建例外的漏洞的镜像标签。</li>
<li>选择包含您要为其创建例外的漏洞的层。</li>
<li>在 <strong>Vulnerabilities</strong> 选项卡中，找到您要为其创建例外的漏洞。</li>
<li>选择漏洞旁边的 <strong>Create exception</strong> 按钮。</li>
</ol>
<p>选择 <strong>Create exception</strong> 按钮会打开 <strong>Create exception</strong> 侧面板。在此面板中，您可以提供例外的详细信息：</p>
<ul>
<li>
<p><strong>Exception type</strong>：例外类型。支持的类型有：</p>
<ul>
<li>
<p><strong>Accepted risk</strong>：由于安全风险极小、修复成本高、依赖上游修复或类似原因，漏洞未被解决。</p>
</li>
<li>
<p><strong>False positive</strong>：漏洞在您的特定用例、配置中不存在安全风险，或者由于已采取的措施阻止了漏洞利用。</p>
<p>如果您选择 <strong>False positive</strong>，则必须提供为什么该漏洞是误报的理由：</p>
</li>
</ul>
</li>
<li>
<p><strong>Additional details</strong>：您想提供的关于该例外的任何其他信息。</p>
</li>
<li>
<p><strong>Scope</strong>：例外的范围。范围可以是：</p>
<ul>
<li><strong>Image</strong>：例外适用于所选镜像。</li>
<li><strong>All images in repository</strong>：例外适用于仓库中的所有镜像。</li>
<li><strong>Specific repository</strong>：例外适用于指定仓库中的所有镜像。</li>
<li><strong>All images in my organization</strong>：例外适用于您组织中的所有镜像。</li>
</ul>
</li>
<li>
<p><strong>Package scope</strong>：例外的范围。软件包范围可以是：</p>
<ul>
<li><strong>Selected package</strong>：例外适用于所选软件包。</li>
<li><strong>Any packages</strong>：例外适用于易受此 CVE 影响的所有软件包。</li>
</ul>
</li>
</ul>
<p>填写完详细信息后，选择 <strong>Create</strong> 按钮以创建例外。</p>
<p>例外现已创建，并计入您所选镜像的分析结果中。该例外也会列在 Docker Scout Dashboard 中 <a class="link" href="https://scout.docker.com/reports/vulnerabilities/exceptions" rel="noopener">Vulnerabilities 页面</a> 的 <strong>Exceptions</strong> 选项卡上。</p>

      </div>
    
  </div>
</div>

