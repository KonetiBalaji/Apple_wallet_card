# Fix: Wallet Pass Not Opening on iPhone

## The Problem

Modern iOS versions (iOS 15+) require **properly signed** wallet passes. Unsigned passes or passes with placeholder signatures won't work.

## Solution: Generate Self-Signed Certificate

### Step 1: Generate Certificate

```bash
./generate_cert.sh
```

This creates:
- `signer.key` (private key)
- `signer.pem` (certificate)

### Step 2: Regenerate Pass with Signing

**Option A: Web UI**
1. Go to http://localhost:5000
2. Fill in the form
3. Before generating, the system will automatically use the certificate if it exists

**Option B: Command Line**
```bash
wallet-card generate -c config.yaml --cert signer.pem --key signer.key
```

**Option C: Update Config**
Edit your config file:
```yaml
signing:
  enabled: true
  cert_file: "signer.pem"
  key_file: "signer.key"
```

Then generate:
```bash
wallet-card generate -c config.yaml
```

### Step 3: Test on iPhone

1. Transfer the new `.pkpass` file to iPhone
2. Open it - should now prompt "Add to Wallet"

## Alternative: Use Safari/Web Link

If signing still doesn't work, try hosting the file on a website:

1. Upload `.pkpass` to your website
2. Share the direct link
3. Open link in Safari on iPhone
4. Safari will automatically detect and prompt to add

## Troubleshooting

**Still not working?**
- Make sure certificate files are in the project root
- Check that the file has proper structure: `./test_pkpass.sh output/yourfile.pkpass`
- Try opening via Safari web link instead of AirDrop
- Some iOS versions are stricter - try on different device/version

