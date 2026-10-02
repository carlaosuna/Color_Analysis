#!/usr/bin/env python3
"""
Color Separation & Ink Analysis Tool
Analyzes PDF files for spot colors, CMYK, RGB, and Pantone colors
"""

import pikepdf
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set
import sys

class ColorAnalyzer:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.colors = {
            'spot_colors': set(),
            'cmyk_colors': set(),
            'rgb_colors': set(),
            'device_colors': set(),
            'lab_colors': set()
        }
        self.color_usages = defaultdict(int)
        self.pages_with_colors = defaultdict(set)
        
    def analyze(self) -> Dict:
        """Analyze PDF for colors"""
        try:
            with pikepdf.open(self.pdf_path) as pdf:
                self._extract_colors(pdf)
                return self._generate_report()
        except Exception as e:
            return {'error': str(e)}
    
    def _extract_colors(self, pdf):
        """Extract color information from PDF"""
        # Check document-level resources
        if '/Resources' in pdf.Root:
            self._scan_resources(pdf.Root['/Resources'], 'document', 0)
        
        # Check each page
        for page_num, page in enumerate(pdf.pages, 1):
            if '/Resources' in page:
                self._scan_resources(page['/Resources'], f'page_{page_num}', page_num)
    
    def _scan_resources(self, resources, source: str, page_num: int):
        """Scan a resources dictionary for colors"""
        try:
            # Check ColorSpace
            if '/ColorSpace' in resources:
                cs = resources['/ColorSpace']
                if isinstance(cs, dict):
                    for name, space in cs.items():
                        self._process_colorspace(space, source, page_num)
        except:
            pass
        
        try:
            # Check ExtGState (graphics state - may have colors)
            if '/ExtGState' in resources:
                gs = resources['/ExtGState']
                if isinstance(gs, dict):
                    for name, state in gs.items():
                        if '/ca' in state or '/CA' in state:
                            # Found transparency - may indicate color
                            pass
        except:
            pass
        
        try:
            # Check Shading (gradients)
            if '/Shading' in resources:
                shading = resources['/Shading']
                if isinstance(shading, dict):
                    for name, shade in shading.items():
                        self._process_shading(shade, source, page_num)
        except:
            pass
    
    def _process_colorspace(self, space, source: str, page_num: int):
        """Process a colorspace definition"""
        try:
            if isinstance(space, list):
                # Multi-element colorspace
                cs_type = space[0]
                
                if cs_type == '/DeviceRGB':
                    self.colors['rgb_colors'].add('RGB')
                    self.pages_with_colors[page_num].add('RGB')
                
                elif cs_type == '/DeviceCMYK':
                    self.colors['cmyk_colors'].add('CMYK')
                    self.pages_with_colors[page_num].add('CMYK')
                
                elif cs_type == '/DeviceGray':
                    self.colors['device_colors'].add('Gray')
                    self.pages_with_colors[page_num].add('Gray')
                
                elif cs_type == '/Separation':
                    # Spot color!
                    if len(space) > 1:
                        spot_name = str(space[1]).strip('/')
                        self.colors['spot_colors'].add(spot_name)
                        self.pages_with_colors[page_num].add(f'Spot: {spot_name}')
                        self.color_usages[f'Spot: {spot_name}'] += 1
                
                elif cs_type == '/DeviceN':
                    # DeviceN can be multiple spots
                    if len(space) > 1 and isinstance(space[1], list):
                        for name in space[1]:
                            spot_name = str(name).strip('/')
                            self.colors['spot_colors'].add(spot_name)
                            self.pages_with_colors[page_num].add(f'Spot: {spot_name}')
                
                elif cs_type == '/Lab':
                    self.colors['lab_colors'].add('LAB')
                    self.pages_with_colors[page_num].add('LAB')
                
                elif cs_type == '/ICCBased':
                    # ICC color profile - usually CMYK or RGB
                    self.colors['cmyk_colors'].add('CMYK (ICC)')
                    self.pages_with_colors[page_num].add('CMYK (ICC)')
            
            elif space == '/DeviceRGB':
                self.colors['rgb_colors'].add('RGB')
                self.pages_with_colors[page_num].add('RGB')
            
            elif space == '/DeviceCMYK':
                self.colors['cmyk_colors'].add('CMYK')
                self.pages_with_colors[page_num].add('CMYK')
            
            elif space == '/DeviceGray':
                self.colors['device_colors'].add('Gray')
                self.pages_with_colors[page_num].add('Gray')
        
        except Exception as e:
            pass
    
    def _process_shading(self, shading, source: str, page_num: int):
        """Process shading/gradient definitions"""
        try:
            if '/ColorSpace' in shading:
                self._process_colorspace(shading['/ColorSpace'], source, page_num)
        except:
            pass
    
    def _generate_report(self) -> Dict:
        """Generate analysis report"""
        report = {
            'file': Path(self.pdf_path).name,
            'summary': {
                'spot_colors': list(self.colors['spot_colors']),
                'cmyk': list(self.colors['cmyk_colors']),
                'rgb': list(self.colors['rgb_colors']),
                'device': list(self.colors['device_colors']),
                'lab': list(self.colors['lab_colors']),
            },
            'color_usage': dict(self.color_usages),
            'pages_affected': {int(k): list(v) for k, v in self.pages_with_colors.items()},
            'stats': {
                'total_spot_colors': len(self.colors['spot_colors']),
                'has_cmyk': len(self.colors['cmyk_colors']) > 0,
                'has_rgb': len(self.colors['rgb_colors']) > 0,
                'has_grayscale': len(self.colors['device_colors']) > 0,
            }
        }
        return report
    
    def get_pantone_suggestion(self, color_name: str) -> str:
        """Try to match spot color to Pantone"""
        # Common spot color to Pantone mappings
        pantone_db = {
            'PANTONE': 'PANTONE',
            'PMS': 'PANTONE',
            'Spot': 'Custom Spot Color',
            'Red': 'PMS 200C (Red)',
            'Blue': 'PMS 280C (Blue)',
            'Green': 'PMS 341C (Green)',
            'Yellow': 'PMS 109C (Yellow)',
            'Black': 'Black',
        }
        
        for key, value in pantone_db.items():
            if key.lower() in color_name.lower():
                return value
        
        return 'Unknown / Custom Color'

def main():
    if len(sys.argv) < 2:
        print("Usage: python color_analyzer.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    if not Path(pdf_file).exists():
        print(f"Error: File not found: {pdf_file}")
        sys.exit(1)
    
    analyzer = ColorAnalyzer(pdf_file)
    report = analyzer.analyze()
    
    # Pretty print the report
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
