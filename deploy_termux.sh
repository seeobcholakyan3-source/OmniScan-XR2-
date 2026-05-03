#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Setting up OmniScan-XR2..."

pkg update -y
pkg install python -y

pip install --upgrade pip

# create venv safely
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

echo "✅ Setup complete. Run: python OmniOrchestrator.py"
