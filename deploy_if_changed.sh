#!/bin/bash
set -e

REPO_URL="https://github.com/JacobLMiller/gmap2.0.git"
LIVE_BRANCH="live"
APP_DIR="$HOME/gmap2.0"
TMP_DIR="/tmp/gmap2.0_live_tmp"

# Clone live branch to temp dir
rm -rf "$TMP_DIR"
git clone --branch "$LIVE_BRANCH" --depth 1 "$REPO_URL" "$TMP_DIR"

# Compare with current app dir
if ! diff -qr "$APP_DIR" "$TMP_DIR" > /dev/null; then
    echo "Changes detected. Deploying new version..."
    # Stop the server (adjust this to your setup)
    sudo docker-compose -f "$APP_DIR/docker-compose.yml" down

    # Update app dir
    cd "$APP_DIR"
    git fetch origin "$LIVE_BRANCH"
    git reset --hard "origin/$LIVE_BRANCH"

    # Restart the server
    sudo docker-compose -f "$APP_DIR/docker-compose.yml" up -d --build
else
    echo "No changes detected. Nothing to do."
fi

# Clean up
rm -rf "$TMP_DIR"