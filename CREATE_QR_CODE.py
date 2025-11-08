#!/usr/bin/env python3
"""Create QR code business card as alternative to Wallet pass."""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import sys

def create_qr_business_card(name, title, email, phone, website, linkedin, github, output_file="business_card_qr.png"):
    """Create a QR code business card."""
    
    # Create vCard data
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
ORG:{title}
EMAIL;TYPE=WORK:{email}
TEL;TYPE=CELL:{phone}
URL:{website}
URL:{linkedin}
URL:{github}
END:VCARD"""
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(vcard)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create business card image
    card_width = 800
    card_height = 500
    card = Image.new('RGB', (card_width, card_height), color='white')
    draw = ImageDraw.Draw(card)
    
    # Try to use a nice font
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add QR code (left side)
    qr_size = 300
    qr_resized = qr_img.resize((qr_size, qr_size))
    card.paste(qr_resized, (50, 100))
    
    # Add text (right side)
    y_pos = 100
    draw.text((400, y_pos), name, fill='black', font=font_large)
    y_pos += 50
    draw.text((400, y_pos), title, fill='gray', font=font_medium)
    y_pos += 60
    draw.text((400, y_pos), f"📧 {email}", fill='black', font=font_small)
    y_pos += 40
    draw.text((400, y_pos), f"📱 {phone}", fill='black', font=font_small)
    if website:
        y_pos += 40
        draw.text((400, y_pos), f"🌐 {website}", fill='blue', font=font_small)
    
    # Save
    card.save(output_file)
    print(f"✅ QR code business card created: {output_file}")
    print(f"📱 Scan with iPhone camera to add contact!")

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        # Get from command line
        name = sys.argv[1] if len(sys.argv) > 1 else "Your Name"
        title = sys.argv[2] if len(sys.argv) > 2 else "Your Title"
        email = sys.argv[3] if len(sys.argv) > 3 else "email@example.com"
        phone = sys.argv[4] if len(sys.argv) > 4 else "+1234567890"
        website = sys.argv[5] if len(sys.argv) > 5 else ""
        linkedin = sys.argv[6] if len(sys.argv) > 6 else ""
        github = sys.argv[7] if len(sys.argv) > 7 else ""
    else:
        # Default
        name = "Balaji Koneti"
        title = "AI Engineer"
        email = "Balajishiva2580@gmail.com"
        phone = "+1234567890"
        website = ""
        linkedin = ""
        github = ""
    
    create_qr_business_card(name, title, email, phone, website, linkedin, github)

