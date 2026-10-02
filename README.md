# 🎨 Color Separation & Ink Analysis Tool

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive tool for analyzing spot colors, CMYK separations, RGB colors, and color profiles in PDF documents. Created to fill the gap left by Foxit PDF Editor's lack of color separation analysis.

## 🎯 Purpose

When Foxit PDF Editor removed the Separations panel, users lost the ability to analyze color modes and detect spot colors. This tool restores that capability with three deployment options:

- **Desktop Application** - For local analysis and daily workflows
- **Web Application** - For team sharing and browser-based access
- **Command-line Tool** - For scripting and automation

## ✨ Features

- ✅ **Spot Color Detection** - Identifies separations and suggests Pantone matches
- ✅ **CMYK Analysis** - Detects 4-color process color spaces
- ✅ **RGB Detection** - Flags screen colors that need conversion
- ✅ **ICC Profiles** - Recognizes embedded color profiles
- ✅ **Page Mapping** - Shows which pages use which colors
- ✅ **JSON Export** - Generate reports for documentation
- ✅ **Grayscale Detection** - Identify B&W content
- ✅ **Offline Access** - Works without internet connection (desktop version)

## 🚀 Quick Start

### Installation (One-time setup)

```bash
# 1. Install Python 3.8 or higher from python.org

# 2. Install dependencies
pip install -r requirements.txt
```

### Run the Application

**Desktop Version (Recommended):**
```bash
python ColorAnalysisApp.py
```

**Web Version (Browser-based):**
```bash
streamlit run color_separation_app.py
```

**Command-line Tool:**
```bash
python color_analyzer.py document.pdf
```

## 📖 Documentation

- [**INSTALLATION.md**](INSTALLATION.md) - Detailed setup guide with troubleshooting
- [**USAGE.md**](USAGE.md) - How to use each version
- [**QUICK_START.md**](docs/QUICK_START.md) - 5-minute getting started guide

## 🖥️ Application Versions

### Desktop Application (`ColorAnalysisApp.py`)

Perfect for daily use with a graphical interface.

**Features:**
- Drag-and-drop file selection
- Visual results display
- JSON export
- Offline access
- Windows/Mac/Linux support

**Launch:**
```bash
python ColorAnalysisApp.py
# or double-click: RUN_DESKTOP.bat (Windows)
```

### Web Application (`color_separation_app.py`)

Browser-based version for team sharing.

**Features:**
- No installation needed for users
- Shareable URL
- Works on any device with a browser
- Streamlit Cloud deployment option

**Launch:**
```bash
streamlit run color_separation_app.py
# or double-click: RUN_WEB.bat (Windows)
```

**Deploy to Streamlit Cloud:**
1. Fork this repo
2. Connect GitHub to Streamlit Cloud
3. Deploy automatically

### Command-line Tool (`color_analyzer.py`)

For integration with scripts and automation pipelines.

**Usage:**
```bash
python color_analyzer.py /path/to/document.pdf

# Output: JSON report to stdout
```

## 📊 Example Output

```json
{
  "file": "document.pdf",
  "summary": {
    "spot_colors": ["PANTONE 200C", "PANTONE 341C"],
    "cmyk": ["CMYK"],
    "rgb": [],
    "device": [],
    "lab": []
  },
  "stats": {
    "total_spot_colors": 2,
    "has_cmyk": true,
    "has_rgb": false,
    "has_grayscale": false
  },
  "pages_affected": {
    "1": ["Spot: PANTONE 200C", "Spot: PANTONE 341C"],
    "2-50": ["Spot: PANTONE 200C"]
  }
}
```

## 🔄 Workflow Integration

This tool works alongside Foxit PDF Editor:

1. **Edit** in Foxit (general PDF work)
2. **Analyze** with this tool (color verification)
3. **Verify** results against print specifications
4. **Export** report for documentation
5. **Send** to printer with confidence

## 🛠️ Requirements

- Python 3.8 or higher
- pikepdf (for PDF analysis)
- streamlit (for web version only)
- tkinter (usually included with Python)

See `requirements.txt` for all dependencies.

## 📦 Installation Options

### Option 1: Local Installation
```bash
pip install -r requirements.txt
```

### Option 2: Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Option 3: Docker
```bash
docker build -t color-analysis .
docker run -p 8501:8501 color-analysis
```

## 🤝 Support & Issues

- 📖 See [INSTALLATION.md](INSTALLATION.md) for setup issues
- 🐛 Found a bug? [Report an issue](../../issues)
- 💡 Have a suggestion? [Start a discussion](../../discussions)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Created to solve the color separation analysis gap left by Foxit PDF Editor when migrating from Adobe Acrobat Pro.

---

**Ready to get started?** → [Read INSTALLATION.md](INSTALLATION.md)
