---
title: Docker Engine prior releases
linkTitle: Prior releases
weight: 100
description: Release notes for Docker CE
keywords: release notes, community
toc_max: 2
aliases:
- /cs-engine/1.12/release-notes/
- /cs-engine/1.12/release-notes/release-notes/
- /cs-engine/1.12/release-notes/prior-release-notes/
- /cs-engine/1.13/release-notes/
- /ee/engine/release-notes/
- /ee/docker-ee/release-notes/
---

## 1.13.1 (2017-02-08)

> [!IMPORTANT]
>
> On Linux distributions where `devicemapper` was the default storage driver, the `overlay2`, or `overlay` is now used by default (if the kernel supports it). To use devicemapper, you can manually configure the storage driver to use through the `--storage-driver` daemon option, or by setting "storage-driver" in the `daemon.json` configuration file.

> [!IMPORTANT]
>
> In Docker 1.13, the managed plugin api changed, as compared to the experimental version introduced in Docker 1.12. You must **uninstall** plugins which you installed with Docker 1.12 _before_ upgrading to Docker 1.13. You can uninstall plugins using the `docker plugin rm` command.

If you have already upgraded to Docker 1.13 without uninstalling
previously-installed plugins, you may see this message when the Docker daemon
starts:

    Error starting daemon: json: cannot unmarshal string into Go value of type types.PluginEnv

To manually remove all plugins and resolve this problem, take the following steps:

1. Remove plugins.json from: `/var/lib/docker/plugins/`.
2. Restart Docker. Verify that the Docker daemon starts with no errors.
3. Reinstall your plugins.

### Contrib

* Do not require a custom build of tini [#28454](https://github.com/docker/docker/pull/28454)
* Upgrade to Go 1.7.5 [#30489](https://github.com/docker/docker/pull/30489)

### Remote API (v1.26) & Client

+ Support secrets in docker stack deploy with compose file [#30144](https://github.com/docker/docker/pull/30144)

### Runtime

* Fix size issue in `docker system df` [#30378](https://github.com/docker/docker/pull/30378)
* Fix error on `docker inspect` when Swarm certificates were expired. [#29246](https://github.com/docker/docker/pull/29246)
* Fix deadlock on v1 plugin with activate error [#30408](https://github.com/docker/docker/pull/30408)
* Fix SELinux regression [#30649](https://github.com/docker/docker/pull/30649)

### Plugins

* Support global scoped network plugins (v2) in swarm mode [#30332](https://github.com/docker/docker/pull/30332)
+ Add `docker plugin upgrade` [#29414](https://github.com/docker/docker/pull/29414)

### Windows

* Fix small regression with old plugins in Windows [#30150](https://github.com/docker/docker/pull/30150)
* Fix warning on Windows [#30730](https://github.com/docker/docker/pull/30730)

## 1.13.0 (2017-01-18)

> [!IMPORTANT]
>
> On Linux distributions where `devicemapper` was the default storage driver, the `overlay2`, or `overlay` is now used by default (if the kernel supports it). To use devicemapper, you can manually configure the storage driver to use through the `--storage-driver` daemon option, or by setting "storage-driver" in the `daemon.json` configuration file.

> [!IMPORTANT]
>
> In Docker 1.13, the managed plugin api changed, as compared to the experimental version introduced in Docker 1.12. You must **uninstall** plugins which you installed with Docker 1.12 _before_ upgrading to Docker 1.13. You can uninstall plugins using the `docker plugin rm` command.

If you have already upgraded to Docker 1.13 without uninstalling
previously-installed plugins, you may see this message when the Docker daemon
starts:

    Error starting daemon: json: cannot unmarshal string into Go value of type types.PluginEnv

To manually remove all plugins and resolve this problem, take the following steps:

1. Remove plugins.json from: `/var/lib/docker/plugins/`.
2. Restart Docker. Verify that the Docker daemon starts with no errors.
3. Reinstall your plugins.

### Builder

+ Add capability to specify images used as a cache source on build. These images do not need to have local parent chain and can be pulled from other registries [#26839](https://github.com/docker/docker/pull/26839)
+ (experimental) Add option to squash image layers to the FROM image after successful builds [#22641](https://github.com/docker/docker/pull/22641)
* Fix dockerfile parser with empty line after escape [#24725](https://github.com/docker/docker/pull/24725)
- Add step number on `docker build` [#24978](https://github.com/docker/docker/pull/24978)
+ Add support for compressing build context during image build [#25837](https://github.com/docker/docker/pull/25837)
+ add `--network` to `docker build` [#27702](https://github.com/docker/docker/pull/27702)
- Fix inconsistent behavior between `--label` flag on `docker build` and `docker run` [#26027](https://github.com/docker/docker/issues/26027)
- Fix image layer inconsistencies when using the overlay storage driver [#27209](https://github.com/docker/docker/pull/27209)
* Unused build-args are now allowed. A warning is presented instead of an error and failed build [#27412](https://github.com/docker/docker/pull/27412)
- Fix builder cache issue on Windows [#27805](https://github.com/docker/docker/pull/27805)
+ Allow `USER` in builder on Windows [#28415](https://github.com/docker/docker/pull/28415)
+ Handle env case-insensitive on Windows [#28725](https://github.com/docker/docker/pull/28725)

### Contrib

+ Add support for building docker debs for Ubuntu 16.04 Xenial on PPC64LE [#23438](https://github.com/docker/docker/pull/23438)
+ Add support for building docker debs for Ubuntu 16.04 Xenial on s390x [#26104](https://github.com/docker/docker/pull/26104)
+ Add support for building docker debs for Ubuntu 16.10 Yakkety Yak on PPC64LE [#28046](https://github.com/docker/docker/pull/28046)
- Add RPM builder for VMWare Photon OS [#24116](https://github.com/docker/docker/pull/24116)
+ Add shell completions to tgz [#27735](https://github.com/docker/docker/pull/27735)
* Update the install script to allow using the mirror in China [#27005](https://github.com/docker/docker/pull/27005)
+ Add DEB builder for Ubuntu 16.10 Yakkety Yak [#27993](https://github.com/docker/docker/pull/27993)
+ Add RPM builder for Fedora 25 [#28222](https://github.com/docker/docker/pull/28222)
+ Add `make deb` support for aarch64 [#27625](https://github.com/docker/docker/pull/27625)

### Distribution

* Update notary dependency to 0.4.2 (full changelogs [here](https://github.com/docker/notary/releases/tag/v0.4.2)) [#27074](https://github.com/docker/docker/pull/27074)
  - Support for compilation on windows [docker/notary#970](https://github.com/docker/notary/pull/970)
  - Improved error messages for client authentication errors [docker/notary#972](https://github.com/docker/notary/pull/972)
  - Support for finding keys that are anywhere in the `~/.docker/trust/private` directory, not just under `~/.docker/trust/private/root_keys` or `~/.docker/trust/private/tuf_keys` [docker/notary#981](https://github.com/docker/notary/pull/981)
  - Previously, on any error updating, the client would fall back on the cache.  Now we only do so if there is a network error or if the server is unavailable or missing the TUF data. Invalid TUF data will cause the update to fail - for example if there was an invalid root rotation. [docker/notary#982](https://github.com/docker/notary/pull/982)
  - Improve root validation and yubikey debug logging [docker/notary#858](https://github.com/docker/notary/pull/858) [docker/notary#891](https://github.com/docker/notary/pull/891)
  - Warn if certificates for root or delegations are near expiry [docker/notary#802](https://github.com/docker/notary/pull/802)
  - Warn if role metadata is near expiry [docker/notary#786](https://github.com/docker/notary/pull/786)
  - Fix passphrase retrieval attempt counting and terminal detection [docker/notary#906](https://github.com/docker/notary/pull/906)
- Avoid unnecessary blob uploads when different users push same layers to authenticated registry [#26564](https://github.com/docker/docker/pull/26564)
* Allow external storage for registry credentials [#26354](https://github.com/docker/docker/pull/26354)

### Logging

* Standardize the default logging tag value in all logging drivers [#22911](https://github.com/docker/docker/pull/22911)
- Improve performance and memory use when logging of long log lines [#22982](https://github.com/docker/docker/pull/22982)
+ Enable syslog driver for windows [#25736](https://github.com/docker/docker/pull/25736)
+ Add Logentries Driver [#27471](https://github.com/docker/docker/pull/27471)
+ Update of AWS log driver to support tags [#27707](https://github.com/docker/docker/pull/27707)
+ Unix socket support for fluentd [#26088](https://github.com/docker/docker/pull/26088)
* Enable fluentd logging driver on Windows [#28189](https://github.com/docker/docker/pull/28189)
- Sanitize docker labels when used as journald field names [#23725](https://github.com/docker/docker/pull/23725)
- Fix an issue where `docker logs --tail` returned less lines than expected [#28203](https://github.com/docker/docker/pull/28203)
- Splunk Logging Driver: performance and reliability improvements [#26207](https://github.com/docker/docker/pull/26207)
- Splunk Logging Driver: configurable formats and skip for verifying connection [#25786](https://github.com/docker/docker/pull/25786)

### Networking

+ Add `--attachable` network support to enable `docker run` to work in swarm-mode overlay network [#25962](https://github.com/docker/docker/pull/25962)
+ Add support for host port PublishMode in services using the `--publish` option in `docker service create` [#27917](https://github.com/docker/docker/pull/27917) and [#28943](https://github.com/docker/docker/pull/28943)
+ Add support for Windows server 2016 overlay network driver (requires upcoming ws2016 update) [#28182](https://github.com/docker/docker/pull/28182)
* Change the default `FORWARD` policy to `DROP` [#28257](https://github.com/docker/docker/pull/28257)
+ Add support for specifying static IP addresses for predefined network on windows [#22208](https://github.com/docker/docker/pull/22208)
- Fix `--publish` flag on `docker run` not working with IPv6 addresses [#27860](https://github.com/docker/docker/pull/27860)
- Fix inspect network show gateway with mask [#25564](https://github.com/docker/docker/pull/25564)
- Fix an issue where multiple addresses in a bridge may cause `--fixed-cidr` to not have the correct addresses [#26659](https://github.com/docker/docker/pull/26659)
+ Add creation timestamp to `docker network inspect` [#26130](https://github.com/docker/docker/pull/26130)
- Show peer nodes in `docker network inspect` for swarm overlay networks [#28078](https://github.com/docker/docker/pull/28078)
- Enable ping for service VIP address [#28019](https://github.com/docker/docker/pull/28019)

### Plugins

- Move plugins out of experimental [#28226](https://github.com/docker/docker/pull/28226)
- Add `--force` on `docker plugin remove` [#25096](https://github.com/docker/docker/pull/25096)
* Add support for dynamically reloading authorization plugins [#22770](https://github.com/docker/docker/pull/22770)
+ Add description in `docker plugin ls` [#25556](https://github.com/docker/docker/pull/25556)
+ Add `-f`/`--format` to `docker plugin inspect` [#25990](https://github.com/docker/docker/pull/25990)
+ Add `docker plugin create` command [#28164](https://github.com/docker/docker/pull/28164)
* Send request's TLS peer certificates to authorization plugins [#27383](https://github.com/docker/docker/pull/27383)
* Support for global-scoped network and ipam plugins in swarm-mode [#27287](https://github.com/docker/docker/pull/27287)
* Split `docker plugin install` into two API call `/privileges` and `/pull` [#28963](https://github.com/docker/docker/pull/28963)

### Remote API (v1.25) & Client

+ Support `docker stack deploy` from a Compose file [#27998](https://github.com/docker/docker/pull/27998)
+ (experimental) Implement checkpoint and restore [#22049](https://github.com/docker/docker/pull/22049)
+ Add `--format` flag to `docker info` [#23808](https://github.com/docker/docker/pull/23808)
* Remove `--name` from `docker volume create` [#23830](https://github.com/docker/docker/pull/23830)
+ Add `docker stack ls` [#23886](https://github.com/docker/docker/pull/23886)
+ Add a new `is-task` ps filter [#24411](https://github.com/docker/docker/pull/24411)
+ Add `--env-file` flag to `docker service create` [#24844](https://github.com/docker/docker/pull/24844)
+ Add `--format` on `docker stats` [#24987](https://github.com/docker/docker/pull/24987)
+ Make `docker node ps` default to `self` in swarm node [#25214](https://github.com/docker/docker/pull/25214)
+ Add `--group` in `docker service create` [#25317](https://github.com/docker/docker/pull/25317)
+ Add `--no-trunc` to service/node/stack ps output [#25337](https://github.com/docker/docker/pull/25337)
+ Add Logs to `ContainerAttachOptions` so go clients can request to retrieve container logs as part of the attach process [#26718](https://github.com/docker/docker/pull/26718)
+ Allow client to talk to an older server [#27745](https://github.com/docker/docker/pull/27745)
* Inform user client-side that a container removal is in progress [#26074](https://github.com/docker/docker/pull/26074)
+ Add `Isolation` to the /info endpoint [#26255](https://github.com/docker/docker/pull/26255)
+ Add `userns` to the /info endpoint [#27840](https://github.com/docker/docker/pull/27840)
- Do not allow more than one mode be requested at once in the services endpoint [#26643](https://github.com/docker/docker/pull/26643)
+ Add capability to /containers/create API to specify mounts in a more granular and safer way [#22373](https://github.com/docker/docker/pull/22373)
+ Add `--format` flag to `network ls` and `volume ls`