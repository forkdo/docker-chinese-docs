# docker trust signer add

**Description:** Add a signer

**Usage:** `docker trust signer add OPTIONS NAME REPOSITORY [REPOSITORY...] `



<!--
此页面是自动生成自 Docker 的源代码。如果您想
建议更改此处显示的文本，请在 GitHub 上的源代码仓库中
提出工单或拉取请求：

https://github.com/docker/cli
-->








## Description

`docker trust signer add` adds signers to signed repositories.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--key` |  |  Path to the signer's public key file |



## Examples

### Add a signer to a repository

To add a new signer, `alice`, to this repository:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo


List of signers and their keys:

SIGNER              KEYS
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: 642692c14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

Add `alice` with `docker trust signer add`:

```console
$ docker trust signer add alice example/trust-demo --key alice.crt
  Adding signer "alice" to example/trust-demo...
  Enter passphrase for repository key with ID 642692c:
Successfully added signer: alice to example/trust-demo
```

`docker trust inspect --pretty` now lists `alice` as a valid signer:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo


List of signers and their keys:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: 642692c14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```



