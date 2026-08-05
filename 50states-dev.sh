#!/bin/bash

# 1. Load environment
source "$HOME/.bashrc" 2>/dev/null || source "$HOME/.profile" 2>/dev/null

# 2. Detect location
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR" || { echo "Project dir not found!"; exit 1; }

echo "🚀 Starting 50States Wireless..."

# 3. DETACHED BROWSER OPENER
# We move this to the top and 'disown' it so it's not tied to the terminal's life
(
  sleep 7
  # Explicitly set the display for Linux Mint GUI
  export DISPLAY=:0
  
  # Try opening both tabs in Firefox
  firefox "http://127.0.0.1:4000/50stateswirelessusa/" "http://localhost:4000/50stateswirelessusa/admin/#/collections/settings" > /dev/null 2>&1 &
) & disown

# 4. Start decap-server in background
npx decap-server --port 8081 &

# 5. Start Jekyll (This stays in the foreground)
echo "🔥 Jekyll is building your site..."
bundle exec jekyll serve
