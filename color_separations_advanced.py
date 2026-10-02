import streamlit as st
import tempfile
from pathlib import Path
import json
import pandas as pd
import pikepdf
import re

st.set_page_config(
    page_title="Color Separation Analysis",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
    <style>
    .header {
        background: linear-gradient(135deg, #c41e3a 0%, #d5576b 100%);
        padding: 40px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .header h1 {
        margin: 0;
        font-size: 2.5em;
    }
    .stat-box {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
        border-left: 5px solid #0052cc;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header">
        <h1>🎨 Color Separation & Ink Analysis</h1>
        <p>Adobe Separations Panel Equivalent - Advanced Content Stream Parsing</p>
    </div>
""", unsafe_allow_html=True)

def extract_colors_from_content(content_bytes):
    """Extract CMYK and RGB colors from PDF content stream"""
    colors = []
    
    try:
        content_str = content_bytes.decode('latin-1', errors='ignore')
        
        # Pattern 1: CMYK color (k = fill, K = stroke)
        # Format: c m y k k (or K)
        cmyk_pattern = r'([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+[kK]'
        
        for match in re.finditer(cmyk_pattern, content_str):
            c, m, y, k = [float(x) for x in match.groups()]
            colors.append({
                'type': 'CMYK',
                'c': c,
                'm': m,
                'y': y,
                'k': k,
                'coverage': round((c + m + y + k) * 25, 1)  # Average coverage
            })
        
        # Pattern 2: RGB color (rg = fill, RG = stroke)
        # Format: r g b rg (or RG)
        rgb_pattern = r'([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+[rR][gG]'
        
        for match in re.finditer(rgb_pattern, content_str):
            r, g, b = [float(x) for x in match.groups()]
            colors.append({
                'type': 'RGB',
                'r': r,
                'g': g,
                'b': b,
                'coverage': round((r + g + b) * 33.33, 1)
            })
    
    except Exception as e:
        pass
    
    return colors

st.markdown("---")

# Upload section
st.markdown("### 📥 Upload PDF")
uploaded_file = st.file_uploader("Select a PDF to analyze", type="pdf")

if uploaded_file:
    st.success(f"✓ File selected: {uploaded_file.name}")
    
    if st.button("🔍 Analyze Separations", use_container_width=True, type="primary"):
        with st.spinner("Analyzing color separations..."):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir) / "temp.pdf"
                    temp_path.write_bytes(uploaded_file.read())
                    
                    # Analyze
                    with pikepdf.open(str(temp_path)) as pdf:
                        separations = []
                        has_cmyk = False
                        has_rgb = False
                        total_coverage = 0
                        
                        # Extract colors from content streams
                        all_colors = []
                        
                        for page_num, page in enumerate(pdf.pages, 1):
                            if '/Contents' in page:
                                try:
                                    contents = page['/Contents']
                                    if hasattr(contents, 'read_bytes'):
                                        content_bytes = contents.read_bytes()
                                        colors = extract_colors_from_content(content_bytes)
                                        all_colors.extend(colors)
                                except:
                                    pass
                        
                        # Also check ColorSpace resources
                        if '/Resources' in pdf.Root:
                            resources = pdf.Root['/Resources']
                            if '/ColorSpace' in resources:
                                cs = resources['/ColorSpace']
                                if isinstance(cs, dict):
                                    for name, space in cs.items():
                                        if isinstance(space, list):
                                            cs_type = space[0]
                                            if cs_type == '/DeviceCMYK':
                                                has_cmyk = True
                                            elif cs_type == '/DeviceRGB':
                                                has_rgb = True
                        
                        # Check page resources
                        for page in pdf.pages:
                            if '/Resources' in page:
                                resources = page['/Resources']
                                try:
                                    if '/ColorSpace' in resources:
                                        cs = resources['/ColorSpace']
                                        if isinstance(cs, dict):
                                            for name, space in cs.items():
                                                if isinstance(space, list):
                                                    cs_type = space[0]
                                                    if cs_type == '/DeviceCMYK':
                                                        has_cmyk = True
                                                    elif cs_type == '/DeviceRGB':
                                                        has_rgb = True
                                except:
                                    pass
                        
                        # Build separations from detected colors
                        if all_colors:
                            cmyk_colors = [c for c in all_colors if c['type'] == 'CMYK']
                            rgb_colors = [c for c in all_colors if c['type'] == 'RGB']
                            
                            if cmyk_colors:
                                has_cmyk = True
                                # Get unique CMYK values
                                unique_cmyk = {}
                                for color in cmyk_colors:
                                    key = (round(color['c'], 2), round(color['m'], 2), 
                                           round(color['y'], 2), round(color['k'], 2))
                                    if key not in unique_cmyk:
                                        unique_cmyk[key] = color
                                
                                # Create separations for each CMYK component
                                if unique_cmyk:
                                    for key, color in unique_cmyk.items():
                                        c, m, y, k = key
                                        
                                        # Add individual CMYK separations
                                        if c > 0:
                                            separations.append({
                                                'name': 'Process Cyan',
                                                'type': 'Process',
                                                'coverage': round(c * 100, 1)
                                            })
                                        if m > 0:
                                            separations.append({
                                                'name': 'Process Magenta',
                                                'type': 'Process',
                                                'coverage': round(m * 100, 1)
                                            })
                                        if y > 0:
                                            separations.append({
                                                'name': 'Process Yellow',
                                                'type': 'Process',
                                                'coverage': round(y * 100, 1)
                                            })
                                        if k > 0:
                                            separations.append({
                                                'name': 'Process Black',
                                                'type': 'Process',
                                                'coverage': round(k * 100, 1)
                                            })
                                    
                                    # Calculate total coverage
                                    if unique_cmyk:
                                        key = list(unique_cmyk.keys())[0]
                                        c, m, y, k = key
                                        total_coverage = round((c + m + y + k) * 100, 1)
                            
                            if rgb_colors:
                                has_rgb = True
                                for color in rgb_colors:
                                    separations.append({
                                        'name': f"RGB Color ({round(color['r']*100)}% R, {round(color['g']*100)}% G, {round(color['b']*100)}% B)",
                                        'type': 'RGB',
                                        'coverage': color['coverage']
                                    })
                        
                        # If no colors found, show message
                        if not separations:
                            st.info("⚠️ No colors detected in content stream or resources. PDF may contain only grayscale or embedded images.")
                            separations = []
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("### 📊 Separations (Adobe Format)")
                        
                        # Metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            process_count = len([s for s in separations if s['type'] == 'Process'])
                            st.metric("Process Colors", process_count)
                        with col2:
                            spot_count = len([s for s in separations if s['type'] == 'Spot'])
                            st.metric("Spot Colors", spot_count)
                        with col3:
                            st.metric("Total Coverage", f"{total_coverage}%")
                        
                        st.markdown("---")
                        
                        if separations:
                            # Separations table
                            st.markdown("**Separations List:**")
                            
                            # Create dataframe
                            df_data = []
                            for sep in separations:
                                df_data.append({
                                    'Name': sep['name'],
                                    'Type': sep['type'],
                                    'Coverage %': sep['coverage'],
                                })
                            
                            df = pd.DataFrame(df_data)
                            
                            # Display table
                            st.dataframe(
                                df,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "Name": st.column_config.TextColumn("Name", width="medium"),
                                    "Type": st.column_config.TextColumn("Type", width="small"),
                                    "Coverage %": st.column_config.NumberColumn("Coverage %", format="%.1f%%", width="small"),
                                }
                            )
                        
                        st.markdown("---")
                        
                        # Summary
                        st.markdown("### 📋 Summary")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            color_mode = ""
                            if has_cmyk:
                                color_mode += "✓ CMYK (Process Colors)<br>"
                            if has_rgb:
                                color_mode += "✓ RGB (Screen Colors)<br>"
                            if not has_cmyk and not has_rgb:
                                color_mode += "⚠️ No colors detected<br>"
                            
                            st.markdown(f"""
                                <div class="stat-box">
                                    <strong>Color Mode</strong><br>
                                    {color_mode}
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            process_count = len([s for s in separations if s['type'] == 'Process'])
                            spot_count = len([s for s in separations if s['type'] == 'Spot'])
                            
                            st.markdown(f"""
                                <div class="stat-box">
                                    <strong>Printing Summary</strong><br>
                                    • Total separations: {len(separations)}<br>
                                    • Process plates: {process_count}<br>
                                    • Spot plates: {spot_count}<br>
                                    • Total coverage: {total_coverage}%
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Export
                        st.markdown("---")
                        
                        export_data = {
                            'file': uploaded_file.name,
                            'total_pages': len(pdf.pages),
                            'separations': df_data if separations else [],
                            'total_coverage': total_coverage,
                            'has_process': has_cmyk,
                            'has_rgb': has_rgb,
                        }
                        
                        st.download_button(
                            label="📥 Download Separations Report (JSON)",
                            data=json.dumps(export_data, indent=2),
                            file_name=f"{Path(uploaded_file.name).stem}_separations.json",
                            mime="application/json"
                        )
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 40px;">
        <p><strong>Color Separation & Ink Analysis</strong></p>
        <p>Advanced PDF color analysis with content stream parsing</p>
        <p style="font-size: 0.85em; color: #999;">Now detects colors embedded in PDF content streams</p>
    </div>
""", unsafe_allow_html=True)
