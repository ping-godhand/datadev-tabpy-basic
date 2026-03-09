Write-Host "Creating Python virtual environment..."
python -m venv .venv

Write-Host "Activating virtual environment..."
& .venv\Scripts\Activate.ps1

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing dependencies..."
pip install pandas==2.2.3 numpy==2.4.3
pip install scikit-learn==1.8.0
pip install openai==2.26.0
pip install yfinance==1.2.0
pip install tabpy==2.13.0

Write-Host ""
Write-Host "Virtual environment created and dependencies installed."
Write-Host "To activate the venv, run:"
Write-Host "    .venv\Scripts\Activate.ps1"
pause
