# Usage Guide

## Quick Reference

| Task | Command |
|------|---------|
| Desktop App | `python ColorAnalysisApp.py` or `RUN_DESKTOP.bat` |
| Web App | `streamlit run color_separation_app.py` or `RUN_WEB.bat` |
| CLI Tool | `python color_analyzer.py document.pdf` |

---

## Desktop Application

### Launch

```bash
python ColorAnalysisApp.py
```

Or Windows users: Double-click `RUN_DESKTOP.bat`

### Usage Steps

**Step 1: Select PDF File**
- Click "📁 Browse PDF"
- Navigate to your PDF file
- Click "Open"
- Filename appears below the button

**Step 2: Analyze**
- Click "🔍 Analyze Colors"
- Wait for results (5-30 seconds depending on PDF size)
- Application will show analysis in the text area

**Step 3: Review Results**

Results display as:
```
COLOR ANALYSIS REPORT
=====================

SPOT COLORS (SEPARATIONS)
  1. PANTONE 200C
  2. PANTONE 341C
     → Suggested Pantone: PMS 280C

COLOR MODES
  CMYK: Yes
  RGB: No
  Grayscale: No

PAGES AFFECTED
  Page 1-50: PANTONE 200C, PANTONE 341C
```

**Step 4: Export (Optional)**
- Click "📥 Export Report (JSON)"
- Choose location to save
- JSON file with analysis is saved

### Understanding Results

**✅ SPOT COLORS (GOOD for print)**
- Each spot color requires a separate printing plate
- Pantone suggestions help identify color standards
- Example: Use for school branding, limited-color printing

**✅ CMYK (GOOD for print)**
- 4-color process (Cyan, Magenta, Yellow, Black)
- Standard for full-color printing
- Photos and complex colors use this

**⚠️ RGB (PROBLEM for print)**
- Screen colors only
- Must be converted to CMYK before printing
- If detected, return to designer for conversion

**✅ GRAYSCALE (OK)**
- Black and white content
- Standard for B&W printing

### Keyboard Shortcuts

- `Ctrl+C` - Copy selected text from results
- `Ctrl+A` - Select all text in results
- `Ctrl+Q` - Quit application (close window)

---

## Web Application

### Launch

```bash
streamlit run color_separation_app.py
```

Or Windows users: Double-click `RUN_WEB.bat`

Browser automatically opens to `http://localhost:8501`

### Usage Steps

**Step 1: Upload PDF**
- Click upload box or drag-drop a PDF
- File immediately appears below
- Shows filename in green checkmark

**Step 2: Select Workflow**
- Choose workflow type (currently only one option)

**Step 3: Analyze**
- Click "🚀 Process PDFs"
- Spinner appears while analyzing
- Results display below

**Step 4: Review**
- See metrics at top (spot colors, CMYK, RGB, pages)
- Expandable sections for detailed info:
  - Spot Colors Found
  - CMYK Details
  - RGB Warnings
  - Pages Affected

**Step 5: Download Report**
- Click "📥 Download Analysis Report (JSON)"
- JSON file downloads to your computer

### Sharing the Web App

To share with team members:

**Option 1: Local Network**
```
Find your computer's IP:
Windows: ipconfig (look for IPv4 Address)
Mac: ifconfig (look for inet)

Share this URL: http://YOUR_IP:8501
Team members on same network can access it
```

**Option 2: Streamlit Cloud (Public)**
1. Push code to GitHub
2. Connect repo to Streamlit Cloud
3. Streamlit automatically deploys
4. Get public URL to share: `https://yourapp.streamlit.app`

### Tips

- App works in any modern browser (Chrome, Safari, Firefox, Edge)
- Files are temporary and deleted after download
- No files stored on server

---

## Command-Line Tool

### Basic Usage

```bash
python color_analyzer.py document.pdf
```

### Output

Outputs JSON to console:

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
  }
}
```

### Advanced Usage

**Save output to file:**
```bash
python color_analyzer.py document.pdf > report.json
```

**Batch process multiple PDFs:**
```bash
for pdf in *.pdf; do
    python color_analyzer.py "$pdf" > "${pdf%.pdf}_analysis.json"
done
```

**Process and pipe to another tool:**
```bash
python color_analyzer.py document.pdf | jq '.summary.spot_colors'
```

---

## Real-World Examples

### Example 1: K-12 Textbook

**File:** `Textbook_Ch1.pdf`

**Steps:**
1. Open Desktop App
2. Select the PDF
3. Click "Analyze Colors"

**Results:**
```
SPOT COLORS: 2
  1. School Blue (PMS 280C)
  2. School Gold (PMS 109C)

PAGES AFFECTED: 1-200 (all use same colors)
```

**Action:** ✅ Print ready! Colors match school branding.

---

### Example 2: Design With RGB Colors

**File:** `Promotional_Poster.pdf`

**Steps:**
1. Open Desktop App
2. Select the PDF
3. Click "Analyze Colors"

**Results:**
```
RGB: Yes (screen colors detected)
CMYK: No
```

**Action:** ⚠️ Not print-ready! Send back to designer to convert RGB → CMYK

---

### Example 3: Full-Color Photo Book

**File:** `AnnualReport_2024.pdf`

**Steps:**
1. Open Web App
2. Upload PDF
3. Click "Analyze"

**Results:**
```
CMYK: Yes (4-color process)
PAGES: 100
```

**Action:** ✅ Print ready for full-color printing!

---

## Interpreting Color Modes

### Spot Colors
- **When to use:** School colors, logos, limited-color printing
- **Cost impact:** One plate per color
- **Print method:** Offset, screen printing
- **Best for:** K-12 materials with specific brand colors

### CMYK
- **When to use:** Photos, complex graphics, full color
- **Cost impact:** Fixed 4-color cost
- **Print method:** Offset printing, digital print
- **Best for:** Annual reports, catalogs, photo books

### RGB
- **When to use:** Screen/web only
- **Print issue:** Must convert to CMYK first
- **Color shift:** RGB to CMYK conversion always shifts colors
- **Action needed:** Return to designer for conversion

### Grayscale
- **When to use:** B&W documents, cost savings
- **Cost impact:** Cheapest option
- **Print method:** Any press
- **Best for:** Internal documents, forms, textbooks

---

## Export Format

### JSON Report Structure

```json
{
  "file": "filename.pdf",
  "pages": 50,
  "spot_colors": ["color1", "color2"],
  "cmyk": ["CMYK"],
  "rgb": [],
  "grayscale": [],
  "pages_with_colors": {
    "1": ["Spot: color1", "Spot: color2"],
    "2": ["Spot: color1"]
  }
}
```

### Importing Reports

JSON files can be:
- Stored in version control
- Imported into print management systems
- Attached to work orders
- Used for quality control documentation

---

## Troubleshooting

### App runs but shows "No colors detected"

**Reason:** PDF stores colors in a format we don't analyze yet

**Solution:** Check with printer - PDF may still be valid for print

### Results differ from Adobe

**Reason:** Different analysis methods

**Solution:** Trust your print provider's analysis - send them the PDF directly

### Web app is slow

**Reason:** Large PDF or slow internet

**Solution:** 
- Try desktop version instead
- Break large PDFs into smaller parts

### Can't open file

**Reason:** File corruption or unsupported format

**Solution:**
- Try opening in Adobe or Foxit first
- Regenerate PDF from source if possible

---

## Next Steps

✅ You're ready to use the application!

- **Desktop users:** Run daily for color verification
- **Web users:** Share URL with team for quick analysis
- **Automation users:** Integrate CLI tool into workflows

Questions? Check [README.md](README.md) or [INSTALLATION.md](INSTALLATION.md)
