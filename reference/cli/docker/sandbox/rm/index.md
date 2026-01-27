# docker sandbox 删除

**Description:** Remove one or more sandboxes

**Usage:** `docker sandbox rm SANDBOX [SANDBOX...]`

**Aliases:** `docker sandbox rm`, `docker sandbox remove`










## Description

Remove one or more sandboxes and all their associated resources.

This command will:
- Check if the sandbox exists
- Remove the sandbox and clean up its associated resources




## Examples

### Remove a sandbox

```console
$ docker sandbox rm abc123def
abc123def
```

### Remove multiple sandboxes

```console
$ docker sandbox rm abc123def def456ghi
abc123def
def456ghi
```

### Remove all sandboxes

```console
$ docker sandbox rm $(docker sandbox ls -q)
```



