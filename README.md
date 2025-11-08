# 💳 Apple Wallet Digital Business Card — Self-Contained & Shareable

Create your **own Apple Wallet Digital Business Card (.pkpass)** entirely offline — no developer account, no third-party APIs, and no app required.

Anyone with an iPhone can open your card via **AirDrop, email, or a link** and instantly add it to Apple Wallet.

---

## ✨ Features

- 🪪 **Fully Offline** — No cloud signing or Apple Developer account needed  
- 🧠 **Python-based** — Lightweight script builds `.pkpass` files locally  
- 🎨 **Customizable Branding** — Logo, photo, name, colors, links  
- 📲 **One-tap Wallet Add** — Works instantly on any iPhone  
- 🔒 **Optional Local Signing** — Self-signed with your own key/cert  
- 💻 **Share Anywhere** — AirDrop, email, or host on your personal website  
- ⚙️ **Configuration Files** — YAML/JSON configuration support  
- 🖥️ **CLI Interface** — Command-line tools for easy generation  
- 🌐 **Web UI** — Beautiful web interface for card creation  
- 🧪 **Production Ready** — Comprehensive testing, Docker support, CI/CD  

---

## 🧩 Project Structure

```
wallet_card/
├── src/
│   ├── wallet_card/
│   │   ├── core/              # Core pass generation logic
│   │   │   ├── pass_generator.py
│   │   │   ├── asset_manager.py
│   │   │   └── validator.py
│   │   ├── templates/         # Template system
│   │   │   ├── base_template.py
│   │   │   └── business_card.py
│   │   ├── cli/               # CLI interface
│   │   │   └── commands.py
│   │   ├── web/               # Web UI
│   │   │   ├── app.py
│   │   │   └── templates/
│   │   └── utils/             # Utilities
│   │       ├── config_loader.py
│   │       └── file_utils.py
├── assets/
│   ├── templates/             # Template images
│   └── user/                  # User-provided assets
├── output/                    # Generated .pkpass files
├── tests/                     # Test suite
├── config/                    # Configuration files
│   ├── default.yaml
│   └── example.yaml
├── docker/                    # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
└── .github/workflows/         # CI/CD pipelines
    └── ci.yml
```

---

## 🛠️ Installation

> Works on macOS, Windows, or Linux.

### Prerequisites

- Python 3.8 or higher
- pip

### Quick Start

1. **Clone or download this repo**
   ```bash
   git clone <repository-url>
   cd wallet_card
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or for development:
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```

3. **Initialize configuration** (optional)
   ```bash
   wallet-card init-config
   ```

---

## 📖 Usage

### Command Line Interface (CLI)

#### Generate a Wallet Card

```bash
# Using default configuration
wallet-card generate

# Using a custom configuration file
wallet-card generate -c config/example.yaml

# Specify output filename
wallet-card generate -c config.yaml -o my_card.pkpass

# With signing certificates
wallet-card generate -c config.yaml --cert signer.pem --key signer.key
```

#### Validate Configuration

```bash
wallet-card validate config/example.yaml
```

#### List Available Templates

```bash
wallet-card list-templates
```

#### Initialize Configuration File

```bash
# Create default config.yaml
wallet-card init-config

# Create config.json instead
wallet-card init-config -o config.json -f json
```

### Web Interface

Start the web server:

```bash
python -m wallet_card.web.app
```

Or using the Makefile:

```bash
make run-web
```

Then open your browser to `http://localhost:5000` and use the web interface to:
- Fill in your information
- Upload images
- Customize colors
- Generate and download your card

### Python API

```python
from wallet_card.templates.business_card import BusinessCardTemplate
from wallet_card.utils.config_loader import ConfigLoader

# Load configuration
config = ConfigLoader.load_config("config/example.yaml")

# Create template instance
template = BusinessCardTemplate()

# Generate pass
output_path = template.generate(config)
print(f"Card generated: {output_path}")
```

---

## ⚙️ Configuration

Configuration files support YAML or JSON format. Here's an example:

```yaml
pass:
  passTypeIdentifier: "pass.com.example.businesscard"
  serialNumber: "unique-123"
  organizationName: "Your Name"
  description: "Digital Business Card"
  foregroundColor: "rgb(255,255,255)"
  backgroundColor: "rgb(0,77,153)"
  labelColor: "rgb(255,255,255)"
  fields:
    primaryFields:
      - key: "name"
        label: "Name"
        value: "Your Name"
    secondaryFields:
      - key: "title"
        label: "Title"
        value: "Your Title"
      - key: "email"
        label: "Email"
        value: "your.email@example.com"
    auxiliaryFields:
      - key: "phone"
        label: "Phone"
        value: "+1 (555) 123-4567"
    backFields:
      - key: "linkedin"
        label: "LinkedIn"
        value: "linkedin.com/in/yourprofile"
      - key: "github"
        label: "GitHub"
        value: "github.com/yourusername"
      - key: "website"
        label: "Website"
        value: "https://yourwebsite.com"

assets:
  icon: "assets/user/icon.png"
  logo: "assets/user/logo.png"
  photo: "assets/user/photo.png"

qr_data: "https://yourwebsite.com"

signing:
  enabled: false
  cert_file: null
  key_file: null
```

### Environment Variables

You can override configuration using environment variables prefixed with `WALLET_CARD_`:

```bash
export WALLET_CARD_PASS_ORGANIZATION_NAME="My Company"
export WALLET_CARD_PASS_DESCRIPTION="My Business Card"
```

---

## 🔒 Self-Signing Your Pass (Advanced)

If you want to add cryptographic signing (optional, for cleaner validation):

1. **Generate a self-signed key and certificate:**
   ```bash
   openssl genrsa -out signer.key 2048
   openssl req -new -x509 -sha256 -key signer.key -out signer.pem -days 365
   ```

2. **Update your configuration:**
   ```yaml
   signing:
     enabled: true
     cert_file: "signer.pem"
     key_file: "signer.key"
   ```

3. **Or use CLI flags:**
   ```bash
   wallet-card generate -c config.yaml --cert signer.pem --key signer.key
   ```

Now your pass is cryptographically signed — still 100% offline.

---

## 📩 Sharing

You can share your `.pkpass` in three ways:

| Method | How to Use |
|--------|------------|
| **AirDrop** | Simply AirDrop the file to any iPhone → "Add to Wallet" |
| **Email** | Attach `.pkpass` and send — recipients tap it to open |
| **Website** | Host it at `https://yourdomain.com/yourname.pkpass` and share the link |

(When opened on iPhone Safari, it adds directly to Wallet.)

---

## 🐳 Docker

### Build Docker Image

```bash
make docker-build
```

Or manually:

```bash
docker build -t wallet-card-generator -f docker/Dockerfile .
```

### Run with Docker Compose

```bash
make docker-run
```

Or manually:

```bash
docker-compose -f docker/docker-compose.yml up
```

The web UI will be available at `http://localhost:5000`.

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Using Makefile
make test
```

Run linters:

```bash
make lint
```

Format code:

```bash
make format
```

---

## 🧰 Dependencies

| Library | Purpose |
|---------|---------|
| Custom Implementation | Generates .pkpass bundles (no external library needed) |
| `Pillow` | Image creation and editing |
| `qrcode` | Generates contact/portfolio QR codes |
| `cryptography` | Enables optional self-signing |
| `pyyaml` | YAML configuration parsing |
| `click` | CLI interface |
| `flask` | Web UI framework |

---

## 🧯 Troubleshooting

| Issue | Cause / Fix |
|-------|-------------|
| `.pkpass` won't open on iPhone | Make sure file is zipped by script (.pkpass = structured zip) |
| Images missing | Ensure assets/ folder and filenames are correct |
| Certificate error | If you skipped signing, it's safe to ignore — iPhone still opens unsigned passes for personal use |
| Wrong link | Update the QR and barcode message URLs in configuration |
| Import errors | Make sure you've installed all dependencies: `pip install -r requirements.txt` |
| CLI not found | Install the package: `pip install -e .` or use `python -m wallet_card.cli.commands` |

---

## 🌍 Optional Web Hosting

You can upload your `.pkpass` to any static host like:

- **Vercel** (`/public/yourcard.pkpass`)
- **Netlify**
- **GitHub Pages**

Then share:

```
https://yourdomain.vercel.app/yourname.pkpass
```

Opening that URL on iPhone triggers "Add to Wallet."

---

## 🏗️ Architecture

### Core Components

- **PassGenerator**: Handles .pkpass file creation using wallet-passes library
- **AssetManager**: Manages image processing and QR code generation
- **Validator**: Validates configuration and input data
- **ConfigLoader**: Loads and merges configuration from files and environment variables
- **Templates**: Extensible template system for different pass types

### Template System

Templates provide a way to customize pass appearance and structure. The base `BaseTemplate` class can be extended to create new pass types:

```python
from wallet_card.templates.base_template import BaseTemplate

class CustomTemplate(BaseTemplate):
    def get_template_config(self):
        return {
            # Your template configuration
        }
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd wallet_card

# Install development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Run linters
make lint
```

---

## 📝 API Documentation

### Core API

#### `PassGenerator`

```python
from wallet_card.core.pass_generator import PassGenerator

generator = PassGenerator(
    assets_dir="assets/user",
    output_dir="output",
    cert_file="signer.pem",  # Optional
    key_file="signer.key"    # Optional
)

output_path = generator.generate(config_dict, output_filename="card.pkpass")
```

#### `AssetManager`

```python
from wallet_card.core.asset_manager import AssetManager

manager = AssetManager("assets/user")
icon_path = manager.prepare_icon("custom_icon.png")
qr_path = manager.generate_qr_code("https://example.com")
```

#### `Validator`

```python
from wallet_card.core.validator import Validator

errors = Validator.validate_config(config_dict)
if errors:
    print("Validation errors:", errors)
```

---

## 🧠 Author

**Balaji Koneti**  
Data Scientist & Engineer

- 🌐 [balaji-konetidev.vercel.app](https://balaji-konetidev.vercel.app)
- 💼 [linkedin.com/in/balaji-koneti](https://linkedin.com/in/balaji-koneti)
- 💻 [github.com/KonetiBalaji](https://github.com/KonetiBalaji)

---

## 🪄 License

This project is open-source under the MIT License.  
Feel free to fork, adapt, and personalize it for your own business card.

---

## 💬 Example Command Flow

```bash
# Step 1: Install
pip install -r requirements.txt

# Step 2: Initialize configuration
wallet-card init-config

# Step 3: Edit config.yaml with your information

# Step 4: Generate card
wallet-card generate -c config.yaml

# Step 5: Share your card
open output/your_card.pkpass
# Airdrop or email to iPhone
```

### Or use the Web UI

```bash
# Start web server
make run-web

# Open browser to http://localhost:5000
# Fill form, upload images, generate and download
```

---

## ✅ Result

A ready-to-share Apple Wallet pass that:

- Shows your professional info beautifully
- Works offline, no app required
- Can be distributed freely
- Is fully owned and generated by you
- Supports multiple interfaces (CLI, Web, API)
- Includes comprehensive testing and documentation
