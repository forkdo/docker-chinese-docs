---
description: Docker 已修复的安全漏洞回顾
keywords: Docker, Docker 文档, 安全, 安全非事件
title: Docker 安全非事件
---

本页面列出了 Docker 已修复的安全漏洞，即在这些漏洞被修复之前，Docker 容器中运行的进程从未受到这些漏洞的影响——假设容器在运行时未添加额外权限或未使用 `--privileged` 运行。

下面的列表甚至不是完全详尽的。相反，它只是我们实际注意到的、经过安全审查并公开披露的少数漏洞的样本。在所有可能性中，未报告的漏洞数量远超已报告的漏洞。幸运的是，由于 Docker 通过 apparmor、seccomp 和权限丢弃（dropping capabilities）实现默认安全的方法，它很可能同样能够缓解未知漏洞和已知漏洞。

已缓解的漏洞：

* [CVE-2013-1956](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1956),
[1957](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1957),
[1958](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1958),
[1959](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1959),
[1979](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-1979),
[CVE-2014-4014](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4014),
[5206](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5206),
[5207](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-5207),
[7970](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7970),
[7975](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-7975),
[CVE-2015-2925](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-2925),
[8543](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-8543),
[CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134),
[3135](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3135) 等：
非特权用户命名空间的引入导致未授权用户可利用的攻击面大幅增加，因为这些用户现在可以通过 `mount()` 等系统调用获得以前仅限 root 的访问权限。所有这些 CVE 都是由于引入用户命名空间而导致安全漏洞的例子。Docker 可以使用用户命名空间来设置容器，但随后通过默认的 seccomp 配置禁止容器内进程创建自己的嵌套命名空间，从而使这些漏洞无法被利用。
* [CVE-2014-0181](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0181),
[CVE-2015-3339](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3339)：
这些是需要存在 setuid 二进制文件的漏洞。Docker 通过 `NO_NEW_PRIVS` 进程标志和其他机制在容器内禁用 setuid 二进制文件。
* [CVE-2014-4699](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4699)：
`ptrace()` 中的漏洞可能导致权限提升。Docker 使用 apparmor、seccomp 并丢弃 `CAP_PTRACE` 权限在容器内禁用 `ptrace()`。
三层保护！
* [CVE-2014-9529](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9529)：
一系列精心设计的 `keyctl()` 调用可能导致内核拒绝服务 / 内存损坏。Docker 使用 seccomp 在容器内禁用 `keyctl()`。
* [CVE-2015-3214](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3214),
[4036](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-4036)：这些是常见虚拟化驱动程序中的漏洞，可能允许来宾操作系统用户在主机操作系统上执行代码。利用这些漏洞需要来宾中的虚拟化设备访问权限。Docker 在未使用 `--privileged` 运行时会隐藏对这些设备的直接访问。有趣的是，这些似乎是容器“比虚拟机更安全”的情况，这与通常认为虚拟机“比容器更安全”的观点相悖。
* [CVE-2016-0728](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-0728)：
由精心设计的 `keyctl()` 调用导致的使用后释放可能引发权限提升。Docker 使用默认的 seccomp 配置在容器内禁用 `keyctl()`。
* [CVE-2016-2383](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-2383)：
eBPF（用于表达 seccomp 过滤器等内容的特殊内核 DSL）中的漏洞允许任意读取内核内存。`bpf()` 系统调用在 Docker 容器内被（讽刺的是）seccomp 阻止。
* [CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134),
[4997](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4997),
[4998](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4998)：
`IPT_SO_SET_REPLACE`、`ARPT_SO_SET_REPLACE` 和 `ARPT_SO_SET_REPLACE` 的 setsockopt 中的漏洞导致内存损坏 / 本地权限提升。这些参数被 `CAP_NET_ADMIN` 阻止，而 Docker 默认不允许该权限。


未缓解的漏洞：

* [CVE-2015-3290](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3290),
[5157](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5157)：内核非屏蔽中断处理中的漏洞允许权限提升。可以在 Docker 容器中利用这些漏洞，因为 `modify_ldt()` 系统调用目前未被 seccomp 阻止。
* [CVE-2016-5195](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5195)：
Linux 内核内存子系统在处理私有只读内存映射的写时复制（COW）中断时存在竞态条件，允许未授权的本地用户获得对只读内存的写访问权限。也被称为“脏牛”（dirty COW）。
*部分缓解*：在某些操作系统上，此漏洞通过 seccomp 过滤 `ptrace` 和 `/proc/self/mem` 为只读的事实得到缓解。