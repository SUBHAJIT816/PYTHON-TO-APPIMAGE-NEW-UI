import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import shutil
import urllib.request
import tempfile
import venv
from PIL import Image, ImageTk
import threading

class ModernAppImageIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("AppImage Maker IDE - Professional")
        self.root.geometry("700x650")
        self.root.configure(bg='#2b2b2b')
        
        # Set theme colors
        self.bg_color = '#2b2b2b'
        self.card_color = '#3c3f41'
        self.accent_color = '#4CAF50'
        self.text_color = '#ffffff'
        self.highlight_color = '#6d4c41'
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="AppImage Maker Pro", 
                              font=('Arial', 20, 'bold'),
                              fg=self.accent_color,
                              bg=self.bg_color)
        title_label.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=20, pady=5)
        
        # Main container with notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Basic Info Tab
        basic_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(basic_frame, text="Basic Information")
        
        # App Details Card
        details_card = self.create_card(basic_frame, "App Details")
        
        self.create_labeled_entry(details_card, "App Name:", "app_name", 0)
        self.create_labeled_entry(details_card, "Version:", "version", 1)
        self.create_labeled_entry(details_card, "Description:", "description", 2)
        
        # Files Tab
        files_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(files_frame, text="Files & Assets")
        
        # Files Card
        files_card = self.create_card(files_frame, "Required Files")
        
        # Icon upload with preview
        icon_frame = tk.Frame(files_card, bg=self.card_color)
        icon_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=10)
        
        tk.Button(icon_frame, 
                 text="📁 Upload Icon (PNG/JPG)", 
                 command=self.upload_icon,
                 bg=self.highlight_color,
                 fg=self.text_color,
                 font=('Arial', 10),
                 relief='flat',
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        self.icon_path = tk.StringVar()
        self.icon_preview_label = tk.Label(icon_frame, text="No icon selected", 
                                          bg=self.card_color, fg='#888888')
        self.icon_preview_label.pack(side=tk.LEFT, padx=10)
        
        # Python code upload
        code_frame = tk.Frame(files_card, bg=self.card_color)
        code_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
        
        tk.Button(code_frame, 
                 text="🐍 Upload Python Code", 
                 command=self.upload_code,
                 bg='#1976D2',
                 fg=self.text_color,
                 font=('Arial', 10),
                 relief='flat',
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        self.code_path = tk.StringVar()
        self.code_label = tk.Label(code_frame, text="No code file selected", 
                                  bg=self.card_color, fg='#888888')
        self.code_label.pack(side=tk.LEFT, padx=10)
        
        # Requirements upload
        req_frame = tk.Frame(files_card, bg=self.card_color)
        req_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
        
        tk.Button(req_frame, 
                 text="📦 Upload Requirements", 
                 command=self.upload_req,
                 bg='#FF9800',
                 fg=self.text_color,
                 font=('Arial', 10),
                 relief='flat',
                 padx=15,
                 pady=8).pack(side=tk.LEFT, padx=5)
        
        self.req_path = tk.StringVar()
        self.req_label = tk.Label(req_frame, text="No requirements file selected", 
                                 bg=self.card_color, fg='#888888')
        self.req_label.pack(side=tk.LEFT, padx=10)
        
        # Output Tab
        output_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(output_frame, text="Output & Logs")
        
        # Log output area
        log_card = self.create_card(output_frame, "Build Log")
        self.log_text = tk.Text(log_card, 
                               height=15, 
                               bg='#1e1e1e', 
                               fg='#00ff00',
                               font=('Consolas', 10),
                               relief='flat')
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create button
        create_btn = tk.Button(self.root, 
                              text="🚀 CREATE APPIMAGE", 
                              command=self.start_create_appimage,
                              bg=self.accent_color,
                              fg=self.text_color,
                              font=('Arial', 14, 'bold'),
                              relief='flat',
                              padx=30,
                              pady=15)
        create_btn.pack(pady=20)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to create AppImage")
        status_bar = tk.Label(self.root, 
                             textvariable=self.status_var,
                             bg=self.bg_color,
                             fg=self.text_color,
                             font=('Arial', 9))
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def create_card(self, parent, title):
        card = tk.Frame(parent, bg=self.card_color, relief='raised', bd=1)
        card.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = tk.Label(card, 
                              text=title,
                              font=('Arial', 12, 'bold'),
                              bg=self.card_color,
                              fg=self.text_color)
        title_label.pack(anchor='w', padx=15, pady=10)
        
        content_frame = tk.Frame(card, bg=self.card_color)
        content_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        return content_frame
        
    def create_labeled_entry(self, parent, label_text, attr_name, row):
        tk.Label(parent, 
                text=label_text,
                bg=self.card_color,
                fg=self.text_color,
                font=('Arial', 10)).grid(row=row, column=0, sticky='w', pady=8)
        
        entry = tk.Entry(parent, 
                        width=40,
                        bg='#1e1e1e',
                        fg=self.text_color,
                        insertbackground=self.text_color,
                        relief='flat')
        entry.grid(row=row, column=1, sticky='ew', pady=8, padx=10)
        setattr(self, attr_name, entry)
        
        parent.columnconfigure(1, weight=1)
        
    def upload_icon(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.ico")]
        )
        if file_path:
            self.icon_path.set(file_path)
            self.icon_preview_label.config(text=os.path.basename(file_path))
            
    def upload_code(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        if file_path:
            self.code_path.set(file_path)
            self.code_label.config(text=os.path.basename(file_path))
            
    def upload_req(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.req_path.set(file_path)
            self.req_label.config(text=os.path.basename(file_path))
            
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def start_create_appimage(self):
        thread = threading.Thread(target=self.create_appimage)
        thread.daemon = True
        thread.start()
        
    def create_appimage(self):
        try:
            self.progress.start()
            self.status_var.set("Building AppImage...")
            
            app_name = self.app_name.get().strip()
            version = self.version.get().strip()
            description = self.description.get().strip()
            icon_path = self.icon_path.get()
            code_path = self.code_path.get()
            req_path = self.req_path.get()

            if not all([app_name, version, description, icon_path, code_path]):
                messagebox.showerror("Error", "All fields except Requirements are required!")
                return

            self.log("Starting AppImage creation process...")
            self.log(f"App: {app_name} v{version}")
            
            with tempfile.TemporaryDirectory() as temp_dir:
                self.log("Created temporary directory")
                
                # Create virtual environment for dependencies
                venv_dir = os.path.join(temp_dir, "venv")
                self.log("Creating virtual environment...")
                venv.create(venv_dir, with_pip=True)
                pip_exe = os.path.join(venv_dir, "bin", "pip")

                # Install requirements if provided
                if req_path and os.path.exists(req_path):
                    self.log("Installing requirements...")
                    subprocess.run([pip_exe, "install", "-r", req_path], check=True, capture_output=True)

                # Install PyInstaller in venv
                self.log("Installing PyInstaller...")
                subprocess.run([pip_exe, "install", "pyinstaller"], check=True, capture_output=True)

                # Run PyInstaller with activated venv
                dist_dir = os.path.join(temp_dir, "dist")
                os.makedirs(dist_dir, exist_ok=True)
                
                exe_name = os.path.splitext(os.path.basename(code_path))[0]
                self.log(f"Building executable with PyInstaller...")
                
                activate_cmd = f"source {venv_dir}/bin/activate && pyinstaller --onefile --distpath {dist_dir} {code_path}"
                subprocess.run(["bash", "-c", activate_cmd], check=True, capture_output=True)

                # Create AppDir structure
                self.log("Creating AppDir structure...")
                app_dir = os.path.join(temp_dir, "AppDir")
                os.makedirs(app_dir)
                usr_dir = os.path.join(app_dir, "usr", "bin")
                os.makedirs(usr_dir)

                exe_path = os.path.join(dist_dir, exe_name)
                shutil.move(exe_path, os.path.join(usr_dir, app_name))

                # Copy icon
                self.log("Copying icon...")
                icon_dest = os.path.join(app_dir, f"{app_name}.png")
                shutil.copy(icon_path, icon_dest)

                # Create AppRun script
                self.log("Creating AppRun script...")
                apprun_content = f"""#!/bin/bash
export APPDIR="$(dirname "$(readlink -f "$0")")"
export PATH="$APPDIR/usr/bin:$PATH"
exec "$APPDIR/usr/bin/{app_name}" "$@"
"""
                with open(os.path.join(app_dir, "AppRun"), "w") as f:
                    f.write(apprun_content)
                os.chmod(os.path.join(app_dir, "AppRun"), 0o755)

                # Create desktop file
                self.log("Creating desktop file...")
                desktop_content = f"""[Desktop Entry]
Name={app_name}
Exec=AppRun
Icon={app_name}
Type=Application
Categories=Utility;
Comment={description}
Version={version}
"""
                with open(os.path.join(app_dir, f"{app_name}.desktop"), "w") as f:
                    f.write(desktop_content)

                # Download appimagetool if not present
                appimagetool_path = "/tmp/appimagetool"
                if not os.path.exists(appimagetool_path):
                    self.log("Downloading appimagetool...")
                    urllib.request.urlretrieve(
                        "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage", 
                        appimagetool_path
                    )
                    os.chmod(appimagetool_path, 0o755)

                # Build AppImage
                self.log("Building AppImage...")
                output_path = os.path.join(os.getcwd(), f"{app_name}-{version}.AppImage")
                subprocess.run([appimagetool_path, app_dir, output_path], check=True, capture_output=True)

            self.log("✓ AppImage creation completed successfully!")
            self.status_var.set(f"AppImage created: {output_path}")
            messagebox.showinfo("Success", f"AppImage created:\n{output_path}")
            
        except subprocess.CalledProcessError as e:
            self.log(f"✗ Error during build process: {e}")
            messagebox.showerror("Build Error", f"Error during build process:\n{str(e)}")
        except Exception as e:
            self.log(f"✗ Unexpected error: {e}")
            messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")
        finally:
            self.progress.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernAppImageIDE(root)
    root.mainloop()