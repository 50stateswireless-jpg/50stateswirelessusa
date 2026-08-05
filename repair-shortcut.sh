#!/bin/bash

# 1. Dynamically detect the folder where THIS script is located
# 'readlink -f' gets the full absolute path regardless of where you run it from
CURRENT_DIR=$(dirname "$(readlink -f "$0")")

echo "🔧 Detecting environment..."
echo "📍 Current Path: $CURRENT_DIR"
echo "👤 Current User: $USER"

# --- START SHORTCUT ---
START_ICON="$CURRENT_DIR/50States Start.desktop"
cat > "$START_ICON" <<EOF
[Desktop Entry]
Name=50States START
Comment=Start Jekyll + Decap CMS
Exec=gnome-terminal -- bash -c "'$CURRENT_DIR/50states-dev.sh'"
Icon=web-github
Terminal=true
Type=Application
Categories=Development;
EOF

# --- STOP SHORTCUT ---
STOP_ICON="$CURRENT_DIR/50States STOP.desktop"
cat > "$STOP_ICON" <<EOF
[Desktop Entry]
Name=50States STOP
Comment=Shutdown Jekyll + Decap CMS
Exec="$CURRENT_DIR/stop-50states.sh"
Icon=process-stop
Terminal=false
Type=Application
Categories=Development;
EOF

# 2. Make all scripts and icons executable
chmod +x "$CURRENT_DIR/50states-dev.sh"
chmod +x "$CURRENT_DIR/stop-50states.sh"
chmod +x "$START_ICON" "$STOP_ICON"

# 3. Tell Linux Mint (Cinnamon/Gio) to trust these launchers
gio set "$START_ICON" metadata::trusted true 2>/dev/null
gio set "$STOP_ICON" metadata::trusted true 2>/dev/null

# 4. OPTIONAL: Copy shortcuts to your actual Desktop folder
# This makes them appear on your desktop wallpaper automatically
cp "$START_ICON" "$HOME/Desktop/"
cp "$STOP_ICON" "$HOME/Desktop/"
chmod +x "$HOME/Desktop/50States Start.desktop"
chmod +x "$HOME/Desktop/50States STOP.desktop"

echo "✅ Shortcuts updated and copied to your Desktop!"
sleep 2
