#!/bin/bash
set -e

echo "=== Pirate Audio Mopidy Setup Installer ==="
echo "This script will install and configure Mopidy with Pirate Audio HAT support"
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should NOT be run as root. Please run as a regular user."
   exit 1
fi

# Update system
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install system dependencies
echo "Installing system dependencies..."
sudo apt install -y python3-pip python3-venv python3-dev git curl wget \
    build-essential libasound2-dev libffi-dev libssl-dev pkg-config \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    python3-gi python3-gi-cairo gir1.2-gstreamer-1.0 \
    python3-setuptools python3-wheel

# Install Pirate Audio dependencies
echo "Installing Pirate Audio dependencies..."
sudo apt install -y python3-rpi.gpio python3-spidev python3-pil python3-numpy

# Install Pirate Audio library
echo "Installing Pirate Audio ST7789 library..."
pip3 install st7789 --user

# Create virtual environment for Mopidy
echo "Creating Python virtual environment..."
python3 -m venv ~/.virtualenvs/mopidy --system-site-packages

# Activate virtual environment and install Mopidy
echo "Installing Mopidy and plugins..."
source ~/.virtualenvs/mopidy/bin/activate
pip install --upgrade pip
pip install mopidy mopidy-iris mopidy-file

# Create Mopidy config directory
mkdir -p ~/.config/mopidy

echo ""
echo "✅ Base installation complete!"
echo "Next steps:"
echo "1. Run ./configure-mopidy.sh to set up configuration"
echo "2. Run ./setup-services.sh to configure systemd services"
echo ""