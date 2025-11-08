# Next Steps After Generating Your Wallet Card

## ✅ Your Card is Ready!

You've successfully generated `DEVELOPER.pkpass`. Here's what to do next:

---

## 📲 Add to Apple Wallet

### On iPhone/iPad:

1. **From Files App:**
   - Open Files app
   - Navigate to Downloads or where you saved the file
   - Tap `DEVELOPER.pkpass`
   - Tap "Add" when prompted

2. **From Email:**
   - Open the email with the attachment
   - Tap the `.pkpass` file
   - Tap "Add to Wallet"

3. **From AirDrop:**
   - AirDrop the file from your Mac/another device
   - Tap "Add" when it opens

4. **From Safari (if hosted):**
   - Open the link on your iPhone
   - Tap "Add to Wallet" button

### On Mac:

1. Double-click the `.pkpass` file
2. It will open in Wallet app
3. Click "Add" to add it to your Wallet

---

## 📤 Share Your Card

### Method 1: AirDrop (Easiest)

```bash
# On Mac, right-click the file and select AirDrop
# Or use command line:
open -a Finder output/DEVELOPER.pkpass
# Then drag to AirDrop
```

### Method 2: Email

1. Attach `output/DEVELOPER.pkpass` to an email
2. Send to recipients
3. They tap the attachment on iPhone to add to Wallet

### Method 3: Host on Website (Best for Sharing)

1. **Upload to your website:**
   ```bash
   # Copy the file to your web server
   cp output/DEVELOPER.pkpass /path/to/your/website/public/
   ```

2. **Share the link:**
   ```
   https://yourdomain.com/DEVELOPER.pkpass
   ```

3. **When someone opens this link on iPhone:**
   - Safari automatically detects it's a `.pkpass` file
   - Shows "Add to Wallet" button
   - One tap to add!

### Method 4: QR Code

1. Generate a QR code pointing to your `.pkpass` URL
2. People scan it with their iPhone camera
3. Automatically opens and adds to Wallet

---

## 🔄 Generate More Cards

### Quick Regenerate:

1. **Web UI:**
   ```bash
   ./run.sh
   # Then go to http://localhost:5000
   ```

2. **Command Line:**
   ```bash
   wallet-card generate -c config.yaml -o new_card.pkpass
   ```

3. **Edit Config:**
   ```bash
   # Edit your config file
   nano config/example.yaml
   
   # Then generate
   wallet-card generate -c config/example.yaml
   ```

---

## 🎨 Customize Your Card

### Update Information:

1. **Via Web UI:**
   - Go to http://localhost:5000
   - Fill in new information
   - Generate new card

2. **Via Config File:**
   ```bash
   # Edit config
   wallet-card init-config
   nano config.yaml
   
   # Generate with new config
   wallet-card generate -c config.yaml
   ```

### Add Images:

1. Place your images in `assets/user/`:
   - `icon.png` (180x180)
   - `logo.png` (320x100)
   - `photo.png` (320x320)

2. Reference in config:
   ```yaml
   assets:
     icon: "assets/user/icon.png"
     logo: "assets/user/logo.png"
     photo: "assets/user/photo.png"
   ```

3. Generate again

---

## 🔒 Optional: Sign Your Pass

For production use, you can cryptographically sign your pass:

```bash
# Generate certificate and key
openssl genrsa -out signer.key 2048
openssl req -new -x509 -sha256 -key signer.key -out signer.pem -days 365

# Generate signed pass
wallet-card generate -c config.yaml --cert signer.pem --key signer.key
```

---

## 📝 Tips

- **Multiple Cards:** Generate different cards for different purposes (personal, work, events)
- **Update Cards:** Regenerate with new info anytime
- **Share Easily:** Host on your website for one-click sharing
- **Test First:** Always test on your own iPhone before sharing widely

---

## 🆘 Troubleshooting

### Card won't open on iPhone?
- Make sure file extension is `.pkpass` (not `.zip`)
- Try opening from Files app instead of email
- Check file size (should be reasonable, not corrupted)

### Need to update the card?
- Just regenerate with new information
- The new card will have updated info

### Want to delete a card?
- Open Wallet app
- Tap the card
- Scroll down and tap "Remove Pass"

---

## 🎉 You're All Set!

Your Apple Wallet Digital Business Card is ready to share. Enjoy!

For more help, check:
- [README.md](README.md) - Full documentation
- [RUN.md](RUN.md) - Running instructions
- [QUICKSTART.md](QUICKSTART.md) - Quick examples

