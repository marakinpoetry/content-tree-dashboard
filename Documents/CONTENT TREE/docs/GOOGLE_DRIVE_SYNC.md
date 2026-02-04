# Google Drive Sync Setup

Sync the `Content/` folder with corporate Google Drive for team collaboration.

> **Автоматичний синк:** Dashboard на проді оновлюється автоматично кожні 3 години через GitHub Actions. Див. [Dashboard/README.md](../Dashboard/README.md) для деталей.

## Quick Start (After Setup)

```bash
# Two-way sync
make sync

# Get team's changes
make sync-pull

# Push your changes
make sync-push

# Preview changes without syncing
make sync-status
```

---

## Initial Setup

### Step 1: Install rclone

```bash
# Mac
brew install rclone

# Windows
winget install Rclone.Rclone

# Linux
sudo apt install rclone
```

### Step 2: Configure Google Drive

```bash
rclone config
```

Follow prompts:
1. `n` (new remote)
2. Name: `gdrive`
3. Storage: `drive` (Google Drive)
4. Client ID: (press Enter for default)
5. Client Secret: (press Enter for default)
6. Scope: `1` (full access)
7. Root folder ID: (press Enter, or paste Shared Drive ID)
8. Service account: (press Enter)
9. Advanced config: `n`
10. Auto config: `y` (opens browser to authorize)
11. Shared Drive: `y` if using corporate Shared Drive
12. Select your Shared Drive from list
13. Confirm: `y`

### Step 3: Test Connection

```bash
# List folders in your Shared Drive
rclone lsd gdrive:
```

You should see your Google Drive folders listed.

---

## How It Works

```
Your computer                    Google Drive                 Colleague
     │                               │                            │
     │  make sync                    │   make sync                │
     │         │                     │          │                 │
     ▼         ▼                     ▼          ▼                 ▼
┌─────────┐  copy   ┌────────────┐  copy   ┌─────────┐
│ Content │◄───────►│  Content   │◄───────►│ Content │
│ (local) │         │  (cloud)   │         │ (local) │
└─────────┘         └────────────┘         └─────────┘
```

- `--update` flag ensures newer files win
- Google Drive = source of truth for collaboration

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `make sync` | Two-way sync (pull + push) |
| `make sync-pull` | Download team's changes |
| `make sync-push` | Upload your changes |
| `make sync-status` | Preview changes (dry run) |
| `./sync_content.sh help` | Show script help |

### Direct rclone commands

```bash
# Download from Drive
rclone copy gdrive:Content ./Content --update

# Upload to Drive
rclone copy ./Content gdrive:Content --update

# True bi-directional sync
rclone bisync ./Content gdrive:Content

# Dry run (see what would change)
rclone copy gdrive:Content ./Content --dry-run
```

---

## Team Member Setup

Each colleague needs to do this **once** on their computer:

### 1. Install rclone
See Step 1 above.

### 2. Configure Google Drive
```bash
rclone config
```
Connect to the same corporate Shared Drive.

### 3. First Download
```bash
# Create local folder
mkdir -p ~/Documents/CONTENT\ TREE/Content

# Download everything from Google Drive
rclone copy gdrive:Content ~/Documents/CONTENT\ TREE/Content --verbose
```

### 4. Ongoing Workflow
```bash
# Start of work: get latest
rclone copy gdrive:Content ~/Documents/CONTENT\ TREE/Content --update

# End of work: push changes
rclone copy ~/Documents/CONTENT\ TREE/Content gdrive:Content --update
```

---

## Recommended Workflow

1. **Start of day:** `make sync-pull`
2. **Work on content**
3. **End of day:** `make sync-push`

Or just run `make sync` before and after working.

---

## Troubleshooting

### "Remote not found"
Run `rclone config` to set up the `gdrive` remote.

### Permission denied
Make sure you have Contributor access to the Shared Drive.

### Conflicts
If same file edited by multiple people, newer timestamp wins with `--update`.
For true conflict resolution, use `rclone bisync` (advanced).

### View rclone config
```bash
rclone config show
```
