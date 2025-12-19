---
description: Docker 缓解的安全漏洞回顾
keywords: Docker, Docker documentation, security, security non-events
title: Docker 安全非事件
---

本页面列出了 Docker 已缓解的安全漏洞，即使在漏洞修复之前，运行在 Docker 容器中的进程也不会受到这些漏洞的影响。此结论的前提是容器在运行时未添加额外能力（capabilities）或未以 `--privileged` 模式运行。

以下列表远非完整。它仅是我们注意到的、已引发安全审查并公开披露的少数漏洞样本。很可能，未被报告的漏洞数量远超已报告的。幸运的是，由于 Docker 通过 apparmor、seccomp 和丢弃能力（capabilities）实现默认安全，它很可能能同样有效地缓解未知漏洞和已知漏洞。

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
[3135](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3135), 等等：
非特权用户命名空间的引入，通过授予此类用户对以前仅限 root 使用的系统调用（如 `mount()`）的合法访问权限，极大地增加了非特权用户的攻击面。所有这些 CVE 都是因引入用户命名空间而导致安全漏洞的示例。Docker 可以使用用户命名空间来设置容器，但随后通过默认的 seccomp 配置文件，禁止容器内的进程创建自己的嵌套命名空间，从而使这些漏洞无法被利用。
* [CVE-2014-0181](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0181),
[CVE-2015-3339](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3339)：
这些漏洞需要存在 setuid 二进制文件。Docker 通过 `NO_NEW_PRIVS` 进程标志和其他机制禁用容器内的 setuid 二进制文件。
* [CVE-2014-4699](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-4699)：
`ptrace()` 中的一个漏洞可能允许提权。Docker 使用 apparmor、seccomp 并通过丢弃 `CAP_PTRACE` 来禁用容器内的 `ptrace()`。这里有三层保护！
* [CVE-2014-9529](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-9529)：
一系列精心构造的 `keyctl()` 调用可能导致内核 DoS 或内存损坏。Docker 使用 seccomp 禁用容器内的 `keyctl()`。
* [CVE-2015-3214](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3214),
[4036](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-4036)：这些是常见虚拟化驱动程序中的漏洞，可能允许客户操作系统用户在主机操作系统上执行代码。利用它们需要访问客户机中的虚拟化设备。Docker 在不使用 `--privileged` 运行时会隐藏对这些设备的直接访问。有趣的是，在这些情况下，容器似乎比虚拟机“更安全”，这与虚拟机比容器“更安全”的普遍认知相悖。
* [CVE-2016-0728](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-0728)：
由精心构造的 `keyctl()` 调用引起的释放后重用（Use-after-free）可能导致提权。Docker 使用默认的 seccomp 配置文件禁用容器内的 `keyctl()`。
* [CVE-2016-2383](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-2383)：
eBPF（一种用于表达 seccomp 过滤器等的特殊内核内 DSL）中的一个漏洞允许任意读取内核内存。`bpf()` 系统调用在 Docker 容器内被（具有讽刺意味地）使用 seccomp 阻止。
* [CVE-2016-3134](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-3134),
[4997](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4997),
[4998](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-4998)：
`setsockopt` 中关于 `IPT_SO_SET_REPLACE`、`ARPT_SO_SET_REPLACE` 和 `ARPT_SO_SET_REPLACE` 的一个漏洞导致内存损坏/本地提权。这些参数被 `CAP_NET_ADMIN` 阻止，而 Docker 默认不允许此能力。

未缓解的漏洞：

* [CVE-2015-3290](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3290),
[5157](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-5157)：内核的不可屏蔽中断处理中的漏洞允许提权。可以在 Docker 容器中被利用，因为 `modify_ldt()` 系统调用目前未使用 seccomp 阻止。
* [CVE-2016-5195](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2016-5195)：
在 Linux 内存子系统处理私有只读内存映射的写时复制（COW）破坏时发现了一个竞争条件，这允许非特权本地用户获得对只读内存的写访问权限。也称为 "dirty COW"。
*部分缓解：* 在某些操作系统上，通过 `ptrace` 的 seccomp 过滤和 `/proc/self/mem` 为只读这一事实的组合，可以缓解此漏洞。