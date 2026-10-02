# Creating Batch Files (Windows Launchers)

Batch files (.bat) are simple Windows scripts. GitHub may not download them due to security settings. Here's how to create them manually:

## Option 1: Manual Creation (5 seconds)

### Create RUN_DESKTOP.bat

1. Open Notepad
2. Copy and paste this exactly:
```batch
@echo off
python ColorAnalysisApp.py
pause
```

3. Go to File → Save As
4. Filename: `RUN_DESKTOP.bat`
5. Save type: **All Files (*.*)**
6. Click Save

### Create RUN_WEB.bat

1. Open Notepad
2. Copy and paste this exactly:
```batch
@echo off
streamlit run color_separation_app.py
pause
```

3. Go to File → Save As
4. Filename: `RUN_WEB.bat`
5. Save type: **All Files (*.*)**
6. Click Save

**That's it!** Now double-click either .bat file to run the app.

---

## Option 2: Using Python to Create Them

If you prefer, run this Python script in your project folder:

```python
# create_launchers.py
import os

# Create RUN_DESKTOP.bat
with open('RUN_DESKTOP.bat', 'w') as f:
    f.write('@echo off\n')
    f.write('python ColorAnalysisApp.py\n')
    f.write('pause\n')

# Create RUN_WEB.bat
with open('RUN_WEB.bat', 'w') as f:
    f.write('@echo off\n')
    f.write('streamlit run color_separation_app.py\n')
    f.write('pause\n')

print("✓ Created RUN_DESKTOP.bat")
print("✓ Created RUN_WEB.bat")
```

Run it:
```bash
python create_launchers.py
```

---

## Option 3: Command Prompt

Open Command Prompt in your project folder and run:

```cmd
echo @echo off > RUN_DESKTOP.bat
echo python ColorAnalysisApp.py >> RUN_DESKTOP.bat
echo pause >> RUN_DESKTOP.bat

echo @echo off > RUN_WEB.bat
echo streamlit run color_separation_app.py >> RUN_WEB.bat
echo pause >> RUN_WEB.bat
```

---

## Verifying the Files

After creating, you should see:
- RUN_DESKTOP.bat (icon looks like a gear/script)
- RUN_WEB.bat (icon looks like a gear/script)

Double-click to test!

---

## Alternative: Skip the Batch Files

You don't need batch files if you prefer command line:

**Desktop App:**
```bash
python ColorAnalysisApp.py
```

**Web App:**
```bash
streamlit run color_separation_app.py
```

Batch files are just convenient shortcuts for Windows users who prefer not to use command line.
