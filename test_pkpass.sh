#!/bin/bash
# Test script to verify pkpass structure

PKPASS_FILE="${1:-output/DEVELOPER.pkpass}"

if [ ! -f "$PKPASS_FILE" ]; then
    echo "❌ File not found: $PKPASS_FILE"
    exit 1
fi

echo "📦 Testing pkpass file: $PKPASS_FILE"
echo ""

# Extract to temp directory
TEMP_DIR=$(mktemp -d)
unzip -q "$PKPASS_FILE" -d "$TEMP_DIR"

echo "📋 Files in pkpass:"
ls -la "$TEMP_DIR"
echo ""

# Check for required files
REQUIRED_FILES=("pass.json" "manifest.json" "signature")
MISSING=0

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$TEMP_DIR/$file" ]; then
        echo "✅ $file exists"
        if [ "$file" == "signature" ]; then
            SIZE=$(stat -f%z "$TEMP_DIR/$file" 2>/dev/null || stat -c%s "$TEMP_DIR/$file" 2>/dev/null)
            echo "   Size: $SIZE bytes"
        fi
    else
        echo "❌ $file MISSING!"
        MISSING=1
    fi
done

echo ""
if [ $MISSING -eq 0 ]; then
    echo "✅ All required files present!"
    echo ""
    echo "📄 pass.json preview:"
    head -20 "$TEMP_DIR/pass.json"
else
    echo "❌ Missing required files!"
fi

# Cleanup
rm -rf "$TEMP_DIR"

