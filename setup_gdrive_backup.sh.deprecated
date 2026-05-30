#!/bin/bash
#
# Miha Backup - Google Drive Setup
# Run this to configure rclone for Google Drive backup
#

echo "=== Miha Backup Setup ==="
echo ""
echo "This will configure Google Drive backup for the Red Dragon MUD project."
echo ""

# Check rclone
if ! command -v rclone &> /dev/null; then
    echo "Installing rclone..."
    curl https://rclone.org/install.sh | bash
fi

# Create rclone config directory
mkdir -p ~/.config/rclone

# Check if already configured
if rclone listremotes 2>/dev/null | grep -q "gdrive"; then
    echo "Google Drive already configured!"
    rclone about gdrive:
    exit 0
fi

echo "Starting Google Drive configuration..."
echo ""
echo "When prompted:"
echo "  1. Choose 'n' for New remote"
echo "  2. Name it: gdrive"
echo "  3. Choose '18' for Google Drive (or type 'drive')"
echo "  4. Press ENTER for Client Id (default)"
echo "  5. Press ENTER for Client Secret (default)"
echo "  6. Choose '1' for Full access"
echo "  7. Press ENTER for root_folder_id"
echo "  8. Press ENTER for service_account_file"
echo "  9. Say 'n' to Edit advanced config"
echo "  10. Say 'n' to Auto config (headless)"
echo "  11. You will get a URL - visit it in your browser"
echo "  12. Authorize and copy the code back"
echo "  13. Say 'y' to confirm"
echo "  14. Say 'q' to quit"
echo ""

read -p "Press ENTER to start rclone config..."
rclone config

echo ""
echo "Testing connection..."
rclone about gdrive:

if [ $? -eq 0 ]; then
    echo ""
    echo "=== Setup Complete ==="
    echo "You can now backup with: ./backup_miha.sh"
    echo "Or by typing 'good night' to Miha"
else
    echo ""
    echo "=== Setup Failed ==="
    echo "Please check the error above and try again."
fi
