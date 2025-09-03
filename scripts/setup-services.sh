#!/bin/bash
set -e

echo "=== SystemD Services Setup ==="
echo ""

# Copy scripts to home directory
echo "Installing Python scripts..."
cp ../src/*.py ~/

# Make scripts executable
chmod +x ~/pirate_buttons_with_cleanup.py
chmod +x ~/load_kinderboeken_playlist_fixed.py
chmod +x ~/pirate_display_with_icons.py

# Update script paths in systemd services
echo "Configuring systemd services..."
CURRENT_USER=$(whoami)
CURRENT_HOME=$HOME

# Create temporary service files with correct paths
sed "s/gxjansen/$CURRENT_USER/g; s|/home/gxjansen|$CURRENT_HOME|g" ../systemd/mopidy.service > /tmp/mopidy.service
sed "s/gxjansen/$CURRENT_USER/g; s|/home/gxjansen|$CURRENT_HOME|g" ../systemd/pirate-buttons.service > /tmp/pirate-buttons.service
sed "s/gxjansen/$CURRENT_USER/g; s|/home/gxjansen|$CURRENT_HOME|g" ../systemd/pirate-playlist.service > /tmp/pirate-playlist.service

# Install systemd services
echo "Installing systemd services..."
sudo cp /tmp/mopidy.service /etc/systemd/system/
sudo cp /tmp/pirate-buttons.service /etc/systemd/system/
sudo cp /tmp/pirate-playlist.service /etc/systemd/system/

# Clean up temporary files
rm /tmp/mopidy.service /tmp/pirate-buttons.service /tmp/pirate-playlist.service

# Add user to required groups
echo "Adding user to required groups..."
sudo usermod -a -G audio,spi,i2c,gpio $CURRENT_USER

# Reload systemd and enable services
echo "Enabling systemd services..."
sudo systemctl daemon-reload
sudo systemctl enable mopidy.service
sudo systemctl enable pirate-buttons.service
sudo systemctl enable pirate-playlist.service

echo ""
echo "✅ SystemD services setup complete!"
echo ""
echo "Services installed and enabled:"
echo "  - mopidy.service (Music server)"
echo "  - pirate-buttons.service (Button controller)"
echo "  - pirate-playlist.service (Auto-load playlist)"
echo ""
echo "⚠️  You may need to log out and back in for group membership to take effect"
echo "⚠️  Services will start automatically after reboot"
echo ""