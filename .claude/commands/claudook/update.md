# claudook/update

Check for and install Claudook updates.

## Usage
```bash
curl -fsSL https://raw.githubusercontent.com/bacoco/claudook/main/update.sh | bash
```

## What it does:
1. Checks current version against latest release
2. Shows changelog for new version
3. Backs up current configuration
4. Downloads and installs update
5. Migrates configuration to new version
6. Verifies installation

## Options:
- `--check-only` - Only check for updates without installing
- `--force` - Force update even if on latest version
- `--beta` - Include beta versions in update check

## Safety:
- Configuration is preserved across updates
- Automatic rollback on failure
- Creates backup before updating