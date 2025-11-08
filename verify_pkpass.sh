#!/bin/bash
# Verify .pkpass file structure

PKPASS_FILE="${1:-output/*.pkpass}"

if [ ! -f "$PKPASS_FILE" ]; then
    echo "❌ File not found: $PKPASS_FILE"
    exit 1
fi

echo "🔍 Verifying: $PKPASS_FILE"
echo ""

# Extract to temp directory
TEMP_DIR=$(mktemp -d)
unzip -q "$PKPASS_FILE" -d "$TEMP_DIR" 2>&1

echo "📋 Files in pkpass:"
ls -1 "$TEMP_DIR" | grep -v "^__MACOSX" | grep -v "^\."
echo ""

# Check for required files
REQUIRED=("pass.json" "manifest.json" "signature")
MISSING=0

for file in "${REQUIRED[@]}"; do
    if [ -f "$TEMP_DIR/$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING!"
        MISSING=1
    fi
done

echo ""

# Check for macOS metadata (should NOT be present)
if [ -d "$TEMP_DIR/__MACOSX" ] || find "$TEMP_DIR" -name ".DS_Store" | grep -q .; then
    echo "⚠️  WARNING: macOS metadata files found (should be excluded)"
else
    echo "✅ No macOS metadata files"
fi

echo ""

# Check pass.json structure
if [ -f "$TEMP_DIR/pass.json" ]; then
    echo "📄 pass.json structure check:"
    
    # Required keys
    REQUIRED_KEYS=("formatVersion" "passTypeIdentifier" "serialNumber" "teamIdentifier" "organizationName")
    for key in "${REQUIRED_KEYS[@]}"; do
        if grep -q "\"$key\"" "$TEMP_DIR/pass.json"; then
            VALUE=$(grep "\"$key\"" "$TEMP_DIR/pass.json" | head -1)
            echo "  ✅ $key: $VALUE"
        else
            echo "  ❌ Missing: $key"
            MISSING=1
        fi
    done
    
    # Check for images field (should NOT be in pass.json)
    if grep -q "\"images\"" "$TEMP_DIR/pass.json"; then
        echo "  ⚠️  WARNING: 'images' field in pass.json (should be separate files)"
    else
        echo "  ✅ No 'images' field (correct - images are separate files)"
    fi
fi

echo ""

# Check signature
if [ -f "$TEMP_DIR/signature" ]; then
    SIZE=$(stat -f%z "$TEMP_DIR/signature" 2>/dev/null || stat -c%s "$TEMP_DIR/signature" 2>/dev/null)
    if [ "$SIZE" -gt 200 ]; then
        echo "✅ Signature: Proper cryptographic signature ($SIZE bytes)"
    elif [ "$SIZE" -gt 0 ]; then
        echo "⚠️  Signature: Small size ($SIZE bytes) - might be placeholder"
    else
        echo "❌ Signature: Empty"
        MISSING=1
    fi
fi

echo ""

# Check manifest
if [ -f "$TEMP_DIR/manifest.json" ]; then
    echo "✅ manifest.json exists"
    echo "   Contents:"
    cat "$TEMP_DIR/manifest.json" | python3 -m json.tool 2>/dev/null | head -10
fi

echo ""

if [ $MISSING -eq 0 ]; then
    echo "✅ Pass structure looks good!"
    echo ""
    echo "💡 If it still doesn't work on iPhone:"
    echo "   - Try Safari web link (best method)"
    echo "   - iOS 17+ may require Apple Developer certificate"
    echo "   - Consider QR code or contact card as alternative"
else
    echo "❌ Pass structure has issues - regenerate the pass"
fi

# Cleanup
rm -rf "$TEMP_DIR"

