#!/bin/bash
# StackUp Scanner — VPS Setup Script
# Run this on your VPS to install and start the scanner

set -e

echo "=== StackUp Opportunity Scanner Setup ==="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
fi

# Get the directory where this script lives
SCANNER_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCANNER_DIR"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Prompt for Telegram setup
echo ""
echo "=== Telegram Bot Setup ==="
echo "1. Open Telegram, search for @BotFather"
echo "2. Send /newbot, name it 'StackUp Scanner'"
echo "3. Copy the API token"
echo ""

if [ -z "$STACKUP_TELEGRAM_TOKEN" ]; then
    read -p "Paste your Telegram bot token: " TELEGRAM_TOKEN
else
    TELEGRAM_TOKEN="$STACKUP_TELEGRAM_TOKEN"
fi

echo ""
echo "4. Open Telegram, search for @userinfobot"
echo "5. Send /start to get your chat ID"
echo ""

if [ -z "$STACKUP_TELEGRAM_CHAT_ID" ]; then
    read -p "Paste your Telegram chat ID: " CHAT_ID
else
    CHAT_ID="$STACKUP_TELEGRAM_CHAT_ID"
fi

# Create environment file
cat > .env << EOF
STACKUP_TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
STACKUP_TELEGRAM_CHAT_ID=${CHAT_ID}
EOF

echo "Saved credentials to .env"

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/stackup-scanner.service > /dev/null << UNIT
[Unit]
Description=StackUp Opportunity Scanner
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=${SCANNER_DIR}
EnvironmentFile=${SCANNER_DIR}/.env
ExecStart=${SCANNER_DIR}/venv/bin/python3 ${SCANNER_DIR}/scanner.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
UNIT

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable stackup-scanner
sudo systemctl start stackup-scanner

echo ""
echo "=== Setup Complete ==="
echo "Scanner is running as a systemd service."
echo ""
echo "Useful commands:"
echo "  sudo systemctl status stackup-scanner    # Check status"
echo "  sudo journalctl -u stackup-scanner -f    # Live logs"
echo "  sudo systemctl restart stackup-scanner   # Restart"
echo "  sudo systemctl stop stackup-scanner      # Stop"
echo ""
echo "Logs also written to: ${SCANNER_DIR}/scanner.log"
echo "Database at: ${SCANNER_DIR}/stackup.db"
