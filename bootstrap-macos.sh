#!/bin/bash
# bootstrap-macos.sh - Complete bootstrap script for macOS
# This script sets up vultitool from scratch on a fresh macOS system

set -euo pipefail

# Colors for output
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'

echo -e "${BLUE}🚀 VultiTool macOS Bootstrap Script${RESET}"
echo -e "${BLUE}====================================${RESET}"
echo ""

# Check if Homebrew is installed
if ! command -v brew > /dev/null 2>&1; then
    echo -e "${YELLOW}📦 Installing Homebrew...${RESET}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ -d "/opt/homebrew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo -e "${GREEN}✅ Homebrew already installed${RESET}"
fi

# Install dependencies
echo -e "${BLUE}📚 Installing dependencies...${RESET}"
brew install python go protobuf git

# Verify we're in the right directory
if [[ ! -f "vultitool.py" ]]; then
    echo -e "${RED}❌ Error: Please run this script from the vultitool repository root${RESET}"
    exit 1
fi

# Run the bootstrap process
echo -e "${BLUE}🔧 Bootstrapping vultitool...${RESET}"
make check-deps
make setup
make build

# Verify installation
echo -e "${BLUE}🧪 Verifying installation...${RESET}"
./vultitool doctor health

echo -e "${BLUE}🎯 Running comprehensive tests...${RESET}"
./vultitool doctor selftest

# Test with a sample file
echo -e "${BLUE}📄 Testing with sample vault file...${RESET}"
./vultitool vault parse tests/fixtures/testGG20-part1of2.vult --summary

echo ""
echo -e "${GREEN}🎉 Bootstrap completed successfully!${RESET}"
echo ""
echo -e "${YELLOW}Next steps:${RESET}"
echo -e "  • Try: ./vultitool vault parse tests/fixtures/testDKLS-1of2.vult"
echo -e "  • Run: ./vultitool help"
echo -e "  • Check: make status"
echo ""
