# docker mcp secret

**Description:** Manage secrets in the local OS Keychain












## Description

Manage secrets in the local OS Keychain




## Examples

### Pass the secret via STDIN

> echo my-secret-password > pwd.txt
> cat pwd.txt | docker mcp secret set POSTGRES_PASSWORD


## Subcommands

| Command | Description |
|---------|-------------|
| [`docker mcp secret ls`](/reference/cli/docker/mcp/secret/ls/) | List all secrets from the local OS Keychain as well as any active Secrets Engine provider
 |
| [`docker mcp secret rm`](/reference/cli/docker/mcp/secret/rm/) | Remove secrets from the local OS Keychain |
| [`docker mcp secret set`](/reference/cli/docker/mcp/secret/set/) | Set a secret in the local OS Keychain |


