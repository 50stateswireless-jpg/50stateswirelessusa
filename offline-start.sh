#!/bin/bash
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

# Force Ruby to use the local 'vendor' folder
export BUNDLE_PATH="$PROJECT_DIR/vendor/bundle"
export BUNDLE_DEPLOYMENT=true

echo "🚀 Starting Offline Environment..."

# 1. Start Decap Proxy (using local node_modules)
./node_modules/.bin/decap-server --port 8081 &

# 2. Start Jekyll (using local bundle)
bundle exec jekyll serve
