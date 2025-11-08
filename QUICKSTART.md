# Quick Start Guide

Get up and running with the Apple Wallet Card Generator in minutes!

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd wallet_card

# Install dependencies
pip install -r requirements.txt
```

## Method 1: Web UI (Easiest)

1. Start the web server:
   ```bash
   python -m wallet_card.web.app
   ```

2. Open your browser to `http://localhost:5000`

3. Fill in the form, upload images, and download your card!

## Method 2: Command Line

1. Initialize a configuration file:
   ```bash
   wallet-card init-config
   ```

2. Edit `config.yaml` with your information

3. Generate your card:
   ```bash
   wallet-card generate -c config.yaml
   ```

4. Find your card in the `output/` directory

## Method 3: Python API

```python
from wallet_card.templates.business_card import BusinessCardTemplate
from wallet_card.utils.config_loader import ConfigLoader

# Load config
config = ConfigLoader.load_config("config/example.yaml")

# Generate
template = BusinessCardTemplate()
output = template.generate(config)
print(f"Card ready: {output}")
```

## Method 4: Legacy Script

For backward compatibility with the original README:

```bash
python make_pass.py
```

## Next Steps

- Customize colors and branding in your config file
- Add your own images to `assets/user/`
- Host your `.pkpass` file on a website for easy sharing
- Check out the full [README.md](README.md) for advanced features

## Troubleshooting

**CLI command not found?**
```bash
pip install -e .
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**Need help?** Check the [README.md](README.md) or open an issue!

