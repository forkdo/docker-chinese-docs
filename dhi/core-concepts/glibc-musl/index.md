# Docker Hardened Images 中的 glibc 和 musl 支持

Docker Hardened Images (DHI) 的构建优先考虑安全性，同时不牺牲与更广泛的开源和企业软件生态系统的兼容性。这种兼容性的一个关键方面是对常见 Linux 标准库的支持：`glibc` 和 `musl`。

## glibc 和 musl 是什么？

在运行基于 Linux 的容器时，镜像的 C 库在应用程序与操作系统交互的方式中起着关键作用。大多数现代 Linux 发行版依赖于以下标准 C 库之一：

- `glibc` (GNU C Library)：主流发行版（如 Debian、Ubuntu 和 Red Hat Enterprise Linux）上的标准 C 库。它得到广泛支持，通常被认为是跨语言、框架和企业软件兼容性最佳的选择。

- `musl`：`glibc` 的轻量级替代品，通常用于极简发行版，如 Alpine Linux。虽然它提供了更小的镜像尺寸和性能优势，但 `musl` 并不总是与期望 `glibc` 的软件完全兼容。

## DHI 兼容性

DHI 镜像提供基于 `glibc`（例如 Debian）和基于 `musl`（例如 Alpine）的变体。对于兼容性至关重要的企业应用程序和语言运行时，我们建议使用基于 glibc 的 DHI 镜像。

## 选择 glibc 还是 musl？

Docker Hardened Images 提供基于 glibc (Debian) 和 musl (Alpine) 的变体，让您可以根据工作负载选择最合适的方案。

如果出现以下情况，请选择基于 Debian (`glibc`) 的镜像：

- 您需要与企业工作负载、语言运行时或专有软件具有广泛的兼容性。
- 您正在使用依赖 `glibc` 的原生扩展的生态系统，如 .NET、Java 或 Python。
- 您希望最大限度地减少因库不兼容而导致的运行时错误风险。

如果出现以下情况，请选择基于 Alpine (`musl`) 的镜像：

- 您希望占用空间最小，镜像尺寸更小，受攻击面更小。
- 您正在构建自定义或严格控制的应用程序堆栈，其中依赖项已知且经过测试。
- 您优先考虑启动速度和精简部署，而不是最大兼容性。

如果您不确定，请从基于 Debian 的镜像开始以确保兼容性，并在对应用程序的依赖项有信心后评估 Alpine。
