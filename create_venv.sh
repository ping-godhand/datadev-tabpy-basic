#!/bin/bash

echo "Creating Python virtual environment..."
python -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
pip install pandas==2.2.3 numpy==2.4.3
pip install scikit-learn==1.8.0
pip install openai==2.26.0
pip install yfinance==1.2.0
pip install tabpy==2.13.0

echo ""
echo "Virtual environment created and dependencies installed."
echo "To activate the venv, run:"
echo "    source .venv/bin/activate"
source .venv/bin/activate