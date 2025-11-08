#!/bin/bash
# Generate self-signed certificate for wallet pass signing

echo "🔐 Generating self-signed certificate for wallet pass..."

# Generate private key
openssl genrsa -out signer.key 2048

# Generate certificate
openssl req -new -x509 -sha256 -key signer.key -out signer.pem -days 365 -subj "/CN=Wallet Pass Signer/O=Personal/C=US"

echo "✅ Certificate generated:"
echo "   - signer.key (private key)"
echo "   - signer.pem (certificate)"
echo ""
echo "Now regenerate your pass with signing enabled!"

