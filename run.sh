#!/bin/bash
# Quick run script for wallet card generator

cd "$(dirname "$0")"

# Add src to Python path
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# Run the web app
python3 -m wallet_card.web.app
