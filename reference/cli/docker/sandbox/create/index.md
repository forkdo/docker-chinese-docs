# docker sandbox create

**Description:** Create a sandbox for an agent

**Usage:** `docker sandbox create [OPTIONS] AGENT WORKSPACE`












## Description

Create a sandbox with access to a host workspace for an agent.

Available agents are provided as subcommands. Use "create AGENT --help" for agent-specific options.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--load-local-template` |  |  Load a locally built template image into the sandbox (useful for testing local changes)<br> |
| `--name` |  |  Name for the sandbox (default: <agent>-<workdir>, letters, numbers, hyphens, and underscores)<br> |
| `-q`, `--quiet` |  |  Suppress verbose output |
| `-t`, `--template` |  |  Container image to use for the sandbox (default: agent-specific image)<br> |






