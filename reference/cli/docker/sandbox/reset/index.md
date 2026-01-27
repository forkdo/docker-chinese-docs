# docker sandbox reset

**Description:** Reset all VM sandboxes and clean up state

**Usage:** `docker sandbox reset [OPTIONS]`












## Description

Reset all VM sandboxes and permanently delete all VM data.

This command will:
- Stop all running VMs gracefully (30s timeout)
- Delete all VM state directories in ~/.docker/sandboxes/vm/
- Clear all internal registries

The daemon will continue running with fresh state after reset.

⚠️  WARNING: This is a destructive operation that cannot be undone!
All running agents will be forcefully terminated and their work will be lost.

By default, you will be prompted to confirm (y/N).
Use --force to skip the confirmation prompt.


## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-f`, `--force` |  |  Skip confirmation prompt |






