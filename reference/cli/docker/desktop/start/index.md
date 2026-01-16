---
title: docker desktop start
url: /reference/cli/docker/desktop/start/
parent:
  title: docker desktop (Beta)
  url: /reference/cli/docker/desktop/
breadcrumbs:
  - title: 参考文档
    url: /reference/
  - title: CLI 参考
    url: /reference/cli/
  - title: docker
    url: /reference/cli/docker/
  - title: docker desktop (Beta)
    url: /reference/cli/docker/desktop/
  - title: docker desktop start
    url: /reference/cli/docker/desktop/start/
next:
  title: docker desktop restart
  url: /reference/cli/docker/desktop/restart/
prev:
  title: docker desktop status
  url: /reference/cli/docker/desktop/status/
---

**Description:** Start Docker Desktop

**Usage:** `docker desktop start [OPTIONS]`





  

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
      <p>由于 WinCred 在安全存储凭据方面存在限制，因此在 Windows 上通过 SSH 执行 <code>docker desktop start</code> 时无法正常工作。</p>
    </div>
  </blockquote>












## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-d`, `--detach` |  |  Do not synchronously wait for the requested operation to complete. |
| `--timeout` |  |  Terminate the running command after the specified timeout with a non-zero exit code. A value of zero (the default) or -1 means no timeout. |






