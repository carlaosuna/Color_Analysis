import streamlit as st
import tempfile
from pathlib import Path
import json
import pikepdf
from collections import defaultdict

st.set_page_config(
    page_title="Color Separation & Ink Analysis",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
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
    .color-swatch {
        display: inline-block;
        width: 60px;
        height: 60px;
        border-radius: 5px;
        margin: 5px;
        border: 2px solid #ddd;
    }
    .spot-color {
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
        color: white;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .cmyk-color {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
        color: white;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .rgb-color {
        background: linear-gradient(135deg, #FFB347, #FFA500);
        color: white;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
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
        <p>Detect spot colors, CMYK, RGB, and Pantone colors in your PDFs</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Upload section
st.markdown("### 📥 Upload PDF")
uploaded_file = st.file_uploader("Select a PDF file to analyze", type="pdf")

if uploaded_file:
    st.success(f"✓ File selected: {uploaded_file.name}")
    
    if st.button("🔍 Analyze Colors", use_container_width=True, type="primary"):
        with st.spinner("Analyzing colors in your PDF..."):
            try:
                # Save uploaded file temporarily
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir) / "temp.pdf"
                    temp_path.write_bytes(uploaded_file.read())
                    
                    # Analyze
                    with pikepdf.open(str(temp_path)) as pdf:
                        colors = {
                            'spot_colors': set(),
                            'cmyk_colors': set(),
                            'rgb_colors': set(),
                            'device_colors': set(),
                            'lab_colors': set()
                        }
                        pages_with_colors = defaultdict(set)
                        
                        # Check document-level
                        if '/Resources' in pdf.Root:
                            resources = pdf.Root['/Resources']
                            if '/ColorSpace' in resources:
                                cs = resources['/ColorSpace']
                                if isinstance(cs, dict):
                                    for name, space in cs.items():
                                        _process_colorspace(space, colors, pages_with_colors, 0)
                        
                        # Check each page
                        for page_num, page in enumerate(pdf.pages, 1):
                            if '/Resources' in page:
                                resources = page['/Resources']
                                try:
                                    if '/ColorSpace' in resources:
                                        cs = resources['/ColorSpace']
                                        if isinstance(cs, dict):
                                            for name, space in cs.items():
                                                _process_colorspace(space, colors, pages_with_colors, page_num)
                                except:
                                    pass
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("### 📊 Analysis Results")
                        
                        # Metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Spot Colors", len(colors['spot_colors']))
                        with col2:
                            st.metric("CMYK", "Yes" if colors['cmyk_colors'] else "No")
                        with col3:
                            st.metric("RGB", "Yes" if colors['rgb_colors'] else "No")
                        with col4:
                            st.metric("Total Pages", len(pdf.pages))
                        
                        st.markdown("---")
                        
                        # Spot Colors
                        if colors['spot_colors']:
                            st.markdown("### 🎨 Spot Colors (Separations)")
                            for color in sorted(colors['spot_colors']):
                                pantone = suggest_pantone(color)
                                st.markdown(f"""
                                    <div class="spot-color">
                                        <strong>{color}</strong><br>
                                        Suggested: {pantone}
                                    </div>
                                """, unsafe_allow_html=True)
                            st.info(f"⚠️ This PDF uses {len(colors['spot_colors'])} spot color(s) that require separate plates for printing.")
                        
                        # CMYK
                        if colors['cmyk_colors']:
                            st.markdown("### 📐 CMYK Colors")
                            st.markdown(f"""
                                <div class="cmyk-color">
                                    <strong>CMYK Color Space Detected</strong><br>
                                    Color separations: Cyan, Magenta, Yellow, Black
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # RGB
                        if colors['rgb_colors']:
                            st.markdown("### 🌈 RGB Colors")
                            st.markdown(f"""
                                <div class="rgb-color">
                                    <strong>RGB Color Space Detected</strong><br>
                                    Screen colors (convert to CMYK for print)
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Pages affected
                        if pages_with_colors:
                            st.markdown("### 📄 Pages with Colors")
                            with st.expander("View affected pages"):
                                for page_num in sorted(pages_with_colors.keys()):
                                    color_list = ", ".join(sorted(pages_with_colors[page_num]))
                                    st.text(f"Page {page_num}: {color_list}")
                        
                        # Summary
                        st.markdown("---")
                        st.markdown("### 📋 Summary")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                                <div class="stat-box">
                                    <strong>Color Mode</strong><br>
                                    {"Spot Color (Separation)" if colors['spot_colors'] else ""}
                                    {"CMYK" if colors['cmyk_colors'] else ""}
                                    {"RGB" if colors['rgb_colors'] else ""}
                                    {"Grayscale" if colors['device_colors'] else ""}
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                                <div class="stat-box">
                                    <strong>Printing Notes</strong><br>
                                    • Spot colors require separate plates<br>
                                    • RGB must be converted for print<br>
                                    • Check color profiles
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Export button
                        st.markdown("---")
                        report = {
                            'file': uploaded_file.name,
                            'spot_colors': list(colors['spot_colors']),
                            'cmyk': list(colors['cmyk_colors']),
                            'rgb': list(colors['rgb_colors']),
                            'grayscale': list(colors['device_colors']),
                            'total_pages': len(pdf.pages)
                        }
                        
                        st.download_button(
                            label="📥 Download Analysis Report (JSON)",
                            data=json.dumps(report, indent=2),
                            file_name=f"{Path(uploaded_file.name).stem}_color_analysis.json",
                            mime="application/json"
                        )
            
            except Exception as e:
                st.error(f"❌ Error analyzing PDF: {str(e)}")

st.markdown("---")

# Footer
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 40px;">
        <p><strong>Color Separation & Ink Analysis Tool</strong></p>
        <p>Analyze spot colors, CMYK, RGB, and color profiles in your PDFs</p>
        <p style="font-size: 0.85em; color: #999;">Files are temporary and not stored</p>
    </div>
""", unsafe_allow_html=True)

def _process_colorspace(space, colors, pages, page_num):
    """Process colorspace definition"""
    try:
        if isinstance(space, list):
            cs_type = space[0]
            
            if cs_type == '/DeviceRGB':
                colors['rgb_colors'].add('RGB')
                pages[page_num].add('RGB')
            elif cs_type == '/DeviceCMYK':
                colors['cmyk_colors'].add('CMYK')
                pages[page_num].add('CMYK')
            elif cs_type == '/DeviceGray':
                colors['device_colors'].add('Gray')
                pages[page_num].add('Gray')
            elif cs_type == '/Separation':
                if len(space) > 1:
                    spot_name = str(space[1]).strip('/')
                    colors['spot_colors'].add(spot_name)
                    pages[page_num].add(f'Spot: {spot_name}')
            elif cs_type == '/DeviceN':
                if len(space) > 1 and isinstance(space[1], list):
                    for name in space[1]:
                        spot_name = str(name).strip('/')
                        colors['spot_colors'].add(spot_name)
                        pages[page_num].add(f'Spot: {spot_name}')
            elif cs_type == '/ICCBased':
                colors['cmyk_colors'].add('CMYK (ICC)')
                pages[page_num].add('CMYK (ICC)')
        else:
            if space == '/DeviceRGB':
                colors['rgb_colors'].add('RGB')
            elif space == '/DeviceCMYK':
                colors['cmyk_colors'].add('CMYK')
            elif space == '/DeviceGray':
                colors['device_colors'].add('Gray')
    except:
        pass

def suggest_pantone(color_name: str) -> str:
    """Suggest Pantone match"""
    pantone_map = {
        'Red': 'PMS 200C',
        'Blue': 'PMS 280C',
        'Green': 'PMS 341C',
        'Yellow': 'PMS 109C',
        'Black': 'Black',
        'Purple': 'PMS 268C',
        'Orange': 'PMS 021C',
        'Pink': 'PMS 217C',
    }
    
    for key, value in pantone_map.items():
        if key.lower() in color_name.lower():
            return value
    
    return "⚠️ Custom/Unknown - Verify with print provider"
