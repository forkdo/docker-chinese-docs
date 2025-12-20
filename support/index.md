# 获取 Docker 产品支持

Docker 根据您的订阅级别和需求提供多种支持渠道。

## 付费订阅支持

所有 Docker Pro、Team 和 Business 订阅用户均可获得 Docker 产品的电子邮件支持。

### 支持响应时间

- Docker Pro：3 个工作日内响应
- Docker Team：2 个工作日内响应，24×5 可用性
- Docker Business：1 个工作日内响应，24×5 可用性

> [!NOTE]
>
> Docker Business 订阅用户可额外购买高级支持服务，享受更快的响应时间和 24×7 可用性。

有关详细的支持功能和响应时间，请参阅 [Docker 定价](https://www.docker.com/pricing/)。

### 支持严重性级别

| 级别 | 描述 |
| :--- | :--- |
| 严重 | 影响众多客户或单个组织内所有用户的广泛或全公司范围的服务中断。业务运营已停止，且无可用解决方案。 |
| 高 | 团队或部门级别的影响，阻止重要用户访问核心功能。存在严重的业务影响，且无可用解决方案。 |
| 中等 | 个人用户或小组影响，导致部分功能丧失。业务运营仍在继续，通常有可用解决方案，但生产力降低。 |

### 请求支持

> [!TIP]
>
> 在寻求支持之前，请查看您产品的故障排除文档。

如果您拥有付费 Docker 订阅，请[联系支持团队](https://hub.docker.com/support/contact/)。

## 社区支持

所有 Docker 用户均可通过社区资源寻求支持，Docker 或社区将尽最大努力回应：

- [Docker 社区论坛](https://forums.docker.com/)
- [Docker 社区 Slack](http://dockr.ly/comm-slack)

## Docker Desktop 支持

Docker Desktop 支持仅对付费订阅用户提供。

### 支持范围








<div
  class="tabs"
  
    x-data="{ selected: '%E6%94%AF%E6%8C%81%E8%8C%83%E5%9B%B4' }"
  
  aria-role="tabpanel"
>
  <div aria-role="tablist" class="tablist">
    
      <button
        class="tab-item"
        :class="selected === '%E6%94%AF%E6%8C%81%E8%8C%83%E5%9B%B4' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E6%94%AF%E6%8C%81%E8%8C%83%E5%9B%B4'"
        
      >
        支持范围
      </button>
    
      <button
        class="tab-item"
        :class="selected === '%E4%B8%8D%E6%94%AF%E6%8C%81%E8%8C%83%E5%9B%B4' &&
          'border-blue border-b-4 dark:border-b-blue-600'"
        
          @click="selected = '%E4%B8%8D%E6%94%AF%E6%8C%81%E8%8C%83%E5%9B%B4'"
        
      >
        不支持范围
      </button>
    
  </div>
  <div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E6%94%AF%E6%8C%81%E8%8C%83%E5%9B%B4' && 'hidden'"
      >
        <p>Docker Desktop 支持包括：</p>
<ul>
<li>账户管理和计费</li>
<li>配置和安装问题</li>
<li>桌面更新</li>
<li>登录问题</li>
<li>推送或拉取问题，包括速率限制</li>
<li>应用程序崩溃或意外行为</li>
<li>自动构建</li>
<li>基本产品“如何使用”问题</li>
</ul>
<p><strong>Windows 特定：</strong></p>
<ul>
<li>在 BIOS 中启用虚拟化</li>
<li>启用 Windows 功能</li>
<li>在
    
  
  <a class="link" href="/desktop/setup/vm-vdi/">某些 VM 或 VDI 环境</a>中运行（仅限 Docker Business）</li>
</ul>

      </div>
    
      <div
        aria-role="tab"
        :class="selected !== '%E4%B8%8D%E6%94%AF%E6%8C%81%E8%8C%83%E5%9B%B4' && 'hidden'"
      >
        <p>Docker Desktop 支持不包括：</p>
<ul>
<li>不受支持的操作系统，包括测试版/预览版</li>
<li>使用仿真运行不同架构的容器</li>
<li>Docker Engine、Docker CLI 或其他捆绑的 Linux 组件</li>
<li>Kubernetes</li>
<li>标记为实验性的功能</li>
<li>系统/服务器管理活动</li>
<li>将桌面作为生产运行时</li>
<li>规模部署/多机安装</li>
<li>常规产品维护（数据备份、磁盘空间、日志轮换）</li>
<li>非 Docker 提供的第三方应用程序</li>
<li>修改或更改的 Docker 软件</li>
<li>硬件故障、滥用或不当使用</li>
<li>早于最新版本的版本（Docker Business 除外）</li>
<li>培训、定制和集成</li>
<li>在单台机器上运行多个实例</li>
</ul>


  

  <blockquote
    
    class="admonition admonition-note admonition not-prose">
    <div class="admonition-header">
      <span class="admonition-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

      </span>
      <span class="admonition-title">
        Note
      </span>
    </div>
    <div class="admonition-content">
      <p>仅在 
    
  
  <a class="link" href="/desktop/setup/vm-vdi/">VM 或 VDI 环境中运行 Docker Desktop</a> 的支持仅对 Docker Business 客户提供。</p>
    </div>
  </blockquote>


      </div>
    
  </div>
</div>


### 支持的版本

- Docker Business：最新版本的六个月内的版本（仅对最新版本应用修复）
- Docker Pro 和 Team：仅最新版本

### 机器数量

- Docker Pro：一台机器
- Docker Team：等于订阅席位的机器数量
- Docker Business：无限机器

### 支持的操作系统

- [Mac 系统要求](/manuals/desktop/setup/install/mac-install.md#system-requirements)
- [Windows 系统要求](/manuals/desktop/setup/install/windows-install.md#system-requirements)
- [Linux 系统要求](/manuals/desktop/setup/install/linux/_index.md#system-requirements)

### 社区资源

- [Docker Desktop for Windows](https://github.com/docker/for-win)
- [Docker Desktop for Mac](https://github.com/docker/for-mac)
- [Docker Desktop for Linux](https://github.com/docker/desktop-linux)

### 诊断数据和隐私

上传诊断信息时，诊断包可能包含用户名和 IP 地址等个人数据。诊断包仅可由直接参与诊断问题的 Docker, Inc. 员工访问。

默认情况下，Docker, Inc. 会在 30 天后删除上传的诊断包。您可以通过指定诊断 ID 或您的 GitHub ID 请求删除诊断包。Docker, Inc. 仅使用数据调查特定用户问题，但可能会得出高级（非个人）指标。

有关更多信息，请参阅 [Docker 数据处理协议](https://www.docker.com/legal/data-processing-agreement)。

