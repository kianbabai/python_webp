import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
from pathlib import Path
import threading

class WebPConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to WebP Converter")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        self.files = []
        self.output_folder = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="🖼️ Image to WebP Converter", 
                         font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Select Images Button
        select_btn = ttk.Button(main_frame, text="Select Images", 
                               command=self.select_images, width=25)
        select_btn.grid(row=1, column=0, pady=5, sticky=tk.W)
        
        # Selected files label
        self.files_label = ttk.Label(main_frame, text="No images selected", 
                                    foreground="gray")
        self.files_label.grid(row=1, column=1, padx=(10, 0), sticky=tk.W)
        
        # Output folder
        output_btn = ttk.Button(main_frame, text="Select Output Folder", 
                               command=self.select_output, width=25)
        output_btn.grid(row=2, column=0, pady=5, sticky=tk.W)
        
        self.output_label = ttk.Label(main_frame, text="Same as source", 
                                     foreground="gray")
        self.output_label.grid(row=2, column=1, padx=(10, 0), sticky=tk.W)
        
        # Quality setting
        quality_frame = ttk.LabelFrame(main_frame, text="Quality Settings", 
                                      padding="10")
        quality_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        ttk.Label(quality_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W)
        
        self.quality_var = tk.IntVar(value=80)
        self.quality_label = ttk.Label(quality_frame, text="80%", 
                                      font=("Segoe UI", 10, "bold"))
        self.quality_label.grid(row=0, column=2, padx=(10, 0))
        
        quality_slider = ttk.Scale(quality_frame, from_=1, to=100, 
                                  variable=self.quality_var, 
                                  orient=tk.HORIZONTAL, length=400,
                                  command=self.update_quality_label)
        quality_slider.grid(row=0, column=1, padx=10)
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, pady=(0, 20), 
                          sticky=(tk.W, tk.E))
        
        self.keep_original = tk.BooleanVar(value=True)
        keep_check = ttk.Checkbutton(options_frame, 
                                    text="Keep original files", 
                                    variable=self.keep_original)
        keep_check.grid(row=0, column=0, sticky=tk.W)
        
        self.lossless = tk.BooleanVar(value=False)
        lossless_check = ttk.Checkbutton(options_frame, 
                                        text="Lossless compression", 
                                        variable=self.lossless)
        lossless_check.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert to WebP", 
                                     command=self.start_conversion,
                                     state=tk.DISABLED)
        self.convert_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=560)
        self.progress.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready", 
                                     foreground="blue")
        self.status_label.grid(row=7, column=0, columnspan=2)
        
    def update_quality_label(self, value):
        self.quality_label.config(text=f"{int(float(value))}%")
        
    def select_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            self.files = list(files)
            self.files_label.config(text=f"{len(self.files)} image(s) selected")
            self.convert_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Ready to convert", foreground="blue")
            
    def select_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            # Truncate path if too long
            display_path = folder if len(folder) < 40 else "..." + folder[-37:]
            self.output_label.config(text=display_path)
            
    def start_conversion(self):
        if not self.files:
            messagebox.showwarning("No Files", "Please select images to convert.")
            return
            
        self.convert_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        
        # Run conversion in separate thread
        thread = threading.Thread(target=self.convert_images, daemon=True)
        thread.start()
        
    def convert_images(self):
        total = len(self.files)
        success = 0
        failed = 0
        
        for i, file_path in enumerate(self.files):
            try:
                self.status_label.config(
                    text=f"Converting {i+1}/{total}: {Path(file_path).name}"
                )
                
                # Open image
                img = Image.open(file_path)
                
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGBA')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Determine output path
                if self.output_folder:
                    output_dir = self.output_folder
                else:
                    output_dir = os.path.dirname(file_path)
                
                # Create output filename
                base_name = Path(file_path).stem
                output_path = os.path.join(output_dir, f"{base_name}.webp")
                
                # Save as WebP
                save_kwargs = {
                    'format': 'WEBP',
                    'quality': self.quality_var.get()
                }
                
                if self.lossless.get():
                    save_kwargs['lossless'] = True
                    save_kwargs.pop('quality')
                
                img.save(output_path, **save_kwargs)
                
                # Delete original if requested
                if not self.keep_original.get():
                    os.remove(file_path)
                
                success += 1
                
            except Exception as e:
                failed += 1
                print(f"Error converting {file_path}: {e}")
            
            # Update progress
            progress = ((i + 1) / total) * 100
            self.progress['value'] = progress
            self.root.update_idletasks()
        
        # Show completion message
        self.progress['value'] = 100
        
        if failed == 0:
            self.status_label.config(
                text=f"✓ Successfully converted {success} image(s)", 
                foreground="green"
            )
            messagebox.showinfo("Success", 
                              f"Successfully converted {success} image(s)!")
        else:
            self.status_label.config(
                text=f"Converted {success}, Failed {failed}", 
                foreground="orange"
            )
            messagebox.showwarning("Completed with errors", 
                                 f"Converted: {success}\nFailed: {failed}")
        
        self.convert_btn.config(state=tk.NORMAL)
        self.files = []
        self.files_label.config(text="No images selected")
        self.progress['value'] = 0

def main():
    root = tk.Tk()
    app = WebPConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()