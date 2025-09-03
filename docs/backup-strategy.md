# Backup Strategy

This document outlines the complete backup strategy for the Pirate Audio Mopidy setup.

## 1. GitHub Repository (Public)

**Location**: `https://github.com/your-username/pirate-audio-mopidy-setup`

**Contents**:
- ✅ Installation scripts
- ✅ Python source code
- ✅ SystemD service configurations  
- ✅ Configuration templates (passwords removed)
- ✅ Documentation
- ✅ Boot configuration settings

**What's NOT included**:
- ❌ Audio files (copyright protected)
- ❌ Private passwords/tokens
- ❌ Personal configuration files
- ❌ Virtual environments
- ❌ OS packages/system files

## 2. Audio Files Backup (Private)

**Size**: ~426MB (43 audio files)
**Location**: Separate private backup

### Recommended Backup Methods:

#### Option A: Local External Storage
```bash
# Backup audio files and playlists
rsync -avh ~/media/ /path/to/external/drive/pirate-audio-media-backup/
```

#### Option B: Private Cloud Storage
```bash
# Using rclone with Dropbox/Google Drive/etc
rclone sync ~/media/ dropbox:pirate-audio-backup/media/
```

#### Option C: Network Attached Storage (NAS)
```bash
# Backup to local NAS
scp -r ~/media/ user@nas-ip:/volume1/backups/pirate-audio/
```

## 3. Full System Image (Optional)

For complete system backup including OS and packages:

```bash
# Create SD card image (run on separate computer)
sudo dd if=/dev/sdX of=pirate-audio-complete-backup.img bs=4M status=progress
```

## 4. Restoration Process

### Quick Setup (New Installation):
1. Flash fresh Raspberry Pi OS
2. Clone GitHub repository
3. Run installation scripts
4. Restore audio files from private backup
5. Configure personal settings

### From System Image:
1. Flash complete image to new SD card
2. Boot and update any changed passwords/settings

## 5. Version Control Strategy

### Git Branches:
- `main` - Stable, tested configuration
- `development` - New features and experiments  
- `hotfix/*` - Quick fixes for critical issues

### Release Tags:
- `v1.0` - Initial working setup
- `v1.1` - Button improvements
- `v2.0` - Display enhancements

## 6. Automated Backup Script

Create `backup-audio.sh` for regular backups:

```bash
#!/bin/bash
# Automated audio backup script

BACKUP_DIR="/path/to/backup/location"
SOURCE_DIR="~/media"
DATE=$(date +%Y%m%d)

# Create timestamped backup
rsync -avh "$SOURCE_DIR/" "$BACKUP_DIR/audio-backup-$DATE/"

# Keep only last 30 days of backups
find "$BACKUP_DIR" -name "audio-backup-*" -type d -mtime +30 -exec rm -rf {} \;

echo "Backup completed: $BACKUP_DIR/audio-backup-$DATE/"
```

## 7. Recovery Testing

**Regular testing schedule**:
- Monthly: Test GitHub repository restoration on fresh Pi
- Quarterly: Test complete audio file restoration  
- Yearly: Test full system image restoration

This ensures backups remain functional and up-to-date.