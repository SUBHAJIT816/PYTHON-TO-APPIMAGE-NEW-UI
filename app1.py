import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
import os
import subprocess
import shutil
import urllib.request
import tempfile
import venv
import platform
import threading

class AppImageIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("AppImage Maker Pro - Advanced IDE")
        self.root.geometry("700x850") # Ektu boro kora hoyeche terminaler jonno
        self.root.configure(bg="#1e1e2e")

        # Custom Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure("TFrame", background="#1e1e2e")
        self.style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 10))
        self.style.configure("Header.TLabel", background="#1e1e2e", foreground="#89b4fa", font=("Segoe UI", 16, "bold"))
        self.style.configure("TEntry", fieldbackground="#313244", foreground="white", borderwidth=0)
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), borderwidth=0, focuscolor='none')
        self.style.map("TButton", background=[('active', '#b4befe'), ('!active', '#89b4fa')])
        
        # Main Container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Section
        self.header = ttk.Label(self.main_frame, text="🚀 AppImage Maker Pro", style="Header.TLabel")
        self.header.pack(pady=(0, 10))

        # --- Application Info Section ---
        self.info_frame = tk.LabelFrame(self.main_frame, text=" Application Details ", bg="#1e1e2e", fg="#fab387", font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.info_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.info_frame, text="App Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.app_name = ttk.Entry(self.info_frame, width=55)
        self.app_name.grid(row=0, column=1, pady=5, padx=5)

        ttk.Label(self.info_frame, text="Version:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.version = ttk.Entry(self.info_frame, width=55)
        self.version.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(self.info_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.description = ttk.Entry(self.info_frame, width=55)
        self.description.grid(row=2, column=1, pady=5, padx=5)

        # --- Assets Section ---
        self.assets_frame = tk.LabelFrame(self.main_frame, text=" Files & Assets ", bg="#1e1e2e", fg="#fab387", font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        self.assets_frame.pack(fill=tk.X, pady=5)

        self.icon_path = tk.StringVar(value="No file selected")
        ttk.Button(self.assets_frame, text="📁 Upload Icon", command=self.upload_icon).grid(row=0, column=0, pady=5, sticky=tk.W)
        ttk.Label(self.assets_frame, textvariable=self.icon_path, font=("Segoe UI", 8), foreground="#a6adc8").grid(row=0, column=1, padx=10, sticky=tk.W)

        self.code_path = tk.StringVar(value="No file selected")
        ttk.Button(self.assets_frame, text="🐍 Upload Code", command=self.upload_code).grid(row=1, column=0, pady=5, sticky=tk.W)
        ttk.Label(self.assets_frame, textvariable=self.code_path, font=("Segoe UI", 8), foreground="#a6adc8").grid(row=1, column=1, padx=10, sticky=tk.W)

        self.req_path = tk.StringVar(value="Optional (.txt)")
        ttk.Button(self.assets_frame, text="📄 Requirements", command=self.upload_req).grid(row=2, column=0, pady=5, sticky=tk.W)
        ttk.Label(self.assets_frame, textvariable=self.req_path, font=("Segoe UI", 8), foreground="#a6adc8").grid(row=2, column=1, padx=10, sticky=tk.W)

        # --- Terminal Section ---
        ttk.Label(self.main_frame, text="Terminal Output:", font=("Segoe UI", 9, "bold"), foreground="#94e2d5").pack(anchor=tk.W, pady=(10, 0))
        self.terminal = ScrolledText(self.main_frame, height=12, bg="#11111b", fg="#a6e3a1", font=("Courier New", 10), borderwidth=0)
        self.terminal.pack(fill=tk.BOTH, expand=True, pady=5)
        self.terminal.insert(tk.END, "Welcome to AppImage Maker Pro Terminal...\n")
        self.terminal.configure(state='disabled')

        # --- Action Section ---
        self.build_btn = tk.Button(self.main_frame, text="BUILD APPIMAGE", command=self.start_build_thread, 
                                   bg="#a6e3a1", fg="#11111b", font=("Segoe UI", 12, "bold"), 
                                   activebackground="#94e2d5", cursor="hand2", bd=0, pady=10)
        self.build_btn.pack(fill=tk.X, pady=(10, 0))

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#313244", fg="#cdd6f4", font=("Segoe UI", 8))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def log(self, text):
        """Terminal-e message add korar helper function."""
        self.terminal.configure(state='normal')
        self.terminal.insert(tk.END, text + "\n")
        self.terminal.see(tk.END)
        self.terminal.configure(state='disabled')
        self.root.update_idletasks()

    def _get_path_linux(self, title, filetypes=None):
        if platform.system() == "Linux":
            try:
                cmd = ["zenity", "--file-selection", f"--title={title}"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            except FileNotFoundError:
                pass
        return filedialog.askopenfilename(title=title, filetypes=filetypes)

    def upload_icon(self):
        file_path = self._get_path_linux("Select Icon", [("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.icon_path.set(os.path.basename(file_path))
            self._full_icon_path = file_path

    def upload_code(self):
        file_path = self._get_path_linux("Select Python Code", [("Python files", "*.py")])
        if file_path:
            self.code_path.set(os.path.basename(file_path))
            self._full_code_path = file_path

    def upload_req(self):
        file_path = self._get_path_linux("Select Requirements File", [("Text files", "*.txt")])
        if file_path:
            self.req_path.set(os.path.basename(file_path))
            self._full_req_path = file_path

    def start_build_thread(self):
        """Main UI thread jano freeze na hoy tai threading use kora hoyeche."""
        thread = threading.Thread(target=self.create_appimage)
        thread.start()

    def run_command(self, cmd, shell=False):
        """Command run kora ebong terminal-e real-time output dekhano."""
        self.log(f"> Executing: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                   text=True, shell=shell, bufsize=1, universal_newlines=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.log(output.strip())
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, cmd)

    def create_appimage(self):
        app_name = self.app_name.get().strip()
        version = self.version.get().strip()
        description = self.description.get().strip()
        
        if not all([app_name, version, description]) or "No file" in self.icon_path.get() or "No file" in self.code_path.get():
            messagebox.showwarning("Incomplete Data", "Please fill all fields!")
            return

        self.build_btn.config(state='disabled', bg="#313244")
        self.status_var.set("Building...")
        self.terminal.configure(state='normal')
        self.terminal.delete('1.0', tk.END)
        self.terminal.configure(state='disabled')
        self.log("--- STARTING BUILD PROCESS ---")

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Venv Setup
                self.log("Setting up virtual environment...")
                venv_dir = os.path.join(temp_dir, "venv")
                venv.create(venv_dir, with_pip=True)
                pip_exe = os.path.join(venv_dir, "bin", "pip")

                if hasattr(self, '_full_req_path'):
                    self.log("Installing requirements...")
                    self.run_command([pip_exe, "install", "-r", self._full_req_path])

                self.log("Installing PyInstaller...")
                self.run_command([pip_exe, "install", "pyinstaller"])

                # PyInstaller Build
                self.log("Running PyInstaller...")
                dist_dir = os.path.join(temp_dir, "dist")
                os.makedirs(dist_dir, exist_ok=True)
                activate_cmd = f"source {venv_dir}/bin/activate && pyinstaller --onefile --distpath {dist_dir} {self._full_code_path}"
                self.run_command(["bash", "-c", activate_cmd])

                # Packaging
                self.log("Structuring AppDir...")
                app_dir = os.path.join(temp_dir, "AppDir")
                os.makedirs(app_dir)
                usr_dir = os.path.join(app_dir, "usr", "bin")
                os.makedirs(usr_dir)

                exe_name = os.path.splitext(os.path.basename(self._full_code_path))[0]
                shutil.move(os.path.join(dist_dir, exe_name), os.path.join(usr_dir, app_name))
                shutil.copy(self._full_icon_path, os.path.join(app_dir, f"{app_name}.png"))

                with open(os.path.join(app_dir, "AppRun"), "w") as f:
                    f.write(f"#!/bin/bash\nexport APPDIR=\"$(dirname \"$(readlink -f \"$0\")\")\"\nexec \"$APPDIR/usr/bin/{app_name}\" \"$@\"\n")
                os.chmod(os.path.join(app_dir, "AppRun"), 0o755)

                desktop_content = f"[Desktop Entry]\nName={app_name}\nExec=AppRun\nIcon={app_name}\nType=Application\nComment={description}\n"
                with open(os.path.join(app_dir, f"{app_name}.desktop"), "w") as f:
                    f.write(desktop_content)

                # AppImage Tool
                appimagetool_path = "/tmp/appimagetool"
                if not os.path.exists(appimagetool_path):
                    self.log("Downloading appimagetool...")
                    urllib.request.urlretrieve("https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage", appimagetool_path)
                    os.chmod(appimagetool_path, 0o755)

                self.log("Finalizing AppImage...")
                output_path = os.path.join(os.getcwd(), f"{app_name}-{version}.AppImage")
                self.run_command([appimagetool_path, app_dir, output_path])

            self.log(f"SUCCESS: AppImage saved at {output_path}")
            self.status_var.set("Done!")
            messagebox.showinfo("Success", f"Build Complete!\n{output_path}")
            
        except Exception as e:
            self.log(f"CRITICAL ERROR: {str(e)}")
            self.status_var.set("Error!")
            messagebox.showerror("Error", f"Build Failed: {str(e)}")
        finally:
            self.build_btn.config(state='normal', bg="#a6e3a1")

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    app = AppImageIDE(root)
    root.mainloop()
