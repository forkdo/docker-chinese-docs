# Docker Desktop for Mac Edge release notes

This page contains information about Docker Desktop Edge releases. Edge releases give you early access to our newest features. Note that some of the features may be experimental, and some of them may not ever reach the Stable release.

For Docker Desktop system requirements, see
[What to know before you install](/manuals/desktop/setup/install/mac-install.md#system-requirements).

## Docker Desktop Community 2.5.4
2020-12-07

### Upgrades

- [Docker Engine 20.10.0-rc2](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Go 1.15.6](https://github.com/golang/go/issues?q=milestone%3AGo1.15.6+label%3ACherryPickApproved+)

### Bug fixes and minor changes

- Changed the «Update and quit» menu entry to «Update and restart».
- Fixed the check for updates dialog reporting the build number instead of the version number of a new version.
- Downgraded the kernel to [4.19.121](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.121-2a1dbedf3f998dac347c499808d7c7e029fbc4d3-amd64/images/sha256-4e7d94522be4f25f1fbb626d5a0142cbb6e785f37e437f6fd4285e64a199883a?context=repo) to reduce the CPU usage of hyperkit. Fixes [docker/for-mac#5044](https://github.com/docker/for-mac/issues/5044)
-  Fixed a bug that DNS would return `NXDOMAIN` when a name exists but the type of record was not found. Fixes [docker/for-mac#5020](https://github.com/docker/for-mac/issues/5020). Related to https://gitlab.alpinelinux.org/alpine/aports/-/issues/11879
- Avoid caching bad file sizes and modes when using `osxfs`. Fixes [docker/for-mac#5045](https://github.com/docker/for-mac/issues/5045).

## Docker Desktop Community 2.5.3
2020-11-30

### Upgrades

- [Compose CLI v1.0.3](https://github.com/docker/compose-cli/releases/tag/v1.0.3)

### Bug fixes and minor changes

- Fixed a possible file sharing error where a file may appear to have the wrong size in a container when it is modified on the host. This is a partial fix for [docker/for-mac#4999](https://github.com/docker/for-mac/issues/4999).
- Removed unnecessary log messages which slow down filesystem event injection.

## Docker Desktop Community 2.5.2
2020-11-26

### New

- Use of three digit version number.
- Starting with Docker Desktop 2.5.2, updates will be much smaller as they will be applied using delta patches.

### Bug fixes and minor changes

- Re-enabled the experimental SOCKS proxy. Fixes [docker/for-mac#5048](https://github.com/docker/for-mac/issues/5048).
- Fixed an unexpected EOF error when trying to start a non-existing container with `-v /var/run/docker.sock:`. See [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025).
- Display an error message instead of crashing when the application needs write access on specific directories. See [docker/for-mac#5068](https://github.com/docker/for-mac/issues/5068)

## Docker Desktop Community 2.5.1.0
2020-11-18

This release contains a Kubernetes upgrade. Note that your local Kubernetes cluster will be reset after installing Docker Desktop.

### Upgrades

- [Docker Engine 20.10.0-rc1](https://github.com/docker/docker-ce/blob/master/CHANGELOG.md#20100)
- [Compose CLI v1.0.2](https://github.com/docker/compose-cli/releases/tag/v1.0.2)
- [Snyk v1.424.4](https://github.com/snyk/snyk/releases/tag/v1.424.4)
- [Kubernetes 1.19.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.3)

### Bug fixes and minor changes

- Renamed 'Run Diagnostics' to 'Get support'.
- Fixed an issue that caused Docker Desktop to crash on MacOS 11.0 (Big Sur) when VirtualBox was also installed. See [docker/for-mac#4997](https://github.com/docker/for-mac/issues/4997).
- Removed BlueStacks warning message. Fixes [docker/for-mac#4863](https://github.com/docker/for-mac/issues/4863).
- Made container start faster in cases where shared volumes have lots of files. Fixes [docker/for-mac#4957](https://github.com/docker/for-mac/issues/4957).
- File sharing: fixed changing ownership of read-only files. Fixes [docker/for-mac#4989](https://github.com/docker/for-mac/issues/4989), [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964).
- Fixed an unexpected EOF error when trying to start a non-existing container. See [docker/for-mac#5025](https://github.com/docker/for-mac/issues/5025).

## Docker Desktop Community 2.4.2.0
2020-10-19

### New

- If you have enabled [Vulnerability Scanning](/docker-hub/repos/manage/vulnerability-scanning/) in Docker Hub, the scan results will now appear in Docker Desktop.

### Upgrades

- [Docker Engine 20.10.0 beta1](https://github.com/docker/docker-ce/blob/0fc7084265b3786a5867ec311d3f916af7bf7a23/CHANGELOG.md)
- [Docker Compose CLI - 0.1.22](https://github.com/docker/compose-cli/releases/tag/v0.1.22)
- [Linux kernel 5.4.39](https://hub.docker.com/layers/linuxkit/kernel/5.4.39-f39f83d0d475b274938c86eaa796022bfc7063d2/images/sha256-8614670219aca0bb276d4749e479591b60cd348abc770ac9ecd09ee4c1575405?context=explore).
- [Kubernetes 1.19.2](https://github.com/kubernetes/kubernetes/releases/tag/v1.19.2)
- [Go 1.15.2](https://github.com/golang/go/issues?q=milestone:Go1.15.2+label:CherryPickApproved)

### Bug fixes and minor changes

- When sharing Linux directories (`/var`, `/bin`, etc) with containers, Docker Desktop avoids watching paths in the host file system.
- When sharing a file into a container (e.g. `docker run -v ~/.gitconfig`) Docker Desktop does not watch the parent directory. Fixes [docker/for-mac#4981](https://github.com/docker/for-mac/issues/4981).
- gRPC FUSE: fix `chown` when the file is read-only. Fixes `rabbitmq`, see [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964).
- gRPC FUSE: generate `ATTRIB` inotify events as well as `MODIFY`. Fixes [docker/for-mac#4962](https://github.com/docker/for-mac/issues/4962).
- gRPC FUSE: return `EOPNOTSUPP` from `fallocate` for unsupported modes. Fixes `minio`. See [docker/for-mac#4964](https://github.com/docker/for-mac/issues/4964).
- Fixed an issue related to NFS mounting. See [docker/for-mac#4958](https://github.com/docker/for-mac/issues/4958).
- Always flush file system caches synchronously on container start. See [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943).
- Allow symlinks to point outside of shared volumes. Fixes [docker/for-mac#4862](https://github.com/docker/for-mac/issues/4862).
- Diagnostics: avoid hanging when Kubernetes is in a broken state.
- Fixed automatic start on log in. See [docker/for-mac#4877](https://github.com/docker/for-mac/issues/4877) and [docker/for-mac#4890](https://github.com/docker/for-mac/issues/4890).

## Docker Desktop Community 2.4.1.0
2020-10-01

### Upgrades

- [Docker Compose CLI - 0.1.18](https://github.com/docker/compose-cli)
- [Docker Compose 1.27.4](https://github.com/docker/compose/releases/tag/1.27.4)
- [Snyk v1.399.1](https://github.com/snyk/snyk/releases/tag/v1.399.1)
- [Docker Engine 19.03.13](https://github.com/docker/docker-ce/releases/tag/v19.03.13)

### Bug fixes and minor changes

- Docker Desktop always flushes filesystem caches synchronously on container start. See [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943).
- Docker Desktop now supports `S_ISUID`, `S_ISGID` and `S_ISVTX` in calls to `chmod(2)` on shared filesystems. See [docker/for-mac#4943](https://github.com/docker/for-mac/issues/4943).
- Fixed a possible premature file handle close when using `gRPC-FUSE`.

## Docker Desktop Community 2.3.7.0
2020-09-17

### New

- [Amazon ECR Credential Helper](https://github.com/awslabs/amazon-ecr-credential-helper/releases/tag/v0.4.0)

### Upgrades

- [Docker ACI integration 0.1.15](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.15)
- [Snyk v0.393.0](https://github.com/snyk/snyk/releases/tag/v1.393.0)

### Bug fixes and minor changes

- Fixed automatic start on log in. See [docker/for-mac#4877](https://github.com/docker/for-mac/issues/4877) and [docker/for-mac#4890](https://github.com/docker/for-mac/issues/4890).
- Docker Desktop now allows symlinks to point outside of shared volumes. Fixes [docker/for-mac#4862](https://github.com/docker/for-mac/issues/4862).
- Removed an artificial file descriptor limit (`setrlimit`) of `10240`. Docker Desktop now relies on the kernel to impose limits via `kern.maxfiles` and `kern.maxfilesperproc`.
- Fixed the VM debug shell used for low-level debugging.
- Fixed compatibility with Go 1.15 clients. See [docker/for-mac#4855](https://github.com/docker/for-mac/issues/4855).
- Avoid exposing `/host_mnt` paths in `docker container inspect` and `docker volume inspect`. Fixes [docker/for-mac#4859](https://github.com/docker/for-mac/issues/4859).
- Fixed container logs lagging under heavy load. See [docker/for-win#8216](https://github.com/docker/for-win/issues/8216).

### Known issues

- The `clock_gettime64` system call returns `EPERM` rather than `ENOSYS`
in i386 images. To work around this issue, disable `seccomp` by using
the `--privileged` flag. See [docker/for-win#8326](https://github.com/docker/for-win/issues/8326).

## Docker Desktop Community 2.3.6.1
2020-09-08

### Upgrades

- [Docker Compose 1.27.0](https://github.com/docker/compose/releases/tag/1.27.0)

### Bug fixes and minor changes

-  Docker Desktop now correctly displays the state of "Use gRPC FUSE for file sharing" in the UI. Fixes [docker/for-mac#4864](https://github.com/docker/for-mac/issues/4864).

## Docker Desktop Community 2.3.6.0
2020-09-01

### New

- In partnership with Snyk, Docker Desktop launches vulnerability scanning for Docker local images.
- Docker ECS plugin has been replaced by ECS cloud integration
- Docker UI:
  - The Images view now has search and filter options.
  - You can now push an image to Docker Hub using the Remote repositories drop-down menu.
- WSL 2 files and directories can now be mounted from the Windows Docker CLI with e.g. `docker run -v \\wsl$\Ubuntu\my-files:/my-files ...`.

### Removal

- Support for MacOS 10.13 has ended, you will need to update your system to keep using Docker Desktop.

### Upgrades

- [Alpine 3.12](https://alpinelinux.org/posts/Alpine-3.12.0-released.html)
- [Kubernetes 1.18.8](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.8)

### Bug fixes and minor changes

- Fixed a Mac CPU usage bug by removing the serial console from `hyperkit`, see [docker/roadmap#12]( https://github.com/docker/roadmap/issues/12#issuecomment-663163280). To open a shell in the VM use either `nc -U ~/Library/Containers/com.docker.docker/Data/debug-shell.sock` (on Mac) or `putty -serial \\.\pipe\dockerDebugShell` (on Windows).

## Docker Desktop Community 2.3.5.0
2020-08-21

### New

- The **Images** view on the Dashboard now allows you to interact with images on Docker Hub. You can now pull a remote repository with specific tags from Docker Hub, or view the details of the repository on the Docker Hub page. To access the new Images view, from the Docker menu, select **Dashboard** > **Images**.

- Docker Desktop now enables BuildKit by default after a reset to factory defaults. To revert to the old docker build experience, go to **Preferences** > **Docker Engine** and then disable the BuildKit feature.

- Docker Desktop now uses **gRPC-FUSE** for file sharing by default. This has much faster file sharing and uses much less CPU than `osxfs`, especially when there are lots of file events on the host. To switch back to `osxfs`, go to **Preferences** > **General** and disable gRPC-FUSE.

### Upgrades

- [Go 1.14.7](https://github.com/golang/go/issues?q=milestone:Go1.14.7+label:CherryPickApproved)
- [Docker ECS integration v1.0.0-beta.5](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.5)
- [Docker Engine 19.03.13-beta2](https://github.com/docker/docker-ce/releases/tag/v19.03.13-beta2)
- [Docker ACI integration 0.1.12](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.12)

### Removal

- The Mutagen file sync feature that we have been experimenting with in recent Edge releases has been removed. Thanks to everyone who has provided feedback on this feature. We are reconsidering how to integrate it based on the feedback we have received so far.

### Bug fixes and minor changes

- Moved **Dashboard** to the top of the whale menu.
- Improved the error handling when `dockerd` crashes.
- Fixed minor bugs in the **Images** view.

## Docker Desktop Community 2.3.4.0
2020-07-28

### New

- Docker Desktop introduces the new **Images** view to the Docker Dashboard. The Images view allows users to view a list of Docker images on the disk, run an image as a container, pull the latest version of an image from Docker Hub, inspect images, and remove any unwanted images from the disk.

  To access the new Images view, from the Docker menu, select **Dashboard** > **Images**.

### Upgrades

- [Docker ECS integration v1.0.0-beta.4](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.4)
- [Kubernetes 1.18.6](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.6)

### Bug fixes and minor changes

- Copying the container logs from the dashboard does not copy the ANSI color codes to the clipboard anymore.
- Mutagen two-way sync now uses `.dockersyncignore` rather than `.dockerignore` to exclude files.

## Docker Desktop Community 2.3.3.2
2020-07-21

### Upgrades

- [Docker ECS integration v1.0.0-beta.2](https://github.com/docker/ecs-plugin/releases/tag/v1.0.0-beta.2)
- [Docker ACI integration 0.1.10](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.10)

### Bug fixes and minor changes

- Mutagen uses the `.dockerignore` file when creating a session to filter the list of synchronized files. See [docker/for-mac#4621](https://github.com/docker/for-mac/issues/4621).
- Docker CLI commands can now bypass any active Mutagen synchronization for volumes using `:cached`. See [docker/for-mac#1592](https://github.com/docker/for-mac/issues/1592#issuecomment-651309816).

## Docker Desktop Community 2.3.3.0
2020-07-09

### Upgrades

- Beta release of Docker ECS integration v1.0.0-beta.1
- [Docker ACI integration v0.1.7](https://github.com/docker/aci-integration-beta/releases/tag/v0.1.7)
- [Docker Compose 1.26.2](https://github.com/docker/compose/releases/tag/1.26.2)

### Bug fixes and minor changes

- Compose-on-Kubernetes is no longer included in the Docker Desktop installer. You can download it separately from the compose-on-kubernetes [release page](https://github.com/docker/compose-on-kubernetes/releases).
- Fixed an incompatibility between `hyperkit` and `osquery` which resulted in excessive `hyperkit` CPU usage. See [docker/for-mac#3499](https://github.com/docker/for-mac/issues/3499#issuecomment-639140844)
- Docker Desktop now respects consistency flags `cached`, `delegated`, `consistent` even when in a list of options (for example, `z,delegated`). See [docker/for-mac#4718](https://github.com/docker/for-mac/issues/4718).
- Docker Desktop now implements the shared volume flag `:delegated` by automatically setting up a two-way file sync with Mutagen.

## Docker Desktop Community 2.3.2.0
2020-06-25

### Upgrades

- [Docker 19.03.12](https://github.com/docker/docker-ce/releases/tag/v19.03.12)
- [Docker Compose 1.26.0](https://github.com/docker/compose/releases/tag/1.26.0)
- [Kubernetes 1.18.3](https://github.com/kubernetes/kubernetes/releases/tag/v1.18.3)
- Beta release of the [Docker ACI integration](/engine/context/aci-integration/)

### Bug fixes and minor changes

- Fixed an issue with startup when the Kubernetes certificates have expired. See [docker/for-mac#4594](https://github.com/docker/for-mac/issues/4594).
- Fixed `hyperkit` on newer Macs / newer versions of `Hypervisor.framework`.
- Added support for the global Mutagen config file `~/.mutagen.yml`.
- Automatically set up a two-way file sync using `:delegated` option with `docker run -v` command.
- Re-added device-mapper to the embedded Linux kernel. See [docker/for-mac#4549](https://github.com/docker/for-mac/issues/4549).
- Improved diagnostics when using two-way synchronization with the Mutagen cache.
- Switched to Mutagen `posix-raw` symlink mode which fixes cases where the symlinks point outside the synchronized directory. See [docker/for-mac#4595](https://github.com/docker/for-mac/issues/4595).
- Removed the legacy Kubernetes context `docker-for-desktop`. The context `docker-desktop` should be used instead. See [docker/for-mac#4089](https://github.com/docker/for-mac/issues/4089).

## Docker Desktop Community 2.3.1.0
2020-05-20

### New

Docker Desktop introduces a directory caching mechanism to greatly improve disk performance in containers. This feature uses [mutagen.io](https://mutagen.io/) to sync files between the host and the containers and benefits from native disk performance.

We appreciate you trying out an early version of the Mutagen file sync feature. Please let us know your feedback by creating an issue in the [Docker Desktop for Mac GitHub](https://github.com/docker/for-mac/issues) repository with the `Mutagen` label.

### Upgrades

- [Docker Compose 1.26.0-rc4](https://github.com/docker/compose/releases/tag/1.26.0-rc4)
- Upgrade to Qemu 4.2.0, add Risc-V support

### Bug fixes and minor changes

- Fixed a performance regression when using shared volumes in 2.2.0.5. Fixes [docker/for-mac#4423](https://github.com/docker/for-mac/issues/4423).
- Fixed containers logs in Docker Desktop **Dashboard** which were sometimes truncated. Fixes [docker/for-win#5954](https://github.com/docker/for-win/issues/5954).

## Docker Desktop Community 2.3.0.1
2020-04-28


### Bug fixes and minor changes

- Fixed a bug that caused starting and stopping of a Compose application from the UI to fail when the path contains whitespace.

## Docker Desktop Community 2.3.0.0
2020-04-20


### Upgrades

- [Docker Compose 1.25.5](https://github.com/docker/compose/releases/tag/1.25.5)
- [Go 1.13.10](https://github.com/golang/go/issues?q=milestone%3AGo1.13.10+label%3ACherryPickApproved)
- [Linux kernel 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-ce15f646db9b062dc947cfc0c1deab019fa63f96-amd64/images/sha256-6c252199aee548e4bdc8457e0a068e7d8e81c2649d4c1e26e4150daa253a85d8?context=repo)
- LinuxKit [init](https://hub.docker.com/layers/linuxkit/init/1a80a9907b35b9a808e7868ffb7b0da29ee64a95/images/sha256-64cc8fa50d63940dbaa9979a13c362c89ecb4439bcb3ab22c40d300b9c0b597e?context=explore), [runc](https://hub.docker.com/layers/linuxkit/runc/69b4a35eaa22eba4990ee52cccc8f48f6c08ed03/images/sha256-57e3c7cbd96790990cf87d7b0f30f459ea0b6f9768b03b32a89b832b73546280?context=explore), and [containerd](https://hub.docker.com/layers/linuxkit/containerd/09553963ed9da626c25cf8acdf6d62ec37645412/images/sha256-866be7edb0598430709f88d0e1c6ed7bfd4a397b5ed220e1f793ee9067255ff1?context=explore)

### Bug fixes and minor changes

> Docker Desktop Edge 2.3.0.0 fixes one issue reported on the [docker/for-mac](https://github.com/docker/for-mac/issues) GitHub repository.

- IPv6 has been re-enabled in the embedded Linux kernel, so listening on IPv6 addresses works again. Fixed [docker/for-win#6206](https://github.com/docker/for-win/issues/6206) and [docker/for-mac#4415](https://github.com/docker/for-mac/issues/4415).
- Fixed a bug where containers disappeared from the UI when Kubernetes context is invalid. Fixes [docker/for-win#6037](https://github.com/docker/for-win/issues/6037).
- Fixed a file descriptor leak in `vpnkit-bridge`. Fixes [docker/for-win#5841](https://github.com/docker/for-win/issues/5841).
- Added a link to the Stable channel from the Docker Desktop UI.
- Made the embedded terminal resizable.
- Fixed bug where diagnostic upload would fail if the username contained spaces.

## Docker Desktop Community 2.2.3.0
2020-04-02


### Upgrades

- [Docker 19.03.8](https://github.com/docker/docker-ce/releases/tag/v19.03.8)
- [Docker Compose 1.26.0-rc3](https://github.com/docker/compose/releases/tag/1.26.0-rc3)
- [Linux 4.19.76](https://hub.docker.com/layers/docker/for-desktop-kernel/4.19.76-4e5d9e5f3bde0abf236f97e4a81b029ae0f5f6e7-amd64/images/sha256-11dc0f6ee3187088219ba1463ebb378f5093a7d98f176ddfd62dd6b741c2dd2d?context=repo)

### New

- Docker Desktop introduces a new onboarding tutorial upon first startup. The Quick Start tutorial guides users to get started with Docker in a few easy steps. It includes a simple exercise to build an example Docker image, run it as a container, push and save the image to Docker Hub.

### Bug fixes and minor changes

> Docker Desktop Edge 2.2.3.0 fixes 7 issues reported on the [docker/for-mac](https://github.com/docker/for-mac/issues) GitHub repository.

- Reduced the size of the Docker Desktop installer from 710 MB to 445 MB.
- Removed dangling `/usr/local/bin/docker-machine` symlinks which avoids custom installs of `docker-machine` being accidentally deleted in future upgrades. Note that if you have installed Docker Machine manually, then the install might have followed the symlink and installed Docker Machine in `/Applications/Docker.app`. In this case, you must manually reinstall Docker Machine after installing this version of Docker Desktop. Fixes [docker/for-mac#4208](https://github.com/docker/for-mac/issues/4208).
- Fixed a bug where the Docker UI could be started without the engine.
- Switched from `ahci-hd` to `virtio-blk` to avoid an AHCI deadlock, see [moby/hyperkit#94](https://github.com/moby/hyperkit/issues/94) and [docker/for-mac#1835](https://github.com/docker/for-mac/issues/1835).
- Capturing diagnostics is now faster and easier.
- Fixed an issue where a container port could not be exposed on a specific host IP. See [docker/for-mac#4209](https://github.com/docker/for-mac/issues/4209).
- Kubernetes: Persistent volumes created by claims are now stored in the virtual machine. Fixes [docker/for-win#5665](https://github.com/docker/for-win/issues/5665).
- Removed port probing from dashboard, just unconditionally showing links to ports that should be available. Fixes [docker/for-mac#4264](https://github.com/docker/for-mac/issues/4264).

### Known issues

- Loopback and unspecified IPv6 addresses (`::` and `::1`) within a container do not currently work. Some web servers and other programs may be using these addresses in their configuration files.

## Docker Desktop Community 2.2.2.0
2020-03-02


This release contains a Kubernetes upgrade. Note that your local Kubernetes cluster will be reset after installing Docker Desktop.

### Upgrades

- [Kubernetes 1.16.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.16.5)
- [Go 1.13.8](https://golang.org/doc/devel/release.html#go1.13)

### Bug fixes and minor changes

- Docker Desktop now shares `/var/folders` by default as it stores per-user temporary files and caches.
- Ceph support has been removed from Docker Desktop to save disk space.

## Docker Desktop Community 2.2.1.0
2020-02-12


### Upgrades

- [Docker Compose 1.25.4](https://github.com/docker/compose/releases/tag/1.25.4)
- [Go 1.12.16](https://golang.org/doc/devel/release.html#go1.12)

## Docker Desktop Community 2.1.7.0
2019-12-11


> [!NOTE]
>
> Docker Desktop Edge 2.1.7.0 is the release candidate for the upcoming major Stable release. Please help us test this version before the wider release and report any issues in the [docker/for-mac](https://github.com/docker/for-mac/issues) GitHub repository.

### Upgrades

- [Docker Compose 1.25.1-rc1](https://github.com/docker/compose/releases/tag/1.25.1-rc1)

### Bug fixes and minor changes

- The Docker Desktop Dashboard now displays port information inline with the container status.
- Fixed an issue that caused the 'back' button on the Dashboard UI to behave inconsistently when repeatedly switching between the container details and the Settings window.
- Various minor improvements to the Dashboard UI.
- Fixed an issue that occurs when sharing overlapping directories.
- Fixed a bug that prevented users from changing the location of the VM disk image.
- Docker Desktop does not inject `inotify` events on directories anymore as these can cause mount points to disappear inside containers. Fixes [docker/for-mac#3976](https://github.com/docker/for-mac/issues/3976).
- Fixed an issue that caused Docker Desktop to fail on startup when there is an incomplete Kubernetes config file.
- Fixed an issue where attempts to log into Docker through Docker Desktop could sometimes fail with the `Incorrect authentication credentials` error. Fixes [docker/for-mac#4010](https://github.com/docker/for-mac/issues/4010).

## Docker Desktop Community 2.1.6.0
2019-11-18


### Upgrades

- [Docker 19.03.5](https://github.com/docker/docker-ce/releases/tag/v19.03.5)
- [Go 1.12.13](https://golang.org/doc/devel/release.html#go1.12)

### New

Added the ability to start and stop Compose-based applications and view combined logs in the Docker Desktop **Dashboard** UI.

### Bug fixes and minor changes

- Fixed port forwarding when containers are using `overlay` networks.
- Fixed a container start error when a container has more than one port with an arbitrary or not-yet-configured external port number. For example, `docker run -p 80 -p 443 nginx`. Fixes [docker/for-win#4935](https://github.com/docker/for-win/issues/4935) and [docker/compose#6998](https://github.com/docker/compose/issues/6998).

## Docker Desktop Community 2.1.5.0
2019-11-04


This release contains a Kubernetes upgrade. Note that your local Kubernetes cluster will be reset after installation.

### Upgrades

- [Kubernetes 1.15.5](https://github.com/kubernetes/kubernetes/releases/tag/v1.15.5)
- [Docker Compose 1.25.0-rc4](https://github.com/docker/compose/releases/tag/1.25.0-rc4)
- Linux kernel 4.19.76

### New

**Docker Desktop Dashboard:** The new Docker Desktop **Dashboard** provides a user-friendly interface which enables you to interact with containers and applications, and manage the lifecycle of your applications directly from the UI. In addition, it allows you to access the logs, view container details, and monitor resource utilization to explore the container behavior.

To access the new Dashboard UI, select the Docker menu from the Mac menu bar and then click **Dashboard**.

### Bug fixes and minor changes

Fixed an issue that caused VMs running on older hardware with macOS Catalina to fail on startup with the error `processor does not support desired secondary processor-based controls`.

### Known issues

- When you start a Docker Compose application and then start a Docker App which has the same name as the Compose application, Docker Desktop displays only one application on the Dashboard. However, when you expand the application, containers that belong to both applications are displayed on the Dashboard.

- When you deploy
