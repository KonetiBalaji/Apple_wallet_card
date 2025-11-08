from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wallet-card-generator",
    version="1.0.0",
    author="Balaji Koneti",
    author_email="koneti.balaji08@gmail.com",
    description="Generate Apple Wallet Digital Business Cards offline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KonetiBalaji/apple-wallet-card",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pillow>=10.0.0",
        "qrcode[pil]>=7.4.2",
        "cryptography>=41.0.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "flask>=3.0.0",
        "werkzeug>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "wallet-card=wallet_card.cli.commands:main",
        ],
    },
)

