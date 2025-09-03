#!/bin/bash
set -e

echo "=== Mopidy Configuration Setup ==="
echo ""

# Copy configuration template
echo "Setting up Mopidy configuration..."
cp ../config/mopidy.conf.template ~/.config/mopidy/mopidy.conf

# Configure boot settings for audio
echo "Configuring boot settings for HiFiBerry DAC..."
sudo cp ../config/boot-config.txt /boot/firmware/config.txt.backup
echo ""
echo "⚠️  IMPORTANT: Boot configuration needs manual review!"
echo "The boot configuration has been backed up to /boot/firmware/config.txt.backup"
echo ""
echo "Please add these lines to /boot/firmware/config.txt:"
echo "dtoverlay=hifiberry-dac"
echo "gpio=25=op,dh"
echo "dtoverlay=spi1-3cs"
echo ""

# Prompt for media directory
echo "Setting up media directory..."
read -p "Enter the path where your audio files will be stored (default: ~/media): " MEDIA_DIR
MEDIA_DIR=${MEDIA_DIR:-"$HOME/media"}

# Create media directory
mkdir -p "$MEDIA_DIR/Luisterboeken"

# Update mopidy.conf with correct paths
sed -i "s|/home/gxjansen/media|$MEDIA_DIR|g" ~/.config/mopidy/mopidy.conf
sed -i "s|/home/gxjansen|$HOME|g" ~/.config/mopidy/mopidy.conf

echo ""
echo "✅ Configuration setup complete!"
echo "Media directory created at: $MEDIA_DIR"
echo ""
echo "⚠️  Manual steps required:"
echo "1. Edit ~/.config/mopidy/mopidy.conf and update any remaining placeholders"
echo "2. Add your audio files to $MEDIA_DIR/Luisterboeken/"
echo "3. Create your playlist file: $MEDIA_DIR/Kinderboeken.m3u8"
echo "4. Reboot after boot configuration changes"
echo ""