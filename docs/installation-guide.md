# Installation Guide

This guide provides detailed instructions for setting up the Pirate Audio Mopidy system from scratch.

## Prerequisites

- Fresh Raspberry Pi OS Bookworm installation
- Pimoroni Pirate Audio HAT properly connected
- Internet connection for downloading packages
- Audio files ready to transfer

## Step 1: Hardware Setup

1. **Connect Pirate Audio HAT** to Raspberry Pi GPIO header
2. **Ensure proper mounting** - the HAT should sit flush with no bent pins
3. **Power on** and complete initial Raspberry Pi setup

## Step 2: Enable Required Interfaces

```bash
sudo raspi-config
```

Navigate to **Interface Options** and enable:
- **SPI** (for display)
- **I2C** (for additional functionality)

## Step 3: Run Installation Scripts

### Base Installation
```bash
cd pirate-audio-mopidy-setup
./scripts/install.sh
```

This script will:
- Update system packages
- Install Python dependencies
- Create virtual environment
- Install Mopidy and plugins
- Install Pirate Audio libraries

### Configuration Setup
```bash
./scripts/configure-mopidy.sh
```

This script will:
- Set up Mopidy configuration
- Create media directories
- Configure audio settings

### Service Setup
```bash
./scripts/setup-services.sh
```

This script will:
- Install Python scripts
- Configure systemd services
- Add user to required groups
- Enable auto-start services

## Step 4: Manual Configuration Steps

### Boot Configuration
Add these lines to `/boot/firmware/config.txt`:
```
dtoverlay=hifiberry-dac
gpio=25=op,dh
dtoverlay=spi1-3cs
```

### Audio Files
1. Copy your audio files to `~/media/Luisterboeken/`
2. Create playlist file `~/media/Kinderboeken.m3u8`

Example playlist format:
```
#EXTM3U
#EXTINF:-1,Track 1
/home/username/media/Luisterboeken/track1.mp3
#EXTINF:-1,Track 2
/home/username/media/Luisterboeken/track2.mp3
```

## Step 5: Final Setup

1. **Reboot** to apply boot configuration:
   ```bash
   sudo reboot
   ```

2. **Verify services** are running:
   ```bash
   sudo systemctl status mopidy
   sudo systemctl status pirate-buttons
   sudo systemctl status pirate-playlist
   ```

3. **Test web interface** at `http://your-pi-ip:6680/iris/`

4. **Test buttons** - A button should start playing your playlist immediately

## Troubleshooting

If you encounter issues, check the [Troubleshooting Guide](troubleshooting.md).

## Next Steps

- Configure additional playlists
- Customize button actions
- Set up display themes
- Add more audio sources