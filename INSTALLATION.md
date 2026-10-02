# Installation Guide

## Prerequisites

- Windows 10/11, macOS, or Linux
- Internet connection (for initial download)
- ~5 minutes of setup time

## Step-by-Step Installation

### 1. Install Python

**Windows:**
1. Go to [python.org](https://www.python.org/downloads/)
2. Download Python 3.8 or higher (3.11+ recommended)
3. Run the installer
4. **IMPORTANT:** Check "Add Python to PATH"
5. Click Install

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3 python3-pip
```

### 2. Verify Python Installation

Open Command Prompt (Windows) or Terminal (Mac/Linux) and run:

```bash
python --version
# Should show: Python 3.8.0 or higher

python -m pip --version
# Should show: pip version ...
```

### 3. Clone or Download This Repository

**Option A: Using Git (if you have it)**
```bash
git clone https://github.com/yourusername/color-separation-analysis.git
cd color-separation-analysis
```

**Option B: Download ZIP**
1. Click green "Code" button on GitHub
2. Click "Download ZIP"
3. Extract the folder

### 4. Install Dependencies

Open Command Prompt/Terminal in the repository folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- `pikepdf` - PDF color analysis
- `streamlit` - Web application framework

**Installation time:** 2-3 minutes

## Verification

Test that everything works:

```bash
# For desktop app
python ColorAnalysisApp.py

# For web app
streamlit run color_separation_app.py
```

You should see the application launch without errors.

## Windows Users: Quick Launch

Double-click either file:
- `RUN_DESKTOP.bat` - Launches desktop app
- `RUN_WEB.bat` - Launches web app

## Troubleshooting

### "python: command not found"

**Cause:** Python not installed or not in PATH

**Solution:**
1. Reinstall Python from python.org
2. **MAKE SURE** to check "Add Python to PATH" during installation
3. Restart Command Prompt after installing

### "ModuleNotFoundError: No module named 'pikepdf'"

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### "pip: command not found"

**Cause:** Python not properly installed

**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Application won't start

**For Desktop App:**
1. Open Command Prompt in the folder
2. Run: `python ColorAnalysisApp.py`
3. This will show the actual error message

**For Web App:**
1. Open Command Prompt in the folder
2. Run: `streamlit run color_separation_app.py`
3. This will show the actual error message

### "permission denied" on Mac/Linux

**Solution:**
```bash
chmod +x color_analyzer.py
python color_analyzer.py document.pdf
```

## Advanced Setup Options

### Virtual Environment (Recommended for development)

Isolate dependencies in a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# When done, deactivate:
deactivate
```

### Docker (Advanced)

```bash
docker build -t color-analysis .
docker run -p 8501:8501 color-analysis
```

## Testing Your Installation

### Desktop App Test

1. Run: `python ColorAnalysisApp.py`
2. Window should open with "Color Separation & Ink Analysis" title
3. Click "📁 Browse PDF"
4. Select any PDF
5. Click "🔍 Analyze Colors"
6. Results should display (may say "no colors detected" depending on PDF)

### Web App Test

1. Run: `streamlit run color_separation_app.py`
2. Browser should open to `localhost:8501`
3. You should see the color analysis interface
4. Upload a PDF and test the analysis

### CLI Tool Test

1. Run: `python color_analyzer.py sample.pdf`
2. Should output JSON to the console

## Keeping Everything Updated

To update dependencies:

```bash
pip install -r requirements.txt --upgrade
```

## Next Steps

✅ Installation complete!

→ **Next:** Read [USAGE.md](USAGE.md) to learn how to use the application
