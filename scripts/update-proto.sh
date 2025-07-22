#!/bin/bash
# update-proto.sh - Fetch latest protobuf definitions from Vultisig commondata repo
# This ensures we always use the official, up-to-date protobuf schemas

set -euo pipefail

# Configuration
COMMONDATA_REPO="https://github.com/vultisig/commondata"
PROTO_DIR="proto"
TMP_DIR="/tmp/vultisig-commondata-$$"
BRANCH="main"

# Colors for output
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'

echo -e "${BLUE}Updating protobuf definitions from official Vultisig sources...${RESET}"

# Clean up on exit
cleanup() {
    if [ -d "$TMP_DIR" ]; then
        rm -rf "$TMP_DIR"
    fi
}
trap cleanup EXIT

# Clone the commondata repository
echo -e "${BLUE}Cloning Vultisig commondata repository...${RESET}"
git clone --depth 1 --branch "$BRANCH" "$COMMONDATA_REPO" "$TMP_DIR"

# Create proto directory if it doesn't exist
mkdir -p "$PROTO_DIR"

# Copy protobuf files
echo -e "${BLUE}Copying protobuf files...${RESET}"

# Check if the proto files exist in the commondata repo
if [ ! -d "$TMP_DIR/proto" ]; then
    echo -e "${RED}❌ Proto directory not found in commondata repo${RESET}"
    exit 1
fi

# Copy all proto files, maintaining directory structure
rsync -av --delete "$TMP_DIR/proto/" "$PROTO_DIR/"

# List what was copied
echo -e "${GREEN}✅ Updated protobuf files:${RESET}"
find "$PROTO_DIR" -name "*.proto" -type f | sed 's/^/  /'

echo -e "${GREEN}✅ Protobuf definitions updated successfully!${RESET}"
echo -e "${YELLOW}Note: Run 'make protobuf' to regenerate language bindings${RESET}"
