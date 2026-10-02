#!/usr/bin/env python3
"""
Color Separation & Ink Analysis - Desktop GUI
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading
from pathlib import Path
import json
import pikepdf
from collections import defaultdict
import webbrowser

class ColorAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Separation & Ink Analysis")
        self.root.geometry("900x700")
        self.root.config(bg="#f0f2f6")
        
        # Color scheme
        self.primary_color = "#c41e3a"
        self.accent_color = "#0052cc"
        self.success_color = "#28a745"
        
        self.selected_file = None
        self.analysis_result = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create UI elements"""
        
        # Header
        header = tk.Frame(self.root, bg=self.primary_color, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="🎨 Color Separation & Ink Analysis",
            font=("Helvetica", 24, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=20)
        
        subtitle = tk.Label(
            header,
            text="Detect spot colors, CMYK, RGB, and Pantone colors",
            font=("Helvetica", 10),
            bg=self.primary_color,
            fg="white"
        )
        subtitle.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f2f6")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Step 1: Upload
        step1_frame = tk.LabelFrame(
            main_frame,
            text="Step 1: Select PDF File",
            font=("Helvetica", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        step1_frame.pack(fill=tk.X, pady=10)
        
        button_frame = tk.Frame(step1_frame, bg="white")
        button_frame.pack(fill=tk.X)
        
        self.browse_btn = tk.Button(
            button_frame,
            text="📁 Browse PDF",
            command=self._browse_file,
            bg=self.accent_color,
            fg="white",
            font=("Helvetica", 10),
            padx=20,
            pady=10
        )
        self.browse_btn.pack(side=tk.LEFT)
        
        self.file_label = tk.Label(
            step1_frame,
            text="No file selected",
            font=("Helvetica", 9),
            fg="#666",
            bg="white"
        )
        self.file_label.pack(pady=10)
        
        # Step 2: Analyze
        step2_frame = tk.LabelFrame(
            main_frame,
            text="Step 2: Analyze",
            font=("Helvetica", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        step2_frame.pack(fill=tk.X, pady=10)
        
        self.analyze_btn = tk.Button(
            step2_frame,
            text="🔍 Analyze Colors",
            command=self._analyze,
            bg=self.success_color,
            fg="white",
            font=("Helvetica", 11, "bold"),
            padx=20,
            pady=12,
            state=tk.DISABLED,
            width=40
        )
        self.analyze_btn.pack()
        
        # Step 3: Results
        step3_frame = tk.LabelFrame(
            main_frame,
            text="Step 3: Results",
            font=("Helvetica", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        step3_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            step3_frame,
            height=15,
            width=80,
            font=("Courier", 9),
            bg="#f9f9f9",
            fg="#333"
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Export button
        export_frame = tk.Frame(self.root, bg="#f0f2f6")
        export_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.export_btn = tk.Button(
            export_frame,
            text="📥 Export Report (JSON)",
            command=self._export,
            bg="#17a2b8",
            fg="white",
            font=("Helvetica", 10),
            padx=20,
            pady=8,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT)
    
    def _browse_file(self):
        """Browse for PDF file"""
        filename = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(
                text=f"✓ {Path(filename).name}",
                fg=self.success_color
            )
            self.analyze_btn.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
    
    def _analyze(self):
        """Analyze selected PDF"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a PDF file first")
            return
        
        self.analyze_btn.config(state=tk.DISABLED)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Analyzing PDF... please wait...\n\n")
        self.root.update()
        
        # Run analysis in thread
        thread = threading.Thread(target=self._run_analysis)
        thread.start()
    
    def _run_analysis(self):
        """Run color analysis"""
        try:
            with pikepdf.open(self.selected_file) as pdf:
                colors = {
                    'spot_colors': set(),
                    'cmyk_colors': set(),
                    'rgb_colors': set(),
                    'device_colors': set(),
                    'lab_colors': set()
                }
                pages_with_colors = defaultdict(set)
                
                # Analyze document
                if '/Resources' in pdf.Root:
                    resources = pdf.Root['/Resources']
                    if '/ColorSpace' in resources:
                        cs = resources['/ColorSpace']
                        if isinstance(cs, dict):
                            for name, space in cs.items():
                                self._process_colorspace(space, colors, pages_with_colors, 0)
                
                # Analyze pages
                for page_num, page in enumerate(pdf.pages, 1):
                    if '/Resources' in page:
                        resources = page['/Resources']
                        try:
                            if '/ColorSpace' in resources:
                                cs = resources['/ColorSpace']
                                if isinstance(cs, dict):
                                    for name, space in cs.items():
                                        self._process_colorspace(space, colors, pages_with_colors, page_num)
                        except:
                            pass
                
                # Build report
                report = self._build_report(
                    colors, pages_with_colors, pdf, self.selected_file
                )
                
                self.analysis_result = report
                self._display_results(report)
                self.export_btn.config(state=tk.NORMAL)
        
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Analysis failed: {str(e)}"))
        
        finally:
            self.root.after(0, lambda: self.analyze_btn.config(state=tk.NORMAL))
    
    def _process_colorspace(self, space, colors, pages, page_num):
        """Process colorspace"""
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
                    colors['cmyk_colors'].add('CMYK (ICC Profile)')
                    pages[page_num].add('CMYK (ICC)')
        except:
            pass
    
    def _build_report(self, colors, pages, pdf, filename):
        """Build analysis report"""
        return {
            'file': Path(filename).name,
            'pages': len(pdf.pages),
            'spot_colors': sorted(list(colors['spot_colors'])),
            'cmyk': list(colors['cmyk_colors']),
            'rgb': list(colors['rgb_colors']),
            'grayscale': list(colors['device_colors']),
            'pages_with_colors': {int(k): sorted(list(v)) for k, v in pages.items()}
        }
    
    def _display_results(self, report):
        """Display results"""
        self.root.after(0, lambda: self._update_results_text(report))
    
    def _update_results_text(self, report):
        """Update results display"""
        self.results_text.delete(1.0, tk.END)
        
        text = "COLOR ANALYSIS REPORT\n"
        text += "=" * 70 + "\n\n"
        
        text += f"File: {report['file']}\n"
        text += f"Total Pages: {report['pages']}\n\n"
        
        text += "SPOT COLORS (SEPARATIONS)\n"
        text += "-" * 70 + "\n"
        if report['spot_colors']:
            for i, color in enumerate(report['spot_colors'], 1):
                pantone = self._suggest_pantone(color)
                text += f"  {i}. {color}\n     → Suggested Pantone: {pantone}\n"
        else:
            text += "  (None detected)\n"
        text += "\n"
        
        text += "COLOR MODES\n"
        text += "-" * 70 + "\n"
        text += f"  CMYK: {'Yes' if report['cmyk'] else 'No'}\n"
        text += f"  RGB: {'Yes' if report['rgb'] else 'No'}\n"
        text += f"  Grayscale: {'Yes' if report['grayscale'] else 'No'}\n"
        text += "\n"
        
        text += "PRINTING NOTES\n"
        text += "-" * 70 + "\n"
        if report['spot_colors']:
            text += f"  ⚠️  {len(report['spot_colors'])} spot color(s) detected.\n"
            text += "     These require separate printing plates.\n"
        if report['rgb']:
            text += "  ⚠️  RGB colors detected - convert to CMYK for print.\n"
        text += "  ✓  Check with print provider before submitting.\n"
        text += "\n"
        
        if report['pages_with_colors']:
            text += "PAGES AFFECTED\n"
            text += "-" * 70 + "\n"
            for page_num in sorted(report['pages_with_colors'].keys()):
                colors = report['pages_with_colors'][page_num]
                text += f"  Page {page_num}: {', '.join(colors)}\n"
        
        self.results_text.insert(tk.END, text)
    
    def _suggest_pantone(self, color_name: str) -> str:
        """Suggest Pantone"""
        pantone_map = {
            'Red': 'PMS 200C',
            'Blue': 'PMS 280C',
            'Green': 'PMS 341C',
            'Yellow': 'PMS 109C',
            'Black': 'Black',
        }
        for key, value in pantone_map.items():
            if key.lower() in color_name.lower():
                return value
        return "Verify with print provider"
    
    def _export(self):
        """Export report as JSON"""
        if not self.analysis_result:
            messagebox.showerror("Error", "No analysis to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.analysis_result, f, indent=2)
                messagebox.showinfo("Success", f"Report exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")

def main():
    root = tk.Tk()
    app = ColorAnalysisApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
