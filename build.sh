#!/usr/bin/env bash
# build.sh - Render build script for Chrome installation

set -o errexit  # Exit on error

echo "🚀 Starting build process..."

# Update package lists
echo "📦 Updating package lists..."
apt-get update

# Install Chrome dependencies
echo "🔧 Installing Chrome dependencies..."
apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates

# Add Google Chrome repository
echo "🌐 Adding Google Chrome repository..."
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update package lists again
apt-get update

# Install Google Chrome
echo "🔥 Installing Google Chrome..."
apt-get install -y google-chrome-stable

# Verify Chrome installation
echo "✅ Verifying Chrome installation..."
google-chrome --version

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎉 Build completed successfully!"