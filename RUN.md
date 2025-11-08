# How to Run the Wallet Card Generator

## ✅ Fixed: No More wallet-passes Dependency!

The project now uses a **custom pkpass generator** - no external `wallet-passes` library needed!

## Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd /Users/balaji/Desktop/Shiva
pip3 install -r requirements.txt
```

**All dependencies should install successfully now!** ✅

### Step 2: Choose Your Method

You have 4 ways to run the project:

#### Option A: Web UI (Easiest) ⭐

```bash
# Add src to Python path and run
PYTHONPATH=src python3 -m wallet_card.web.app
```

Or install the package first:
```bash
pip3 install -e .
python3 -m wallet_card.web.app
```

Then open: **http://localhost:5000**

#### Option B: Command Line

```bash
# Install the CLI command
pip3 install -e .

# Initialize config
wallet-card init-config

# Edit config.yaml with your info, then:
wallet-card generate -c config.yaml
```

#### Option C: Legacy Script

```bash
PYTHONPATH=src python3 make_pass.py
```

#### Option D: Python API

```python
import sys
sys.path.insert(0, 'src')

from wallet_card.templates.business_card import BusinessCardTemplate
from wallet_card.utils.config_loader import ConfigLoader

config = ConfigLoader.load_config("config/example.yaml")
template = BusinessCardTemplate()
output = template.generate(config)
print(f"Card ready: {output}")
```

### Step 3: Get Your Card

Your `.pkpass` file will be in the `output/` directory. Share it via:
- AirDrop to iPhone
- Email attachment
- Host on a website

---

## Detailed Instructions

### Method 1: Web UI (Recommended for Beginners)

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   # Option 1: Without installing package
   PYTHONPATH=src python3 -m wallet_card.web.app
   
   # Option 2: Install package first (recommended)
   pip3 install -e .
   python3 -m wallet_card.web.app
   ```

3. **Open browser:**
   - Go to: `http://localhost:5000`
   - Fill in the form
   - Upload images (optional)
   - Click "Generate Wallet Card"
   - Download your `.pkpass` file

4. **Stop the server:**
   - Press `Ctrl+C` in the terminal

### Method 2: Command Line Interface

1. **Install the package:**
   ```bash
   pip3 install -e .
   ```

2. **Create a config file:**
   ```bash
   wallet-card init-config
   ```

3. **Edit the config:**
   ```bash
   # Edit config.yaml with your information
   nano config.yaml
   # or
   open config.yaml
   ```

4. **Generate your card:**
   ```bash
   wallet-card generate -c config.yaml
   ```

5. **Find your card:**
   ```bash
   ls output/
   ```

### Method 3: Using Makefile

```bash
# Install dependencies
make install

# Run web UI
make run-web

# Run tests
make test

# Format code
make format
```

### Method 4: Docker

```bash
# Build image
make docker-build

# Run container
make docker-run

# Access at http://localhost:5000
```

---

## Troubleshooting

### Issue: Module not found errors

**Solution 1: Use PYTHONPATH**
```bash
PYTHONPATH=src python3 -m wallet_card.web.app
```

**Solution 2: Install the package**
```bash
pip3 install -e .
```

### Issue: CLI command not found

```bash
# Install in development mode
pip3 install -e .

# Or use Python module directly
PYTHONPATH=src python3 -m wallet_card.cli.commands generate -c config.yaml
```

### Issue: Port 5000 already in use

```bash
# Use a different port
export FLASK_RUN_PORT=5001
python3 -m wallet_card.web.app
```

### Issue: Permission errors

```bash
# Use user installation
pip3 install --user -r requirements.txt
pip3 install --user -e .
```

---

## Example Workflow

```bash
# 1. Navigate to project
cd /Users/balaji/Desktop/Shiva

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Install package (for CLI)
pip3 install -e .

# 4. Create config
wallet-card init-config

# 5. Edit config.yaml (add your name, email, etc.)

# 6. Generate card
wallet-card generate -c config.yaml

# 7. Open the generated file
open output/*.pkpass
```

---

## What Changed?

- ✅ **Removed `wallet-passes` dependency** - now uses custom implementation
- ✅ **All dependencies install successfully**
- ✅ **Works completely offline**
- ✅ **No external library needed for pkpass generation**

---

## Next Steps

- Read the full [README.md](README.md) for advanced features
- Check [QUICKSTART.md](QUICKSTART.md) for more examples
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

---

## Need Help?

- Check the [README.md](README.md) documentation
- Review error messages in the terminal
- Ensure all dependencies are installed
- Verify Python version (3.8+): `python3 --version`
